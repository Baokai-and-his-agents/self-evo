#!/usr/bin/env python3
"""Read-only run validator for self-evo (MVP 1.5, Issue #5).

Manually executable:
    python scripts/validate_run.py            # human-readable
    python scripts/validate_run.py --json     # machine-readable

It reports structured PASS / WARN / BLOCK findings for the lifecycle checks
required by Issue #5 section A. It is strictly read-only: it never repairs,
commits, or mutates task state. Findings are computed from live repo state
(git + gh) plus the local coordination mirrors under state/ and data/.

Finding schema:
    {"check", "level": "PASS"|"WARN"|"BLOCK", "detail"}
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _policy  # noqa: E402

REPO_ROOT = _policy.REPO_ROOT

# Map a level to an exit-ish severity for human display; programmatic callers
# should read the JSON and inspect the highest BLOCK/WARN themselves.
LEVEL_ORDER = {"PASS": 0, "WARN": 1, "BLOCK": 2}

BASE_REF_ENV = "SELF_EVO_BASE_REF"


# --------------------------------------------------------------------------- #
# Shell helpers                                                               #
# --------------------------------------------------------------------------- #
#
# subprocess decoding: on Windows (especially a Chinese/GBK locale) the default
# text-mode decoder is the system ANSI codepage (GBK), which raises
# UnicodeDecodeError on git/gh UTF-8 output and can leave CompletedProcess.stdout
# as None. We therefore decode explicitly as UTF-8 with errors="replace" (safe,
# lossy fallback) and treat any None output as an empty string. This makes the
# validator run successfully on a Windows/GBK machine (Issue #5 review item 3).

def _run(cmd_args: list[str], *, timeout: int) -> tuple[str, int]:
    """Run a command, returning (stdout_text, returncode).

    Always returns a string (never None) and never raises on a decoding or
    subprocess error — callers get "" on any failure so the read-only validator
    degrades to empty data instead of crashing.
    """
    try:
        proc = subprocess.run(
            cmd_args, cwd=REPO_ROOT, capture_output=True,
            text=True, encoding="utf-8", errors="replace", timeout=timeout,
        )
    except (OSError, subprocess.SubprocessError):
        return "", 1
    out = proc.stdout if proc.stdout is not None else ""
    return out, proc.returncode


def _git(args: list[str]) -> str:
    out, rc = _run(["git", *args], timeout=10)
    if rc != 0:
        return ""
    # rstrip (not strip): the leading space in `git status --porcelain`
    # output (' M path') is significant; stripping it would shift the
    # column-based path parse by one character.
    return out.rstrip()


def _gh(args: list[str]) -> str:
    out, rc = _run(["gh", *args], timeout=15)
    return out.strip() if rc == 0 else ""


def _read_json(path: str) -> dict | None:
    full = os.path.join(REPO_ROOT, path)
    try:
        with open(full, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


# --------------------------------------------------------------------------- #
# State accessors                                                             #
# --------------------------------------------------------------------------- #

def current_branch() -> str:
    return _git(["rev-parse", "--abbrev-ref", "HEAD"])


def _ref_exists(ref: str) -> bool:
    out, rc = _run(["git", "rev-parse", "--verify", "--quiet", ref + "^{commit}"],
                   timeout=10)
    return rc == 0 and bool(out.strip())


def resolve_base_ref(policy: dict) -> str | None:
    """Resolve the PR base ref robustly for local and CI/agent worktrees.

    Order: SELF_EVO_BASE_REF env > origin/<protected> (default origin/main) >
    <protected> local ref > upstream/main. Returns None if no base can be
    resolved (shallow/sparse clone with no main) so the caller can WARN.
    """
    candidates: list[str] = []
    env_base = os.environ.get(BASE_REF_ENV)
    if env_base:
        candidates.append(env_base)
    protected = policy.get("branches", {}).get("protected", []) or ["main"]
    for b in protected:
        candidates.append(f"origin/{b}")
    for b in protected:
        candidates.append(b)
    candidates.append("upstream/main")
    for c in candidates:
        if _ref_exists(c):
            return c
    return None


def committed_changed_files(base_ref: str | None) -> list[str]:
    """Files changed on the branch relative to base (committed). NUL-safe.

    Triple-dot (base...HEAD) yields the changes reachable from HEAD since the
    merge-base with base — exactly the PR diff. Returns [] if base is None.
    """
    if not base_ref:
        return []
    out = _git(["-c", "core.quotepath=false", "diff", "--name-only", "-z",
                f"{base_ref}...HEAD"])
    return [p for p in out.split("\0") if p]


def workingtree_changed_files() -> list[str]:
    """Staged + unstaged + untracked + renamed + deleted files (NUL-safe)."""
    out = _git(["-c", "core.quotepath=false", "status", "--porcelain", "-z"])
    parts = out.split("\0")
    files: list[str] = []
    i = 0
    while i < len(parts):
        field = parts[i]
        if not field:
            i += 1
            continue
        if len(field) < 3:
            i += 1
            continue
        status = field[:2]
        path = field[3:]
        files.append(path.strip('"'))
        i += 1
        # Renames/copies carry a second NUL-separated field (the source path).
        if "R" in status or "C" in status:
            i += 1
    return [f for f in files if f]


def changed_files(policy: dict | None = None) -> list[str]:
    """Union of committed branch changes and working-tree changes, normalized.

    A clean committed PR branch no longer appears to have zero changes: the
    committed diff vs the base ref is included. (Issue #5 review item 1.)
    """
    pol = policy if policy is not None else _policy.load_policy()
    base = resolve_base_ref(pol)
    combined = committed_changed_files(base) + workingtree_changed_files()
    norm = sorted({_policy._norm(f) for f in combined if f})
    return norm


def changed_files_base_resolvable(policy: dict) -> bool:
    """Whether a base ref could be resolved (for the changed-files WARN detail)."""
    return resolve_base_ref(policy) is not None


def issue_labels(issue_number: int) -> list[str]:
    raw = _gh(["issue", "view", str(issue_number), "--json", "labels"])
    try:
        return [l["name"] for l in json.loads(raw).get("labels", [])]
    except (ValueError, TypeError):
        return []


def has_draft_pr_for_branch(branch: str) -> bool:
    """True only when an OPEN PR for the branch is a DRAFT (isDraft == true).

    A ready/non-draft PR does not satisfy the 'changes need a draft PR' gate,
    because the whole point is that unreviewed agent changes stay draft.
    (Issue #5 review item 6.)
    """
    raw = _gh(["pr", "list", "--head", branch, "--state", "open",
               "--json", "number,isDraft,title"])
    try:
        prs = json.loads(raw)
    except (ValueError, TypeError):
        return False
    return any(pr.get("number") and pr.get("isDraft") is True for pr in prs)


def claim_for_issue(issue_number: int) -> dict | None:
    return _read_json(f"state/claims/{issue_number}.json")


def _all_claims() -> list[dict]:
    claims_dir = os.path.join(REPO_ROOT, "state", "claims")
    out: list[dict] = []
    if not os.path.isdir(claims_dir):
        return out
    for fn in sorted(os.listdir(claims_dir)):
        if not fn.endswith(".json"):
            continue
        data = _read_json(f"state/claims/{fn}")
        if data and data.get("issue") is not None:
            out.append(data)
    return out


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
# Issue / run identity derivation                                             #
# --------------------------------------------------------------------------- #

def issue_from_branch(branch: str) -> int | None:
    """Parse the leading issue number from an agent branch name.

    e.g. 'agent/local-code-worker-01/5-hooks-validator' -> 5.
    """
    if not branch:
        return None
    last = branch.replace("\\", "/").rsplit("/", 1)[-1]
    m = re.match(r"(\d+)", last)
    return int(m.group(1)) if m else None


def issue_from_coordination() -> tuple[int | None, str]:
    """Derive the issue from state/claims/** when the branch can't say.

    Prefers a claim whose branch matches the current branch; falls back to a
    sole claim record; reports ambiguity when several claims exist and none
    match. (Issue #5 review item 8.)
    """
    branch = current_branch()
    claims = _all_claims()
    matching = [c for c in claims if c.get("branch") == branch]
    if len(matching) == 1:
        return matching[0]["issue"], f"from claim matching branch '{branch}'"
    if len(claims) == 1:
        return claims[0]["issue"], "from sole claim record"
    if len(claims) > 1:
        return None, (f"ambiguous: {len(claims)} claim records; none match "
                      f"branch '{branch}'")
    return None, "no claim records under state/claims/"


def derive_current_issue(policy: dict) -> tuple[int | None, str]:
    """Resolve the active issue: SELF_EVO_ISSUE env > agent branch > claim.

    Standard Claude Stop payloads carry no issue field, so the Stop hook relies
    on this. Returns (issue_or_None, explanation). (Issue #5 review item 8.)
    """
    env = os.environ.get("SELF_EVO_ISSUE")
    if env and env.strip().isdigit():
        return int(env.strip()), f"from env SELF_EVO_ISSUE={env.strip()}"
    branch = current_branch()
    iss = issue_from_branch(branch)
    if iss:
        return iss, f"derived from agent branch '{branch}'"
    iss2, why = issue_from_coordination()
    if iss2:
        return iss2, why
    return None, ("could not determine issue: SELF_EVO_ISSUE unset, branch "
                  f"'{branch}' has no leading issue number, and {why}")


def _parse_run_id(run_id: str) -> dict:
    """Split a run_id like '2026-06-18-run-002' into date + token."""
    m = re.match(r"^(\d{4}-\d{2}-\d{2})-run-(\d+)$", str(run_id))
    if m:
        return {"run_id": run_id, "date": m.group(1), "token": f"run-{m.group(2)}"}
    return {"run_id": run_id, "date": None, "token": None}


def active_run_identity(issue_number: int) -> dict | None:
    """Derive the active run identity from the claim (then heartbeat).

    Used so that an unrelated run-001 summary does not satisfy run-002.
    (Issue #5 review item 7.)
    """
    claim = claim_for_issue(issue_number) or {}
    run_id = claim.get("run_id")
    if not run_id:
        hb = heartbeat() or {}
        w = next((w for w in hb.get("workers", [])
                  if w.get("issue") == issue_number), None)
        if w:
            run_id = w.get("run_id")
    if not run_id:
        return None
    return _parse_run_id(run_id)


def _summary_references(rel_dir: str, filename: str, ident: dict,
                        issue_number: int) -> bool:
    """True if a summary file's content names the run_id or the issue."""
    full = os.path.join(REPO_ROOT, "data", "runs", rel_dir, filename)
    try:
        with open(full, "r", encoding="utf-8") as fh:
            text = fh.read()
    except OSError:
        return False
    run_id = ident.get("run_id")
    if run_id and run_id in text:
        return True
    # Issue references: 'issue: 5', '#5', 'Issue #5'.
    return (f"issue: {issue_number}" in text
            or f"#{issue_number}" in text
            or f"Issue #{issue_number}" in text)


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


def check_changed_files_have_draft_pr(policy, issue_number: int, branch: str) -> dict:
    changed = changed_files(policy)
    base_ok = changed_files_base_resolvable(policy)
    if not changed:
        if base_ok:
            return {"check": "changed_files_have_draft_pr", "level": "PASS",
                    "detail": "no branch or working-tree changes; draft PR not required"}
        return {"check": "changed_files_have_draft_pr", "level": "WARN",
                "detail": (f"no changes detected and base ref could not be resolved "
                           f"(set {BASE_REF_ENV} or ensure origin/main is present); "
                           "draft PR gate skipped")}
    has_pr = has_draft_pr_for_branch(branch)
    pr_detail = ("found" if has_pr
                 else "NOT found (a ready/open non-draft PR does not satisfy this gate)")
    return {
        "check": "changed_files_have_draft_pr",
        "level": "PASS" if has_pr else "BLOCK",
        "detail": (f"{len(changed)} changed file(s) vs base; DRAFT PR for branch "
                   f"'{branch}' {pr_detail}"),
    }


def check_run_summary_exists(issue_number: int, date_str: str) -> dict:
    ident = active_run_identity(issue_number)
    if not ident:
        return {
            "check": "run_summary_exists", "level": "WARN",
            "detail": (f"no run_id in claim/heartbeat for issue #{issue_number}; "
                       "cannot verify a run-specific summary (record run_id in the "
                       "claim, or set SELF_EVO_ISSUE)"),
        }
    # Look under the identity's own date first, then the supplied date.
    dates = []
    if ident.get("date"):
        dates.append(ident["date"])
    if date_str not in dates:
        dates.append(date_str)
    summaries: list[str] = []
    for d in dates:
        summaries += run_summaries_for_today(d)
    summaries = sorted(set(summaries))
    token = ident.get("token")
    matched = []
    for d in dates:
        for s in run_summaries_for_today(d):
            if s in matched:
                continue
            if token and (s == f"{token}.summary.md" or s.startswith(f"{token}.")):
                matched.append(s)
            elif _summary_references(d, s, ident, issue_number):
                matched.append(s)
    if matched:
        return {"check": "run_summary_exists", "level": "PASS",
                "detail": f"run summary for {ident['run_id']} found: {', '.join(matched)}"}
    if summaries:
        return {
            "check": "run_summary_exists", "level": "WARN",
            "detail": (f"{len(summaries)} summary file(s) present but none match "
                       f"run identity {ident['run_id']} (token '{token}'); an "
                       f"unrelated summary does NOT satisfy this run: {', '.join(summaries)}"),
        }
    return {"check": "run_summary_exists", "level": "WARN",
            "detail": f"no run summary under data/runs/{ident.get('date') or date_str}/"}


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
    changed = changed_files(policy)
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
    policy = _policy.load_policy()
    changed = changed_files(policy)
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
        check_changed_files_have_draft_pr(policy, issue_number, branch),
        check_run_summary_exists(issue_number, date_str),
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


def _today() -> str:
    # Determinism note: the validator is read-only and reflects live state; the
    # date only selects which run-summary directory to look at.
    return datetime.date.today().isoformat()


def _worst_name(idx: int) -> str:
    return {0: "PASS", 1: "WARN", 2: "BLOCK"}.get(idx, "?")


def main() -> int:
    ap = argparse.ArgumentParser(description="self-evo read-only run validator")
    ap.add_argument("--issue", type=int, default=None,
                    help="GitHub issue number to validate "
                         "(default: derive from SELF_EVO_ISSUE / agent branch / claim)")
    ap.add_argument("--date", default=None,
                    help="run date YYYY-MM-DD (default: today from system clock)")
    ap.add_argument("--json", action="store_true", help="emit JSON only")
    args = ap.parse_args()

    date_str = args.date or _today()
    policy = _policy.load_policy()

    issue_number = args.issue
    issue_source = "explicit --issue"
    if issue_number is None:
        issue_number, issue_source = derive_current_issue(policy)
    if issue_number is None:
        msg = (f"self-evo validator: {issue_source}. Pass --issue N or set "
               f"SELF_EVO_ISSUE, or run on an agent/ branch named '<N>-...'.")
        if args.json:
            sys.stdout.write(json.dumps(
                {"error": "issue_undetermined", "detail": msg}))
        else:
            sys.stderr.write(msg + "\n")
        return 2

    findings = collect_findings(policy, issue_number=issue_number, date_str=date_str)
    summary = summarize(findings)

    if args.json:
        sys.stdout.write(json.dumps({
            "issue": issue_number, "issue_source": issue_source,
            "date": date_str, "summary": summary, "findings": findings,
        }, indent=2))
        return 0

    print(f"self-evo run validator -- issue #{issue_number} ({issue_source}) -- {date_str}")
    print("-" * 64)
    for f in findings:
        print(f"[{f['level']:5}] {f['check']}: {f['detail']}")
    print("-" * 64)
    print(f"PASS={summary['pass']} WARN={summary['warn']} BLOCK={summary['block']}"
          f" (worst={_worst_name(summary['worst'])})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
