# C11-D to C11-E full-family roadmap â€” V11

**Date:** 2026-11-01. This roadmap is retained across context changes; do not restart accepted E0/E1 gates.

## Product objective

Production-ready output for Challenge, Visual Loop and Visual Drill. Keep the existing C11-C generators and mechanics intact. Add C11-D presentation, enabled family-scoped editorial, and D3 Music V5. Both GUI and CLI use the same shared production service. Final output is MP4 with FFmpeg mux, independent gameplay/music seed domains, and FFprobe A/V validation. CHALLENGE_001 A/B is the first technical control only, not the final product.

## Ordered E gates

1. **E0 â€” foundation and continuity:** repository authority, protected baseline and execution governance. Accepted; do not repeat.
2. **E1 â€” shared production service:** same adapter/service for CLI and GUI. Automated suite 2/2 passed; manual GUI observation remains pending and must be recorded later.
3. **E2 â€” first physical integration control:** Challenge presentation/editorial sidecar, title-only A/B, same gameplay, separate titles. Pre-render numeric contract 30/30 and Python contract 9/9 passed. R3 partially generated A and failed because final MP4 remained full-range `yuvj420p/pc`. The encode-range correction now produces `yuv420p/tv`; next is R4 with two renders, all frame comparisons, FFprobe/SHA checks and independent visual review. E3 remains blocked until E2 is formally accepted.
4. **E3 â€” D3 Music V5:** implement/verify deterministic music generation using `request.music_seed` independent from gameplay `request.seed`; integrate FFmpeg audio mux; FFprobe audio/video stream, codec, sample rate, channel layout, duration, offsets and A/V synchronization. Include negative tests and repeatability.
5. **E4A â€” Challenge integration:** production Challenge family adapter consumes allowed presentation and enabled editorial fields; preserve source mechanics.
6. **E4B â€” Visual Loop integration:** Loop binder/adapter and editorial mapping; prove correct family-specific fields.
7. **E4C â€” Visual Drill integration:** Drill binder/adapter and editorial mapping; prove correct family-specific fields.
8. **E5 â€” cross-family quality:** deterministic reruns, gameplay/music seed isolation, FFmpeg/FFprobe A/V behavior, GUI/CLI parity, negative cases, no leakage between family adapters.
9. **E6 â€” Smoke18:** six smoke scenarios per family (18 total), including media metadata and visual review controls.
10. **E7 â€” Matrix101:** 54 Challenge + 27 Loop + 20 Drill. CH_008/CH_009 remain held because their declared 11-second duration conflicts with 12 seconds of phase sum (3+7+0+2). Runnable population is 99 until explicit resolution; never call 101 complete prematurely.
11. **E8 â€” independent acceptance and promotion:** separate review, complete evidence, freeze package and explicit authority to promote D/E over C. Until then C11-C 2.19.12 remains authoritative.

## Current continuation point

- R1: stale test 09; no render.
- R2: stale test 09; no render.
- R3: A only; MP4 rejected for `yuvj420p/pc`; B not run.
- R4: next; runner source SHA `158325324626085ebf319f68906ca8778f9a08eb39c6e8441da146c12ee4f953`; request ID `C11E-E2-CH001-AB-20261101-V9-R4`.
- Seeds: gameplay `193847`, music `840001`; E2 audio remains disabled.