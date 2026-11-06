# C11-E Current Documentation Index — V37

Supersedes V36. Current authority is `C11E_CURRENT_AUTHORITY_20261106_V77.md`.

## Current E authority and planning

| Document | Purpose |
|---|---|
| `C11E_CURRENT_AUTHORITY_20261106_V77.md` | Current accepted gates, hashes, governance and order |
| `C11E_GATES_ACCEPTANCE_MATRIX_20261106_V75.md` | Gate-by-gate acceptance matrix |
| `C11E_E3_EXECUTION_BACKLOG_20261106_V52.md` | Immediate work and dependency backlog |
| `C11E_E4A_CHALLENGE_LOOP_DRILL_ALIGNMENT_20261106_V31.md` | Shared Challenge/Loop/Drill contract alignment |
| `C11D_TO_C11E_FULL_FAMILY_ROADMAP_20261106_V65.md` | D-to-E family rollout and C→D cutover conditions |
| `C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261106_V11.md` | PS 5.1, ASCII source, pins, receipts and add-only rules |

## E4B Loop current evidence reviews

| Document | Purpose |
|---|---|
| `C11E_E4B_LOOP_SOURCE_REVIEW_20261106_V6.md` | Producer/D9/E1 and protected C11-C source boundary |
| `C11E_E4B_LOOP_COMPOSITION_REVIEW_20261106_V5.md` | Candidate outer composition, still unapproved |
| `C11E_E4B_LOOP_GUI_CLI_PARITY_REVIEW_20261106_V5.md` | Populated GUI/CLI parity plus 81-row family matrix parity |
| `C11E_E4B_LOOP_FAMILY_MATRIX_REVIEW_20261106_V2.md` | Windows acceptance and hash-level independent audit |
| `C11E_E4B_LOOP_FAMILY_MATRIX_EXECUTION_PLAN_20261106_V2.md` | Matrix commands and output paths; no rerun unless regression |
| `C11E_E4B_LOOP_WINDOWS_MATRIX_ACCEPTANCE_REVIEW_20261106_V1.md` | Independent Windows evidence acceptance |
| `C11E_E4B_LOOP_POLICY_READINESS_REVIEW_20261106_V1.md` | Current proposal hashes and stale packet V1 reconciliation |
| `C11E_E4B_LOOP_POLICY_DECISION_DOCKET_20261106_V1.md` | Exact current hashes and operator decision fields; all remain pending |
| `C11E_E4B_LOOP_D_ONLY_CONSUMER_IMPLEMENTATION_BLUEPRINT_20261106_V1.md` | Conditional next implementation, requiring current policy decisions |

## Current audit tools

- `tools/c11d/d9/c11e_e4b_loop_policy_readiness.py` — read-only comparison/audit of the accepted matrix, D9.8 metadata and current policy proposal pins.
- `tools/c11d/d9/test_c11e_e4b_loop_policy_readiness.py` — focused tests for the readiness audit.
- `tools/c11d/d9/RUN_C11E_E4B_LOOP_POLICY_READINESS_V1.ps1` — PS 5.1 wrapper; no Git, source writes, render, generator or media.

## Prompt authority

- `prompts/C11E_CONTINUATION_MASTER_PROMPT_20261106_V75.md`
- `prompts/C11E_NEXT_WINDOW_START_PROMPT_20261106_V75.md`
- `prompts/C11E_FIRST_PROMPT_20261106_V19.md`

## Superseded documents retained

V76/V74 and earlier E4B docs remain historical and add-only. They record pre-Windows matrix state and must not be treated as current after the acceptance in V77. D decision packet V1 remains a historical `REVIEW_PACKET_ONLY_ALL_POLICIES_UNAPPROVED` record; its A.3/B.1/D.1 hashes are stale and must not authorize a current proposal.
