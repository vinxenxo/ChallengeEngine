# Roadmap — C11-C 2.19.6 Candidate → Final C11-C Freeze → D

## Current gate

C11-C is at **2.19.6 consolidated repair candidate** status. The old 2.19.2 freeze claim is superseded for final-freeze purposes. The immediate objective is one consolidated workstation acceptance, not another patch chain.

## Acceptance sequence

1. Consolidate the 2.19.x documentation and archive superseded patch/current files.
2. Run focused C11-C contracts, including the parallel worker-isolation contract.
3. Run the full logical corpus and the historical C11-A.1/retrocompatibility gates.
4. Run physical smoke/export acceptance.
5. Run the complete C11-C Art Direction review with `Workers=7` and record `MAX_OBSERVED_CONCURRENCY` > 1.
6. Run Visual Drill review smoke.
7. Only after all evidence is green, create the next formal C11-C freeze and then activate D.

## D sequence after the new freeze

1. **D0 — Baseline inventory and Challenge recovery.** Inventory the exact frozen repository and recover CHALLENGE_001 … CHALLENGE_009 into evidence-backed dossiers.
2. **D1 — Challenge visual convergence.** Define visual parity against the proven C11-C language without modifying mechanics or timing truth.
3. **D2 — Asset-family/template registry.** Introduce versioned declarative asset families and semantic slots.
4. **D3 — Procedural Music V5.** Design/implement richer deterministic music without hidden gameplay coupling.
5. **D4 — Production request/personalization.** Define a canonical per-video request and persist its provenance.
6. **D5 — Artifact/provenance normalization.** Make reconstruction inputs explicit and auditable.
7. **D6 — Seed registry and traceability.** Track historical/used/reserved/released/invalidated seed states.
8. **D7 — Challenge production matrix.** Drive nine historical Challenges through the normalized content/presentation/audio/delivery model.
9. **D8 — Media QA/release evidence.** Recover and operationalize the historical Final Export intent.
10. **D9 — Suite evolution.** Extend operator surfaces only where dedicated contracts justify them.

## Boundary carried into D

No D work may silently modify:

- simulation mechanics/mathematics;
- RNG ownership/algorithm;
- `SimulationResult`;
- `winning_frame`;
- `close_calls`;
- `WinningFrameDetector`;
- `RenderedFrameStream`;
- C7/C9 contracts;
- logical 540×960 C11-B/C geometry.
