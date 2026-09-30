# C11-C Producer 0.9.7 — Current State

The Producer is a thin orchestration layer over canonical C11-C launchers.

## Current routing

- Challenges: `tools/qa/c11/run_c11c_challenge_bulk_qa.ps1` for current review.
- Historical A1 compatibility: `tools/qa/c11/run_c11a1_challenge_bulk_qa.ps1` only when explicitly requested.
- Visual Loops: canonical root C11-C production launcher.
- Visual Drills: Suite Producer wrapper around the canonical drill path.

The Producer does not implement mechanics, RNG, simulation truth or renderers.

## Backend version terminology

The Producer schema may still identify the underlying certified engine/profile lineage as 2.16.9. That is an engine-truth provenance identifier, not a claim that the surrounding C11-C 2.19.12 orchestration/tooling is obsolete.

## GUI/CLI parity

Producer GUI actions and direct commands invoke the same canonical backends. D must preserve this rule.
