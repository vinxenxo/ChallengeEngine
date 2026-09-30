# C11-C Producer 0.9.7 — Operator Surface

The Producer is the audiovisual orchestration surface inside `c11c-suite`.

## Current backend routing

- Challenge review: `tools/qa/c11/run_c11c_challenge_bulk_qa.ps1`.
- Historical C11-A.1 qualification: `tools/qa/c11/run_c11a1_challenge_bulk_qa.ps1` only for explicit compatibility evidence.
- Visual Loop production: canonical C11-C bulk production launchers.
- Visual Drill production: `run_visual_drill_production.ps1` delegates to the canonical authoring/review path.
- Art Direction bulk review: `tools/prototypes/c11c_bulk/run_c11c_art_direction_batch_v4.ps1` with the established private-worker model.

## Operator parity

The GUI is an orchestration client. It does not implement mechanics, simulation, structural RNG or a duplicate renderer. The same canonical commands must remain available from the console.

During D, use the Producer GUI and direct CLI together. A GUI success must be reproducible through the corresponding canonical command and manifest/provenance path.

## Engine-lineage terminology

The Producer schema may identify the certified engine/profile lineage as 2.16.9. This is provenance for the underlying immutable engine contract. It does not replace the current C11-C 2.19.12 orchestration/tooling baseline.

## Current release state

Producer 0.9.7 has passed the final C11-C 2.19.12 acceptance together with the GUI contract. Any active Producer/Suite routing change after acceptance requires a fresh full acceptance before freeze.
