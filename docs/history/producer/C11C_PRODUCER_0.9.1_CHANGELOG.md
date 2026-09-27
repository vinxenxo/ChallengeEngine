# C11-C Producer 0.9.1 — Changelog

## Based on

Producer 0.9.0 / C11-C 2.18.0 stabilization state.

## Hotfixes

- Added the missing `QFrame` import required by `_build_recipe()`.
- Corrected `self_test.py` so `loop_text` and `drill_text` are initialized before their assertions.
- Added a complete PowerShell/console test command guide covering global tests, Producer self-tests, historical Challenge QA and manual Challenge/Loop/Drill production.
- Kept the backend C11-C 2.16.9 frozen and unchanged.

## Validation performed in build environment

- Python syntax compilation of `main.py`, `self_test.py` and `preflight.py`: PASS.
- JSON parsing of Producer metadata: PASS.
- Structural verification of the QFrame import and corrected self-test ordering: PASS.
- Windows/PySide6 runtime GUI acceptance remains a project-side check because the build environment does not provide the user's Windows GUI runtime.
