# C11-C 2.19.12 V9 — worker bootstrap / root layout / permanent rules

ROOT-RELATIVE overlay. Extract directly into the repository root.

## Repairs

1. `tools/prototypes/c11c_bulk/C11CReviewWorkerIsolation.ps1`
   - keeps one private WorkerRoot per worker;
   - bootstraps the worker `.godot/global_script_class_cache.cfg` so `PresentationProfile` is resolvable;
   - suppresses bootstrap pipeline output so `New-C11CReviewWorkerPool` returns one pool object only;
   - preserves `WorkerRoot`, no mutex and no serial fallback.

2. `tools/maintenance/verify_repository_layout.ps1`
   - removes the PowerShell 5.1 trailing comma parser bug.

3. `c11c-suite/c11c-maintenance/organize_repository_root.ps1`
   - preserves conflicting `OVERLAY_MANIFEST.json` as a timestamped root snapshot instead of overwriting legacy evidence.

4. `c11c-suite/self_test.py` and `tests/C11CParallelReviewWorkerIsolationContractTest.gd`
   - retain the known-good versions and add regression assertions for worker-pool output containment.

5. `docs/current/c11c/`
   - records the V8 packaging mistake and permanent operating rules.

`c11c-studio` is historical-only and is not an operational project component. The active operational control surface is split into the smaller suites under `c11c-suite/`.

No engine/core/challenge-definition/asset implementation is changed by this overlay.
