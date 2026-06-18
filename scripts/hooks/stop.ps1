<#
.SYNOPSIS
  Windows PowerShell entrypoint for the self-evo Stop hook (Issue #5).

.DESCRIPTION
  Thin wrapper around scripts/hooks/stop.py (single source of truth). Reads the
  Stop payload from stdin, runs lifecycle validation, writes the explanation to
  stderr, and exits 0 (allow stop) or 2 (block stop, full-enforce only).

  Wire in .claude/settings.json (Windows) as:
    "hooks": { "Stop": [ { "matcher": "", "hooks": [
      { "type": "command",
        "command": "pwsh -NoProfile -File scripts/hooks/stop.ps1" } ] } ] }

  Escape hatch: set env SELF_EVO_STOP_GUARD=1 to allow stop unconditionally
  (used to break a Stop-hook loop when a blocker requires human action).

  Requires Python 3 on PATH (documented prerequisite; not installed by the agent).
#>

$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$target = Join-Path $here "stop.py"

function Resolve-Python {
    foreach ($cand in @("python", "python3")) {
        $f = Get-Command $cand -ErrorAction SilentlyContinue
        if ($f) { return $cand }
    }
    $py = Get-Command py -ErrorAction SilentlyContinue
    if ($py) { return "py -3" }
    throw "Python 3 not found on PATH."
}

$py = Resolve-Python
$input | & cmd /c "$py `"$target`""
exit $LASTEXITCODE
