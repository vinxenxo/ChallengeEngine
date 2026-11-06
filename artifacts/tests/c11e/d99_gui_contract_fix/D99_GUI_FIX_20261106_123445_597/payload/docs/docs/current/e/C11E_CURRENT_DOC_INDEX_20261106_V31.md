# C11-E Current Documentation Index — V31

**Authority:** Current Authority V71; Matrix V69; Backlog V46; Family Roadmap V59; Alignment V25; PowerShell Style Guide V7.

## Read first

1. `AGENTS.md`, `.continue/rules/CONTINUE.md`, `README.md` (legacy V18-era references; malformed frozen-manifest hash text is historical only).
2. `docs/current/e/C11E_CURRENT_AUTHORITY_20261106_V71.md`.
3. `docs/current/e/C11E_GATES_ACCEPTANCE_MATRIX_20261106_V69.md`.
4. `docs/current/e/C11E_E3_EXECUTION_BACKLOG_20261106_V46.md`.
5. `docs/current/e/C11E_E4A_CHALLENGE_LOOP_DRILL_ALIGNMENT_20261106_V25.md`.
6. `docs/history/c11d/C11D_TO_C11E_FULL_FAMILY_ROADMAP_20261106_V59.md`.
7. `docs/current/e/C11E_E4A7_D_COMPOSITED_CHALLENGE_AV_PLAN_20261106_V3.md`.
8. `docs/history/c11e/C11E_E4A7_POSTRUN_EVIDENCE_REVIEW_20261106_V2.md`.
9. `docs/current/e/C11E_E1_GUI_CLI_RUNTIME_PARITY_PLAN_20261106_V3.md`.
10. `docs/current/e/C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261106_V7.md`.
11. `docs/history/c11e/C11E_D99_GUI_PRESENTATION_OPTIONS_CONTRACT_INCIDENT_20261106_V2.md` (read before applying the GUI patch).
12. Earlier recovery postmortem V1, source-pin reconciliation V1 and E4A6 capture postmortem lineage.

## Prompts

- `prompts/C11E_CONTINUATION_MASTER_PROMPT_20261106_V69.md`.
- `prompts/C11E_NEXT_WINDOW_START_PROMPT_20261106_V69.md`.
- `prompts/C11E_FIRST_PROMPT_20261106_V13.md`.

## Additional incident checkpoint

Read `docs/history/c11e/C11E_D99_GUI_PRESENTATION_OPTIONS_CONTRACT_INCIDENT_20261106_V2.md` before modifying the Producer GUI. No `presentation_options` field belongs in D9.9; all approved editorial keys remain in canonical editorial output, with blank values normalized by D9.8 to `UNKNOWN`.

## Current state

E4A.6 and E4A.7 remain PASS_TEST_ONLY; visual review and operator listening A/B/C are PASS. The V1 D99 runner passed its source pins and targeted tests but failed at the `File.Replace` call because its backup path was null; its catch block also used invalid bare `false` values. V2 is the corrected combined source/documentation runner. Full E4A remains IN_PROGRESS until V2 applies the exact GUI source postimage and a new manual GUI/E1/D9.9 parity run passes. Do not rerun visual/audio workers. E4B/E4C remain ordered after full E4A.

C11-C 2.19.12 remains frozen production authority. All test-only and governance limits remain in force. Runners must not invoke Git.
