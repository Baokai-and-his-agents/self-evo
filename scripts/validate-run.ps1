<#
.SYNOPSIS
  Windows PowerShell entrypoint for the self-evo run validator (Issue #5).

.DESCRIPTION
  Thin wrapper. The canonical implementation is scripts/validate_run.py (a
  single source of truth shared with the hooks and the offline tests). This
  .ps1 exists because Issue #5 prefers a PowerShell entrypoint for the Windows
  workspace. It locates python/python3, forwards arguments, and preserves the
  child exit code so PowerShell callers see the same result as a direct call.

  Requires: Python 3 on PATH (python, python3, or py -3). Python is a stated
  prerequisite of this tool; the agent does not install it globally.

.PARAMETER Issue
  GitHub issue number to validate (default 5).

.PARAMETER Date
  Run date YYYY-MM-DD (defaults to today).

.PARAMETER AsJson
  Emit JSON only.

.EXAMPLE
  pwsh scripts/validate-run.ps1 -Issue 5
  pwsh scripts/validate-run.ps1 -Issue 5 -AsJson
#>

[CmdletBinding()]
param(
    [int]$Issue = 5,
    [string]$Date = "",
    [switch]$AsJson
)

$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$target = Join-Path $here "validate_run.py"

function Resolve-Python {
    foreach ($cand in @("python", "python3")) {
        $found = Get-Command $cand -ErrorAction SilentlyContinue
        if ($found) { return $cand }
    }
    $py = Get-Command py -ErrorAction SilentlyContinue
    if ($py) { return "py -3" }
    throw "Python 3 not found on PATH. Install Python 3 (this is a documented prerequisite of the validator)."
}

$py = Resolve-Python
$args = @($target, "--issue", $Issue)
if ($Date) { $args += @("--date", $Date) }
if ($AsJson) { $args += "--json" }

# Invoke via cmd to support the "py -3" multi-token resolver.
& cmd /c "$py $($args -join ' ')"
exit $LASTEXITCODE
