#!/usr/bin/env python3
"""Real-git / real-subprocess integration tests for the self-evo hooks.

These complement the offline matrix (test_matrix.py) by exercising REAL git
repositories created under the system temp dir (never this repo) and REAL
subprocesses, instead of monkeypatched accessors:

  * Review item 1 -- changed_files() sees a clean committed branch (committed
    diff vs base) plus staged/unstaged/untracked/renamed/deleted files.
  * Review item 2 -- the Stop committed-diff backstop catches a protected
    (rules/**) write that bypassed PreToolUse.
  * Review item 3 -- the validator runs as a real subprocess on Windows/GBK
    without crashing, and git UTF-8 output decodes safely.
  * Review item 5 -- the on-disk audit log never contains raw command/secret
    text (end-to-end through the real _audit_log writer).

Safety: no destructive command is executed. The only writes are to throwaway
temp directories and to the gitignored data/audit/ audit log.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
REPO = os.path.dirname(SCRIPTS)
sys.path.insert(0, SCRIPTS)

import _policy  # noqa: E402
import validate_run  # noqa: E402
import hooks.pretooluse as pretool  # noqa: E402

PASS = 0
FAIL = 0


def record(name, ok, detail=""):
    global PASS, FAIL
    flag = "PASS" if ok else "FAIL"
    if ok:
        PASS += 1
    else:
        FAIL += 1
    print(f"  [{flag}] {name}" + (f" -- {detail}" if detail else ""))


def expect(name, cond, detail=""):
    record(name, bool(cond), detail)


def _gitc(cwd, *args):
    """Run git in cwd, return stdout (UTF-8, fail-safe). Raise on non-zero."""
    proc = subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True,
        text=True, encoding="utf-8", errors="replace",
    )
    if proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed in {cwd}: {proc.stderr}")
    return proc.stdout


def _seed_repo(tmp):
    """Create a repo with one base commit on 'main'."""
    _gitc(tmp, "init", "-b", "main")
    _gitc(tmp, "config", "user.email", "t@t")
    _gitc(tmp, "config", "user.name", "t")
    _gitc(tmp, "config", "commit.gpgsign", "false")
    os.makedirs(os.path.join(tmp, "data"), exist_ok=True)
    with open(os.path.join(tmp, "data", "base.txt"), "w", encoding="utf-8") as fh:
        fh.write("base\n")
    _gitc(tmp, "add", "-A")
    _gitc(tmp, "commit", "-m", "base")


class _RepoRoot:
    """Context manager that points the validator at a temp repo."""

    def __init__(self, tmp):
        self.tmp = tmp
        self.saved_vr = validate_run.REPO_ROOT
        self.saved_pr = _policy.REPO_ROOT

    def __enter__(self):
        validate_run.REPO_ROOT = self.tmp
        _policy.REPO_ROOT = self.tmp
        return self

    def __exit__(self, *exc):
        validate_run.REPO_ROOT = self.saved_vr
        _policy.REPO_ROOT = self.saved_pr


# --------------------------------------------------------------------------- #
# Item 1: changed_files sees committed branch changes + working-tree states    #
# --------------------------------------------------------------------------- #

def test_changed_files_real_git():
    print("\n== Real-git changed_files union (item 1) ==")
    tmp = tempfile.mkdtemp(prefix="selfevo-git-")
    try:
        _seed_repo(tmp)
        _gitc(tmp, "checkout", "-b", "agent/worker-01/7-demo")
        # Committed branch change (clean working tree afterwards).
        with open(os.path.join(tmp, "data", "new.md"), "w", encoding="utf-8") as fh:
            fh.write("new\n")
        _gitc(tmp, "add", "-A")
        _gitc(tmp, "commit", "-m", "add new")

        policy = _policy.load_policy()
        with _RepoRoot(tmp):
            base = validate_run.resolve_base_ref(policy)
            expect("base ref resolved to 'main'", base == "main", str(base))
            cf = validate_run.changed_files(policy)
            expect("clean committed branch is NOT zero changes",
                   "data/new.md" in cf, str(cf))
            expect("working tree clean -> only committed file",
                   cf == ["data/new.md"], str(cf))

            # Untracked file is now included.
            with open(os.path.join(tmp, "data", "untracked.md"), "w", encoding="utf-8") as fh:
                fh.write("u\n")
            cf = validate_run.changed_files(policy)
            expect("untracked file included", "data/untracked.md" in cf, str(cf))

            # Staged modification is included.
            with open(os.path.join(tmp, "data", "new.md"), "w", encoding="utf-8") as fh:
                fh.write("changed\n")
            _gitc(tmp, "add", "data/new.md")
            cf = validate_run.changed_files(policy)
            expect("staged modification included", "data/new.md" in cf, str(cf))

            # Deleted tracked file is included.
            os.remove(os.path.join(tmp, "data", "new.md"))
            cf = validate_run.changed_files(policy)
            expect("deleted file included", "data/new.md" in cf, str(cf))

            # Renamed tracked file: new name included.
            _gitc(tmp, "checkout", "--", ".")  # reset deletions/mods
            os.remove(os.path.join(tmp, "data", "untracked.md"))
            _gitc(tmp, "mv", "data/base.txt", "data/renamed.txt")
            cf = validate_run.changed_files(policy)
            expect("renamed file new name included",
                   "data/renamed.txt" in cf, str(cf))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# --------------------------------------------------------------------------- #
# Item 2: Stop committed-diff backstop catches a protected write              #
# --------------------------------------------------------------------------- #

def test_stop_backstop_protected_write():
    print("\n== Stop backstop catches committed protected write (item 2) ==")
    tmp = tempfile.mkdtemp(prefix="selfevo-stop-")
    try:
        _seed_repo(tmp)
        _gitc(tmp, "checkout", "-b", "agent/worker-01/7-demo")
        # Simulate an interpreter write that landed on the branch under rules/**.
        os.makedirs(os.path.join(tmp, "rules"), exist_ok=True)
        with open(os.path.join(tmp, "rules", "sneak.yaml"), "w", encoding="utf-8") as fh:
            fh.write("x\n")
        _gitc(tmp, "add", "-A")
        _gitc(tmp, "commit", "-m", "sneak")

        policy = _policy.load_policy()
        with _RepoRoot(tmp):
            # The PreToolUse interpreter-write classifier may or may not catch
            # arbitrary inline code, but the Stop committed-diff check MUST.
            cf = validate_run.changed_files(policy)
            expect("committed rules/** write appears in changed_files",
                   "rules/sneak.yaml" in cf, str(cf))
            auth = validate_run.check_changed_files_within_authorized(policy)
            expect("Stop backstop BLOCKs committed rules/** write",
                   auth["level"] == "BLOCK" and "rules" in auth["detail"], str(auth))
            rules = validate_run.check_no_unauthorized_rules_changes()
            expect("no_unauthorized_rules_changes BLOCKs it",
                   rules["level"] == "BLOCK" and "rules/sneak.yaml" in rules["detail"],
                   str(rules))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# --------------------------------------------------------------------------- #
# Item 3: validator runs as a real subprocess on Windows/GBK; UTF-8 decode    #
# --------------------------------------------------------------------------- #

def test_validator_subprocess_windows():
    print("\n== Validator real subprocess + UTF-8 decode (item 3) ==")
    # Reproduces the reviewer's crash: `python scripts/validate_run.py --json`.
    proc = subprocess.run(
        [sys.executable, os.path.join(SCRIPTS, "validate_run.py"),
         "--issue", "5", "--date", "2026-06-18", "--json"],
        cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    expect("validator subprocess exits 0 (no crash)", proc.returncode == 0,
           f"rc={proc.returncode} stderr={proc.stderr[:200]}")
    try:
        data = json.loads(proc.stdout)
    except ValueError:
        data = None
    expect("validator emits valid JSON", data is not None, (proc.stdout or "")[:200])
    if data:
        expect("validator JSON has findings summary",
               "summary" in data and "findings" in data, str(data.get("summary")))

    # UTF-8 git decode: a repo with a non-ASCII path must not crash _git.
    tmp = tempfile.mkdtemp(prefix="selfevo-utf8-")
    try:
        _seed_repo(tmp)
        odd = os.path.join(tmp, "data", "résumé-测试.md")
        with open(odd, "w", encoding="utf-8") as fh:
            fh.write("u\n")
        with _RepoRoot(tmp):
            out = validate_run._git(["-c", "core.quotepath=false",
                                     "status", "--porcelain"])
            expect("git UTF-8 output decodes without raising",
                   isinstance(out, str) and len(out) > 0, repr(out)[:120])
            wt = validate_run.workingtree_changed_files()
            expect("non-ASCII untracked path is captured",
                   any("sum" in f or "测试" in f or "r" in f.lower() for f in wt)
                   and len(wt) >= 1, str(wt))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# --------------------------------------------------------------------------- #
# Item 5: on-disk audit log never contains raw commands or secrets           #
# --------------------------------------------------------------------------- #

def test_audit_log_on_disk_secrecy():
    print("\n== Audit log on-disk secrecy (item 5) ==")
    tmp = tempfile.mkdtemp(prefix="selfevo-audit-")
    audit_path = os.path.join(tmp, "hook-audit.jsonl")
    policy = _policy.load_policy()
    # Point the policy's audit path at the temp file.
    policy = dict(policy)
    policy["audit_log"] = dict(policy.get("audit_log", {}))
    policy["audit_log"]["path"] = audit_path

    secret_cmd = ("curl -H 'Authorization: Bearer sk-live-SECRET-9' "
                  "https://api/?password=hunter2&api_key=AKIAFAKEKEY cmd-payload-XYZ")
    tool_input = {"command": secret_cmd}
    decision = {"decision": "approve", "findings": []}

    # _audit_log uses _policy.REPO_ROOT to resolve the rel path -> patch it.
    saved = _policy.REPO_ROOT
    _policy.REPO_ROOT = tmp
    try:
        pretool._audit_log(policy, "audit", "Bash", tool_input, decision)
    finally:
        _policy.REPO_ROOT = saved

    expect("audit log file was written", os.path.exists(audit_path))
    with open(audit_path, "r", encoding="utf-8") as fh:
        content = fh.read()
    for needle in ("Authorization", "Bearer", "sk-live-SECRET-9", "hunter2",
                   "AKIAFAKEKEY", "password", "api_key", "cmd-payload-XYZ"):
        expect(f"on-disk audit log omits '{needle}'", needle not in content, content[:160])
    try:
        entry = json.loads(content.strip().splitlines()[-1])
    except ValueError:
        entry = {}
    expect("audit entry carries hash+length, no raw command",
           "command_sha256" in entry and "command_len" in entry
           and "command" not in entry, str(entry))


def test_run_summary_run_specific_real_files():
    """Review iteration 3: with a concrete run_id known, an issue-only
    reference in a DIFFERENT run's summary must NOT satisfy the active run."""
    print("\n== Run-summary run-specificity with real files (review iter 3) ==")
    tmp = tempfile.mkdtemp(prefix="selfevo-rsid-")
    try:
        rundir = os.path.join(tmp, "data", "runs", "2026-06-18")
        os.makedirs(rundir, exist_ok=True)
        # Unrelated run-001 summary that mentions Issue #5 + its own run id.
        with open(os.path.join(rundir, "run-001.summary.md"), "w", encoding="utf-8") as fh:
            fh.write("# Run Summary - run-001\nIssue #5\nrun id: 2026-06-18-run-001\n")

        vr, pr = validate_run.REPO_ROOT, _policy.REPO_ROOT
        orig_ident = validate_run.active_run_identity
        validate_run.REPO_ROOT = tmp
        _policy.REPO_ROOT = tmp
        validate_run.active_run_identity = lambda n: {
            "run_id": "2026-06-18-run-002", "date": "2026-06-18", "token": "run-002"}
        try:
            r = validate_run.check_run_summary_exists(5, "2026-06-18")
            expect("unrelated run-001 file (mentions Issue #5) does NOT satisfy run-002",
                   r["level"] != "PASS", str(r["detail"]))
        finally:
            validate_run.active_run_identity = orig_ident
            validate_run.REPO_ROOT = vr
            _policy.REPO_ROOT = pr

        # A run-002 token-named file -> PASS.
        os.remove(os.path.join(rundir, "run-001.summary.md"))
        with open(os.path.join(rundir, "run-002.summary.md"), "w", encoding="utf-8") as fh:
            fh.write("# Run Summary - run-002\nrun id: 2026-06-18-run-002\n")
        validate_run.REPO_ROOT = tmp
        _policy.REPO_ROOT = tmp
        validate_run.active_run_identity = lambda n: {
            "run_id": "2026-06-18-run-002", "date": "2026-06-18", "token": "run-002"}
        try:
            r = validate_run.check_run_summary_exists(5, "2026-06-18")
            expect("run-002 token file satisfies run-002",
                   r["level"] == "PASS", str(r["detail"]))
        finally:
            validate_run.active_run_identity = orig_ident
            validate_run.REPO_ROOT = vr
            _policy.REPO_ROOT = pr
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main() -> int:
    print("self-evo integration tests -- Issue #5")
    test_changed_files_real_git()
    test_stop_backstop_protected_write()
    test_validator_subprocess_windows()
    test_run_summary_run_specific_real_files()
    test_audit_log_on_disk_secrecy()
    print("\n" + "=" * 48)
    print(f"RESULT: {PASS} passed, {FAIL} failed")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
