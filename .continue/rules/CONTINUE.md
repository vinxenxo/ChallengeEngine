# ChallengeEngineV01_STATELESS — Continuity Rules

## Authority order

1. Executable source code and current declarative definitions.
2. Live numbered docs under `docs/`.
3. Executable tests and their explicit PASS markers.
4. Checkpoint handovers.
5. `docs/history/` only for historical context.

## Current state

C11-B is frozen. The repository organization checkpoint must preserve that state. C11-C is presentation-only art direction.

## Architecture

```text
Definition -> deterministic simulation -> SimulationResult/FrameSnapshot
           -> passive presentation -> RenderedFrameStream
           -> production/export orchestration
```

`SimulationResult` is gameplay truth. Presentation must not recompute it. Structural RNG and cosmetic RNG remain separate.

## Repository rules

- New generated outputs belong under `artifacts/`.
- Test fixtures belong under `tests/fixtures/`.
- Active code belongs under `core/` or the established project entry points.
- Historical scripts/documents belong under `docs/history/` rather than active tooling.
- Do not recreate `output/`, `qa/` or `export/` as new source roots.

## Testing

The canonical logical runner is `python .\tests\run_all.py`. Every `*Test.gd` must be explicitly registered in `KNOWN_SUITES`.

For deterministic/release validation use the runbook at `docs/operations/TEST_RUNBOOK.md`.
