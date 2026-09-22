param(
    [Parameter(Mandatory=$true)]
    [int[]]$Seeds,
    [switch]$KeepExistingReviewAssets
)

$ErrorActionPreference = 'Stop'
$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$ReviewRoot = Join-Path $ProjectRoot 'artifacts\prototypes\c11c_review_assets'
$bulk = Join-Path $PSScriptRoot 'run_c11c_multiseed_bulk.ps1'
$reviews = Join-Path $PSScriptRoot 'export_all_review_assets.ps1'

if ($Seeds.Count -lt 1) { throw 'At least one seed is required.' }
foreach ($seed in $Seeds) {
    if ($seed -lt 1 -or $seed -gt 2147483646) { throw "Seed out of range: $seed" }
}

Write-Host '[C11-C-STYLE-REVIEW] STEP 1/3 - NO ARTIFACT CLEANUP'
Write-Host '[C11-C-STYLE-REVIEW] Existing prototype artifacts are preserved.'
Write-Host '[C11-C-STYLE-REVIEW] Use clean_c11c_artifacts.ps1 or reset_c11c_artifacts.ps1 explicitly when needed.'

Write-Host '[C11-C-STYLE-REVIEW] STEP 2/3 - review assets'
if (-not $KeepExistingReviewAssets) {
    if (Test-Path -LiteralPath $ReviewRoot) { Remove-Item -LiteralPath $ReviewRoot -Recurse -Force }
    New-Item -ItemType Directory -Force -Path $ReviewRoot | Out-Null
} else {
    New-Item -ItemType Directory -Force -Path $ReviewRoot | Out-Null
}

Write-Host '[C11-C-STYLE-REVIEW] STEP 3/3 - multiseed render + review export'
& powershell -NoProfile -ExecutionPolicy Bypass -File $bulk -Seeds $Seeds
$bulkExit = [int]$LASTEXITCODE
if ($bulkExit -ne 0) { throw "Multiseed bulk failed: exit=$bulkExit" }

if (-not (Test-Path -LiteralPath $reviews)) { throw "Review exporter not found: $reviews" }
& powershell -NoProfile -ExecutionPolicy Bypass -File $reviews -InputRoot (Join-Path $ProjectRoot 'artifacts\prototypes') -OutputRoot $ReviewRoot
$reviewExit = [int]$LASTEXITCODE
if ($reviewExit -ne 0) { throw "Review export failed: exit=$reviewExit" }

Write-Host '[C11-C-STYLE-REVIEW] COMPLETE - review corpus rebuilt'
Write-Host ("[C11-C-STYLE-REVIEW] Seeds: " + ($Seeds -join ', '))
Write-Host ("[C11-C-STYLE-REVIEW] Renders: " + ($Seeds.Count * 5))
Write-Host ("[C11-C-STYLE-REVIEW] Review root: " + $ReviewRoot)
