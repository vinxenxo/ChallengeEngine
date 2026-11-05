# C11-D to C11-E Full-Family Roadmap — V41

**Date:** 2026-11-05. Supersedes V40 for current implementation status only; no governance lock is superseded.

## Product outcome

One C11-E orchestration service with family-specific adapters for Challenge, Visual Loop and Visual Drill. It will generate validated audiovisual outputs on demand through the existing GUI/CLI contract while preserving C11-C mechanics, source truth, native binders and family music semantics. D+E replaces C11-C as production factory only after E8 and an explicit promotion decision.

## Current progress

- E0/E1/E2 accepted in declared scopes; E3 retains accepted scope.
- E4A.2 and E4A.3D.1 accepted test-only evidence.
- E4A.5B PASS: Challenge root/source reviewed against user-provided latest snapshot; 88 historical members reconcile as 83 exact + 5 authorized. Git provenance is unavailable in archive.
- E4A.6 D-only consumer implementation and static tests prepared. The consumer is optional/lazy-loaded from a separate envelope argument, invoked after the four native binder calls, uses one shared-layer mount and leaves one timeline advance per frame. 16 Python tests pass; Windows Godot 4.7.1 live-root receipt still required.
- Current C Challenge A/V path is Godot 540x960 + optional C7 PCM + FFmpeg H.264/AAC mux/FFprobe. It is not D3 V5; actual D3 engine/audio generation and mux remain unproven.

## Ordered gates

1. **Finish E4A.6:** Windows PS5.1 apply runner; Godot 4.7.1 headless live-root proof; require 900 frames, one layer mount, correct Hook/CTA ownership, zero native CTA ownership during active D CTA; clean stderr and exit 0.
2. **E4A final:** actual D3 V5 Challenge music generation with independent `music_seed`, audio/mux/FFprobe, source-time correctness, human visual/listening review and GUI/CLI prepare parity.
3. **E4B:** 27 Visual Loop grammars; preserve five families, Loop timing and existing family/grammar music.
4. **E4C:** 20 Visual Drill variants; preserve four types, Drill timing/music and END_CTA precedence.
5. **E5:** cross-family determinism, seed isolation, adapter/profile non-leakage and GUI/CLI parity.
6. **E6:** Smoke18, six complete A/V cases per family.
7. **E7:** Matrix101 (54 Challenge + 27 Loop + 20 Drill); CH_008/009 remain held until declared 11s vs phase-sum 12s is authoritatively reconciled.
8. **E8:** complete regression map, independent acceptance, immutable freeze and explicit promotion decision.

E4B/E4C remain held until Challenge E4A.6 and D3 A/V acceptance are complete.

## Invariants and governance

C11-C 2.19.12 manifest SHA-256 remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. No changes to protected C11-C mechanics, RNG, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C binders, Loop/Drill semantics, C launcher or QA caller. No automatic seed generation or serialization of `FrameSnapshot.custom_data`. Renderer/production dispatch/media remain OFF; `release_authority=NONE`.
