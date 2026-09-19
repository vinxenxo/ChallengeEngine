[CmdletBinding()]
param(
    [string]$Reference = "",
    [string]$Output = "artifacts/regression/runs/c11_freeze/RETROCOMPATIBILITY_REPORT.json"
)
$ErrorActionPreference = "Stop"
$args = @(".\tools\c11freeze\run_retrocompatibility.py", "--output", $Output)
if (-not [string]::IsNullOrWhiteSpace($Reference)) { $args += @("--reference", $Reference) }
python.exe @args
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
