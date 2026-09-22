param(
    [Parameter(Mandatory=$false)]
    [int[]]$Seeds = @(),
    [Parameter(Mandatory=$false)]
    [ValidateRange(1,50)]
    [int]$VariationsPerFamily = 5,
    [switch]$ResetReviewAssets
)
$ErrorActionPreference='Stop'
$ProjectRoot=(Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$Bulk=Join-Path $PSScriptRoot 'run_c11c_multiseed_bulk.ps1'
$Reviews=Join-Path $PSScriptRoot 'export_all_review_assets.ps1'
$ReviewRoot=Join-Path $ProjectRoot 'artifacts\prototypes\c11c_review_assets'
if($Seeds.Count -eq 0){
    $Seeds=@()
    while($Seeds.Count -lt $VariationsPerFamily){$candidate=Get-Random -Minimum 1000000 -Maximum 2147483646;if($Seeds -notcontains $candidate){$Seeds += [int]$candidate}}
} elseif($Seeds.Count -ne $VariationsPerFamily){throw "When -Seeds is supplied, pass exactly $VariationsPerFamily seeds."}
foreach($seed in $Seeds){if($seed -lt 1 -or $seed -gt 2147483646){throw "Seed out of range: $seed"}}
Write-Host '[C11-C-ART-DIRECTION] =========================================='
Write-Host '[C11-C-ART-DIRECTION] NEW ART-DIRECTION REVIEW CORPUS'
Write-Host '[C11-C-ART-DIRECTION] NO prototype cleanup is performed.'
Write-Host "[C11-C-ART-DIRECTION] Variations per family: $VariationsPerFamily"
Write-Host '[C11-C-ART-DIRECTION] Families: 5'
Write-Host "[C11-C-ART-DIRECTION] Total renders: $($VariationsPerFamily * 5)"
Write-Host "[C11-C-ART-DIRECTION] Seeds: $($Seeds -join ', ')"
if($ResetReviewAssets -and (Test-Path -LiteralPath $ReviewRoot)){Remove-Item -LiteralPath $ReviewRoot -Recurse -Force}
New-Item -ItemType Directory -Force -Path $ReviewRoot | Out-Null
$bulkParams=@{Seeds=@($Seeds)}
& $Bulk @bulkParams
if(-not $?){throw 'Multiseed bulk failed.'}
$reviewParams=@{InputRoot=(Join-Path $ProjectRoot 'artifacts\prototypes');OutputRoot=$ReviewRoot;Seeds=@($Seeds)}
& $Reviews @reviewParams
if(-not $?){throw 'Review asset export failed.'}
$expected=$VariationsPerFamily*5
$stage=Join-Path $ProjectRoot 'artifacts\prototypes'
$batch=@(Get-ChildItem -Path $stage -Recurse -Filter '*.mp4' -File | Where-Object { $_.Name -match '_seed_[0-9]+\.mp4$' -and $_.FullName -notlike '*c11c_review_assets*' })
$seedStrings=@($Seeds|ForEach-Object {$_.ToString()})
$batch=@($batch|Where-Object {$seedStrings -contains ([regex]::Match($_.Name,'_seed_([0-9]+)\.mp4$').Groups[1].Value)})
if($batch.Count -ne $expected){throw "Review corpus count failed: expected $expected canonical MP4s, found $($batch.Count)."}
$seedManifest=[ordered]@{schema='C11-C-ART-DIRECTION-REVIEW-SEEDS-V3';revision='2.1.4';mode='random_or_explicit_seed_batch';family_count=5;variations_per_family=$VariationsPerFamily;render_count=$expected;seeds=@($Seeds);review_root=$ReviewRoot;prototype_cleanup_performed=$false;review_assets_reset=[bool]$ResetReviewAssets;delivery_contract='720x1280 / 30 FPS / 18.0 s / 540 frames'}
[System.IO.File]::WriteAllText((Join-Path $ReviewRoot 'C11-C_ART_DIRECTION_REVIEW_SEEDS.json'),($seedManifest|ConvertTo-Json -Depth 8),(New-Object System.Text.UTF8Encoding($false)))
Write-Host "[C11-C-ART-DIRECTION] COMPLETE - $expected renders generated."
return
