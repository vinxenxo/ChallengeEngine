# C11-D — Approved Milestones

**Entry condition:** C11-C 2.19.12 sealed archive + verified archive SHA-256 + source-tree SHA-256 + freeze receipt.

## Invariant across all D milestones

GUI and CLI are co-equal operator surfaces. Every new capability must have a canonical console path and a thin GUI wrapper over that operation, with identical inputs, provenance and reproducible outputs.

| ID | Milestone | Required gate |
|---|---|---|
| D0 | Baseline proof + 9 Challenge recovery dossiers | archive/tree hashes, inventory, nine dossiers, mismatch register, no C11 engine changes |
| D1 | Challenge visual/editorial parity | parity contract, one pilot, focused regression, safe-area proof |
| D1.5 | Layout/template sub-checkpoint | safe-area template contract; does not introduce a new branch or duplicate the D1 gate |
| D2 | Reusable Atari-2600-inspired asset families/templates | schema, registry, slot compatibility, swap/provenance test |
| D3 | Procedural Music V5 | design contract, deterministic A/V comparison, mobile/loudness QA |
| D4 | Declarative production request + personalization | request schema, GUI/CLI parity, request hash, exact reproduction |
| D5 | Provenance + artifact topology | topology contract, dry-run migration, preservation/safety tests |
| D6 | Seed registry + governance | lifecycle schema, collision/reuse controls, GUI/CLI parity |
| D7 | Nine-Challenge matrix + catalog | normalized matrix, catalog indexes, deterministic rerun |
| D8 | Media QA + release pipeline | complete media audit, release candidate, hashes/evidence |
| D9 | Suite integration/evolution | consistent exposure in Test/Producer/Maintenance/Catalog/Config |
| D10 | New mechanics | authored truth, answer data, explicit timing semantics, focused + integration regression, rollback evidence |

## Ordering rationale

D0-D2 recover and stabilize the Challenge visual/content foundation. D3 establishes deterministic music before personalization. D4-D6 make production requests, artifacts and seeds reproducible. D7-D9 industrialize the nine-Challenge production and operator surfaces. D10 remains last so new mechanics cannot destabilize the recovered foundation.

## Decision

**APPROVED.** Sequence:

`D0 → D1 (+ D1.5 sub-checkpoint) → D2 → D3 → D4 → D5 → D6 → D7 → D8 → D9 → D10`

D10 does not begin while D1-D6 foundations are unstable.
