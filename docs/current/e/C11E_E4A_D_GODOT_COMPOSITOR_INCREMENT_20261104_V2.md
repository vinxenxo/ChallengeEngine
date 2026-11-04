# C11-E E4A.3 — D-owned Godot compositor execution correction V2

**Date:** 2026-11-04  
**Status:** PREPARATION PASS / WINDOWS GODOT RUNTIME OPEN  
**Frozen C11-C manifest:** `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`

## V1 execution finding

The operator applied overlay V1. The 46/46 focused Python contract tests passed. The runner then invoked Godot using `--headless`; its GDScript branch waits for `RenderingServer.frame_post_draw` while obtaining SubViewport textures. Godot's own documentation says `--headless` disables all rendering and window management and that RenderingServer calls return dummy values. This is the diagnosed hang mechanism, not a C11-C render failure.

V1 emitted no completed Godot exit code/receipt/report. No PASS claim is accepted. Preserve the partial V1 run; Ctrl+C the foreground command if still active.

## V2 changes

1. `build_godot_command()` no longer passes `--headless`; the existing Godot renderer runs so SubViewport frames can actually be drawn.
2. Runner uses `subprocess.Popen` with stdout/stderr redirected directly to durable files rather than buffered `capture_output`.
3. A heartbeat is printed every five seconds while Godot runs.
4. Godot has a 90-second hard timeout. On expiry the child is terminated, then killed if needed, and the exception reports exact preserved log paths.
5. `EVIDENCE_DIR` is printed as soon as its directory is created, before extraction/Godot.
6. Runner prints stage markers before each FFmpeg sample extraction and before Godot launch.
7. GDScript prints per-variant/sample BEGIN/DONE markers and explicit markers around `process_frame` and `RenderingServer.frame_post_draw` awaits.
8. Test suite enforces non-headless launch and bounded process/log behavior.

## Reused evidence and scope

Input is the accepted E4A.2 directory `artifacts/tests/c11e/e4a_real_body_pixel_review/RUN_20261104_002559_542bcf60`, not a new C11-C render. It contains the pinned original C11-C base MP4 and test-only normalized REVIEW_720 derivative. FFmpeg extracts six still frames; only the existing D-owned in-memory materializer's isolated test branch composes 18 PNGs.

The branch is not the production Producer dispatch or full-duration compositor. Placeholder typography and placement remain unapproved. `player_name`/`challenge_label` remain geometry-blocked. No media/audio or production renderer is created.

## Exact V2 source hashes

- `materialize_challenge_visual_payload_in_memory.gd`: `3d1c8288ffbea3ff328d785def5fabba250b042c0d2d1b1f94215b1c62cde29b`.
- `c11e_e4a_d_compositor_real_body_pixel_review.py`: `3165f99ddf37252b3ed2fc5becbe98877b0c945d5ef57dcbfb59dd18cc7852f1`.
- `test_c11e_e4a_d_compositor_real_body_pixel_review.py`: `1e51fa2e47339097e6c66354cf2920eccff804d032787d0b268e2bdef2c22300`.
- Preparation focused tests: 50/50 PASS; py_compile PASS.

## Runtime acceptance criteria

Godot 4.7.1, renderer enabled, exit 0, exact compositor marker, 6/6 backgrounds, 18/18 720×1280 PNGs, 12/12 comparisons, A exactly equals the source RGB image, B/C visual contract passes, BODY identical at six source points, source MP4s/frame PNGs remain byte-identical, manifest SHA remains unchanged. Required report/receipt/SHA sums and stdout/stderr must be included in uploaded RUN ZIP.

`VISUAL_PLACEMENT=UNAPPROVED` is expected and required. `production_renderer=false`, `production_dispatch=false`, `production_media=false`, `D4.8=BLOCKED`, `D9.10=PREPARE_ONLY`, `release_authority=NONE` remain unchanged.
