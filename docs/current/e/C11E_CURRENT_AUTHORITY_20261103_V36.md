# C11-E Current Authority — V36

**Date:** 2026-11-03  
**Authority:** the active Windows checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS` remains authoritative. This document supersedes prior C11-E status notes where the E4A.1 runtime state differs.

## 1. Accepted and reusable gates

- E0/E1, bounded E2 R4, E3.2, E3 Challenge audio/mux pilot and E3 50/50 negative controls remain accepted within scope. Do not rerun absent relevant source drift.
- E4A source discovery, read-only GUI contract successor and Gate A assessment remain accepted within their bounded scopes. Do not repeat them.
- Challenge Editorial Presentation Policy V1 was explicitly approved by the operator (`APROBAR POLICY V1`); approval JSON SHA-256 `764629384896a255cf992da89fa427c19f60f9b2e623b81ad17d909674b466b5`.
- E4A.1 Windows pixel fixture is now accepted within its test-fixture scope. Godot 4.7.1 actual Windows run: exit 0; 23/23 Python tests; 18 PNGs 540×960; 12/12 comparisons; report SHA `adefba7fe65400efa30d422e0547499c60b79a400eed8e4d90cf1dc9a5d7597f`; receipt SHA `d90394548ae9dc5ac7b75199c96d423605e9c645dedf0616b8bdfbd1b165ea53`.

## 2. E4A.1 precise scope

The fixture proves title/subtitle pixels only in HEADER/HOOK, CTA only in FOOTER/CTA, zero changes at sampled GAME/REVEAL boundaries and B/C pixel identity for language + unresolved Challenge values. It draws an empty/neutral BODY; the 420 real gameplay snapshots were not rasterized. `gameplay_body_pixel_identity=NOT_TESTED_GAMEPLAY_NOT_RASTERIZED_IN_THIS_EDITORIAL_LAYER_FIXTURE`. This is not full Challenge render or production consumer acceptance.

Evidence ZIP: `RUN_20261103_233430_586c3cf4.zip`, SHA-256 `ecd2b141603e004d00a9d814f9ca670dbca2ea611de4b32d76dcbcd13c70c7c2`.

## 3. Current E4A.2 work item

Prepared an add-only runner and 25 focused tests:
- runner `tools/c11d/d9/c11e_e4a_challenge_real_body_pixel_review.py`, SHA `a852e5f4238f14b30a887f579bad3e4284c420c427dc625667a0ec60190fff1a`;
- tests `tools/c11d/d9/test_c11e_e4a_challenge_real_body_pixel_review.py`, SHA `5e967ec3b8fd87cc9effe079356912e8f6b69f8994a368dc8f1c15cfb95dcb0c`;
- tests 25/25 and Python compilation PASS in preparation environment;
- FFmpeg synthetic integration simulation 18 PNG / 12 comparison PASS, not a real C11-C gameplay result.

The runner calls the existing C11-C Challenge script with CHALLENGE_004/seed 314159/REVIEW_720/NoSound and a fresh `artifacts/tests` root. It requires one H.264 yuv420p 720×1280 30fps 450-frame 15s video with no audio, then makes six exact sampled A/B/C PNG triplets and verifies BODY pixel identity. It uses E1/D9.9 output and approved policy mapping; it is an isolated test consumer, not the D production compositor.

**Current state:** `E4A.2_PREPARED; WINDOWS_REAL_GAMEPLAY_RUN_PENDING`. Do not claim E4A.2 PASS until the actual Windows runner completes and its evidence ZIP is inspected.

## 4. Immediate next action

Apply `C11E_E4A_REAL_BODY_PIXEL_OVERLAY_V1.zip` with its corrected ZIP SHA and run the Python entry point once. It automatically invokes the existing C11-C Challenge producer only under the new test-evidence root. Preserve and upload the resulting `RUN_*` evidence ZIP. If FFmpeg/FFprobe are not on PATH, use `C11E_FFMPEG_EXECUTABLE` and `C11E_FFPROBE_EXECUTABLE` environment paths. No C11-C source or manifest edits are part of the increment.

## 5. Subsequent E4A gates

- E4A.3: connect the D-owned composition payload to the actual D Challenge visual consumer; do not create a parallel binder/producer or use `hook_text`/`cta_main` aliases.
- Resolve `player_name` and `challenge_label` geometry only from canonical D1.5/profile/family evidence; otherwise leave blocked.
- E4A.4: test-only A/V qualification via the previously accepted E3 D3 V5/FFmpeg/FFprobe route; then operator visual review and E4A closure.
- E4B Loop → E4C Drill → E5 determinism/seed isolation/profile leakage/GUI-CLI parity → E6 Smoke18 → E7 Matrix101 (99 provisional; CH_008/009 held for 11s/12s discrepancy) → E8 full historical C11-C corpus review, independent acceptance, freeze and separate promotion.

## 6. Non-negotiable governance

C11-C 2.19.12 remains the sole production authority. Frozen manifest: 796,318 bytes; SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. No changes to C11-C mechanics, RNG, generators, presentation binders, C11-C editorial layer, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, `FrameSnapshot.custom_data`, `core/audio` or D3 V5. No sixth module or parallel binder/producer.

Production D renderer OFF; D9.10 `PREPARE_ONLY`; D4.8 `BLOCKED`; D9.14/D9.16 `BLOCKED`; D9.17 `BLOCKED_NO_GO`; D10 `BLOCKED_FOR_PROMOTION`; `release_authority=NONE`; no freeze or promotion.


## 7. E4A.2 final prepared source pins (2026-11-03 23:38 Europe/Madrid)

- Runner SHA-256: `a852e5f4238f14b30a887f579bad3e4284c420c427dc625667a0ec60190fff1a`.
- 25-test module SHA-256: `5e967ec3b8fd87cc9effe079356912e8f6b69f8994a368dc8f1c15cfb95dcb0c`.
- Final focused tests: 25/25 PASS; `py_compile` PASS.
- Final synthetic FFmpeg exercise: 18/18 720×1280 PNGs, 12/12 comparisons; HEADER and FOOTER-only changes, BODY zero changes, B/C identity. This was generated from `testsrc2`; it is not a real Challenge runtime result.
- E4A.1 ZIP precheck correction: actual package SHA was `a2207a949d03572eb5a33d592874c383c8e1a0427b9e8f3c274dab723207d4f7`; the prior instruction's hash typo did not prevent the operator from applying payloads and completing the Godot runner.

E4A.2 remains `PREPARED / WINDOWS_REAL_GAMEPLAY_RUN_PENDING`. The new runner must be run from the active Windows checkout and its evidence ZIP inspected before the gate can pass.
