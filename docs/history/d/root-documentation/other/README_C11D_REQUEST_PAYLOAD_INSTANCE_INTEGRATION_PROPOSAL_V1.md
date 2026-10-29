# C11-D Request → Payload Instance Integration Proposal V1 (add-only)

This package adds a proposal contract, strict JSON Schema (Draft 2020-12), a D-only checkpoint, and a read-only validation test. It does not modify any existing file, implement integration, emit renderer input or create media.

## Contents

- `definitions/c11d/production/D_RENDERER_CANDIDATE_REQUEST_PAYLOAD_INSTANCE_INTEGRATION_PROPOSAL_V1.json`
- `definitions/c11d/production/D_RENDERER_CANDIDATE_REQUEST_PAYLOAD_INSTANCE_INTEGRATION_PROPOSAL_SCHEMA_V1.json`
- `docs/current/d/D_RENDERER_CANDIDATE_REQUEST_PAYLOAD_INSTANCE_INTEGRATION_PROPOSAL_CHECKPOINT_V1.md`
- `tools/c11d/d9/test_d_renderer_candidate_request_payload_instance_integration_proposal.py`

The contract pins the current 54-file I/O audit source set and records the operator-supplied identity fingerprint/reports as observations. The test is read-only. It checks the frozen C11-C manifest SHA/byte count, renderer policy docket, I/O audit contract and its 54 live source pins, strict contract state and governance locks. If `jsonschema` is installed it performs Draft 2020-12 instance validation and schema-negative mutations; otherwise it reports a structural-only schema inspection and does not claim full schema-engine validation.

Apply only after validating the ZIP SHA-256. Never extract this ZIP wholesale over the checkout. Check that all five destination paths are absent before adding; stop on any collision. After applying, run the separate test command from the repository root:

```powershell
python -B .\tools\c11d\d9\test_d_renderer_candidate_request_payload_instance_integration_proposal.py
if ($LASTEXITCODE -ne 0) { throw 'Request-payload integration proposal audit failed.' }
```

All locks remain unchanged: renderer OFF, media false, candidate input inadmissible, D4.8 blocked, release authority NONE, C11-C immutable.
