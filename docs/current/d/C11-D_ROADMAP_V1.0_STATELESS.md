# Challenge Engine V1.0 STATELESS — C11-D Roadmap

**Entry baseline: C11-C 2.19.12 FROZEN.**

D is an additive productization branch around an immutable C11-C baseline. GUI and command-line execution are co-equal operator surfaces: both call the same canonical backend commands, produce the same manifests and remain reproducible.

## D0 — Baseline lock, inventory and recovery

Freeze and hash the C11-C archive; inventory source, profiles, assets, seeds, manifests, Suite surfaces and historical evidence. Recover `CHALLENGE_001` through `CHALLENGE_009` into dossiers before changing Challenge presentation.

**Gate:** machine-readable inventory, nine recovery dossiers, verified baseline provenance.

## D1 — Challenge visual parity

Define and implement the Challenge presentation binding that follows the established C11-C composition/editorial/typography hierarchy while preserving Challenge timing, mechanics and deterministic answer truth.

**Gate:** visual-parity contract + one representative Challenge pilot + focused regression.

## D2 — Atari-2600-inspired asset families and templates

Create a declarative, versioned asset-family registry with semantic slots, compatible Challenge routes, palette/style metadata, preview references, hashes and provenance. Asset families must be interchangeable across Challenges without duplicating mechanic code.

**Gate:** schema, registry, swap test and provenance test.

## D3 — Procedural Music V5

Design before implementation: layered timbre, harmony, rhythm, motif, texture and spatial treatment. Keep the system deterministic and mathematically parameterized while decoupled from gameplay event truth and structural RNG.

**Gate:** design contract, deterministic render comparison, loudness/mobile QA.

## D4 — Declarative production request and personalization

One canonical request selects seed, content/Challenge, asset family, palette, typography, copy, music profile, delivery profile and single/batch mode. Hash the request and persist exact provenance.

**Gate:** request schema + CLI/GUI parity test + reproducibility test.

## D5 — Artifact, manifest and provenance topology

Separate durable products, reviews, tests, logs, scratch and indexes. Preserve source/config hashes, commands and manifests. Migrate in stages; never delete historical evidence as part of reorganization.

**Gate:** topology contract + migration dry-run + artifact safety tests.

## D6 — Seed registry and traceability

Introduce states such as `USED`, `RESERVED`, `RELEASED`, `INVALIDATED`, `HISTORICAL`. Reject known-used seeds by default; deliberate reuse requires an explicit auditable operator action.

**Gate:** registry schema + collision/reuse tests + GUI/CLI parity.

## D7 — Challenge production matrix and catalog

Drive all nine Challenges through normalized asset, visual, music, seed and delivery layers. Make the matrix queryable through `c11c-catalog` and reproducible from the CLI.

**Gate:** controlled matrix, catalog indexes, deterministic rerun evidence.

## D8 — Media QA and release pipeline

Recover the historical Final Export intent inside the new architecture: technical media checks, metadata, A/V QA, release packaging and reproducible evidence.

**Gate:** release candidate package + full media audit.

## D9 — Suite evolution

Extend `c11c-suite` deliberately into Test, Producer, Maintenance, Catalog and Config surfaces. New Asset, Music and Seed Registry surfaces appear only when their contracts are mature.

**Non-negotiable:** every GUI action has a direct CLI equivalent; no GUI-only logic path.

## D10 — New cognitive mechanics

Only after D1-D6 are stable, schedule new mechanics from the historical Drill/Challenge roadmap: predictive occlusion/morphing, N-back/flash recognition, pursuit depth/flanker loading, peripheral quadrant/rhythm layers and future Challenge mechanics. Every new mechanic gets authored truth, answer data, focused contracts and explicit checkpoints.

## Sequencing

```text
D0 baseline/recovery
  ↓
D1 visual parity
  ↓
D2 assets/templates
  ↓
D3 music V5
  ↓
D4 production request/personalization
  ↓
D5 artifacts/provenance
  ↓
D6 seed registry
  ↓
D7 production matrix/catalog
  ↓
D8 media QA/release
  ↓
D9 Suite evolution
  ↓
D10 new mechanics
```

This ordering is designed to prevent another generation of one-off pipelines.
