# C11-D D9.10 Post-Runtime Integration Fix Overlay V2

Date: 2026-10-09

## Purpose

The operator-confirmed direct offscreen Qt runtime `D910_QT_GUI_RUNTIME_FIX_01` passes 3/3. The combined acceptance `D910_QT_ACCEPTANCE_FIX_01` returned 5/7 because the baseline candidate audit found an out-of-scope modification of `docs/current/07_ROADMAP.md`, and aggregate Suite step 13 still asserted `negative=12/12` while the strengthened D9.13 lifecycle emits `negative=14/14` plus `persisted_parity_regression=4/4`.

This overlay (a) synchronizes the aggregate assertion to the stronger test contract; (b) restores `docs/current/07_ROADMAP.md` to its exact immutable manifest-recorded bytes; and (c) updates current handover/checkpoint/changelog/history. It does not modify the frozen manifest, suppress candidate checks, weaken negative coverage, or change governance semantics.

## Identity checks

- `release/C11C_FREEZE_PACKAGE_MANIFEST.json`: SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` (unchanged).
- `docs/current/07_ROADMAP.md`: SHA-256 `5e847ead237c614d1618e0a012f823e92ef95068441e8ce4872a225beee5d989` (matches the exact frozen-manifest entry).
- The roadmap restore is required because the candidate audit correctly rejects source drift outside approved D extension roots.

## Files

- `c11c-suite/self_test.py`
- `docs/current/07_ROADMAP.md`
- `docs/current/d/D9.10_QT_GUI_RUNTIME_ACCEPTANCE_CHECKPOINT.md`
- `docs/current/d/D9_SUITE_INTEGRATION_CHANGELOG.md`
- `docs/current/d/MASTER_HANDOVER_C11D_CURRENT.md`
- `docs/current/d/START_PROMPT_C11D_CURRENT.md`
- `docs/history/c11d/d9/D9.10_QT_GUI_RUNTIME_PARITY_SCHEMA_FIX_20261009.md`

## Application

From `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`, check this ZIP's SHA-256, then extract it over the repository root. Immediately verify the two hashes listed above before tests. ZIP contains only the modified aggregate assertion, canonical roadmap bytes and current/history documentation.

## Fresh Windows verification

```powershell
python .\tools\c11d\d9\test_cross_suite_lifecycle.py --parity-contract-only
python .\tools\c11d\d9\test_cross_suite_lifecycle.py
python .\tools\c11d\d9\test_d910_gui_runtime_contract.py
python .\tools\c11d\d9\test_editorial_render_bridge.py
python .\c11c-suite\c11c-producer\test_producer_gui_contract.py
python .\tools\c11d\d9\test_d910_gui_runtime_acceptance.py --run-id D910_QT_GUI_RUNTIME_FIX_02
python .\tools\c11d\d9\capture_d910_acceptance.py --run-id D910_QT_ACCEPTANCE_FIX_02 --include-qt-gui-runtime --include-aggregate
python .\tools\c11d\baseline_candidate\test_d_baseline_candidate.py
python -u .\c11c-suite\self_test.py
```

Expected target, not claimed result: direct runtime 3/3; combined acceptance 7/7; aggregate 22/22; candidate preflight PASS with `freeze_eligible=false` and five existing blockers retained. Any residual failure must remain visible and be diagnosed.

## Governance

C11-C 2.19.12 and its frozen manifest remain immutable. D9.10 adapter remains `PREPARE_ONLY`; renderer OFF; media false; D4.8 `BLOCKED`; `release_authority=NONE`; D9 OPEN; D10 BLOCKED. `operator_gui_runtime_observed=false` remains truthful for offscreen testing and must not be reinterpreted as human observation. The definitive GUI remains deferred until the complete D baseline is accepted and frozen.
