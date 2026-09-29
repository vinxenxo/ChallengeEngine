# Testing and Regression — C11-C 2.19.12

## Current status

C11-C is at the final 2.19.12 closure-candidate gate. Earlier 2.19.x acceptance documents are historical evidence.

## Logical test corpus

Current corpus: 139 registered logical `*Test.gd` suites. Two physical-export suites are intentionally skipped by the default logical run.

## Logical runner

```powershell
python .\tests\run_all.py
```

The runner has a bounded process-level retry for exact Windows exit status `0xC06D007F` (up to three additional attempts). It never retries deterministic test FAIL markers, fatal patterns, timeouts, missing PASS markers after exit code 0, or other non-zero statuses.

## Review

The complete audiovisual corpus is 52 videos: 27 Visual Loop grammars + 20 Visual Drill renders + 5 Longforms. The Art Direction capture must observe concurrency greater than one with `Workers=7`.

## Final gate

```powershell
.\c11c-suite\c11c-test\run_c11c_acceptance.bat
```

Final acceptance must be green before the C11-C freeze receipt is created.
