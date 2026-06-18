#!/usr/bin/env python3
"""Claude Code Stop lifecycle hook for self-evo (MVP 1.5, Issue #5).

Runs the lifecycle subset of the read-only validator and explains any
incomplete state. Behaviour by rollout mode:
  * audit / pretool-enforce -> never block Stop; only report.
  * full-enforce           -> block Stop (exit 2) when there are BLOCK
                              lifecycle findings, so the worker is forced to
                              fix them before ending the run.

Anti-loop protection (required by Issue #5): blocking Stop re-invokes this hook
after the worker responds, which can loop forever when a finding is not
worker-fixable (e.g. waiting on a human). We cap consecutive blocks at
policy.audit_log.stop_loop_block_limit (default 2) using a counter under
data/audit/ (an audit file, not task state), and we honour env
SELF_EVO_STOP_GUARD=1 as an unconditional escape hatch. The counter resets to 0
whenever a Stop check passes cleanly.
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _policy  # noqa: E402
import validate_run  # noqa: E402

REPO_ROOT = _policy.REPO_ROOT
GUARD_ENV = "SELF_EVO_STOP_GUARD"

# Only lifecycle-shaped checks make sense at Stop time (the worker is finishing).
STOP_CHECK_NAMES = {
    "run_summary_exists",
    "changed_files_have_draft_pr",
    "review_has_released_claim",
    "heartbeat_idle_before_review",
    "tasks_md_matches_issue",
    "no_unauthorized_rules_changes",
    "changed_files_within_authorized_paths",
}


def load_counter(policy: dict) -> int:
    rel = policy.get("audit_log", {}).get("stop_loop_counter_path",
                                          "data/audit/stop-loop.counter")
    try:
        with open(os.path.join(REPO_ROOT, rel), "r", encoding="utf-8") as fh:
            return int(fh.read().strip() or "0")
    except (OSError, ValueError):
        return 0


def save_counter(policy: dict, value: int) -> None:
    rel = policy.get("audit_log", {}).get("stop_loop_counter_path",
                                          "data/audit/stop-loop.counter")
    path = os.path.join(REPO_ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(str(value))


def lifecycle_findings(policy, issue_number: int, date_str: str) -> list[dict]:
    all_findings = validate_run.collect_findings(
        policy, issue_number=issue_number, date_str=date_str)
    # run_summary_exists is WARN-level by design (not a hard blocker); surface
    # it as an explanation but it does not force a block on its own.
    return [f for f in all_findings if f["check"] in STOP_CHECK_NAMES]


def explain(findings: list[dict]) -> str:
    blocks = [f for f in findings if f["level"] == "BLOCK"]
    warns = [f for f in findings if f["level"] == "WARN"]
    lines = []
    if blocks:
        lines.append("self-evo Stop hook: incomplete lifecycle state detected:")
        for f in blocks:
            lines.append(f"  - BLOCK {f['check']}: {f['detail']}")
    if warns:
        for f in warns:
            lines.append(f"  - WARN {f['check']}: {f['detail']}")
    if not blocks and not warns:
        lines.append("self-evo Stop hook: lifecycle checks passed.")
    return "\n".join(lines)


def main() -> int:
    raw = sys.stdin.read()
    issue_number = 5
    try:
        if raw.strip():
            payload = json.loads(raw)
            # Hook may be told which issue via env or payload field.
            issue_number = int(os.environ.get("SELF_EVO_ISSUE",
                                              payload.get("issue", 5)))
    except ValueError:
        pass

    # Unconditional escape hatch so a worker can always end a run.
    if os.environ.get(GUARD_ENV) == "1":
        return 0

    policy = _policy.load_policy()
    mode = _policy.resolve_rollout_mode(policy)
    block_enabled = _policy.mode_blocks_stop(policy, mode)
    date_str = validate_run._today()

    findings = lifecycle_findings(policy, issue_number, date_str)
    blocks = [f for f in findings if f["level"] == "BLOCK"]
    explanation = explain(findings)

    if not block_enabled or not blocks:
        # Clean (or audit/pretool-enforce): always allow stop; reset counter.
        save_counter(policy, 0)
        if findings:
            sys.stderr.write(explanation + "\n")
        return 0

    # full-enforce with BLOCK findings: consider blocking, subject to loop cap.
    counter = load_counter(policy)
    limit = int(policy.get("audit_log", {}).get("stop_loop_block_limit", 2))
    if counter >= limit:
        save_counter(policy, 0)
        sys.stderr.write(
            "self-evo Stop hook: loop cap reached; allowing stop. "
            "Remaining blockers need human action:\n" + explanation + "\n")
        return 0

    save_counter(policy, counter + 1)
    sys.stderr.write(
        f"self-evo Stop hook BLOCKING stop (attempt {counter + 1}/{limit}, "
        f"mode={mode}). Fix the issues below or set {GUARD_ENV}=1 to override:\n"
        + explanation + "\n")
    return 2


if __name__ == "__main__":
    sys.exit(main())
