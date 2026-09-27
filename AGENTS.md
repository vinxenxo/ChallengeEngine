# Agent Guide — ChallengeEngineV01_STATELESS

## Authoritative next-context baseline

`ChallengeEngine-C11-C2.16.9 FROZEN.zip`

Retrieve that exact Library file before continuing in a new context.

## Current documentation

Read `docs/current/00_PROJECT_OVERVIEW.md` through `docs/current/07_ROADMAP.md` first. Current specialized handoffs live below `docs/current/`.

## Engineering boundary

Four layers: definitions/authoring, deterministic runtime/mechanics, passive presentation, production orchestration. Presentation does not calculate gameplay truth. Structural RNG remains owned by runtime/authoring contracts. Python Producer is orchestration only.

## Regression

```powershell
python .	estsun_all.py
```

Every discovered `*Test.gd` must have an explicit `KNOWN_SUITES` registration and PASS marker. Failed suites are re-run automatically with `--verbose` for diagnostics.

## Frozen C11-C milestone

C11-C 2.16 is frozen. Post-freeze changes are additive and belong to a new versioned line. Do not modify the frozen baseline silently.
