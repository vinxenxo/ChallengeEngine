#requires -Version 5.1
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 1.0

$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$CliPath = Join-Path $ProjectRoot 'tools\c11d\d4\production_cli.py'
$ArtifactDir = Join-Path $ProjectRoot 'artifacts\tests\c11d_d4\d4_5'
$EvidencePath = Join-Path $ArtifactDir 'd4_5_cli_adapter_evidence.json'
$PlanPath = Join-Path $ArtifactDir 'd4_5_cli_plan.json'
$ReceiptPath = Join-Path $ArtifactDir 'd4_5_validation_receipt.json'

if(-not (Test-Path -LiteralPath $CliPath)){
    throw 'D4.5 CLI adapter is missing.'
}

New-Item -ItemType Directory -Force -Path $ArtifactDir | Out-Null

& python.exe $CliPath `
    --self-test `
    --evidence $EvidencePath `
    --plan $PlanPath `
    --receipt $ReceiptPath

if($LASTEXITCODE -ne 0){
    throw 'D4.5 CLI adapter self-test failed.'
}

$Receipt = [System.IO.File]::ReadAllText($ReceiptPath) | ConvertFrom-Json
$Plan = [System.IO.File]::ReadAllText($PlanPath) | ConvertFrom-Json

if([string]$Receipt.result -ne 'PASS' -or [string]$Receipt.status -ne 'CLOSED'){
    throw 'D4.5 receipt is not PASS/CLOSED.'
}

foreach($RequiredPass in @(
    'cli_adapter',
    'canonical_normalizer_reused',
    'personalization_resolver_reused',
    'orchestrator_reused',
    'review_request_pass',
    'production_request_pass',
    'deterministic_repeat_pass',
    'invalid_request_rejected',
    'invalid_personalization_rejected',
    'forbidden_simulation_controls_rejected'
)){
    if(-not [bool]$Receipt.$RequiredPass){
        throw "D4.5 receipt gate failed: $RequiredPass"
    }
}

if([string]$Receipt.runtime_authority -ne 'NONE'){
    throw 'D4.5 runtime authority must remain NONE.'
}

if([bool]$Receipt.renderer_activation -or [bool]$Receipt.production_execution){
    throw 'D4.5 must not activate renderer or production execution.'
}

if([string]$Plan.mode -ne 'PRODUCTION'){
    throw 'D4.5 stored CLI plan must represent the PRODUCTION request.'
}

if([string]$Plan.runtime_authority -ne 'NONE' -or [bool]$Plan.renderer_activation -or [bool]$Plan.orchestrator_execution){
    throw 'D4.5 stored plan crossed the plan-only runtime boundary.'
}

Write-Host ''
Write-Host '=================================================='
Write-Host ' C11-D D4.5 - CLI ADAPTER'
Write-Host '=================================================='
Write-Host '[OK] Canonical D4.2 normalizer reused.'
Write-Host '[OK] D4.3 personalization resolver reused.'
Write-Host '[OK] D4.4 canonical orchestrator reused.'
Write-Host '[OK] REVIEW request validated and planned.'
Write-Host '[OK] PRODUCTION request planned without execution.'
Write-Host '[OK] Invalid request rejected by D4.2.'
Write-Host '[OK] Invalid personalization rejected by D4.3.'
Write-Host '[OK] Forbidden simulation control rejected.'
Write-Host '[OK] Deterministic repeat produced identical plan and SHA-256.'
Write-Host ('[OK] Plan SHA-256 owned by D4.4: {0}.' -f $Receipt.production_plan_sha256)
Write-Host '[OK] CLI added no plan identity fields.'
Write-Host '[OK] Renderer activation = FALSE.'
Write-Host '[OK] Production execution = FALSE.'
Write-Host '[OK] runtime_authority = NONE.'
Write-Host '[OK] D4.5 receipt verified.'
Write-Host ''
Write-Host '=================================================='
Write-Host ' C11-D D4.5 - PASS / CLOSED'
Write-Host '=================================================='
Write-Host 'NEXT: D4.6 - GUI Adapter'
