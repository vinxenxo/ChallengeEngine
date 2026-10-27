# C11-D — Request→Payload Instance Integration Checkpoint V2

**Date:** 2026-10-27  
**State:** `BOUNDED_V2_IN_MEMORY_INTEGRATION_IMPLEMENTED_RUNTIME_REVIEW_PENDING`

**Cumulative phase ledger:** `docs/current/d/C11D_ENGINEERING_PHASE_LEDGER_20261027_V1.md` (reuse prior accepted evidence unless its pinned sources change).

## Previous gate closed

The operator ran the new proposal test in the active Windows checkout and supplied the following result:

- `PROPOSAL_TEST_EXIT_CODE=0`
- `source_pins=54/54`
- `io_gap_groups=10/10`
- `complete=0 partial=6 blocked=4`
- `schema_engine=DRAFT2020_12`
- `schema_negatives=6/6`
- `REQUEST_PAYLOAD_INTEGRATION_PROPOSAL_VALIDATION=PASS`
- frozen C11-C manifest unchanged, `renderer=OFF`, `media_created=false`, `candidate_input_admissible=false`.

This result is operator-reported Windows evidence. The proposal contract SHA-256 is `3e65d03532417502ff9a957bc9a6efca01a974641aeaa1b9b00a11b1bdad4e81`, its schema is `f75a98b9e666a2d668bdbc1f5c5605fb12851b704e0f5ee9df0bd798b0385cba`, its focused test is `965619065a41a609c84a8dabc7302e4d87c4e9e157b0966ef0ba1990faeb3280`. Do not rerun that proposal test unless its source pins change.

## Decision and bounded implementation

Separate decision record: `D_RENDERER_REQUEST_PAYLOAD_INSTANCE_INTEGRATION_DECISION_V1.md` (JSON companion under `definitions/c11d/production/`). It accepts implementation and runtime review only for the three fixed fixtures already present in materialization V1: Challenge CHALLENGE_004, Loop harmonic_membrane, Drill tracking/tier-2. It does not authorize candidate input or production.

The V2 interface imports and reuses the existing canonical D9.9 planner, dynamic binder V1, fixed payload materialization-binding V1 and editorial sidecar V1. It does not create another request binder. The V2 receipt checks identical request IDs/hashes, selector identity, gameplay/music seeds, variation/profile identities, plan/bridge/adapter/source-binding lineage, dynamic request-specific manifest and digest, and canonical editorial sidecar hashes.

**Important digest distinction:** the dynamic binder payload hash and legacy fixed-fixture `payload_instance_sha256` describe different versioned payload serializations. V2 records each in a separate field and makes no cross-contract digest-equivalence claim. The test must not silently compare them as though they were interchangeable. `payload_digest_equivalence_proven=false` remains explicit.

## Next Windows execution

1. Apply this add-only overlay using its supplied SHA-256 and verify all listed file hashes; do not overwrite any existing destination.
2. Run the focused unit test `python -B .\tools\c11d\d9\test_d_renderer_request_scoped_payload_materialization_binding_v2.py`.
3. Only if the focused test passes, run `python -B .\tools\c11d\d9\d_renderer_request_scoped_payload_materialization_binding_v2.py --godot $env:C11D_GODOT_EXECUTABLE --timeout 180` using Godot 4.7.1 Mono. Capture stdout and stderr separately. This one runner invokes the existing materialization, dynamic binder and sidecar interfaces and emits an integration receipt to stdout only. It writes no JSON receipt files or media.
4. If a runtime join fails, stop on its first reason. Do not loosen equality checks, refresh pins, or rerun the broad suite to get a green console. Capture the failing comparison and diagnose only that interface edge.
5. After a clean V2 runtime receipt, refresh the I/O gap/identity reports once for the changed source tree. Do not claim any I/O group is complete from the V2 PASS alone.

## Preparation-sandbox unit test (not active Windows acceptance)

The staged V2 focused Python unit test was run in the isolated preparation sandbox after assembly: `Ran 10 tests in 7.933s`, `OK`. This includes the 60-source-pin contract check and the identity/schema negative cases. It is only a preparation sanity check. Run the same focused test once in the active Windows checkout after applying the overlay; no Windows V2 result or Godot V2 runtime receipt has yet been reported.

## Expected bounded receipt

`fixtures=3/3`, `canonical_request_joins=3/3`, `payload_manifest_digests=3/3`, `editorial_sidecar_joins=3/3`, `sidecar_fields=14/14`, `visual_payload_consumed=0/14`, `payload_digest_equivalence=NOT_CLAIMED`, source pins `60/60`.

These are expected assertions, not a runtime PASS claim. Runtime review remains pending until the operator supplies actual stdout/exit code.

## Unchanged locks

C11-C 2.19.12 and its frozen manifest remain immutable at `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` (796,318 bytes). `renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; `approved_bindings=0`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14/D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`. All spatial/temporal/audio policies stay unapproved, no master seed, no payload persistence, no renderer input, no dispatch and no media.
