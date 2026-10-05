#requires -Version 5.1
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 1.0

$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$GuiAdapterPath = Join-Path $ProjectRoot 'tools\c11d\d4\gui_production_adapter.py'
$ArtifactDir = Join-Path $ProjectRoot 'artifacts\tests\c11d_d4\d4_6'
$EvidencePath = Join-Path $ArtifactDir 'd4_6_gui_adapter_evidence.json'
$PlanPath = Join-Path $ArtifactDir 'd4_6_gui_plan.json'
$ParityPath = Join-Path $ArtifactDir 'd4_6_gui_cli_parity.json'
$ReceiptPath = Join-Path $ArtifactDir 'd4_6_validation_receipt.json'
$DocsDir = Join-Path $ProjectRoot 'docs\current\d'
$ContractPath = Join-Path $DocsDir 'D4.6_GUI_ADAPTER_CONTRACT.md'
$MasterPath = Join-Path $DocsDir 'MASTER_HANDOVER_C11D_CURRENT.md'
$StartPath = Join-Path $DocsDir 'START_PROMPT_C11D_CURRENT.md'
$Utf8NoBom = New-Object -TypeName System.Text.UTF8Encoding -ArgumentList @($false)
$NewLine = [Environment]::NewLine

if(-not (Test-Path -LiteralPath $GuiAdapterPath)){
    throw 'D4.6 GUI adapter is missing.'
}

foreach($Checkpoint in @('d4_2','d4_3','d4_4')){
    $ReceiptPathForCheckpoint = Join-Path $ProjectRoot (Join-Path 'artifacts\tests\c11d_d4' (Join-Path $Checkpoint ($Checkpoint + '_validation_receipt.json')))
    if(-not (Test-Path -LiteralPath $ReceiptPathForCheckpoint)){
        throw "Required predecessor receipt is missing: $ReceiptPathForCheckpoint"
    }
    $Previous = [System.IO.File]::ReadAllText($ReceiptPathForCheckpoint) | ConvertFrom-Json
    if([string]$Previous.result -ne 'PASS' -or [string]$Previous.status -ne 'CLOSED'){
        throw "Required predecessor is not PASS/CLOSED: $Checkpoint"
    }
}

New-Item -ItemType Directory -Force -Path $ArtifactDir | Out-Null

& python.exe $GuiAdapterPath `
    --self-test `
    --evidence $EvidencePath `
    --plan $PlanPath `
    --parity $ParityPath `
    --receipt $ReceiptPath

if($LASTEXITCODE -ne 0){
    throw 'D4.6 GUI adapter self-test failed.'
}

$Receipt = [System.IO.File]::ReadAllText($ReceiptPath) | ConvertFrom-Json
$Plan = [System.IO.File]::ReadAllText($PlanPath) | ConvertFrom-Json
$Parity = [System.IO.File]::ReadAllText($ParityPath) | ConvertFrom-Json

if([string]$Receipt.result -ne 'PASS' -or [string]$Receipt.status -ne 'CLOSED'){
    throw 'D4.6 receipt is not PASS/CLOSED.'
}

foreach($RequiredPass in @(
    'gui_adapter',
    'canonical_normalizer_reused',
    'personalization_resolver_reused',
    'orchestrator_reused',
    'review_pass',
    'production_pass',
    'gui_cli_canonical_request_equal',
    'gui_cli_plan_equal',
    'gui_cli_sha256_equal',
    'personalization_isolation',
    'invalid_request_rejected',
    'invalid_personalization_rejected',
    'forbidden_simulation_control_rejected'
)){
    if(-not [bool]$Receipt.$RequiredPass){
        throw "D4.6 receipt gate failed: $RequiredPass"
    }
}

if([string]$Receipt.runtime_authority -ne 'NONE'){
    throw 'D4.6 runtime authority must remain NONE.'
}
if([bool]$Receipt.renderer_activation -or [bool]$Receipt.production_execution -or [bool]$Receipt.gui_activation){
    throw 'D4.6 activation boundary failed.'
}
if([string]$Plan.mode -ne 'PRODUCTION' -or [string]$Plan.runtime_authority -ne 'NONE'){
    throw 'D4.6 stored plan is invalid.'
}
if([bool]$Plan.renderer_activation -or [bool]$Plan.gui_activation -or [bool]$Plan.orchestrator_execution){
    throw 'D4.6 plan crossed the inactive execution boundary.'
}
if(-not [bool]$Parity.gui_cli_canonical_request_equal -or -not [bool]$Parity.gui_cli_plan_equal -or -not [bool]$Parity.gui_cli_sha256_equal){
    throw 'D4.6 GUI/CLI parity artifact failed.'
}

# Write the contract deterministically; repeated runs overwrite the same file.
$ContractText = @'
# C11-D D4.6 - GUI Adapter Contract

## Status

PASS / CLOSED. Next: D4.7 - GUI/CLI Parity.

## Adapter responsibility

The GUI adapter is a toolkit-independent data API. It maps GUI payload data to the shared Production Request shape and stamps interface provenance as GUI. It does not depend on PySide, Tkinter, Godot Control, Electron, or any other GUI framework.

The canonical flow is:

```text
GUI -> D4.2 normalizer -> D4.3 personalization resolver -> D4.4 orchestrator -> Production Plan
CLI -> D4.2 normalizer -> D4.3 personalization resolver -> D4.4 orchestrator -> Production Plan
```

The GUI and CLI inputs differ only in interface provenance for the parity fixture. D4.2 normalizes that provenance away; canonical requests, plans, and plan hashes then match.

## Ownership

GUI Adapter owns:

- GUI payload to Production Request input mapping;
- GUI interface provenance metadata.

GUI Adapter does not own:

- Challenge validation;
- personalization rules;
- delivery profile rules;
- seed generation or music generation;
- orchestration and plan identity;
- simulation or rendering.

The adapter imports and calls `production_request_normalizer.py`, `personalization_resolver.py`, and `canonical_production_orchestrator.py`. It adds no Production Plan fields. The plan hash comes from the D4.4 orchestrator.

## Output and execution boundary

The API returns `status=PLANNED`, D4.2 request hash, D4.4 plan hash, the canonical plan, and explicit `execution=false` / `renderer=false` values. Both REVIEW and PRODUCTION modes stop at plan creation. No GUI activation, renderer call, simulation call, or physical production occurs; runtime authority is `NONE`.

## Evidence

- Adapter: `tools/c11d/d4/gui_production_adapter.py`
- Runner: `tools/c11d/d4/run_d4_6_gui_adapter.ps1`
- Fixtures: `artifacts/tests/c11d_d4/d4_6/fixtures/`
- Evidence: `artifacts/tests/c11d_d4/d4_6/d4_6_gui_adapter_evidence.json`
- GUI plan: `artifacts/tests/c11d_d4/d4_6/d4_6_gui_plan.json`
- GUI/CLI parity: `artifacts/tests/c11d_d4/d4_6/d4_6_gui_cli_parity.json`
- Receipt: `artifacts/tests/c11d_d4/d4_6/d4_6_validation_receipt.json`

The gate verifies REVIEW and PRODUCTION, GUI/CLI canonical request and plan parity, personalization isolation, D4.2/D4.3 validation ownership, simulation-control rejection, and the no-execution boundary.
'@
[System.IO.File]::WriteAllText($ContractPath,$ContractText + $NewLine,$Utf8NoBom)

# Refresh the authoritative current-state block idempotently.
$CurrentState = @'
## Current state - D4.6

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
NEXT: D4.7 - GUI/CLI Parity.

D4.6 provides a toolkit-independent GUI data adapter into the same D4.2/D4.3/D4.4 pipeline as the CLI. GUI activation, renderer activation, and production execution remain false; runtime authority is NONE.

'@
$MasterText = [System.IO.File]::ReadAllText($MasterPath)
$MasterPattern = '(?s)## Current state[^\r\n]*\r?\n.*?(?=## Strategic objective)'
if([System.Text.RegularExpressions.Regex]::IsMatch($MasterText,$MasterPattern)){
    $MasterText = [System.Text.RegularExpressions.Regex]::Replace($MasterText,$MasterPattern,($CurrentState + $NewLine),1)
} else {
    throw 'Could not locate current state section in MASTER_HANDOVER.'
}
$MasterMarker = '<!-- C11D_D4_6_HANDOFF_V1 -->'
$Handoff = @'
<!-- C11D_D4_6_HANDOFF_V1 -->

## C11-D D4.6 CLOSED / PASS

- Added a toolkit-independent GUI data adapter using the canonical D4.2 normalizer, D4.3 personalization resolver, and D4.4 orchestrator.
- REVIEW and PRODUCTION requests produce plans only; the renderer and physical execution remain inactive.
- GUI and CLI canonical requests, Production Plans, and plan SHA-256 values match for semantically equivalent payloads.
- Personalization changes its hash and plan identity without changing seed or music_seed.
- Invalid requests, invalid personalization, and forbidden simulation controls are rejected by their canonical components.
- Runtime authority remains NONE.
- Contract: `docs/current/d/D4.6_GUI_ADAPTER_CONTRACT.md`.
- Evidence, plan, parity, fixtures, and receipt: `artifacts/tests/c11d_d4/d4_6/`.
- Next active checkpoint: **D4.7 - GUI/CLI Parity**.
'@
if(-not $MasterText.Contains($MasterMarker)){
    $MasterText = $MasterText.TrimEnd() + $NewLine + $NewLine + $Handoff + $NewLine
}
[System.IO.File]::WriteAllText($MasterPath,$MasterText,$Utf8NoBom)

$StartText = [System.IO.File]::ReadAllText($StartPath)
$StartTitle = '# C11-D START PROMPT'
$StartTitleIndex = $StartText.IndexOf($StartTitle,[System.StringComparison]::Ordinal)
$StartReadFirstIndex = $StartText.IndexOf('## Read first',[System.StringComparison]::Ordinal)
if($StartTitleIndex -lt 0 -or $StartReadFirstIndex -lt 0 -or $StartReadFirstIndex -le $StartTitleIndex){
    throw 'Could not locate current state section in START_PROMPT.'
}
$StartCurrent = @'
Continue ChallengeEngineV01_STATELESS from C11-D D4.6 CLOSED / PASS.

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
NEXT = D4.7 - GUI/CLI Parity.

The GUI adapter is data-only and reuses the canonical D4.2/D4.3/D4.4 pipeline. GUI, renderer, and production execution remain inactive; runtime authority is NONE. C11-C 2.19.12 remains frozen and immutable.

'@
$StartPrefix = $StartText.Substring(0,$StartTitleIndex + $StartTitle.Length)
$StartSuffix = $StartText.Substring($StartReadFirstIndex)
$StartText = $StartPrefix + $NewLine + $NewLine + $StartCurrent + $NewLine + $StartSuffix
$StartMarker = '<!-- C11D_D4_6_HANDOFF_V1 -->'
if(-not $StartText.Contains($StartMarker)){
    $StartText = $StartText.TrimEnd() + $NewLine + $NewLine + $Handoff + $NewLine
}
[System.IO.File]::WriteAllText($StartPath,$StartText,$Utf8NoBom)

foreach($Required in @($EvidencePath,$PlanPath,$ParityPath,$ReceiptPath,$ContractPath,$MasterPath,$StartPath)){
    if(-not (Test-Path -LiteralPath $Required)){
        throw "D4.6 output missing: $Required"
    }
}

Write-Host '=================================================='
Write-Host ' C11-D D4.6 - GUI ADAPTER'
Write-Host '=================================================='
Write-Host '[OK] D4.2 PASS/CLOSED verified.'
Write-Host '[OK] D4.3 PASS/CLOSED verified.'
Write-Host '[OK] D4.4 PASS/CLOSED verified.'
Write-Host '[OK] GUI REVIEW request normalized.'
Write-Host '[OK] GUI PRODUCTION request normalized.'
Write-Host '[OK] GUI canonical request generated.'
Write-Host '[OK] GUI Production Plan generated.'
Write-Host '[OK] GUI canonical request == CLI canonical request.'
Write-Host '[OK] GUI Production Plan == CLI Production Plan.'
Write-Host '[OK] GUI SHA-256 == CLI SHA-256.'
Write-Host '[OK] Personalization isolation verified.'
Write-Host '[OK] Invalid request rejected by D4.2.'
Write-Host '[OK] Invalid personalization rejected by D4.3.'
Write-Host '[OK] Simulation controls rejected.'
Write-Host '[OK] Renderer activation = NONE.'
Write-Host '[OK] Production execution = NONE.'
Write-Host '[OK] Runtime authority = NONE.'
Write-Host '[OK] Contract and current handovers updated.'
Write-Host ''
Write-Host '=================================================='
Write-Host ' C11-D D4.6 - PASS / CLOSED'
Write-Host '=================================================='
Write-Host 'NEXT: D4.7 - GUI/CLI Parity'
