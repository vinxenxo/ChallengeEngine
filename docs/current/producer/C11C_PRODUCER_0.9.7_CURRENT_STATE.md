# C11-C Producer 0.9.7 — Current State

The Producer is an orchestration layer around canonical C11-C scripts for Challenges, Visual Loops and Visual Drills.

Current Challenge review launcher: `tools/qa/c11/run_c11c_challenge_bulk_qa.ps1`. The historical A1 qualification runner is retained separately for regression evidence and is not used by `REVIEW_CHALLENGES`.

The Producer does not implement mechanics, RNG, simulation truth or renderers. `Workers=7` concurrency remains owned by the canonical Art Direction runner.
