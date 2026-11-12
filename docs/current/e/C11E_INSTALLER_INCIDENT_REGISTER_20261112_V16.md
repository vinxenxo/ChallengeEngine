# INSTALLER AND RUNTIME INCIDENT REGISTER OVERRIDE — V1.4 GUI A/V acceptance — 2026-11-12

V1.4 locale-safe shared A/V adapter is now operational on the operator's Windows checkout. The operator's subsequent GUI-origin `tracking/tier-1` run reached native C11-C capture, D Qt composition, FAMILY_MUSIC_V4 A/B/C, FFmpeg/FFprobe and final mux. The complete A/V receipt reports `PASS_E4C_DRILL_SINGLE_SELECTOR_A_V_QUALIFICATION`, and the operator confirmed visual/audio review PASS. This closes the V1.4 runtime defect; no new installer or adapter repair is justified by this evidence.

Installer incidents V1–V1.3 remain documented below as historical failures and must not be rerun. V1.4 itself is the active installed runtime. The next V1.5 overlay is ADD_ONLY: new docs/prompts, one CLI smoke runner and its contract test; it does not replace any existing source module and uses no File.Replace.


**Current E4C position (2026-11-12):** the first single-selector GUI A/V qualification is accepted for `visual_drills / tracking / tier-1`. The operator confirmed visual and listening review PASS. Evidence `D99-GUI-6514F1066E79-production.zip` SHA-256 `5fb910dd7515ca1f80f2fa77a0829836613e933ca7106f00852ccd31d797f8e4`; tests/plan bundle `D99-GUI-6514F1066E79-tests.zip` SHA-256 `5c94ad64666548db478a4265a71345efe28c2a346f215e7cdb477f51dc8dde91`; qualification receipt SHA-256 `d8aad7176ed99d8bc0c067cece58272c5ac44045d55d746c768ea72324d459db`; RUNNING receipt SHA-256 `2f9b388b3541548d79c254161290ad73241109349aea1f57c1ac9c10e092ab2a`. The receipt status is `PASS_E4C_DRILL_SINGLE_SELECTOR_A_V_QUALIFICATION`.

**Independent audit:** 91/91 E1 source pins are identical at pre-execution, immediately-pre-render and post-execution; GUI/CLI E1 semantic identity parity PASS; 810/810 frames composed at 30 fps; phases PRE_ROLL/GAME/END_CTA = 90/630/90 frames; GAME editorial fields are populated and D-composed. `FAMILY_MUSIC_V4` `FLOWING_VECTOR` produces 27s, 44.1 kHz stereo PCM16; A/B seed 840001 WAV SHA `e54b960c799102fb104a99ccd7b94c4a41b5b22d54665acda72106b36646f277` is identical, C seed 840002 WAV SHA `5e81b6426f7915c7cad4c658fc24b90cd17c870a4497f45136a53e43b71efd40` differs. Final A and C are 27s, H.264 High 720×1280 yuv420p TV, 30 fps, 810 frames; AAC-LC 48 kHz stereo; both start at 0. Receipt stream hashes prove video A/C identical and audio A/C different; independent extraction also confirms raw H.264 SHA `500fc010b0d39062997d73643643943d03552082d75a2b8db6c55a3bbe5ad150` matches, while AAC elementary stream SHA differs (`23162fb059ca5e215758d6bbd58b6baba0efc9bd13e94d5921fd96726e19cd67` vs `f98747cc8f408521a3d00e7f4d90a066f3adf366de46d6f89bfefb65e26e86cd`). Final A SHA `7604f69e7c28e044a4bdb7fccc76c74604495ec9bbe4b46fcbca23a62b7c49ba`; final C SHA `d93753dabcfd85f3a3e721125081a649fbfa3a033a751e77a39df4c38357bf84`. Native source SHA `d10950bca9358de4ffe8a9f4f24c8c35cdb37e25050775a9220a4d15ffb45338`; silent D-composed intermediate SHA `60fd3155e70691bb7f2e636d20539e5898554669503888ee34bb78402c9589ad`.

Governance: C11-C frozen manifest remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; `c11c_source_mutation=false`; D3 V5 not invoked; source C11-C audio remains disabled via `-NoSound`; renderer invocation is solely the explicitly authorized isolated E4C qualification scope; `production_dispatch=false`; `release_authority=NONE`. E1 stays `PREPARE_ONLY`, `family_adapter.status=NOT_CONNECTED_E1`. Do not turn these isolated test results into production dispatch or release authority.

**Next gates:** (1) CLI-origin A/V smoke through the existing CLI facade with `--execute-drill-av --origin CLI`, using the same shared D executor and a fresh request ID; (2) 20-selector family A/V matrix; count the accepted GUI `tracking/tier-1` pilot as matrix row 1 and do not rerun it for matrix coverage; (3) E4C closeout only after CLI smoke, all remaining 19 selectors, receipts, human review and source-pin integrity. Then E5 → E6 Smoke18 → E7 Matrix101 (CH_008/009 held; 99 provisional) → E8 historical C-to-E regression, independent acceptance, freeze and separately authorized promotion.

---

## Superseded prior revision content

## V1.3 installation acceptance and separate E4C runtime defect — 2026-11-12

V1.3 was successfully installed on Windows: forward/rollback `File.Replace` API preflight PASS, 13/13 staged tests, 6/6 py_compile, and `PASS_REPLACE_AND_ADD_ONLY_INSTALL`. The next GUI A/V run exposed a runtime adapter issue, not an installer issue: locale-sensitive `0.75` speed formatting became `75000` at the C11-C PowerShell parameter boundary. The run stopped before native media generation; output root remains preserved. V1.4 changes the D adapter and tests, retains the V1.3 installer transaction model and adds a Windows `es-ES` typed-double wrapper smoke before writes.



## D99-GUI-85201B7B4FF7 — single-selector A/V pilot diagnosis — 2026-11-12

**Authoritative evidence:** `D99-GUI-85201B7B4FF7.zip` SHA-256 `0913179f9852b7b1f75c2a7e2f763a111bc8d807d08d20036a2891ae94661f56`; `D99-GUI-85201B7B4FF7-tests.zip` SHA-256 `16f0e199429deffb85025cd35d0cfd4fe2ec9fe237cf66482f6de6b14cd6ef23`.

The GUI's **Resolver + Plan** stage is successful, not a failure: E1 receipt is `PASS_E1_PREPARATION_ONLY`; GUI/CLI semantic parity is `PASS`; D9.10 bridge planning is `PASS_BRIDGE_PLANNING_ONLY`; D composition plan is valid with real GAME-visible editorial; the request is `visual_drills / tracking / tier-1`, gameplay seed `12345`, music seed `840001`, `REVIEW_720`. This remains deliberately plan-only at E1 and does not claim renderer or dispatch activation. The second GUI action, the shared D A/V executor, fails before the native C11-C producer starts.

Exact failure from `logs/c11c_drill_producer.log`: C11-C's `run_visual_drill_production.ps1` rejects `-SpeedMultiplier` because it receives `75000`, outside `[ValidateRange(0.1,3.0)]`. The pinned profile `profiles/difficulty/visual_drill_tracking.json` has tier 1 `speed_multiplier=0.75` (source SHA-256 `6de8812bd46904e122ecdd0eae22fb2979bd75399c34779248c6569e833c921e`). The adapter applied Python's host decimal separator and sent `0,75000`. On the operator's locale, Windows PowerShell 5.1 parameter binding split/coerced that comma decimal and delivered `75000`. This is a cross-locale numeric argument-boundary defect in the D adapter, not a defect in the pinned C11-C launcher or difficulty profile.

The failure occurs before a successful C11-C capture. There is no native MP4, no D frame composition, no FAMILY_MUSIC_V4 WAV generation, no mux, and no final FFprobe result in this run. The failure does not indicate an editorial, font, Qt, geometry, phase/timebase, music determinism, or A/V stream-equivalence defect. The first evidence bundle contains `RUNNING` and `FAILURE` receipts and the exact native producer log. The `-tests.zip` is a preparation/parity/contract receipt bundle; it does not show a second independent A/V failure. Do not infer additional failures from its intentionally plan-only receipts.

**V1.4 correction:** remove host-locale formatting entirely. Python emits an ASCII invariant string such as `0.75000` to a string-typed PowerShell wrapper. The wrapper parses it with `[System.Globalization.CultureInfo]::InvariantCulture`, sets the wrapper thread culture to invariant for the call, then invokes the existing pinned C11-C launcher with an already-typed `[double]$speed`. The native C11-C launcher remains byte-identical and receives `0.75`; C11-C stays silent via `-NoSound`. The wrapper is retained in the run logs and its hash/argument are written into the execution receipt. Regression tests cover invariant formatting, wrapper parse/type handoff, and absence of host-locale formatting. The V1.4 installer additionally executes this exact wrapper against a dummy parameter-compatible launcher while forcing `es-ES`, and requires the dummy to record `0.75` before any repository mutation.

The failed output root `artifacts/production/c11e/D99-GUI-85201B7B4FF7` is intentionally preserved. It must not be overwritten. The retry must use a **new unique request_id/output root** (generate a fresh GUI request and repeat Resolver + Plan); do not delete or recycle this failed evidence. After V1.4 installation PASS: audit its postimages/source pins, rerun the GUI plan stage with a fresh ID, then execute only `tracking/tier-1`. Continue only when native capture, D composition, FAMILY_MUSIC_V4 A/B/C, final A/C video/audio stream hashes, FFprobe, and human visual/listening review pass. CLI smoke/parity follows on the same shared adapter. Do not start the 20-selector A/V matrix until the single-selector result is accepted.

Governance is unchanged: E1 `PREPARE_ONLY`; `family_adapter.status=NOT_CONNECTED_E1`; `production_dispatch=false`; `release_authority=NONE`; no Git checks; commits operator-managed; C11-C frozen manifest SHA remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.


---

## Incident V1.2 — File.Replace called with null destination backup path (2026-11-11)

**Observed on Windows:** V1.2 passed package inventory, support pins, destination checks, Python/PySide6 probes, six-file `py_compile`, 13/13 staged tests and immediate pre-transaction rechecks. It entered `TRANSACTION_START`, journaled OP-001 for `c11c-suite/c11c-producer/main.py`, created and verified an exact preimage backup, then raised `System.IO.File.Replace` path-format error.

**Root cause:** Both forward replacement and rollback called `[System.IO.File]::Replace(source, destination, $null, $true)`. Windows PowerShell/.NET Framework rejected the null `destinationBackupFileName`. The same invalid pattern existed in rollback, so it was not sufficient to patch only the forward call.

**Evidence/state:** The operator diagnostic reports `rollback=COMPLETE`; OP-001 is `JOURNALED_BEFORE_MUTATION` and `rollback=ALREADY_PREIMAGE`. The destination SHA remained the original preimage. No C11-C source mutation, production dispatch or release authorization occurred.

**Correction:** V1.3 uses a unique, non-existing destination backup path for every forward `File.Replace`, journals it, and verifies that it contains the exact preimage. Rollback uses a second unique, non-existing path, journals it before mutation, verifies that it contains the displaced postimage and verifies the restored destination against the original preimage. A disposable same-volume forward+rollback `File.Replace` preflight runs in the isolated stage before the actual transaction.

**Disposition:** V1.2 is rejected. V1.3 remains unqualified until its actual Windows PS5.1 AST, transaction API preflight, runtime probes, six-file `py_compile`, 13/13 tests, immediate rechecks and full postimage/receipt checks pass.

---

## Incident V1.1 — Python unittest stderr misclassified as PowerShell failure (2026-11-11)

**Observed on Windows:** The V1.1 installer passed package extraction/inventory, source support pins, destination checks, Python 3.13 and PySide6/Qt probes, and staged `py_compile`. At `STAGED_UNIT_TESTS`, the failure diagnostic captured the first verbose unittest line ending `... ok`. The PowerShell stack points into `Invoke-Python`; the failure JSON has an empty transaction journal and `rollback=NOT_NEEDED`.

**Root cause:** `unittest -v` writes progress and summary to stderr. The V1.1 helper used `& $Exe @Arguments 2>&1` while the installer had `$ErrorActionPreference='Stop'`. Windows PowerShell 5.1 converted the native stderr stream to `NativeCommandError` and terminated before `$LASTEXITCODE` could establish process success. This was not a failing test; the observed test case had status `ok`.

**Correction:** V1.2 uses .NET `System.Diagnostics.ProcessStartInfo`, properly quotes Windows arguments, redirects stdout/stderr separately, starts both asynchronous stream reads before waiting, and uses the process exit code as the only pass/fail condition. It retains complete output for diagnostics. Tests are neither suppressed nor weakened.

**Disposition:** V1.1 failed closed before transaction; `journal=[]`, `rollback=NOT_NEEDED`, no repository writes. V1.2 is a candidate, not yet Windows-qualified. Require the installer to report `STAGED_TESTS=13/13`, `PY_COMPILE=6/6`, immediate rechecks and a complete postimage receipt before GUI/CLI smoke.

---

## Incident V1 — PowerShell 5.1 native argument quoting damaged Python `-c` probe (2026-11-11)

**Observed:** The operator extracted the complete V1 ZIP, verified package manifest and payload paths, then the installer failed in staged Python validation with `File "<string>", line 1`. The failure preceded `EvidenceRoot`, transaction journal creation and all checkout writes.

**Root cause:** The installer passed quote-bearing Python source through `python.exe -c` using a PowerShell 5.1 native executable argument array. PowerShell 5.1's native argument serialization can alter embedded quotes; the version probe's Python source therefore arrived malformed. The original V1 local Linux syntax/test checks did not exercise this Windows PowerShell-to-native-process boundary.

**Correction:** V1.1 creates two transient Python source files (`_installer_python_version_probe.py` and `_installer_pyside6_qt_probe.py`) inside the unique staging directory and invokes Python with each file path. Both probes are included in staged `py_compile`. No inline Python source remains in the installer. The installer also records `stage`, error and PowerShell stack trace in a failure JSON under `%TEMP%` so a pre-transaction fault is diagnosable without a repository write.

**Disposition:** V1 failed closed before transaction; no rollback required and no checkout mutation occurred. V1.1 is a corrected candidate, not yet Windows-qualified. Require PS5.1 AST, Python 3.13/PySide6/Qt probes, six-file `py_compile`, 13/13 tests, immediate source/destination rechecks and the transactional receipt before GUI/CLI smoke or A/V execution.

---

# CURRENT OVERLAY INCIDENT STATE — E4C A/V ADAPTER V1.1 — 2026-11-11

This package is a new candidate and has not been installed on the active Windows checkout. Earlier consumer V1–V9 incident records remain historical and are not repeated or reopened. The shared A/V installer has no active-Windows receipt at package issuance. Its pre-write gates and rollback behavior are described in E4C Plan V18 and the installation-contract history record.

Potential failure boundaries: missing canonical Python 3.13/PySide6; PS5.1 AST/runtime incompatibility; source pin drift; differing replacement preimage; add-only collision; stage compile/test failure; missing FFmpeg/FFprobe/Godot; native capture or composition failure; A/B non-repeatability; C seed not producing changed audio; A/C video hash mismatch; post-run source pin drift. Every failure must close without release authority and preserve the available diagnostic receipt.

---

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


**Observed:** V6 passed all package/source/decision/destination/staging preflights and stopped at staged-guide validation: `Staged PowerShell runner style guide V16 lacks required rule: No new Python dependency`.

**Evidence:** `E4C_DRILL_VISUAL_PIXEL_CONSUMER_V6_20261111T004628_177cd6f5.zip`; `INSTALL_FAILURE.json` records `stage=STAGED_VALIDATION`, `journal=[]`, `rollback_status=NOT_NEEDED`, renderer OFF, no media and release authority NONE.

**Root cause:** V16 stated that PySide6 must be reused and Pillow/RAQM/pip/environment mutation were forbidden, but omitted the installer's exact literal anchor. The same guide retained a V14 subsection that still described Pillow 12.3.0 provisioning. A phrase-only patch would have left a contradictory policy document.

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


## V1.5 CLI smoke overlay — staged Python timeout (2026-11-12)
Operator run passed package SHA, 19/19 source pins, PS AST 2/2, `ADD_OPERATIONS=15`; it failed closed in `STAGING_AND_PYTHON_TESTS` with `PYTHON_TIMEOUT: ;`. Diagnostic journal `[]`, rollback complete, no C11-C mutation, no production dispatch, release NONE. Diagnosis: installer `Invoke-Python` used reserved/colliding `$Args` parameter and positional array binding; command line was not surfaced. V1.6 replaces this with named `$PythonArguments`, named invocation, empty-array guards, redirected/closed stdin, command-line diagnostics and installer-contract regression tests. V1.6 remains add-only. Do not rerun V1.5.
