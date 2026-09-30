# C11-D — Approved Milestones

**Decision:** APPROVED for execution after C11-C 2.19.12 is frozen.

| ID | Milestone | Gate before next |
|---|---|---|
| D0 | Baseline proof, repository inventory and recovery of the 9 historical Challenges | Frozen tree verified; 9 dossiers complete; no mechanics changed |
| D1 | Challenge visual/editorial parity with C11-C | One pilot proves composition/typography/copy/audio-direction without changing timing truth |
| D1.5 | Declarative platform/layout template contract | Layout schema + focused contract test |
| D2 | Reusable Atari-2600-inspired asset families/templates | Semantic slots, family registry, provenance and cross-Challenge binding test |
| D3 | Procedural Music V5 | Design contract first; deterministic layered implementation + audio QA |
| D4 | Declarative production request + per-video personalization | Exact request hash + reproduction test |
| D5 | Artifact topology + provenance | Products/reviews/tests/logs/scratch/indexes separated and queryable |
| D6 | Seed registry + anti-reuse policy | USED/RESERVED/RELEASED/INVALIDATED/HISTORICAL states + audit trail |
| D7 | 9-Challenge production matrix | Shared visual/asset/music/seed/layout profiles drive matrix from one backend |
| D8 | Media QA + release evidence | Technical A/V validation, package manifest, hashes, reproducibility |
| D9 | Suite evolution | GUI and CLI remain parity surfaces; new capabilities only after stable contracts |

## Sequencing decision

**D0 -> D1 -> D1.5 -> D2 -> D3 -> D4 -> D5 -> D6 -> D7 -> D8 -> D9.**

Do not introduce new Challenge mechanics before D1-D6 are stable. D is not a reason to reopen C11-B/C engine truth.

## Rationale

The sequence separates recovery, visual convergence, reusable content primitives, audio, production declaration, provenance and seed control before the large production matrix. This prevents the one-off pipeline fragmentation that C11-C spent 2.19.x eliminating.
