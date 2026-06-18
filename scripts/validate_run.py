#!/usr/bin/env python3
"""Read-only run validator for self-evo (MVP 1.5, Issue #5).

Manually executable:
    python3 scripts/validate_run.py            # human-readable
    python3 scripts/validate_run.py --json     # machine-readable

It reports structured PASS / WARN / BLOCK findings for the lifecycle checks
required by Issue #5 section A. It is strictly read-only: it never repairs,
commits, or mutates task state. Findings are computed from live repo state
(git + gh) plus the local coordination mirrors under state/ and data/.

Finding schema:
    {"check", "level": "PASS"|"WARN"|"BLOCK", "detail"}
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _policy  # noqa: E402

REPO_ROOT = _policy.REPO_ROOT

# Map a level to an exit-ish severity for human display; programmatic callers
# should read the JSON and inspect the highest BLOCK/WARN themselves.
LEVEL_ORDER = {"PASS": 0, "WARN": 1, "BLOCK": 2}


# --------------------------------------------------------------------------- #
# Shell helpers                                                               #
# --------------------------------------------------------------------------- #

def _git(args: list[str]) -> str:
    try:
        out = subprocess.run(
            ["git", *args], cwd=REPO_ROOT, capture_output=True, text=True, timeout=10
        )
        if out.returncode != 0:
            return ""
        # rstrip (not strip): the leading space in `git status --porcelain`
        # output (' M path') is significant; stripping it would shift the
        # column-based path parse by one character.
        return out.stdout.rstrip()
    except (OSError, subprocess.SubprocessError):
        return ""


def _gh(args: list[str]) -> str:
    try:
        out = subprocess.run(
            ["gh", *args], cwd=REPO_ROOT, capture_output=True, text=True, timeout=15
        )
        return out.stdout.strip() if out.returncode == 0 else ""
    except (OSError, subprocess.SubprocessError):
        return ""


def _read_json(path: str) -> dict | None:
    full = os.path.join(REPO_ROOT, path)
    try:
        with open(full, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


def _file_exists(rel: str) -> bool:
    return os.path.exists(os.path.join(REPO_ROOT, rel))


# --------------------------------------------------------------------------- #
# State accessors                                                             #
# --------------------------------------------------------------------------- #

def current_branch() -> str:
    return _git(["rev-parse", "--abbrev-ref", "HEAD"])


def changed_tracked_files() -> list[str]:
    """Repo-relative paths of tracked files that are staged or modified."""
    out = _git(["status", "--porcelain"])
    files: list[str] = []
    for line in out.splitlines():
        if not line.strip():
            continue
        # porcelain v1: "XY path" or "XY orig -> path"
        path = line[3:].strip()
        if "->" in path:
            path = path.split("->", 1)[1].strip()
        files.append(path.strip('"'))
    return [f for f in files if f]


def issue_labels(issue_number: int) -> list[str]:
    raw = _gh(["issue", "view", str(issue_number), "--json", "labels"])
    try:
        return [l["name"] for l in json.loads(raw).get("labels", [])]
    except ValueError:
        return []


def has_draft_pr_for_branch(branch: str) -> bool:
    raw = _gh(["pr", "list", "--head", branch, "--state", "open",
               "--json", "number,isDraft,title"])
    try:
        prs = json.loads(raw)
    except ValueError:
        prs = []
    return any(pr.get("number") for pr in prs)


def claim_for_issue(issue_number: int) -> dict | None:
    return _read_json(f"state/claims/{issue_number}.json")


def heartbeat() -> dict | None:
    return _read_json("state/heartbeat.json")


def run_summaries_for_today(date_str: str) -> list[str]:
    d = os.path.join(REPO_ROOT, "data", "runs", date_str)
    if not os.path.isdir(d):
        return []
    return sorted(f for f in os.listdir(d) if f.endswith(".summary.md"))


def tasks_md_status(issue_number: int) -> str | None:
    """Coarse parse of data/tasks/TASKS.md for the section an issue sits in."""
    full = os.path.join(REPO_ROOT, "data", "tasks", "TASKS.md")
    try:
        with open(full, "r", encoding="utf-8") as fh:
            text = fh.read()
    except OSError:
        return None
    needle = f"Issue #{issue_number}"
    current = None
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            current = stripped[3:].strip()
        if needle in line:
            return current
    return None


# --------------------------------------------------------------------------- #
# Checks                                                                      #
# --------------------------------------------------------------------------- #

def check_branch_is_agent(policy) -> dict:
    branch = current_branch()
    prefix = policy["branches"]["agent_prefix"]
    ok = branch.startswith(prefix)
    return {
        "check": "branch_is_agent_branch",
        "level": "PASS" if ok else "BLOCK",
        "detail": f"current branch '{branch}' "
                  f"{'matches' if ok else 'does NOT match'} agent prefix '{prefix}'",
    }


def check_claim_exists(issue_number: int) -> dict:
    claim = claim_for_issue(issue_number)
    ok = bool(claim) and claim.get("issue") == issue_number
    return {
        "check": "issue_claim_exists",
        "level": "PASS" if ok else "BLOCK",
        "detail": (f"state/claims/{issue_number}.json present for issue #{issue_number}"
                   if ok else f"no valid claim record at state/claims/{issue_number}.json"),
    }


def check_changed_files_have_draft_pr(issue_number: int, branch: str) -> dict:
    changed = changed_tracked_files()
    if not changed:
        return {"check": "changed_files_have_draft_pr", "level": "PASS",
                "detail": "no tracked file changes; draft PR not required"}
    has_pr = has_draft_pr_for_branch(branch)
    return {
        "check": "changed_files_have_draft_pr",
        "level": "PASS" if has_pr else "BLOCK",
        "detail": (f"{len(changed)} changed tracked file(s); draft PR for branch "
                   f"'{branch}' {'found' if has_pr else 'NOT found'}"),
    }


def check_run_summary_exists(date_str: str) -> dict:
    sums = run_summaries_for_today(date_str)
    ok = bool(sums)
    return {
        "check": "run_summary_exists",
        "level": "PASS" if ok else "WARN",
        "detail": (f"data/runs/{date_str}/ has {len(sums)} summary file(s)"
                   if ok else f"no run summary under data/runs/{date_str}/"),
    }


def check_review_has_released_claim(issue_number: int) -> dict:
    labels = issue_labels(issue_number)
    in_review = any(l == "status:review" for l in labels)
    claim = claim_for_issue(issue_number)
    if not in_review:
        return {"check": "review_has_released_claim", "level": "PASS",
                "detail": f"issue #{issue_number} not in status:review; n/a"}
    released = claim and claim.get("status") in ("released", "review")
    return {
        "check": "review_has_released_claim",
        "level": "PASS" if released else "BLOCK",
        "detail": (f"issue in status:review; claim status='{claim.get('status') if claim else None}'"
                   if claim else "issue in status:review but no claim record"),
    }


def check_heartbeat_idle_before_review(issue_number: int) -> dict:
    labels = issue_labels(issue_number)
    in_review = any(l == "status:review" for l in labels)
    hb = heartbeat() or {"workers": []}
    mine = next((w for w in hb.get("workers", [])
                 if w.get("issue") == issue_number), None)
    if not in_review:
        return {"check": "heartbeat_idle_before_review", "level": "PASS",
                "detail": "issue not in review; n/a"}
    idle = mine and mine.get("status") in ("idle", "stopped")
    return {
        "check": "heartbeat_idle_before_review",
        "level": "PASS" if idle else "BLOCK",
        "detail": (f"heartbeat status='{mine.get('status') if mine else None}'"
                   if mine else "no heartbeat entry for this issue"),
    }


def check_tasks_md_matches_issue(issue_number: int) -> dict:
    section = tasks_md_status(issue_number)
    labels = issue_labels(issue_number)
    if "status:review" in labels:
        want = "Review"
    elif "status:claimed" in labels or "status:running" in labels:
        want = "Claimed"
    elif "status:done" in labels:
        want = "Done"
    elif "status:open" in labels:
        want = "Open"
    else:
        return {"check": "tasks_md_matches_issue", "level": "WARN",
                "detail": f"issue #{issue_number} has no recognized status label"}
    ok = section == want
    return {
        "check": "tasks_md_matches_issue",
        "level": "PASS" if ok else "WARN",
        "detail": f"TASKS.md section='{section}', expected '{want}' for issue labels {labels}",
    }


def check_changed_files_within_authorized(policy) -> dict:
    changed = changed_tracked_files()
    bad: list[str] = []
    for f in changed:
        zone = _policy.classify_path(f, policy)
        if zone in ("read_only", "proposal_required", "protected_claude_config",
                    "outside"):
            bad.append(f"{f} ({zone})")
    if not bad:
        return {"check": "changed_files_within_authorized_paths", "level": "PASS",
                "detail": f"all {len(changed)} changed file(s) within authorized paths"}
    return {
        "check": "changed_files_within_authorized_paths",
        "level": "BLOCK",
        "detail": "changed files outside authorized write zones: " + "; ".join(bad),
    }


def check_no_unauthorized_rules_changes() -> dict:
    """No rules/** edits should appear among tracked changes on an agent branch."""
    changed = changed_tracked_files()
    rules = [f for f in changed if f.replace("\\", "/").startswith("rules/")]
    if not rules:
        return {"check": "no_unauthorized_rules_changes", "level": "PASS",
                "detail": "no rules/** changes detected"}
    return {
        "check": "no_unauthorized_rules_changes",
        "level": "BLOCK",
        "detail": "rules/** must not be edited by the worker: " + "; ".join(rules),
    }


# --------------------------------------------------------------------------- #
# Orchestration                                                               #
# --------------------------------------------------------------------------- #

def collect_findings(policy, *, issue_number: int, date_str: str) -> list[dict]:
    branch = current_branch()
    return [
        check_branch_is_agent(policy),
        check_claim_exists(issue_number),
        check_changed_files_have_draft_pr(issue_number, branch),
        check_run_summary_exists(date_str),
        check_review_has_released_claim(issue_number),
        check_heartbeat_idle_before_review(issue_number),
        check_tasks_md_matches_issue(issue_number),
        check_changed_files_within_authorized(policy),
        check_no_unauthorized_rules_changes(),
    ]


def summarize(findings: list[dict]) -> dict:
    levels = [f["level"] for f in findings]
    return {
        "total": len(findings),
        "pass": levels.count("PASS"),
        "warn": levels.count("WARN"),
        "block": levels.count("BLOCK"),
        "worst": max((LEVEL_ORDER[l] for l in levels), default=0),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="self-evo read-only run validator")
    ap.add_argument("--issue", type=int, default=5,
                    help="GitHub issue number to validate (default: 5)")
    ap.add_argument("--date", default=None,
                    help="run date YYYY-MM-DD (default: today from system clock)")
    ap.add_argument("--json", action="store_true", help="emit JSON only")
    args = ap.parse_args()

    date_str = args.date or _today()
    policy = _policy.load_policy()
    findings = collect_findings(policy, issue_number=args.issue, date_str=date_str)
    summary = summarize(findings)

    if args.json:
        sys.stdout.write(json.dumps({
            "issue": args.issue, "date": date_str, "summary": summary,
            "findings": findings,
        }, indent=2))
        return 0

    print(f"self-evo run validator — issue #{args.issue} — {date_str}")
    print("-" * 64)
    for f in findings:
        print(f"[{f['level']:5}] {f['check']}: {f['detail']}")
    print("-" * 64)
    print(f"PASS={summary['pass']} WARN={summary['warn']} BLOCK={summary['block']}"
          f" (worst={_worst_name(summary['worst'])})")
    return 0


def _today() -> str:
    # Determinism note: the validator is read-only and reflects live state; the
    # date only selects which run-summary directory to look at.
    import datetime
    return datetime.date.today().isoformat()


def _worst_name(idx: int) -> str:
    return {0: "PASS", 1: "WARN", 2: "BLOCK"}.get(idx, "?")


if __name__ == "__main__":
    sys.exit(main())
