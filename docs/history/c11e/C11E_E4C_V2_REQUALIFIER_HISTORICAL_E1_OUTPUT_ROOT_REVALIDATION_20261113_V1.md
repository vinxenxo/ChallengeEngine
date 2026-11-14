# C11-E E4C V2.3 R2 — Historical E1 output-root revalidation incident and correction

**Date:** 2026-11-13  
**Incident:** `E4C-CLI-COMPOSITION-V2-20261113T064622Z-c4d2534d`  
**Disposition:** Root cause established; D-owned correction prepared; R2 installer pending operator execution.

## Evidence and failure

The original evidence set is `E4C-CLI-SMOKE-20261112T091253Z-5a2e96b8`. Its accepted qualification receipt SHA is `57fe829b2ae83fc16a962710b8a1ef8e4635ebf8fd4326714ed24c69c4a0f903`; its E1 intent self-hash is `9dfe5c1c4568ed7fbc4bb4260d47da4e518b1a163811fb88f2a9f1bff55c304e`.

The previous V2 requalifier returned exit code 2 before FFmpeg composition. `E4C_DRILL_V2_REQUALIFICATION_FAILURE.json` and `runner_failure.json` recorded:

`existing E1 shared service rejected the Drill intent: E1 output root appeared after preparation; overwrite is forbidden`

The diagnostic archive supplied by the operator is `C11E_E4C_V2_REQUALIFIER_DIAGNOSTICS_E4C-CLI-COMPOSITION-V2-20261113T064622Z-c4d2534d.zip`, SHA-256 `b70882a4d34e98563697fd06706e5de772174a10671f36b72030e1361f6bd674`.

## Root cause

The immutable E1 intent says:

- `output.created=false`
- `output.overwrite_policy=DENY_EXISTING`
- `output.planned_root_exists=false`
- `output.planned_root=artifacts/production/c11e/E4C-CLI-SMOKE-20261112T091253Z-5a2e96b8`

Those fields describe the state **at E1 preparation time**. The accepted CLI smoke subsequently materialized that exact planned output directory, including its media and execution receipt. The V2 requalifier loaded the historic intent and then called `consumer.build_composition_plan(intent, root)`. That ordinary consumer path calls `c11e_production_service.validate_c11e_production_intent()`, which correctly treats an already-existing planned root as an overwrite hazard for a new E1 execution. The requalifier was not starting a new E1 run; it was reading/recomposing a previously accepted evidence set. Reapplying the fresh-dispatch guard to this historical receipt was therefore a temporal contract mismatch.

No FFmpeg composition began; the diagnostic flags confirm no new native capture, no Godot, no C11-C launcher, no family-music generation, no production dispatch and no release authority. The original smoke media and receipts remain intact.

## Required correction

1. Keep `c11e_production_service.py` and its `DENY_EXISTING` check byte-for-byte unchanged.
2. Keep ordinary `build_composition_plan()` routed through `_validate_intent()` and the shared E1 service. The live/fresh E1 path remains strict.
3. Add a separate D-only `build_composition_plan_for_existing_media(intent, project_root, accepted_e1_receipt, expected_existing_output_root)` path.
4. This historical path validates: schema 1.3 and intent self-hash; accepted shared execution receipt schema/status and request identity; E1 preparation-only receipt validity and exact intent hash; E1 GUI/CLI parity; no dispatch/release/C11-C mutation; immutable original output snapshot (`created=false`, `DENY_EXISTING`, `planned_root_exists=false`); path equality across planned root, receipt evidence root and requested evidence root; on-disk receipt/intent byte-object equality; D9 preparation self-hash and not-dispatchable flags; and exact equality of four 91-row pin inventories (intent, receipt pre-execution, pre-renderer and post-execution).
5. The requalifier still compares current 91 source pins against the accepted receipt before composition and after composition. No new source capture or audio generation is permitted.
6. The PowerShell wrapper must preserve logs and partial outputs and automatically produce a diagnostic ZIP on any caught runner failure or timeout. It must rethrow the original error and must not suppress the original failure if ZIP assembly itself fails.

## R2 implementation scope

Four hash-guarded file replacements: D visual composition consumer, its tests, existing-media V2 requalifier, and PowerShell wrapper. Thirteen versioned documents/prompts are added. Installer invariants: source pins 21/21, frozen C11-C baseline unchanged, 4 REPLACE + 13 ADD_ONLY, 17 total operations, 19 manifest package files; staged Python compile 3/3; staged Qt-offscreen suite 27/27; PowerShell AST 2/2; built-in File.Replace forward/rollback; immediate pre-write recheck; full postimage and post-pin audit. The operator decision record remains immutable and is not copied or modified.

Architect-side checks before release: real historical receipt/intent validated against all 91 pins; seven focused correction cases passed (six historical-intent validations plus the ordinary E1 strict-path regression); static `py_compile` 3/3 passed. These do not substitute for the operator's Windows PowerShell/PySide6 installer runtime checks.

## Recovery and next action

- Preserve the old failed log root and diagnostic ZIP; do not rerun the old requalifier build.
- Install the R2 ZIP once into a new Downloads package folder. Stop on any failed gate and preserve installer receipt/journal/failure.
- Independently audit 17 destination postimages and 21 source pins.
- Only after audit PASS, run the corrected wrapper once against the original CLI smoke evidence directory.
- On failure, the wrapper should emit `V2_REQUALIFIER_DIAGNOSTICS_<runId>.zip` under the run's `artifacts/tests/c11e/e4c_drill_v2_requalification/<runId>/` log directory, print its SHA-256, and preserve the original `runner_failure.json`.
- On technical PASS, inspect seven review frames and A/B/C outputs, then obtain explicit operator visual/audio acceptance. This is still only selector `tracking/tier-1`, row 1/20 after that acceptance.

## Governance

C11-C 2.19.12 and its frozen manifest remain immutable. E1 remains `PREPARE_ONLY`; `family_adapter.status=NOT_CONNECTED_E1`; no dispatch; `release_authority=NONE`. `GIT_CHECKS=SKIPPED`; `COMMITS=OPERATOR_MANAGED`. No pip changes, no external coding agent, no repeat of accepted smoke or music generation.
