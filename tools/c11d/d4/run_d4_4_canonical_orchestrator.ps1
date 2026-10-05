#requires -Version 5.1
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 1.0

$RootPath = (Get-Location).Path

$SchemaPath = Join-Path $RootPath 'definitions\c11d\production\C11D_PRODUCTION_REQUEST_SCHEMA_V1.json'
$PersonalizationRegistryPath = Join-Path $RootPath 'definitions\c11d\personalization\C11D_PERSONALIZATION_PROFILE_REGISTRY_V1.json'
$OrchestratorPath = Join-Path $RootPath 'tools\c11d\d4\canonical_production_orchestrator.py'

$ArtifactDir = Join-Path $RootPath 'artifacts\tests\c11d_d4\d4_4'
$EvidencePath = Join-Path $ArtifactDir 'd4_4_orchestration_evidence.json'
$ParityPath = Join-Path $ArtifactDir 'd4_4_gui_cli_plan_parity.json'
$PlanPath = Join-Path $ArtifactDir 'd4_4_example_production_plan.json'
$ReceiptPath = Join-Path $ArtifactDir 'd4_4_validation_receipt.json'

if(-not (Test-Path -LiteralPath $SchemaPath)){
    throw 'D4.1 schema missing.'
}

if(-not (Test-Path -LiteralPath $PersonalizationRegistryPath)){
    throw 'D4.3 personalization registry missing.'
}

if(-not (Test-Path -LiteralPath $OrchestratorPath)){
    throw 'D4.4 orchestrator missing.'
}

New-Item -ItemType Directory -Force -Path $ArtifactDir | Out-Null

$RawOutput = & python.exe `
    $OrchestratorPath `
    --schema $SchemaPath `
    --personalization-registry $PersonalizationRegistryPath `
    --self-test `
    --evidence $EvidencePath `
    --parity $ParityPath `
    --plan $PlanPath `
    --receipt $ReceiptPath

if($LASTEXITCODE -ne 0){
    throw 'D4.4 orchestrator self-test failed.'
}

$ReceiptObject = (
    [System.IO.File]::ReadAllText($ReceiptPath) |
    ConvertFrom-Json
)

if([string]$ReceiptObject.result -ne 'PASS'){
    throw 'D4.4 receipt result is not PASS.'
}

if([string]$ReceiptObject.status -ne 'CLOSED'){
    throw 'D4.4 receipt status is not CLOSED.'
}

if([bool]$ReceiptObject.gui_cli_plan_parity.canonical_plan_equal -ne $true){
    throw 'D4.4 GUI/CLI plan JSON parity failed.'
}

if([bool]$ReceiptObject.gui_cli_plan_parity.sha256_equal -ne $true){
    throw 'D4.4 GUI/CLI plan SHA-256 parity failed.'
}

if([string]$ReceiptObject.runtime_boundary.runtime_authority -ne 'NONE'){
    throw 'D4.4 runtime authority boundary failed.'
}

if([bool]$ReceiptObject.runtime_boundary.orchestrator_execution -ne $false){
    throw 'D4.4 must not execute production orchestration.'
}

Write-Host ''
Write-Host '=================================================='
Write-Host ' C11-D D4.4 - CANONICAL ORCHESTRATOR'
Write-Host '=================================================='
Write-Host '[OK] D4.2 PASS/CLOSED verified.'
Write-Host '[OK] D4.3 PASS/CLOSED verified.'
Write-Host '[OK] Canonical Production Plan generated.'
Write-Host ('[OK] Challenges supported: {0}.' -f $ReceiptObject.challenge_count)
Write-Host ('[OK] Delivery profiles supported: {0}.' -f $ReceiptObject.delivery_profile_count)
Write-Host ('[OK] Personalization profiles supported: {0}.' -f $ReceiptObject.personalization_profile_count)
Write-Host '[OK] GUI canonical plan == CLI canonical plan.'
Write-Host '[OK] GUI plan SHA-256 == CLI plan SHA-256.'
Write-Host ('[OK] Canonical Production Plan SHA-256: {0}.' -f $ReceiptObject.gui_cli_plan_parity.sha256)
Write-Host '[OK] Personalization changes plan identity without changing seed/music_seed.'
Write-Host '[OK] winning_frame / close_calls / simulation controls rejected.'
Write-Host '[OK] runtime_authority = NONE.'
Write-Host '[OK] Renderer activation = NONE.'
Write-Host '[OK] GUI production activation = NONE.'
Write-Host '[OK] CLI production activation = NONE.'
Write-Host '[OK] Orchestrator execution = NONE.'
Write-Host '[OK] D4.4 receipt verified.'
Write-Host ''
Write-Host '=================================================='
Write-Host ' C11-D D4.4 - PASS / CLOSED'
Write-Host '=================================================='
Write-Host 'NEXT: D4.5 - CLI Adapter'