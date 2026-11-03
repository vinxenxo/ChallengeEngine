# C11-E Next Window Start Prompt — V25

Continue the project in `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. The user will attach the latest filtered `C11E_WORKING_CONTEXT_*.zip`, `.sha256` and `.report.json`. Never extract this snapshot over the active checkout; active Windows source is authority.

## Read first

1. `docs/current/e/C11E_CURRENT_AUTHORITY_20261103_V25.md`
2. `docs/current/e/C11E_GATES_ACCEPTANCE_MATRIX_20261103_V25.md`
3. `docs/current/e/C11E_E3_EXECUTION_BACKLOG_20261103_V2.md`
4. `docs/current/e/C11E_E3_AUDIO_PILOT_TEST_20261103_V1.md`
5. `docs/current/e/C11E_E3_WINDOWS_TEST_ACCEPTANCE_20261103_V1.md`
5. `docs/current/e/C11E_EXECUTION_HYGIENE_AND_ASSISTANT_ERROR_LOG_20261103_V21.md`
6. `docs/current/e/C11E_GUI_PRIMARY_WORKFLOW_AND_CLI_COMPATIBILITY_20261103_V1.md`
7. `docs/history/c11e/C11E_E3_2_FORMAL_CLOSURE_AND_DECISION_RECORD_20261103_V1.md`
8. `docs/history/c11e/C11E_ARCHITECTURE_DECISION_RECORD_AND_BACKLOG_20261103_V1.md`
9. `docs/history/c11e/C11E_E3_CHALLENGE_AUDIOVISUAL_IMPLEMENTATION_PLAN_20261103_V1.md`
10. `docs/history/c11d/C11D_TO_C11E_FULL_FAMILY_ROADMAP_20261103_V15.md`
11. `docs/current/e/C11E_CONTEXT_SNAPSHOT_OPERATOR_GUIDE_20261103_V1.md`
12. `prompts/C11E_CONTINUATION_MASTER_PROMPT_20261103_V25.md`

Read live `AGENTS.md` and `.continue/rules/CONTINUE.md` for boundaries.

## Last accepted Windows result

- V1.3 audio patch: PASS, 10/10 postimages.
- V1.4 Windows runner: Python 3.13.14; compile PASS; 31/31 `test_c11e*.py` PASS; PySide6 6.11.2 PASS.
- Test receipt SHA-256 `84fc86c96ca237c7dd16837666882e80afe6dda8292a04527d19fcbd3579e30b` in `Documents\C11E_E3_TEST_EVIDENCE\C11E_E3_TESTS_V14_f371a0bfdccf407aba5e3e4cbf6c5f4b`.
- Temporary FFmpeg mux test was run; no production audio, renderer, gameplay rerender or GUI launch.
- Do not reapply V1.3 and do not rerun the 31-test suite unless source/test pins change.

## First task — continue E3, do not restart

Perform E3-GUI-01. Derive the actual existing Producer GUI launch entry point from live source; do not invent it. Launch GUI on Windows and observe the E3 action in the existing universal editorial surface. Verify it calls the E1 shared service. From the GUI, run one controlled CH001 audio attach pilot using the immutable E2 R4 MP4 as input and fresh test-only output. Do not rerender gameplay.

Use `challenge_8bit_v1`, music seed `840001` (seed-difference control `840002`), gameplay seed `193847` as R4 provenance, variation 0, and tempo 104 BPM only as a D9.2 pilot fixture. Derive duration via FFprobe from the exact R4 source (9 seconds). Preserve raw WAV; apply the active D3.3 mastering implementation; trim final audio to video duration; mux by video stream copy; FFprobe one video + one audio stream and verify frame identity, audio format/non-silence and <=0.15s historical pilot drift. Collect full structured receipt, hashes and logs. CLI is automated parity only.

Stop at the first failure, preserve evidence and report it. Do not repeat documentation phases, installer repair, Git bookkeeping or accepted tests. Do not move to E4 until E3 exit evidence is complete.

## Full-family road map

E3 Challenge music/mux -> E4A Challenge -> E4B Loop -> E4C Drill -> E5 cross-family determinism and GUI/CLI parity -> E6 Smoke18 -> E7 Matrix101 (99 provisional runnable; CH_008/009 held for 11s vs 12s conflict) -> E8 independent acceptance/freeze/promotion.

C11-C 2.19.12 remains production authority; `release_authority=NONE`.
