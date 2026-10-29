# C11-D GUI Editorial View Model Overlay V1

## Purpose

Adds a D-owned, in-memory composition seam between the existing GUI selection/state, editorial draft lifecycle, and the shared canonical D9.8/D9.9/D9.10 context. It is designed for the future GUI to consume without creating a second editorial resolver or a second backend.

## Files added (7)

- `definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_EDITORIAL_VIEW_MODEL_CONTRACT_V1.json`
- `definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_EDITORIAL_VIEW_MODEL_CONTRACT_SCHEMA_V1.json`
- `definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_EDITORIAL_VIEW_MODEL_SCHEMA_V1.json`
- `tools/c11d/d9/shared_production_context_gui_editorial_view_model.py`
- `tools/c11d/d9/test_shared_production_context_gui_editorial_view_model.py`
- `docs/current/d/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_EDITORIAL_VIEW_MODEL_CHECKPOINT_V1.md`
- `README_C11D_GUI_EDITORIAL_VIEW_MODEL_OVERLAY_V1.md`

## What it guarantees

- Source-pinned lineage of 45 inputs, led by the exact frozen C11-C manifest SHA-256.
- GUI and editorial-draft content/family/selector/mode must agree; incomplete or stale-bound drafts are rejected.
- Existing dynamic catalog determines family/selector options and mode compatibility.
- Draft profile and overrides are authoritative for edited editorial values. Canonical D9.8 resolution remains the authority for effective values.
- Existing GUI adapter context must be exactly equal to the direct shared façade context. D9.8 draft preview values must equal the canonical bound editorial values.
- View-model output is schema-validated and sealed with a canonical SHA-256. Input objects are not mutated.
- Challenges, Visual Loops, and Visual Drills are covered. Existing Loop/Drill `PRODUCTION` mode restrictions are preserved; Longform is not added.

## Apply and verify

Download this ZIP to the user's `Downloads` directory. Apply it from the repo root with the inline PowerShell block provided in the conversation. The block must verify the ZIP SHA-256, exact frozen-manifest SHA-256, seven expected new-file hashes, and destination absence before copying. It must append continuity notes to the current Master Handover, Start Prompt, and renderer baseline preparation plan while preserving their existing bytes. Do not hash-gate those mutable documents to an old fixed SHA and do not replace them from a packaged snapshot.

Windows acceptance commands:

```powershell
python -B .\tools\c11d\d9\test_shared_production_context_gui_editorial_view_model.py
python -B .\tools\c11d\d9\shared_production_context_gui_editorial_view_model.py --audit-only
```

After those pass, run the parent GUI/catalog/state/facade/adapter/draft/binding tests, cross-suite lifecycle, baseline-candidate preflight, `tests\run_all.py`, and the C11-C Suite. Record actual Windows output; preparation-workspace results are not operator acceptance.

## Not a renderer or approval

The view model returns `PREPARED_SHARED_GUI_CONTEXT_NOT_RENDERER_INPUT`. It does not update GUI widgets, persist the state, emit renderer-native input, dispatch, execute production, create media, approve a baseline, or grant release authority.

## Governance

Frozen C11-C manifest remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; `D9.10=PREPARE_ONLY`; `D4.8=BLOCKED`; renderer OFF; `media_created=false`; `release_authority=NONE`; D9.17 NO-GO; D10 blocked. Next after Windows acceptance: read-only D renderer I/O contract gap audit, not another editorial binding layer.
