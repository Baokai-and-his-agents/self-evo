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
import re
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
# Shell-write classification (pure, best-effort)                              #
# --------------------------------------------------------------------------- #

def _strip_quotes(token: str) -> str:
    token = token.strip()
    if len(token) >= 2 and token[0] in "\"'" and token[-1] == token[0]:
        return token[1:-1]
    return token


# Tokens that appear after a redirect/operator but are not file targets.
_NON_FILE_TARGETS = {"&1", "&2", "&-", "/dev/null", "nul", "con", "prn", "aux"}


def _extract_write_paths(command: str) -> list[str]:
    """Best-effort extraction of file paths a shell command writes to.

    Covers the deterministic write surfaces across Bash and PowerShell:
    redirections (``>``/``>>``/``1>``/``&>``), ``tee``/``Tee-Object``, the
    PowerShell content cmdlets (``Set-Content``/``Add-Content``/``Out-File``/
    ``Tee-Object``/``New-Item``/``Clear-Content``) via ``-Path``/``-FilePath``/
    ``-LiteralPath`` or positionally, ``cp``/``mv``/``Copy-Item``/``Move-Item``
    destinations, coreutils ``dd of=`` and ``install SRC DEST``, ``[System.IO.
    File]::WriteAllText`` style writes, and the common ``python|node|perl -c
    "<inline open(...)>"`` interpreter pattern.

    Cannot be perfectly classified before execution: variable-indirect paths
    (``$p``/``${var}``), here-docs feeding an interpreter, aliases, and any
    Turing-complete inline interpreter code can hide the real target. We catch
    the common literal patterns and rely on the Stop hook's committed-diff check
    as the reliable backstop for anything that still lands on the branch. See
    scripts/README.md.
    """
    paths: list[str] = []

    def add(tok: str) -> None:
        tok = _strip_quotes(tok)
        if tok and tok.lower() not in _NON_FILE_TARGETS and not tok.startswith("-"):
            paths.append(tok)

    # 1. Redirections:  >  >>  1>  2>  &>  (skip 2>&1 / >&2 / &-).
    for m in re.finditer(
        r"(?:\d|&)?>{1,2}\s*(\"[^\"]+\"|'[^']+'|[^\s|;&<>]+)", command
    ):
        add(m.group(1))

    # 2. tee / Tee-Object <target>  (optional flags / -FilePath).
    for m in re.finditer(
        r"\b(?:tee|Tee-Object)\b(?:\s+-(?:[A-Za-z]+))*(?:\s+(?:-FilePath|-Path))?\s+"
        r"(\"[^\"]+\"|'[^']+'|[^\s|;&]+)",
        command, re.I,
    ):
        add(m.group(1))

    # 3. PowerShell write cmdlets with an explicit -Path / -FilePath / -LiteralPath.
    for m in re.finditer(
        r"\b(?:Set-Content|Add-Content|Out-File|Tee-Object|New-Item|Clear-Content)\b"
        r"[^|;&\n]*?(?:-Path|-FilePath|-LiteralPath)\s+(\"[^\"]+\"|'[^']+'|[^\s|;&]+)",
        command, re.I,
    ):
        add(m.group(1))

    # 4. PowerShell write cmdlets positional: Set-Content <path> ...
    for m in re.finditer(
        r"\b(?:Set-Content|Add-Content|Out-File)\s+(\"[^\"]+\"|'[^']+'|[^\s|;&]+)",
        command, re.I,
    ):
        add(m.group(1))

    # 5. cp/mv/Copy-Item/Move-Item — destination is the last non-flag token.
    for m in re.finditer(r"\b(?:cp|mv|copy|move|Copy-Item|Move-Item)\b(.+)", command, re.I):
        toks = re.findall(r"(\"[^\"]+\"|'[^']+'|[^\s]+)", m.group(1))
        toks = [t for t in toks if not _strip_quotes(t).startswith("-")]
        if len(toks) >= 2:
            add(toks[-1])

    # 5b. coreutils `dd ... of=<path>` (write target).
    for m in re.finditer(
        r"\bdd\b[^|;&\n]*?\bof=\s*(\"[^\"]+\"|'[^']+'|[^\s|;&]+)", command, re.I
    ):
        add(m.group(1))

    # 5c. coreutils `install SRC... DEST` (DEST is the last token). Split on
    # shell separators so `install` is treated as the copy command only when it
    # leads a sub-command -- never as the subcommand of pip/npm/apt/etc.
    for seg in re.split(r"(?:&&|\|\||[;|\n])", command):
        seg2 = re.sub(r"^(?:[A-Za-z_][\w.]*=\S+\s+)*(?:sudo\s+|time\s+)*",
                      "", seg.strip())
        head = seg2.split(None, 1)
        if len(head) == 2 and head[0].lower() == "install":
            toks = [t for t in re.findall(r"(\"[^\"]+\"|'[^']+'|[^\s]+)", head[1])
                    if not _strip_quotes(t).startswith("-")]
            if len(toks) >= 2:
                add(toks[-1])

    # 6. .NET static file writes: [System.IO.File]::WriteAllText('path', ...)
    for m in re.finditer(
        r"\[?(?:System\.IO\.File|IO\.File|io\.file)\]?\s*::\s*"
        r"(?:WriteAll(?:Text|Lines|Bytes)|AppendAll(?:Text|Lines))\s*\(\s*"
        r"(\"[^\"]+\"|'[^']+'|[^,)\s]+)",
        command, re.I,
    ):
        add(m.group(1))

    # 7. Interpreter inline write: python -c "...open('path','w')..."
    for m in re.finditer(
        r"(?:python|python3|py|node|perl|ruby)\b(?:\s+-\S+)*\s+(?:-c|-e)\s+"
        r"(\"[^\"]*\"|'[^']*')",
        command, re.I,
    ):
        snippet = m.group(1)
        for om in re.finditer(
            r"(?:open|WriteAllText|WriteAllLines|AppendAllText)\s*\(\s*"
            r"([\"'][^\"']+[\"'])", snippet, re.I,
        ):
            add(om.group(1))

    return [p for p in paths if p]


def classify_shell_write(command: str, policy: dict[str, Any]) -> list[dict[str, Any]]:
    """Detect shell-level writes to protected / out-of-zone paths.

    Returns one finding per distinct write target that lands in a read-only,
    protected, proposal-required, or outside zone. read_write/authorized_write
    targets produce no finding. Detection is best-effort and intentionally
    conservative; the Stop hook's committed-diff check is the reliable backstop.
    """
    findings: list[dict[str, Any]] = []
    seen: set[str] = set()
    for path in _extract_write_paths(command):
        key = path.replace("\\", "/")
        if key in seen:
            continue
        seen.add(key)
        zone = classify_path(path, policy)
        if zone == "read_only":
            findings.append(_finding(
                "BLOCK", "shell_write_to_rules",
                f"Shell write to read-only zone ({zone})"))
        elif zone in ("protected_claude_config", "protected_hook_implementation"):
            findings.append(_finding(
                "BLOCK", "shell_write_to_protected",
                f"Shell write to protected path ({zone})"))
        elif zone == "proposal_required":
            findings.append(_finding(
                "WARN", "shell_write_proposal_required",
                f"Shell write to proposal-required zone ({zone})"))
        elif zone == "outside":
            findings.append(_finding(
                "BLOCK", "shell_write_outside",
                "Shell write outside authorized repository paths"))
        # read_write / authorized_write -> allow, no finding.
    return findings


# --------------------------------------------------------------------------- #
# Tool-use classification (pure)                                             #
# --------------------------------------------------------------------------- #

# Tools whose tool_input carries a writable file path.
WRITE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
READ_TOOLS = {"Read"}

# Tools whose tool_input carries a shell command string. Claude Code 2.1.174+
# ships a first-class PowerShell tool alongside Bash; both carry a "command"
# field and must be inspected identically for dangerous operations and shell
# writes. (PowerShell may also expose the script under "script".)
SHELL_TOOLS = {"Bash", "PowerShell"}


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

    if tool_name in SHELL_TOOLS:
        # Bash and the first-class PowerShell tool both carry a command string.
        command = (tool_input.get("command") or tool_input.get("script") or "")
        # Dangerous command patterns -> BLOCK (shell-agnostic substrings).
        for f in classify_command(command, policy):
            code = f["code"]
            findings.append(_finding("BLOCK", code, f["reason"], pattern=f["pattern"]))
        # Shell writes to protected / out-of-zone paths -> BLOCK/WARN.
        findings.extend(classify_shell_write(command, policy))
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
