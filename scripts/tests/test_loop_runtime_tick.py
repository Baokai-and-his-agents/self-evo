#!/usr/bin/env python3
"""Tests for the Stage R runtime-confined no-op tick."""

from __future__ import annotations

import json
import os
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
    print("\n" + "=" * 48)
    print(f"RESULT: {PASS} passed, {FAIL} failed")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
