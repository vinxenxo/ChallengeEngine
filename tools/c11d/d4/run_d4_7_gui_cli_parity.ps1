#requires -Version 5.1
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 1.0

$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$ParityPath = Join-Path $ProjectRoot 'tools\c11d\d4\gui_cli_parity.py'
$ArtifactDir = Join-Path $ProjectRoot 'artifacts\tests\c11d_d4\d4_7'
$MatrixPath = Join-Path $ArtifactDir 'd4_7_parity_matrix.json'
$EvidencePath = Join-Path $ArtifactDir 'd4_7_parity_evidence.json'
$ReceiptPath = Join-Path $ArtifactDir 'd4_7_validation_receipt.json'
$DocsDir = Join-Path $ProjectRoot 'docs\current\d'
$ContractPath = Join-Path $DocsDir 'D4.7_GUI_CLI_PARITY_CONTRACT.md'
$MasterPath = Join-Path $DocsDir 'MASTER_HANDOVER_C11D_CURRENT.md'
$StartPath = Join-Path $DocsDir 'START_PROMPT_C11D_CURRENT.md'
$Utf8NoBom = New-Object -TypeName System.Text.UTF8Encoding -ArgumentList @($false)
$NewLine = [Environment]::NewLine

if(-not (Test-Path -LiteralPath $ParityPath)){
    throw 'D4.7 parity matrix runner is missing.'
}

foreach($Checkpoint in @('d4_2','d4_3','d4_4','d4_5','d4_6')){
    $PreviousReceiptPath = Join-Path $ProjectRoot (Join-Path 'artifacts\tests\c11d_d4' (Join-Path $Checkpoint ($Checkpoint + '_validation_receipt.json')))
    if(-not (Test-Path -LiteralPath $PreviousReceiptPath)){
        throw "Required predecessor receipt is missing: $PreviousReceiptPath"
    }
    $Previous = [System.IO.File]::ReadAllText($PreviousReceiptPath) | ConvertFrom-Json
    if([string]$Previous.result -ne 'PASS' -or [string]$Previous.status -ne 'CLOSED'){
        throw "Required predecessor is not PASS/CLOSED: $Checkpoint"
    }
}

New-Item -ItemType Directory -Force -Path $ArtifactDir | Out-Null
& python.exe $ParityPath --output-dir $ArtifactDir
if($LASTEXITCODE -ne 0){
    throw 'D4.7 parity matrix did not achieve a full PASS.'
}

$Matrix = [System.IO.File]::ReadAllText($MatrixPath) | ConvertFrom-Json
$Evidence = [System.IO.File]::ReadAllText($EvidencePath) | ConvertFrom-Json
$Receipt = [System.IO.File]::ReadAllText($ReceiptPath) | ConvertFrom-Json

if([string]$Receipt.result -ne 'PASS' -or [string]$Receipt.status -ne 'CLOSED'){
    throw 'D4.7 receipt is not PASS/CLOSED.'
}
if([int]$Receipt.test_cases -ne 102 -or [int]$Receipt.passed_cases -ne 102 -or [int]$Receipt.failed_cases -ne 0){
    throw 'D4.7 requires exactly 102/102 passing cases.'
}
foreach($Gate in @('canonical_request_parity','interface_origin_normalized_unknown','request_sha256_parity','production_plan_parity','plan_sha256_parity','seed_isolation','personalization_isolation','plan_hash_owned_by_d44')){
    if(-not [bool]$Receipt.$Gate){throw "D4.7 receipt gate failed: $Gate"}
}
if([string]$Receipt.runtime_authority -ne 'NONE' -or [bool]$Receipt.renderer_activation -or [bool]$Receipt.production_execution){
    throw 'D4.7 runtime boundary failed.'
}
if([int]$Matrix.total_cases -ne 102 -or [int]$Matrix.passed_cases -ne 102 -or [int]$Matrix.failed_cases -ne 0){
    throw 'D4.7 parity matrix does not report 102/102.'
}
if([int]$Evidence.challenge_coverage -ne 9 -or [int]$Evidence.delivery_profile_coverage -ne 5 -or [int]$Evidence.mode_coverage -ne 2){
    throw 'D4.7 coverage evidence is incomplete.'
}

$ContractText = @'
# C11-D D4.7 - GUI / CLI Parity Acceptance Contract

## Status

PASS / CLOSED. Next: D4.8 - Production Activation Governance.

## Objective

D4.7 adds no pipeline component. It exercises the existing GUI adapter (D4.6) and CLI adapter (D4.5) across the D4.1 vocabulary and compares their D4.2 canonical requests, request SHA-256 values, D4.4 Production Plans, and plan SHA-256 values with exact structural equality and no tolerance.

## Acceptance matrix

- 90 core cases: 9 Challenges x 5 delivery profiles x 2 modes.
- 12 personalization cases: 3 selected Challenges x 2 modes x 2 registered profiles.
- Required gate: 102 of 102 cases pass, with zero failures.
- For every pair, GUI and CLI input differ only in `request_origin` (`GUI` versus `CLI`). D4.2 canonicalizes that provenance as `UNKNOWN`.
- Every case compares canonical request structure and hash, plan structure and hash, runtime authority, renderer/execution flags, and D4.4 hash ownership.

## Personalization and seeds

For both adapters, changing `player_name` from ANA to LUIS must preserve `seed` and `music_seed` while changing the D4.3 personalization hash and D4.4 plan hash.

## Validation and ownership

Negative cases verify that missing `music_seed` is rejected by D4.2, a non-allowlisted personalization field is rejected by D4.3, and `winning_frame` is rejected by the canonical request normalizer. D4.7 contains no replacement validation rules.

The plan and plan hash are produced by `canonical_production_orchestrator.py`. GUI and CLI are consumers; neither adapter owns or alters plan identity.

## Runtime boundary

REVIEW and PRODUCTION cases both stop at plan creation. Renderer activation and production execution are false, runtime authority is `NONE`, and no simulation-derived controls enter requests.

## Evidence

- Matrix: `artifacts/tests/c11d_d4/d4_7/d4_7_parity_matrix.json`
- Evidence: `artifacts/tests/c11d_d4/d4_7/d4_7_parity_evidence.json`
- Receipt: `artifacts/tests/c11d_d4/d4_7/d4_7_validation_receipt.json`
- Comparator: `tools/c11d/d4/gui_cli_parity.py`
- Runner: `tools/c11d/d4/run_d4_7_gui_cli_parity.ps1`
'@
[System.IO.File]::WriteAllText($ContractPath,$ContractText + $NewLine,$Utf8NoBom)

$CurrentState = @'
## Current state - D4.7

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
NEXT: D4.8 - Production Activation Governance.

D4.7 passed all 102 exact GUI/CLI parity cases. Runtime authority remains NONE; renderer activation and production execution remain false.

'@
$MasterText = [System.IO.File]::ReadAllText($MasterPath)
$MasterPattern = '(?s)## Current state[^\r\n]*\r?\n.*?(?=## Strategic objective)'
if(-not [System.Text.RegularExpressions.Regex]::IsMatch($MasterText,$MasterPattern)){
    throw 'Could not locate current state section in MASTER_HANDOVER.'
}
$MasterText = [System.Text.RegularExpressions.Regex]::Replace($MasterText,$MasterPattern,($CurrentState + $NewLine),1)
$HandoffMarker = '<!-- C11D_D4_7_HANDOFF_V1 -->'
$Handoff = @'
<!-- C11D_D4_7_HANDOFF_V1 -->

## C11-D D4.7 CLOSED / PASS

- Exact 102/102 GUI/CLI parity cases passed: 90 Challenge/profile/mode combinations and 12 personalization combinations.
- Canonical request JSON and SHA-256 matched for every pair.
- Production Plan JSON and SHA-256 matched for every pair.
- `request_origin` is normalized to UNKNOWN and excluded from semantic identity.
- Personalization changes its identity and plan hash without changing `seed` or `music_seed` through either adapter.
- D4.2/D4.3 negative validation remained authoritative; forbidden simulation controls are rejected.
- D4.4 owns plan identity. Renderer activation and production execution remain false; runtime authority is NONE.
- Contract: `docs/current/d/D4.7_GUI_CLI_PARITY_CONTRACT.md`.
- Matrix, evidence, and receipt: `artifacts/tests/c11d_d4/d4_7/`.
- Next active checkpoint: **D4.8 - Production Activation Governance**.
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
Continue ChallengeEngineV01_STATELESS from C11-D D4.7 CLOSED / PASS.

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
NEXT = D4.8 - Production Activation Governance.

All 102 D4.7 GUI/CLI parity cases pass. D4.4 owns plan identity. Renderer activation and production execution remain false; runtime authority is NONE. C11-C 2.19.12 remains frozen and immutable.

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
        throw "D4.7 output missing: $Required"
    }
}

Write-Host '=================================================='
Write-Host ' C11-D D4.7 - GUI / CLI PARITY ACCEPTANCE'
Write-Host '=================================================='
Write-Host '[OK] D4.2 PASS/CLOSED verified.'
Write-Host '[OK] D4.3 PASS/CLOSED verified.'
Write-Host '[OK] D4.4 PASS/CLOSED verified.'
Write-Host '[OK] D4.5 PASS/CLOSED verified.'
Write-Host '[OK] D4.6 PASS/CLOSED verified.'
Write-Host '[OK] Challenges discovered: 9.'
Write-Host '[OK] Delivery profiles discovered: 5.'
Write-Host '[OK] Core matrix: 90/90.'
Write-Host '[OK] Personalization matrix: 12/12.'
Write-Host '[OK] Canonical request JSON and SHA-256 parity: PASS.'
Write-Host '[OK] Production Plan JSON and SHA-256 parity: PASS.'
Write-Host '[OK] Seed isolation and personalization identity: PASS.'
Write-Host '[OK] D4.4 owns all Production Plan hashes.'
Write-Host '[OK] Renderer activation = FALSE.'
Write-Host '[OK] Production execution = FALSE.'
Write-Host '[OK] Runtime authority = NONE.'
Write-Host '[OK] Contract and current handovers updated.'
Write-Host ''
Write-Host '=================================================='
Write-Host ' C11-D D4.7 - PASS / CLOSED'
Write-Host '=================================================='
Write-Host 'NEXT: D4.8 - Production Activation Governance'
