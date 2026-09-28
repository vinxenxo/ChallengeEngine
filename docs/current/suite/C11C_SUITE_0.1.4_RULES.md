# C11-C Suite 0.1.4 — Operational Rules

## Ownership

`c11c-suite/` is the canonical active Suite surface. `c11c-studio/` is retired and must not be updated or required for operation.

## Launcher parity

Every operational test/QA capability must have a canonical implementation, direct console route, relevant Suite/GUI route where appropriate, and current documentation. BAT launchers must resolve the repository root through `C11C_PROJECT_ROOT` and propagate child exit codes.

## 2.19.6 Art Direction worker architecture

The Art Direction batch keeps `Workers=7` as genuine concurrency. A worker owns a private temporary Godot project root. The source `.godot` and `override.cfg` are not copied. Each worker is initialized once with:

`godot.exe --headless --editor --path <worker> --audio-driver Dummy --quit`

The bootstrap must produce `.godot/global_script_class_cache.cfg` and register `PresentationProfile`. Only preparation is sequential; captures remain concurrent. A project-global mutex is prohibited.

## Retired studio rule

Operational `.py/.ps1/.bat/.cmd` sources under `c11c-suite/` must contain no `c11c-studio` dependency. `c11c-maintenace/run.bat` is a compatibility delegate only.

## Godot contract-test lifecycle

Command-line Godot tests using `extends SceneTree` / `extends MainLoop` must enter through `_initialize()` (or a deliberately chosen `_init()` lifecycle) and terminate explicitly. `_ready()` is not the command-line MainLoop entrypoint.

## Validation

```powershell
python .\c11c-suite\self_test.py
python .\c11c-suite\c11c-producer\self_test.py
.\c11c-suite\c11c-test\run_suite.bat C11CParallelReviewWorkerIsolationContractTest.gd
python .\tests\run_all.py
.\FULL_ACCEPTANCE_C11C_2.19.6.ps1
```
