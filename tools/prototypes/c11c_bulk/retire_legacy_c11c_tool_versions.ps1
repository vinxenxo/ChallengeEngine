param([switch]$Apply)
$ErrorActionPreference='Stop'
$targets=@(
'run_c11c_art_direction_review_v2.0.8.ps1','run_c11c_art_direction_review_v2.0.9.ps1','run_c11c_art_direction_review_v2.1.0.ps1','run_c11c_art_direction_review_v2.1.1.ps1',
'run_c11c_production_v2.1.0.ps1','run_c11c_production_v2.1.1.ps1',
'run_c11c_style_review_v2.0.4.ps1','run_c11c_style_review_v2.0.5.ps1','run_c11c_style_review_v2.0.6.ps1','run_c11c_style_review_v2.0.8.ps1','run_c11c_style_review_v2.0.9.ps1','run_c11c_style_review_v2.1.0.ps1'
)
foreach($name in $targets){$p=Join-Path $PSScriptRoot $name;if(Test-Path -LiteralPath $p){if($Apply){Remove-Item -LiteralPath $p -Force;Write-Host "[C11C-TOOLS] REMOVED $name"}else{Write-Host "[C11C-TOOLS] WOULD REMOVE $name"}}}
Write-Host "[C11C-TOOLS] $(if($Apply){'RETIRE COMPLETE'}else{'DRY-RUN COMPLETE. Use -Apply to retire superseded versioned launchers.'})"
return
