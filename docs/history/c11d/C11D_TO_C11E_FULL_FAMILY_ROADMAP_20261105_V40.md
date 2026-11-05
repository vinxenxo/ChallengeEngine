# C11-D to C11-E Full-Family Roadmap — V40

**Date:** 2026-11-05. Supersedes V39 for current E progress only; no governance lock is superseded.

## Product outcome

One C11-E orchestration service with family-specific adapters for Challenge, Visual Loop and Visual Drill. It will produce validated audiovisual outputs on demand through the existing GUI/CLI contract while preserving C11-C mechanics, source truth, native binders and family music semantics. Only after E8 and explicit promotion may D+E replace C11-C as the production factory.

## Current progress

- E0/E1/E2 remain accepted in declared scopes; E3 remains at its previously accepted scope.
- E4A.2 and E4A.3D.1 remain accepted test-only evidence. E4A.3D.1 proves isolated real-body compositor mechanics, not a live Challenge root.
- E4A.5B read-only source review is PASS on the latest supplied snapshot (`a70ff52e...`). The 88-member source handoff reconciles as 83 exact + 5 authorized postimages; Challenge root/scene, phase call sites, C launcher, QA caller, E1 GUI/service and A/V path were reviewed. Snapshot contains no `.git`, so branch/HEAD/dirty status is unknown.
- E4A.6 minimum D-only consumer design is ready but not implemented. It must attach after each existing native binder call, avoid a second full `PresentationUI` apply, mount the shared editorial layer once, and assign CTA ownership by approved source-time window.
- Existing C Challenge A/V path is understood (Godot native 540x960 + optional C7 PCM, FFmpeg scale/H.264 + AAC mux/FFprobe). This is not D3 V5. D3 engine/audio generation and mux remain unproven.

## Ordered gates

1. E4A.6: implement and test the D-owned Challenge live consumer/envelope; preserve native timeline and single-pass binder; verify Hook/Countdown/CTA ownership.
2. E4A final: D3 V5 Challenge music engine, independent `music_seed`, actual audio generation, FFmpeg mux/FFprobe and GUI/CLI prepare parity. Complete separate human visual/listening review.
3. E4B: 27 Visual Loop grammar identities, existing Loop family/grammar music, editorial/layout/timing.
4. E4C: 20 Visual Drill variants, existing Drill music, phase and END_CTA precedence.
5. E5: cross-family determinism, gameplay/music seed isolation, no adapter/profile leakage and GUI/CLI parity.
6. E6: Smoke18 (six audiovisual cases per family).
7. E7: Matrix101 (54 Challenge + 27 Loop + 20 Drill); CH_008/009 stay held until declared 11s vs phase-sum 12s is reconciled by authority.
8. E8: full C-to-E regression map, independent acceptance, immutable freeze and explicit promotion decision.

E4B/E4C remain held until Challenge E4A.6 and D3 A/V acceptance are complete.

## Invariants and governance

C11-C 2.19.12 manifest SHA-256 remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. No changes to C11-C core/audio, mechanics, binders, RNG ownership, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C11-C presentation contracts, C launcher or QA caller. No parallel renderer, Producer or sixth GUI module. Production renderer/dispatch/media remain disabled and `release_authority=NONE` until an explicit E8 authority decision.
