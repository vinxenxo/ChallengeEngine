[CmdletBinding()]
param([switch]$SkipHeavyPhysical,[switch]$SkipReviews)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$ProjectRoot=(Resolve-Path $PSScriptRoot).Path
Set-Location $ProjectRoot
$stamp=Get-Date -Format 'yyyyMMdd_HHmmss'
$A1Root="artifacts\qa\c11a1_challenge\full_acceptance_$stamp"
$Acceptance=[ordered]@{docs_consolidated=$false;suite_self_test=$false;producer_self_test=$false;producer_gui=$false;launcher_audit=$false;parallel_contract=$false;envelope_path_contract=$false;retro_reference=$false;logical=$false;c11a1=$false;retro=$false;physical_smoke=$false;physical_export=$false;video_review=$false}
function Invoke-Step([string]$Label,[scriptblock]$Action){
  Write-Host "`n=============================================="; Write-Host $Label; Write-Host "=============================================="; & $Action; if($LASTEXITCODE -ne 0){throw "$Label failed with exit code $LASTEXITCODE"}
}
Invoke-Step 'C11-C 2.19 documentation consolidation' { powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\maintenance\consolidate_c11c_2_19_documentation.ps1 }; $Acceptance.docs_consolidated=$true
Invoke-Step 'C11-C Suite 0.1.4 self-test' { python .\c11c-suite\self_test.py }; $Acceptance.suite_self_test=$true
Invoke-Step 'Producer 0.9.7 self-test' { python .\c11c-suite\c11c-producer\self_test.py }; $Acceptance.producer_self_test=$true
Invoke-Step 'Producer GUI contract' { python .\c11c-suite\c11c-producer\test_producer_gui_contract.py }; $Acceptance.producer_gui=$true
Invoke-Step 'C11-C Suite launcher audit' { powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\qa\c11\verify_c11c_suite_launchers.ps1 }; $Acceptance.launcher_audit=$true
Invoke-Step 'C11-C parallel worker contract' { & .\c11c-suite\c11c-test\run_suite.bat C11CParallelReviewWorkerIsolationContractTest.gd }; $Acceptance.parallel_contract=$true
Invoke-Step 'C11-C Visual Drill envelope path contract' { & .\c11c-suite\c11c-test\run_suite.bat C11CVisualDrillReviewEnvelopePathContractTest.gd }; $Acceptance.envelope_path_contract=$true
Invoke-Step 'Retro reference contract' { python .\c11c-suite\test_retro_reference_contract.py }; $Acceptance.retro_reference=$true
Invoke-Step 'Full logical corpus' { python .\tests\run_all.py }; $Acceptance.logical=$true
Invoke-Step 'C11-A.1 - 54 fresh runs' { powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\qa\c11\run_c11a1_challenge_bulk_qa.ps1 -OutputRoot $A1Root }; $Acceptance.c11a1=$true
Invoke-Step 'Retrocompatibility - 54 telemetry/A-B checks' { powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\c11freeze\run_retrocompatibility.ps1 }; $Acceptance.retro=$true
if(-not $SkipHeavyPhysical){
  Invoke-Step 'C10-C physical smoke' { powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\qa\c10\run_C10C_physical_export.ps1 }; $Acceptance.physical_smoke=$true
  Invoke-Step 'Physical export suite' { powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\c11freeze\run_physical_export_suite.ps1 }; $Acceptance.physical_export=$true
}
if(-not $SkipReviews){
  Invoke-Step 'C11-C complete video review - all 52 products' { powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\qa\c11\run_c11c_complete_video_review.ps1 -Workers 7 -Reset }; $Acceptance.video_review=$true
}
New-Item -ItemType Directory -Force -Path .\artifacts\tests\reports | Out-Null
$complete=(-not $SkipHeavyPhysical) -and (-not $SkipReviews) -and $Acceptance.docs_consolidated -and $Acceptance.suite_self_test -and $Acceptance.producer_self_test -and $Acceptance.producer_gui -and $Acceptance.launcher_audit -and $Acceptance.parallel_contract -and $Acceptance.envelope_path_contract -and $Acceptance.retro_reference -and $Acceptance.logical -and $Acceptance.c11a1 -and $Acceptance.retro -and $Acceptance.physical_smoke -and $Acceptance.physical_export -and $Acceptance.video_review
$status=if($complete){'PASS'}else{'PARTIAL'}
$report=[ordered]@{revision='2.19.9';status=$status;generated_at=(Get-Date).ToUniversalTime().ToString('o');skip_heavy_physical=[bool]$SkipHeavyPhysical;skip_reviews=[bool]$SkipReviews;checks=$Acceptance}
$report|ConvertTo-Json -Depth 8|Set-Content -LiteralPath .\artifacts\tests\reports\C11C_2.19.9_ACCEPTANCE_REPORT.json -Encoding UTF8
if($status -ne 'PASS'){throw 'C11-C 2.19.9 acceptance is PARTIAL; final freeze evidence was not produced.'}
Write-Host 'C11-C 2.19.9 - FINAL CONSOLIDATED ACCEPTANCE PASS'
