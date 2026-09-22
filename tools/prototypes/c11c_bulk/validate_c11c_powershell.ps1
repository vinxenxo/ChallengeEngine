$ErrorActionPreference='Stop'
$ProjectRoot=(Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$files=@(
    (Join-Path $PSScriptRoot 'clean_c11c_artifacts.ps1'),
    (Join-Path $PSScriptRoot 'reset_c11c_artifacts.ps1'),
    (Join-Path $PSScriptRoot 'export_review_gifs.ps1'),
    (Join-Path $PSScriptRoot 'export_review_keyframes.ps1'),
    (Join-Path $PSScriptRoot 'export_all_review_assets.ps1'),
    (Join-Path $PSScriptRoot 'run_c11c_multiseed_bulk.ps1'),
    (Join-Path $PSScriptRoot 'run_c11c_art_direction_review.ps1'),
    (Join-Path $PSScriptRoot 'run_c11c_production.ps1'),
    (Join-Path $PSScriptRoot 'run_c11c_production_bulk.ps1'),
    (Join-Path $PSScriptRoot 'run_all_c11c_visual_loops.ps1'),
    (Join-Path $PSScriptRoot 'validate_c11c_delivery_configuration.ps1'),
    (Join-Path $PSScriptRoot 'run_c11c_art_direction_review_v2.1.2.ps1'),
    (Join-Path $ProjectRoot 'tools\prototypes\c11c_common\C11CMovieCapture.ps1')
)
foreach($family in @('c11c_geometric_waves_v1','c11c_fractal_bloom_v1','c11c_sacred_symmetry_v1','c11c_living_particles_v1','c11c_invisible_forces_v1')){
    $files += Join-Path $ProjectRoot ("tools\prototypes\$family\run_prototype.ps1")
}
$errors=0
foreach($file in $files){
    if(-not(Test-Path -LiteralPath $file)){ Write-Host "[C11C-PS-PARSE] FAIL MISSING $file"; $errors++; continue }
    $tokens=$null; $parseErrors=$null
    [void][System.Management.Automation.Language.Parser]::ParseFile($file,[ref]$tokens,[ref]$parseErrors)
    if($parseErrors.Count -eq 0){ Write-Host "[C11C-PS-PARSE] PASS $file" }
    else { Write-Host "[C11C-PS-PARSE] FAIL $file"; $parseErrors | ForEach-Object { Write-Host "  $($_.Message) line=$($_.Extent.StartLineNumber) col=$($_.Extent.StartColumnNumber)" }; $errors++ }
}
if($errors -gt 0){ throw "Canonical C11-C PowerShell parse validation failed: $errors file(s)." }
Write-Host "[C11C-PS-PARSE] COMPLETE - $($files.Count) canonical PowerShell files parsed successfully."
return
