# ChallengeEngineV01_STATELESS

Deterministic challenge/video factory built on Godot 4.7.1 with a strict separation between declarative definitions, deterministic simulation, passive presentation and production orchestration.

## Current state

**C11-B — semantic FREEZE CLOSED / repository organization PREPARED — PENDING USER VALIDATION.**

The behavior is frozen. This maintenance checkpoint only reorganizes the repository and its evidence paths. The organized tree must pass the complete runbook before it is committed as the new working baseline.

Pre-cleanup owner-supplied evidence:

```text
logical             103/103
C11 contracts       PASS
C11-A               54/54
C11-A.1             54/54
retro               54/54
stress              288 cases / 576 executions
physical            2/2
video matrix        54/54 video renders
```

## Repository

See `docs/04_REPOSITORY_STRUCTURE.md` for the canonical layout.

Generated output belongs under `artifacts/`. Historical material is retained below `docs/history/` and `artifacts/legacy/` and is not part of the active execution path.

## Architecture

```text
Definition
    ↓
Deterministic SimulationResult
    ↓
CoordinateMapper / PresentationFramer
    ↓
UnifiedSocialFrame
    ↓
RenderedFrameStream
    ↓
Production
```

See `docs/01_ARCHITECTURE.md`, `docs/03_PRESENTATION.md` and `docs/contracts/C11_ARCHITECTURE_MANIFESTO.md`.

## Tests

Fast logical regression:

```powershell
python .\tests\run_all.py
```

Complete validation is in `docs/operations/TEST_RUNBOOK.md`.

## Production

`build_factory.py` is the canonical factory CLI. Its normal output root is `artifacts/production/challenges`.

See `docs/06_PRODUCTION_AND_DISTRIBUTION.md`.

## Roadmap

After repository organization is validated and committed:

**C11-C Art Direction → C11-D Final Export → C11-E Distribution → Production**

See `docs/07_ROADMAP.md` and `docs/master-prompts/START_PROMPT_C11C_ART_DIRECTION.md`.
