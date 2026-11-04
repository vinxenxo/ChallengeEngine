# C11-D to C11-E Full-Family Roadmap — V39

**Date:** 2026-11-04. Supersedes V38 for current E progress; does not supersede governance locks.

## Product outcome

One C11-E production service with family-specific adapters for Challenge, Visual Loop and Visual Drill. It produces validated audiovisual outputs on demand through the existing GUI/CLI contract while preserving C11-C mechanics, source truth, binders and existing family music routes. Only after E8 and explicit promotion may D+E replace C11-C as the production factory.

## Current progress

E4A.3D.1 now has an isolated technical proof over real C11-C Challenge 004 frames: 6/6 source samples, 18/18 composited PNGs, 12/12 region comparisons, six-sample BODY identity, native hook recomposition, CTA single ownership and clean Godot stderr. A frame-signature format-string arity defect was corrected; the report gate was corrected to honor C11-C's font-metric word-boundary wrapping instead of requiring a fixed semantic split between rendered lines 2 and 3.

This is not a live root integration proof, production compositor approval, D1.5 geometry approval or release acceptance.

## Ordered gates

- E0/E1/E2: accepted in their bounded scopes.
- E3: retain its previously accepted scope and negative-control closure.
- E4A.2 / E4A.3D.1: accepted test-only real-body compositor proof.
- **E4A.5B:** read-only Challenge root/launcher source closure, including main scene, `GeneradorMaestro.gd`, transitive resources, C launcher, QA caller and phase-specific consumer call sites.
- **E4A.6:** minimum D-only live Challenge consumer integration at the source-proven seam; validate single owner for Hook/Countdown/CTA, correct editorial visibility, D3 V5 audio, mux/FFprobe and GUI/CLI.
- E4B: 27 Visual Loop grammar identities, existing Loop family/grammar music, editorial/layout/timing.
- E4C: 20 Visual Drill variants, existing Drill music, phase and END_CTA precedence.
- E5: cross-family determinism, gameplay/music seed isolation, no adapter/profile leakage and GUI/CLI parity.
- E6: Smoke18 (six audiovisual cases per family).
- E7: Matrix101 (54 Challenge + 27 Loop + 20 Drill); CH_008/009 remain held pending temporal authority.
- E8: full C-to-E regression map, independent acceptance, immutable freeze and explicit promotion.

## Invariants and governance

C11-C 2.19.12 manifest SHA-256 remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. No changes to C11-C core/audio, mechanics, binders, RNG ownership, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, or C11-C presentation contracts. No parallel renderer, Producer or sixth GUI module. Production renderer/dispatch/media remain disabled and `release_authority=NONE` until explicit E8 authority.