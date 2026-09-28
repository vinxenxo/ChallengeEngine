# START PROMPT — ChallengeEngineV01_STATELESS — C11-C 2.19.6 Final Repair

Continue from **C11-C 2.19.6 FINAL REPAIR CANDIDATE — NOT FROZEN**.

## First objective

Verify the repaired worker contract. Do not alter the proven concurrent worker implementation.

```powershell
python .\c11c-suite\self_test.py
python .\c11c-suite\c11c-producer\self_test.py
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\maintenance\verify_c11c_2_19_6_final_repair.ps1
.\c11c-suite\c11c-test\run_suite.bat C11CParallelReviewWorkerIsolationContractTest.gd
```

The focused test must print:

```text
[C11C_PARALLEL_REVIEW_WORKER_ISOLATION_CONTRACT_SUITE] PASS
```

## Second objective

Run the real 7-worker review:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\tools\prototypes\c11c_bulk\run_c11c_art_direction_batch_v4.ps1 `
  -Workers 7 -Loops -Reset
```

Required runtime proof: worker bootstrap PASS, 720×1280 @ 30 FPS and `MAX_OBSERVED_CONCURRENCY > 1`. The workstation already demonstrated `7`.

## Prohibited regression

Do not add a mutex. Do not change the batch to one-at-a-time. Do not reintroduce `c11c-studio`.

## Final stage

```powershell
python .\tests\run_all.py
.\FULL_ACCEPTANCE_C11C_2.19.6.ps1
```

Only after full PASS can the formal 2.19.6 freeze seal be considered.
