# C11-D V2-B Candidate Evidence Audit — Runtime Receipt Schema ID Fix (2026-10-20, V1)

## Defect

The candidate evidence auditor rejected `CHALLENGE_001/BASELINE_R1` with `receipt identity mismatch` before any candidate aggregation. This was an auditor contract literal mismatch, not a runtime receipt failure.

The real runtime producer (`tools/c11d/d9/d_renderer_challenge_visual_payload_v2b_safe_projection_runtime.py` and its Godot harness) emits the strict receipt schema ID `C11D-CHALLENGE-VISUAL-PAYLOAD-V2B-SAFE-PROJECTION-RUNTIME-RECEIPT-V1`. The auditor incorrectly compared it against `C11D-V2B-SAFE-PROJECTION-RUNTIME-RECEIPT-V1`. The separate static implementation receipt correctly uses `C11D-V2B-RUNTIME-IMPLEMENTATION-TEST-RECEIPT-V1`; these identifiers must not be conflated.

## Fix

- Added explicit `RUNTIME_RECEIPT_ID` constant matching the runtime contract/schema/harness.
- Updated the runtime receipt validator to use that constant.
- Updated the audit fixture to model the actual runtime receipt schema.
- Added a negative regression test proving the former wrong schema ID is rejected.
- Expected static suite: `40/40`.

## Scope and governance

This patch only replaces the auditor and its unit test and adds this checkpoint. It does not change the runtime runner, any runtime receipts/report, the 45 planner invocations, the 45 Godot processes, the challenge sources, or the V2-B design/runtime contracts. Do not rerun Godot to address this auditor-only schema defect.

Keep: `renderer=OFF`, `payload_materialized=false`, `media_created=false`, `candidate_input_admissible=false`, `approved_bindings=0`, `approved_custom_data_bindings=0`, `D9.10=PREPARE_ONLY`, `D4.8=BLOCKED`, `D9.17=BLOCKED_NO_GO`, `D10=BLOCKED_FOR_PROMOTION`, `baseline_approval=MISSING`, `freeze_eligible=false`, and `release_authority=NONE`. Every candidate remains `OBSERVED_NOT_APPROVED`; no raw `custom_data` values may be included.

## Operator sequence

1. Apply this preconditioned overlay only if the currently installed audit/test hashes match the manifest before-hashes.
2. Run the focused static suite; require exit code 0 and marker `C11D_V2B_CANDIDATE_EVIDENCE_AUDIT_TESTS_PASS=40/40`.
3. Rerun only the candidate-evidence audit against the existing accepted runtime report and implementation receipt. Do not rerun the runtime matrix.
4. Validate the resulting audit JSON and hashes before use as semantic-review evidence.
