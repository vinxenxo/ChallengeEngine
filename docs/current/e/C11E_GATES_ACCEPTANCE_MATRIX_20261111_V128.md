# CURRENT GATE OVERRIDE — E4C SHARED A/V EXECUTION — 2026-11-11

## E4C A/V adapter integration gate (new, pending active Windows)

| Control | Required evidence | Status at package issue |
|---|---|---|
| E1 contract | E1 status remains `PASS_E1_PREPARATION_ONLY`; `family_adapter.status=NOT_CONNECTED_E1` | Implemented in adapter; Windows runtime pending |
| GUI/CLI common path | Existing Qt Producer and existing CLI facade call exactly one D adapter | Implemented; GUI smoke pending |
| Editorial visibility | At least one non-empty non-`UNKNOWN` title/subtitle/CTA; GAME visible and PRE_ROLL/END_CTA/DONE hidden | 13 local tests cover core gate; Windows runtime pending |
| Source pins | Same exact E1 pin set at initial precheck, immediately before renderer capture, and post execution | Implemented; live receipt pending |
| Native source | Existing C11-C Drill launcher with `-NoSound`; 690/810 frames per existing contract | Windows capture pending |
| Music | `FAMILY_MUSIC_V4` via existing `C11CSafeAmbient.py`, `request.music_seed` only | Windows run pending |
| Seed experiment | A/B music 840001 exact repeat; C 840002 distinct; gameplay 12345 unchanged | Windows run pending |
| Bitstream isolation | A/C video stream SHA identical; audio stream SHA different | Windows FFmpeg/FFprobe receipt pending |
| Delivery | H.264 High 720x1280 30fps yuv420p TV + AAC-LC 48kHz stereo; sync/duration within adapter tolerances | Windows FFprobe pending |
| Governance | dispatch false; `release_authority=NONE`; no E1 status promotion or C11-C source mutation | Required in adapter receipt |

## Installer gate

Do not install until package inventory/SHA, seven user-accepted source pins, extra direct dependency pins, PowerShell 5.1 AST, destination preimages/add-only states, Python 3.13/PySide6 runtime, staged py_compile and 13 tests pass. Immediate pre-transaction pin/destination rechecks are mandatory. Rollback must restore only when the current file is the expected postimage and the backup matches the exact preimage; refuse unknown states. No Git checks, pip or shared dependency mutation.

The A/V result is an isolated qualification output. It does not close E4C or authorize general production media/dispatch. Continue E5 → E6 Smoke18 → E7 Matrix101 (99 provisional, CH_008/009 held) → E8.

---

## V9 current state — 2026-11-11

Consumer V8 stopped in `STAGED_VALIDATION` before any repository transaction. The exact cause was a StrictMode ordering bug in the installer: `$testSource` was inspected for the removed `QT_VERSION_STR` token before it was assigned from the staged test file. The run's journal is empty and `rollback=NOT_NEEDED`; no rollback or repository recovery is required. V9 fixes this by loading both `$consumerSource` and `$testSource` first, validating both are non-empty, and only then inspecting their contents. This is an installer-only correction. The Qt consumer, 35-test module and E1 service replacement bytes are unchanged from V8.

V9 also corrects the run ID and receipt/failure schema identities to V9. It preserves the 18-operation scope (one exact-pinned E1 service REPLACE + 17 D-owned ADDs), all 13 support pins, 10 design/font pins, exact-hash operator decisions, frozen C11-C manifest and no-new-dependency policy. The installer uses the existing canonical Producer Python/PySide6 only; it must not invoke pip, install/uninstall packages, change requirements or mutate shared environment dependencies.

V9 is a candidate only. Windows PowerShell 5.1 AST, Qt runtime probe, py_compile 3/3, tests 35/35, immediate pre-transaction rechecks and successful receipt are still pending. No consumer V1–V8 transaction has been recorded. Stop at first failure; do not repeat A.3 V5, binder V2, Godot V3, Loop22 or historical authoring accepted gates.

Next step: verify V9 ZIP SHA and sidecar, then run the V9 installer with the existing canonical `-PythonExe`. Require the same 18 destination states and all pre-write gates. After PASS, inspect `INSTALL_RECEIPT.json`, its SHA and all 18 postimages before any E1 integration review. C11-C remains sole production authority; renderer OFF; dispatch/media/audio OFF; `release_authority=NONE`.

---

## Current gate — E4C Drill Qt consumer V7 (2026-11-11)

## V8 current state — 2026-11-11

V7 failed closed in `STAGED_VALIDATION` before transaction. Its installer imported `QT_VERSION_STR` from `PySide6.QtCore`; the canonical PySide6 runtime does not export that symbol. This is an installer probe defect, not evidence that PySide6, Qt, QImage or QPainter is missing. The preceding imports of `PySide6.__version__` succeeded. `journal=[]`; `rollback=NOT_NEEDED`; no checkout write occurred.

V8 changes the probe to `from PySide6.QtCore import qVersion` and records `qVersion()` as the Qt runtime version. It requires Qt 6.x, alongside Python 3.13.x, existing PySide6 6.8–6.x, non-null RGB888 QImage and active QPainter. The official Qt for Python API lists `qVersion()` as a QtCore function. V8 does not install, upgrade or uninstall packages, invoke pip, edit requirements, or mutate the shared Python environment.

The consumer, its 35 Qt tests and the E1 service replacement are byte-identical to V7. No functional test result is inferred from the failed V7 runtime probe. V8 must still pass Windows PowerShell 5.1 AST, inventory/pins/destinations/staging, runtime probe, `py_compile` 3/3, all 35 Qt tests and immediate pre-transaction checks before any write. Do not repeat accepted A.3, binder V2, Godot V3, Loop22 or historical Drill authoring.

Governance remains unchanged: C11-C frozen manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; renderer OFF; dispatch/media/audio OFF; `release_authority=NONE`; operator manages commits; Git checks skipped.

### Consumer V8 gate
V7 failed before compilation/tests because the probe imported unsupported `QT_VERSION_STR`. V8 corrects this to `qVersion()`. Gate remains OPEN until canonical Python/PySide6/Qt offscreen probe, `py_compile` 3/3, tests 35/35, restored process environment and pre-transaction rechecks all PASS.

---


Consumer V6: `FAILED_CLOSED_PRE_TRANSACTION` at `STAGED_VALIDATION` because staged guide V15 lacked literal `No new Python dependency`. V6 had already passed rollback, AST, package inventory, pins, operator decisions, destination states and source staging. Evidence run `E4C_DRILL_VISUAL_PIXEL_CONSUMER_V6_20261111T004628_177cd6f5`; journal empty; rollback not needed.

Consumer V7: candidate only, not installed. Guide V16 explicitly prohibits new Python dependencies and removes the conflicting active Pillow instructions. Existing PySide6 Qt is reused. Acceptance requires Windows AST, full inventory/pins/destinations/staging, Qt probe, py_compile 3/3 and Qt test suite 35/35 before transaction. No pass is inferred from previous Pillow tests. No dependency changes are allowed.

---

## Current blocker — V6 Qt backend qualification (2026-11-11)

V4 consumer install failed closed because `PIL` was absent from canonical Python; no transaction occurred. V5's proposed global Pillow install is superseded/forbidden and must be rolled back. V6 reuses existing PySide6 and has rewritten consumer/tests. Gate is OPEN until Windows Qt runtime probe + py_compile 3/3 + all 35 new Qt tests pass. No accepted A.3/binder/Godot/Loop evidence is repeated.

## Current dependency blocker — V4 diagnostic

`PYTHON_PILLOW_RUNTIME.stderr.log` from run `E4C_DRILL_VISUAL_PIXEL_CONSUMER_V4_20261111T001315_ed8f8d25` contains `ModuleNotFoundError: No module named 'PIL'`. The interpreter is canonical Python 3.13.14; the dependency is absent. V1/V2/V4 are failed closed before transaction; V3 was superseded before Windows. V5 requires manual installation of Pillow 12.3.0 into that same runtime and RAQM verification before its installer can pass.

# C11-E Gates and Acceptance Matrix — V123 (2026-11-11)

| Gate | State | Evidence / boundary |
|---|---|---|
| E0–E3 | ACCEPTED_WITHIN_RECORDED_SCOPES | Reuse receipts; do not expand scope. |
| E4A Challenge | ACCEPTED_WITHIN_RECORDED_SCOPE | Do not repeat accepted visual/A/V/GUI evidence. |
| E4B Loop22 | CLOSED_OPERATOR_APPROVED | 44/44 A/V, 22/22 A/B, 25/25 tests and human visual/audio review. |
| Historical Drill authoring | PASS | 20/20 on 24 pins; authoring adapter only. |
| E4C binder V2 | PASS_ACTIVE_WINDOWS | 20/20 selectors, repeats, request manifests and lineage; 67/67 pins; receipt `31f631c3c23c6c1d277d67f52dd887010ee51be869798ab8db3fbdec8658fa01`. |
| E4C Godot console V3 | PASS_ACTIVE_WINDOWS | Receipt `526c7d360863af8fb53707c9c83162173f4c1f1eb349ee8d767fb97665167a31`; 4.7.1 Mono smoke and preflight reuse PASS. |
| A.1/A.3/B.1/D.1 decisions | PASS_BOUNDED | Exact record `49efd5494f351f09d7597c4699e9c12e361b36884b6bfadacd822e6ff1480e04`; recorded D-owned design/contract + delivery envelope only. |
| A.3 Drill design-contract | CLOSED_PASS_ACTIVE_WINDOWS | V5 receipt `d39eec2b3c1d969a3cb0d4e6aaa14b87aadcba74e42e58d283e00ea50768e881`; 3 replacements +26 adds; suites 33+5+7+10; py_compile 8/8. Do not rerun. |
| Drill phase ownership audit | PASS_READ_ONLY | Phase audit V2, 8 source pins /12 checks. |
| Drill geometry + timebase | APPROVED_AS_PROPOSED | Exact hashes approved by record `eb95da188065b8ebcb2371e2a6bcff6762ce000a5ca74f8ea384ecec4ee58303`, D-owned design/contract + isolated pixel tests only. |
| Consumer V1 | FAILED_CLOSED_PRE_TRANSACTION | Package omitted required guide V12; no transaction. |
| Consumer V2 | FAILED_CLOSED_PRE_TRANSACTION | Literal rollback-heading mismatch; empty journal; `rollback=NOT_NEEDED`. |
| Consumer V3 | SUPERSEDED_BEFORE_WINDOWS | Faithful V121 replay exposed missing `challenges/`, full `assets/`, `docs/current/d/`; no Windows attempt or transaction. |
| Consumer V4 | FAILED_CLOSED_PRE_TRANSACTION | All earlier Windows checks passed; Python 3.13.14 preflight failed with `ModuleNotFoundError: No module named 'PIL'`. No transaction. |
| Consumer V5 | DEPENDENCY_PREPARATION_PENDING | Adds D-owned `Pillow==12.3.0` requirements pin, explicit `-PythonExe`, exact Pillow-version and RAQM probe; no automatic package installation. After operator-managed prerequisite, Windows AST/runtime/py_compile 3/3/35 tests/receipt required. 19 operations (1 REPLACE +18 ADD). |
| E1 GUI/CLI + Qt runtime | OPEN | Only existing E1 shared service and existing Producer; actual source-frame observation required. |
| Drill family A/V | NOT_QUALIFIED | Silent protected C11-C capture, native `FAMILY_MUSIC_V4`, separate seeds, FFmpeg/FFprobe and human review; audio requires its own authority. |
| E5 | PENDING | Determinism, seed isolation, profile/binder non-leakage, GUI/CLI parity. |
| E6 Smoke18 | PENDING | Six complete A/V cases per family. |
| E7 Matrix101 | PENDING_SCOPED | 54 Challenge +27 Loop +20 Drill target; CH_008/009 held; 99 provisional. |
| E8 | BLOCKED_PENDING_E7 | Historical C-to-E row map, independent acceptance, freeze and separate explicit promotion. |

## Consumer V5 pre-transaction requirements

ZIP 25 members / 24 manifest rows; 19 typed operations; frozen C11-C manifest 796,318 bytes / SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; 13 support pins +10 approved design/font pins; operator decision checks; 18 destination states; short `%TEMP%` staging; staged guide V14, docket V7, phase audit V2 and incident register V5; stage-root check `STAGING_SOURCE_ROOTS=PASS_CHALLENGES_ASSETS_DOCS_CURRENT_D`; Python 3.13.x + exact Pillow 12.3.0 + RAQM (operator-managed; no auto-install); py_compile 3/3; tests 35/35; immediate pre-transaction rechecks. No checkout write before every check passes.

C11-C 2.19.12 remains sole production authority. Renderer OFF; dispatch/media false; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`.
