# C11-E Current Documentation Index — V38

Supersedes V37. Current authority: `C11E_CURRENT_AUTHORITY_20261106_V78.md`.

## Current authority and planning

| Document | Purpose |
|---|---|
| `C11E_CURRENT_AUTHORITY_20261106_V78.md` | Current approved decisions, E4B static contract status and governance |
| `C11E_GATES_ACCEPTANCE_MATRIX_20261106_V76.md` | Current gate-by-gate state |
| `C11E_E3_EXECUTION_BACKLOG_20261106_V53.md` | Immediate Windows verification and next integration work |
| `C11E_E4A_CHALLENGE_LOOP_DRILL_ALIGNMENT_20261106_V31.md` | Shared content-family contract alignment |
| `C11D_TO_C11E_FULL_FAMILY_ROADMAP_20261106_V66.md` | Full family rollout and cutover sequence |
| `C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261106_V11.md` | PS 5.1, pins, receipts, add-only constraints |

## E4B Loop reviews and decisions

| Document | Purpose |
|---|---|
| `C11E_E4B_LOOP_SOURCE_REVIEW_20261106_V6.md` | D9 / E1 and protected C11-C source boundary |
| `C11E_E4B_LOOP_COMPOSITION_REVIEW_20261106_V5.md` | Historical composition proposal review |
| `C11E_E4B_LOOP_GUI_CLI_PARITY_REVIEW_20261106_V5.md` | GUI/CLI parity and family matrix |
| `C11E_E4B_LOOP_FAMILY_MATRIX_REVIEW_20261106_V2.md` | 81-case plan-only matrix acceptance |
| `C11E_E4B_LOOP_POLICY_READINESS_REVIEW_20261106_V1.md` | Current hash readiness audit (historical state before operator approval) |
| `C11E_E4B_LOOP_POLICY_DECISION_DOCKET_20261106_V1.md` | Historical decision form; superseded by the operator decision record |
| `C11E_E4B_LOOP_FAMILY_STAGE_CONTRACT_REVIEW_20261106_V1.md` | 27-selector family-stage contract proof and limitations |
| `C11E_E4B_D98_D99_SEMANTIC_RECONCILIATION_20261106_V1.md` | Plan-only D9.8/D9.9/D9.10 interpretation |
| `C11E_E4B_AUDIO_SEED_BOUNDARY_REVIEW_20261106_V1.md` | Visual seed vs music seed and D.1 limits |

## Versioned D-owned records and tools

- `docs/current/e/C11E_E4B_OPERATOR_POLICY_DECISION_RECORD_20261106_V1.json` — the five current-hash decisions given by the operator; it does not grant execution or release authority.
- `docs/current/e/C11E_E4B_D98_D99_SEMANTIC_RECONCILIATION_20261106_V2.json` — machine-readable plan-only reconciliation.
- `tools/c11d/d9/C11E_E4B_LOOP_FAMILY_CONTRACT_SOURCE_PINS_V1.json` — 40 source pins.
- `tools/c11d/d9/c11e_e4b_loop_family_contract_audit.py` — read-only source/decision/family-interface audit.
- `tools/c11d/d9/c11e_e4b_loop_family_stage_contract.py` — pure in-memory D-only family-stage contract builder.
- `tools/c11d/d9/test_c11e_e4b_loop_family_contract.py` — seven focused tests including 27 canonical family/grammar paths.
- Top-level `INSTALL_C11E_E4B_LOOP_FAMILY_CONTRACT_V1.ps1` in the package — add-only installer (not copied into the checkout).
- `tools/c11d/d9/RUN_C11E_E4B_LOOP_FAMILY_CONTRACT_V1.ps1` — PS 5.1 runner with logs and receipt.

## Current continuation prompts

- `prompts/C11E_CONTINUATION_MASTER_PROMPT_20261106_V76.md`
- `prompts/C11E_NEXT_WINDOW_START_PROMPT_20261106_V76.md`
- `prompts/C11E_FIRST_PROMPT_20261106_V20.md`

V77/V37 and earlier records remain immutable history. The V1 approval docket remains historical and is not the authority for the five decisions now recorded in the D-owned V1 decision record.
