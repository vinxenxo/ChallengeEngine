# C11-E E4A.2 — real C11-C gameplay BODY pixel review V3

**Date:** 2026-11-04  
**Status:** corrected runner prepared; Windows post-render replay pending; E4A remains open.

## Objective

Use one already generated, real CHALLENGE_004 C11-C MP4 to prove that the policy-scoped test overlay changes only HEADER/HOOK or FOOTER/CTA while preserving the actual rasterized gameplay BODY at six named time samples. Do not invoke Godot again for the corrected run: reuse the existing run directory when present.

## Confirmed source run

`RUN_20261103_235800_fd6fb07c.zip`, SHA-256 `2430588990a6d82aad68082fab000b71b5218af42f27cce75633b7153e06a53d`, 4,698,162 bytes, valid ZIP/CRC. The contained base MP4 is 11,535,510 bytes, SHA-256 `fdd0598e20ddc6201e54cc2dad7fd3362c2ef80961df44f3ef4676fb97a765de`; FFprobe reports H.264 720×1280, 60fps, 900 frames, 15 seconds, `yuvj420p` full range (`pc`), no audio. The adjacent manifest reports `REVIEW_720`, 60fps/900 frames and audio off but declares `pixel_format=yuv420p`, which differs from the encoded MP4. Both facts must remain visible in the new receipt.

## V1 execution failure (not a generator failure)

The C11-C producer completed successfully and the operator confirms the rendered video is visually OK. V1's test harness incorrectly expected the direct C11-C MP4 to already be a 30fps/450-frame limited-range `yuv420p` output. It stopped at `yuvj420p; expected yuv420p` before frame extraction. Python focused tests passed 25/25. The later manually printed PASS marker after the thrown exception is invalid and must not be copied into any ledger as PASS.

## V2 technical correction

The original source MP4 is retained byte-for-byte. The corrected runner probes source metadata then creates a separate test-only derivative at `review_delivery/CHALLENGE_004_REVIEW_720_30FPS_TEST_ONLY.mp4` using FFmpeg:

- Full-range `yuvj420p/pc`: `fps=30,scale=in_range=full:out_range=tv,format=yuv420p`.
- Already limited-range `yuv420p/tv`: `fps=30,format=yuv420p` without expanding it as full range.
- Unknown format/range combinations fail closed.

The derivative must probe as H.264, `yuv420p/tv`, 720×1280, 30fps, 450 frames, 15 seconds, and no audio. Six delivery samples remain 0, 89, 90, 300, 390 and 449. The runner then produces 18 PNGs and 12 comparisons.

The `--reuse-c11c-base-run` option accepts only a `RUN_*` directory directly under `artifacts/tests/c11e/e4a_real_body_pixel_review`; it copies the existing MP4/manifest/logs to a new run evidence tree, validates identity and no-audio, and does not relaunch Godot. It preserves a fresh, self-contained evidence ZIP.

## Local replay against the exact uploaded source MP4

The V2 normalization and pixel functions were run in the preparation environment against the exact uploaded MP4 SHA above: normalization probe passed; 18/18 PNGs; 12/12 comparisons. For HOOK samples A→B had 11,488 and 11,518 changed pixels respectively, all in HEADER; GAME and REVEAL first samples had zero changes; CTA samples had 6,647 each, all in FOOTER. No A→B BODY pixel changed. B→C had zero changes at all six samples. This verifies the corrected post-processing logic against the supplied media, not the Windows runner itself.

## Visual geometry is not accepted

The montage shows test-only title/subtitle placeholders can visually overlap the existing C11-C hook headline. D1.5 only establishes the 540×960 region partition (scaled to 720×1280); it explicitly leaves generic safe area and typography unknown. Therefore V2 marks fixture coordinates `TEST_ONLY_REGION_CONFINEMENT; PLACEMENT_UNAPPROVED`. Do not treat the pixel-region proof as production text-layout acceptance. Challenge overlay fields `player_name` and `challenge_label` remain blocked pending canonical geometry.

## Source pins and preparation tests

- Runner: `5c0e8765bb29b58ddefc1b9593be188227e77725431c3dc959c1ce6866529a9b`
- Tests: `657f459ce11621a2dde133da5234ea27754c56b3acb5a10c8b37ff952a48d07b`
- 33/33 focused Python tests PASS; `py_compile` PASS.
- No C11-C source or frozen manifest change; no D9.10 dispatch or D production renderer.

## Required immediate execution

Install `C11E_E4A_REAL_BODY_PIXEL_OVERLAY_V2.zip` using its SHA-256 sidecar, verify replacements against the exact V1 preimages, run the 33-test file, and run:

`python -B .\tools\c11d\d9\c11e_e4a_challenge_real_body_pixel_review.py --reuse-c11c-base-run ".\artifacts\tests\c11e\e4a_real_body_pixel_review\RUN_20261103_235800_fd6fb07c"`

Capture exit code immediately. Do not print any success marker after a failure. Upload the complete new RUN ZIP. E4A.2 acceptance still requires the corrected Windows report/receipt, FFprobe, 18 PNGs/12 comparisons, unchanged BODY hashes, and operator review of the region-only test behavior.
