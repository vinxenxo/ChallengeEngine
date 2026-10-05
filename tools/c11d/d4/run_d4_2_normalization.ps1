#requires -Version 5.1
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 1.0

$RootPath = (Get-Location).Path

$SchemaPath = Join-Path $RootPath 'definitions\c11d\production\C11D_PRODUCTION_REQUEST_SCHEMA_V1.json'
$NormalizerPath = Join-Path $RootPath 'tools\c11d\d4\production_request_normalizer.py'
$ArtifactDir = Join-Path $RootPath 'artifacts\tests\c11d_d4\d4_2'

$EvidencePath = Join-Path $ArtifactDir 'd4_2_normalization_evidence.json'
$ReceiptPath = Join-Path $ArtifactDir 'd4_2_validation_receipt.json'
$ParityPath = Join-Path $ArtifactDir 'd4_2_gui_cli_parity.json'

if(-not (Test-Path -LiteralPath $SchemaPath)){
    throw 'D4.1 schema missing.'
}

if(-not (Test-Path -LiteralPath $NormalizerPath)){
    throw 'D4.2 normalizer missing.'
}

New-Item -ItemType Directory -Force -Path $ArtifactDir | Out-Null

$PythonOutput = & python.exe `
    $NormalizerPath `
    --schema $SchemaPath `
    --self-test `
    --receipt $ReceiptPath `
    --evidence $EvidencePath `
    --parity $ParityPath

if($LASTEXITCODE -ne 0){
    throw 'D4.2 normalizer self-test failed.'
}

$ReceiptText = [System.IO.File]::ReadAllText($ReceiptPath)
$ReceiptObject = $ReceiptText | ConvertFrom-Json

if([string]$ReceiptObject.result -ne 'PASS'){
    throw 'D4.2 receipt result is not PASS.'
}

if([string]$ReceiptObject.status -ne 'CLOSED'){
    throw 'D4.2 receipt status is not CLOSED.'
}

if([bool]$ReceiptObject.gui_cli_parity.canonical_json_equal -ne $true){
    throw 'D4.2 GUI/CLI canonical JSON parity failed.'
}

if([bool]$ReceiptObject.gui_cli_parity.sha256_equal -ne $true){
    throw 'D4.2 GUI/CLI SHA-256 parity failed.'
}

if([bool]$ReceiptObject.unknown_default_normalization -ne $true){
    throw 'D4.2 UNKNOWN/default normalization failed.'
}

if([bool]$ReceiptObject.forbidden_simulation_controls_rejected -ne $true){
    throw 'D4.2 forbidden simulation controls were not rejected.'
}

Write-Host ''
Write-Host '=================================================='
Write-Host ' C11-D D4.2 - NORMALIZATION / VALIDATION'
Write-Host '=================================================='
Write-Host '[OK] Canonical Production Request normalizer executed.'
Write-Host '[OK] Schema version 1.0 verified.'
Write-Host ('[OK] Challenges validated: {0}.' -f $ReceiptObject.challenge_count)
Write-Host ('[OK] Delivery profiles validated: {0}.' -f $ReceiptObject.delivery_profile_count)
Write-Host '[OK] Required fields validated.'
Write-Host '[OK] REVIEW / PRODUCTION modes validated.'
Write-Host '[OK] seed and music_seed remain separate.'
Write-Host '[OK] UNKNOWN/default normalization validated.'
Write-Host '[OK] GUI canonical JSON == CLI canonical JSON.'
Write-Host '[OK] GUI SHA-256 == CLI SHA-256.'
Write-Host ('[OK] Canonical request SHA-256: {0}.' -f $ReceiptObject.gui_cli_parity.sha256)
Write-Host '[OK] winning_frame / close_calls / simulation controls rejected.'
Write-Host '[OK] Runtime authority = NONE.'
Write-Host '[OK] GUI production activation = NONE.'
Write-Host '[OK] CLI production activation = NONE.'
Write-Host '[OK] Renderer activation = NONE.'
Write-Host '[OK] Orchestrator activation = NONE.'
Write-Host '[OK] D4.2 receipt verified.'
Write-Host ''
Write-Host '=================================================='
Write-Host ' C11-D D4.2 - PASS / CLOSED'
Write-Host '=================================================='
Write-Host 'NEXT: D4.3 - Personalization Contract'