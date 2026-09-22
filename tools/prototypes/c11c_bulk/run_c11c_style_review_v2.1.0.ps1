param(
    [Parameter(Mandatory=$true)]
    [int[]]$Seeds,
    [switch]$KeepExistingReviewAssets,
    [switch]$ResetReviewAssets
)
$ErrorActionPreference = 'Stop'
$ProjectRoot=(Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$ReviewRoot=Join-Path $ProjectRoot 'artifacts\prototypes\c11c_review_assets'
$bulk=Join-Path $PSScriptRoot 'run_c11c_multiseed_bulk.ps1'
$reviews=Join-Path $PSScriptRoot 'export_all_review_assets.ps1'
if ($KeepExistingReviewAssets -and $ResetReviewAssets) { throw 'Use either -KeepExistingReviewAssets or -ResetReviewAssets, not both.' }
foreach ($seed in $Seeds) { if ($seed -lt 1 -or $seed -gt 2147483646) { throw "Seed out of range: $seed" } }
if ($ResetReviewAssets) {
    if (Test-Path -LiteralPath $ReviewRoot) { Remove-Item -LiteralPath $ReviewRoot -Recurse -Force }
}
New-Item -ItemType Directory -Force -Path $ReviewRoot | Out-Null
Write-Host '[C11-C-STYLE-REVIEW] Prototype artifacts are never cleaned by this command.'
try { & $bulk -Seeds $Seeds } catch { throw "Multiseed bulk failed: $($_.Exception.Message)" }
if (-not $?) { throw 'Multiseed bulk failed.' }
if (-not (Test-Path -LiteralPath $reviews)) { throw "Review exporter not found: $reviews" }
try { & $reviews -InputRoot (Join-Path $ProjectRoot 'artifacts\prototypes') -OutputRoot $ReviewRoot } catch { throw "Review export failed: $($_.Exception.Message)" }
if (-not $?) { throw 'Review export failed.' }
Write-Host '[C11-C-STYLE-REVIEW] COMPLETE'
return
