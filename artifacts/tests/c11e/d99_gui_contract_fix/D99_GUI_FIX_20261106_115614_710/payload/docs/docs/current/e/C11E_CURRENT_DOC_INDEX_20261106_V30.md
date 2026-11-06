# C11-E Current Documentation Index — V30

**Authority:** Current Authority V70; Matrix V68; Backlog V45; Family Roadmap V58; Alignment V24; PowerShell Style Guide V6.

## Read first

1. `AGENTS.md`, `.continue/rules/CONTINUE.md`, `README.md` (legacy V18-era references; malformed frozen-manifest hash text is historical only).
2. `docs/current/e/C11E_CURRENT_AUTHORITY_20261106_V70.md`.
3. `docs/current/e/C11E_GATES_ACCEPTANCE_MATRIX_20261106_V68.md`.
4. `docs/current/e/C11E_E3_EXECUTION_BACKLOG_20261106_V45.md`.
5. `docs/current/e/C11E_E4A_CHALLENGE_LOOP_DRILL_ALIGNMENT_20261106_V24.md`.
6. `docs/history/c11d/C11D_TO_C11E_FULL_FAMILY_ROADMAP_20261106_V58.md`.
7. `docs/current/e/C11E_E4A7_D_COMPOSITED_CHALLENGE_AV_PLAN_20261106_V3.md`.
8. `docs/history/c11e/C11E_E4A7_POSTRUN_EVIDENCE_REVIEW_20261106_V2.md`.
9. `docs/current/e/C11E_E1_GUI_CLI_RUNTIME_PARITY_PLAN_20261106_V2.md`.
10. `docs/current/e/C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261106_V6.md`.
11. `docs/history/c11e/C11E_D99_GUI_PRESENTATION_OPTIONS_CONTRACT_INCIDENT_20261106_V1.md` (read before applying the GUI patch).
12. Earlier recovery postmortem V1, source-pin reconciliation V1 and E4A6 capture postmortem lineage.

## Prompts

- `prompts/C11E_CONTINUATION_MASTER_PROMPT_20261106_V68.md`.
- `prompts/C11E_NEXT_WINDOW_START_PROMPT_20261106_V68.md`.
- `prompts/C11E_FIRST_PROMPT_20261106_V12.md`.

## Additional incident checkpoint

Read `docs/history/c11e/C11E_D99_GUI_PRESENTATION_OPTIONS_CONTRACT_INCIDENT_20261106_V1.md` before modifying the Producer GUI. No `presentation_options` field belongs in D9.9; all approved editorial keys remain in canonical editorial output, with blank values normalized by D9.8 to `UNKNOWN`.

## Current state

E4A.6 PASS_TEST_ONLY + visual review. E4A.7 PASS_TEST_ONLY + independent ZIP audit; operator listening A/B/C PASS. Full E4A remains IN_PROGRESS pending the surgical D99 GUI request cleanup and a new GUI/E1/D9.9 parity run. Do not rerun visual/audio workers. E4B/E4C remain ordered after full E4A.

C11-C 2.19.12 remains frozen production authority. All test-only and governance limits remain in force. Runners must not invoke Git.
