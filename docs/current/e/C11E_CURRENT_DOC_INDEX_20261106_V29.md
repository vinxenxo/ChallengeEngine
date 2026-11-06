# C11-E Current Documentation Index — V29

**Authority:** Current Authority V69; Gates Matrix V67; Execution Backlog V44; Family Roadmap V57; Family Alignment V23; PowerShell Runner Style Guide V5.

## Read first

1. `AGENTS.md`, `.continue/rules/CONTINUE.md`, `README.md` are legacy V18-era navigation only; their malformed frozen-manifest SHA is documented historically and is not authoritative.
2. `docs/current/e/C11E_CURRENT_AUTHORITY_20261106_V69.md`.
3. `docs/current/e/C11E_GATES_ACCEPTANCE_MATRIX_20261106_V67.md`.
4. `docs/current/e/C11E_E3_EXECUTION_BACKLOG_20261106_V44.md`.
5. `docs/current/e/C11E_E4A_CHALLENGE_LOOP_DRILL_ALIGNMENT_20261106_V23.md`.
6. `docs/history/c11d/C11D_TO_C11E_FULL_FAMILY_ROADMAP_20261106_V57.md`.
7. `docs/current/e/C11E_E4A7_D_COMPOSITED_CHALLENGE_AV_PLAN_20261106_V2.md`.
8. `docs/current/e/C11E_E1_GUI_CLI_PARITY_CLOSEOUT_PLAN_20261106_V1.md`.
9. `docs/current/e/C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261106_V5.md`.
10. `docs/history/c11e/C11E_E4A7_D_COMPOSITED_CHALLENGE_AV_POSTRUN_REVIEW_20261106_V1.md`.
11. `docs/history/c11e/C11E_E4A7_AUDIO_MUX_SOURCE_PIN_RECONCILIATION_20261106_V1.md` and E4A.6 recovery postmortem V1.

## Prompts

- `prompts/C11E_CONTINUATION_MASTER_PROMPT_20261106_V67.md`.
- `prompts/C11E_NEXT_WINDOW_START_PROMPT_20261106_V67.md`.
- `prompts/C11E_FIRST_PROMPT_20261106_V11.md`.

## Current state

- E4A.6: `PASS_TEST_ONLY`, user visual review PASS, Recovery V1.2 receipt SHA `3279011fa16479d4901c5b271463707a437ce7458d306c1667ab222cb1603980`, silent D-composited MP4 SHA `841b03531301c7e70c0e09ce3e9f536241d2072a87792e099ed7a955bef8c52f`.
- E4A.7: Windows worker exit 0 and final `PASS_TEST_ONLY_D3V5_D33_MUX` marker reported. The uploaded wrapper does not contain its child run ZIP. Obtain and verify child SHA `ad4024cc6caa3b9140a284390b852c76f3dcd5d50d88cf03813d6bb4e374d293` before independent artifact audit.
- Operator listening A/B/C and E1 GUI/CLI parity remain pending. Full Challenge E4A remains open.

## Next action

Upload the child archive `RUN_20261106T070808Z-62F31F9C.zip`, then complete listening review and E1 GUI/CLI parity. Do not rerun E4A.7 or regenerate Challenge video.

## Ordered campaign

Full E4A → E4B Loop → E4C Drill → E5 → E6 Smoke18 → E7 Matrix101 → E8 complete historical C-to-E regression, independent acceptance/freeze and separate promotion. CH_008/009 held for 11 s / 12 s discrepancy.

C11-C 2.19.12 remains immutable production authority. Renderer/dispatch/production media OFF; `release_authority=NONE`.
