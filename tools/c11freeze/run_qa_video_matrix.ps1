[CmdletBinding()]
param(
    [string]$ConfigDir = "artifacts/qa/video_matrix/configs",
    [string]$OutputDir = "artifacts/qa/video_matrix/videos"
)

$ErrorActionPreference = "Stop"
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

if (-not (Test-Path $ConfigDir)) { throw "Missing QA config directory: $ConfigDir" }
python.exe .\build_factory.py --batch $ConfigDir --output $OutputDir
$code = $LASTEXITCODE
if ($code -ne 0) { exit $code }
Write-Host "[C11FREEZE] QA video matrix PASS"
