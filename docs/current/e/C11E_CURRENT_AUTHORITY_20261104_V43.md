# C11-E Current Authority — V43

**Date:** 2026-11-04  
**Checkout authority:** `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`  
**Immediate action:** verify the already-created E4A.4 worker ZIP using the self-contained V3 recovery script. No D3/audio/mux rerun.  
**Production baseline:** C11-C 2.19.12 remains the only production authority.

## 1. Product objective and protected boundary

Deliver one C11-E production path for Challenge, Visual Loop and Visual Drill. Preserve C11-C generators/mechanics and existing family audio implementations. Add D-owned presentation/editorial, family-correct music, independent gameplay/music seeds, FFmpeg mux, FFprobe/audio QA, immutable receipts and GUI/CLI parity through the existing E1 service. No second producer, parallel binder, sixth suite module or `c11d-control`.

Frozen manifest: **796,318 bytes**, SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. Do not edit protected C11-C generation/mechanics/RNG, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, `FrameSnapshot.custom_data`, `core/audio`, D3 V5, E1 or the frozen manifest. Governance stays locked: renderer OFF, D4.8 BLOCKED, D9.10 PREPARE_ONLY, D9.14/D9.16 BLOCKED, D9.17 BLOCKED_NO_GO, D10 BLOCKED_FOR_PROMOTION, `release_authority=NONE`.

## 2. Accepted evidence retained

- E4A.2: real C11-C BODY reference, normalized CHALLENGE_004, 720x1280, 30 FPS, 450 frames/15s; accepted receipt/report and ZIP hashes remain in V40/V42.
- E4A.3 V2: render-enabled Godot 4.7.1, 6/6 real frames, 18/18 PNGs, 12/12 comparisons, BODY identity preserved; receipt `3670428feae3b34766677b4cdba3985babecbda9ee781eebe4cc57c318cd9f1c`.
- E4A.3 visual disposition: operator confirms countdown-on hook/editorial composition is intentional for that selected video configuration. It is not a failed render. Future GUI must expose a visibility option through E1. The layout test obligation is broader than a single all-fields-visible sample; see `C11E_E4A_PRESENTATION_CONFIGURATION_COVERAGE_PLAN_20261104_V1.md`.
- E4A.4 focused tests: 42/42 PASS. Worker exit 0 and `C11E_E4A4_CHALLENGE_AUDIO_MUX=PASS_ISOLATED_TEST_ONLY`.

## 3. E4A.4 worker evidence — wrapper recovery pending

Worker run ID (receipt/report identity): `20261104T013653Z-8469583E`. Its evidence folder and ZIP use the filesystem/archive name `RUN_20261104T013653Z-8469583E`; the `RUN_` prefix is not part of the JSON `run_id`.

- Inner receipt SHA-256: `8d351c513b6972d4f583dfe6678ab46e0441ab0466315a03abf1ce1179c115ca`.
- Worker ZIP SHA-256: `ccdef6038be84bb4216f6777592a7adf6ba0ec084887f536088df6bbe952d01f`.
- Worker ZIP: `artifacts/tests/c11e/e4a_audio_mux_review/RUN_20261104T013653Z-8469583E.zip`.
- Wrapper log ZIP SHA-256: `ce348246172f61839e4bed961aa5f3140806e8820abb633f592008c222371da5`.

The audiovisual worker completed successfully. The first apply wrapper then failed at line 185 while constructing an `[ordered]` summary. Recovery V1 failed before its body because of a parameter-default path expression. Recovery V2 ran but had an incorrect identity comparison: it compared receipt `run_id` (`20261104T013653Z-8469583E`) to the folder name (`RUN_20261104T013653Z-8469583E`). Correct relation is `folder_name = 'RUN_' + receipt.run_id`; archive entries are prefixed by the folder name. This mismatch is a recovery-validator defect, not evidence of a media failure.

The new V3 recovery utility is one self-contained `.ps1`: no companion overlay ZIP and no nested extraction structure. It corrects the identity relation, verifies the existing worker ZIP/sidecar/inner receipt/report/SHA256SUMS/media inventory and applies only new versioned documentation. It does not run D3 V5, D3.3, FFmpeg, FFprobe, Godot or any gameplay renderer.

E4A.4 remains `WORKER_PASS_PENDING_INDEPENDENT_ARCHIVE_VERIFICATION_AND_OPERATOR_REVIEW` until the V3 verifier succeeds, the worker ZIP is uploaded for independent inspection, and the operator confirms audible quality and A/V sync.

## 4. Presentation/layout interpretation and test strategy

The E4A.3 countdown-on composition is an intentionally selected configuration. Do not classify the coincidence of countdown hook and editorial as a universal defect. Conversely, do not generalize that one composition as the only valid layout or infer every editorial field must always be visible.

The C11-D presentation/editorial layer is configurable. Challenge runs have historically used different presentation arrangements. The verification plan must therefore test **grounded configuration cases**, not one hard-coded “print every field” case:

1. recover the actual per-Challenge presentation and editorial switches/values from the historical Challenge definitions, binders, profiles, test cases and run receipts;
2. distinguish countdown/hook visibility and phase behavior from D editorial field presence;
3. cover representative enabled/disabled combinations for the policy-authorized fields `title`, `subtitle`, `call_to_action`, plus omission of empty values;
4. exercise the operator-confirmed countdown-on case and countdown-off case, and other historical arrangements supported by evidence;
5. verify each state at the correct phase and region, including no unintended changes to body pixels, timing or source video;
6. do not invent an exhaustive Cartesian product where historical contracts do not define it.

Existing D1.1 maps CHALLENGE_001..009 but marks timing and geometry UNKNOWN; D1.5 establishes the logical 540x960 Header/Body/Footer regions while generic safe-area, CTA geometry and typography remain UNKNOWN; D1.7 establishes nine declarative mappings without Challenge layout overrides. The historical C binder demonstrates phase-scoped `show_hook`/countdown and CTA visibility, but remains protected reference evidence, not an implementation target. Challenge-specific `player_name` and `challenge_label` remain geometry-blocked; `language` is metadata-only. Preserve approved policy V1 mappings.

Future GUI controls must be request-level values handled by the same E1 service; never implement presentation business logic only in the GUI.

## 5. Ordered next work

1. Run the standalone V3 recovery script. It must match `RUN_` + `receipt.run_id` and verify the existing archive without replaying work.
2. Upload the original worker ZIP and independently inspect A/B/C MP4s, raw/master WAVs, stream metadata, hashes, timing and receipts; complete operator listening and sync review.
3. Continue E4A with evidence-grounded presentation configuration coverage and the E1 countdown visibility option; prove representative variants, not only all-fields-visible.
4. Complete Challenge D presentation/editorial + D3 V5 audio A/V integration using the existing worker/pipeline contract.
5. E4B Loop; E4C Drill; E5 determinism/seed isolation/non-leakage/GUI-CLI parity; E6 Smoke18; E7 Matrix101; E8 historical C11-C row map, independent acceptance, freeze and explicit promotion.

Matrix101 remains 54 Challenge + 27 Loop + 20 Drill; CH_008/009 remain held while declared 11s conflicts with 12s phase sum (3+7+0+2), so 99 provisional runnable. No accepted gate is repeated without relevant source/test changes.
