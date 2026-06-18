#!/usr/bin/env python3
"""Claude Code PreToolUse safety hook for self-evo.

Input  (stdin, JSON): {"session_id", "tool_name", "tool_input", ...}
Output (stdout, JSON): one decision object.
Exit codes: 0 = allow; 2 = block (Claude Code convention; stderr is surfaced).

Behaviour by rollout mode (see scripts/policy.json):
  * audit            -> never deny; emit audit findings to the audit log.
  * pretool-enforce  -> deny BLOCK findings; report WARN findings.
  * full-enforce     -> same as pretool-enforce for PreToolUse.

Hooks are deterministic and read-only w.r.t. task state. The only write is an
append to data/audit/hook-audit.jsonl (an audit log, not task state).
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _policy  # noqa: E402


def emit(decision: dict) -> int:
    """Print the Claude Code hook output and return the exit code."""
    findings = decision.get("findings", [])
    if decision["decision"] == "block":
        out = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": decision["reason"],
            }
        }
        sys.stdout.write(json.dumps(out))
        return 2
    # allow: emit a structured allow note only when there is something to report,
    # otherwise stay silent so Claude Code treats it as a plain allow.
    if findings:
        out = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
                "permissionDecisionReason": decision["reason"],
            }
        }
        sys.stdout.write(json.dumps(out))
    return 0


def main() -> int:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except ValueError:
        # Malformed input is never a reason to block the worker.
        return 0

    tool_name = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {}) or {}

    policy = _policy.load_policy()
    mode = _policy.resolve_rollout_mode(policy)
    block_enabled = _policy.mode_blocks_pretooluse(policy, mode)

    findings = _policy.classify_tool_use(tool_name, tool_input, policy)

    # In enforce modes, a likely-secret READ is promoted from WARN to BLOCK.
    if block_enabled:
        for f in findings:
            if f["code"] == "read_likely_secret":
                f["level"] = "BLOCK"
                f["action"] = "block"

    decision = _policy.synthesize_decision(findings, block_enabled=block_enabled)
    decision["mode"] = mode

    # Audit logging is best-effort and never blocks the worker.
    try:
        _audit_log(policy, mode, tool_name, tool_input, decision)
    except OSError:
        pass

    return emit(decision)


def _audit_log(policy, mode, tool_name, tool_input, decision) -> None:
    rel = policy.get("audit_log", {}).get("path", "data/audit/hook-audit.jsonl")
    path = os.path.join(_policy.REPO_ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    entry = {
        "event": "pretooluse",
        "mode": mode,
        "tool_name": tool_name,
        "decision": decision["decision"],
        "codes": [f["code"] for f in decision.get("findings", [])],
        "target": tool_input.get("file_path") or tool_input.get("command", ""),
    }
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")


if __name__ == "__main__":
    sys.exit(main())
