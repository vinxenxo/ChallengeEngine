#requires -Version 5.1
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 1.0

$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$AcceptancePath = Join-Path $ProjectRoot 'tools\c11d\d4\d4_full_acceptance.py'
$ArtifactDir = Join-Path $ProjectRoot 'artifacts\tests\c11d_d4\d4_9'
$MatrixPath = Join-Path $ArtifactDir 'd4_9_acceptance_matrix.json'
$EvidencePath = Join-Path $ArtifactDir 'd4_9_regression_evidence.json'
$ReceiptPath = Join-Path $ArtifactDir 'd4_9_validation_receipt.json'
$DocsDir = Join-Path $ProjectRoot 'docs\current\d'
$ContractPath = Join-Path $DocsDir 'D4.9_FULL_D4_ACCEPTANCE_CONTRACT.md'
$MasterPath = Join-Path $DocsDir 'MASTER_HANDOVER_C11D_CURRENT.md'
$StartPath = Join-Path $DocsDir 'START_PROMPT_C11D_CURRENT.md'
$HistoryDir = Join-Path $ProjectRoot 'docs\history\master-prompts\c11d'
$NewLine = [Environment]::NewLine
$Utf8NoBom = New-Object -TypeName System.Text.UTF8Encoding -ArgumentList @($false)

if(-not (Test-Path -LiteralPath $AcceptancePath)){
    throw 'D4.9 acceptance evaluator is missing.'
}
New-Item -ItemType Directory -Force -Path $ArtifactDir,$HistoryDir | Out-Null

& python.exe $AcceptancePath --output-dir $ArtifactDir
$AcceptanceExitCode = $LASTEXITCODE
if(-not (Test-Path -LiteralPath $ReceiptPath)){
    throw 'D4.9 validation receipt was not produced.'
}

$Matrix = [System.IO.File]::ReadAllText($MatrixPath) | ConvertFrom-Json
$Evidence = [System.IO.File]::ReadAllText($EvidencePath) | ConvertFrom-Json
$Receipt = [System.IO.File]::ReadAllText($ReceiptPath) | ConvertFrom-Json
$IsPass = (
    $AcceptanceExitCode -eq 0 -and
    [string]$Receipt.result -eq 'PASS' -and
    [string]$Receipt.status -eq 'CLOSED' -and
    [bool]$Receipt.d4_complete
)

$ContractStatus = if($IsPass){'PASS / CLOSED'}else{'BLOCKED; see d4_9_validation_receipt.json'}
$NextText = if($IsPass){'D5 - Artifact Topology + Provenance'}else{'D4.9 - Resolve blocked acceptance gates'}
$ContractText = @"
# C11-D D4.9 - Full D4 Acceptance Contract

## Status

$ContractStatus

## Purpose

D4.9 is an acceptance runner, not another functional pipeline component. It runs the focused D4.2-D4.8 regressions and verifies the recorded D4.0-D4.8 receipts, architecture, GUI/CLI parity, governance, hashes, frozen C11-C identity, and runtime boundary. It does not reconstruct missing checkpoint states or repair hashes to force a pass.

## Acceptance gates

1. D4.0 through D4.8 receipts report PASS / CLOSED.
2. GUI and CLI adapters use the same D4.2 normalizer, D4.3 resolver, and D4.4 orchestrator; no parallel renderer/Godot path is present.
3. D4.7 remains 102/102 with structural request and plan equality and matching hashes.
4. D4.8 remains 8/8, renderer DISABLED, and production authorization false.
5. D4.2, D4.4, D4.6, D4.7, and D4.8 request/plan/authorization hash links agree.
6. The D4.0 frozen C11-C archive identity remains `$($Receipt.frozen_c11c_archive_sha256)`; the archive is not reopened by D4.9.
7. Static runtime scan and predecessor evidence show renderer activation false, production execution false, and runtime authority NONE.
8. The acceptance summary is deterministic and repeatable.

## D4 closure meaning

D4 CLOSED means canonical Production Request normalization, personalization resolution, Production Plan orchestration, CLI and GUI adapters, GUI/CLI parity, activation governance, and full acceptance are consolidated.

D4 CLOSED does not mean physical production is active. It does not activate a renderer, batch production, MP4 generation, publishing, or upload. D4.8 keeps renderer policy DISABLED and physical production NOT AUTHORIZED. `AUTHORIZED` is a governance decision state, not proof that a video was generated.

## Delivery profile source

The five delivery profiles remain sourced from the D4.1 schema's evidence-backed `delivery_profile_id.evidence_values`. No independent delivery-profile registry is created by D4.9.

## Evidence

- Acceptance runner: `tools/c11d/d4/run_d4_9_full_acceptance.ps1`
- Regression evaluator: `tools/c11d/d4/d4_full_acceptance.py`
- Matrix: `artifacts/tests/c11d_d4/d4_9/d4_9_acceptance_matrix.json`
- Regression evidence: `artifacts/tests/c11d_d4/d4_9/d4_9_regression_evidence.json`
- Receipt: `artifacts/tests/c11d_d4/d4_9/d4_9_validation_receipt.json`

Next checkpoint: $NextText.
"@
[System.IO.File]::WriteAllText($ContractPath,$ContractText + $NewLine,$Utf8NoBom)

if(-not $IsPass){
    Write-Host 'D4.9 acceptance did not pass. Current handovers and closure snapshots were not advanced.'
    Write-Host ('Result: {0} / {1}' -f $Receipt.result,$Receipt.status)
    Write-Host ('Receipt: {0}' -f $ReceiptPath)
    exit 1
}

$CurrentState = @'
## Current state - D4 CLOSED

D0: CLOSED / PASS
D1: CLOSED / PASS
D2: CLOSED / PASS
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
D4.9: PASS / CLOSED
D4: CLOSED
NEXT: D5 - Artifact Topology + Provenance.

D4 closure consolidates the declarative request pipeline and governance. It does not activate physical production; renderer policy remains DISABLED and runtime authority remains NONE.

'@
$MasterText = [System.IO.File]::ReadAllText($MasterPath)
$MasterPattern = '(?s)## Current state[^\r\n]*\r?\n.*?(?=## Strategic objective)'
if(-not [System.Text.RegularExpressions.Regex]::IsMatch($MasterText,$MasterPattern)){
    throw 'Could not locate current state section in MASTER_HANDOVER.'
}
$MasterText = [System.Text.RegularExpressions.Regex]::Replace($MasterText,$MasterPattern,($CurrentState + $NewLine),1)
$HandoffMarker = '<!-- C11D_D4_9_HANDOFF_V1 -->'
$Handoff = @'
<!-- C11D_D4_9_HANDOFF_V1 -->

## C11-D D4.9 CLOSED / PASS - D4 CLOSED

- D4.0-D4.8 predecessor receipts and focused component regressions passed.
- The D4.7 GUI/CLI matrix remains 102/102 with canonical request, request SHA-256, plan, and plan SHA-256 parity.
- D4.8 governance remains 8/8; renderer policy is DISABLED and physical production is NOT AUTHORIZED.
- Request, plan, GUI/CLI parity, and authorization hash links are coherent; plan hash ownership remains with D4.4.
- Frozen C11-C archive identity remains the D4.0 recorded SHA-256; the frozen archive was not reopened.
- Runtime scan is clean; renderer activation and production execution are false; runtime authority is NONE.
- D4.9 contract: `docs/current/d/D4.9_FULL_D4_ACCEPTANCE_CONTRACT.md`.
- Matrix, regression evidence, and receipt: `artifacts/tests/c11d_d4/d4_9/`.
- D4 is CLOSED. Next: **D5 - Artifact Topology + Provenance**.
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
Continue ChallengeEngineV01_STATELESS from C11-D D4 CLOSED / PASS.

## Current D state

D0 = CLOSED / PASS
D1 = CLOSED / PASS
D2 = CLOSED / PASS
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
D4.9 = PASS / CLOSED
D4 = CLOSED
NEXT = D5 - Artifact Topology + Provenance.

D4 closure does not activate physical production. Renderer policy remains DISABLED; runtime authority is NONE. C11-C 2.19.12 remains frozen and immutable.

'@
$StartPrefix = $StartText.Substring(0,$StartTitleIndex + $StartTitle.Length)
$StartSuffix = $StartText.Substring($ReadFirstIndex)
$StartText = $StartPrefix + $NewLine + $NewLine + $StartCurrent + $NewLine + $StartSuffix
if(-not $StartText.Contains($HandoffMarker)){
    $StartText = $StartText.TrimEnd() + $NewLine + $NewLine + $Handoff + $NewLine
}
[System.IO.File]::WriteAllText($StartPath,$StartText,$Utf8NoBom)

$ContractTextCheck = [System.IO.File]::ReadAllText($ContractPath)
$MasterTextCheck = [System.IO.File]::ReadAllText($MasterPath)
$StartTextCheck = [System.IO.File]::ReadAllText($StartPath)
$ContractHeadingCount = [System.Text.RegularExpressions.Regex]::Matches(
    $ContractTextCheck,
    '(?m)^# C11-D D4\.9 - Full D4 Acceptance Contract$'
).Count
$MasterMarkerCount = [System.Text.RegularExpressions.Regex]::Matches(
    $MasterTextCheck,
    [System.Text.RegularExpressions.Regex]::Escape($HandoffMarker)
).Count
$StartMarkerCount = [System.Text.RegularExpressions.Regex]::Matches(
    $StartTextCheck,
    [System.Text.RegularExpressions.Regex]::Escape($HandoffMarker)
).Count
if($ContractHeadingCount -ne 1 -or $MasterMarkerCount -ne 1 -or $StartMarkerCount -ne 1){
    throw 'D4.9 idempotency check failed: duplicated contract section or handover marker.'
}

$UtcStamp = (Get-Date).ToUniversalTime().ToString('yyyyMMdd_HHmmss_fff')
Copy-Item -LiteralPath $MasterPath -Destination (Join-Path $HistoryDir ('MASTER_HANDOVER_C11D_D4_9_CLOSED_{0}.md' -f $UtcStamp))
Copy-Item -LiteralPath $StartPath -Destination (Join-Path $HistoryDir ('START_PROMPT_C11D_D4_9_CLOSED_{0}.md' -f $UtcStamp))

foreach($Required in @($MatrixPath,$EvidencePath,$ReceiptPath,$ContractPath,$MasterPath,$StartPath)){
    if(-not (Test-Path -LiteralPath $Required)){
        throw "D4.9 acceptance output missing: $Required"
    }
}

Write-Host '=================================================='
Write-Host ' C11-D D4.9 - FULL D4 ACCEPTANCE'
Write-Host '=================================================='
foreach($Checkpoint in @('D4.0','D4.1','D4.2','D4.3','D4.4','D4.5','D4.6','D4.7','D4.8')){
    Write-Host (('[OK] {0} PASS/CLOSED' -f $Checkpoint))
}
Write-Host '[OK] Canonical Production Request integrity.'
Write-Host '[OK] GUI / CLI parity: 102/102.'
Write-Host '[OK] Production Plan integrity.'
Write-Host '[OK] Governance integrity: 8/8.'
Write-Host '[OK] Frozen C11-C archive identity preserved.'
Write-Host '[OK] Runtime boundary clean.'
Write-Host '[OK] Idempotency PASS.'
Write-Host '[OK] No duplicate handover markers.'
Write-Host '[OK] D4 acceptance complete.'
Write-Host ''
Write-Host '=================================================='
Write-Host ' C11-D D4.9 - PASS / CLOSED'
Write-Host ' D4 = CLOSED'
Write-Host '=================================================='
Write-Host 'NEXT: D5 - Artifact Topology + Provenance'
Write-Host ('ACCEPTANCE SHA-256: {0}' -f $Receipt.acceptance_sha256)
Write-Host ('SNAPSHOT UTC: {0}' -f $UtcStamp)
