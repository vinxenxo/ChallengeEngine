# START PROMPT - ChallengeEngineV01_STATELESS / C11-C 2.19 CONSOLIDATED

Continue the closing C11-C branch at **2.19.12**.

Current state: **final repair candidate - NOT FROZEN**.

## First reads

1. `MASTER_HANDOVER_C11C_2.19_CONSOLIDATED.md`
2. `docs/current/c11c/C11-C_2.19.12_CLOSURE_AND_FREEZE_READINESS.md`
3. `docs/current/c11c/C11-C_2.19_CONSOLIDATION_AND_FAILURE_PREVENTION.md`
4. `docs/current/c11c/C11-C_2.19_COMPLETE_VIDEO_REVIEW_RUNBOOK.md`
5. `docs/current/c11c/C11-C_2.19_COMMAND_SHEET.md`
6. `docs/current/c11c/C11-C_2.19_DOCUMENTATION_INDEX.md`

## Fast focused validation

```powershell
.\c11c-suite\c11c-test\run_suite.bat C11A1FactoryIsolationContractTest.gd
.\c11c-suite\c11c-test\test_powershell_parse.bat
.\FULL_ACCEPTANCE_C11C_2.19.12_A1_SINGLE.ps1 -ChallengeId CHALLENGE_001 -Seed 12345
```

Optional second single smoke:

```powershell
.\FULL_ACCEPTANCE_C11C_2.19.12_A1_SINGLE.ps1 -ChallengeId CHALLENGE_007 -Seed 914213074
```

## Final closure

When focused evidence is green, execute:

```powershell
.\FULL_ACCEPTANCE_C11C_2.19.12.ps1
```

Do not substitute a partial acceptance with `-SkipHeavyPhysical` or `-SkipReviews` for the freeze gate.

## Non-negotiable rules

- No `core/` changes during this QA repair cycle.
- No new parallel backend.
- A1 routes through the canonical Challenge producer.
- The historical A1 manifest is an adapter only.
- `build_factory.py` is not the current A1 authority; the operator will supply the last historical copy at freeze time.
- Under `StrictMode`, declare every property before later assignment.
- Preserve real `Workers=7` concurrency; never serialize to hide a race.
- Preserve C11-B/C frozen engineering boundaries.

## Freeze

Only after the full acceptance prints:

`C11-C 2.19.12 - FINAL CONSOLIDATED ACCEPTANCE PASS`

is C11-C formally frozen.

Then move to the D entry documents. D starts with read-only inventory and Challenge recovery, not a new mechanic.
