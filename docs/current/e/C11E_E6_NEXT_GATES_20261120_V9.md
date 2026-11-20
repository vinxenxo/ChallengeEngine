# C11-E E6 next gates — V9

## Immediate bounded action

Install the direct RGB24 visual-probe overlay ADD_ONLY, run the 28 focused manifest tests once, then run the exact one-shot L2 script once. It creates one fresh direct viewport capture from the pinned C11-C `fractal_bloom/radial_bloom` scene at gameplay seed 100006/frame 0, and performs one QImage composition.

## Why not decode historic MP4

All checked R1V and Loop22 sidecars provide `yuvj420p`/full-range but omit matrix, primaries and transfer. There is no defensible BT.709 assumption. The new direct viewport path bypasses historic YUV decode and performs no colour transform. It does not claim equality with the historic MP4 frame.

## After the one-frame artifact

1. Inspect the captured source and `composited_frame.png` visually; explicitly approve/reject the resampler.
2. Run a separately versioned L3 set of negative controls, no-change source checks, exact pixel-buffer identity and geometry/band checks.
3. Only after L2/L3 decisions, prepare a separately approved six-selector Loop manifest. No implicit widening.

Smoke18 remains separately blocked. No audio, FFmpeg, FFprobe, mux, dispatch or production renderer is included in this one-frame probe. E6 accepted remains zero.
