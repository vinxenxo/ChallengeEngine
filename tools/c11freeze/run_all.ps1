[CmdletBinding()]
param(
    [switch]$SkipPhysical,
    [int]$SeedLimit = 0,
    [int]$SeedRepeat = 2
)
$ErrorActionPreference = "Stop"

& .\tools\c11freeze\run_core_suite.ps1
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& .\tools\c11freeze\run_c11_suite.ps1
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python.exe .\tests\run_all.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& .\tools\c11freeze\run_retrocompatibility.ps1
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
if (-not $SkipPhysical) {
    & .\tools\c11freeze\run_physical_export_suite.ps1
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
$stress = @('.\tools\c11freeze\run_seed_stress.py','--repeat',$SeedRepeat)
if ($SeedLimit -gt 0) { $stress += @('--limit',$SeedLimit) }
python.exe @stress
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host '[C11FREEZE] FULL FREEZE GATE PASS' -ForegroundColor Green
