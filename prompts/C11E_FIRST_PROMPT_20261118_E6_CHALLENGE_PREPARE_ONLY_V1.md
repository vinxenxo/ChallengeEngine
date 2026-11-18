# FIRST PROMPT — CONTINUE C11-E E6 CHALLENGE PREPARE_ONLY (2026-11-18)

Continue in the active checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`.

## Authority and workflow

The active checkout is sole source authority. ZIP snapshots are evidence-only. Never extract snapshots over the checkout. `GIT_CHECKS=SKIPPED; COMMITS=OPERATOR_MANAGED; SOURCE_FILE_PINS=ENFORCED`. Do not invoke Git or inspect HEAD/status/branch. Use Windows PowerShell 5.1 and Python 3.13.14. Fail closed, preserve evidence, and do not retry automatically.

C11-C 2.19.12 remains immutable. Frozen manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; D4.8 R1V V2 SHA-256 `0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07` remains BLOCKED. E1 PREPARE_ONLY; renderer OFF; dispatch/media false; release authority NONE.

## Current E6 state

The E6 reuse-requalification receipt `E6SMK18REQUAL_20261118T141200Z_BA5AC046` was operator-verified at SHA-256 `4d63b8caec7a975cc0362ee9d7a5924f5ab8371e8e8e1457e1d60956bf65ce33`: 21/21, 13 reuse candidates, 0 E6 accepted, five fresh Challenge A/V requirements.

The target Smoke18 denominator is 18 top-level groups: six Challenge, six Loop, six Drill. The Challenge plan prepares 18 A/B/C subruns for the six Challenge groups; those subruns must never inflate the top-level count.

## New overlay

`C11E_E6_CHALLENGE_PREPARE_ONLY_ORCHESTRATOR_V1` adds one D9 orchestrator. It must:

- consume selector, definition path/hash, mechanic, gameplay seed, music seed, native timebase and request settings only from the pinned external manifest;
- call `prepare_c11e_production_intent()` and `validate_c11e_production_intent()` from the existing E1 service;
- call `build_envelope()` and `validate_envelope_static()` from the existing E6 plan-only module;
- create six groups × A/B/C = 18 E1 intents and 18 static D envelopes;
- reject unknown/mismatched selector/definition, missing seeds, invalid A/B/C seed relation, timebase mismatch, envelope mismatch, unsafe paths and any execution request;
- add its source pins, receipt and SHA sidecars; preserve all existing evidence.

Do not call the old `run_plan()` or `_challenge_request()` because they embed selector/music fixture values. Do not edit the E1 service, D9.9 resolver, plan-only builder, producer schema, Challenge definitions, GeneradorMaestro.gd, C11-C sources or frozen manifest.

## Install and run

Follow `README_C11E_E6_CHALLENGE_PREPARE_ONLY_ORCHESTRATOR_V1.md` exactly. Verify the ZIP sidecar. Extract into a new empty directory. Run the ADD_ONLY installer first; do not run the runner unless the exact install status is PASS. The installer executes the 40-test suite exactly once before writes. The runner checks the successful installation receipt and stored test result, installed payload hashes, PowerShell AST, Python 3.13.14 and active source pins, then performs one PREPARE_ONLY integration run. It does not rerun tests. Do not use a manually copied or modified payload.

## Expected boundary

The best possible outcome is `PASS_PREPARE_ONLY_18_E1_INTENTS_18_D_ENVELOPES_EXECUTION_HELD`. E6_ACCEPTED remains 0; selector selection remains proposal/not frozen; music seeds 840001/840002 and 104 BPM remain proposal-only; E1 tempo_bpm and duration_seconds stay null. No Godot, FFmpeg, FFprobe, D3, audio, PCM, mux, renderer, dispatch, BatchId or media generation. D4.8 remains BLOCKED and release authority NONE.

After the receipt passes, inspect its complete JSON and sidecars, then plan the next static proof only. Do not infer six-selector Godot runtime or any A/V authorization from a plan-only PASS.


## Build validation note

40/40 static tests passed. An isolated integration fixture built from the nightly snapshot passed 18 E1 intents and 18 static D envelopes with receipt/plan/input-manifest sidecars. A synthetic requalification receipt was used only inside that temporary fixture because the operator's current receipt is not part of the nightly snapshot; it is not included in this package. The active checkout execution must use the real pinned report. Native PowerShell 5.1 AST and live source pins remain mandatory local checks.
