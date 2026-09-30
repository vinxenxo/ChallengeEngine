[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$Root=(Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
Set-Location $Root

$required=[ordered]@{
  'c11c-suite\run.bat'=@('C11C_PROJECT_ROOT','main.py','cd /d')
  'c11c-suite\c11c-test\run.bat'=@('C11C_PROJECT_ROOT','main.py','cd /d')
  'c11c-suite\c11c-test\run_all.bat'=@('C11C_PROJECT_ROOT','tests\run_all.py')
  'c11c-suite\c11c-test\run_suite.bat'=@('C11C_PROJECT_ROOT','--headless','--path')
  'c11c-suite\c11c-test\run_c11c_complete_review.bat'=@('C11C_PROJECT_ROOT','run_c11c_complete_video_review.ps1','-Workers 7')
  'c11c-suite\c11c-test\run_c11c_acceptance.bat'=@('C11C_PROJECT_ROOT','FULL_ACCEPTANCE_C11C_2.19.12.ps1')
  'c11c-suite\c11c-test\run_c11c_one_video_each_type.bat'=@('C11C_PROJECT_ROOT','run_c11c_one_video_each_type.ps1')
  'c11c-suite\c11c-test\run_c11c_focused_validation.bat'=@('C11C_PROJECT_ROOT','run_c11c_focused_validation.ps1')
  'c11c-suite\c11c-producer\run.bat'=@('C11C_PROJECT_ROOT','main.py','cd /d')
  'c11c-suite\c11c-producer\test_gui_contract.bat'=@('C11C_PROJECT_ROOT','test_producer_gui_contract.py')
  'c11c-suite\c11c-maintenance\run.bat'=@('C11C_PROJECT_ROOT','main.py','cd /d')
  'c11c-suite\c11c-catalog\run.bat'=@('C11C_PROJECT_ROOT','main.py','cd /d')
  'c11c-suite\c11c-config\run.bat'=@('C11C_PROJECT_ROOT','main.py','cd /d')
  'c11c-suite\test_retro_reference_contract.bat'=@('C11C_PROJECT_ROOT','test_retro_reference_contract.py')
  'c11c-suite\c11c-maintenace\run.bat'=@('call','c11c-maintenance\run.bat')
}
foreach($rel in $required.Keys){
  $p=Join-Path $Root $rel
  if(-not(Test-Path -LiteralPath $p)){throw "Missing launcher: $rel"}
  $t=Get-Content -Raw -LiteralPath $p
  foreach($marker in $required[$rel]){if($t.IndexOf($marker,[StringComparison]::OrdinalIgnoreCase) -lt 0){throw "$rel missing marker: $marker"}}
}

$suiteFiles=@(Get-ChildItem -LiteralPath (Join-Path $Root 'c11c-suite') -Recurse -File | Where-Object {$_.Extension.ToLowerInvariant() -in @('.py','.ps1','.bat','.cmd')})
$studioRefs=@($suiteFiles | Where-Object {$_.Name -ne 'self_test.py' -and (Get-Content -Raw -LiteralPath $_.FullName -ErrorAction SilentlyContinue).Contains('c11c-studio')})
if($studioRefs.Count -gt 0){throw ('Operational c11c-studio dependency detected: ' + (($studioRefs | ForEach-Object {$_.FullName}) -join '; '))}

$alias=(Get-Content -Raw -LiteralPath (Join-Path $Root 'c11c-suite\c11c-maintenace\run.bat')).ToLowerInvariant()
if($alias.IndexOf('c11c-maintenance\run.bat',[StringComparison]::OrdinalIgnoreCase) -lt 0){throw 'Compatibility maintenance launcher does not delegate to canonical c11c-maintenance.'}
$producerSchemaPath=Join-Path $Root 'c11c-suite\c11c-producer\producer_schema.json'
$producerManifestPath=Join-Path $Root 'c11c-suite\c11c-producer\BUILD_MANIFEST.json'
$producerSchema=Get-Content -Raw -LiteralPath $producerSchemaPath | ConvertFrom-Json
$producerManifest=Get-Content -Raw -LiteralPath $producerManifestPath | ConvertFrom-Json
$currentChallengeLauncher='tools/qa/c11/run_c11c_challenge_bulk_qa.ps1'
if([string]$producerSchema.review_challenges_launcher -ne $currentChallengeLauncher){throw 'Producer schema REVIEW_CHALLENGES launcher is not the current C11-C Challenge review.'}
if([string]$producerManifest.review_challenges_launcher -ne $currentChallengeLauncher){throw 'Producer build manifest REVIEW_CHALLENGES launcher is not the current C11-C Challenge review.'}

Write-Host '[C11-C-SUITE-LAUNCHERS] PASS - all active launchers target c11c-suite; retired c11c-studio is not an operational dependency.'
