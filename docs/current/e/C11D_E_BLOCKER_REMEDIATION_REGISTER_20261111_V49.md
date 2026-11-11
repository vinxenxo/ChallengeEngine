## V9 current blocker state — E4C Drill visual consumer (2026-11-11)

V8 failed before transaction because StrictMode inspected `$testSource` before initialization. V9 fixes assignment order. V8 journal was empty and rollback was not needed. Consumer acceptance remains open; no consumer package V1–V8 transaction occurred.

---

## Current blocker — V6 runner-guide policy mismatch (2026-11-11)

## V8 current state — 2026-11-11

V7 failed closed in `STAGED_VALIDATION` before transaction. Its installer imported `QT_VERSION_STR` from `PySide6.QtCore`; the canonical PySide6 runtime does not export that symbol. This is an installer probe defect, not evidence that PySide6, Qt, QImage or QPainter is missing. The preceding imports of `PySide6.__version__` succeeded. `journal=[]`; `rollback=NOT_NEEDED`; no checkout write occurred.

V8 changes the probe to `from PySide6.QtCore import qVersion` and records `qVersion()` as the Qt runtime version. It requires Qt 6.x, alongside Python 3.13.x, existing PySide6 6.8–6.x, non-null RGB888 QImage and active QPainter. The official Qt for Python API lists `qVersion()` as a QtCore function. V8 does not install, upgrade or uninstall packages, invoke pip, edit requirements, or mutate the shared Python environment.

The consumer, its 35 Qt tests and the E1 service replacement are byte-identical to V7. No functional test result is inferred from the failed V7 runtime probe. V8 must still pass Windows PowerShell 5.1 AST, inventory/pins/destinations/staging, runtime probe, `py_compile` 3/3, all 35 Qt tests and immediate pre-transaction checks before any write. Do not repeat accepted A.3, binder V2, Godot V3, Loop22 or historical Drill authoring.

Governance remains unchanged: C11-C frozen manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; renderer OFF; dispatch/media/audio OFF; `release_authority=NONE`; operator manages commits; Git checks skipped.

### V7/V8 probe incident
Root cause is the invalid `QT_VERSION_STR` import in the installer, not a missing or broken Qt runtime. Remediation uses supported `PySide6.QtCore.qVersion()` and validates Qt 6.x. Keep the gate open until Windows executes all new Qt tests.

---


V6 reached staged validation after all package, rollback, AST, pin, decision, destination and staging checks. It failed because guide V15 did not contain the exact `No new Python dependency` anchor required by the installer. The guide's top V15 rules already prohibited Pillow/RAQM and environment mutation, but an inherited V14 section still described the superseded Pillow pin/provisioning. This is a documentation/validator consistency defect, not a Qt runtime failure. Evidence run `E4C_DRILL_VISUAL_PIXEL_CONSUMER_V6_20261111T004628_177cd6f5`: `journal=[]`, `rollback=NOT_NEEDED`, no transaction.

V7 candidate advances guide V16 with the exact normative phrase and removes the contradictory active Pillow instructions by explicitly marking them superseded. No consumer, E1 service, test, pin or approval changes are made. V7 still requires active-Windows Qt probe, py_compile 3/3 and 35/35 before writes. No new Python dependency, pip, requirements edit or shared environment mutation is allowed.

---

## Current blocker — E4C consumer must reuse existing Qt runtime (2026-11-11)

**ID:** E4C-VC-QT-001  
**State:** OPEN / QT_BACKEND_REQUALIFICATION_REQUIRED.  
**Correction:** The prior Pillow remediation was rejected as an architectural mistake. The operator was instructed to install Pillow globally; Pillow==12.3.0 was installed successfully, but the subsequent Python `-c` verification failed because PowerShell stripped nested quotes. Do not retain this dependency. Remove only that accidentally added Pillow package from the canonical Python 3.13 interpreter and verify `importlib.util.find_spec('PIL')` returns `None`.

The consumer is being migrated to the existing PySide6 already declared by the Producer. No new package, pip operation, requirements edit or global environment mutation is authorized. V6 is a new Qt rendering backend; its 35 tests must run on Windows before any transaction. Existing accepted binder/A.3/Loop/Godot gates remain closed and are not repeated. Renderer OFF; dispatch/media/audio/release OFF.

## Current blocker — E4C consumer runtime dependency (2026-11-11)

**ID:** E4C-VC-PILLOW-001  
**State:** OPEN / OPERATOR_ENVIRONMENT_PREREQUISITE  
**Root cause:** the canonical project Python 3.13.14 executable starts correctly but lacks the `PIL` module. The V4 runtime probe exited with `ModuleNotFoundError: No module named 'PIL'`; RAQM was not reached.  
**Evidence:** `e4c_drill_visual_pixel_consumer.zip`, run `E4C_DRILL_VISUAL_PIXEL_CONSUMER_V4_20261111T001315_ed8f8d25`. All 18 prior operations checks passed; `journal=[]`, rollback `NOT_NEEDED`, no checkout write.  
**Remediation:** manually install exact D-owned dependency `Pillow==12.3.0` into the same Python 3.13 runtime used by Producer; verify RAQM true; then run V5 with explicit `-PythonExe`. No dependency installation is automated.  
**Protection:** do not edit C11-C/root requirements; no renderer, dispatch, media, audio or release authority.

# C11-D / C11-E Blocker Remediation Register — V45 (2026-11-11)

| ID | Gate / issue | State | Required closure |
|---|---|---|---|
| E4C-A3-LINEAGE | D9.8 lineage pointer and review-manifest bridge | CLOSED_PASS_ACTIVE_WINDOWS | A.3 V5 receipt `d39eec2b3c1d969a3cb0d4e6aaa14b87aadcba74e42e58d283e00ea50768e881`; 3 replacements +26 adds; suites 33+5+7+10; py_compile 8/8. No rerun. |
| E4C-DRILL-SOURCE | Native Drill phase and ownership | PASS_READ_ONLY | Phase audit V2, 8 exact C11-C pins /12 checks; preserve native header/footer and END_CTA CTA. |
| E4C-DRILL-GEOMETRY | D outer-band composition | APPROVED_AS_PROPOSED | Exact geometry SHA approved for D-owned design/contract and isolated pixel scope only. |
| E4C-DRILL-TIMEBASE | GAME payload → final-presentation frame mapping | APPROVED_AS_PROPOSED | Exact timebase SHA approved for D-owned design/contract and isolated pixel scope only. |
| E4C-DRILL-CONSUMER | Consumer V4 install and 35-test Windows stage | PENDING_ACTIVE_WINDOWS_V4 | Local faithful V121 stage passes py_compile 3/3 and 35/35; Windows PS5.1 AST/runtime/tests/receipt required before write. |
| E4C-GUI | Existing Qt Producer GUI runtime | OPEN | Observe actual GUI route through existing shared E1 service; verify GUI/CLI parity. |
| E4C-DRILL-AV | Native family music, mux and human review | NOT_QUALIFIED | Silent protected C11-C capture; existing `FAMILY_MUSIC_V4`; independent seeds; FFmpeg/FFprobe; human review. D.1 is envelope only. |
| E5 | Cross-family determinism/seed isolation/profile non-leakage/GUI-CLI parity | PENDING | After E4C family closeout. |
| E6 | Smoke18 | PENDING | Six complete A/V scenarios per family. |
| E7 | Matrix101 | PENDING_SCOPED | 54+27+20 target; CH_008/009 held, 99 provisional. |
| E8 | Historical C-to-E regression, independent acceptance, freeze/promotion | BLOCKED | Complete E7, independent acceptance and separate explicit authority. |

## Current package failures and control

- Consumer V1: pre-transaction fail; missing required guide V12 from package.
- Consumer V2: pre-transaction fail; exact rollback heading absent from staged guide despite equivalent semantics; empty journal, `rollback=NOT_NEEDED`.
- Consumer V3: superseded before Windows; faithful stage replay found missing read-only test roots `challenges/`, full `assets/`, `docs/current/d/`.
- Consumer V4: prepared; includes the three path-budgeted/copied roots, stage-root assertions, explicit rollback policy and implementation inspection. Windows acceptance pending. Only 18 manifest operations can transact; copied roots are staged read-only test inputs.

Operator geometry/timebase record SHA `eb95da188065b8ebcb2371e2a6bcff6762ce000a5ca74f8ea384ecec4ee58303`. C11-C 2.19.12 remains sole production authority; renderer OFF; dispatch/media false; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`.
