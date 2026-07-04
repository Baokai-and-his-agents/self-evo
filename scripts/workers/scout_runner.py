#!/usr/bin/env python3
"""Autonomous Scout Runner — Stage A vertical slice.

Scouts approved public read-only sources (per data/exploration/scout-source-registry.schema.yaml),
dedupes by URL hash, applies a keep budget, and writes a decision-oriented daily report.

Design follows project conventions (see scripts/loop_runtime_tick.py):
- Explicit ScoutBoundaryError for hard limits.
- urllib.request with hard timeout for every external call.
- Frozen dataclasses for result types.
- Token/cost is recorded as 'unknown' when the fetch interface does not expose it
  (README Stage A: do not pretend to control what is not observable).

Boundaries enforced (README 阶段 A + blueprint 第 1094-1099 行):
- max_wall_clock_seconds: 总墙上时钟
- max_sources: 来源数量上限
- max_items_per_source: 每来源扫描上限
- max_items_kept: 保留项目总数
- max_retries_per_source: 单来源重试上限
- request_timeout_seconds: 单次 HTTP 超时
- 超时后保留部分结果,不抛异常丢失已抓内容

This runner only reads public sources approved under public-web-read scope.
It never writes GitHub state, never modifies tracked repository files.
Output is confined to data/exploration/ (daily report) and state/ (cursor).
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCES_FILE = REPO_ROOT / "data" / "exploration" / "scout-sources.yaml"
CURSOR_FILE = REPO_ROOT / "state" / "scout-cursor.json"
REPORT_DIR = REPO_ROOT / "data" / "exploration" / "daily_reports"
RESOURCE_APPROVALS_FILE = REPO_ROOT / "rules" / "RESOURCE_APPROVALS.yaml"

# urllib UA — identifies as research bot per schema access_mode public-web-read
USER_AGENT = "self-evo-scout/0.1 (+research bot, public read-only)"

# Allowed URL schemes — schema requires public HTTP(S) only.
ALLOWED_URL_SCHEMES = ("http://", "https://")

# Allowed access modes (from scout-source-registry.schema.yaml).
ALLOWED_ACCESS_MODES = ("public-web-read",)


class ScoutBoundaryError(RuntimeError):
    """Raised when a Scout run would breach a hard limit before producing any output."""


class SourceFetchError(RuntimeError):
    """Raised when a single source fails all retries."""


@dataclass(frozen=True)
class Boundaries:
    """Hard limits for a Scout run. Enforced before and during execution."""
    max_wall_clock_seconds: int = 600
    max_sources: int = 20
    max_items_per_source: int = 50
    max_items_kept: int = 80
    max_retries_per_source: int = 2
    request_timeout_seconds: int = 15


@dataclass(frozen=True)
class ScoutItem:
    """A single discovered item from a source."""
    source_id: str
    title: str
    url: str
    summary: str = ""
    timestamp: str = ""
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SourceResult:
    """Result of fetching one source."""
    source_id: str
    items: tuple[ScoutItem, ...]
    fetched: bool
    error: str = ""
    attempts: int = 0


@dataclass(frozen=True)
class ScoutRunReport:
    """Final report of a Scout run."""
    run_id: str
    started_at: str
    ended_at: str
    wall_clock_seconds: int
    sources_attempted: int
    sources_succeeded: int
    items_scanned: int
    items_kept: int
    duplicates_removed: int
    items: tuple[ScoutItem, ...]
    errors: tuple[str, ...]
    # Token/cost is explicitly unknown — fetch interface (urllib/gh) does not
    # expose model token usage. Recorded per README Stage A honesty rule.
    token_cost: str = "unknown"


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.UTC).replace(microsecond=0)


def format_run_id(now: dt.datetime) -> str:
    return now.astimezone(dt.UTC).strftime("%Y-%m-%dT%H-%M-%SZ")


def load_approved_scopes(approvals_path: Path = RESOURCE_APPROVALS_FILE) -> dict[str, set[str]]:
    """Load approved resource_id → scopes map from rules/RESOURCE_APPROVALS.yaml.

    Runner must verify each source's resource_approval_id is approved and that
    its required_scopes are a subset of the approved scopes (schema 第 109-112 行).
    """
    if not approvals_path.exists():
        return {}
    try:
        import yaml  # type: ignore
    except ImportError:
        # Without PyYAML we cannot validate approvals — fail closed (no sources).
        return {}
    try:
        data = yaml.safe_load(approvals_path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    if not isinstance(data, dict):
        return {}
    approved: dict[str, set[str]] = {}
    for res in data.get("resources", []) or []:
        if not isinstance(res, dict):
            continue
        if str(res.get("status", "")).lower() == "approved":
            rid = str(res.get("id", ""))
            scopes = res.get("scope", []) or []
            if rid:
                approved[rid] = {str(s) for s in scopes}
    return approved


def validate_source(source: dict[str, Any], approved: dict[str, set[str]]) -> list[str]:
    """Validate a source against schema + approval rules. Returns list of errors (empty = valid).

    Enforces (scout-source-registry.schema.yaml 第 100-135 行):
    - access_mode must be in allowed set (public-web-read)
    - resource_approval_id must exist in approved map with status approved
    - required_scopes must be subset of approved scopes
    - base_url must use public HTTP(S) scheme
    """
    errors: list[str] = []
    sid = str(source.get("id", "?"))
    access_mode = str(source.get("access_mode", ""))
    if access_mode not in ALLOWED_ACCESS_MODES:
        errors.append(f"{sid}: access_mode '{access_mode}' not in {ALLOWED_ACCESS_MODES}")
    base_url = str(source.get("base_url", ""))
    if not base_url.startswith(ALLOWED_URL_SCHEMES):
        errors.append(f"{sid}: base_url must be http(s), got '{base_url}'")
    approval_id = str(source.get("resource_approval_id", ""))
    if approval_id not in approved:
        errors.append(f"{sid}: resource_approval_id '{approval_id}' not approved (or rules/ unreadable)")
    else:
        required = {str(s) for s in (source.get("required_scopes", []) or [])}
        if not required:
            # schema 要求 minItems: 1,空 required_scopes 是 schema 绕过(Codex recheck)
            errors.append(f"{sid}: required_scopes must be non-empty (schema minItems: 1)")
        else:
            missing = required - approved[approval_id]
            if missing:
                errors.append(f"{sid}: required_scopes {sorted(missing)} not in approved scopes for '{approval_id}'")
    return errors


def load_sources(
    sources_path: Path = SOURCES_FILE,
    approvals_path: Path = RESOURCE_APPROVALS_FILE,
) -> list[dict[str, Any]]:
    """Load and validate scout sources.

    Requires PyYAML (the previous minimal parser was buggy and could silently
    return [] on valid files — see docs/REFACTOR-final-review-by-codex.md).
    Validates each source against schema + RESOURCE_APPROVALS before returning.
    Invalid sources are dropped with a stderr warning, not silently trusted.
    """
    if not sources_path.exists():
        raise ScoutBoundaryError(
            f"sources file not found: {sources_path}. "
            "Create data/exploration/scout-sources.yaml with source registry entries."
        )
    try:
        import yaml  # type: ignore
    except ImportError as e:
        raise ScoutBoundaryError(
            "PyYAML is required to load scout sources (the minimal fallback parser was "
            "removed — it silently failed on real registry files). Install with: pip install pyyaml"
        ) from e
    data = yaml.safe_load(sources_path.read_text(encoding="utf-8"))
    raw_sources = data.get("sources", []) if isinstance(data, dict) else []
    raw_sources = [s for s in raw_sources if s.get("enabled", True)]

    approved = load_approved_scopes(approvals_path)
    if not approved:
        # Fail closed: if we can't read approvals, we can't validate safety — refuse all.
        raise ScoutBoundaryError(
            f"no approved resources loaded from {approvals_path}; cannot validate sources. "
            "Ensure rules/RESOURCE_APPROVALS.yaml is readable and PyYAML is installed."
        )

    valid: list[dict[str, Any]] = []
    for src in raw_sources:
        errs = validate_source(src, approved)
        if errs:
            for e in errs:
                print(f"WARNING: dropping source: {e}", file=sys.stderr)
        else:
            valid.append(src)
    return valid


def load_cursor(cursor_path: Path = CURSOR_FILE) -> dict[str, Any]:
    """Load dedup cursor. Returns empty dict if absent (first run)."""
    if not cursor_path.exists():
        return {}
    try:
        return json.loads(cursor_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def save_cursor(cursor: dict[str, Any], cursor_path: Path = CURSOR_FILE) -> None:
    """Persist dedup cursor atomically."""
    cursor_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = cursor_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(cursor, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(cursor_path)


def url_hash(url: str) -> str:
    """Stable short hash for dedup. Not security-sensitive."""
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]


def dedupe(items: Iterable[ScoutItem], seen: set[str]) -> tuple[tuple[ScoutItem, ...], int]:
    """Dedupe by URL hash. Returns (kept, duplicates_removed)."""
    kept: list[ScoutItem] = []
    dups = 0
    for item in items:
        h = url_hash(item.url)
        if h in seen:
            dups += 1
            continue
        seen.add(h)
        kept.append(item)
    return tuple(kept), dups


def fetch_url(url: str, *, timeout: int) -> str:
    """Fetch URL content with hard timeout. Raises on HTTP error."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        if resp.status >= 400:
            raise urllib.error.HTTPError(url, resp.status, "HTTP error", resp.headers, None)
        return resp.read().decode("utf-8", errors="replace")


def fetch_with_retries(
    url: str, *, timeout: int, max_retries: int
) -> tuple[str, int]:
    """Fetch with bounded retries. Returns (content, attempts). Raises on final failure."""
    last_err: Exception | None = None
    for attempt in range(1, max_retries + 1):
        try:
            return fetch_url(url, timeout=timeout), attempt
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as e:
            last_err = e
    assert last_err is not None
    raise SourceFetchError(f"{url}: {last_err}") from last_err


def _localname(tag: str) -> str:
    """Strip XML namespace from a tag (ElementTree formats it as '{ns}local')."""
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def parse_rss_atom(content: str, source_id: str) -> tuple[ScoutItem, ...]:
    """Parse RSS/Atom XML into items. Namespace-agnostic and malformed-feed-safe."""
    items: list[ScoutItem] = []
    try:
        root = ET.fromstring(content)
    except ET.ParseError:
        return tuple(items)
    # Walk all descendants; branch on local name so namespace prefixes don't matter.
    for el in root.iter():
        if _localname(el.tag) != "entry" and _localname(el.tag) != "item":
            continue
        title = ""
        url = ""
        summary = ""
        for child in el:
            cname = _localname(child.tag)
            if cname == "title":
                title = (child.text or "").strip()
            elif cname == "link":
                # Atom <link href="..."/> vs RSS <link>text</link>
                url = child.get("href", "") or (child.text or "").strip()
            elif cname in ("summary", "description"):
                summary = (child.text or "").strip()[:300]
        if title and url:
            items.append(ScoutItem(source_id=source_id, title=title, url=url, summary=summary))
    return tuple(items)


def parse_json_items(content: str, source_id: str) -> tuple[ScoutItem, ...]:
    """Parse JSON API response. Handles dict-arrays and generic structures.

    Note: HN topstories returns a bare array of integer IDs, which cannot be
    turned into items without a second fetch — that is handled by a dedicated
    HN fetcher (fetch_hn_topstories), not here. A bare scalar array yields 0 items.
    """
    items: list[ScoutItem] = []
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        return tuple(items)
    arr = data if isinstance(data, list) else data.get("items") or data.get("data") or []
    if not isinstance(arr, list):
        return tuple(items)
    for el in arr[:50]:
        if not isinstance(el, dict):
            continue
        title = str(el.get("title") or el.get("name") or "").strip()
        url = str(el.get("url") or el.get("link") or "").strip()
        if not url and el.get("id"):
            url = f"{source_id}#{el['id']}"
        summary = str(el.get("summary") or el.get("description") or "")[:300].strip()
        if title and url:
            items.append(ScoutItem(source_id=source_id, title=title, url=url, summary=summary))
    return tuple(items)


def fetch_hn_topstories(
    base_url: str, source_id: str, *, timeout: int, max_items: int, deadline_ts: float | None
) -> tuple[ScoutItem, ...]:
    """Fetch HN topstories: list endpoint returns bare ID array, need 2nd-hop per-item fetch.

    Respects deadline_ts (absolute wall-clock seconds) for hard wall-clock enforcement —
    aborts the 2nd-hop loop early if budget exhausted, keeping partial results.
    """
    try:
        ids_text, _ = fetch_with_retries(base_url, timeout=timeout, max_retries=1)
        ids = json.loads(ids_text)
    except (SourceFetchError, json.JSONDecodeError, ValueError):
        return ()
    if not isinstance(ids, list):
        return ()
    items: list[ScoutItem] = []
    for item_id in ids[:max_items]:
        if deadline_ts is not None and utc_now().timestamp() >= deadline_ts:
            break  # hard wall clock — keep partial results
        # HN item endpoint: strip trailing /topstories.json, use /item/<id>.json
        api_root = base_url.rsplit("/topstories.json", 1)[0]
        item_url = f"{api_root}/item/{item_id}.json"
        try:
            body, _ = fetch_with_retries(item_url, timeout=timeout, max_retries=1)
            obj = json.loads(body)
        except (SourceFetchError, json.JSONDecodeError, ValueError):
            continue
        if not isinstance(obj, dict):
            continue
        title = str(obj.get("title") or "").strip()
        url = str(obj.get("url") or "").strip()
        if not url:
            url = f"https://news.ycombinator.com/item?id={item_id}"
        score = obj.get("score")
        summary = f"HN score: {score}" if score is not None else ""
        if title:
            items.append(ScoutItem(source_id=source_id, title=title, url=url, summary=summary))
    return tuple(items)


def fetch_source(
    source: dict[str, Any],
    boundaries: Boundaries,
    *,
    deadline_ts: float | None = None,
) -> SourceResult:
    """Fetch one source with retries. Returns SourceResult (never raises).

    deadline_ts: absolute wall-clock seconds; when set, the inner fetch loops
    (e.g. HN 2nd-hop) check it and abort early, keeping partial results. This
    makes the wall-clock boundary actually hard — previously a single source
    could overrun by timeout × retries.
    """
    sid = str(source.get("id", "unknown"))
    stype = str(source.get("type", "web"))
    base_url = str(source.get("base_url", ""))
    if not base_url:
        return SourceResult(source_id=sid, items=(), fetched=False, error="missing base_url")

    # Cap per-request timeout by remaining wall-clock budget so a single source
    # cannot overrun the hard deadline (Codex recheck: 普通来源也要尊重 deadline).
    effective_timeout = boundaries.request_timeout_seconds
    if deadline_ts is not None:
        remaining = deadline_ts - utc_now().timestamp()
        if remaining <= 0:
            return SourceResult(source_id=sid, items=(), fetched=False, error="wall clock exhausted before fetch")
        # Leave room for parsing; cap timeout to remaining seconds.
        effective_timeout = max(1, int(remaining))

    # HN topstories needs special 2-hop handling (list returns bare ID array).
    if "topstories.json" in base_url or "firebaseio.com" in base_url and "topstories" in base_url:
        try:
            items = fetch_hn_topstories(
                base_url, sid,
                timeout=effective_timeout,
                max_items=boundaries.max_items_per_source,
                deadline_ts=deadline_ts,
            )
            return SourceResult(source_id=sid, items=items, fetched=True, attempts=1)
        except Exception as e:
            return SourceResult(source_id=sid, items=(), fetched=False, error=f"HN fetch: {e}")

    try:
        content, attempts = fetch_with_retries(
            base_url,
            timeout=effective_timeout,
            max_retries=boundaries.max_retries_per_source,
        )
    except SourceFetchError as e:
        return SourceResult(source_id=sid, items=(), fetched=False, error=str(e), attempts=boundaries.max_retries_per_source)
    # Route by declared type. RSS/Atom XML via parse_rss_atom; JSON via parse_json_items.
    if stype in ("rss", "git"):
        items = parse_rss_atom(content, sid)
    elif stype == "api":
        items = parse_json_items(content, sid)
    else:  # web — best effort: extract <title> and <a href>
        items = _extract_web_links(content, sid)
    items = items[: boundaries.max_items_per_source]
    return SourceResult(source_id=sid, items=items, fetched=True, attempts=attempts)


def _extract_web_links(content: str, source_id: str) -> tuple[ScoutItem, ...]:
    """Minimal HTML link extraction for web-type sources."""
    items: list[ScoutItem] = []
    title_match = re.search(r"<title[^>]*>(.*?)</title>", content, re.IGNORECASE | re.DOTALL)
    page_title = title_match.group(1).strip() if title_match else source_id
    for m in re.finditer(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', content, re.IGNORECASE | re.DOTALL):
        url = m.group(1).strip()
        text = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        if url.startswith("http") and text and len(text) > 3:
            items.append(ScoutItem(source_id=source_id, title=text[:200], url=url, summary=f"from {page_title}"))
    return tuple(items)


def write_daily_report(report: ScoutRunReport, report_dir: Path = REPORT_DIR) -> Path:
    """Write a decision-oriented daily report (information → action candidates)."""
    report_dir.mkdir(parents=True, exist_ok=True)
    path = report_dir / f"{report.run_id}-scout.md"
    lines = [
        f"# Scout Daily Report — {report.run_id}",
        "",
        f"**运行时段:** {report.started_at} → {report.ended_at} ({report.wall_clock_seconds}s)",
        f"**来源:** 尝试 {report.sources_attempted},成功 {report.sources_succeeded}",
        f"**项目:** 扫描 {report.items_scanned},去重 {report.duplicates_removed},保留 {report.items_kept}",
        f"**Token/Cost:** {report.token_cost} (fetch 接口未暴露模型 token,如实标记)",
        "",
        "## 保留项目(决策候选)",
        "",
    ]
    if not report.items:
        lines.append("_(本次运行无新项目。可能原因:来源已全部抓取过、来源暂时无更新、或全部失败。)_")
    else:
        for i, item in enumerate(report.items, 1):
            lines.append(f"### {i}. {item.title}")
            lines.append(f"- **来源:** {item.source_id}")
            lines.append(f"- **链接:** {item.url}")
            if item.summary:
                lines.append(f"- **摘要:** {item.summary}")
            lines.append(f"- **下一步候选:** _(待人工 review 或 preference learner 标注)_")
            lines.append("")
    if report.errors:
        lines.append("## 失败来源")
        lines.append("")
        for err in report.errors:
            lines.append(f"- {err}")
        lines.append("")
    lines.append("## 决策建议")
    lines.append("")
    lines.append("_(此区块由人工填写。基于上方保留项目,选择 1-3 个进入 `type:learn` 或 `type:build` 任务。)_")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def run_scout(boundaries: Boundaries, sources_path: Path = SOURCES_FILE) -> ScoutRunReport:
    """Run a single Scout tick with hard boundary enforcement."""
    run_id = format_run_id(utc_now())
    started = utc_now()
    started_ts = started.timestamp()

    sources = load_sources(sources_path)
    if len(sources) > boundaries.max_sources:
        sources = sources[: boundaries.max_sources]

    cursor = load_cursor()
    seen: set[str] = set(cursor.get("seen_urls", []))
    all_items: list[ScoutItem] = []
    errors: list[str] = []
    sources_succeeded = 0

    # Hard wall-clock deadline (absolute timestamp). Passed into fetch_source so
    # its inner loops (e.g. HN 2nd-hop) also abort early, not just the per-source gate.
    deadline_ts = started_ts + boundaries.max_wall_clock_seconds

    for source in sources:
        # Per-source gate — stop early if budget exhausted, keep partial results.
        elapsed = utc_now().timestamp() - started_ts
        if elapsed >= boundaries.max_wall_clock_seconds:
            errors.append(f"wall clock budget exhausted at {int(elapsed)}s, stopped before {source.get('id', '?')}")
            break
        result = fetch_source(source, boundaries, deadline_ts=deadline_ts)
        if result.fetched:
            sources_succeeded += 1
            all_items.extend(result.items)
        else:
            errors.append(f"source {result.source_id}: {result.error}")

    scanned = len(all_items)
    # Keep budget FIRST, then update seen — otherwise over-budget items get
    # written into cursor and never appear again (Codex review bug #5).
    # Truncate before dedupe so seen only records URLs we actually kept.
    if len(all_items) > boundaries.max_items_kept:
        all_items = all_items[: boundaries.max_items_kept]
    kept, dups = dedupe(all_items, seen)

    ended = utc_now()
    wall = int(ended.timestamp() - started_ts)

    # Persist updated cursor for cross-run dedup.
    cursor["seen_urls"] = sorted(seen)
    cursor["last_run"] = ended.isoformat()
    cursor["total_kept"] = cursor.get("total_kept", 0) + len(kept)
    save_cursor(cursor)

    return ScoutRunReport(
        run_id=run_id,
        started_at=started.isoformat(),
        ended_at=ended.isoformat(),
        wall_clock_seconds=wall,
        sources_attempted=len(sources),
        sources_succeeded=sources_succeeded,
        items_scanned=scanned,
        items_kept=len(kept),
        duplicates_removed=dups,
        items=kept,
        errors=tuple(errors),
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Autonomous Scout Runner (Stage A)")
    p.add_argument("--max-wall-clock", type=int, default=600, help="总墙上时钟秒数 (default 600)")
    p.add_argument("--max-sources", type=int, default=20, help="来源数上限 (default 20)")
    p.add_argument("--max-items-per-source", type=int, default=50, help="每来源扫描上限 (default 50)")
    p.add_argument("--max-items-kept", type=int, default=80, help="保留项目总数 (default 80)")
    p.add_argument("--max-retries", type=int, default=2, help="单来源重试上限 (default 2)")
    p.add_argument("--request-timeout", type=int, default=15, help="单次 HTTP 超时秒 (default 15)")
    p.add_argument("--sources-file", type=str, default=None, help="覆盖默认 sources 路径")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    boundaries = Boundaries(
        max_wall_clock_seconds=args.max_wall_clock,
        max_sources=args.max_sources,
        max_items_per_source=args.max_items_per_source,
        max_items_kept=args.max_items_kept,
        max_retries_per_source=args.max_retries,
        request_timeout_seconds=args.request_timeout,
    )
    sources_path = Path(args.sources_file) if args.sources_file else SOURCES_FILE
    try:
        report = run_scout(boundaries, sources_path)
    except ScoutBoundaryError as e:
        print(f"BOUNDARY ERROR: {e}", file=sys.stderr)
        return 2
    path = write_daily_report(report)
    print(f"Scout run {report.run_id} complete.")
    print(f"  sources: {report.sources_succeeded}/{report.sources_attempted} succeeded")
    print(f"  items: {report.items_kept} kept ({report.duplicates_removed} dupes removed)")
    print(f"  wall clock: {report.wall_clock_seconds}s")
    print(f"  errors: {len(report.errors)}")
    print(f"  report: {path}")
    if report.errors:
        print(f"  token/cost: {report.token_cost}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
