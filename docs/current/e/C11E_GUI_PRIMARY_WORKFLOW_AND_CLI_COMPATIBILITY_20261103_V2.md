# C11-E Development CLI and GUI Execution Contract — V2

**Date:** 2026-11-03  
**Purpose:** Clarify development sequencing and preserve the future GUI-only production target without suppressing CLI use during engineering.

## 1. Current development workflow

The engineering order is **CLI-first where practical, followed by GUI integration of the same implementation**.

- Implement request semantics, shared service, family adapters, render/audio scripts, validators and receipts as independently executable Python/CLI workflows first.
- Keep each script separately invokable for deterministic tests, controlled diagnostics and development automation.
- Connect the same service/scripts to the current low-fidelity Producer GUI. The GUI callback prepares the canonical request/intent, then dispatches the script/worker (for example, E3 through `QProcess`).
- GUI callbacks must not reimplement business logic or fork family-specific production logic.
- Both CLI and GUI execution paths are in-scope tests during development. Compare normalized request, editorial values, layout/presentation selection, seed domains, family adapter, media result and receipt semantics. Execution-origin metadata may legitimately differ.

The `c11e_production_cli.py` is the E1 intent-preparation adapter. The E3 worker `c11e_e3_audio_pilot.py` is itself a CLI script and can run standalone with a prepared intent; the GUI calls that same script and adds `--operator-gui` only as execution provenance.

## 2. Existing GUI role

The current Producer GUI is a low-fidelity integration surface. Its role during development is to expose selectors/values and dispatch the tested scripts. It is not a reason to implement or debug all logic visually first. It must display progress, logs, failure details, final artifact and QA summary when those capabilities are in scope.

## 3. Future production operating model

After the D/E baseline formally replaces C, a later GUI redesign/implementation phase will make all ordinary human production generation available through the new GUI. That future GUI-only operating model does not retroactively constrain development sequencing and does not remove CLI compatibility from automated testing, separate-process parity, reproducibility or controlled engineering.

## 4. Acceptance sequence

1. CLI/service implementation and contract tests.
2. CLI subprocess tests and immutable receipt semantics.
3. Existing low-fidelity GUI integration using the same service/worker.
4. GUI runtime tests and visible error/progress/result handling.
5. Cross-path semantic parity and failure-path tests.
6. After C replacement, new-GUI-only operator acceptance; CLI retained for CI/compatibility.

Do not create a second producer, independent CLI business-logic branch, sixth suite module or `c11d-control`.
