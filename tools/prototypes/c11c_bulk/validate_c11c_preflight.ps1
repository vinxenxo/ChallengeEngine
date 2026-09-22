$ErrorActionPreference='Stop'
$ProjectRoot=(Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$parse=Join-Path $PSScriptRoot 'validate_c11c_powershell.ps1'
$delivery=Join-Path $PSScriptRoot 'validate_c11c_delivery_configuration.ps1'
Write-Host '[C11C-PREFLIGHT] STEP 1/3 - PowerShell parser'
& $parse
if(-not $?){throw 'PowerShell parser validation failed.'}
Write-Host '[C11C-PREFLIGHT] STEP 2/3 - Delivery configuration'
& $delivery
if(-not $?){throw 'C11-C delivery validation failed.'}
Write-Host '[C11C-PREFLIGHT] STEP 3/3 - Canonical launcher set'
$required=@(
  (Join-Path $PSScriptRoot 'run_c11c_art_direction_review.ps1'),
  (Join-Path $PSScriptRoot 'run_c11c_multiseed_bulk.ps1'),
  (Join-Path $PSScriptRoot 'run_c11c_production.ps1'),
  (Join-Path $ProjectRoot 'tools\prototypes\c11c_common\C11CMovieCapture.ps1')
)
foreach($path in $required){if(-not(Test-Path -LiteralPath $path)){throw "Required canonical tool missing: $path"}}
$obsolete=@('run_c11c_art_direction_review_v2.0.8.ps1','run_c11c_art_direction_review_v2.0.9.ps1','run_c11c_art_direction_review_v2.1.0.ps1','run_c11c_art_direction_review_v2.1.1.ps1','run_c11c_production_v2.1.0.ps1','run_c11c_production_v2.1.1.ps1','run_c11c_style_review_v2.0.4.ps1','run_c11c_style_review_v2.0.5.ps1','run_c11c_style_review_v2.0.6.ps1','run_c11c_style_review_v2.0.8.ps1','run_c11c_style_review_v2.0.9.ps1','run_c11c_style_review_v2.1.0.ps1','run_c11c_style_review_v2.1.1.ps1')
$found=@($obsolete | Where-Object {Test-Path -LiteralPath (Join-Path $PSScriptRoot $_)})
if($found.Count -gt 0){throw "Superseded launchers still present: $($found -join ', ')"}
Write-Host '[C11C-PREFLIGHT] PASS - canonical toolchain ready for the 25-video Art Direction 2.0 corpus.'
return
