# C11-C Suite 0.1.4 — C11-C 2.19.12 consolidated repair candidate

`c11c-suite/` is the canonical active operator and QA surface. C11-C 2.19.12 is a repair candidate, not frozen.

## Current contract

- Producer: 0.9.7.
- Godot: 4.7.1 stable Mono.
- Review delivery: 720x1280 @ 30 FPS.
- Visual Loops: 5 families / 27 grammars.
- Visual Drills: tracking, saccade, pursuit, peripheral_scan.
- Challenges: 9 definitions.
- Longforms: 5 x 180s.
- Complete visual review: 52 products.
- Family coverage smoke: 23 products (5 loops + 4 drills + 9 challenges + 5 longforms).

## Routing rules

Every Suite launcher resolves `C11C_PROJECT_ROOT` and changes directory to the repository root before dispatch. `c11c-maintenace/` is a compatibility alias only and delegates to `c11c-maintenance/`.

`c11c-studio/` is retired and is not an operational dependency.

## Frozen boundaries

The Suite orchestrates tests, review and delivery but does not implement mechanics, RNG, simulation truth, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7 audio ownership/contracts, C9 semantics or logical 540x960 social geometry.

## Runtime order

Focused contracts -> 3-video smoke -> family coverage smoke -> full logical -> complete 52-video review -> final acceptance. `Workers=7` must remain genuine concurrency with private worker project roots; no mutex or serial fallback.
