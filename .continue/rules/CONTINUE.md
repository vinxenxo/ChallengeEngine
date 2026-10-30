# CONTINUE.md — C11-E engineering continuation (V4)

## Current state

The active workstream is C11-E on local Git branch `main`; never switch branches or refs. Current reviewed HEAD: `bc8330e794fe37efe0c4f9c2bb0c0bd389f28f2c`. C11-C 2.19.12 remains the production baseline until independent E8 acceptance.

E0 bootstrap has been independently reviewed and is PASS. The addendum updates this routing file and `AGENTS.md` to V4 while preserving their exact V3 versions under `docs/history/c11e/`. E1 source architecture review is complete at inspection level; E1 implementation remains in progress.

Read `AGENTS.md`, `docs/current/e/README.md`, `C11E_CURRENT_AUTHORITY_20261030_V4.md`, `C11E_GATES_ACCEPTANCE_MATRIX_20261030_V4.md`, `C11E_E0_REVIEW_AND_E1_SOURCE_ARCHITECTURE_20261030_V1.md`, `C11E_DOCUMENTATION_RECONCILIATION_20261030_V4.md`, and charter/contract/risk register V3.

## Functional focus

Implement one canonical E production service inside existing `c11c-suite/c11c-producer`; GUI and CLI must call it. Reuse D9.9 resolution where valid, but do not repurpose D9.10 or `shared_production_context_service.py` (D preparation-only). No physical render during E1.

Then E2 adds a dedicated visible `editorial.title` slot for Challenge and exactly two isolated `CHALLENGE_001` MP4s differing only in title. Keep `content.hook`, CTA and simulation truth independent. Compare frames/pixels and confirm gameplay seed, duration and frame count unchanged.

## Non-negotiables

Preserve C11-C freeze manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`, 796318 bytes. Do not change simulation, `SimulationResult`, `winning_frame`, `close_calls`, RNG, mechanics, frame stream or challenge definitions. `request.seed` and `request.music_seed` are independent. D3 is E3. Loops/Drills are E4. CHALLENGE_008/009 remain excluded until the 11 s/12 s discrepancy is resolved. Do not alter D receipts or governance flags.

PowerShell 5.1 only; full pasteable blocks. Prehash sources, stop on drift, preserve outputs and receipts. No branch changes, commit, push, renderer in E1, stale PASS, or docs-only workstreams.
