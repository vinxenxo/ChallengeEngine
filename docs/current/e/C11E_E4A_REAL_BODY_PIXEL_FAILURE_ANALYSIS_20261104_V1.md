# C11-E E4A.2 real-body pixel runner — failure analysis V1

**Date:** 2026-11-04  
**Disposition:** `HARNESS_CONTRACT_MISMATCH_IDENTIFIED_AND_REMEDIATION_PREPARED`

## 1. Operator execution

The Windows overlay installed all 11 files. The frozen C11-C manifest remained unchanged. Focused tests passed 25/25. The existing C11-C runner completed and wrote one `CHALLENGE_004` MP4 under the isolated `artifacts/tests` path. The subsequent E4A.2 Python runner exited **1** before extracting any PNG because it incorrectly applied the 30fps/450-frame/yuv420p delivery assertion directly to the unnormalized C11-C output.

The console later displayed `C11E_E4A_REAL_BODY_PIXEL_OVERLAY_AND_WINDOWS_TEST=PASS`, but this was printed after `$RunExit` had been checked and thrown. It is not a valid result and is explicitly rejected as acceptance evidence. The actual runner terminal marker was `C11E_E4A_REAL_BODY_PIXEL_REVIEW=FAIL`; exit code 1.

## 2. Exact uploaded evidence

Evidence ZIP: `RUN_20261103_235800_fd6fb07c.zip`  
ZIP size: 4,698,162 bytes  
ZIP SHA-256: `2430588990a6d82aad68082fab000b71b5218af42f27cce75633b7153e06a53d`  
ZIP CRC: valid (`testzip=None`); 16 entries.

The preserved C11-C base MP4:

- Path in run: `c11c_base_render/CHALLENGE_004/CHALLENGE_004_seed_314159.mp4`
- Size: 11,535,510 bytes
- SHA-256: `fdd0598e20ddc6201e54cc2dad7fd3362c2ef80961df44f3ef4676fb97a765de`
- FFprobe: H.264, 720×1280, `yuvj420p`, color range `pc` (full), 60/1 fps, 900 frames, 15.000 seconds, exactly one video stream and no audio.
- C11-C `production_manifest.json`: `delivery_profile=REVIEW_720`, `fps=60`, `frames=900`, `audio_present=false`, but `pixel_format=yuv420p`. Thus the manifest pixel-format field disagrees with the encoded stream (`yuvj420p`). This is recorded as source-output metadata evidence; no C11-C code or manifest is changed.

The C11-C generator stdout contains its PASS line and its PowerShell process necessarily returned zero: the Python runner would have stopped before FFprobe otherwise. Godot output and video file are present; the operator reports that the generated video is visually OK.

## 3. Root cause

E4A.2 V1 assumed that the direct C11-C `REVIEW_720` MP4 was already normalized to the downstream 30fps/450-frame/limited-range `yuv420p` review target. The real current C11-C path emits 60fps/900 frames and, in this run, full-range `yuvj420p`. The failure therefore occurred in the **test harness contract**, not in Godot generation, challenge mechanics or the frozen C11-C producer.

## 4. Remediation

V2 preserves the original C11-C MP4 and derives a separate test-only review copy:

`fps=30,scale=in_range=full:out_range=tv,format=yuv420p`

FFmpeg encodes that derivative as H.264 `yuv420p/tv`, 720×1280, 30fps, 450 frames, 15 seconds, without audio. FFprobe records both the original source and the normalized derivative. A limited-range `yuv420p` source uses a distinct no-range-expansion path; unknown source range pairs fail closed.

The runner also supports `--reuse-c11c-base-run`, restricted to an existing `RUN_*` directory directly under the approved E4A `artifacts/tests` root. It copies the already-generated base video, its adjacent manifest and source logs into a new evidence package, validates CHALLENGE_004/seed 314159/REVIEW_720/audio-off, and **does not rerun Godot or C11-C**.

## 5. Exact-MP4 replay result (preparation only)

The corrected normalization and pixel-comparison functions were exercised against the exact MP4 bytes from the uploaded ZIP in the preparation environment. This is not yet the corrected Windows runner acceptance:

- Normalized derivative FFprobe: H.264, `yuv420p`, range `tv`, 720×1280, 30fps, 450 frames, 15 seconds, no audio.
- PNGs: 18/18.
- Pixel comparisons: 12/12.
- Hook first/last: 11,488 / 11,518 A→B changed pixels; every changed pixel was inside HEADER; zero outside and zero BODY changes.
- GAME first and REVEAL first: zero A→B changes.
- CTA first/last: 6,647 / 6,647 A→B changed pixels; every changed pixel was inside FOOTER; zero outside and zero BODY changes.
- B→C: zero pixel differences at all six samples.
- BODY crop identity: unchanged across A/B at every sampled point.

## 6. Visual-layout limitation discovered

The 18-image montage reveals that the test-only title/subtitle placeholder text can overlap the existing C11-C hook headline in HEADER/HOOK. The pixel test only proves region confinement and BODY invariance; it does **not** validate final text placement, safe area, hierarchy, typography or compositor stacking.

D1.5 explicitly leaves generic safe-area insets, padding/margins and generic typography constraints UNKNOWN. The fixture coordinates are placeholders and are not approved production coordinates. Do not move them to guessed positions or claim visual-layout acceptance. E4A.3 must resolve the D-owned composition/layout against authoritative profile/family evidence and keep C11-C read-only.

## 7. Corrected source identity

- Runner SHA-256: `5c0e8765bb29b58ddefc1b9593be188227e77725431c3dc959c1ce6866529a9b`
- Focused tests SHA-256: `657f459ce11621a2dde133da5234ea27754c56b3acb5a10c8b37ff952a48d07b`
- Focused tests: 33/33 PASS in preparation environment.
- `py_compile`: PASS.

## 8. Gate decision and next step

E4A.2 remains **OPEN / WINDOWS CORRECTED RUN REQUIRED**. Do not rerender C11-C if the original run folder still exists. Apply the V2 hash-gated overlay, run 33 tests, then execute the corrected runner with `--reuse-c11c-base-run` pointing to `RUN_20261103_235800_fd6fb07c`. Inspect its new ZIP, report, source and normalized video FFprobe, PNGs, BODY hashes and SHA256SUMS. Then perform operator visual review of region-only behavior; the placeholder overlap itself remains an explicit non-acceptance for production layout.

C11-C 2.19.12 stays the only production authority. D4.8 `BLOCKED`; D9.10 `PREPARE_ONLY`; D9.14/D9.16 `BLOCKED`; D9.17 `BLOCKED_NO_GO`; D10 `BLOCKED_FOR_PROMOTION`; `release_authority=NONE`. No production renderer, dispatch, media or promotion is authorized.
