#!/usr/bin/env python3
"""Stage R runtime-confined loop tick.

PR 1 intentionally implements only the runtime boundary and a no-op tick:
no GitHub access, no worker, no reviewer, no promotion, and no tracked writes.
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


class RuntimeBoundaryError(RuntimeError):
    """Raised when a Stage R tick would write outside runtime confinement."""


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


@dataclass(frozen=True)
class NoopArtifacts:
    input: dict[str, Any]
    decision: str
    result: dict[str, Any]


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


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run one Stage R runtime-confined no-op tick."
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
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        summary = run_noop_tick(Path(args.repo_root), run_id=args.run_id)
    except RuntimeBoundaryError as exc:
        payload = {
            "stage": "R",
            "status": "error",
            "selected_issue": None,
            "outcome": "runtime_boundary_violation",
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
        print(f"Stage R no-op tick wrote {summary['run_dir']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
