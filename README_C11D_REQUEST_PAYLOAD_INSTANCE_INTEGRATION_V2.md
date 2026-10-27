# C11-D Request→Payload Instance Integration V2 — add-only overlay R3 with cumulative phase ledger

## Scope

This increment records a distinct decision and adds the V2 successor to the existing materialization-binding interface for exactly three previously contracted fixed review fixtures. It imports the existing D request planner, dynamic binder, materialization V1 and editorial carrier V1; it does not add a second request binder or change any existing file.

## Decision and implementation

- Decision JSON: `definitions/c11d/production/D_RENDERER_REQUEST_PAYLOAD_INSTANCE_INTEGRATION_DECISION_V1.json`
- Decision checkpoint: `docs/current/d/D_RENDERER_REQUEST_PAYLOAD_INSTANCE_INTEGRATION_DECISION_V1.md`
- V2 contract: `definitions/c11d/production/D_RENDERER_REQUEST_SCOPED_PAYLOAD_MATERIALIZATION_BINDING_V2.json`
- V2 output schema: `definitions/c11d/production/D_RENDERER_REQUEST_SCOPED_PAYLOAD_MATERIALIZATION_BINDING_SCHEMA_V2.json`
- Runner: `tools/c11d/d9/d_renderer_request_scoped_payload_materialization_binding_v2.py`
- Focused unit test: `tools/c11d/d9/test_d_renderer_request_scoped_payload_materialization_binding_v2.py`
- Checkpoint: `docs/current/d/D_RENDERER_REQUEST_PAYLOAD_INSTANCE_INTEGRATION_CHECKPOINT_V2.md`

## Critical digest rule

Dynamic binder payload digest and the V1 fixture payload-instance digest belong to different versioned serializations. The V2 receipt carries them separately and explicitly does not claim digest equivalence. All request identity, selected fields, seed/profile, lineage and editorial sidecar hash joins must be exact; any mismatch fails closed.

## Cumulative documentation of approved phases

The overlay now also adds `docs/current/d/C11D_ENGINEERING_PHASE_LEDGER_20261027_V1.md`. It records all phases in this workstream that are already closed, the exact operator-reported results and hashes, the sandbox-only V2 unit-test result, current blockers, and a no-retest policy for accepted gates whose source pins did not change. The V2 checkpoint links back to that ledger. Do not treat the sandbox PASS as Windows or Godot acceptance.

## Apply and verify

Validate this ZIP SHA-256 before extraction. All nine repository target files are new, including the phase ledger; stop if any target exists. Do not extract wholesale over the repository. Verify each staged SHA-256 before copying and after copying; recheck the frozen C11-C manifest SHA and byte count.

Then run the focused unit test:

```powershell
python -B .\tools\c11d\d9\test_d_renderer_request_scoped_payload_materialization_binding_v2.py
if ($LASTEXITCODE -ne 0) { throw 'V2 request-payload integration unit test failed.' }
```

Only after it passes, run the bounded Godot receipt runner:

```powershell
python -B .\tools\c11d\d9\d_renderer_request_scoped_payload_materialization_binding_v2.py --godot $env:C11D_GODOT_EXECUTABLE --timeout 180
if ($LASTEXITCODE -ne 0) { throw 'V2 request-payload integration runtime receipt failed.' }
```

Expected runtime summary (not yet an observed result): `fixtures=3/3`, `canonical_request_joins=3/3`, `payload_manifest_digests=3/3`, `editorial_sidecar_joins=3/3`, `sidecar_fields=14/14`, `visual_payload_consumed=0/14`, `payload_digest_equivalence=NOT_CLAIMED`, `source_pins=60/60`.

## Governance

`renderer=OFF`, `media_created=false`, `payload_materialized=false`, `candidate_input_admissible=false`, `D4.8=BLOCKED`, `release_authority=NONE`. C11-C remains immutable. No payload/receipt files, renderer input, dispatch, pixels, media, policy approvals, baseline freeze or promotion.
