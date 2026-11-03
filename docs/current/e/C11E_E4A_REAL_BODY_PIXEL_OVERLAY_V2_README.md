# C11-E E4A real-body pixel correction overlay V2

Apply at the repository root with a PowerShell 5.1 block that verifies the ZIP SHA, frozen C11-C manifest SHA, all payload postimages and exact V1 preimages before replacing the two existing E4A.2 Python files. The remaining V37 documents are add-only. Do not extract the ZIP wholesale over the checkout.

## Corrective purpose

The V1 E4A.2 runner expected the raw C11-C `REVIEW_720` MP4 to be 30fps/450 frames/yuv420p. The supplied successful CHALLENGE_004 output is H.264 720×1280, 60fps/900 frames, `yuvj420p/pc`, 15s. V2 preserves it byte-for-byte and creates a separate test-only 30fps/450-frame `yuv420p/tv` derivative for sampling. It records the source/manifest pixel-format discrepancy.

V2 adds `--reuse-c11c-base-run` so the existing `RUN_20261103_235800_fd6fb07c` MP4 can be reused without Godot or C11-C rerender. This argument only accepts an existing RUN directory directly below `artifacts/tests/c11e/e4a_real_body_pixel_review`.

## Apply and execute

1. Validate the package and replace only the runner/test pair when the installed files match their recorded V1 preimages (or exact V2 postimages for idempotency).
2. Add the versioned authority, backlog, matrix, increment, failure analysis, roadmap and both continuation prompts.
3. Run `python -B .\tools\c11d\d9\test_c11e_e4a_challenge_real_body_pixel_review.py` and require 33/33.
4. Run `python -B .\tools\c11d\d9\c11e_e4a_challenge_real_body_pixel_review.py --reuse-c11c-base-run ".\artifacts\tests\c11e\e4a_real_body_pixel_review\RUN_20261103_235800_fd6fb07c"`.
5. Capture `$LASTEXITCODE` immediately. A thrown error means FAIL; do not type a later success marker manually.

## Acceptance boundary

The corrected runner is still test-only. Its placeholder typography establishes pixel-region confinement, not production visual layout. The reviewed montage has overlap with the C11-C hook headline; D1.5 safe area/typography remains UNKNOWN. No production renderer, D9.10 dispatch, production media or release authority is enabled.
