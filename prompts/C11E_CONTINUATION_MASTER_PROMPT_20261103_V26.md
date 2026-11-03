# C11-E Continuation Master Prompt — V26

Act as lead implementation engineer for `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. The live Windows checkout is the sole authority; context snapshots are read-only reference and must never be extracted over the checkout.

## Mission

Complete the C11-E successor for Challenge, Visual Loop and Visual Drill using existing C11-C generators/mechanics and family audio implementations. Add D presentation/layout, enabled family-scoped editorial fields, correct family music, FFmpeg mux, FFprobe/audio QA and immutable receipts. Preserve C11-C protected code and its frozen manifest until formal E8 approval.

## Development CLI/GUI clarification — binding

During current engineering, implement and test reusable scripts/service through CLI first where practical, then connect the same script/service to the current low-fidelity Producer GUI. Both CLI and GUI execution paths must remain available and tested. The GUI dispatches already implemented scripts; do not duplicate production logic in callbacks. The later operating-model goal — all human generation through a newly built GUI — occurs only after D/E replaces C. It does not mean all current development/tests must be GUI-first. Keep CLI for automation, CI, compatibility, diagnostics and separate-process tests.

## Accepted current evidence

- E0, E1, E2 bounded CH001 R4 and E3.2 remain accepted.
- E3 V1.3 overlay applied; do not reapply.
- E3 V1.4 Windows suite 31/31 PASS (Python 3.13.14; PySide6 6.11.2).
- E3-GUI-01 PASS: actual current Producer GUI invoked the E3 audio worker via QProcess after preparing E1 intent.
- CH001 R4 audio attach pilot PASS: receipt SHA `910d600e06dcdb2356f9f787fd0c82d45db203e35b471cd5c7cdba10d6ec5aab`; ZIP SHA `b696663c704a623715debab7a978c1b41016151778a74214927c8151763da270`.
- Operator confirmed A and C are expected and have no audio/render defects. B is same-seed A repeat.
- No gameplay rerender or production promotion.

## Immediate task: E3 negative controls V1.5

Apply `C11E_E3_NEGATIVE_CONTROLS_OVERLAY_V1_5.zip` only if every preimage pin matches the active checkout. It modifies only the E3 audio pipeline final-mux validator and adds a new 19-test module and versioned docs. It does not modify the D3 V5 engine, E1 service, C11-C, core/audio, D9 governance, `main.py` or GUI callback.

Run `RUN_C11E_E3_NEGATIVE_CONTROLS_V1_5.ps1` on Windows. It must:

1. Use Python 3.13 and confirm FFmpeg/FFprobe.
2. Compile the changed Python modules.
3. Run the full C11-E discovery suite (`test_c11e*.py`), expected 50 tests (31 accepted + 19 new), because the E3 pipeline source changed.
4. Preserve process exit codes, stdout/stderr, hashes, test transcript and immutable receipt under a fresh Documents evidence root.
5. Keep all media test-only; no gameplay renderer, no rerender, no production media.
6. Stop at first failure and never emit PASS after failure.

On 50/50 PASS, record E3 negative controls PASS and close E3 formally. Then implement E4A Challenge presentation/layout/editorial integration, CLI-first with the same scripts wired into the current Producer GUI. E4A must prove the correct D presentation and editorial values consume the expected fields and that D3 V5 audio is attached via the accepted E3 pipeline. Do not change C11-C mechanics or visual generators.

Then proceed E4B Loop, E4C Drill, E5 cross-family determinism/seed isolation and both execution paths, E6 Smoke18, E7 Matrix101 and E8 independent acceptance. Matrix101 is 54 Challenge + 27 Loop + 20 Drill; CH_008/009 remain held until the 11s/12s duration conflict is resolved. Map every historical C11-C test/review case (including 27 reviews and 9 Challenge cases plus remaining categories) into explicit E evidence; Smoke18 is not full coverage.

## Hard rules

- Refresh live source pins before any later code patch; if any pin differs, stop and reconcile.
- No in-place historical document mutation; add versioned docs for every accepted milestone/iteration.
- No repeat of accepted tests unless source/test pins change. V1.5 changes a source pin; the full 50-test suite is therefore required.
- No ZIP extraction over the active checkout, no Git bookkeeping unless materially required.
- No edits to `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, protected C11-C mechanics/generators, `core/audio`, canonical definitions, C11-C manifest, D4.8/D9.10 governance.
- No sixth suite module, second producer, parallel binder or `c11d-control`.
- `release_authority=NONE`, `baseline_promotion=false`, `freeze_eligible=false` until E8 and separate explicit approval.

## Current authority

C11-C 2.19.12 remains authoritative. Manifest 796,318 bytes / SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
