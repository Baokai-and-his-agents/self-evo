<#
.SYNOPSIS
  Windows PowerShell entrypoint for the self-evo PreToolUse hook (Issue #5).

.DESCRIPTION
  Thin wrapper around scripts/hooks/pretooluse.py (single source of truth).
  Reads the Claude Code PreToolUse payload from stdin, writes the decision JSON
  to stdout, and exits 0 (allow) or 2 (block).

  Wire in .claude/settings.json (Windows) as:
    "hooks": { "PreToolUse": [ { "matcher": "*", "hooks": [
      { "type": "command",
        "command": "pwsh -NoProfile -File scripts/hooks/pretool-use.ps1" } ] } ] }

  Requires Python 3 on PATH (documented prerequisite; not installed by the agent).
#>

$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$target = Join-Path $here "pretooluse.py"

function Resolve-Python {
    foreach ($cand in @("python", "python3")) {
        $f = Get-Command $cand -ErrorAction SilentlyContinue
        if ($f) { return $cand }
    }
    $py = Get-Command py -ErrorAction SilentlyContinue
    if ($py) { return "py -3" }
    throw "Python 3 not found on PATH."
}

# Forward stdin to the python child so the JSON payload passes through unchanged.
$py = Resolve-Python
$input | & cmd /c "$py `"$target`""
exit $LASTEXITCODE
