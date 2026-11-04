# C11-E E4A.3 — D-owned Godot real-body compositor proof V1

**Date:** 2026-11-04  
**Status:** prepared; Python contracts 46/46 PASS; Windows Godot 4.7.1 execution pending. E4A.3 is OPEN.

## Purpose

Exercise the existing D-owned Challenge source-timebase materializer's explicitly isolated E4A test branch over actual C11-C Challenge frames. The test must use the same E1-prepared A/B/C intents and D semantic composition objects already accepted in E4A.2, not introduce a new editorial binder or policy mapping.

## Inputs

- Accepted E4A.2 `RUN_20261104_002559_542bcf60`.
- Original C11-C silent CHALLENGE_004/seed 314159 base MP4 SHA `fdd0598e20ddc6201e54cc2dad7fd3362c2ef80961df44f3ef4676fb97a765de`.
- E4A.2 normalized review MP4 SHA `edbd446d67142d20e138e55563f16cbae8d9a4c39469fd2bebcb3c9d5723fb9e` (H.264, `yuv420p/tv`, 720×1280, 30fps, 450 frames, 15s, no audio).
- Six delivery stills at frame indexes 0, 89, 90, 300, 390, 449 and corresponding source-time indexes 0, 178, 180, 600, 780, 898. The source Challenge phase ranges remain calculated from the canonical CHALLENGE_004 timeline.
- Existing E1 A/B/C intents preserved by accepted E4A.2 evidence.

## Execution path

1. Verify every source pin, previous E4A.2 receipt/report, source MP4 and normalized MP4.
2. Extract six original delivery stills only with FFmpeg `select`; no drawtext, re-encode, video generation or audio.
3. Invoke the current D-owned `materialize_challenge_visual_payload_in_memory.gd` with an explicit test config. The test branch validates frame paths/hashes, creates transparent 720×1280 Godot `SubViewport` layers, draws only the approved policy's HEADER/HOOK and FOOTER/CTA semantic fields with test-only placeholder typography, and alpha-composites each layer over the corresponding real background frame.
4. Produce A/B/C × six stills (18 PNGs). Verify A equals its original background pixel-for-pixel (RGB); A→B changes only HEADER for HOOK and FOOTER for CTA; GAME/REVEAL stay identical; B/C remain pixel-identical; BODY crop hashes match across A/B/C at all six samples.
5. Python independently validates Godot PNG hashes and pixel invariants. Receipt captures Godot version/command/stdout/stderr, FFmpeg frame extraction commands, all source pins and before/after hashes of original/normalized MP4 and six base frames.

## D materializer source change

The materializer remains D-owned and its default path remains source-timebase/in-memory review only. The new explicit E4A config mode is test-only and restricted to `artifacts/tests/c11e/e4a_d_compositor_pixel_review/`. It does not produce production renderer input or dispatch D9.10. The frame invariance fingerprint now uses only explicit visual snapshot fields (`position`, `rotation`, `scale`, `opacity`, `texture_index`, `variant_id`) and never reads or serializes `FrameSnapshot.custom_data`. No C11-C source, binder, generator or manifest is modified.

## Test/acceptance boundaries

- Python preparation suite: 46/46 PASS; `py_compile` PASS.
- Godot runtime not yet run in this preparation environment. Windows 4.7.1 Mono invocation is required.
- Expected test output: 18 PNGs / 12 comparisons, six base-frame records, independent BODY identity, source hashes unchanged.
- This is a six-sample test of the existing D-owned materializer's explicit Godot layer branch. It is not a full-duration D compositor, final MP4, A/V acceptance, production dispatch, Producer GUI integration, or release acceptance.
- `VISUAL_PLACEMENT=UNAPPROVED_D1_5_SAFE_AREA_TYPOGRAPHY_UNKNOWN`; title/subtitle placeholders can overlap C11-C HOOK content. `player_name`/`challenge_label` remain blocked geometry; language metadata only.

## Exact pins

- Materializer V3: `e925cc319852e9fe79c26f9dd791ff1f43a0d3465ae30159819be5f57fb001e1`.
- Python runner: `9d00faf38213ade848f722a72bf0ba6ef102975f43bd9e960648780bf3d2c629`.
- Python tests: `b33a158ddd29f1581f86a7d6ceabef4a66a1a5a8a51aaada9b8489c730876973`.
- Frozen C11-C manifest: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

## Next

Apply the V1 overlay and run 46 tests, then execute `c11e_e4a_d_compositor_real_body_pixel_review.py --base-run "artifacts/tests/c11e/e4a_real_body_pixel_review/RUN_20261104_002559_542bcf60"`. Do not rerun C11-C or Godot capture. Upload the complete E4A.3 `RUN_*` ZIP for verification. E4A remains open pending E4A.3 runtime, E4A.4 A/V, visual layout and operator review.
