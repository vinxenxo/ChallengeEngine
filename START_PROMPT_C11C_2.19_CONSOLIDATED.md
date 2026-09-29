# START PROMPT — ChallengeEngineV01_STATELESS / C11-C 2.19 CONSOLIDATED

Continue from **C11-C 2.19.12 FULL CONSOLIDATED REPAIR CANDIDATE — NOT FROZEN**.

## First reads

1. `MASTER_HANDOVER_C11C_2.19_CONSOLIDATED.md`
2. `START_PROMPT_C11C_2.19_CONSOLIDATED.md`
3. `docs/current/c11c/C11-C_2.19_CONSOLIDATED_STATE.md`
4. `docs/current/c11c/C11-C_2.19_CONSOLIDATED_ACCEPTANCE_GATE.md`
5. `docs/current/c11c/C11-C_2.19_COMPLETE_VIDEO_REVIEW_RUNBOOK.md`
6. `docs/current/c11c/C11-C_2.19_COMMAND_SHEET.md`
7. `docs/current/c11c/C11-C_2.19_DOCUMENTATION_INDEX.md`
8. `docs/history/c11c/releases/C11-C_2.19_CONSOLIDATED_HISTORY.md`

## Step 1 — static and focused contracts

```powershell
python .\c11c-suite\self_test.py
python .\c11c-suite\c11c-producer\self_test.py
python .\c11c-suite\c11c-producer\test_producer_gui_contract.py
.\c11c-suite\c11c-producer\test_gui_contract.bat
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\qa\c11\verify_c11c_suite_launchers.ps1
.\c11c-suite\c11c-test\run_suite.bat C11CVisualDrillReviewEnvelopePathContractTest.gd
.\c11c-suite\c11c-test\run_suite.bat C11CParallelReviewWorkerIsolationContractTest.gd
```

The envelope-path test is valid only when the console ends after `[C11C_VISUAL_DRILL_ENVELOPE_PATH_CONTRACT_SUITE] PASS` with exit code 0. `PASS` followed by `FAIL (0 failure(s))` is a failed test.

## Step 2 — focused validation

```powershell
.\c11c-suite\c11c-test\run_c11c_focused_validation.bat
```

## Step 3 — one video per content type

```powershell
.\c11c-suite\c11c-test\run_c11c_one_video_each_type.bat
```

This is the fast runtime smoke: 1 Visual Loop + 1 Visual Drill + 1 Longform. It must not be confused with the 52-video complete review.

## Step 4 — full logical

```powershell
python .\tests\run_all.py
```

## Step 5 — complete 52-video review

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\tools\qa\c11\run_c11c_complete_video_review.ps1 `
  -Workers 7 `
  -Reset
```

`Workers=7` means real concurrent capture. Never serialize it to make a failure disappear.

## Step 6 — final acceptance candidate

```powershell
.\c11c-suite\c11c-test\run_c11c_acceptance.bat
```

## Mandatory guardrails

- `c11c-suite/` is the active Suite.
- `c11c-studio/` is retired: do not update it and do not use it.
- Private worker roots are the solution to capture-state collisions; the canonical field is `WorkerRoot`.
- Do not add a global mutex or serial fallback.
- Preserve all frozen engine/RNG/C7/C9/social geometry boundaries.
- Do not freeze until fresh workstation evidence is fully green.

## Challenge diagnostic before full family coverage

Use `c11c-suite/c11c-test/run_c11c_challenge_family_smoke.bat -ChallengeId CHALLENGE_003` first when Challenge family coverage exposes a failure. It uses `MIN_540` by default and delegates to the canonical Challenge smoke/production path; it does not shorten timing or change Challenge definitions.

Read `docs/current/c11c/C11-C_2.19_CONSOLIDATION_AND_FAILURE_PREVENTION.md` for the consolidated 2.16.9→2.19 operational lessons. Do not create standalone console runners outside Suite registration.
