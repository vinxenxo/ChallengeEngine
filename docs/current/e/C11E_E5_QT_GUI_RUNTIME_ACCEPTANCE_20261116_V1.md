# C11-E E5 Visible Qt Producer Runtime Acceptance — V1

**Date:** 2026-11-16  
**Status:** `PENDING_OPERATOR_VISIBLE_QT_SESSION`  
**Purpose:** Complete the only remaining E5 evidence item after the three-family representative A/V review was accepted.

## 1. Scope and safety boundary

Exercise the existing Producer window from the active checkout and the existing `RESOLVER + PLAN EDITORIAL / PUENTE (SIN RENDER)` action for the three E5 representatives. This is an operator-visible Qt runtime/session check, not an automated offscreen test and not a renderer qualification.

The only permitted action is the existing plan-only resolver button. It calls the current GUI path through `prepare_c11e_production_intent(..., request_origin="GUI")`, invokes the corresponding CLI preparation, compares semantic intent and D9 bridge parity, and writes immutable request/plan/lifecycle receipts.

Do not click or invoke:

- `C11-E E4B · VALIDAR 5 FAMILIAS / 27 GRAMÁTICAS · PLAN ONLY` (E4B already accepted).
- `D9.14 REAL-MEDIA CERTIFICATION PREFLIGHT · NO MEDIA`.
- `C11-E E3 · AUDIO + MUX PILOT CHALLENGE_001 / R4`.
- `C11-E E4C · EJECUTAR DRILL A/V CUALIFICACIÓN`.
- Any render, export, production or media action.

No source patch, renderer input, Godot, FFmpeg, media generation, production dispatch, output under `artifacts/production/c11e`, BatchId or release operation is part of this test.

## 2. Start the existing visible application

Use the active Windows checkout only:

`C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`

Start the existing Producer with:

`c11c-suite\c11c-producer\run.bat`

Do not use `QT_QPA_PLATFORM=offscreen`; the operator must see the real window. Open the existing tab `C11-D · EDITORIAL UNIVERSAL (D9.9)` (or the current UI label corresponding to that existing surface). Do not start a second Producer or add a new tab/module.

Before the first click, optionally note a timestamp in PowerShell for later evidence packaging:

```powershell
$E5QtSessionStartUtc = [DateTime]::UtcNow
```

## 3. Three representative requests

Use one visible window and execute the following three cases sequentially. After each one, wait for the status bar to report `D9.13 LIFECYCLE PASS` and `C11-E E1 SERVICE PASS`; verify that the E1 and GUI↔CLI tabs show PASS before changing the selector.

| Case | Content type | Family | Variant / subtype | Mode | Gameplay seed | Music seed |
|---|---|---|---|---|---:|---:|
| Challenge | `Challenge` | `parking_v2` | `CHALLENGE_004` | `REVIEW · PLAN` | 314159 | 840001 |
| Visual Loop | `Visual Loop` | `c11c_fractal_bloom_v1` | `radial_bloom` | `PRODUCTION · PLAN ONLY` | 100006 | 500006 |
| Visual Drill | `Visual Drill` | `tracking` | `tier-2` | `PRODUCTION · PLAN ONLY` | 12345 | 840001 |

For all three cases:

- Delivery profile: `REVIEW_720`.
- Presentation profile: `social_default_v1`.
- Variation index: `0`.
- Audio enabled: ON.
- `Activar datos editoriales en este plan`: ON.
- Scope: retain the current/default scope; do not introduce optional per-field controls.
- Leave title, subtitle and CTA blank; for Challenge also leave player name and challenge label blank. Retain the current language value (`es` in the reviewed source).
- Do not add `presentation_options` or a Hook/countdown checkbox; Challenge's E1 default remains internal.
- Click only `RESOLVER + PLAN EDITORIAL / PUENTE (SIN RENDER)`.

The request values above are the existing E5 canary baselines. The Loop/Drill mode is a plan-only mode; `D4.8` remains BLOCKED.

## 4. Required evidence per visible GUI execution

The existing GUI handler creates one unique directory per click under:

`artifacts/tests/c11d_d9/producer_universal/D99-GUI-<ID>/`

Each of the three directories must contain at least:

- `request.json`
- `canonical_request.json`
- `editorial_resolution.json`
- `universal_plan.json`
- `editorial_render_bridge_plan.json`
- `d_render_adapter_envelope.json`
- `d4_subplan_evidence.json`
- `gui_cli_parity.json`
- `c11e_production_intent.json`
- `c11e_gui_cli_parity.json`
- `c11e_production_intent_receipt.json`
- `producer_universal_receipt.json`
- `cross_suite_lifecycle_receipt.json`

Loop must also contain `loop_family_stage_contract.json`. Drill must also contain `drill_family_stage_contract.json` and `drill_dynamic_request_binding_preview.json`.

Acceptance for every case:

- `c11e_gui_cli_parity.json.status == "PASS"` and all entries in `checks` are true.
- `c11e_production_intent_receipt.json.status == "PASS_E1_PREPARATION_ONLY"` and `gui_cli_parity == "PASS"`.
- `gui_cli_parity.json.status == "PASS"` and all entries in `checks` are true; nested `e1_shared_service.status == "PASS"`.
- `producer_universal_receipt.json.result == "PASS_BRIDGE_PLANNING_ONLY"` and `gui_cli_parity == "PASS"`.
- Request content type, family, variant/subtype, mode and seeds match the matrix above.
- The E1 intent records GUI origin, and CLI parity records both origins.
- Family-specific Loop/Drill stage contract is present and validates for the selected family.
- `renderer_input_emitted=false`; `renderer_dispatch_invoked=false`; `renderer=false`; `production_execution=false`; `media_created=false`; `release_authority=NONE`.
- `family_adapter.status == "NOT_CONNECTED_E1"`; preserve this fail-closed boundary.
- Lifecycle validation passes and source pins are current.

The GUI may display the existing D9.9/D9.10/D9.13 labels. The key C11-E confirmation is that the E1 service status is PASS for the GUI-origin request, the CLI semantic parity is PASS, and all execution boundaries remain false.

## 5. Evidence packaging after the three cases

Package only the three new `D99-GUI-*` run directories created during this session. Do not include the repository, production media, E4 folders, or unrelated historic D99 runs. Preserve the original run directory names and all files within each directory.

Suggested PowerShell collection after the three cases:

```powershell
$ProjectRoot = 'C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS'
$EvidenceRoot = Join-Path $ProjectRoot 'artifacts\tests\c11d_d9\producer_universal'
$Out = Join-Path $env:USERPROFILE ('Downloads\C11E_E5_QT_GUI_RUNTIME_EVIDENCE_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.zip')

if (-not (Test-Path -LiteralPath $EvidenceRoot -PathType Container)) { throw 'GUI evidence root missing.' }
$Runs = @(Get-ChildItem -LiteralPath $EvidenceRoot -Directory | Where-Object {
    $_.Name -like 'D99-GUI-*' -and $_.CreationTimeUtc -ge $E5QtSessionStartUtc
} | Sort-Object CreationTimeUtc)
if ($Runs.Count -ne 3) { throw "Expected exactly 3 new GUI runs; found $($Runs.Count). Do not package unrelated folders." }
Compress-Archive -Path $Runs.FullName -DestinationPath $Out -CompressionLevel Optimal
$ZipSha = (Get-FileHash -LiteralPath $Out -Algorithm SHA256).Hash
$ZipSha | Set-Content -LiteralPath ($Out + '.sha256') -Encoding ASCII
Write-Host "E5_QT_GUI_EVIDENCE_ZIP=$Out"
Write-Host "E5_QT_GUI_EVIDENCE_SHA256=$ZipSha"
Write-Host "E5_QT_GUI_EVIDENCE_SHA256_SIDECAR=$($Out).sha256"
Write-Host 'E5_QT_GUI_RUNS=3/3'
```

If the timestamp variable was not set before the session, do not use the script above as written; select the three exact new folder names manually and package only those. If any case fails, stop, preserve all three (including partial) folders and console output, and do not retry by reusing an existing request directory.

## 6. Exit decision

A verified PASS for all three visible Qt cases closes the remaining E5 GUI-runtime acceptance item in the declared TEST_ONLY scope. Combined with the E5 PREPARE_ONLY canary, test-only A/V evidence and operator A/V approval, the project can then issue an E5 full-phase closeout and proceed to E6 Smoke18 planning/execution.

`NOT_CONNECTED_E1` remains a deliberate no-dispatch boundary. Do not connect family adapters, turn on renderer input, change D4.8, dispatch media or infer release authority as part of this GUI test. E6 remains HELD until E5 closeout is formally published.
