#!/usr/bin/env python3
"""Claude Code PreToolUse safety hook for self-evo.

Input  (stdin, JSON): {"session_id", "tool_name", "tool_input", ...}
Output (stdout, JSON): one decision object on exit 0.
Exit codes: 0 = allow or structured deny (JSON processed); 2 reserved for
hard shell errors (stdout JSON is then ignored, so we avoid it for denials).

Behaviour by rollout mode (see scripts/policy.json):
  * audit            -> never deny; emit audit findings to the audit log.
  * pretool-enforce  -> deny BLOCK findings; report WARN findings.
  * full-enforce     -> same as pretool-enforce for PreToolUse.

Output contract (current official Claude Code hook schema):
  * Deny:  exit 0 + {"hookSpecificOutput": {"hookEventName": "PreToolUse",
            "permissionDecision": "deny", "permissionDecisionReason": ...}}.
            The reason is shown to Claude. (Issue #5 review item 9: exiting 2
            drops stdout, so the deny reason would be lost.)
  * Allow: exit 0; emit an allow note only when there is something to report,
            otherwise stay silent (plain allow).

Hooks are deterministic and read-only w.r.t. task state. The only write is an
append to data/audit/hook-audit.jsonl (an audit log, not task state), and that
log NEVER records raw commands, file contents, or secrets -- only minimal safe
metadata (codes, path zone, command length + hash). (Issue #5 review item 5.)
"""

from __future__ import annotations

import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _policy  # noqa: E402


def emit(decision: dict) -> int:
    """Print the Claude Code hook output (exit 0) and return the exit code.

    We always exit 0 so stdout JSON is processed: a deny is expressed via
    permissionDecision, not via exit code 2 (whose stdout is ignored).
    """
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
        return 0
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


def _safe_target_summary(tool_name: str, tool_input: dict, policy: dict) -> dict:
    """Minimal, secret-free metadata about the tool target.

    For write/edit tools we record only the classified zone of the path (never
    the path itself -- a path could be a secret-ish file). For shell tools we
    record only the command length and a sha256 prefix (never the command text,
    which routinely carries tokens, Authorization headers, and passwords).
    """
    if tool_name in _policy.WRITE_TOOLS:
        fp = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
        zone = _policy.classify_path(fp, policy) if fp else None
        return {"target_zone": zone}
    if tool_name in _policy.SHELL_TOOLS:
        command = (tool_input.get("command") or tool_input.get("script") or "")
        digest = hashlib.sha256(command.encode("utf-8", "replace")).hexdigest()[:16]
        return {"command_len": len(command), "command_sha256": digest}
    return {}


def _audit_log(policy, mode, tool_name, tool_input, decision) -> None:
    rel = policy.get("audit_log", {}).get("path", "data/audit/hook-audit.jsonl")
    path = os.path.join(_policy.REPO_ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # Only safe metadata is ever recorded: fixed finding codes, a path *zone*
    # (never the path/command text), a command length, and a sha256 prefix.
    # Command payloads, file contents, tokens, and Authorization/password values
    # therefore cannot appear in the log by construction.
    entry = {
        "event": "pretooluse",
        "mode": mode,
        "tool_name": tool_name,
        "decision": decision["decision"],
        "codes": [f["code"] for f in decision.get("findings", [])],
    }
    entry.update(_safe_target_summary(tool_name, tool_input, policy))
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")


if __name__ == "__main__":
    sys.exit(main())
