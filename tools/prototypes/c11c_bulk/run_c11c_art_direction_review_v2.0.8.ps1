param(
    [int[]]$Seeds = @(),
    [int]$VariationsPerFamily = 5,
    [switch]$KeepExistingReviewAssets
)

$ErrorActionPreference = 'Stop'
$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$StyleReview = Join-Path $PSScriptRoot 'run_c11c_style_review_v2.0.8.ps1'
$ReviewRoot = Join-Path $ProjectRoot 'artifacts\prototypes\c11c_review_assets'

if ($VariationsPerFamily -lt 1 -or $VariationsPerFamily -gt 50) {
    throw 'VariationsPerFamily must be between 1 and 50.'
}

if ($Seeds.Count -eq 0) {
    $Seeds = @()
    while ($Seeds.Count -lt $VariationsPerFamily) {
        $candidate = Get-Random -Minimum 1000000 -Maximum 2147483646
        if ($Seeds -notcontains $candidate) { $Seeds += [int]$candidate }
    }
} elseif ($Seeds.Count -ne $VariationsPerFamily) {
    throw "When -Seeds is provided, pass exactly $VariationsPerFamily seeds."
}

foreach ($seed in $Seeds) {
    if ($seed -lt 1 -or $seed -gt 2147483646) { throw "Seed out of range: $seed" }
}

Write-Host '[C11-C-ART-DIRECTION] =========================================='
Write-Host '[C11-C-ART-DIRECTION] NEW ART-DIRECTION REVIEW CORPUS'
Write-Host '[C11-C-ART-DIRECTION] No artifact cleanup is performed.'
Write-Host "[C11-C-ART-DIRECTION] Variations per family: $VariationsPerFamily"
Write-Host '[C11-C-ART-DIRECTION] Families: 5'
Write-Host ("[C11-C-ART-DIRECTION] Total renders: " + ($VariationsPerFamily * 5))
Write-Host ("[C11-C-ART-DIRECTION] Seeds: " + ($Seeds -join ', '))
Write-Host ''

# The style-review launcher owns only its review-assets output; it never cleans prototype artifacts.
& powershell -NoProfile -ExecutionPolicy Bypass -File $StyleReview -Seeds $Seeds -KeepExistingReviewAssets:$KeepExistingReviewAssets
$exit = [int]$LASTEXITCODE
if ($exit -ne 0) { throw "Style review failed: exit=$exit" }

# Write the seed manifest AFTER review-assets regeneration so it cannot be deleted by the review reset.
New-Item -ItemType Directory -Force -Path $ReviewRoot | Out-Null
$seedManifest = [ordered]@{
    schema = 'C11-C-ART-DIRECTION-REVIEW-SEEDS-V1'
    revision = '2.0.8'
    mode = 'random_seed_batch'
    family_count = 5
    variations_per_family = $VariationsPerFamily
    render_count = $VariationsPerFamily * 5
    seeds = @($Seeds)
    review_root = $ReviewRoot
    cleanup_performed = $false
}
$seedManifestPath = Join-Path $ReviewRoot 'C11-C_ART_DIRECTION_REVIEW_SEEDS.json'
$seedManifest | ConvertTo-Json -Depth 8 | Set-Content -Path $seedManifestPath -Encoding UTF8

Write-Host '[C11-C-ART-DIRECTION] COMPLETE - 5 variations per family generated.'
Write-Host "[C11-C-ART-DIRECTION] Seed manifest: $seedManifestPath"
