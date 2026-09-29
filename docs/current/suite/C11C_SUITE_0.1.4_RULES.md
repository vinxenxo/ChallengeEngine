# C11-C Suite 0.1.4 — Operational Rules

## Ownership

`c11c-suite/` is the canonical active Suite surface. `c11c-studio/` is retired and must not be updated or required for operation.

## Launcher parity

Every operational test/QA capability must have:

1. a canonical repository implementation;
2. a direct console route;
3. the relevant Suite/GUI route when appropriate;
4. current documentation.

`c11c-test/run_suite.bat` accepts `GODOT_BIN` when the user needs to select an explicit Godot executable.

## 2.19.5 Art Direction concurrency

The Art Direction batch keeps the requested `Workers=7` concurrency. A worker is not merely a logical queue slot: it owns an independent temporary Godot project root, including its own temporary `override.cfg` and `.godot` state.

A project-global mutex is prohibited because it converts the worker pool into serial execution.

## Godot contract-test lifecycle

Command-line Godot tests implemented with `extends SceneTree` / `extends MainLoop` must enter through `_initialize()` (or intentionally through `_init()` for tests designed for that lifecycle). They must terminate explicitly with `quit()` or an intentional MainLoop termination return. `_ready()` is a Node callback and is not the command-line MainLoop entrypoint.

The 2.19.5 worker-isolation contract test is explicitly guarded by the Suite self-test against regression to `_ready()`.

## Retired studio rule

Operational `.py/.ps1/.bat/.cmd` sources under `c11c-suite/` must contain no `c11c-studio` dependency. The static Suite self-test enforces this.

## GUI / backend boundary

The Suite and Producer remain orchestration surfaces. They do not implement mechanics, RNG, timing truth or gameplay calculations.

## Validation

Focused contracts precede the full logical corpus and the consolidated acceptance gate:

```powershell
python .\c11c-suite\self_test.py
python .\tests\run_all.py
.\FULL_ACCEPTANCE_C11C_2.19.5.ps1
```
