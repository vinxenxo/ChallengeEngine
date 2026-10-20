# C11-D V2-B Runtime Acceptance & Candidate Evidence Checkpoint — V1 (2026-10-20)

## Status

**V2-B safe source-state projection runtime: PASS, scope-limited.** This acceptance covers only the in-memory source-frame observation harness and seed sensitivity matrix. It is not payload, renderer, media, candidate-input, binding, or promotion acceptance.

## Operator-confirmed Windows evidence

- Static implementation tests: `198/198`.
- Static implementation receipt: `C:\Users\vinxe\AppData\Local\Temp\C11DV2BTEST_5666cc2d00\implementation_test_receipt.json`; SHA-256 `e64cfd259914c471d03e8578b955140ad487b04694c5f682834517d823fcbfc4`.
- Static stdout SHA-256 `02cf98c041d0e3c40282164500df99e16f0b058eb9d899081ada30829bd1cd43`; stderr SHA-256 `c3c6847bb978b4cf9804af7069222f6443d686b6f05a37c3dc2bc73d4033a0cd`.
- Runtime report: `C:\Users\vinxe\AppData\Local\Temp\C11DV2BRUNTIME_1c9e26c59a594755a1351bc8222d5ed1\report.json`; SHA-256 `f7a1522695cbd6d3f3681d3f266b625e3062d5141c32cddbb4532bcb466e0446`.
- Runtime runner process exit code `0`; stdout SHA-256 `25a1ac41d160c672b7b13555fcd243fb289f2091807c2c960c31042088d5deac`; stderr SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- Runtime result `PASS_SAFE_PROJECTION_SEED_SENSITIVITY`; canonical planner calls `45/45`; independent Godot processes `45/45`; accepted selectors `9/9`.
- Runner-reported Godot: `4.7.1.stable.mono.official.a13da4feb`.
- Reconciliation block: `C11D_V2B_RUNTIME_EVIDENCE_RECONCILIATION=PASS`; per-run stdout/stderr logs `45/45` each; source pins `81/81`; authority-input pins `9/9`.
- C11-C frozen manifest before/after: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

The operator's wrapper also displayed a failure in its extra direct `godot.exe --version` probe, a split `else` syntax error, and a report-marker comparison error. These are wrapper-level issues—not accepted gate results. The Python runner itself exited `0`, reported a successful internal Godot 4.7.1 Mono probe, emitted the `PASS_SAFE_PROJECTION_SEED_SENSITIVITY` marker with empty stderr, and its report and evidence were then independently reconciled to PASS. Do not cite the failed wrapper substeps as passed; do not rerun the 45+45 matrix solely to address them.

## Accepted interpretation

All nine selectors passed the contract comparisons. The matrix measured five roles per selector: baseline repeat, gameplay-seed mutation, music-seed mutation, and editorial-only mutation. The test contract uses the safe base-projection hash—not request or plan identity—as gameplay-seed sensitivity oracle. Candidate probes are per-field and hash-only. The safe projection remains source-frame ordered over `position`, `rotation`, `scale`, `opacity`, `texture_index`, and `variant_id`; coordinate transformation, interpolation, resampling and renderer-native inputs remain prohibited.

`target_x` for Pilot is invariant by design and is not the seed-sensitivity oracle; Hit `target_position` is per-run constant; Catch/Find `target_position` are source-frame tracks; Choose `active_selection` and Count `displayed_count` are typed source-frame observations. This does not by itself approve any binding or establish visual correctness in the rendered output.

## Next gate: candidate evidence audit and explicit semantic review

1. Apply the separate ADD_ONLY candidate-evidence audit overlay and execute its focused static tests.
2. Run the audit tool against the exact runtime report and static receipt above. It must reverify current source/authority pins and the hashes of all evidence files referenced by `report.json`, and emit only per-selector/per-field hash and type summaries. It must not rerun Godot.
3. Use the sanitized audit output to prepare a separate field-by-field semantic review packet. Each candidate remains `OBSERVED_NOT_APPROVED`; any approval must be a separate explicit, recorded operator/reviewer decision.
4. Independently, continue the pre-existing renderer-baseline preparation sequence: fresh active-checkout I/O gap audit and candidate identity inventory, then resolve request-specific payload identity and policy approval gaps. Do not implement a payload-side consumer while region/visibility/timebase policies are unapproved.

## Governance locks

Keep `renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `automatic_seed_generation=false`; `master_seed=NOT_ADOPTED`; `approved_bindings=0`; `approved_custom_data_bindings=0`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`.

Challenge 008/009 timeline acceptance remains blocked by the 11-second declared total versus 12-second phase sum. Challenge 004 V1 harness remains immutable. Do not serialize full `custom_data`; do not create payload/media or renderer input. C11-C remains unchanged.
