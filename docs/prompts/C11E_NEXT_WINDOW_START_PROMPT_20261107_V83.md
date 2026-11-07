# Next Window Prompt — C11-E V85 / E4B R1P archive recovery / R1V design

Continue development in the active Windows checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. The active checkout is the only source authority. V84 and prior ZIPs are context/evidence snapshots only: do not unpack them over the checkout, inspect or operate Git, or repeat accepted documentary phases. Preserve PowerShell 5.1 conventions (`Start-Process -Wait -PassThru`, captured stdout/stderr and SHA-256, no PS7-only syntax).

## Current accepted state

- C11-C 2.19.12 remains immutable. Freeze manifest SHA-256: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- E4A D99 GUI parity: `PASS_TEST_ONLY`; fixture already exists at `artifacts/tests/c11d_d9/producer_universal/D99-GUI-37559C528640/`. Do not rerun it.
- E4B static family grammar mapping: live audit `PASS_STATIC_SOURCE_MAPPING`, 5/5 families and 27/27 explicit selectors.
- E4B family matrix and D9.9/D9.10 planning contracts remain accepted TEST_ONLY / STATIC_PLAN_ONLY.
- `GeneradorMaestro.gd` contains the intentional opt-in E4A.6 D-only editorial-envelope postimage. Preserve `KNOWN_E4A6_D_ONLY_POSTIMAGE_POLICY_CONFLICT`; do not restore it, edit the frozen manifest or weaken protected-path candidate policy.

## R1P run already executed — do not rerun

Run ID: `E4B_R1P_20261107_032743_5F75045C`. The report is `PASS_R1P_PARAMETER_PAYLOADS_27_OF_27`; report canonical SHA-256 `9e09940c7a915d1533a2ba0a97765626f5c5d8533c870cda27012d4d90c97b41`; receipt-hash-set SHA-256 `523add74c2607d6b5c85fb5f9b270fa5fbca800d3dd05d05131482b044e1a42d`; parent-bindings SHA-256 `460165c92f3afaebc023a49ab5e0fdb86f7fe4c8133032bb54f6bef67ef0911a`; source-manifest SHA-256 `bb5b101492d18ee6c27a649874ffac75aa5dcb2de44cbdc5718902b4cfc6e441`.

The R1P generation/finalization succeeded: 27 JSON receipts, 27 SHA sidecars, 27 deterministic repeat hashes, five family mappings, canonical D9.9/D9.10 parent bindings, separated gameplay/music seed domains, captured process evidence and 30 source pins. The final runner error was a packaging false-negative: the ZIP contains literal `receipts\\...` entries, while the V1 predicate counts only `receipts/...`. The run's recipes are not missing. The original ZIP and evidence are retained.

## Immediate operator action — recovery only

After installing the add-only archive-recovery overlay, run exactly once from the active checkout root:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\tools\c11d\d9\RECOVER_C11E_E4B_R1P_EXISTING_RUN_V1.ps1" -RunId "E4B_R1P_20261107_032743_5F75045C"
```

This script validates the existing run/report, 27 receipts and sidecars, parent bindings, all 30 source pins against the active checkout, original ZIP member bytes, process receipt and captured stdout/stderr hashes. It creates a new `_RECOVERED.zip`, without overwriting the original, rerunning Godot, regenerating recipes or modifying source. Accept only `PASS_R1P_ARCHIVE_RECOVERED_AND_PAYLOADS_REVALIDATED_27_OF_27`. Retain the recovery report, PowerShell process receipt, ZIP hash and console output.

The separate `RUN_C11E_E4B_R1P_LOOP_PARAMETER_PAYLOADS_V2.ps1` corrects the archive-entry predicate by normalizing `FullName` separators and checking 27 JSON receipts plus 27 sidecars. V1 remains immutable. Do not execute V2 for this already completed run.

## Next engineering work — R1V design only

`C11E_E4B_R1V_ACTUAL_FRAME_INVENTORY_DESIGN_20261107_V1.md` defines a separate actual C11-C frame inventory/decoded-pixel-hash stage. The design records measured frame count, ordered frame index/PTS/time, pixel dimensions/format and per-frame pixel SHA; it links each run to the R1P receipt and D9.9/D9.10 parents. Expected timing descriptors are 20/22/23 sec at 30 FPS (600/660/690 frames), but actual frame count must be measured, not inferred.

Do not execute R1V yet. Actual family launchers, prototypes, frame capture/extraction, FFmpeg, visual pilots, compositor, D3/audio and media remain blocked until independent D4.8 authorization and explicit disposition of the known baseline-policy conflict. After those entry conditions, qualify five predeclared silent selectors (one per family) before considering the remaining 22 selectors. No parallel binder or additional GUI surface.

## Immutable governance locks

Keep `renderer=OFF`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `release_authority=NONE`. Preserve C11-C mechanics/RNG/protected paths, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, independent `request.seed` / `request.music_seed`, and the five GUI surfaces. CH_008/009 remain held; provisional runnable scope remains 99, not 101.

## Response discipline

Perform source inspection in the active checkout only. Do not ask the operator to locate the V80 D99 parity fixture or repeat accepted tests. Do not invent PASS claims: the uploaded V84 ZIP and R1P evidence were independently reviewed, but the recovery tool must produce the final active-checkout recovery receipt. Keep installer behavior minimal, add-only and collision-failing; no elaborate installer regression suite.
