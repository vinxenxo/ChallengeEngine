#requires -Version 5.1
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 1.0

$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$GovernancePath = Join-Path $ProjectRoot 'tools\c11d\d4\production_activation_governance.py'
$PolicyPath = Join-Path $ProjectRoot 'definitions\c11d\production\C11D_PRODUCTION_ACTIVATION_POLICY_V1.json'
$ArtifactDir = Join-Path $ProjectRoot 'artifacts\tests\c11d_d4\d4_8'
$MatrixPath = Join-Path $ArtifactDir 'd4_8_governance_matrix.json'
$EvidencePath = Join-Path $ArtifactDir 'd4_8_authorization_evidence.json'
$ReceiptPath = Join-Path $ArtifactDir 'd4_8_validation_receipt.json'
$DocsDir = Join-Path $ProjectRoot 'docs\current\d'
$ContractPath = Join-Path $DocsDir 'D4.8_PRODUCTION_ACTIVATION_GOVERNANCE_CONTRACT.md'
$MasterPath = Join-Path $DocsDir 'MASTER_HANDOVER_C11D_CURRENT.md'
$StartPath = Join-Path $DocsDir 'START_PROMPT_C11D_CURRENT.md'
$Utf8NoBom = New-Object -TypeName System.Text.UTF8Encoding -ArgumentList @($false)
$NewLine = [Environment]::NewLine

if(-not (Test-Path -LiteralPath $GovernancePath)){
    throw 'D4.8 governance evaluator is missing.'
}
if(-not (Test-Path -LiteralPath $PolicyPath)){
    throw 'D4.8 activation policy is missing.'
}

foreach($Checkpoint in @('d4_2','d4_3','d4_4','d4_5','d4_6','d4_7')){
    $PreviousReceiptPath = Join-Path $ProjectRoot (Join-Path 'artifacts\tests\c11d_d4' (Join-Path $Checkpoint ($Checkpoint + '_validation_receipt.json')))
    if(-not (Test-Path -LiteralPath $PreviousReceiptPath)){
        throw "Required predecessor receipt is missing: $PreviousReceiptPath"
    }
    $Previous = [System.IO.File]::ReadAllText($PreviousReceiptPath) | ConvertFrom-Json
    if([string]$Previous.result -ne 'PASS' -or [string]$Previous.status -ne 'CLOSED'){
        throw "Required predecessor is not PASS/CLOSED: $Checkpoint"
    }
}

$Policy = [System.IO.File]::ReadAllText($PolicyPath) | ConvertFrom-Json
if([string]$Policy.renderer_activation_policy.state -ne 'DISABLED'){
    throw 'D4.8 renderer policy must remain DISABLED.'
}

New-Item -ItemType Directory -Force -Path $ArtifactDir | Out-Null
& python.exe $GovernancePath --output-dir $ArtifactDir
if($LASTEXITCODE -ne 0){
    throw 'D4.8 governance test suite failed.'
}

$Matrix = [System.IO.File]::ReadAllText($MatrixPath) | ConvertFrom-Json
$Evidence = [System.IO.File]::ReadAllText($EvidencePath) | ConvertFrom-Json
$Receipt = [System.IO.File]::ReadAllText($ReceiptPath) | ConvertFrom-Json
if([string]$Receipt.result -ne 'PASS' -or [string]$Receipt.status -ne 'CLOSED'){
    throw 'D4.8 receipt is not PASS/CLOSED.'
}
if(-not [bool]$Receipt.predecessors_closed -or [string]$Receipt.renderer_policy -ne 'DISABLED'){
    throw 'D4.8 predecessor or renderer policy gate failed.'
}
if([bool]$Receipt.production_authorization -or [bool]$Receipt.renderer_called -or [bool]$Receipt.production_execution){
    throw 'D4.8 must not authorize or execute physical production under DISABLED policy.'
}
if([string]$Receipt.runtime_authority -ne 'NONE'){
    throw 'D4.8 runtime authority must remain NONE.'
}
if([int]$Matrix.total_cases -ne [int]$Matrix.passed_cases -or [int]$Matrix.failed_cases -ne 0){
    throw 'D4.8 governance matrix has failed cases.'
}
if([string]$Evidence.production_blocked_reasons -notmatch 'RENDERER_POLICY_DISABLED'){
    throw 'D4.8 did not block PRODUCTION for the disabled renderer policy.'
}
if([string]$Evidence.review_blocked_reasons -notmatch 'REVIEW_MODE'){
    throw 'D4.8 did not block REVIEW authorization.'
}

$ContractText = @'
# C11-D D4.8 - Production Activation Governance Contract

## Status

PASS / CLOSED. The physical renderer remains DISABLED. Next: D4.9 - Full D4 Acceptance.

## Purpose

D4.8 evaluates whether a D4.4 Production Plan satisfies the declarative activation policy. It returns AUTHORIZED or BLOCKED and provenance evidence. It never invokes a renderer, encoder, simulator, Godot, FFmpeg, or production execution.

## Formal lifecycle states

The policy defines `DRAFT`, `NORMALIZED`, `PLANNED`, `VALIDATED`, `AUTHORIZED`, `EXECUTING`, `COMPLETED`, `FAILED`, and `BLOCKED`. D4.8 can report states through `AUTHORIZED` and `BLOCKED`; `EXECUTING`, `COMPLETED`, and `FAILED` are reserved for later phases. A plan authorization decision does not mean media was produced.

## Authorization rules

- REVIEW requests may validate but are never authorized for physical production; the reason is `REVIEW_MODE`.
- PRODUCTION requires all D4.2-D4.7 predecessors PASS/CLOSED, request and plan integrity, valid provenance, isolated seeds, a registered personalization profile/version, and a known delivery profile.
- The delivery-profile vocabulary is read from the evidence-backed `delivery_profile_id.evidence_values` declaration in the D4.1 Production Request schema. No separate delivery profile registry exists in the current definitions tree.
- A PRODUCTION request with all validation gates passing is still BLOCKED with `RENDERER_POLICY_DISABLED` under the D4.8 policy.
- D4.8 verifies plan identity using D4.4's `canonical_production_orchestrator.sha256`; it does not own or replace plan hashing.
- Request identity is verified with D4.2's normalizer hash and rebound to the plan by rebuilding through D4.4. Personalization profile and values are verified through D4.3.
- Seed collision is rejected. The dedicated music seed must match the plan's music step and must not consume gameplay or structural RNG.

## Policy

`definitions/c11d/production/C11D_PRODUCTION_ACTIVATION_POLICY_V1.json` is the versioned policy source. Renderer state is `DISABLED`; REVIEW authorization is false; provenance and predecessor requirements are explicit. Policy approval can create an authorization decision in a future governance state, but D4.8 itself does not execute production.

## Evidence

- Evaluator: `tools/c11d/d4/production_activation_governance.py`
- Runner: `tools/c11d/d4/run_d4_8_activation_governance.ps1`
- Matrix: `artifacts/tests/c11d_d4/d4_8/d4_8_governance_matrix.json`
- Evidence: `artifacts/tests/c11d_d4/d4_8/d4_8_authorization_evidence.json`
- Receipt: `artifacts/tests/c11d_d4/d4_8/d4_8_validation_receipt.json`

The gate covers REVIEW, PRODUCTION blocked by renderer policy, an open predecessor, modified plan/request hashes, modified seed/personalization, seed collision, provenance, profile registration, and deterministic authorization output. Physical execution flags remain false and runtime authority is `NONE`.
'@
[System.IO.File]::WriteAllText($ContractPath,$ContractText + $NewLine,$Utf8NoBom)

$CurrentState = @'
## Current state - D4.8

D0: CLOSED / PASS
D1: functional checkpoints complete
D2: CLOSED
D3: CLOSED / PASS
D4.0: PASS / CLOSED
D4.1: PASS / CLOSED
D4.2: PASS / CLOSED
D4.3: PASS / CLOSED
D4.4: PASS / CLOSED
D4.5: PASS / CLOSED
D4.6: PASS / CLOSED
D4.7: PASS / CLOSED
D4.8: PASS / CLOSED
NEXT: D4.9 - Full D4 Acceptance.

D4.8 governance is active as a decision-only gate. Renderer policy is DISABLED and physical production is NOT AUTHORIZED; runtime authority is NONE.

'@
$MasterText = [System.IO.File]::ReadAllText($MasterPath)
$MasterPattern = '(?s)## Current state[^\r\n]*\r?\n.*?(?=## Strategic objective)'
if(-not [System.Text.RegularExpressions.Regex]::IsMatch($MasterText,$MasterPattern)){
    throw 'Could not locate current state section in MASTER_HANDOVER.'
}
$MasterText = [System.Text.RegularExpressions.Regex]::Replace($MasterText,$MasterPattern,($CurrentState + $NewLine),1)
$HandoffMarker = '<!-- C11D_D4_8_HANDOFF_V1 -->'
$Handoff = @'
<!-- C11D_D4_8_HANDOFF_V1 -->

## C11-D D4.8 CLOSED / PASS

- Added versioned production activation policy and decision-only governance evaluator.
- D4.2-D4.7 receipts must all be PASS/CLOSED.
- D4.2 request identity, D4.4 plan identity, D4.3 personalization profile/version, D4.1 delivery profile vocabulary, seeds, and provenance are checked.
- REVIEW is validated but blocked with `REVIEW_MODE`.
- PRODUCTION passes validation but is blocked with `RENDERER_POLICY_DISABLED`.
- Tampered plan, request, seed, and personalization data are rejected; seed collision is explicitly rejected.
- Authorization is deterministic. D4.4 remains owner of Production Plan hashes.
- Renderer, FFmpeg/Godot production calls, and physical execution remain false; runtime authority is NONE.
- Contract: `docs/current/d/D4.8_PRODUCTION_ACTIVATION_GOVERNANCE_CONTRACT.md`.
- Policy: `definitions/c11d/production/C11D_PRODUCTION_ACTIVATION_POLICY_V1.json`.
- Evidence, matrix, and receipt: `artifacts/tests/c11d_d4/d4_8/`.
- Next active checkpoint: **D4.9 - Full D4 Acceptance**.
'@
if(-not $MasterText.Contains($HandoffMarker)){
    $MasterText = $MasterText.TrimEnd() + $NewLine + $NewLine + $Handoff + $NewLine
}
[System.IO.File]::WriteAllText($MasterPath,$MasterText,$Utf8NoBom)

$StartText = [System.IO.File]::ReadAllText($StartPath)
$StartTitle = '# C11-D START PROMPT'
$StartTitleIndex = $StartText.IndexOf($StartTitle,[System.StringComparison]::Ordinal)
$ReadFirstIndex = $StartText.IndexOf('## Read first',[System.StringComparison]::Ordinal)
if($StartTitleIndex -lt 0 -or $ReadFirstIndex -le $StartTitleIndex){
    throw 'Could not locate current state section in START_PROMPT.'
}
$StartCurrent = @'
Continue ChallengeEngineV01_STATELESS from C11-D D4.8 CLOSED / PASS.

## Current D state

D0 = CLOSED / PASS
D1 = functional checkpoints complete
D2 = CLOSED
D3 = CLOSED / PASS
D4.0 = PASS / CLOSED
D4.1 = PASS / CLOSED
D4.2 = PASS / CLOSED
D4.3 = PASS / CLOSED
D4.4 = PASS / CLOSED
D4.5 = PASS / CLOSED
D4.6 = PASS / CLOSED
D4.7 = PASS / CLOSED
D4.8 = PASS / CLOSED
NEXT = D4.9 - Full D4 Acceptance.

D4.8 is authorization governance only. Renderer policy is DISABLED, production is NOT AUTHORIZED, and physical execution remains false. Runtime authority is NONE. C11-C 2.19.12 remains frozen and immutable.

'@
$StartPrefix = $StartText.Substring(0,$StartTitleIndex + $StartTitle.Length)
$StartSuffix = $StartText.Substring($ReadFirstIndex)
$StartText = $StartPrefix + $NewLine + $NewLine + $StartCurrent + $NewLine + $StartSuffix
if(-not $StartText.Contains($HandoffMarker)){
    $StartText = $StartText.TrimEnd() + $NewLine + $NewLine + $Handoff + $NewLine
}
[System.IO.File]::WriteAllText($StartPath,$StartText,$Utf8NoBom)

foreach($Required in @($MatrixPath,$EvidencePath,$ReceiptPath,$ContractPath,$MasterPath,$StartPath)){
    if(-not (Test-Path -LiteralPath $Required)){
        throw "D4.8 output missing: $Required"
    }
}

Write-Host '=================================================='
Write-Host ' C11-D D4.8 - ACTIVATION GOVERNANCE'
Write-Host '=================================================='
Write-Host '[OK] D4.2-D4.7 PASS/CLOSED verified.'
Write-Host '[OK] Formal lifecycle states verified.'
Write-Host '[OK] REVIEW validated and blocked by REVIEW_MODE.'
Write-Host '[OK] PRODUCTION validated and blocked by RENDERER_POLICY_DISABLED.'
Write-Host '[OK] Open predecessor blocked.'
Write-Host '[OK] Plan/request hash integrity verified.'
Write-Host '[OK] Tampered duration, music_seed, and personalization rejected.'
Write-Host '[OK] Seed collision rejected.'
Write-Host '[OK] D4.3 profile/version and D4.1 delivery profile verified.'
Write-Host '[OK] Provenance and seed isolation verified.'
Write-Host '[OK] Authorization decision is idempotent.'
Write-Host '[OK] D4.4 remains owner of plan hash.'
Write-Host '[OK] Renderer called = FALSE.'
Write-Host '[OK] FFmpeg/Godot production called = FALSE.'
Write-Host '[OK] Physical production = NOT AUTHORIZED.'
Write-Host '[OK] Runtime authority = NONE.'
Write-Host '[OK] Contract and current handovers updated.'
Write-Host ''
Write-Host '=================================================='
Write-Host ' C11-D D4.8 - PASS / CLOSED'
Write-Host '=================================================='
Write-Host 'NEXT: D4.9 - Full D4 Acceptance'
