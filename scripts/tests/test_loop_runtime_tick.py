#!/usr/bin/env python3
"""Tests for the Stage R runtime-confined no-op tick."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent
sys.path.insert(0, str(SCRIPTS))

import loop_runtime_tick as tick  # noqa: E402


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


def expect(name: str, cond: bool, detail: str = "") -> None:
    record(name, bool(cond), detail)


def _git(cwd: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if check and proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr}")
    return proc


def _seed_repo(*, ignore_runtime: bool) -> Path:
    tmp = Path(tempfile.mkdtemp(prefix="selfevo-stage-r-"))
    _git(tmp, "init", "-b", "main")
    _git(tmp, "config", "user.email", "t@t")
    _git(tmp, "config", "user.name", "t")
    _git(tmp, "config", "commit.gpgsign", "false")
    (tmp / "README.md").write_text("base\n", encoding="utf-8")
    if ignore_runtime:
        (tmp / ".gitignore").write_text(".self-evo/runtime/\n", encoding="utf-8")
    _git(tmp, "add", "-A")
    _git(tmp, "commit", "-m", "base")
    return tmp


def test_runtime_writer_allows_runtime_writes() -> None:
    print("\n== Runtime writer allows runtime writes ==")
    tmp = Path(tempfile.mkdtemp(prefix="selfevo-writer-"))
    try:
        writer = tick.RuntimeWriter(tmp, "run-001")
        path = writer.write_text("decision.md", "ok\n")
        expect("file is written", path.exists(), str(path))
        expect("file stays inside runtime", ".self-evo/runtime/runs/run-001" in str(path))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_runtime_writer_rejects_outside_runtime() -> None:
    print("\n== Runtime writer rejects outside writes ==")
    tmp = Path(tempfile.mkdtemp(prefix="selfevo-writer-escape-"))
    try:
        writer = tick.RuntimeWriter(tmp, "run-001")
        blocked = False
        try:
            writer.write_text("../../../escape.txt", "bad\n")
        except tick.RuntimeBoundaryError:
            blocked = True
        expect("path traversal is blocked", blocked)
        expect("escape file was not written", not (tmp / "escape.txt").exists())
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_runtime_writer_rejects_absolute_path() -> None:
    print("\n== Runtime writer rejects absolute paths ==")
    tmp = Path(tempfile.mkdtemp(prefix="selfevo-writer-absolute-"))
    try:
        writer = tick.RuntimeWriter(tmp, "run-001")
        blocked = False
        try:
            writer.write_text(tmp / "escape.txt", "bad\n")
        except tick.RuntimeBoundaryError:
            blocked = True
        expect("absolute path is blocked", blocked)
        expect("absolute escape file was not written", not (tmp / "escape.txt").exists())
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_runtime_writer_rejects_bad_run_id() -> None:
    print("\n== Runtime writer rejects path-like run ids ==")
    tmp = Path(tempfile.mkdtemp(prefix="selfevo-writer-runid-"))
    try:
        for bad in ("../escape", "runs/../../x", "space bad"):
            blocked = False
            try:
                tick.RuntimeWriter(tmp, bad)
            except tick.RuntimeBoundaryError:
                blocked = True
            expect(f"bad run_id blocked: {bad}", blocked)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_runtime_writer_rejects_symlink_runtime() -> None:
    print("\n== Runtime writer rejects symlink runtime components ==")
    tmp = Path(tempfile.mkdtemp(prefix="selfevo-writer-symlink-"))
    outside = Path(tempfile.mkdtemp(prefix="selfevo-writer-outside-"))
    try:
        (tmp / ".self-evo").symlink_to(outside, target_is_directory=True)
        blocked = False
        try:
            tick.RuntimeWriter(tmp, "run-001")
        except tick.RuntimeBoundaryError:
            blocked = True
        expect("symlink component is blocked", blocked)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        shutil.rmtree(outside, ignore_errors=True)


def test_tick_fails_when_runtime_not_ignored() -> None:
    print("\n== Tick requires gitignored runtime ==")
    tmp = _seed_repo(ignore_runtime=False)
    try:
        blocked = False
        try:
            tick.run_noop_tick(tmp, run_id="run-001")
        except tick.RuntimeBoundaryError as exc:
            blocked = ".self-evo/runtime/" in str(exc)
        expect("tick blocks without .self-evo/runtime/ ignore", blocked)
        expect("runtime directory not created", not (tmp / ".self-evo").exists())
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_tick_fails_when_runtime_has_tracked_files() -> None:
    print("\n== Tick rejects tracked runtime content ==")
    tmp = _seed_repo(ignore_runtime=True)
    try:
        (tmp / ".self-evo" / "runtime").mkdir(parents=True)
        forced = tmp / ".self-evo" / "runtime" / "tracked.txt"
        forced.write_text("tracked\n", encoding="utf-8")
        _git(tmp, "add", "-f", ".self-evo/runtime/tracked.txt")
        _git(tmp, "commit", "-m", "force tracked runtime")
        blocked = False
        try:
            tick.run_noop_tick(tmp, run_id="run-001")
        except tick.RuntimeBoundaryError as exc:
            blocked = "tracked files" in str(exc)
        expect("tracked runtime content blocks tick", blocked)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_noop_tick_creates_expected_artifacts() -> None:
    print("\n== No-op tick artifact contract ==")
    tmp = _seed_repo(ignore_runtime=True)
    try:
        summary = tick.run_noop_tick(tmp, run_id="2026-06-28T00-00-00Z")
        run_dir = tmp / summary["run_dir"]
        expected = {"input.json", "decision.md", "result.json"}
        actual = {p.name for p in run_dir.iterdir()}
        expect("required files exist", expected <= actual, str(sorted(actual)))

        result = json.loads((run_dir / "result.json").read_text(encoding="utf-8"))
        input_payload = json.loads((run_dir / "input.json").read_text(encoding="utf-8"))
        expect("result status is noop", result.get("status") == "noop", str(result))
        expect("result outcome is no_suitable_issue",
               result.get("outcome") == "no_suitable_issue", str(result))
        expect("selected_issue is null", result.get("selected_issue") is None, str(result))
        expect("input stage is R", input_payload.get("stage") == "R", str(input_payload))
        expect("input mode is noop", input_payload.get("mode") == "noop", str(input_payload))
        expect("GitHub fetch is explicitly deferred",
               input_payload.get("github", {}).get("mode") == "not_implemented_in_pr1",
               str(input_payload))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_noop_tick_rejects_existing_run_dir() -> None:
    print("\n== No-op tick refuses to overwrite run directories ==")
    tmp = _seed_repo(ignore_runtime=True)
    try:
        tick.run_noop_tick(tmp, run_id="same-run")
        blocked = False
        try:
            tick.run_noop_tick(tmp, run_id="same-run")
        except tick.RuntimeBoundaryError as exc:
            blocked = "already exists" in str(exc)
        expect("second tick with same run_id is blocked", blocked)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_noop_tick_does_not_create_tracked_diff() -> None:
    print("\n== No-op tick leaves tracked diff clean ==")
    tmp = _seed_repo(ignore_runtime=True)
    try:
        tick.run_noop_tick(tmp, run_id="run-clean")
        status = _git(tmp, "status", "--porcelain").stdout.strip()
        expect("git status remains clean because runtime is ignored", status == "", repr(status))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_cli_success_json() -> None:
    print("\n== CLI success JSON contract ==")
    tmp = _seed_repo(ignore_runtime=True)
    try:
        proc = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "loop_runtime_tick.py"),
                "--repo-root",
                str(tmp),
                "--run-id",
                "cli-json",
                "--offline-noop",
                "--json",
            ],
            cwd=tmp,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        expect("CLI exits 0", proc.returncode == 0, proc.stderr[:200])
        try:
            payload = json.loads(proc.stdout)
        except ValueError:
            payload = {}
        expect("CLI emits result payload", payload.get("run_id") == "cli-json", proc.stdout[:200])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_cli_boundary_error_json() -> None:
    print("\n== CLI boundary error JSON contract ==")
    tmp = _seed_repo(ignore_runtime=False)
    try:
        proc = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "loop_runtime_tick.py"),
                "--repo-root",
                str(tmp),
                "--run-id",
                "cli-error",
                "--offline-noop",
                "--json",
            ],
            cwd=tmp,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        expect("CLI exits 2 on boundary error", proc.returncode == 2, proc.stdout[:200])
        try:
            payload = json.loads(proc.stdout)
        except ValueError:
            payload = {}
        expect("CLI reports runtime_boundary_violation",
               payload.get("outcome") == "runtime_boundary_violation", str(payload))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _fake_issue(
    number: int = 12,
    *,
    state: str = "OPEN",
    labels: list[str] | None = None,
    assignees: list[str] | None = None,
) -> dict:
    return {
        "number": number,
        "title": "Document Stage R worker output",
        "url": f"https://github.com/Baokai-and-his-agents/self-evo/issues/{number}",
        "state": state,
        "body": "Create runtime-only work artifacts for Stage R.",
        "updatedAt": "2026-06-28T00:00:00Z",
        "assignees": [{"login": login} for login in (assignees or [])],
        "labels": [{"name": label} for label in (labels or ["risk:low"])],
    }


def test_stage_r_no_suitable_issue_writes_reviewed_noop() -> None:
    print("\n== Stage R no suitable issue writes reviewed no-op ==")
    tmp = _seed_repo(ignore_runtime=True)
    try:
        def fetcher(repo_root, *, labels, limit):
            return []

        summary = tick.run_stage_r_tick(tmp, run_id="no-issue", issue_fetcher=fetcher)
        run_dir = tmp / summary["run_dir"]
        result = json.loads((run_dir / "result.json").read_text(encoding="utf-8"))
        review = (run_dir / "review.md").read_text(encoding="utf-8")
        expect("result is noop", result.get("status") == "noop", str(result))
        expect("outcome is no_suitable_issue",
               result.get("outcome") == "no_suitable_issue", str(result))
        expect("review is advisory abstain", "disposition: `abstain`" in review, review)
        expect("no work artifact is written", not (run_dir / "work.md").exists())
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_stage_r_selected_issue_writes_worker_artifacts() -> None:
    print("\n== Stage R selected issue writes worker artifacts ==")
    tmp = _seed_repo(ignore_runtime=True)
    try:
        def fetcher(repo_root, *, labels, limit):
            return [_fake_issue()]

        summary = tick.run_stage_r_tick(tmp, run_id="issue-work", issue_fetcher=fetcher)
        run_dir = tmp / summary["run_dir"]
        expected = {
            "input.json",
            "decision.md",
            "work.md",
            "evidence.md",
            "proposed.patch",
            "review.md",
            "result.json",
        }
        actual = {p.name for p in run_dir.iterdir()}
        result = json.loads((run_dir / "result.json").read_text(encoding="utf-8"))
        expect("full artifact set exists", expected <= actual, str(sorted(actual)))
        expect("selected issue is recorded",
               result.get("selected_issue", {}).get("number") == 12, str(result))
        expect("empty patch requires revision",
               result.get("outcome") == "needs_revision", str(result))
        expect("review verdict requires revision",
               result.get("review_verdict") == "needs_revision", str(result))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_stage_r_valid_patch_can_be_ready_for_promote() -> None:
    print("\n== Stage R valid patch can become ready for promote ==")
    tmp = _seed_repo(ignore_runtime=True)
    try:
        def fetcher(repo_root, *, labels, limit):
            return [_fake_issue()]

        patch_text = "\n".join([
            "diff --git a/README.md b/README.md",
            "index df967b9..8b4e377 100644",
            "--- a/README.md",
            "+++ b/README.md",
            "@@ -1 +1 @@",
            "-base",
            "+base updated",
            "",
        ])
        summary = tick.run_stage_r_tick(
            tmp,
            run_id="valid-patch",
            issue_fetcher=fetcher,
            proposed_patch_text=patch_text,
        )
        run_dir = tmp / summary["run_dir"]
        result = json.loads((run_dir / "result.json").read_text(encoding="utf-8"))
        expect("outcome is ready_for_promote",
               result.get("outcome") == "ready_for_promote", str(result))
        expect("review approves applicable patch",
               result.get("review_verdict") == "approved", str(result))
        expect("patch was not applied to checkout",
               (tmp / "README.md").read_text(encoding="utf-8") == "base\n")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_stage_r_fetch_failed_writes_error_result() -> None:
    print("\n== Stage R fetch failure writes runtime error result ==")
    tmp = _seed_repo(ignore_runtime=True)
    try:
        def fetcher(repo_root, *, labels, limit):
            raise tick.IssueFetchError("network unavailable")

        summary = tick.run_stage_r_tick(tmp, run_id="fetch-failed", issue_fetcher=fetcher)
        run_dir = tmp / summary["run_dir"]
        result = json.loads((run_dir / "result.json").read_text(encoding="utf-8"))
        expect("result status is error", result.get("status") == "error", str(result))
        expect("outcome is fetch_failed", result.get("outcome") == "fetch_failed", str(result))
        expect("error is captured", "network unavailable" in result.get("error", ""), str(result))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_patch_check_valid_and_invalid() -> None:
    print("\n== Patch check valid and invalid patches ==")
    tmp = _seed_repo(ignore_runtime=True)
    try:
        valid_patch = tmp / "valid.patch"
        valid_patch.write_text(
            "\n".join([
                "diff --git a/README.md b/README.md",
                "index df967b9..8b4e377 100644",
                "--- a/README.md",
                "+++ b/README.md",
                "@@ -1 +1 @@",
                "-base",
                "+base updated",
                "",
            ]),
            encoding="utf-8",
        )
        invalid_patch = tmp / "invalid.patch"
        invalid_patch.write_text("not a patch\n", encoding="utf-8")
        valid = tick.check_patch_applicability(tmp, valid_patch)
        invalid = tick.check_patch_applicability(tmp, invalid_patch)
        expect("valid patch is applicable", valid.applicable, str(valid))
        expect("invalid patch is rejected", not invalid.applicable, str(invalid))
        expect("valid check did not apply patch",
               (tmp / "README.md").read_text(encoding="utf-8") == "base\n")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_patch_check_rejects_unsafe_paths() -> None:
    print("\n== Patch check rejects unsafe paths ==")
    tmp = _seed_repo(ignore_runtime=True)
    try:
        unsafe_patch = tmp / "unsafe.patch"
        unsafe_patch.write_text(
            "\n".join([
                "diff --git a/../../escape b/../../escape",
                "--- a/../../escape",
                "+++ b/../../escape",
                "@@ -0,0 +1 @@",
                "+bad",
                "",
            ]),
            encoding="utf-8",
        )
        result = tick.check_patch_applicability(tmp, unsafe_patch)
        expect("unsafe path is rejected", result.status == "unsafe_patch_path", str(result))
        expect("unsafe patch is not applicable", not result.applicable, str(result))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_runtime_review_does_not_mutate_worker_artifacts() -> None:
    print("\n== Runtime review does not mutate worker artifacts ==")
    tmp = _seed_repo(ignore_runtime=True)
    try:
        def fetcher(repo_root, *, labels, limit):
            return [_fake_issue()]

        summary = tick.run_stage_r_tick(tmp, run_id="review-no-mutate", issue_fetcher=fetcher)
        run_dir = tmp / summary["run_dir"]
        before = {
            name: (run_dir / name).read_text(encoding="utf-8")
            for name in ("work.md", "evidence.md", "proposed.patch")
        }
        # Reading review.md should be the only reviewer interaction in PR 2.
        (run_dir / "review.md").read_text(encoding="utf-8")
        after = {
            name: (run_dir / name).read_text(encoding="utf-8")
            for name in ("work.md", "evidence.md", "proposed.patch")
        }
        expect("worker artifacts are unchanged", before == after, str(after))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_stage_r_tick_keeps_tracked_diff_clean() -> None:
    print("\n== Stage R tick keeps tracked diff clean ==")
    tmp = _seed_repo(ignore_runtime=True)
    try:
        def fetcher(repo_root, *, labels, limit):
            return [_fake_issue()]

        tick.run_stage_r_tick(tmp, run_id="tracked-clean", issue_fetcher=fetcher)
        status = _git(tmp, "status", "--porcelain").stdout.strip()
        expect("git status remains clean", status == "", repr(status))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_stage_r_skips_issue_with_assignees() -> None:
    print("\n== Stage R skips an issue that is already assigned ==")
    tmp = _seed_repo(ignore_runtime=True)
    try:
        def fetcher(repo_root, *, labels, limit):
            return [
                _fake_issue(12, assignees=["other-worker"]),
                _fake_issue(13),
            ]

        summary = tick.run_stage_r_tick(tmp, run_id="skip-assigned", issue_fetcher=fetcher)
        run_dir = tmp / summary["run_dir"]
        result = json.loads((run_dir / "result.json").read_text(encoding="utf-8"))
        expect("assigned issue #12 is skipped",
               result.get("selected_issue", {}).get("number") == 13, str(result))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_stage_r_skips_issue_with_active_claim_label() -> None:
    print("\n== Stage R skips an issue carrying a status:running claim ==")
    tmp = _seed_repo(ignore_runtime=True)
    try:
        def fetcher(repo_root, *, labels, limit):
            return [
                _fake_issue(14, labels=["risk:low", "status:running"]),
                _fake_issue(15, labels=["risk:low"]),
            ]

        summary = tick.run_stage_r_tick(tmp, run_id="skip-running", issue_fetcher=fetcher)
        run_dir = tmp / summary["run_dir"]
        result = json.loads((run_dir / "result.json").read_text(encoding="utf-8"))
        expect("status:running issue #14 is skipped",
               result.get("selected_issue", {}).get("number") == 15, str(result))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_stage_r_no_suitable_issue_when_all_claimed() -> None:
    print("\n== Stage R writes no-op when every open issue is claimed ==")
    tmp = _seed_repo(ignore_runtime=True)
    try:
        def fetcher(repo_root, *, labels, limit):
            return [
                _fake_issue(16, assignees=["worker-a"]),
                _fake_issue(17, labels=["risk:low", "status:claimed"]),
                _fake_issue(18, labels=["risk:low", "status:blocked"]),
            ]

        summary = tick.run_stage_r_tick(tmp, run_id="all-claimed", issue_fetcher=fetcher)
        run_dir = tmp / summary["run_dir"]
        result = json.loads((run_dir / "result.json").read_text(encoding="utf-8"))
        expect("result is noop when all issues claimed",
               result.get("status") == "noop", str(result))
        expect("outcome is no_suitable_issue",
               result.get("outcome") == "no_suitable_issue", str(result))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_stage_r_project_filter_restricts_issue_pool() -> None:
    print("\n== Stage R --project adds a project:<name> label filter ==")
    tmp = _seed_repo(ignore_runtime=True)
    try:
        seen_labels: dict = {}

        def fetcher(repo_root, *, labels, limit):
            seen_labels["labels"] = list(labels)
            return []  # no issues -> noop, we only assert the filter here

        tick.run_stage_r_tick(
            tmp, run_id="project-filter", issue_fetcher=fetcher,
            project="fx-strategy-research",
        )
        expect("project filter injected as label",
               "project:fx-strategy-research" in seen_labels["labels"],
               str(seen_labels))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_stage_r_project_filter_combines_with_other_labels() -> None:
    print("\n== Stage R --project combines with --label (AND semantics) ==")
    tmp = _seed_repo(ignore_runtime=True)
    try:
        seen_labels: dict = {}

        def fetcher(repo_root, *, labels, limit):
            seen_labels["labels"] = list(labels)
            return []

        tick.run_stage_r_tick(
            tmp, run_id="project-and-label", issue_fetcher=fetcher,
            labels=["risk:low"], project="self-evo",
        )
        expect("both risk:low and project:self-evo present",
               "risk:low" in seen_labels["labels"]
               and "project:self-evo" in seen_labels["labels"],
               str(seen_labels))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_stage_r_no_project_keeps_global_pool() -> None:
    print("\n== Stage R without --project keeps the global issue pool ==")
    tmp = _seed_repo(ignore_runtime=True)
    try:
        seen_labels: dict = {}

        def fetcher(repo_root, *, labels, limit):
            seen_labels["labels"] = list(labels)
            return []

        tick.run_stage_r_tick(tmp, run_id="no-project", issue_fetcher=fetcher)
        expect("no project label injected",
               not any(l.startswith("project:") for l in seen_labels["labels"]),
               str(seen_labels))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_gh_issue_list_command_is_read_only() -> None:
    print("\n== GitHub issue list command is read-only ==")
    cmd = tick.build_gh_issue_list_command(labels=["risk:low", "loop"], limit=5)
    text = " ".join(cmd)
    expect("uses gh issue list", cmd[:3] == ["gh", "issue", "list"], text)
    for forbidden in ("create", "edit", "close", "comment", "pr"):
        expect(f"does not contain write verb: {forbidden}", forbidden not in cmd, text)
    expect("labels are included", cmd.count("--label") == 2, text)


def main() -> int:
    print("self-evo Stage R runtime tick tests")
    test_runtime_writer_allows_runtime_writes()
    test_runtime_writer_rejects_outside_runtime()
    test_runtime_writer_rejects_absolute_path()
    test_runtime_writer_rejects_bad_run_id()
    test_runtime_writer_rejects_symlink_runtime()
    test_tick_fails_when_runtime_not_ignored()
    test_tick_fails_when_runtime_has_tracked_files()
    test_noop_tick_creates_expected_artifacts()
    test_noop_tick_rejects_existing_run_dir()
    test_noop_tick_does_not_create_tracked_diff()
    test_cli_success_json()
    test_cli_boundary_error_json()
    test_stage_r_no_suitable_issue_writes_reviewed_noop()
    test_stage_r_selected_issue_writes_worker_artifacts()
    test_stage_r_valid_patch_can_be_ready_for_promote()
    test_stage_r_fetch_failed_writes_error_result()
    test_patch_check_valid_and_invalid()
    test_patch_check_rejects_unsafe_paths()
    test_runtime_review_does_not_mutate_worker_artifacts()
    test_stage_r_tick_keeps_tracked_diff_clean()
    test_stage_r_skips_issue_with_assignees()
    test_stage_r_skips_issue_with_active_claim_label()
    test_stage_r_no_suitable_issue_when_all_claimed()
    test_stage_r_project_filter_restricts_issue_pool()
    test_stage_r_project_filter_combines_with_other_labels()
    test_stage_r_no_project_keeps_global_pool()
    test_gh_issue_list_command_is_read_only()
    print("\n" + "=" * 48)
    print(f"RESULT: {PASS} passed, {FAIL} failed")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
