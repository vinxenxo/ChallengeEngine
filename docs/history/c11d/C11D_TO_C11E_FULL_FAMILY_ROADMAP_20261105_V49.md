# C11-D to C11-E Full-Family Roadmap — V49

**Date:** 2026-11-05. Supersedes V48 for the E4A.6 postprocess recovery state.

## Product outcome

One C11-E orchestration service and family-specific adapters for Challenge, Visual Loop and Visual Drill. Preserve C11-C mechanics, gameplay truth and family timelines. D contributes presentation/layout/editorial; Challenge uses D3 Music V5, while Loop/Drill retain their existing family music. GUI and CLI share one service. Full MP4 outputs use FFmpeg mux, FFprobe and immutable receipts. Only E8 plus separate approval can promote D/E over C11-C.

## Current Challenge progress

- E4A.2 source/body base, E4A.3D.1 D compositor proof, E4A.4 isolated audio/mux pilot and E4A.5B read-only source closure are accepted in their recorded test-only scopes.
- E4A.6 live-root consumer PASS_TEST_ONLY: 17/17 focused tests, Godot 4.7.1, 900 frames, one shared layer mount, expected header/footer/CTA owner counters.
- Movie Maker capture completed: exact 900-frame/60 FPS/15-second AVI exists. Correct evidence is configured marker, phase telemetry 180/420/180/120, audio export disabled and recording completion. Do not recapture.
- Postprocess V1 stopped before work due 63-character SHA constant; V2 stopped at SOURCE_FFPROBE due wrapper ExitCode observation; V3 fixed that and encoded/probed the silent MP4, then failed at BOUNDARY_STILLS because `-vsync` is unsupported in the operator's FFmpeg. A subsequent V3 run refused to overwrite the already-generated MP4. V4 revalidates and reuses that MP4 when valid, otherwise encodes a verified temporary candidate; it uses `-fps_mode vfr` and stages eight stills before promotion. No Godot/Movie Maker rerun.
- Operator feedback: no obvious visual defects. This does not constitute D1.5/D1.1/D1.7 safe-area or production layout approval.

## Baseline source discrepancy

The frozen C11-C manifest (796,318 bytes, SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`) pins the original `GeneradorMaestro.gd` SHA `4f10144c62c7bc149bd46aa37494b1df40c7185544b8477153150eec71c1aaf9`. The active D-only postimage is `d42782e8f5bb94ff0ede653a1c4624dc91541cc8203abf136b09a8fc288a7d82`. Do not alter the frozen artifact/manifest and do not further edit the shared source path until D/E integration isolation is explicitly decided.

## Ordered next gates

1. Run V4 postprocess once against the existing AVI. Verify/reuse V3's MP4, extract eight stills through `-fps_mode vfr`, produce contact sheet and add-only docs. No recapture.
2. Resolve the C11-C manifest source-path divergence before further runtime changes.
3. Run full E4A D-composited A/V with D3 V5 Challenge profile, D3.3 mastering, accepted AAC mux/FFprobe contract, exact FFprobe duration, independent music seeds, A/B/C cases, same video stream, non-silence and <=0.15s A/V drift. Human listening/visual review and GUI/CLI parity required.
4. E4B Loop; 5. E4C Drill; 6. E5 cross-family determinism/seed isolation/profile isolation/GUI-CLI parity; 7. E6 Smoke18; 8. E7 Matrix101 (CH_008/009 held for 11s/12s); 9. E8 full C-to-E regression map, independent acceptance, freeze and separate promotion.

## Governance

C11-C remains production authority. Renderer OFF, production dispatch OFF, media OFF, `release_authority=NONE`. D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION.
