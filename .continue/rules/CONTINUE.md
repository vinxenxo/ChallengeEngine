# CONTINUE.md — ChallengeEngineV01_STATELESS / C11-C 2.19.6

The active state is **C11-C 2.19.6 FINAL REPAIR CANDIDATE — NOT FROZEN**.

The 2.19.6 worker runtime already demonstrates genuine concurrency. The acceptance failure was a false-negative test ordering check. The repaired test compares the actual worker-pool creation call site to the first `Start-LoopReviewJob -FamilyId` invocation.

`c11c-suite/` is the sole active Suite implementation. `c11c-studio/` is retired and must remain untouched.

Do not reintroduce a global mutex or serialize Movie Maker captures. Preparation may be sequential; capture must remain concurrent.

Before acceptance:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\tools\maintenance\verify_c11c_2_19_6_final_repair.ps1

.\c11c-suite\c11c-test\run_suite.bat C11CParallelReviewWorkerIsolationContractTest.gd

powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\tools\prototypes\c11c_bulk\run_c11c_art_direction_batch_v4.ps1 `
  -Workers 7 -Loops -Reset

python .\tests\run_all.py
.\FULL_ACCEPTANCE_C11C_2.19.6.ps1
```

Do not start C11-D until C11-C is formally frozen.
