[CmdletBinding()]
param([switch]$SkipHeavyPhysical,[switch]$SkipReviews)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$ProjectRoot=(Resolve-Path $PSScriptRoot).Path
Set-Location $ProjectRoot
$stamp=Get-Date -Format 'yyyyMMdd_HHmmss'
$A1Root="artifacts\qa\c11a1_challenge\full_acceptance_$stamp"
$AcceptanceEvidence=[ordered]@{focused_parallel_contract=$false;art_direction_concurrency=$false;worker_class_cache_bootstrap=$false}
function Invoke-Step([string]$Label,[scriptblock]$Action){ Write-Host "`n=============================================="; Write-Host $Label; Write-Host "=============================================="; & $Action; if($LASTEXITCODE -ne 0){throw "$Label failed with exit code $LASTEXITCODE"} }
Invoke-Step 'C11-C final-repair static verifier' { powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\maintenance\verify_c11c_2_19_6_final_repair.ps1 }
Invoke-Step 'C11-C Suite 0.1.4 self-test' { python .\c11c-suite\self_test.py }
Invoke-Step 'Producer 0.9.7 self-test' { python .\c11c-suite\c11c-producer\self_test.py }
Invoke-Step 'Producer GUI contract' { python .\c11c-suite\c11c-producer\test_producer_gui_contract.py }
Invoke-Step 'C11-C parallel worker contract' { & .\c11c-suite\c11c-test\run_suite.bat C11CParallelReviewWorkerIsolationContractTest.gd; $AcceptanceEvidence.focused_parallel_contract=$true }
Invoke-Step 'Retro reference contract' { python .\c11c-suite\test_retro_reference_contract.py }
Invoke-Step 'Full logical corpus' { python .\tests\run_all.py }
Invoke-Step 'C11-A.1 — 54 fresh runs' { powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\qa\c11\run_c11a1_challenge_bulk_qa.ps1 -OutputRoot $A1Root }
Invoke-Step 'Retrocompatibility — 54 telemetry/A-B checks' { powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\c11freeze\run_retrocompatibility.ps1 }
if(-not $SkipHeavyPhysical){ Invoke-Step 'C10-C physical smoke' { powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\qa\c10\run_C10C_physical_export.ps1 }; Invoke-Step 'Physical export suite' { powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\c11freeze\run_physical_export_suite.ps1 } }
if(-not $SkipReviews){ Invoke-Step 'C11-C Art Direction corpus — Workers=7 concurrent' { powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\prototypes\c11c_bulk\run_c11c_art_direction_batch_v4.ps1 -Workers 7 -All -Reset; $manifestPath='.\artifacts\prototypes\c11c_art_direction_review\C11-C_ART_DIRECTION_REVIEW_CORPUS_MANIFEST.json'; if(-not(Test-Path -LiteralPath $manifestPath)){throw "Missing manifest: $manifestPath"}; $m=Get-Content -Raw -LiteralPath $manifestPath|ConvertFrom-Json; if([int]$m.workers -ne 7){throw 'Workers != 7'}; if([int]$m.max_observed_worker_concurrency -le 1){throw 'Genuine concurrency not proven'}; if([string]$m.worker_isolation -ne 'per_worker_temporary_godot_project'){throw 'Wrong worker isolation'}; if([string]$m.worker_bootstrap -ne 'per_worker_godot_headless_editor_class_scan'){throw 'Missing class-cache bootstrap declaration'}; if([string]$m.worker_global_script_class_cache -ne 'required'){throw 'Class-cache requirement missing'}; $AcceptanceEvidence.art_direction_concurrency=$true; $AcceptanceEvidence.worker_class_cache_bootstrap=$true }; Invoke-Step 'C11-C Visual Drill review smoke' { powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\prototypes\c11c_bulk\run_c11c_visual_drill_review.ps1 -Seeds 314159 -Families tracking,saccade,pursuit,peripheral_scan -Smoke -ResetReviewAssets } }
New-Item -ItemType Directory -Force -Path .\artifacts\tests\reports|Out-Null
$report=[ordered]@{revision='2.19.6';status=if($AcceptanceEvidence.focused_parallel_contract -and $AcceptanceEvidence.art_direction_concurrency -and $AcceptanceEvidence.worker_class_cache_bootstrap -and -not $SkipHeavyPhysical -and -not $SkipReviews){'PASS'}else{'PARTIAL'};generated_at=(Get-Date).ToUniversalTime().ToString('o');focused_parallel_contract=$AcceptanceEvidence.focused_parallel_contract;art_direction_concurrency=$AcceptanceEvidence.art_direction_concurrency;worker_class_cache_bootstrap=$AcceptanceEvidence.worker_class_cache_bootstrap;skip_heavy_physical=[bool]$SkipHeavyPhysical;skip_reviews=[bool]$SkipReviews}
$report|ConvertTo-Json -Depth 6|Set-Content -LiteralPath .\artifacts\tests\reports\C11C_2.19.6_ACCEPTANCE_REPORT.json -Encoding UTF8
if($report.status -ne 'PASS'){throw 'C11-C 2.19.6 acceptance is PARTIAL; final freeze evidence was not produced.'}
Write-Host 'C11-C 2.19.6 — FINAL REPAIR CONSOLIDATED ACCEPTANCE PASS'
