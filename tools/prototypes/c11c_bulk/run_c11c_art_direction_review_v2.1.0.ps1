param(
    [int[]]$Seeds = @(),
    [int]$VariationsPerFamily = 5,
    [switch]$ResetReviewAssets
)

$ErrorActionPreference = 'Stop'
$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$Bulk = Join-Path $PSScriptRoot 'run_c11c_multiseed_bulk.ps1'
$Reviews = Join-Path $PSScriptRoot 'export_all_review_assets.ps1'
$ReviewRoot = Join-Path $ProjectRoot 'artifacts\prototypes\c11c_review_assets'

if ($VariationsPerFamily -lt 1 -or $VariationsPerFamily -gt 50) { throw 'VariationsPerFamily must be between 1 and 50.' }
if ($Seeds.Count -eq 0) {
    $Seeds = @()
    while ($Seeds.Count -lt $VariationsPerFamily) {
        $candidate = Get-Random -Minimum 1000000 -Maximum 2147483646
        if ($Seeds -notcontains $candidate) { $Seeds += [int]$candidate }
    }
} elseif ($Seeds.Count -ne $VariationsPerFamily) {
    throw "When -Seeds is provided, pass exactly $VariationsPerFamily seeds."
}
foreach ($seed in $Seeds) { if ($seed -lt 1 -or $seed -gt 2147483646) { throw "Seed out of range: $seed" } }

Write-Host '[C11-C-ART-DIRECTION] =========================================='
Write-Host '[C11-C-ART-DIRECTION] NEW ART-DIRECTION REVIEW CORPUS'
Write-Host '[C11-C-ART-DIRECTION] NO prototype artifact cleanup is performed.'
Write-Host "[C11-C-ART-DIRECTION] Variations per family: $VariationsPerFamily"
Write-Host '[C11-C-ART-DIRECTION] Families: 5'
Write-Host ("[C11-C-ART-DIRECTION] Total renders: " + ($VariationsPerFamily * 5))
Write-Host ("[C11-C-ART-DIRECTION] Seeds: " + ($Seeds -join ', '))

if ($ResetReviewAssets) {
    if (Test-Path -LiteralPath $ReviewRoot) { Remove-Item -LiteralPath $ReviewRoot -Recurse -Force }
    New-Item -ItemType Directory -Force -Path $ReviewRoot | Out-Null
    Write-Host '[C11-C-ART-DIRECTION] Review assets reset ONLY; prototype artifacts untouched.'
} else { New-Item -ItemType Directory -Force -Path $ReviewRoot | Out-Null }

try { & $Bulk -Seeds $Seeds } catch { throw "Multiseed bulk failed: $($_.Exception.Message)" }
if (-not $?) { throw 'Multiseed bulk failed.' }
if (-not (Test-Path -LiteralPath $Reviews)) { throw "Review exporter not found: $Reviews" }
try { & $Reviews -InputRoot (Join-Path $ProjectRoot 'artifacts\prototypes') -OutputRoot $ReviewRoot } catch { throw "Review export failed: $($_.Exception.Message)" }
if (-not $?) { throw 'Review export failed.' }

$seedManifest = [ordered]@{
    schema='C11-C-ART-DIRECTION-REVIEW-SEEDS-V1'; revision='2.1.0'; mode='random_or_explicit_seed_batch'
    family_count=5; variations_per_family=$VariationsPerFamily; render_count=$VariationsPerFamily*5; seeds=@($Seeds)
    review_root=$ReviewRoot; prototype_cleanup_performed=$false; review_assets_reset=[bool]$ResetReviewAssets
}
$seedManifestPath=Join-Path $ReviewRoot 'C11-C_ART_DIRECTION_REVIEW_SEEDS.json'
$seedManifest | ConvertTo-Json -Depth 8 | Set-Content -Path $seedManifestPath -Encoding UTF8
Write-Host '[C11-C-ART-DIRECTION] COMPLETE - 5 variations per family generated.'
Write-Host "[C11-C-ART-DIRECTION] Seed manifest: $seedManifestPath"
return
