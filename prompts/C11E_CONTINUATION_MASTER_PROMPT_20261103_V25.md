# C11-E Continuation Master Prompt — V25

Act as the lead implementation engineer for `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. Continue the live project from the user's active Windows checkout and the latest attached `C11E_WORKING_CONTEXT_*.zip`. The checkout is authority; the snapshot is filtered context only and must never be extracted over the checkout.

## Mission — do not lose the full product objective

Deliver the C11-E successor production workflow for **Challenge, Visual Loop and Visual Drill**. The result must use the existing C11-C generators/mechanics, D presentation/layout and the correct enabled family-scoped editorial values, attach the correct family music, mux with FFmpeg, validate with FFprobe and write an immutable run receipt. Normal operator production is GUI-only through the existing Producer GUI. The CLI is retained only as a separate-process automated compatibility adapter over the same E1 shared service. No parallel producer, no sixth suite module, no `c11d-control`.

## Current state — 2026-11-03

- E0 and E1 accepted; the E1 shared service remains common to GUI/CLI. Real GUI operator observation is still pending.
- E2 R4 formally closes the bounded CH001 title-to-pixels A/B control only. It does not prove all Challenges, Loop, Drill, audio or GUI runtime.
- E3.2 D3 V5 contract binding to E1 intent is accepted/committed.
- E3 V1.3 audio pipeline overlay is installed in Windows: 10/10 postimages verified; `main.py` replacement plus 9 added payloads. Patch ZIP SHA `69ae53e1ee1edbf7db015b3e311f0826e0d94f4195b5153ed8820d69af0030c1`.
- The separate V1.4 Windows test runner passed Python compile, 31/31 `test_c11e*.py` tests and PySide6 import 6.11.2. Receipt SHA `84fc86c96ca237c7dd16837666882e80afe6dda8292a04527d19fcbd3579e30b`. Temporary FFmpeg mux integration was exercised. No production audio, renderer, gameplay rerender or GUI launch.
- Do not repeat E0/E1/E2/E3.2, V1.3 patch installation or V1.4 31-test suite unless their code/test pins change.

## Immediate next action

Execute **E3-GUI-01**: inspect the actual GUI launch path in the active Producer code, launch the existing Windows Producer GUI, observe the E3 control in the existing universal editorial surface, and run one controlled CH001 audio attach pilot from the GUI against the immutable R4 video using a fresh test-only output directory. Confirm E1 shared-service invocation, GUI progress/log/error/result visibility and evidence. Do not rerender gameplay. Do not invent a launch command; read it from the active checkout.

For the first Challenge pilot: profile `challenge_8bit_v1`; gameplay seed `193847` as R4 provenance; music seed `840001` (changed-seed control `840002`); `variation_index=0`; `tempo_bpm=104` only as the historical D9.2 pilot fixture, not a global default; duration derived from FFprobe-verified R4 source (270 frames / 30 fps = 9s), never the V5 4s fallback.

Preserve raw WAV. Follow active D3.3's 30s measurement/loudnorm precedent (`I=-14`, `TP=-1`, `LRA=7`, 48 kHz stereo PCM); trim deterministically to 9s for final A/V. No invented fades, ducking or defaults. Mux video by stream copy; refresh D9.2 source pins before relying on AAC 192 kb/s/48 kHz/stereo, `-shortest`, `+faststart`, 0.15s tolerance. FFprobe exactly one video/one audio stream, non-silent audio, correct profile/sample rate/layout/timing, no truncated audio and frame-identical video. Same seed repeats the same PCM; changed music seed changes audio only. Collect all commands, versions, logs, exit codes, hashes, ffprobe JSON and structured receipt. CLI parity is automated only.

## Documentation to read first

1. `docs/current/e/C11E_CURRENT_AUTHORITY_20261103_V25.md`
2. `docs/current/e/C11E_GATES_ACCEPTANCE_MATRIX_20261103_V25.md`
3. `docs/current/e/C11E_E3_EXECUTION_BACKLOG_20261103_V2.md`
4. `docs/current/e/C11E_E3_AUDIO_PILOT_TEST_20261103_V1.md`
5. `docs/current/e/C11E_E3_WINDOWS_TEST_ACCEPTANCE_20261103_V1.md`
5. `docs/current/e/C11E_EXECUTION_HYGIENE_AND_ASSISTANT_ERROR_LOG_20261103_V21.md`
6. `docs/current/e/C11E_GUI_PRIMARY_WORKFLOW_AND_CLI_COMPATIBILITY_20261103_V1.md`
7. `docs/history/c11e/C11E_E3_2_FORMAL_CLOSURE_AND_DECISION_RECORD_20261103_V1.md`
8. `docs/history/c11e/C11E_ARCHITECTURE_DECISION_RECORD_AND_BACKLOG_20261103_V1.md`
9. `docs/history/c11e/C11E_E3_CHALLENGE_AUDIOVISUAL_IMPLEMENTATION_PLAN_20261103_V1.md`
10. `docs/history/c11d/C11D_TO_C11E_FULL_FAMILY_ROADMAP_20261103_V15.md`
11. `docs/current/e/C11E_CONTEXT_SNAPSHOT_OPERATOR_GUIDE_20261103_V1.md`

Also read live `AGENTS.md` and `.continue/rules/CONTINUE.md`, but do not edit them merely to reconcile wording. The latest active source wins over old docs/snapshot.

## Operating rules

- Keep patch application, tests, GUI launch and docs separate. Do not bundle them into another installer.
- No more installer churn: V1.3 patch PASS and V1.4 test PASS are accepted.
- Do not take over Git operations or ask the operator to repeat Git status/commit checks unless source pinning is materially required before a code edit. The operator controls local commits.
- Before the next code modification, refresh exact live hashes for changed E3 service/engine/contract, D3 spec/profile/source, D3.2/D3.3 and D9.2 runner/validator, and the GUI entry/callback. Do not assume the old E3.2 HEAD is still current.
- The test suite's 31/31 PASS and PySide6 import do not equal a manual GUI runtime PASS.
- On failure stop at the first failed stage. Preserve stdout/stderr, native exit code, SHA-256, exact output, and test-only media. Never print PASS markers after failure.
- Do not rerun gameplay to test a music-seed change.
- Do not touch `core/audio`, protected C11-C generators/mechanics, frozen C11-C manifest, canonical definitions, D4.8/D9.10 locks, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector` or `RenderedFrameStream`.
- No production release, freeze, promotion or expanded authority. `release_authority=NONE`.

## Full roadmap

E3 Challenge audio pilot and QA -> E4A Challenge presentation/editorial -> E4B Visual Loop -> E4C Visual Drill -> E5 cross-family determinism/seed isolation/GUI-primary + CLI parity -> E6 Smoke18 (6 per family) -> E7 Matrix101 (54+27+20; CH_008/009 held due 11s/12s conflict, 99 provisional runnable) -> E8 independent acceptance/freeze/explicit promotion.

C11-C 2.19.12 remains the sole production baseline until E8.
