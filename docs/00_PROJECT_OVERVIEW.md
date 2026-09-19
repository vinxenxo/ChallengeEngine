# ChallengeEngineV01_STATELESS — Project Overview

## Purpose

ChallengeEngineV01_STATELESS is a deterministic challenge and video factory built on Godot 4.7.1. The project separates declarative definitions, deterministic simulation, passive presentation and production orchestration so visual evolution does not redefine gameplay truth.

## Current state

**C11-B — CLOSED / CERTIFIED / FROZEN.**

The C11-B freeze established and validated the common 540×960 social presentation frame:

```text
HEADER   Y 0..144
BODY     Y 144..816
FOOTER   Y 816..960
```

The repository is now entering a separate **Repository Organization Checkpoint**. This checkpoint is a maintenance/restructure operation: it must preserve the C11-B behavior and all executable regression coverage.

## Frozen pillars

1. Stateless deterministic simulation.
2. Explicit semantic RNG stream ownership.
3. `SimulationResult` / frame snapshots as gameplay truth.
4. Passive presentation.
5. `RenderedFrameStream` as the visual runtime contract.
6. C7 audiovisual contracts, including the authoritative audio policy gates.
7. C9 authoring contracts and canonical production metadata.
8. Reproducible QA and evidence under `artifacts/`.

## Current working rule

Repository cleanup may move files and update references, but must not alter simulation mathematics, RNG behavior, canonical definitions, winning-frame semantics or frozen presentation contracts. After the cleanup, the reorganized repository must pass the complete documented validation suite before it becomes the new working baseline.

## Where to start

- Architecture: `docs/01_ARCHITECTURE.md`
- Contracts and data: `docs/02_DATA_AND_CONTRACTS.md`
- Presentation: `docs/03_PRESENTATION.md`
- Repository layout: `docs/04_REPOSITORY_STRUCTURE.md`
- Testing: `docs/05_TESTING_AND_REGRESSION.md`
- Production/distribution: `docs/06_PRODUCTION_AND_DISTRIBUTION.md`
- Roadmap: `docs/07_ROADMAP.md`
- Test runbook: `docs/operations/TEST_RUNBOOK.md`
- Current handover: `docs/master-prompts/MASTER_HANDOVER_C11_B_REPOSITORY_ORGANIZATION.md`
