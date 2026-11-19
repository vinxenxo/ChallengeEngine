# C11-E E6 Option C Native Qt Probe V2.4 — exact A3 diagnostic field contract

Date: 2026-11-19  
Mode: `ADD_ONLY`; no existing file or receipt is replaced.

## Confirmed V2.3 incident

V2.3 installed successfully (10/10). Its 13 focused regressions passed. The V2.3 runner then loaded the A3 V3 adjudicator by pinned absolute path and stopped at `A3_LEGACY_DIAGNOSTIC_EXPECTED_ACTUAL_MISMATCH:old`. No QImage tests ran. The V2.3 receipt remains evidence of a blocked preflight and is not modified.

## Root cause proven from original producer

The exact source is the Smoke18 overlay's `diagnose_c11e_e6_loop_policy_v2_receipt.py`, SHA-256 `90375a6c21550d67e6aa1f374d5e5c8dcd7c06b630c51b34ad83313fbb7b2fc2`. Its `validate_a3_objects()` output maps fields as follows:

| Diagnostic field | Actual source / meaning | Required value |
|---|---|---|
| `old_pointer_expected` | Expected SHA-256 of the whole historical review manifest | `2075da9c33c689861a68d3bd8fb19b7ed593c6e76010ab200880746aa6d1a470` |
| `old_pointer_actual` | Value found at historical `/source_lineage/6/sha256` | `50655c82521a353f1db6920f4d099cad92452ae369251f9fbde45cbaee4e8c53` |
| `bridge_old_pointer_value` | Bridge's recorded old pointer value | Same old pointer value above |
| `new_pointer_expected` | SHA-256 of pinned D9.8 editorial model file | `dabb458fc2215156ddb5ebea7e8ebec811098886ce2858733ba9fb13f6075ccb` |
| `new_pointer_actual` | Value found at current `/source_lineage/6/sha256` | Same D9.8 model SHA above |
| `bridge_new_pointer_value` | Bridge's recorded new pointer value | Same new pointer value above |
| `pointer_target_path` | Bridge's model target path | `definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json` |

The two old values are intentionally different because they are different hash domains. The bug in V2.2/V2.3 was asserting `old_pointer_expected == old_pointer_actual`. This is not a reason to weaken verification: each field must match its own source exactly.

## V2.4 correction

- Adds a new adjudicator V4 and new runner under `tools/c11d/d9/c11e_e6_option_c_native_qt_probe_v2_4/`.
- Embeds and SHA-pins the exact original diagnostic generator source under `support/reference/`; the adjudicator verifies that source pin before interpreting the diagnostic.
- Validates all six identity rows (bridge, archive, current manifest, D9.8 model, A3 proposal, operator decision) against exact path/SHA pairs and active files.
- Validates each legacy field independently against the source-derived mapping above; no equality assumption across different domains.
- Rechecks whole-file preimage/postimage SHA-256 and byte counts, bridge values, D9.8 file pin, exact one-pointer structural reconstruction, and the specialized Loop V2 receipt counts/status.
- Reuses the already-installed V2 QImage implementation and its existing 37-test suite by exact path. It does not replace or reinstall that payload.

## Local regression coverage

Thirteen new A3 tests exercise the exact original field shape, each field's rejection path, identity cardinality, one-pointer reconstruction, count invariants and generator provenance. Four direct-file-loader tests continue to cover exact path loading, unrelated `support` namespace collision, SHA mismatch and missing file. Total: 17 focused tests.

## Scope and governance

V2.4 is add-only. The V2.1, V2.2 and V2.3 files/receipts are retained unchanged. The runner writes under `artifacts/tests/c11e/e6_option_c_native_qt_probe_v2_4/`. It does not invoke Godot, FFmpeg, FFprobe, audio generation, mux, renderer, production dispatch or BatchId. `e6_accepted=0`, `release_authority=NONE`; C11-C and D4.8 V2 remain unchanged and pinned. A successful run can prove only `PASS_QIMAGE_STAGE_BENCHMARKED_NOT_END_TO_END`.
