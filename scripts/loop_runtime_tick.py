#!/usr/bin/env python3
"""Stage R runtime-confined loop tick.

The tick is intentionally conservative: it may read GitHub Issues through `gh`,
write candidate artifacts under `.self-evo/runtime/**`, and perform an advisory
runtime review. It never writes GitHub state or tracked repository files.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import datetime as dt
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_REL = Path(".self-evo/runtime")
RUNS_REL = RUNTIME_REL / "runs"
RUN_ID_RE = re.compile(r"^[A-Za-z0-9_.-]+$")
ISSUE_JSON_FIELDS = "number,title,url,labels,state,body,updatedAt,assignees"


class RuntimeBoundaryError(RuntimeError):
    """Raised when a Stage R tick would write outside runtime confinement."""


class IssueFetchError(RuntimeError):
    """Raised when read-only GitHub issue fetch fails."""


@dataclass(frozen=True)
class CommandResult:
    stdout: str
    stderr: str
    returncode: int


@dataclass(frozen=True)
class PatchCheck:
    applicable: bool
    status: str
    detail: str


@dataclass(frozen=True)
class NoopArtifacts:
    input: dict[str, Any]
    decision: str
    result: dict[str, Any]


@dataclass(frozen=True)
class WorkArtifacts:
    input: dict[str, Any]
    decision: str
    work: str
    evidence: str
    patch: str
    review: str
    result: dict[str, Any]


@dataclass(frozen=True)
class ErrorArtifacts:
    input: dict[str, Any]
    decision: str
    result: dict[str, Any]


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.UTC).replace(microsecond=0)


def format_run_id(now: dt.datetime) -> str:
    return now.astimezone(dt.UTC).strftime("%Y-%m-%dT%H-%M-%SZ")


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def git_ignores_runtime(repo_root: Path) -> bool:
    """Return whether Git ignores the runtime root in this checkout."""
    try:
        proc = subprocess.run(
            ["git", "check-ignore", "-q", "--no-index", str(RUNTIME_REL) + "/"],
            cwd=repo_root,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return proc.returncode == 0


def runtime_has_tracked_files(repo_root: Path) -> bool:
    """Return whether Git already tracks anything under runtime."""
    try:
        proc = subprocess.run(
            ["git", "ls-files", "-z", "--", str(RUNTIME_REL)],
            cwd=repo_root,
            capture_output=True,
            text=False,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return proc.returncode == 0 and bool(proc.stdout)


def tracked_worktree_changes(repo_root: Path) -> list[str]:
    """Return non-ignored working-tree paths for the real checkout."""
    try:
        proc = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=all"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return []
    if proc.returncode != 0:
        return []
    paths: list[str] = []
    for line in proc.stdout.splitlines():
        if len(line) >= 4:
            paths.append(line[3:])
    return sorted(paths)


def reject_existing_symlink_components(repo_root: Path, rel_path: Path) -> None:
    """Reject existing symlinks along a repo-relative path before writing."""
    current = repo_root
    for part in rel_path.parts:
        current = current / part
        if current.exists() and current.is_symlink():
            raise RuntimeBoundaryError(f"runtime path component is a symlink: {current}")


def require_runtime_ignored(repo_root: Path) -> None:
    if runtime_has_tracked_files(repo_root):
        raise RuntimeBoundaryError(
            ".self-evo/runtime/ contains tracked files; refusing runtime writes"
        )
    if not git_ignores_runtime(repo_root):
        raise RuntimeBoundaryError(
            ".self-evo/runtime/ must be ignored by Git before Stage R can run"
        )
    reject_existing_symlink_components(repo_root, RUNTIME_REL)


def validate_run_id(run_id: str) -> None:
    if not RUN_ID_RE.fullmatch(run_id):
        raise RuntimeBoundaryError(
            "run_id may contain only letters, numbers, underscore, dot, and dash"
        )


def run_command(cmd: list[str], *, cwd: Path, timeout: int) -> CommandResult:
    try:
        proc = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return CommandResult("", str(exc), 1)
    return CommandResult(proc.stdout or "", proc.stderr or "", proc.returncode)


def issue_label_names(issue: dict[str, Any]) -> list[str]:
    return [
        str(label.get("name", ""))
        for label in issue.get("labels", [])
        if isinstance(label, dict) and label.get("name")
    ]


def compact_issue(issue: dict[str, Any]) -> dict[str, Any]:
    body = str(issue.get("body") or "")
    return {
        "number": issue.get("number"),
        "title": issue.get("title"),
        "url": issue.get("url"),
        "state": issue.get("state"),
        "labels": issue_label_names(issue),
        "updatedAt": issue.get("updatedAt"),
        "body_excerpt": body[:800],
    }


def build_gh_issue_list_command(*, labels: list[str], limit: int) -> list[str]:
    cmd = [
        "gh",
        "issue",
        "list",
        "--state",
        "open",
        "--limit",
        str(limit),
        "--json",
        ISSUE_JSON_FIELDS,
    ]
    for label in labels:
        cmd.extend(["--label", label])
    return cmd


def fetch_open_issues(repo_root: Path, *, labels: list[str], limit: int) -> list[dict[str, Any]]:
    result = run_command(
        build_gh_issue_list_command(labels=labels, limit=limit),
        cwd=repo_root,
        timeout=20,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "gh issue list failed").strip()
        raise IssueFetchError(detail)
    try:
        payload = json.loads(result.stdout)
    except ValueError as exc:
        raise IssueFetchError(f"could not parse gh issue list JSON: {exc}") from exc
    if not isinstance(payload, list):
        raise IssueFetchError("gh issue list returned non-list JSON")
    return [issue for issue in payload if isinstance(issue, dict)]


# Status labels that mark an issue as actively claimed by another worker.
# Per rules/TASK_POLICY.md ("If an issue already has an active claim, do not
# work on it unless the lease has expired."), Stage R must not pick these up.
# GitHub labels + assignees are the authoritative source; state/claims/ is only
# a coordination mirror, so claim awareness is based on issue fields alone.
ACTIVE_CLAIM_LABELS = frozenset(
    {"status:claimed", "status:running", "status:blocked"}
)


def _has_active_claim(issue: dict[str, Any], labels: set[str]) -> bool:
    if labels & ACTIVE_CLAIM_LABELS:
        return True
    assignees = issue.get("assignees")
    return bool(assignees)


def select_issue(issues: list[dict[str, Any]]) -> dict[str, Any] | None:
    for issue in issues:
        if str(issue.get("state", "")).upper() != "OPEN":
            continue
        labels = {name.lower() for name in issue_label_names(issue)}
        if "in review" in labels or "status:review" in labels:
            continue
        if _has_active_claim(issue, labels):
            continue
        if not issue.get("number") or not issue.get("title"):
            continue
        return issue
    return None


def check_patch_applicability(repo_root: Path, patch_path: Path) -> PatchCheck:
    try:
        patch_text = patch_path.read_text(encoding="utf-8")
    except OSError as exc:
        return PatchCheck(False, "patch_read_failed", str(exc))
    if not patch_text.strip():
        return PatchCheck(False, "empty_patch", "proposed.patch is empty")
    unsafe = unsafe_patch_paths(patch_text)
    if unsafe:
        return PatchCheck(
            False,
            "unsafe_patch_path",
            "patch contains unsafe paths: " + ", ".join(unsafe),
        )
    result = run_command(
        ["git", "apply", "--check", str(patch_path)],
        cwd=repo_root,
        timeout=20,
    )
    detail = (result.stderr or result.stdout).strip()
    if result.returncode == 0:
        return PatchCheck(True, "applicable", detail or "git apply --check passed")
    return PatchCheck(False, "not_applicable", detail or "git apply --check failed")


def unsafe_patch_paths(patch_text: str) -> list[str]:
    paths: list[str] = []
    for line in patch_text.splitlines():
        if line.startswith("diff --git "):
            parts = line.split()
            paths.extend(parts[2:4])
        elif line.startswith("--- ") or line.startswith("+++ "):
            path = line[4:].split("\t", 1)[0].strip()
            if path != "/dev/null":
                paths.append(path)

    unsafe: list[str] = []
    for path in paths:
        clean = path
        if clean.startswith(("a/", "b/")):
            clean = clean[2:]
        p = Path(clean)
        if p.is_absolute() or ".." in p.parts:
            unsafe.append(path)
    return sorted(set(unsafe))


class RuntimeWriter:
    """Write only under `.self-evo/runtime/**` for one Stage R run."""

    def __init__(self, repo_root: Path, run_id: str):
        self.repo_root = repo_root.resolve()
        validate_run_id(run_id)
        reject_existing_symlink_components(self.repo_root, RUNTIME_REL)
        self.runtime_root = (self.repo_root / RUNTIME_REL).resolve()
        self.run_dir = (self.repo_root / RUNS_REL / run_id).resolve()
        self.run_id = run_id
        self._ensure_inside_runtime(self.run_dir)
        if self.run_dir.exists():
            raise RuntimeBoundaryError(f"runtime run already exists: {self.run_dir}")

    def _ensure_inside_runtime(self, path: Path) -> None:
        resolved = path.resolve(strict=False)
        if not _is_relative_to(resolved, self.runtime_root):
            raise RuntimeBoundaryError(
                f"refusing to write outside {RUNTIME_REL}: {path}"
            )

    def write_text(self, relative_path: str | Path, text: str) -> Path:
        target = self.run_dir / relative_path
        self._ensure_inside_runtime(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        return target

    def write_json(self, relative_path: str | Path, payload: dict[str, Any]) -> Path:
        text = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        return self.write_text(relative_path, text)


def build_noop_artifacts(
    *,
    run_id: str,
    started_at: str,
    finished_at: str,
) -> "NoopArtifacts":
    input_payload = {
        "run_id": run_id,
        "stage": "R",
        "mode": "noop",
        "fetched_at": started_at,
        "github": {
            "mode": "not_implemented_in_pr1",
            "issues": [],
            "prs": [],
        },
        "notes": [
            "PR 1 only verifies the runtime boundary and no-op artifact contract.",
            "GitHub read-only issue selection is deferred to PR 2.",
        ],
    }

    decision_md = "\n".join(
        [
            "# Stage R Decision",
            "",
            f"- run_id: `{run_id}`",
            "- decision: no-op",
            "- outcome: `no_suitable_issue`",
            "",
            "This PR 1 tick intentionally does not fetch GitHub issues or select work.",
            "It only proves that Stage R can create a gitignored runtime run directory",
            "and write the required no-op artifacts without touching tracked files.",
            "",
        ]
    )

    result_payload = {
        "run_id": run_id,
        "stage": "R",
        "status": "noop",
        "selected_issue": None,
        "outcome": "no_suitable_issue",
        "artifacts": {
            "input": "input.json",
            "decision": "decision.md",
            "result": "result.json",
        },
        "review_verdict": None,
        "budget": {
            "spent_usd": 0.0,
            "limit_usd": 0.0,
        },
        "started_at": started_at,
        "finished_at": finished_at,
        "error": None,
    }
    return NoopArtifacts(
        input=input_payload,
        decision=decision_md,
        result=result_payload,
    )


def run_noop_tick(repo_root: Path, *, run_id: str | None = None) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    require_runtime_ignored(repo_root)

    started = utc_now()
    resolved_run_id = run_id or format_run_id(started)
    validate_run_id(resolved_run_id)

    artifacts = build_noop_artifacts(
        run_id=resolved_run_id,
        started_at=started.isoformat().replace("+00:00", "Z"),
        finished_at=started.isoformat().replace("+00:00", "Z"),
    )
    writer = RuntimeWriter(repo_root, resolved_run_id)
    writer.write_json("input.json", artifacts.input)
    writer.write_text("decision.md", artifacts.decision)
    finished = utc_now()
    final_result = dict(artifacts.result)
    final_result["finished_at"] = finished.isoformat().replace("+00:00", "Z")
    writer.write_json("result.json", final_result)

    return {
        "run_id": resolved_run_id,
        "run_dir": str(writer.run_dir.relative_to(repo_root)),
        "result": final_result,
    }


def build_fetch_error_artifacts(
    *,
    run_id: str,
    started_at: str,
    finished_at: str,
    labels: list[str],
    limit: int,
    error: str,
) -> ErrorArtifacts:
    input_payload = {
        "run_id": run_id,
        "stage": "R",
        "mode": "github_read",
        "fetched_at": started_at,
        "github": {
            "mode": "read_only",
            "labels": labels,
            "limit": limit,
            "issues": [],
            "error": error,
        },
    }
    decision = "\n".join([
        "# Stage R Decision",
        "",
        f"- run_id: `{run_id}`",
        "- decision: fetch failed",
        "- outcome: `fetch_failed`",
        "",
        error,
        "",
    ])
    result = {
        "run_id": run_id,
        "stage": "R",
        "status": "error",
        "selected_issue": None,
        "outcome": "fetch_failed",
        "artifacts": {
            "input": "input.json",
            "decision": "decision.md",
            "result": "result.json",
        },
        "review_verdict": None,
        "budget": {"spent_usd": 0.0, "limit_usd": 0.0},
        "started_at": started_at,
        "finished_at": finished_at,
        "error": error,
    }
    return ErrorArtifacts(input=input_payload, decision=decision, result=result)


def build_no_issue_artifacts(
    *,
    run_id: str,
    started_at: str,
    finished_at: str,
    issues: list[dict[str, Any]],
    labels: list[str],
    limit: int,
) -> WorkArtifacts:
    compact_issues = [compact_issue(issue) for issue in issues]
    input_payload = {
        "run_id": run_id,
        "stage": "R",
        "mode": "github_read",
        "fetched_at": started_at,
        "github": {
            "mode": "read_only",
            "labels": labels,
            "limit": limit,
            "issues": compact_issues,
        },
        "selected_issue": None,
    }
    decision = "\n".join([
        "# Stage R Decision",
        "",
        f"- run_id: `{run_id}`",
        "- decision: no-op",
        "- outcome: `no_suitable_issue`",
        f"- issues_considered: {len(compact_issues)}",
        "",
        "No open issue matched the Stage R selection constraints.",
        "",
    ])
    review = "\n".join([
        "# Runtime Review",
        "",
        "- disposition: `abstain`",
        "- review_scope: no-op decision",
        "- github_write_check: no GitHub write operations are part of this tick",
        "- tracked_write_check: runtime-only artifacts are expected",
        "- next_action: wait for a suitable issue or adjust selection labels",
        "",
    ])
    result = {
        "run_id": run_id,
        "stage": "R",
        "status": "noop",
        "selected_issue": None,
        "outcome": "no_suitable_issue",
        "artifacts": {
            "input": "input.json",
            "decision": "decision.md",
            "review": "review.md",
            "result": "result.json",
        },
        "review_verdict": "abstain",
        "budget": {"spent_usd": 0.0, "limit_usd": 0.0},
        "started_at": started_at,
        "finished_at": finished_at,
        "error": None,
    }
    return WorkArtifacts(input_payload, decision, "", "", "", review, result)


def build_issue_work_artifacts(
    *,
    run_id: str,
    started_at: str,
    finished_at: str,
    issues: list[dict[str, Any]],
    selected: dict[str, Any],
    labels: list[str],
    limit: int,
    patch_check: PatchCheck,
    patch_text: str,
    tracked_changes: list[str],
) -> WorkArtifacts:
    selected_compact = compact_issue(selected)
    input_payload = {
        "run_id": run_id,
        "stage": "R",
        "mode": "github_read",
        "fetched_at": started_at,
        "github": {
            "mode": "read_only",
            "labels": labels,
            "limit": limit,
            "issues": [compact_issue(issue) for issue in issues],
        },
        "selected_issue": selected_compact,
    }
    decision = "\n".join([
        "# Stage R Decision",
        "",
        f"- run_id: `{run_id}`",
        "- decision: selected one issue",
        f"- selected_issue: #{selected_compact['number']} {selected_compact['title']}",
        "- outcome: `needs_revision`",
        "",
        "The issue is suitable for a runtime-confined candidate pass. This PR 2",
        "deterministic worker writes analysis and review artifacts, but does not",
        "invent a code patch without an implementation agent.",
        "",
    ])
    work = "\n".join([
        "# Stage R Work",
        "",
        f"- issue: #{selected_compact['number']}",
        f"- title: {selected_compact['title']}",
        f"- url: {selected_compact['url']}",
        f"- labels: {', '.join(selected_compact['labels']) or '(none)'}",
        "",
        "## Candidate Direction",
        "",
        "A runtime-confined worker selected this issue and prepared the artifact",
        "set required for later implementation work. The deterministic PR 2 worker",
        "does not apply changes to the checkout and does not claim the issue is",
        "ready to promote.",
        "",
        "## Patch Status",
        "",
        f"- patch_check: `{patch_check.status}`",
        f"- applicable: `{str(patch_check.applicable).lower()}`",
        f"- detail: {patch_check.detail}",
        "",
    ])
    evidence = "\n".join([
        "# Stage R Evidence",
        "",
        "## GitHub Snapshot",
        "",
        f"- issue_number: {selected_compact['number']}",
        f"- issue_state: {selected_compact['state']}",
        f"- issue_url: {selected_compact['url']}",
        f"- labels: {', '.join(selected_compact['labels']) or '(none)'}",
        "",
        "## Runtime Boundary",
        "",
        "- GitHub operations: read-only `gh issue list`",
        "- Checkout writes: none expected outside `.self-evo/runtime/**`",
        f"- non_ignored_worktree_changes_observed: {tracked_changes}",
        "",
        "## Confidence",
        "",
        "- selection_confidence: medium",
        "- implementation_confidence: low until a real patch is produced",
        "",
    ])
    review_disposition = "approved" if patch_check.applicable else "needs_revision"
    review = "\n".join([
        "# Runtime Review",
        "",
        f"- disposition: `{review_disposition}`",
        f"- selected_issue: #{selected_compact['number']}",
        "- scope_check: selected one existing open issue",
        "- evidence_check: evidence records issue metadata and runtime boundary",
        f"- patch_check: `{patch_check.status}`",
        f"- git_apply_check: {patch_check.detail}",
        "- github_write_check: no GitHub write operations are part of this tick",
        "- tracked_write_check: worker artifacts are runtime-only",
        "- final_approval: human required; this review is advisory only",
        "",
        "## Next Action",
        "",
        "Produce a non-empty candidate patch in a future worker pass before promote.",
        "",
    ])
    outcome = "ready_for_promote" if patch_check.applicable else "needs_revision"
    result = {
        "run_id": run_id,
        "stage": "R",
        "status": "work",
        "selected_issue": {
            "number": selected_compact["number"],
            "url": selected_compact["url"],
            "title": selected_compact["title"],
        },
        "outcome": outcome,
        "artifacts": {
            "input": "input.json",
            "decision": "decision.md",
            "work": "work.md",
            "evidence": "evidence.md",
            "patch": "proposed.patch",
            "review": "review.md",
            "result": "result.json",
        },
        "review_verdict": review_disposition,
        "budget": {"spent_usd": 0.0, "limit_usd": 0.0},
        "started_at": started_at,
        "finished_at": finished_at,
        "error": None,
    }
    return WorkArtifacts(input_payload, decision, work, evidence, patch_text, review, result)


def write_artifacts(writer: RuntimeWriter, artifacts: WorkArtifacts | ErrorArtifacts) -> dict[str, Any]:
    writer.write_json("input.json", artifacts.input)
    writer.write_text("decision.md", artifacts.decision)
    if isinstance(artifacts, WorkArtifacts):
        if artifacts.work:
            writer.write_text("work.md", artifacts.work)
        if artifacts.evidence:
            writer.write_text("evidence.md", artifacts.evidence)
        if artifacts.patch or artifacts.result["status"] == "work":
            writer.write_text("proposed.patch", artifacts.patch)
        if artifacts.review:
            writer.write_text("review.md", artifacts.review)
    writer.write_json("result.json", artifacts.result)
    return artifacts.result


def run_stage_r_tick(
    repo_root: Path,
    *,
    run_id: str | None = None,
    labels: list[str] | None = None,
    limit: int = 20,
    issue_fetcher: Any | None = None,
    project: str | None = None,
    # NOTE: the CLI (main()) does not expose this; real runs leave it empty, so
    # the patch check falls back to empty_patch and the outcome is always
    # `needs_revision`. `ready_for_promote` is only reached when a caller
    # (currently tests, or a future worker) injects a non-empty patch here.
    proposed_patch_text: str | None = None,
) -> dict[str, Any]:
    """Run a single advisory-only Stage R runtime tick.

    Reads open issues, picks at most one, writes runtime-only candidate
    artifacts under ``.self-evo/runtime/runs/<run_id>/``, and runs an advisory
    Runtime Review. Nothing canonical or on GitHub is mutated.

    If ``project`` is given, only issues carrying the ``project:<name>`` label
    are considered (translated to a ``--label project:<name>`` filter), so the
    tick works within a single project's issue pool instead of the global one.
    """
    repo_root = repo_root.resolve()
    require_runtime_ignored(repo_root)

    started = utc_now()
    resolved_run_id = run_id or format_run_id(started)
    validate_run_id(resolved_run_id)
    writer = RuntimeWriter(repo_root, resolved_run_id)
    label_filter = list(labels or [])
    if project:
        label_filter.append(f"project:{project}")
    fetcher = issue_fetcher or fetch_open_issues
    started_at = started.isoformat().replace("+00:00", "Z")

    try:
        issues = fetcher(repo_root, labels=label_filter, limit=limit)
    except IssueFetchError as exc:
        finished_at = utc_now().isoformat().replace("+00:00", "Z")
        artifacts = build_fetch_error_artifacts(
            run_id=resolved_run_id,
            started_at=started_at,
            finished_at=finished_at,
            labels=label_filter,
            limit=limit,
            error=str(exc),
        )
        result = write_artifacts(writer, artifacts)
        return {"run_id": resolved_run_id, "run_dir": str(writer.run_dir.relative_to(repo_root)), "result": result}

    selected = select_issue(issues)
    if not selected:
        finished_at = utc_now().isoformat().replace("+00:00", "Z")
        artifacts = build_no_issue_artifacts(
            run_id=resolved_run_id,
            started_at=started_at,
            finished_at=finished_at,
            issues=issues,
            labels=label_filter,
            limit=limit,
        )
        result = write_artifacts(writer, artifacts)
        return {"run_id": resolved_run_id, "run_dir": str(writer.run_dir.relative_to(repo_root)), "result": result}

    patch_text = proposed_patch_text or ""
    patch_path = writer.write_text("proposed.patch", patch_text)
    patch_check = check_patch_applicability(repo_root, patch_path)
    artifacts = build_issue_work_artifacts(
        run_id=resolved_run_id,
        started_at=started_at,
        finished_at=utc_now().isoformat().replace("+00:00", "Z"),
        issues=issues,
        selected=selected,
        labels=label_filter,
        limit=limit,
        patch_check=patch_check,
        patch_text=patch_text,
        tracked_changes=tracked_worktree_changes(repo_root),
    )
    result = write_artifacts(writer, artifacts)
    return {"run_id": resolved_run_id, "run_dir": str(writer.run_dir.relative_to(repo_root)), "result": result}


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run one Stage R runtime-confined tick: read open GitHub "
        "issues, write candidate runtime artifacts, and run an advisory "
        "Runtime Review. Does not modify canonical files or GitHub state."
    )
    parser.add_argument(
        "--repo-root",
        default=str(REPO_ROOT),
        help="repository root; defaults to this script's repository",
    )
    parser.add_argument(
        "--run-id",
        help="optional deterministic run id for tests or manual replay",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit machine-readable output",
    )
    parser.add_argument(
        "--offline-noop",
        action="store_true",
        help="run the PR 1 no-op contract without reading GitHub",
    )
    parser.add_argument(
        "--label",
        action="append",
        default=[],
        help="GitHub issue label filter; may be provided more than once",
    )
    parser.add_argument(
        "--project",
        help="restrict the tick to one project's issues by adding a "
        "`project:<name>` label filter (e.g. fx-strategy-research)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="maximum open issues to read through gh",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        if args.offline_noop:
            summary = run_noop_tick(Path(args.repo_root), run_id=args.run_id)
        else:
            summary = run_stage_r_tick(
                Path(args.repo_root),
                run_id=args.run_id,
                labels=args.label,
                limit=args.limit,
                project=args.project,
            )
    except (RuntimeBoundaryError, IssueFetchError) as exc:
        payload = {
            "stage": "R",
            "status": "error",
            "selected_issue": None,
            "outcome": "runtime_boundary_violation"
            if isinstance(exc, RuntimeBoundaryError) else "fetch_failed",
            "error": str(exc),
        }
        if args.json:
            print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
        else:
            print(f"Stage R tick blocked: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    else:
        print(f"Stage R tick wrote {summary['run_dir']}")
    return 1 if summary.get("result", {}).get("status") == "error" else 0


if __name__ == "__main__":
    sys.exit(main())
