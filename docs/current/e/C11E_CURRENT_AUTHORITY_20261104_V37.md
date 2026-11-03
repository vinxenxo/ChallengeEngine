# C11-E Current Authority — V37

**Date:** 2026-11-04. Active Windows checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS` remains authoritative. Context ZIPs are evidence only; never extract them over the checkout.

## Accepted and reusable

E0/E1, bounded E2 R4, E3.2, E3 Challenge A/V pilot and 50/50 negative controls remain accepted within scope. E4A source discovery, GUI successor contract, Gate A readiness and explicitly operator-approved Policy V1 remain accepted within their bounded scope. E4A.1 Windows Godot fixture remains accepted only as a neutral-body fixture (23/23 tests, 18 PNG @ 540×960, 12 comparisons; receipt `d90394548ae9dc5ac7b75199c96d423605e9c645dedf0616b8bdfbd1b165ea53`).

## E4A.2 source render evidence and failure

The user supplied `RUN_20261103_235800_fd6fb07c.zip` (4,698,162 bytes, SHA `2430588990a6d82aad68082fab000b71b5218af42f27cce75633b7153e06a53d`, valid CRC). Its C11-C base MP4 SHA is `fdd0598e20ddc6201e54cc2dad7fd3362c2ef80961df44f3ef4676fb97a765de`: H.264 720×1280, `yuvj420p/pc`, 60fps, 900 frames, 15 seconds, silent. It belongs to CHALLENGE_004/seed 314159/REVIEW_720. Operator reports the video is visually OK.

The first E4A.2 runner did **not** pass. Focused tests 25/25 passed, but the runner exited 1 at the incorrect assumption that the raw C11-C MP4 was already 30fps/450/yuv420p. Actual source is 60fps/900 and `yuvj420p/pc`; the manifest declares `pixel_format=yuv420p`, creating a metadata/encoded-stream discrepancy. The runner stopped before PNG extraction. A success marker typed after that exception is invalid. C11-C generation itself completed and the frozen manifest remained unchanged.

## Corrective E4A.2 V2

The new runner leaves original C11-C media untouched and normalizes a test-only derivative to H.264 `yuv420p/tv`, 720×1280, 30fps, 450 frames, 15s, no audio. It probes both original and derivative, records manifest-versus-stream pixel format, and fail-closes on unknown range pairs. It accepts `--reuse-c11c-base-run` pointing only to a prior `RUN_*` directory under the approved E4A test-artifacts root; this copies the existing media/manifests/logs and avoids rerunning Godot.

V2 runner SHA: `5c0e8765bb29b58ddefc1b9593be188227e77725431c3dc959c1ce6866529a9b`. Test SHA: `657f459ce11621a2dde133da5234ea27754c56b3acb5a10c8b37ff952a48d07b`. Preparation: 33/33 focused tests and `py_compile` PASS. Corrected normalization/pixel code replayed successfully against the exact uploaded MP4: 18/18 PNGs, 12/12 comparisons, zero A/B BODY changes, B/C identity.

**Important visual caveat:** review montage shows that the test-only title/subtitle coordinates overlap the existing C11-C hook headline. D1.5 leaves safe area and generic typography unknown. Pixel-region confinement is not visual layout approval. The report therefore marks fixture placements unapproved. Do not guess production coordinates or change protected C11-C content.

## Current disposition

`E4A.2_WINDOWS_CORRECTED_REPLAY_REQUIRED`; E4A remains OPEN. Next: install V2 overlay, run 33/33 tests, run the updated Python runner with `--reuse-c11c-base-run ".\artifacts\tests\c11e\e4a_real_body_pixel_review\RUN_20261103_235800_fd6fb07c"`, then inspect the new complete evidence ZIP and perform operator review. No need to rerender Godot when the original run directory exists.

After E4A.2: E4A.3 must connect the D composition into the actual D-owned Challenge visual consumer and resolve layout/staking from authoritative evidence, not `hook_text`/`cta_main` C aliases. E4A.4 is test-only A/V reuse of accepted E3 D3 V5/mux/FFprobe, then visual review and E4A closeout. Continue E4B Loop, E4C Drill, E5, E6 Smoke18, E7 Matrix101 and E8 historic corpus reconciliation/independent acceptance/freeze/explicit promotion.

## Immutable authority and governance

C11-C 2.19.12 remains sole production baseline. Frozen manifest: 796,318 bytes; SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. Do not mutate C11-C mechanics, generators, RNG, presentation binders/editorial, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, `FrameSnapshot.custom_data`, `core/audio`, D3 V5 or E1 service. No sixth module, parallel binder/producer or production dispatch.

Production D renderer OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`; no freeze or promotion.
