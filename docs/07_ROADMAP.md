# Roadmap to Production

This roadmap distinguishes completed/frozen engineering from future product work. Closed checkpoints are not reopened for convenience.

## Completed foundation

### C6-F0.8 — Visual runtime foundation

Deterministic visual loop/drill runtime, presentation and content/runtime boundaries frozen.

### C7 — Audiovisual

Audio generation, audiovisual export and policy gates frozen.

### C9 — Authoring

Productive challenge authoring and canonical generation contracts frozen.

### C10 — Visual authoring → runtime → physical export

Closed and certified.

### C11-A / C11-A.1 — Qualification

Closed and certified. Visual and challenge seed qualification matrices established the reference evidence used by later regression.

### C11-B — Unified Social Frame

Closed, certified and frozen. The common 540×960 Header/Body/Footer structure was introduced without changing simulation truth.

## C11-B Repository Organization

Maintenance checkpoint immediately after the semantic freeze.

**Goal:** make the repository understandable and maintainable without losing any executable test, fixture, contract or historically useful evidence.

**Acceptance:** the new layout passes the complete runbook, retired active roots are absent, documentation points to current paths, and the organization is committed separately from the semantic C11-B freeze.

## C11-C — Art Direction

First product-evolution checkpoint after repository organization.

1. inventory owner-supplied reference images;
2. define common visual vocabulary;
3. define measurable design tokens and layout constraints;
4. prototype one representative route;
5. physically render and compare;
6. propagate the accepted design system;
7. run visual regression across the defined routes;
8. freeze C11-C.

### Frozen during C11-C

The following remain closed unless a separate checkpoint explicitly reopens them:

- mechanic mathematics;
- RNG algorithms, versions and ownership;
- canonical challenge/visual definitions;
- `SimulationResult` semantics;
- winning-frame semantics;
- `RenderedFrameStream` contract;
- C7 audio contracts;
- C9 authoring contracts;
- C11-B Header/Body/Footer structure.

## C11-D — Final Export

Lock production presentation profiles, export settings, media QA, provenance and release-candidate evidence.

Deliverables should include:

- deterministic source snapshot;
- final visual/audio profiles;
- production render matrix;
- manifest/provenance records;
- physical media validation;
- reproducible export instructions.

## C11-E — Distribution

Finalize distribution metadata, packaging, platform-specific delivery procedures and operational release recovery.

Deliverables should include:

- versioned release package;
- distribution metadata;
- final checksums/provenance;
- release checklist;
- rollback/recovery procedure.

## Production launch gate

Production launch requires an explicitly versioned source snapshot and all applicable gates green. At minimum:

```text
SOURCE SNAPSHOT
    ↓
LOGICAL REGRESSION
    ↓
DETERMINISM / RETRO
    ↓
PHYSICAL MEDIA QA
    ↓
PROVENANCE / MANIFEST
    ↓
RELEASE CANDIDATE
    ↓
DISTRIBUTION QA
    ↓
PRODUCTION
```

No art-direction change is considered production-ready merely because it looks correct interactively; it must survive the physical export path and the applicable deterministic regression.

## Long-term principle

The project should grow by adding explicit checkpoints, not by silently mutating frozen ones. Every future architectural change should identify its contract, its migration path and its regression gates before implementation begins.
