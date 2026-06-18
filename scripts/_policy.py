"""Shared guardrail policy and classification logic for self-evo hooks.

This module is the single place that decides what is dangerous or authorized.
The PowerShell entrypoints and the offline tests both import the same functions
here (directly, or via the JSON produced), so the three surfaces cannot drift.

Design constraints from Issue #5 and rules/PERMISSIONS.yaml:
  * Hooks are deterministic and read-only with respect to task state.
  * The only files a hook may write live under data/audit/ (audit log +
    stop-loop counter). It never mutates state/** task state, never commits,
    and never opens PRs.
  * Rollout mode precedence: env SELF_EVO_ROLLOUT_MODE > scripts/hooks/config.json
    > policy.default_rollout_mode. The committed default must remain "audit".

Pure (no I/O) helpers: path classification, command classification, tool-use
classification. I/O helpers (load mode, append audit log) are isolated so the
pure functions are easy to unit-test deterministically.
"""

from __future__ import annotations

import fnmatch
import json
import os
from typing import Any, Iterable

# --------------------------------------------------------------------------- #
# Paths                                                                       #
# --------------------------------------------------------------------------- #

_HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = _HERE
REPO_ROOT = os.path.dirname(SCRIPTS_DIR)
POLICY_PATH = os.path.join(SCRIPTS_DIR, "policy.json")
CONFIG_PATH = os.path.join(SCRIPTS_DIR, "hooks", "config.json")

MODE_ENV = "SELF_EVO_ROLLOUT_MODE"
VALID_MODES = ("audit", "pretool-enforce", "full-enforce")


# --------------------------------------------------------------------------- #
# Policy loading                                                              #
# --------------------------------------------------------------------------- #

def load_policy(policy_path: str = POLICY_PATH) -> dict[str, Any]:
    """Load the guardrail contract JSON. Pure file read."""
    with open(policy_path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def resolve_rollout_mode(
    policy: dict[str, Any],
    *,
    env: dict[str, str] | None = None,
    config_path: str = CONFIG_PATH,
) -> str:
    """Resolve the active rollout mode.

    Precedence: SELF_EVO_ROLLOUT_MODE env > scripts/hooks/config.json >
    policy.default_rollout_mode. Falls back to default on any problem so a
    missing/misconfigured file can never silently raise enforcement.
    """
    default = policy.get("default_rollout_mode", "audit")

    env_map = os.environ if env is None else env
    mode = env_map.get(MODE_ENV)
    if mode in VALID_MODES:
        return mode

    try:
        with open(config_path, "r", encoding="utf-8") as fh:
            cfg = json.load(fh)
        mode = cfg.get("rollout_mode")
        if mode in VALID_MODES:
            return mode
    except (OSError, ValueError):
        pass

    return default if default in VALID_MODES else "audit"


def mode_blocks_pretooluse(policy: dict[str, Any], mode: str) -> bool:
    return bool(policy.get("rollout_modes", {}).get(mode, {}).get("pretooluse_blocks"))


def mode_blocks_stop(policy: dict[str, Any], mode: str) -> bool:
    return bool(policy.get("rollout_modes", {}).get(mode, {}).get("stop_blocks"))


# --------------------------------------------------------------------------- #
# Path helpers (pure)                                                         #
# --------------------------------------------------------------------------- #

def _norm(path: str) -> str:
    """Normalize to repo-relative, forward-slash, with a leading './' stripped.

    Note: we only strip a literal './' prefix — NOT leading dots — so dotfiles
    like '.env' and '.github/' are preserved (stripping dots would turn '.env'
    into 'env' and break secret/path matching).
    """
    if os.path.isabs(path):
        try:
            path = os.path.relpath(path, REPO_ROOT)
        except ValueError:
            path = os.path.basename(path)
    p = path.replace("\\", "/")
    while p.startswith("./"):
        p = p[2:]
    return p


def _match_any(rel_path: str, patterns: Iterable[str]) -> bool:
    rel_path = rel_path.replace("\\", "/")
    base = os.path.basename(rel_path)
    for pat in patterns:
        pat = pat.replace("\\", "/")
        if fnmatch.fnmatch(rel_path, pat):
            return True
        # "**/foo" should also match a bare "foo" at any depth (incl. repo root),
        # because fnmatch's "*" does not cross the leading directory boundary.
        if pat.startswith("**/"):
            suffix = pat[3:]
            if fnmatch.fnmatch(rel_path, suffix) or fnmatch.fnmatch(base, suffix):
                return True
        # "dir/**" should also match the directory itself.
        if pat.endswith("/**") and (rel_path == pat[:-4] or rel_path.startswith(pat[:-3])):
            return True
    return False


def classify_path(rel_path: str, policy: dict[str, Any]) -> str:
    """Return the most restrictive path zone for a repo-relative path.

    One of: read_only, proposal_required, protected_hook_implementation,
    protected_claude_config, read_write, authorized_write, outside.
    """
    paths = policy.get("paths", {})
    rp = _norm(rel_path)
    if _match_any(rp, paths.get("read_only", [])):
        return "read_only"
    if _match_any(rp, paths.get("protected_claude_config", [])):
        return "protected_claude_config"
    if _match_any(rp, paths.get("protected_hook_implementation", [])):
        return "protected_hook_implementation"
    if _match_any(rp, paths.get("proposal_required", [])):
        return "proposal_required"
    if _match_any(rp, paths.get("read_write", [])):
        return "read_write"
    # Authorized write roots that are not already classified.
    for root in paths.get("authorized_write_roots", []):
        if rp == root.rstrip("/") or rp.startswith(root):
            return "authorized_write"
    return "outside"


def is_likely_secret_path(rel_path: str, policy: dict[str, Any]) -> bool:
    rp = _norm(rel_path)
    secrets = policy.get("secrets", {})
    if _match_any(rp, secrets.get("path_patterns", [])):
        return True
    base = os.path.basename(rp).upper()
    return any(frag in base for frag in secrets.get("name_fragments", []))


# --------------------------------------------------------------------------- #
# Command classification (pure)                                              #
# --------------------------------------------------------------------------- #

def _cmd_contains(command: str, patterns: Iterable[str]) -> str | None:
    """Return the first pattern found (case-insensitive, whitespace-tolerant)."""
    norm = " ".join(command.lower().split())
    for pat in patterns:
        p = " ".join(pat.lower().split())
        if p and p in norm:
            return pat
    return None


def classify_command(command: str, policy: dict[str, Any]) -> list[dict[str, str]]:
    """Inspect a shell command string for dangerous operations.

    Returns a list of findings, each {"code", "reason", "pattern"}.
    Detection is intentionally substring-based; see known-limitations in
    scripts/README.md for false positives/negatives.
    """
    findings: list[dict[str, str]] = []
    dc = policy.get("dangerous_commands", {})

    hit = _cmd_contains(command, dc.get("recursive_delete", {}).get("patterns", []))
    if hit:
        findings.append({
            "code": "dangerous_recursive_delete",
            "reason": "Recursive deletion of a home/root/git path is destructive.",
            "pattern": hit,
        })

    hit = _cmd_contains(command, dc.get("force_push", {}).get("patterns", []))
    if hit:
        findings.append({
            "code": "force_push",
            "reason": "Force push rewrites shared history.",
            "pattern": hit,
        })

    hit = _cmd_contains(command, dc.get("protected_branch_push", {}).get("patterns", []))
    if hit:
        findings.append({
            "code": "protected_branch_push",
            "reason": "Direct push to a protected branch (main).",
            "pattern": hit,
        })

    return findings


# --------------------------------------------------------------------------- #
# Tool-use classification (pure)                                             #
# --------------------------------------------------------------------------- #

# Tools whose tool_input carries a writable file path.
WRITE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
READ_TOOLS = {"Read"}


def classify_tool_use(
    tool_name: str,
    tool_input: dict[str, Any],
    policy: dict[str, Any],
) -> list[dict[str, Any]]:
    """Classify one tool invocation into a list of findings.

    Each finding: {"level": "BLOCK"|"WARN", "code", "reason", "action": "block"|"allow"}.
    BLOCK findings are downgraded to allow in audit mode by the caller, not here,
    so this function stays pure and mode-independent.
    """
    findings: list[dict[str, Any]] = []
    tool_input = tool_input or {}

    if tool_name in WRITE_TOOLS:
        fp = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
        zone = classify_path(fp, policy)
        if zone in ("read_only",):
            findings.append(_finding("BLOCK", "write_to_rules",
                          f"Write to read-only zone ({zone}): {fp}"))
        elif zone in ("protected_claude_config", "protected_hook_implementation"):
            findings.append(_finding("BLOCK", "write_to_protected_hook_impl",
                          f"Write to protected hook/config path ({zone}): {fp}"))
        elif zone == "proposal_required":
            findings.append(_finding("WARN", "write_proposal_required",
                          f"Write to proposal-required zone ({zone}): {fp}"))
        elif zone == "outside":
            findings.append(_finding("BLOCK", "write_outside_authorized",
                          f"Write outside authorized repository paths: {fp}"))
        # read_write / authorized_write -> allow, no finding.
        return findings

    if tool_name == "Bash":
        command = tool_input.get("command", "") or ""
        # First, dangerous command patterns -> BLOCK.
        for f in classify_command(command, policy):
            code = f["code"]
            findings.append(_finding("BLOCK", code, f["reason"], pattern=f["pattern"]))
        # If no dangerous command, an ordinary git push to a non-protected ref is allowed.
        return findings

    if tool_name in READ_TOOLS:
        fp = tool_input.get("file_path", "") or ""
        if fp and is_likely_secret_path(fp, policy):
            findings.append(_finding("WARN", "read_likely_secret",
                          f"Read of a likely secret/private-key file: {fp}"))
        # In enforce modes the caller promotes read_likely_secret to BLOCK.
        return findings

    return findings


def _finding(level: str, code: str, reason: str, **extra: Any) -> dict[str, Any]:
    action = "block" if level == "BLOCK" else "allow"
    out: dict[str, Any] = {"level": level, "code": code, "reason": reason, "action": action}
    out.update(extra)
    return out


# --------------------------------------------------------------------------- #
# Decision synthesis                                                          #
# --------------------------------------------------------------------------- #

def synthesize_decision(
    findings: list[dict[str, Any]],
    *,
    block_enabled: bool,
) -> dict[str, Any]:
    """Merge findings into a single hook decision.

    In audit mode (block_enabled=False) every finding is allow + the original
    level is preserved for reporting. A single BLOCK finding with enforcement
    on yields a deny.
    """
    blocks = [f for f in findings if f["level"] == "BLOCK"]
    will_block = block_enabled and bool(blocks)

    if will_block:
        reasons = "; ".join(f"{f['code']}: {f['reason']}" for f in blocks)
        return {
            "decision": "block",
            "permission_decision": "deny",
            "reason": reasons,
            "findings": findings,
        }
    return {
        "decision": "approve",
        "permission_decision": "allow",
        "reason": "" if not findings else "audit: " + "; ".join(
            f"{f['code']}" for f in findings),
        "findings": findings,
    }
