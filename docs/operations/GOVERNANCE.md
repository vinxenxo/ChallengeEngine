# Engineering Governance — Current

## Source authority

The Git repository is the source of truth for current code, tests, fixtures and active tools. Current numbered documentation and the latest handover are the source of truth for intent and process.

## Contract discipline

`AUDIT → CONTRACT → ISOLATION → INTEGRATION → REGRESSION → BATCH → FREEZE` remains the standard progression for a new mathematical or system capability.

A frozen boundary cannot be changed as an incidental side effect of another checkpoint.

## Determinism discipline

The same validated definition, seed, RNG contract and engine version must reproduce the same logical simulation telemetry. Presentation and production layers may transform the visual representation but may not alter gameplay truth.

## Repository discipline

Generated state does not belong in live source directories. Historical evidence remains available but is explicitly marked as historical. Every new generated path must have one canonical owner and one documented cleanup/recovery strategy.
