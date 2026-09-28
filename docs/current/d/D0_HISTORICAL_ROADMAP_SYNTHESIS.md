# D0 — Historical / Legacy Roadmap Synthesis

## Sources reviewed

The D sequence is derived from the frozen current roadmap plus the older roadmap and contracts preserved under `docs/history/`. The key references are:

- `docs/07_ROADMAP.md` — current C11 freeze → C11-D Final Export → C11-E Distribution lineage.
- `docs/history/reference/06_ROADMAP.md` — historical C11-C Art Direction, C11-D Final Export and C11-E Distribution.
- `docs/history/reference/ROADMAP_PHASES.md` — historical architecture progression from base pipeline through stateless RNG, semantic streams, authoring/runtime boundaries and productization.
- `docs/history/reference/contracts/MECHANICS_SPECIFICATION_V0.1.md` — six mathematical mechanic families and the distinction between mechanics and presentation/themes.
- `docs/history/reference/contracts/PRODUCTION_PROVENANCE_CONTRACT_V1.0.md` — provenance categories, manifest authority, asset-family/version fields and canonical production evidence.

## What this means for D

### Recover before redesign

The historical roadmaps consistently place asset/template work and production productization after the core mechanics/runtime contracts. Therefore D starts by recovering the nine existing Challenges and their asset intent rather than inventing a new mechanic immediately.

### Reusable asset families

The historical production provenance contract already treats `asset_family_version` as declarative provenance. The older roadmap also calls for production assets and reusable templates. D should turn that intent into a first-class versioned asset-family registry instead of copying graphics into each Challenge.

### Final export lineage

The historical C11-D wording emphasizes production-grade exports, metadata, quality validation and packaging. D should inherit those goals after the Challenge production request, provenance and artifact model are normalized.

### Mechanics remain separate

The historical mechanics contract defines six mathematical families and explicitly distinguishes themes such as retro/garage/sports/scifi from mathematical families. The proposed Atari-2600-inspired presentation for D therefore belongs to the asset/presentation layer, not to the mechanic taxonomy.

## Recommended D order

```text
D0  baseline + recovery inventory
 ↓
D1  Challenge visual convergence
 ↓
D2  asset family/template registry
 ↓
D3  procedural music V5 design + implementation
 ↓
D4  per-video production request / personalization
 ↓
D5  artifact + provenance normalization
 ↓
D6  seed registry / anti-reuse / traceability
 ↓
D7  Challenge production matrix
 ↓
D8  media QA / export / release evidence
 ↓
D9  Suite evolution
```

New mechanics should be scheduled after these layers are sufficiently stable to avoid rebuilding the production pipeline around every new content family.
