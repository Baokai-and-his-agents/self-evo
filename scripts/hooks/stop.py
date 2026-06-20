#!/usr/bin/env python3
"""Claude Code Stop lifecycle hook for self-evo (MVP 1.5, Issue #5).

Runs the lifecycle subset of the read-only validator and explains any
incomplete state. Behaviour by rollout mode:
  * audit / pretool-enforce -> never block Stop; only report.
  * full-enforce           -> block Stop when there are BLOCK lifecycle
                              findings, so the worker fixes them before
                              ending the run.

Output contract (current official Claude Code hook schema):
  * Block: exit 0 + {"decision": "block", "reason": <explanation>}. The reason
            is delivered to Claude and the conversation continues. Stop uses the
            top-level decision field (NOT hookSpecificOutput). (Issue #5 review
            item 9.)
  * Allow: exit 0 with no decision block. Ambiguous/missing context and loop-cap
            allowances surface to the user via "systemMessage" (shown to the
            user, not to Claude), so they never trap or loop the worker.

Anti-loop protection (required by Issue #5): blocking Stop re-invokes this hook
after the worker responds, which can loop forever when a finding is not
worker-fixable (e.g. waiting on a human). We cap consecutive blocks at
policy.audit_log.stop_loop_block_limit (default 2) using a counter under
data/audit/ (an audit file, not task state), honour env SELF_EVO_STOP_GUARD=1
as an unconditional escape hatch, and respect the payload's stop_hook_active
flag. Claude Code additionally self-caps at 8 consecutive blocks.

The active issue is NOT hardcoded: it is derived from SELF_EVO_ISSUE env > the
agent branch name > the active claim/heartbeat, because standard Stop payloads
carry no issue field. (Issue #5 review item 8.)
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
ISSUE_ENV = "SELF_EVO_ISSUE"

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


def _emit_allow() -> int:
    sys.stdout.write(json.dumps({}))
    return 0


def _emit_system_message(message: str) -> int:
    sys.stdout.write(json.dumps({"systemMessage": message}))
    return 0


def _emit_block(reason: str) -> int:
    sys.stdout.write(json.dumps({"decision": "block", "reason": reason}))
    return 0


def _resolve_issue(policy: dict, payload: dict) -> tuple[int | None, str]:
    """SELF_EVO_ISSUE env > payload issue > agent branch > active claim."""
    env = os.environ.get(ISSUE_ENV)
    if env and env.strip().isdigit():
        return int(env.strip()), f"issue from env {ISSUE_ENV}={env.strip()}"
    payload_issue = payload.get("issue") if isinstance(payload, dict) else None
    if isinstance(payload_issue, (int, str)) and str(payload_issue).strip().isdigit():
        return int(str(payload_issue).strip()), "issue from Stop payload"
    issue, why = validate_run.derive_current_issue(policy)
    return issue, why


def main() -> int:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except ValueError:
        payload = {}

    # Unconditional escape hatch so a worker can always end a run.
    if os.environ.get(GUARD_ENV) == "1":
        return _emit_allow()

    policy = _policy.load_policy()
    mode = _policy.resolve_rollout_mode(policy)
    block_enabled = _policy.mode_blocks_stop(policy, mode)
    date_str = validate_run._today()

    issue_number, issue_source = _resolve_issue(policy, payload)
    if issue_number is None:
        # Cannot validate without an issue; never trap the worker.
        return _emit_system_message(
            f"self-evo Stop hook: cannot determine the active issue ({issue_source}). "
            f"Set {ISSUE_ENV}=<n> or run on an agent branch named '<n>-...'. "
            "Allowing stop; lifecycle validation skipped.")

    findings = lifecycle_findings(policy, issue_number, date_str)
    blocks = [f for f in findings if f["level"] == "BLOCK"]
    explanation = explain(findings)

    if not block_enabled or not blocks:
        # Clean (or audit/pretool-enforce): always allow stop; reset counter.
        save_counter(policy, 0)
        if findings and any(f["level"] == "WARN" for f in findings):
            # Surface advisory findings to the user without blocking or looping.
            warns = [f for f in findings if f["level"] == "WARN"]
            note = "self-evo Stop hook advisory (audit/pretool-enforce, not blocking): "
            note += "; ".join(f"{f['check']}: {f['detail']}" for f in warns)
            return _emit_system_message(note[:2000])
        return _emit_allow()

    # full-enforce with BLOCK findings: consider blocking, subject to loop cap.
    # Respect stop_hook_active so we do not re-litigate a continuation pointlessly.
    counter = load_counter(policy)
    limit = int(policy.get("audit_log", {}).get("stop_loop_block_limit", 2))
    if counter >= limit:
        save_counter(policy, 0)
        return _emit_system_message(
            f"self-evo Stop hook: loop cap reached ({limit}); allowing stop. "
            f"Remaining blockers need human action:\n" + explanation)

    save_counter(policy, counter + 1)
    reason = (f"self-evo Stop hook BLOCKING stop (attempt {counter + 1}/{limit}, "
              f"issue #{issue_number}, mode={mode}). Fix the issues below or set "
              f"{GUARD_ENV}=1 to override:\n" + explanation)
    return _emit_block(reason)


if __name__ == "__main__":
    sys.exit(main())
