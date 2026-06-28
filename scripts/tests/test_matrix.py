#!/usr/bin/env python3
"""Offline deterministic test matrix for the self-evo hooks (Issue #5, section D).

Covers the required matrix plus the review-item regressions:
  * authorized data/** write            -> PASS
  * attempted rules/** write            -> BLOCK (audit: reported but allowed)
  * direct main push (Bash + PowerShell) -> BLOCK
  * force push                          -> BLOCK
  * agent branch push                   -> PASS
  * changed files without Draft PR      -> Stop BLOCK (full-enforce)
  * review with active claim            -> Stop BLOCK (full-enforce)
  * complete lifecycle                  -> PASS (Stop allows)
  * PowerShell Set-Content / redirection, Bash redirection, interpreter writes
  * draft-PR gate requires isDraft == true (a ready PR does not satisfy)
  * run-summary is specific to the active run identity (run-001 != run-002)
  * audit-log target summary never leaks raw command/secret text

Safety contract: this file NEVER executes a destructive command. It feeds
command STRINGS into the pure classifier and injects fake repo state into the
validator via attribute patches; no destructive git/gh subprocess and no repo
write is performed by the cases under test. (Real-git + real-subprocess tests
live in test_integration.py.)
"""

from __future__ import annotations

import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
sys.path.insert(0, SCRIPTS)

import _policy  # noqa: E402
import validate_run  # noqa: E402
import hooks.stop as stop  # noqa: E402
import hooks.pretooluse as pretool  # noqa: E402

policy = _policy.load_policy()

PASS = 0
FAIL = 0


def record(name: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    flag = "PASS" if ok else "FAIL"
    if ok:
        PASS += 1
    else:
        FAIL += 1
    print(f"  [{flag}] {name}" + (f" -- {detail}" if detail else ""))


def expect(name, cond, detail=""):
    record(name, bool(cond), detail)


# --------------------------------------------------------------------------- #
# Helpers that drive the pure classifier                                      #
# --------------------------------------------------------------------------- #

def classify(tool_name, tool_input):
    return _policy.classify_tool_use(tool_name, tool_input, policy)


def decide(tool_name, tool_input, *, block_enabled):
    findings = classify(tool_name, tool_input)
    return _policy.synthesize_decision(findings, block_enabled=block_enabled)


def bash(command):
    return classify("Bash", {"command": command})


def powershell(command):
    return classify("PowerShell", {"command": command})


def codes(findings):
    return [x["code"] for x in findings]


def has_block(findings, code=None):
    return any(x["level"] == "BLOCK" and (code is None or x["code"] == code)
               for x in findings)


def write(path):
    return classify("Write", {"file_path": path})


# --------------------------------------------------------------------------- #
# PreToolUse matrix                                                           #
# --------------------------------------------------------------------------- #

def test_pretool_matrix():
    print("\n== PreToolUse matrix ==")

    # 1. authorized data/** write -> PASS
    f = write("data/runs/2026-06-18/run-002.summary.md")
    expect("authorized data/** write: PASS", not has_block(f), str(codes(f)))

    # 2. attempted rules/** write -> BLOCK in enforce; audit allows but reports
    f = write("rules/PERMISSIONS.yaml")
    expect("rules/** write flagged (write_to_rules)",
           "write_to_rules" in codes(f), str(codes(f)))
    expect("rules/** write BLOCK in enforce",
           decide("Write", {"file_path": "rules/PERMISSIONS.yaml"}, block_enabled=True)["decision"] == "block")
    expect("rules/** write ALLOW in audit (reported)",
           decide("Write", {"file_path": "rules/PERMISSIONS.yaml"}, block_enabled=False)["decision"] == "approve")

    # 3. direct main push (Bash + PowerShell) -> BLOCK
    expect("Bash main push flagged", has_block(bash("git push origin main"), "protected_branch_push"))
    expect("PowerShell main push flagged",
           has_block(powershell("git push origin main"), "protected_branch_push"))
    expect("main push BLOCK in enforce",
           decide("Bash", {"command": "git push origin main"}, block_enabled=True)["decision"] == "block")

    # 4. force push (Bash + PowerShell) -> BLOCK
    expect("Bash force push flagged", has_block(bash("git push --force origin agent/x"), "force_push"))
    expect("PowerShell force push flagged",
           has_block(powershell("git push --force origin agent/x"), "force_push"))

    # 5. agent branch push -> PASS
    f = bash("git push origin agent/local-code-worker-01/5-hooks-validator")
    expect("agent branch push: PASS (no findings)", f == [], str(codes(f)))

    # 6. dangerous recursive deletion -> BLOCK
    expect("recursive delete flagged", has_block(bash("rm -rf ~"), "dangerous_recursive_delete"))
    expect("PowerShell recursive delete flagged",
           has_block(powershell("Remove-Item -Recurse -Force C:\\"), "dangerous_recursive_delete"))

    # 7. write outside authorized paths -> BLOCK
    f = write("README.md")
    expect("write outside authorized flagged", "write_outside_authorized" in codes(f), str(codes(f)))

    # 8. protected hook implementation write -> BLOCK
    f = write("scripts/hooks/pretooluse.py")
    expect("write to protected hook impl flagged",
           "write_to_protected_hook_impl" in codes(f), str(codes(f)))

    # 9. likely secret read -> WARN(audit) / BLOCK(enforce)
    f = classify("Read", {"file_path": ".env"})
    expect("read likely secret flagged", "read_likely_secret" in codes(f), str(codes(f)))

    # 10. normal test command -> PASS
    expect("normal test command: PASS", bash("python scripts/tests/test_matrix.py") == [])

    # 11. draft PR creation -> PASS
    expect("draft PR creation: PASS",
           bash("gh pr create --draft --base main --head agent/local-code-worker-01/5-hooks-validator") == [])

    # 12. .github protected write -> WARN (proposal_required)
    f = write(".github/CODEOWNERS")
    expect(".github write flagged as proposal_required",
           any(x["code"] == "write_proposal_required" for x in f), str(codes(f)))


def test_shell_write_bypasses():
    """Review item 2: shell-level writes that previously bypassed Bash-only
    detection must now be caught for both Bash and PowerShell."""
    print("\n== Shell-write bypass regression ==")

    expect("PowerShell Set-Content rules -> BLOCK",
           has_block(powershell("Set-Content rules/PERMISSIONS.yaml 'x'"), "shell_write_to_rules"))
    expect("PowerShell > rules redirect -> BLOCK",
           has_block(powershell("'x' > rules/PERMISSIONS.yaml"), "shell_write_to_rules"))
    expect("PowerShell Out-File .claude -> BLOCK",
           has_block(powershell("'x' | Out-File -FilePath .claude/settings.json"), "shell_write_to_protected"))
    expect("PowerShell >> scripts append -> BLOCK",
           has_block(powershell("'x' >> scripts/policy.json"), "shell_write_to_protected"))

    expect("Bash echo > rules redirect -> BLOCK",
           has_block(bash("echo x > rules/PERMISSIONS.yaml"), "shell_write_to_rules"))
    expect("Bash echo >> rules append -> BLOCK",
           has_block(bash("echo x >> rules/PERMISSIONS.yaml"), "shell_write_to_rules"))
    expect("Bash tee rules -> BLOCK",
           has_block(bash("echo x | tee rules/PERMISSIONS.yaml"), "shell_write_to_rules"))
    expect("Bash cp into .claude -> BLOCK",
           has_block(bash("cp x .claude/settings.json"), "shell_write_to_protected"))

    # Interpreter inline write to a protected path -> BLOCK (common pattern).
    expect("Bash python -c open('rules/...') -> BLOCK",
           has_block(bash("python -c \"open('rules/X','w')\""), "shell_write_to_rules"))

    # PowerShell -LiteralPath variants (review iteration 3).
    expect("PowerShell Set-Content -LiteralPath rules -> BLOCK",
           has_block(powershell("Set-Content -LiteralPath rules/PERMISSIONS.yaml -Value bad"), "shell_write_to_rules"))
    expect("PowerShell Add-Content -LiteralPath rules -> BLOCK",
           has_block(powershell("Add-Content -LiteralPath rules/x -Value y"), "shell_write_to_rules"))
    expect("PowerShell Clear-Content -LiteralPath rules -> BLOCK",
           has_block(powershell("Clear-Content -LiteralPath rules/x"), "shell_write_to_rules"))
    expect("PowerShell Out-File -LiteralPath rules -> BLOCK",
           has_block(powershell("Out-File -LiteralPath rules/x -InputObject z"), "shell_write_to_rules"))
    expect("PowerShell New-Item -LiteralPath rules -> BLOCK",
           has_block(powershell("New-Item -LiteralPath rules/new -ItemType File"), "shell_write_to_rules"))
    expect("PowerShell Copy-Item -Destination rules -> BLOCK",
           has_block(powershell("Copy-Item -LiteralPath data/src -Destination rules/dst"), "shell_write_to_rules"))

    # Bash dd of= / install destination (review iteration 3).
    expect("Bash dd of=rules -> BLOCK",
           has_block(bash("dd if=/dev/zero of=rules/sneak bs=1 count=1"), "shell_write_to_rules"))
    expect("Bash dd of=rules (minimal) -> BLOCK",
           has_block(bash("dd of=rules/x"), "shell_write_to_rules"))
    expect("Bash install src rules -> BLOCK",
           has_block(bash("install src rules/PERMISSIONS.yaml"), "shell_write_to_rules"))
    expect("Bash install -m 644 src rules -> BLOCK",
           has_block(bash("install -m 644 src rules/x"), "shell_write_to_rules"))

    # No false positives on benign shell writes / dev-null / fd duplication.
    expect("Bash echo > /dev/null: no finding",
           bash("echo x > /dev/null") == [], str(codes(bash("echo x > /dev/null"))))
    expect("Bash 2>&1: no finding", bash("cmd 2>&1") == [], str(codes(bash("cmd 2>&1"))))
    expect("Bash echo > data/x: no finding (authorized)",
           bash("echo x > data/runs/x.md") == [], str(codes(bash("echo x > data/runs/x.md"))))
    # `install` is the coreutils copy command only when it leads a sub-command;
    # pip/npm/make install must NOT be flagged.
    expect("pip install pkg pkg2: no finding",
           bash("pip install requests flask") == [], str(codes(bash("pip install requests flask"))))
    expect("npm install pkg: no finding",
           bash("npm install left-pad") == [], str(codes(bash("npm install left-pad"))))
    expect("make install: no finding",
           bash("make install") == [], str(codes(bash("make install"))))


def test_audit_log_secrecy():
    """Review item 5: the audit target summary never contains raw command or
    secret text (the full file-write secrecy test is in test_integration.py)."""
    print("\n== Audit-log target summary secrecy ==")
    secret_cmd = ("curl -H 'Authorization: Bearer sk-SECRET-TOKEN-123' "
                  "https://x/?password=hunter2&api_key=AKIAFAKE")
    summ = pretool._safe_target_summary("Bash", {"command": secret_cmd}, policy)
    blob = json.dumps(summ)
    for needle in ("Authorization", "Bearer", "sk-SECRET-TOKEN-123", "hunter2",
                   "AKIAFAKE", "password", "api_key", "curl"):
        expect(f"audit summary omits '{needle}'", needle not in blob, blob[:120])
    expect("audit summary carries hash + length only",
           "command_sha256" in summ and "command_len" in summ and len(summ) == 2, str(summ))

    # Write tool: only the path ZONE is logged, never the path itself.
    summ2 = pretool._safe_target_summary(
        "Write", {"file_path": "rules/PERMISSIONS.yaml"}, policy)
    blob2 = json.dumps(summ2)
    expect("write audit logs zone not path",
           summ2.get("target_zone") == "read_only" and "PERMISSIONS" not in blob2, blob2)


def test_projects_zone_authorization():
    """Operating-method/projects split: projects/** is a writable zone for
    operated business projects, parallel to data/**. The split must not weaken
    the other boundaries: rules/** stays read-only and .github/docs stay
    proposal_required."""
    print("\n== projects/ zone authorization ==")

    # 1. projects/** write -> PASS (no block, no finding) — same as data/**
    f = write("projects/fx-strategy-research/experiments/fx_backtest/README.md")
    expect("projects/** write: PASS (no findings)", f == [], str(codes(f)))

    # 2. a new file deep under projects/** is also writable
    f = write("projects/fx-strategy-research/runs/2026-06-29/run-001.summary.md")
    expect("new projects/** file writable", not has_block(f), str(codes(f)))

    # 3. a brand-new project dir is writable too (not just fx-strategy-research)
    f = write("projects/new-project/experiments/x.md")
    expect("new projects/<project>/ writable", not has_block(f), str(codes(f)))

    # 4. shell write under projects/** -> PASS (authorized zone)
    f = bash("echo hi > projects/fx-strategy-research/memory/note.md")
    expect("shell write under projects/**: PASS", not has_block(f), str(codes(f)))

    # 5. regression: rules/** still read-only (split did not weaken it)
    f = write("rules/PERMISSIONS.yaml")
    expect("rules/** still read-only after split",
           "write_to_rules" in codes(f), str(codes(f)))

    # 6. regression: .github/** still proposal_required
    f = write(".github/CODEOWNERS")
    expect(".github/** still proposal_required",
           any(x["code"] == "write_proposal_required" for x in f), str(codes(f)))

    # 7. regression: docs/** still proposal_required
    f = write("docs/ARCHITECTURE.md")
    expect("docs/** still proposal_required",
           any(x["code"] == "write_proposal_required" for x in f), str(codes(f)))


# --------------------------------------------------------------------------- #
# Fake repo state for lifecycle/Stop tests                                    #
# --------------------------------------------------------------------------- #

class FakeState:
    """In-memory stand-in for validate_run's git/gh/file accessors."""

    def __init__(self):
        self.branch = "agent/local-code-worker-01/5-hooks-validator"
        self.changed = []
        self.labels = ["status:claimed"]
        self.has_pr = False
        self.claim = {"issue": 5, "status": "claimed",
                      "run_id": "2026-06-18-run-002", "branch": self.branch}
        self.heartbeat = {"workers": [{"issue": 5, "status": "running",
                                       "run_id": "2026-06-18-run-002"}]}
        self.summaries = ["run-002.summary.md"]
        self.tasks_section = "Claimed"
        self.run_identity = {"run_id": "2026-06-18-run-002",
                             "date": "2026-06-18", "token": "run-002"}
        self.base_resolvable = True

    def install(self):
        v = validate_run
        v.current_branch = lambda: self.branch
        v.changed_files = lambda *a, **k: list(self.changed)
        v.changed_files_base_resolvable = lambda *a, **k: self.base_resolvable
        v.resolve_base_ref = lambda *a, **k: ("origin/main" if self.base_resolvable else None)
        v.issue_labels = lambda n: list(self.labels)
        v.has_draft_pr_for_branch = lambda b: self.has_pr
        v.claim_for_issue = lambda n: dict(self.claim) if self.claim else None
        v.heartbeat = lambda: dict(self.heartbeat)
        v.run_summaries_for_today = lambda d: list(self.summaries)
        v.tasks_md_status = lambda n: self.tasks_section
        v.active_run_identity = lambda n: dict(self.run_identity) if self.run_identity else None
        v._today = lambda: "2026-06-18"


def restore_accessors():
    import importlib
    importlib.reload(validate_run)


# --------------------------------------------------------------------------- #
# Draft-PR gate + run-identity specificity                                    #
# --------------------------------------------------------------------------- #

def test_draft_pr_gate():
    """Review item 6: a ready/open non-draft PR must NOT satisfy the draft gate."""
    print("\n== Draft-PR isDraft gate ==")
    orig = validate_run._gh
    try:
        validate_run._gh = lambda a: json.dumps([{"number": 7, "isDraft": False, "title": "ready"}])
        expect("ready PR does not satisfy draft gate",
               validate_run.has_draft_pr_for_branch("agent/x") is False)
        validate_run._gh = lambda a: json.dumps([{"number": 8, "isDraft": True, "title": "draft"}])
        expect("draft PR satisfies draft gate",
               validate_run.has_draft_pr_for_branch("agent/x") is True)
        validate_run._gh = lambda a: json.dumps([])
        expect("no PR -> False", validate_run.has_draft_pr_for_branch("agent/x") is False)
        validate_run._gh = lambda a: "not-json"
        expect("malformed gh -> False (fail safe)",
               validate_run.has_draft_pr_for_branch("agent/x") is False)
    finally:
        validate_run._gh = orig


def test_run_summary_specificity():
    """Review item 7: an unrelated run-001 summary must not satisfy run-002."""
    print("\n== Run-summary run-identity specificity ==")
    fs = FakeState()
    fs.run_identity = {"run_id": "2026-06-18-run-002", "date": "2026-06-18", "token": "run-002"}

    fs.summaries = ["run-001.summary.md"]  # unrelated run on same date
    fs.install()
    r = validate_run.check_run_summary_exists(5, "2026-06-18")
    expect("unrelated run-001 does NOT satisfy run-002", r["level"] != "PASS", str(r["detail"]))

    fs.summaries = ["run-002.summary.md"]  # matches
    fs.install()
    r = validate_run.check_run_summary_exists(5, "2026-06-18")
    expect("matching run-002 satisfies", r["level"] == "PASS", str(r["detail"]))

    fs.run_identity = None  # cannot determine identity
    fs.summaries = ["run-002.summary.md"]
    fs.install()
    r = validate_run.check_run_summary_exists(5, "2026-06-18")
    expect("missing run identity -> WARN (not pass)", r["level"] == "WARN", str(r["detail"]))

    restore_accessors()


def test_issue_derivation():
    """Review item 8: issue is derived from branch/claim, not hardcoded."""
    print("\n== Issue derivation ==")
    expect("issue_from_branch parses leading N",
           validate_run.issue_from_branch("agent/local-code-worker-01/5-hooks-validator") == 5)
    expect("issue_from_branch on non-agent branch -> None",
           validate_run.issue_from_branch("main") is None)


# --------------------------------------------------------------------------- #
# Stop / lifecycle matrix                                                     #
# --------------------------------------------------------------------------- #

def test_stop_matrix():
    print("\n== Stop / lifecycle matrix ==")

    # --- changed files without Draft PR -> Stop BLOCK ---
    fs = FakeState()
    fs.changed = ["data/runs/2026-06-18/run-002.summary.md"]
    fs.has_pr = False
    fs.install()
    findings = stop.lifecycle_findings(policy, 5, "2026-06-18")
    by_check = {f["check"]: f["level"] for f in findings}
    expect("changed files without PR -> BLOCK",
           by_check.get("changed_files_have_draft_pr") == "BLOCK", str(by_check))

    # --- review with active claim -> Stop BLOCK ---
    fs = FakeState()
    fs.labels = ["status:review"]
    fs.claim = {"issue": 5, "status": "claimed", "run_id": "2026-06-18-run-002"}
    fs.heartbeat = {"workers": [{"issue": 5, "status": "running", "run_id": "2026-06-18-run-002"}]}
    fs.tasks_section = "Review"
    fs.has_pr = True
    fs.changed = ["data/runs/2026-06-18/run-002.summary.md"]
    fs.install()
    findings = stop.lifecycle_findings(policy, 5, "2026-06-18")
    by_check = {f["check"]: f["level"] for f in findings}
    expect("review with active claim -> BLOCK",
           by_check.get("review_has_released_claim") == "BLOCK", str(by_check))
    expect("heartbeat still running before review -> BLOCK",
           by_check.get("heartbeat_idle_before_review") == "BLOCK", str(by_check))

    # --- complete lifecycle -> PASS (Stop allows even in full-enforce) ---
    fs = FakeState()
    fs.labels = ["status:review"]
    fs.changed = ["data/runs/2026-06-18/run-002.summary.md"]
    fs.has_pr = True
    fs.claim = {"issue": 5, "status": "released", "run_id": "2026-06-18-run-002"}
    fs.heartbeat = {"workers": [{"issue": 5, "status": "stopped", "run_id": "2026-06-18-run-002"}]}
    fs.tasks_section = "Review"
    fs.install()
    findings = stop.lifecycle_findings(policy, 5, "2026-06-18")
    blocks = [f for f in findings if f["level"] == "BLOCK"]
    expect("complete lifecycle: no BLOCK findings", blocks == [],
           str([f["check"] for f in blocks]))
    restore_accessors()


def test_stop_loop_cap():
    """Review item 9: Stop now exits 0 always; block is expressed as JSON
    {decision:block}. Loop cap: block, block, then allow (cap=2)."""
    print("\n== Stop anti-loop cap (exit 0 + JSON decision) ==")
    store = {"n": 0}

    def fake_load(policy_):
        return store["n"]

    def fake_save(policy_, value):
        store["n"] = value

    fs = FakeState()
    fs.labels = ["status:review"]
    fs.claim = {"issue": 5, "status": "claimed", "run_id": "2026-06-18-run-002"}
    fs.heartbeat = {"workers": [{"issue": 5, "status": "running", "run_id": "2026-06-18-run-002"}]}
    fs.tasks_section = "Review"
    fs.has_pr = True
    fs.changed = ["data/runs/2026-06-18/run-002.summary.md"]
    fs.install()

    orig_load, orig_save = stop.load_counter, stop.save_counter
    os.environ["SELF_EVO_ROLLOUT_MODE"] = "full-enforce"
    os.environ.pop("SELF_EVO_STOP_GUARD", None)
    os.environ.pop("SELF_EVO_ISSUE", None)
    results = []
    try:
        for _ in range(3):
            sys.stdin = io.StringIO(json.dumps({}))
            out, err = io.StringIO(), io.StringIO()
            real_in, real_out, real_err = sys.stdin, sys.stdout, sys.stderr
            sys.stdout, sys.stderr = out, err
            code = stop.main()
            sys.stdout, sys.stderr = real_out, real_err
            sys.stdin = real_in
            try:
                decision = json.loads(out.getvalue() or "{}").get("decision")
            except ValueError:
                decision = "<parse error>"
            results.append((code, decision))
    finally:
        stop.load_counter, stop.save_counter = orig_load, orig_save
        os.environ.pop("SELF_EVO_ROLLOUT_MODE", None)
        restore_accessors()
    # exit 0 throughout; decision block, block, then None (allow) on cap.
    expect("stop loop cap: [(0,block),(0,block),(0,None)]",
           results == [(0, "block"), (0, "block"), (0, None)], str(results))


def test_stop_emit_contract():
    """Review item 9: Stop block surfaces {decision:block,reason}; Stop allow
    emits no decision; ambiguous issue emits systemMessage."""
    print("\n== Stop emit contract ==")

    fs = FakeState()
    fs.labels = ["status:review"]
    fs.claim = {"issue": 5, "status": "claimed", "run_id": "2026-06-18-run-002"}
    fs.heartbeat = {"workers": [{"issue": 5, "status": "running", "run_id": "2026-06-18-run-002"}]}
    fs.tasks_section = "Review"
    fs.has_pr = True
    fs.changed = ["data/runs/2026-06-18/run-002.summary.md"]
    fs.install()
    os.environ["SELF_EVO_ROLLOUT_MODE"] = "full-enforce"
    os.environ.pop("SELF_EVO_STOP_GUARD", None)
    os.environ.pop("SELF_EVO_ISSUE", None)
    store = {"n": 0}
    stop.load_counter = lambda p: store["n"]
    stop.save_counter = lambda p, v: store.__setitem__("n", v)
    try:
        # block -> decision:block with reason
        sys.stdin = io.StringIO(json.dumps({}))
        out = io.StringIO()
        real = sys.stdout; sys.stdout = out
        rc = stop.main(); sys.stdout = real
        obj = json.loads(out.getvalue())
        expect("Stop block -> exit 0", rc == 0)
        expect("Stop block JSON has decision=block + reason",
               obj.get("decision") == "block" and bool(obj.get("reason")), str(obj)[:120])

        # audit mode -> allow, no decision block
        os.environ["SELF_EVO_ROLLOUT_MODE"] = "audit"
        sys.stdin = io.StringIO(json.dumps({}))
        out = io.StringIO(); sys.stdout = out
        stop.main(); sys.stdout = real
        obj = json.loads(out.getvalue() or "{}")
        expect("Stop audit allow -> no decision block", "decision" not in obj, str(obj)[:120])
    finally:
        restore_accessors()
        os.environ.pop("SELF_EVO_ROLLOUT_MODE", None)


def test_pretool_emit_contract():
    """Review item 9: PreToolUse deny -> exit 0 + permissionDecision:deny."""
    print("\n== PreToolUse emit contract ==")
    os.environ["SELF_EVO_ROLLOUT_MODE"] = "full-enforce"
    try:
        sys.stdin = io.StringIO(json.dumps(
            {"tool_name": "Bash", "tool_input": {"command": "git push origin main"}}))
        out = io.StringIO()
        real = sys.stdout; sys.stdout = out
        rc = pretool.main(); sys.stdout = real
        obj = json.loads(out.getvalue())
        expect("PreToolUse deny -> exit 0", rc == 0)
        hso = obj.get("hookSpecificOutput", {})
        expect("PreToolUse deny JSON has permissionDecision=deny + reason",
               hso.get("permissionDecision") == "deny" and bool(hso.get("permissionDecisionReason")),
               str(obj)[:120])
    finally:
        os.environ.pop("SELF_EVO_ROLLOUT_MODE", None)


# --------------------------------------------------------------------------- #
# Rollout modes                                                               #
# --------------------------------------------------------------------------- #

def test_rollout_modes():
    print("\n== Rollout mode resolution ==")
    expect("default mode is audit",
           _policy.resolve_rollout_mode(policy, env={}) == "audit")
    expect("env override to full-enforce",
           _policy.resolve_rollout_mode(policy, env={"SELF_EVO_ROLLOUT_MODE": "full-enforce"}) == "full-enforce")
    expect("invalid env ignored -> audit",
           _policy.resolve_rollout_mode(policy, env={"SELF_EVO_ROLLOUT_MODE": "yolo"}) == "audit")
    expect("audit blocks neither",
           _policy.mode_blocks_pretooluse(policy, "audit") is False
           and _policy.mode_blocks_stop(policy, "audit") is False)
    expect("pretool-enforce blocks pretool only",
           _policy.mode_blocks_pretooluse(policy, "pretool-enforce") is True
           and _policy.mode_blocks_stop(policy, "pretool-enforce") is False)
    expect("full-enforce blocks both",
           _policy.mode_blocks_pretooluse(policy, "full-enforce") is True
           and _policy.mode_blocks_stop(policy, "full-enforce") is True)


def main() -> int:
    print("self-evo offline test matrix -- Issue #5")
    test_pretool_matrix()
    test_shell_write_bypasses()
    test_audit_log_secrecy()
    test_projects_zone_authorization()
    test_draft_pr_gate()
    test_run_summary_specificity()
    test_issue_derivation()
    test_stop_matrix()
    test_stop_loop_cap()
    test_stop_emit_contract()
    test_pretool_emit_contract()
    test_rollout_modes()
    print("\n" + "=" * 48)
    print(f"RESULT: {PASS} passed, {FAIL} failed")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
