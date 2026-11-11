## V9 current state — 2026-11-11

Consumer V8 stopped in `STAGED_VALIDATION` before any repository transaction. The exact cause was a StrictMode ordering bug in the installer: `$testSource` was inspected for the removed `QT_VERSION_STR` token before it was assigned from the staged test file. The run's journal is empty and `rollback=NOT_NEEDED`; no rollback or repository recovery is required. V9 fixes this by loading both `$consumerSource` and `$testSource` first, validating both are non-empty, and only then inspecting their contents. This is an installer-only correction. The Qt consumer, 35-test module and E1 service replacement bytes are unchanged from V8.

V9 also corrects the run ID and receipt/failure schema identities to V9. It preserves the 18-operation scope (one exact-pinned E1 service REPLACE + 17 D-owned ADDs), all 13 support pins, 10 design/font pins, exact-hash operator decisions, frozen C11-C manifest and no-new-dependency policy. The installer uses the existing canonical Producer Python/PySide6 only; it must not invoke pip, install/uninstall packages, change requirements or mutate shared environment dependencies.

V9 is a candidate only. Windows PowerShell 5.1 AST, Qt runtime probe, py_compile 3/3, tests 35/35, immediate pre-transaction rechecks and successful receipt are still pending. No consumer V1–V8 transaction has been recorded. Stop at first failure; do not repeat A.3 V5, binder V2, Godot V3, Loop22 or historical authoring accepted gates.

Next step: verify V9 ZIP SHA and sidecar, then run the V9 installer with the existing canonical `-PythonExe`. Require the same 18 destination states and all pre-write gates. After PASS, inspect `INSTALL_RECEIPT.json`, its SHA and all 18 postimages before any E1 integration review. C11-C remains sole production authority; renderer OFF; dispatch/media/audio OFF; `release_authority=NONE`.

---

## Incident V6 — policy anchor omitted and historical dependency guidance remained active (2026-11-11)

## V8 current state — 2026-11-11

V7 failed closed in `STAGED_VALIDATION` before transaction. Its installer imported `QT_VERSION_STR` from `PySide6.QtCore`; the canonical PySide6 runtime does not export that symbol. This is an installer probe defect, not evidence that PySide6, Qt, QImage or QPainter is missing. The preceding imports of `PySide6.__version__` succeeded. `journal=[]`; `rollback=NOT_NEEDED`; no checkout write occurred.

V8 changes the probe to `from PySide6.QtCore import qVersion` and records `qVersion()` as the Qt runtime version. It requires Qt 6.x, alongside Python 3.13.x, existing PySide6 6.8–6.x, non-null RGB888 QImage and active QPainter. The official Qt for Python API lists `qVersion()` as a QtCore function. V8 does not install, upgrade or uninstall packages, invoke pip, edit requirements, or mutate the shared Python environment.

The consumer, its 35 Qt tests and the E1 service replacement are byte-identical to V7. No functional test result is inferred from the failed V7 runtime probe. V8 must still pass Windows PowerShell 5.1 AST, inventory/pins/destinations/staging, runtime probe, `py_compile` 3/3, all 35 Qt tests and immediate pre-transaction checks before any write. Do not repeat accepted A.3, binder V2, Godot V3, Loop22 or historical Drill authoring.

Governance remains unchanged: C11-C frozen manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; renderer OFF; dispatch/media/audio OFF; `release_authority=NONE`; operator manages commits; Git checks skipped.

### Incident V7 — invalid PySide6 Qt version symbol
**Observed:** Windows V7 passed archive integrity, source/design pins, destination states, stage roots and PowerShell AST, then failed during staged runtime probe with `ImportError: cannot import name 'QT_VERSION_STR' from 'PySide6.QtCore'`.

**Root cause:** installer assumed a PySide6 binding constant not exported by the installed runtime. This did not demonstrate a missing PySide6 installation or broken QImage/QPainter.

**Correction:** V8 imports `qVersion` from `PySide6.QtCore`, calls `qVersion()`, emits the returned Qt version and requires major version 6. No dependency change is permitted.

**Disposition:** V7 failed closed in `STAGED_VALIDATION`; journal empty; rollback not needed; no repository mutation. V8 remains unqualified until its Windows runtime probe, py_compile and all 35 Qt tests pass.

---


**Observed:** V6 passed all package/source/decision/destination/staging preflights and stopped at staged-guide validation: `Staged PowerShell runner style guide V15 lacks required rule: No new Python dependency`.

**Evidence:** `E4C_DRILL_VISUAL_PIXEL_CONSUMER_V6_20261111T004628_177cd6f5.zip`; `INSTALL_FAILURE.json` records `stage=STAGED_VALIDATION`, `journal=[]`, `rollback_status=NOT_NEEDED`, renderer OFF, no media and release authority NONE.

**Root cause:** V15 stated that PySide6 must be reused and Pillow/RAQM/pip/environment mutation were forbidden, but omitted the installer's exact literal anchor. The same guide retained a V14 subsection that still described Pillow 12.3.0 provisioning. A phrase-only patch would have left a contradictory policy document.

**Correction:** V7 carries guide V16, which contains the exact normative phrase `No new Python dependency` and explicitly marks V14/V5 Pillow content as superseded and forbidden for this consumer. V7 installer references guide V16 and incident register V7. No code, E1 service, test or transaction operation has been expanded. No Python package installation is permitted.

**Disposition:** V6 FAILED_CLOSED_PRE_TRANSACTION; V7 candidate awaiting active Windows qualification. Do not repeat accepted gates or infer Qt acceptance from Pillow evidence.

---

## Incident V5 — assistant-directed shared Python mutation rejected (2026-11-11)

- **Action:** assistant incorrectly instructed user to install Pillow 12.3.0 into the canonical Producer Python. The `pip install` succeeded. The following inline Python probe failed with `SyntaxError` because PowerShell stripped nested double quotes; RAQM was not evaluated.
- **User correction:** shared Producer environment must not be modified to satisfy this D-owned consumer. This is accepted as a governance/architecture constraint.
- **Recovery:** uninstall only the newly added Pillow package; verify `importlib.util.find_spec('PIL')` is `None`. Do not uninstall/upgrade PySide6. No repository writes occurred because V5 installer was not run.
- **Correction:** V6 uses existing PySide6; no extra package, pip, requirements file or global environment change. Rewritten Qt tests are new evidence and must pass Windows qualification.

## Incident V4 — missing Pillow in canonical Python runtime (2026-11-11)

- **Run:** `E4C_DRILL_VISUAL_PIXEL_CONSUMER_V4_20261111T001315_ed8f8d25`.
- **Stage:** `STAGED_VALIDATION`; no transaction, `journal=[]`, `rollback=NOT_NEEDED`.
- **Checks passed:** ZIP SHA, rollback code inspection, PowerShell AST, package inventory, support pins, design/font pins, operator decisions, destination states, staging source-root contract, staged source/design pins and staged document dependencies.
- **Failure:** `PYTHON_PILLOW_RUNTIME.stderr.log` reports `ModuleNotFoundError: No module named 'PIL'`. The executable is the canonical Python 3.13.14 path used by historical project D99/E4C runs. This is an absent runtime dependency, not a Python version mismatch or consumer test failure. RAQM was not reached.
- **Cause:** V4 introduced a Pillow/RAQM runtime requirement but did not add an explicit D-owned dependency lock or operator setup step. Existing C11-C requirements declare PySide6 only.
- **Correction:** V5 adds `tools/c11d/d9/requirements-visual-consumer.txt` (`Pillow==12.3.0`), requires explicit `-PythonExe`, logs the selected runtime, checks exact Pillow version + RAQM and reports the manual install action. Installer does not use pip. Keep this dependency out of protected C11-C requirements.
- **Disposition:** V4 FAILED_CLOSED_PRE_TRANSACTION. V5 awaits operator-managed installation into the same Python runtime used by Producer, then Windows qualification. Do not retry V4 or repeat accepted suites.

# C11-E Installer Incident Register — V5

**Date:** 2026-11-10  
**Scope:** A.3 Drill design-contract V2–V5 and Consumer V1–V4 package/install recovery.  
**Active checkout:** `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`  
**Authority:** source SHA-256 pins + frozen C11-C manifest; operator-managed commits; no Git checks.

## Executive outcome

A.3 V5 is installed and accepted (3 pinned replacements +26 add-only files; changed-source suites 33+5+7+10 and py_compile 8/8). Consumer V1 and V2 failed closed before transaction. Consumer V3 was superseded before Windows execution because local faithful replay showed incomplete read-only stage inputs. Consumer V4 fixes that stage dependency closure; active Windows AST/runtime/tests/receipt remain pending. No Consumer V1–V4 transaction has occurred.

## Incident chronology

| Package | Stage / observed result | Root cause | Transaction | Corrective control |
|---|---|---|---|---|
| A.3 V2 | STAGED_VALIDATION; projected path 269 chars | Deep evidence path exceeded Windows path budget | Not started; `rollback=NOT_NEEDED` | Short `%TEMP%` stage and projected path ceiling. |
| A.3 V3 | STAGED_VALIDATION; StrictMode `.mode` access | Inventory metadata rows were traversed as operation rows | Not started | Validated `$operationEntries` payload subset only. |
| A.3 V4 | STAGED_VALIDATION; `Unknown option: -3` | Direct `python.exe` received py-launcher-only `-3.13` | Not started | Resolve direct Python 3.13 executable, probe version, invoke without selector. |
| A.3 V5 | `PASS_PINNED_REPLACEMENT_PLUS_ADD_ONLY` | Corrections integrated | Applied / accepted | Receipt retained; no repeat. |
| Consumer V1 | PACKAGE_PREFLIGHT; guide V12 missing | Installer required a guide absent from package | Not started | Bundle the guide as pinned ADD; validate package and stage postimage. |
| Consumer V2 | STAGED_VALIDATION; missing literal rollback anchor | Guide semantics were correct but lacked exact required heading | Not started; empty journal; `rollback=NOT_NEEDED` | Add explicit `Hash-guarded rollback` heading and inspect implementation guards. |
| Consumer V3 | Local source-stage replay failed before tests; no Windows attempt | Test stage omitted `challenges/`, full `assets/`, and `docs/current/d/` | Not started | Add all roots to path-budget check and read-only staging copy. |
| Consumer V4 | Faithful reconstructed V121 stage passes; Windows pending | Corrected stage dependency closure | Pending | Require Windows PS5.1 AST, complete preflight, Python/Pillow/RAQM, compile 3/3, tests 35/35 and exact receipt before write. |

## A.3 V5 active Windows acceptance evidence

- Run: `E4C_A3_DRILL_CONTRACT_V5_20261110T181034_fde3ca43`.
- Receipt: `artifacts/tests/c11e/e4c_a3_drill_contract_overlay/E4C_A3_DRILL_CONTRACT_V5_20261110T181034_fde3ca43/INSTALL_RECEIPT.json`.
- Receipt SHA-256: `d39eec2b3c1d969a3cb0d4e6aaa14b87aadcba74e42e58d283e00ea50768e881`.
- `PASS_PINNED_REPLACEMENT_PLUS_ADD_ONLY`; 3 replacements +26 additions; 13 support pins; AST/inventory PASS; staged 8-module compile and 33+5+7+10 suites PASS.
- Frozen C11-C manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; renderer OFF; release NONE.

## Consumer V1/V2 exact diagnostics

V1 run `E4C_DRILL_VISUAL_PIXEL_CONSUMER_V1_20261110T230315_e5929ed8`: ZIP SHA, AST, 21-member inventory, 13 support pins and 10 design/font pins passed; `PACKAGE_PREFLIGHT` then failed because guide V12 was missing from payload. No transaction.

V2 run `E4C_DRILL_VISUAL_PIXEL_CONSUMER_V2_20261110T232426_a8472872`: ZIP SHA, AST, 23-member inventory, 18 typed operations, 13+10 pins, exact operator decision scope, 18 destination states and 55-character `%TEMP%` root passed. `STAGED_VALIDATION` failed because the guide lacked literal `hash-guarded rollback`. Failure JSON records an empty journal, `rollback_status=NOT_NEEDED`, `renderer=OFF`, `media_created=false`, `release_authority=NONE`.

## Consumer V3/V4 source-stage findings

V3 was never attempted on active Windows. A faithful staged replay against the V121 nightly baseline found `challenges/CHALLENGE_004.json` missing. Adding only `challenges/` exposed `assets/c6/garage_background.svg`; adding full `assets/` exposed `docs/current/d/D1.5_PLATFORM_LAYOUT_TEMPLATE_CONTRACT.md`. This established the complete source-root closure required by the E1 → Drill binder → D9.9/D9.10 path. With all roots included, unchanged sources passed 35/35 locally under Python 3.13.5 / Pillow 12.3.0 / RAQM.

V4 path-budget-checks and copies `challenges/`, full `assets/`, and `docs/current/d/` read-only before Python. It asserts the roots exist and logs `STAGING_SOURCE_ROOTS=PASS_CHALLENGES_ASSETS_DOCS_CURRENT_D`. The transaction remains exactly 18 operations (one E1 service REPLACE +17 D-owned ADDs); stage baseline files are never transaction operations. V4 Windows acceptance and receipt remain pending.
