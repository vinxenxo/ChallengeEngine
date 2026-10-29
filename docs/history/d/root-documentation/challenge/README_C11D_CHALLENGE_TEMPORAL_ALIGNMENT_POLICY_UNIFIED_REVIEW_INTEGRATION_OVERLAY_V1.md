# C11-D Challenge Temporal Alignment — Unified Review Integration Overlay V1

## SHA-256

Compute this against the delivered ZIP before extraction. The final archive digest will be supplied alongside the download.

## Scope

This overlay integrates the existing `D_RENDERER_CHALLENGE_TEMPORAL_ALIGNMENT_POLICY_PROPOSAL_V1.json` into the current unified in-memory review. It modifies the unified contract, schema, review validator and test file; updates the temporal proposal checkpoint; and adds an integration checkpoint plus a history record.

It does **not** add or change any Godot harness, renderer dispatch, video output, payload persistence, or production route. It does not approve the temporal policy. All prior proposal contracts must already be present in the checkout.

## Expected focused result

- Unified contract tests: 23/23.
- `cross_artifact_checks`: 14/14.
- Source lineage: 17/17.
- Canonical unresolved gates: 8.
- `review=CONSISTENT_NOT_VIDEO_READY`, renderer OFF, no media, D4.8 BLOCKED, release authority NONE.

## Windows application

Run from the repository root:

```powershell
Get-FileHash "$env:USERPROFILE\Downloads\C11D_CHALLENGE_TEMPORAL_ALIGNMENT_POLICY_UNIFIED_REVIEW_INTEGRATION_OVERLAY_V1.zip" -Algorithm SHA256
Expand-Archive `
  -LiteralPath "$env:USERPROFILE\Downloads\C11D_CHALLENGE_TEMPORAL_ALIGNMENT_POLICY_UNIFIED_REVIEW_INTEGRATION_OVERLAY_V1.zip" `
  -DestinationPath "." `
  -Force

python -m py_compile `
  .	ools\c11d\d9\d_renderer_unified_content_review.py `
  .	ools\c11d\d9	est_d_renderer_unified_content_review.py `
  .	ools\c11d\d9
un_d_renderer_unified_content_review.py

python .	ools\c11d\d9	est_d_renderer_challenge_temporal_alignment_policy.py
python .	ools\c11d\d9	est_d_renderer_unified_content_review.py
python .	ools\c11d\d9
un_d_renderer_unified_content_review.py --godot godot
python .	ools\c11d\d9	est_cross_suite_lifecycle.py
python .	ools\c11daseline_candidate	est_d_baseline_candidate.py
python -u .\c11c-suite\self_test.py
```

## Approval boundary

Integration is evidence of consistency, not approval. Do not change policy states, close unresolved gates, unfreeze C11-C, authorize D4.8, enable the renderer or create video from this overlay.
