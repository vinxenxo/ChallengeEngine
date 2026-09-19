$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
Set-Location $root

$ids = @(
  "challenge_001_seed_12345_A",
  "challenge_001_seed_12345_B",
  "challenge_001_seed_54321"
)

foreach ($id in $ids) {
    $file = ".\artifacts\qa\c11b_visibility\runs\$id\stdout.txt"

    Write-Host ""
    Write-Host "========== $id ==========" -ForegroundColor Cyan

    $line = Get-Content -LiteralPath $file |
        Where-Object { $_ -match '^\[C11B_VISIBILITY_JSON\]' } |
        Select-Object -Last 1

    if ($null -eq $line) {
        Write-Host "NO HAY C11B_VISIBILITY_JSON" -ForegroundColor Red
        continue
    }

    $json = $line -replace '^\[C11B_VISIBILITY_JSON\]', ''
    $p = $json | ConvertFrom-Json

    Write-Host "logical :" ($p.object_logical_position | ConvertTo-Json -Compress)
    Write-Host "expected:" ($p.object_expected_position | ConvertTo-Json -Compress)
    Write-Host "actual  :" ($p.object_actual_position | ConvertTo-Json -Compress)
    Write-Host "entities:" ($p.entities | ConvertTo-Json -Compress)
}