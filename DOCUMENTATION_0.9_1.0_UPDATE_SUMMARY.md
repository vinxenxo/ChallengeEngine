# Documentation update summary — 0.9.0 → 1.0.0

## Scope
Documentation only. No `.gd` or challenge fixture JSON has been modified by this update package.

## Current-state corrections applied

- Updated live production status to 0.9.0 FROZEN / VALIDATED.
- Formalized `factory_version = 0.9.0` and `manifest_version = 1.0`.
- Documented mixed RNG 1.0/2.0 batch semantics.
- Documented canonical output isolation and provenance snapshot rules.
- Updated stale 3+7+1 references in live-facing guidance by explicitly marking them historical and stating 2+7+2 as the live contract.
- Updated root READMEs and live roadmap/testing/governance documentation.
- Added a 0.9.0 handover.
- Added a formal 0.9.0 provenance contract document.
- Added a revised FIND V1 contract draft.
- Preserved old checkpoint handovers and checkpoint-status documents as historical records.

## FIND draft not frozen

The FIND draft remains `DRAFT / REVISION REQUIRED` for two reasons:

1. `close_calls` should not be frozen as a raw per-frame distractor count; an event-based false-positive contract is safer and semantically meaningful.
2. The presentation layer must not regenerate structural distractor positions or consume structural RNG. The exact one-time static transport mechanism is still an isolation/presentation-contract decision.
