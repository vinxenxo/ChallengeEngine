# C11-D Loop/Drill Editorial Field-Window Unified Review Integration Overlay V1

This is a minimal overlay for a repository that already has the Loop/Drill Editorial Field-Window Proposal V1, Challenge Sample-Selection Proposal V1, Coordinate/Sample Composition Proposal V1, and their current unified-review integrations applied.

## Included files

- `definitions/c11d/production/D_RENDERER_UNIFIED_CONTENT_REVIEW_V1.json` — pins the Loop/Drill proposal and keeps all relevant approvals false.
- `definitions/c11d/production/D_RENDERER_UNIFIED_CONTENT_REVIEW_SCHEMA_V1.json` — requires the new cross-artifact check and constrains proposal-only Loop/Drill review metadata.
- `tools/c11d/d9/d_renderer_unified_content_review.py` — validates the proposal contract, links its fixtures to materialized Loop/Drill identity/timing, and preserves null evaluated windows when raw editorial strings are absent.
- `tools/c11d/d9/test_d_renderer_unified_content_review.py` — checks the joined metadata, parity, and non-promotion/non-fabrication controls.
- `tools/c11d/d9/run_d_renderer_unified_content_review.py` — advertises 13/13 cross-artifact checks and reports the Loop/Drill proposal state.
- `docs/current/d/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_CHECKPOINT.md` — updates the proposal's next-step note.
- `docs/current/d/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_UNIFIED_REVIEW_INTEGRATION_CHECKPOINT.md` — records the new integration and its limits.

## Apply

From the repository root, verify the ZIP SHA-256, then extract it once over the existing C11-D working tree. It must be applied **after** the Loop/Drill Editorial Field-Window Proposal V1.

```powershell
Get-FileHash "$env:USERPROFILE\Downloads\C11D_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_UNIFIED_REVIEW_INTEGRATION_OVERLAY_V1.zip" -Algorithm SHA256
Expand-Archive `
  -LiteralPath "$env:USERPROFILE\Downloads\C11D_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_UNIFIED_REVIEW_INTEGRATION_OVERLAY_V1.zip" `
  -DestinationPath "." `
  -Force

python -m py_compile `
  .\tools\c11d\d9\d_renderer_unified_content_review.py `
  .\tools\c11d\d9\test_d_renderer_unified_content_review.py `
  .\tools\c11d\d9\run_d_renderer_unified_content_review.py

python .\tools\c11d\d9\test_d_renderer_loop_drill_editorial_field_windows.py
python .\tools\c11d\d9\test_d_renderer_unified_content_review.py
python .\tools\c11d\d9\run_d_renderer_unified_content_review.py --godot godot
```

Then run the lifecycle, baseline-candidate and aggregate regressions already used by the operator:

```powershell
python .\tools\c11d\d9\test_cross_suite_lifecycle.py
python .\tools\c11d\baseline_candidate\test_d_baseline_candidate.py
python -u .\c11c-suite\self_test.py
```

## Expected review state

The integrated run should report `cross_artifact=13/13`, `source_lineage=16/16`, `loop_drill_editorial=FULL_SPAN_NONEMPTY_FIELDS_PROPOSAL_ONLY`, `unresolved_gates=8`, and `review=CONSISTENT_NOT_VIDEO_READY`. Per-field `visibility_windows` remain null in the joined report because raw Loop/Drill editorial strings are not exposed by the current runtime summary. The report must not fabricate evaluated windows.

The two Loop/Drill gates are now named `VISUAL_LOOP_EDITORIAL_FIELD_MAPPING_NOT_APPROVED` and `VISUAL_DRILL_EDITORIAL_FIELD_MAPPING_NOT_APPROVED`. This overlay does **not** approve the proposal, enable the renderer, create media, write persistent reports or payloads, change C11-C simulation truth, authorize D4.8, grant release authority, or make the D baseline freeze-eligible.

## Preparation validation

In a reconstructed full-project tree, syntax checks and focused tests passed: Loop/Drill proposal 22/22; coordinate/sample composition 18/18; sample-selection negative controls 22/22; coordinate projection 18/18; delivery timebase negative controls 42/42; timeline negative controls 55/55; unified review unit tests 20/20 with cross-checks 13/13 and source lineage 16/16. No Godot executable was run in the preparation environment after this overlay; the Windows integrated harness result remains required.
