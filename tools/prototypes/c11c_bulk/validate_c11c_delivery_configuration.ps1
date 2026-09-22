$ErrorActionPreference='Stop'
$ProjectRoot=(Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$families=@('c11c_geometric_waves_v1','c11c_fractal_bloom_v1','c11c_sacred_symmetry_v1','c11c_living_particles_v1','c11c_invisible_forces_v1')
foreach($family in $families){
    $p=Join-Path $ProjectRoot ("tools\prototypes\$family\run_prototype.ps1")
    if(-not(Test-Path -LiteralPath $p)){throw "Missing launcher: $p"}
    $s=Get-Content -Raw $p
    foreach($needle in @("'--resolution','720','1280'","'--fixed-fps','30'","'--quit-after','540'",'C11CMovieCapture.ps1','-Width 720 -Height 1280')){if($s -notlike "*$needle*"){throw "${family}: required launcher token missing: $needle"}}
    if($s -match 'project\.godot'){throw "${family}: launcher must not edit project.godot."}
}
$helper=Get-Content -Raw (Join-Path $ProjectRoot 'tools\prototypes\c11c_common\C11CMovieCapture.ps1')
foreach($needle in @('window/size/viewport_width=$Width','window/size/viewport_height=$Height','window/size/window_width_override=$Width','window/size/window_height_override=$Height')){if($helper -notlike "*$needle*"){throw "Movie capture helper missing viewport override: $needle"}}
$orchestrators=@('run_c11c_multiseed_bulk.ps1','export_all_review_assets.ps1','run_all_c11c_visual_loops.ps1','run_c11c_production.ps1','run_c11c_production_bulk.ps1','run_c11c_art_direction_review.ps1')
foreach($name in $orchestrators){$s=Get-Content -Raw (Join-Path $PSScriptRoot $name);if($s -match '&\s+powershell\.exe'){throw "$name must not spawn nested powershell.exe."}}
$prod=Get-Content -Raw (Join-Path $PSScriptRoot 'run_c11c_production.ps1')
if($prod -notmatch 'artifacts\\production\\audiovisual'){throw 'Production launcher does not target protected production root.'}
Write-Host '[C11C-DELIVERY-VALIDATION] PASS - 720x1280 capture args, direct PowerShell invocation, bulk/review separation, production policy.'
return
