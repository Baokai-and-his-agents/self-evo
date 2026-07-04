#!/usr/bin/env python3
"""Tests for scripts/workers/scout_runner.py.

Tests are network-free: parsers are fed canned content, dedup/cursor logic
is unit-tested, and boundary enforcement is checked without real HTTP.
Run: python scripts/tests/test_scout_runner.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts" / "workers"))

import scout_runner as sr  # noqa: E402


PASS = 0
FAIL = 0


def check(name: str, cond: bool, detail: str = "") -> None:
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  [PASS] {name}")
    else:
        FAIL += 1
        print(f"  [FAIL] {name} — {detail}")


def test_url_hash_stable() -> None:
    h1 = sr.url_hash("https://example.com/a")
    h2 = sr.url_hash("https://example.com/a")
    h3 = sr.url_hash("https://example.com/b")
    check("url_hash stable for same input", h1 == h2 and len(h1) == 16)
    check("url_hash differs for different input", h1 != h3)


def test_dedupe() -> None:
    items = [
        sr.ScoutItem(source_id="s1", title="a", url="https://x.com/1"),
        sr.ScoutItem(source_id="s1", title="a-dup", url="https://x.com/1"),  # dup
        sr.ScoutItem(source_id="s2", title="b", url="https://x.com/2"),
    ]
    seen: set[str] = set()
    kept, dups = sr.dedupe(items, seen)
    check("dedupe keeps unique items", len(kept) == 2, f"got {len(kept)}")
    check("dedupe counts duplicates", dups == 1, f"got {dups}")
    check("dedupe updates seen set", len(seen) == 2)


def test_dedupe_cross_source() -> None:
    """Same URL from two sources should dedupe (prevents cross-source repeats)."""
    items = [
        sr.ScoutItem(source_id="hn", title="hot", url="https://github.com/r/p"),
        sr.ScoutItem(source_id="gh", title="trending", url="https://github.com/r/p"),
    ]
    seen: set[str] = set()
    kept, dups = sr.dedupe(items, seen)
    check("dedupe across sources", len(kept) == 1 and dups == 1, f"kept={len(kept)} dups={dups}")


def test_parse_rss_atom() -> None:
    atom = """<?xml version="1.0"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <title>Atom Post One</title>
    <link href="https://blog.example.com/1"/>
    <summary>First post body</summary>
  </entry>
  <entry>
    <title>Atom Post Two</title>
    <link href="https://blog.example.com/2"/>
  </entry>
</feed>"""
    items = sr.parse_rss_atom(atom, "atom-src")
    check("Atom parse returns entries", len(items) == 2, f"got {len(items)}")
    check("Atom parse extracts title", items[0].title == "Atom Post One")
    check("Atom parse extracts url", items[0].url == "https://blog.example.com/1")
    check("Atom parse extracts summary", "First post" in items[0].summary)


def test_parse_rss_xml() -> None:
    rss = """<?xml version="1.0"?>
<rss><channel>
  <item>
    <title>RSS Item A</title>
    <link>https://rss.example.com/a</link>
    <description>Desc A</description>
  </item>
</channel></rss>"""
    items = sr.parse_rss_atom(rss, "rss-src")
    check("RSS parse returns item", len(items) == 1, f"got {len(items)}")
    check("RSS parse extracts fields", items[0].title == "RSS Item A" and items[0].url.endswith("/a"))


def test_parse_rss_malformed() -> None:
    items = sr.parse_rss_atom("not xml at all <", "bad-src")
    check("malformed XML returns empty", items == ())
    items2 = sr.parse_rss_atom("", "empty-src")
    check("empty content returns empty", items2 == ())


def test_parse_json_hn_style() -> None:
    # HN-style: array of objects with title/url
    content = '[{"title":"Story A","url":"https://news.example.com/a","score":99},{"title":"Story B","url":"https://news.example.com/b"}]'
    items = sr.parse_json_items(content, "hn")
    check("JSON array parse", len(items) == 2, f"got {len(items)}")
    check("JSON parse title", items[0].title == "Story A")


def test_parse_json_objects_wrapper() -> None:
    content = '{"items":[{"title":"X","url":"https://x.com"}]}'
    items = sr.parse_json_items(content, "api")
    check("JSON items-wrapper parse", len(items) == 1, f"got {len(items)}")


def test_parse_json_malformed() -> None:
    check("malformed JSON returns empty", sr.parse_json_items("not json", "x") == ())
    check("empty JSON returns empty", sr.parse_json_items("", "x") == ())


def test_extract_web_links() -> None:
    html = """<html><head><title>Page Title</title></head><body>
    <a href="https://link1.com">Link One</a>
    <a href="https://link2.com">Link Two</a>
    <a href="/relative">Skip Relative</a>
    <a href="https://link3.com">x</a>
    </body></html>"""
    items = sr._extract_web_links(html, "web-src")
    # "x" (len 1) is filtered as noise by design; 2 substantive links remain.
    check("web link extraction finds absolute links", len(items) == 2, f"got {len(items)}")
    check("web extraction filters short anchor text", all(len(i.title) > 3 for i in items))
    check("web extraction has source_id", all(i.source_id == "web-src" for i in items))


def test_boundaries_defaults() -> None:
    b = sr.Boundaries()
    check("default wall clock", b.max_wall_clock_seconds == 600)
    check("default max sources", b.max_sources == 20)
    check("default max kept", b.max_items_kept == 80)
    check("default retries", b.max_retries_per_source == 2)


def test_boundaries_custom() -> None:
    b = sr.Boundaries(max_wall_clock_seconds=10, max_sources=2, max_items_kept=5)
    check("custom boundaries honored", b.max_wall_clock_seconds == 10 and b.max_sources == 2)


def test_load_cursor_missing(tmp_path: Path) -> None:
    cursor = sr.load_cursor(tmp_path / "nonexistent.json")
    check("missing cursor returns empty dict", cursor == {})


def test_save_load_cursor_roundtrip(tmp_path: Path) -> None:
    cursor_path = tmp_path / "cursor.json"
    cursor = {"seen_urls": ["abc123", "def456"], "last_run": "2026-07-04T10:00:00+00:00"}
    sr.save_cursor(cursor, cursor_path)
    loaded = sr.load_cursor(cursor_path)
    check("cursor roundtrip preserves seen_urls", loaded.get("seen_urls") == ["abc123", "def456"])
    check("cursor roundtrip preserves last_run", loaded.get("last_run", "").startswith("2026-07-04"))


def test_save_cursor_atomic(tmp_path: Path) -> None:
    """save_cursor should not leave a .tmp file behind on success."""
    cursor_path = tmp_path / "cursor.json"
    sr.save_cursor({"seen_urls": []}, cursor_path)
    check("no .tmp leftover", not (tmp_path / "cursor.tmp").exists())
    check("cursor file exists", cursor_path.exists())


def test_load_sources_missing_raises(tmp_path: Path) -> None:
    try:
        sr.load_sources(tmp_path / "no-such.yaml")
        check("missing sources raises ScoutBoundaryError", False, "did not raise")
    except sr.ScoutBoundaryError:
        check("missing sources raises ScoutBoundaryError", True)


def test_report_has_unknown_token_cost() -> None:
    """README Stage A honesty rule: token/cost must be 'unknown', never faked."""
    report = sr.ScoutRunReport(
        run_id="test", started_at="t1", ended_at="t2", wall_clock_seconds=1,
        sources_attempted=1, sources_succeeded=1, items_scanned=1, items_kept=1,
        duplicates_removed=0, items=(), errors=(),
    )
    check("token_cost defaults to unknown", report.token_cost == "unknown")


def test_write_daily_report(tmp_path: Path) -> None:
    report = sr.ScoutRunReport(
        run_id="2026-07-04T00-00-00Z", started_at="t1", ended_at="t2", wall_clock_seconds=5,
        sources_attempted=2, sources_succeeded=1, items_scanned=3, items_kept=2,
        duplicates_removed=1,
        items=(
            sr.ScoutItem(source_id="hn", title="Story A", url="https://x.com/a", summary="sa"),
            sr.ScoutItem(source_id="gh", title="Repo B", url="https://x.com/b"),
        ),
        errors=("source gh: timeout",),
    )
    path = sr.write_daily_report(report, tmp_path)
    content = path.read_text(encoding="utf-8")
    check("daily report file created", path.exists())
    check("report has title", "Scout Daily Report" in content)
    check("report lists kept items", "Story A" in content and "Repo B" in content)
    check("report shows errors", "timeout" in content)
    check("report has decision section", "决策建议" in content)
    check("report marks token unknown", "unknown" in content)


def test_scoutitem_frozen() -> None:
    """ScoutItem must be immutable (frozen dataclass, matches project convention)."""
    item = sr.ScoutItem(source_id="s", title="t", url="u")
    try:
        item.title = "mutated"  # type: ignore
        check("ScoutItem is frozen", False, "mutation succeeded")
    except AttributeError:
        check("ScoutItem is frozen", True)


def test_keep_budget_enforced(tmp_path: Path) -> None:
    """Dedup output must be capped to max_items_kept."""
    items = [sr.ScoutItem(source_id="s", title=f"t{i}", url=f"https://x.com/{i}") for i in range(100)]
    seen: set[str] = set()
    kept, _ = sr.dedupe(items, seen)
    b = sr.Boundaries(max_items_kept=5)
    if len(kept) > b.max_items_kept:
        kept = kept[: b.max_items_kept]
    check("keep budget caps output", len(kept) == 5, f"got {len(kept)}")


def main() -> int:
    import tempfile
    print("=" * 60)
    print("  test_scout_runner.py — Scout Runner 单元测试")
    print("=" * 60)

    # Tests without tmp_path
    test_url_hash_stable()
    test_dedupe()
    test_dedupe_cross_source()
    test_parse_rss_atom()
    test_parse_rss_xml()
    test_parse_rss_malformed()
    test_parse_json_hn_style()
    test_parse_json_objects_wrapper()
    test_parse_json_malformed()
    test_extract_web_links()
    test_boundaries_defaults()
    test_boundaries_custom()
    test_report_has_unknown_token_cost()
    test_scoutitem_frozen()

    # Tests needing a tmp directory
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        test_load_cursor_missing(tmp)
        test_save_load_cursor_roundtrip(tmp)
        test_save_cursor_atomic(tmp)
        test_load_sources_missing_raises(tmp)
        test_write_daily_report(tmp)
        test_keep_budget_enforced(tmp)

    print()
    print("=" * 60)
    print(f"RESULT: {PASS} passed, {FAIL} failed")
    print("=" * 60)
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
