#!/usr/bin/env python3
"""Offline deterministic test matrix for the self-evo hooks (Issue #5, section D).

Covers the required matrix:
  * authorized data/** write            -> PASS
  * attempted rules/** write            -> BLOCK (audit: reported but allowed)
  * direct main push                    -> BLOCK
  * force push                          -> BLOCK
  * agent branch push                   -> PASS
  * changed files without Draft PR      -> Stop BLOCK (full-enforce)
  * review with active claim            -> Stop BLOCK (full-enforce)
  * complete lifecycle                  -> PASS (Stop allows)

Safety contract: this file NEVER executes a destructive command. It feeds
command STRINGS into the pure classifier and injects fake repo state into the
validator via attribute patches; no git/gh subprocess and no filesystem write
to repo paths is performed by the cases under test.
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
import hooks.pretooluse as pretool  # noqa: E402  (ensures import path works)

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
    print(f"  [{flag}] {name}" + (f" — {detail}" if detail else ""))


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


def write(path):
    return classify("Write", {"file_path": path})


# --------------------------------------------------------------------------- #
# PreToolUse matrix                                                           #
# --------------------------------------------------------------------------- #

def test_pretool_matrix():
    print("\n== PreToolUse matrix ==")

    # 1. authorized data/** write -> PASS (no BLOCK finding, decision approve)
    f = write("data/runs/2026-06-18/run-002.summary.md")
    expect("authorized data/** write: PASS",
           not any(x["level"] == "BLOCK" for x in f),
           str([x["code"] for x in f]))

    # 2. attempted rules/** write -> BLOCK in enforce; audit allows but reports
    f = write("rules/PERMISSIONS.yaml")
    codes = [x["code"] for x in f]
    expect("rules/** write flagged (write_to_rules)", "write_to_rules" in codes, str(codes))
    d_enforce = decide("Write", {"file_path": "rules/PERMISSIONS.yaml"}, block_enabled=True)
    d_audit = decide("Write", {"file_path": "rules/PERMISSIONS.yaml"}, block_enabled=False)
    expect("rules/** write BLOCK in enforce", d_enforce["decision"] == "block")
    expect("rules/** write ALLOW in audit (reported)", d_audit["decision"] == "approve")

    # 3. direct main push -> BLOCK
    f = bash("git push origin main")
    expect("direct main push flagged (protected_branch_push)",
           any(x["code"] == "protected_branch_push" for x in f),
           str([x["code"] for x in f]))
    expect("direct main push BLOCK in enforce",
           decide("Bash", {"command": "git push origin main"}, block_enabled=True)["decision"] == "block")

    # 4. force push -> BLOCK
    f = bash("git push --force origin agent/x")
    expect("force push flagged (force_push)",
           any(x["code"] == "force_push" for x in f), str([x["code"] for x in f]))
    expect("force push BLOCK in enforce",
           decide("Bash", {"command": "git push --force-with-lease origin agent/x"},
                  block_enabled=True)["decision"] == "block")

    # 5. agent branch push -> PASS
    f = bash("git push origin agent/local-code-worker-01/5-hooks-validator")
    expect("agent branch push: PASS (no findings)", f == [], str([x["code"] for x in f]))

    # 6. dangerous recursive deletion -> BLOCK
    f = bash("rm -rf ~")
    expect("recursive delete flagged (dangerous_recursive_delete)",
           any(x["code"] == "dangerous_recursive_delete" for x in f), str([x["code"] for x in f]))

    # 7. write outside authorized paths -> BLOCK
    f = write("README.md")
    codes = [x["code"] for x in f]
    expect("write outside authorized flagged (write_outside_authorized)",
           "write_outside_authorized" in codes, str(codes))
    expect("write outside authorized BLOCK in enforce",
           decide("Write", {"file_path": "README.md"}, block_enabled=True)["decision"] == "block")

    # 8. protected hook implementation write -> BLOCK
    f = write("scripts/hooks/pretooluse.py")
    codes = [x["code"] for x in f]
    expect("write to protected hook impl flagged",
           "write_to_protected_hook_impl" in codes, str(codes))

    # 9. likely secret read -> WARN(audit) / BLOCK(enforce)
    f = classify("Read", {"file_path": ".env"})
    expect("read likely secret flagged (read_likely_secret)",
           any(x["code"] == "read_likely_secret" for x in f), str([x["code"] for x in f]))

    # 10. normal test command -> PASS
    f = bash("python3 scripts/tests/test_matrix.py")
    expect("normal test command: PASS", f == [], str([x["code"] for x in f]))

    # 11. draft PR creation -> PASS
    f = bash("gh pr create --draft --base main --head agent/local-code-worker-01/5-hooks-validator")
    expect("draft PR creation: PASS", f == [], str([x["code"] for x in f]))

    # 12. .github protected write -> WARN (proposal_required), not allowed silently
    f = write(".github/CODEOWNERS")
    expect(".github write flagged as proposal_required",
           any(x["code"] == "write_proposal_required" for x in f),
           str([x["code"] for x in f]))


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
        self.claim = {"issue": 5, "status": "claimed"}
        self.heartbeat = {"workers": [{"issue": 5, "status": "running"}]}
        self.summaries = ["run-002.summary.md"]
        self.tasks_section = "Claimed"

    def install(self):
        v = validate_run
        v.current_branch = lambda: self.branch
        v.changed_tracked_files = lambda: list(self.changed)
        v.issue_labels = lambda n: list(self.labels)
        v.has_draft_pr_for_branch = lambda b: self.has_pr
        v.claim_for_issue = lambda n: dict(self.claim) if self.claim else None
        v.heartbeat = lambda: dict(self.heartbeat)
        v.run_summaries_for_today = lambda d: list(self.summaries)
        v.tasks_md_status = lambda n: self.tasks_section
        validate_run._today = lambda: "2026-06-18"


def restore_accessors():
    import importlib
    importlib.reload(validate_run)


# --------------------------------------------------------------------------- #
# Stop / lifecycle matrix                                                     #
# --------------------------------------------------------------------------- #

def test_stop_matrix():
    print("\n== Stop / lifecycle matrix ==")

    # --- changed files without Draft PR -> Stop BLOCK (full-enforce) ---
    fs = FakeState()
    fs.changed = ["data/runs/2026-06-18/run-002.summary.md"]
    fs.has_pr = False
    fs.labels = ["status:claimed"]
    fs.install()
    findings = stop.lifecycle_findings(policy, 5, "2026-06-18")
    by_check = {f["check"]: f["level"] for f in findings}
    expect("changed files without PR -> BLOCK",
           by_check.get("changed_files_have_draft_pr") == "BLOCK", str(by_check))

    # --- review with active claim -> Stop BLOCK ---
    fs = FakeState()
    fs.labels = ["status:review"]
    fs.claim = {"issue": 5, "status": "claimed"}  # active, not released
    fs.heartbeat = {"workers": [{"issue": 5, "status": "running"}]}
    fs.tasks_section = "Review"
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
    fs.claim = {"issue": 5, "status": "released"}
    fs.heartbeat = {"workers": [{"issue": 5, "status": "stopped"}]}
    fs.tasks_section = "Review"
    fs.install()
    findings = stop.lifecycle_findings(policy, 5, "2026-06-18")
    blocks = [f for f in findings if f["level"] == "BLOCK"]
    expect("complete lifecycle: no BLOCK findings", blocks == [],
           str([f["check"] for f in blocks]))


def test_stop_loop_cap():
    print("\n== Stop anti-loop cap ==")
    # Force a permanent BLOCK and confirm: block, block, then allow (cap=2).
    store = {"n": 0}

    def fake_load(policy_):
        return store["n"]

    def fake_save(policy_, value):
        store["n"] = value

    fs = FakeState()
    fs.labels = ["status:review"]
    fs.claim = {"issue": 5, "status": "claimed"}
    fs.heartbeat = {"workers": [{"issue": 5, "status": "running"}]}
    fs.tasks_section = "Review"
    fs.install()

    orig_load, orig_save = stop.load_counter, stop.save_counter
    stop.load_counter = fake_load
    stop.save_counter = fake_save
    os.environ["SELF_EVO_ROLLOUT_MODE"] = "full-enforce"
    os.environ.pop("SELF_EVO_STOP_GUARD", None)
    codes = []
    try:
        for _ in range(3):
            sys.stdin = io.StringIO(json.dumps({"issue": 5}))
            err = io.StringIO()
            real_stderr = sys.stderr
            sys.stderr = err
            code = stop.main()
            sys.stderr = real_stderr
            codes.append(code)
            sys.stdin = sys.__stdin__
    finally:
        stop.load_counter = orig_load
        stop.save_counter = orig_save
        os.environ.pop("SELF_EVO_ROLLOUT_MODE", None)
        restore_accessors()
    expect("stop loop cap: block, block, allow", codes == [2, 2, 0], str(codes))


def test_rollout_modes():
    print("\n== Rollout mode resolution ==")
    # default audit
    expect("default mode is audit",
           _policy.resolve_rollout_mode(policy, env={}) == "audit")
    # env override
    expect("env override to full-enforce",
           _policy.resolve_rollout_mode(policy, env={"SELF_EVO_ROLLOUT_MODE": "full-enforce"}) == "full-enforce")
    # invalid env ignored -> falls back
    expect("invalid env ignored -> audit",
           _policy.resolve_rollout_mode(policy, env={"SELF_EVO_ROLLOUT_MODE": "yolo"}) == "audit")
    # mode flags
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
    print("self-evo offline test matrix — Issue #5")
    test_pretool_matrix()
    test_stop_matrix()
    test_stop_loop_cap()
    test_rollout_modes()
    print("\n" + "=" * 48)
    print(f"RESULT: {PASS} passed, {FAIL} failed")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
