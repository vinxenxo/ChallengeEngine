[CmdletBinding()]
param()
$ErrorActionPreference = "Stop"
$root = Join-Path (Get-Location) "artifacts/tests/logs"
New-Item -ItemType Directory -Force -Path $root | Out-Null
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$log = Join-Path $root "run_all_$stamp.log"
python.exe .\tests\run_all.py 2>&1 | Tee-Object -FilePath $log
$code = $LASTEXITCODE
Write-Host "[C11FREEZE] run_all exit code: $code"
if ($code -ne 0) { exit $code }
