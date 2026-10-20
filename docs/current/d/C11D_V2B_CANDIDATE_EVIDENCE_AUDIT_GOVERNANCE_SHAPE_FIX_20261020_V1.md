# C11-D V2-B Candidate Evidence Auditor — Governance Shape Fix (2026-10-20, V1)

## Diagnosis

The first candidate evidence audit stopped fail-closed with `AuditError:governance lock changed: approved_bindings`. This was an auditor defect, not a runtime failure. The canonical V2-B runtime report carries `approved_bindings` and `approved_custom_data_bindings` at the report root. The nested `governance_locks` map intentionally contains the lock fields from the runtime contract and does not contain those two counters.

The V1 auditor incorrectly placed both binding counters in the expected nested map, while also validating them correctly at the report root. Its synthetic test fixture repeated the same schema mistake, so the static tests did not detect the divergence.

## Correction

- Keep root-level approved-binding checks at zero.
- Validate the nested governance map against the exact canonical runtime governance object, including `visual_seed_sensitivity=NOT_TESTED_UNTIL_V2B_RUNTIME_ACCEPTED`; do not include binding counters there.
- Update the fixture to match the canonical runtime report and add a regression test rejecting unexpected nested binding-count fields.
- Re-run the focused auditor suite before retrying the audit. No Godot process is rerun.

## Preconditions / immutable evidence

- V2-B runtime report SHA-256: `f7a1522695cbd6d3f3681d3f266b625e3062d5141c32cddbb4532bcb466e0446`.
- Runtime implementation receipt SHA-256: `e64cfd259914c471d03e8578b955140ad487b04694c5f682834517d823fcbfc4`.
- Frozen C11-C manifest SHA-256 remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- The corrected static suite contains 39 tests; a successful run must return process exit code 0 and print `C11D_V2B_CANDIDATE_EVIDENCE_AUDIT_TESTS_PASS=39/39`.

## Governance

This repair only corrects the read-only evidence auditor. It does not rerun Godot, modify the accepted runtime report, approve semantic bindings, materialize payload, create media, enable renderer, or change release/baseline authority. Candidate fields remain `OBSERVED_NOT_APPROVED`.
