# Agent Guide — ChallengeEngineV01_STATELESS

## Current baseline

**C11-B FREEZE** is the authoritative functional baseline. The repository organization work is a path/layout refactor only and must preserve all C11-B behavior and regression coverage.

Read `docs/00_PROJECT_OVERVIEW.md` first, then `docs/01_ARCHITECTURE.md`, `docs/02_DATA_AND_CONTRACTS.md`, `docs/03_PRESENTATION.md`, `docs/04_REPOSITORY_STRUCTURE.md`, `docs/05_TESTING_AND_REGRESSION.md` and `docs/07_ROADMAP.md`.

## Engineering boundary

The project has four layers:

1. Definitions
2. Deterministic simulation
3. Passive presentation
4. Production orchestration

Presentation cannot calculate gameplay truth. Simulation cannot depend on presentation. Structural RNG cannot be consumed by cosmetic rendering.

## Important live paths

- `Main.tscn` — project entry scene
- `GeneradorMaestro.gd` — live composition/runtime root
- `build_factory.py` — production factory
- `core/` — engine source
- `challenges/` — canonical challenge corpus
- `definitions/` — canonical visual definitions
- `profiles/` — profiles
- `tests/` — regression corpus
- `tests/fixtures/` — test-only inputs
- `tools/c11freeze/` — deterministic/freeze automation
- `artifacts/` — generated evidence
- `docs/` — live documentation

## Determinism

`DeterministicLCG` remains stateless. RNG streams must have explicit ownership. Presentation must not change simulation output, winning frame or gameplay telemetry.

## Testing contract

Run from the repository root:

```powershell
python .\tests\run_all.py
```

For the full validation sequence use `docs/operations/TEST_RUNBOOK.md`.

Every discovered `*Test.gd` requires an explicit `KNOWN_SUITES` entry and declared PASS marker in `tests/run_all.py`. A missing registration is a deliberate fatal error.

## Repository hygiene

Do not create new generated-output roots. Use `artifacts/`. Keep caches and generated import state out of Git. Do not delete a test or fixture simply because it looks old; first determine whether it protects compatibility or a frozen contract.

Historical documents and one-off patch scripts are retained under `docs/history/` when their audit value justifies it. They are not live implementation paths.

## C11-C

The next product phase is Art Direction. It may change presentation assets, typography, styling, visual hierarchy and passive renderer appearance. It must not cross the frozen simulation/RNG/data contract boundary without a new checkpoint.
