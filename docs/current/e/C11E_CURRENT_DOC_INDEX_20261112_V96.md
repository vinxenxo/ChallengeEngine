# DOCUMENT INDEX OVERRIDE — D99 locale failure and V1.4 repair — 2026-11-12

Latest authority: `C11E_CURRENT_AUTHORITY_20261112_V134.md`; latest gates `C11E_GATES_ACCEPTANCE_MATRIX_20261112_V129.md`; latest backlog `C11E_E3_EXECUTION_BACKLOG_20261112_V105.md`; blocker register V51; roadmap V77; E4C plan V22; installer incident register V14; runner style guide V20.

Latest E4C evidence record: `docs/history/c11e/C11E_E4C_DRILL_LOCALE_DECIMAL_ARGUMENT_FAILURE_20261112_V1.md`. The three continuity prompts at `prompts/` are updated to V135/V135/V59 and are included in the V1.4 overlay. The `D99-GUI-85201B7B4FF7` plan/parity artifacts pass; the first A/V capture is blocked by locale-sensitive speed argument conversion before C11-C capture. V1.4 is the only allowed repair candidate; V1.3 is installed, do not rerun it.



## D99-GUI-85201B7B4FF7 — single-selector A/V pilot diagnosis — 2026-11-12

**Authoritative evidence:** `D99-GUI-85201B7B4FF7.zip` SHA-256 `0913179f9852b7b1f75c2a7e2f763a111bc8d807d08d20036a2891ae94661f56`; `D99-GUI-85201B7B4FF7-tests.zip` SHA-256 `16f0e199429deffb85025cd35d0cfd4fe2ec9fe237cf66482f6de6b14cd6ef23`.

The GUI's **Resolver + Plan** stage is successful, not a failure: E1 receipt is `PASS_E1_PREPARATION_ONLY`; GUI/CLI semantic parity is `PASS`; D9.10 bridge planning is `PASS_BRIDGE_PLANNING_ONLY`; D composition plan is valid with real GAME-visible editorial; the request is `visual_drills / tracking / tier-1`, gameplay seed `12345`, music seed `840001`, `REVIEW_720`. This remains deliberately plan-only at E1 and does not claim renderer or dispatch activation. The second GUI action, the shared D A/V executor, fails before the native C11-C producer starts.

Exact failure from `logs/c11c_drill_producer.log`: C11-C's `run_visual_drill_production.ps1` rejects `-SpeedMultiplier` because it receives `75000`, outside `[ValidateRange(0.1,3.0)]`. The pinned profile `profiles/difficulty/visual_drill_tracking.json` has tier 1 `speed_multiplier=0.75` (source SHA-256 `6de8812bd46904e122ecdd0eae22fb2979bd75399c34779248c6569e833c921e`). The adapter applied Python's host decimal separator and sent `0,75000`. On the operator's locale, Windows PowerShell 5.1 parameter binding split/coerced that comma decimal and delivered `75000`. This is a cross-locale numeric argument-boundary defect in the D adapter, not a defect in the pinned C11-C launcher or difficulty profile.

The failure occurs before a successful C11-C capture. There is no native MP4, no D frame composition, no FAMILY_MUSIC_V4 WAV generation, no mux, and no final FFprobe result in this run. The failure does not indicate an editorial, font, Qt, geometry, phase/timebase, music determinism, or A/V stream-equivalence defect. The first evidence bundle contains `RUNNING` and `FAILURE` receipts and the exact native producer log. The `-tests.zip` is a preparation/parity/contract receipt bundle; it does not show a second independent A/V failure. Do not infer additional failures from its intentionally plan-only receipts.

**V1.4 correction:** remove host-locale formatting entirely. Python emits an ASCII invariant string such as `0.75000` to a string-typed PowerShell wrapper. The wrapper parses it with `[System.Globalization.CultureInfo]::InvariantCulture`, sets the wrapper thread culture to invariant for the call, then invokes the existing pinned C11-C launcher with an already-typed `[double]$speed`. The native C11-C launcher remains byte-identical and receives `0.75`; C11-C stays silent via `-NoSound`. The wrapper is retained in the run logs and its hash/argument are written into the execution receipt. Regression tests cover invariant formatting, wrapper parse/type handoff, and absence of host-locale formatting. The V1.4 installer additionally executes this exact wrapper against a dummy parameter-compatible launcher while forcing `es-ES`, and requires the dummy to record `0.75` before any repository mutation.

The failed output root `artifacts/production/c11e/D99-GUI-85201B7B4FF7` is intentionally preserved. It must not be overwritten. The retry must use a **new unique request_id/output root** (generate a fresh GUI request and repeat Resolver + Plan); do not delete or recycle this failed evidence. After V1.4 installation PASS: audit its postimages/source pins, rerun the GUI plan stage with a fresh ID, then execute only `tracking/tier-1`. Continue only when native capture, D composition, FAMILY_MUSIC_V4 A/B/C, final A/C video/audio stream hashes, FFprobe, and human visual/listening review pass. CLI smoke/parity follows on the same shared adapter. Do not start the 20-selector A/V matrix until the single-selector result is accepted.

Governance is unchanged: E1 `PREPARE_ONLY`; `family_adapter.status=NOT_CONNECTED_E1`; `production_dispatch=false`; `release_authority=NONE`; no Git checks; commits operator-managed; C11-C frozen manifest SHA remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.


---

## Installer V1.3 correction

V1.2 failed at transaction OP-001 because `File.Replace` received a null destination-backup path. V1.3 passes unique non-existing backup paths for both replacement and rollback, verifies SHA-256 of preserved pre/post images, and runs a two-direction disposable .NET API probe before transaction. See Installer Incident Register V13 and Installer Correction Record V3. Windows PS5.1 acceptance remains pending.

## V1.2 installer correction

The latest shared Drill A/V overlay candidate is V1.2. Its installer captures native Python stdout and stderr independently using .NET ProcessStartInfo; unittest's normal stderr progress is no longer interpreted as a PowerShell terminating error. See Installer Incident Register V12 and Installer Correction Record V2. V1.2 remains a candidate until Windows PS5.1 installation passes its full pre-write gates and transaction receipt.

## Current installer incident — V1.1

V1 failed in the staged Python version probe because PowerShell 5.1 altered a quote-bearing `python.exe -c` argument; the observed console error began `File "<string>", line 1`. The failure occurred before evidence/transaction creation. V1.1 invokes temporary `.py` files by path, compiles both probes, and writes a stage-specific `%TEMP%` failure diagnostic. See `docs/history/c11e/C11E_E4C_DRILL_SHARED_AV_INSTALLER_CORRECTION_20261111_V1.md`.

# DOCUMENT INDEX OVERRIDE — E4C SHARED A/V ADAPTER V1.1 — 2026-11-11

This increment records the GUI/CLI shared D execution boundary, the strict visible-editorial gate, pre/immediate-pre/post source pin validation, the single-selector A/V qualification contract, and the transactional installer. Use Authority V131, Gates V128, Backlog V104, Blocker V50, Roadmap V76 and E4C Plan V19 as this overlay's current documents. The implementation is `tools/c11d/d9/c11e_e4c_drill_execution.py`; only the existing Producer GUI and E1 CLI facade are modified. The corresponding historical records are under `docs/history/c11e/`; current continuation prompts are under `prompts/`.

---

## V9 current state — 2026-11-11

Consumer V8 stopped in `STAGED_VALIDATION` before any repository transaction. The exact cause was a StrictMode ordering bug in the installer: `$testSource` was inspected for the removed `QT_VERSION_STR` token before it was assigned from the staged test file. The run's journal is empty and `rollback=NOT_NEEDED`; no rollback or repository recovery is required. V9 fixes this by loading both `$consumerSource` and `$testSource` first, validating both are non-empty, and only then inspecting their contents. This is an installer-only correction. The Qt consumer, 35-test module and E1 service replacement bytes are unchanged from V8.

V9 also corrects the run ID and receipt/failure schema identities to V9. It preserves the 18-operation scope (one exact-pinned E1 service REPLACE + 17 D-owned ADDs), all 13 support pins, 10 design/font pins, exact-hash operator decisions, frozen C11-C manifest and no-new-dependency policy. The installer uses the existing canonical Producer Python/PySide6 only; it must not invoke pip, install/uninstall packages, change requirements or mutate shared environment dependencies.

V9 is a candidate only. Windows PowerShell 5.1 AST, Qt runtime probe, py_compile 3/3, tests 35/35, immediate pre-transaction rechecks and successful receipt are still pending. No consumer V1–V8 transaction has been recorded. Stop at first failure; do not repeat A.3 V5, binder V2, Godot V3, Loop22 or historical authoring accepted gates.

Next step: verify V9 ZIP SHA and sidecar, then run the V9 installer with the existing canonical `-PythonExe`. Require the same 18 destination states and all pre-write gates. After PASS, inspect `INSTALL_RECEIPT.json`, its SHA and all 18 postimages before any E1 integration review. C11-C remains sole production authority; renderer OFF; dispatch/media/audio OFF; `release_authority=NONE`.

---

## Latest index override — V89 / Consumer V7 (2026-11-11)

## V8 current state — 2026-11-11

V7 failed closed in `STAGED_VALIDATION` before transaction. Its installer imported `QT_VERSION_STR` from `PySide6.QtCore`; the canonical PySide6 runtime does not export that symbol. This is an installer probe defect, not evidence that PySide6, Qt, QImage or QPainter is missing. The preceding imports of `PySide6.__version__` succeeded. `journal=[]`; `rollback=NOT_NEEDED`; no checkout write occurred.

V8 changes the probe to `from PySide6.QtCore import qVersion` and records `qVersion()` as the Qt runtime version. It requires Qt 6.x, alongside Python 3.13.x, existing PySide6 6.8–6.x, non-null RGB888 QImage and active QPainter. The official Qt for Python API lists `qVersion()` as a QtCore function. V8 does not install, upgrade or uninstall packages, invoke pip, edit requirements, or mutate the shared Python environment.

The consumer, its 35 Qt tests and the E1 service replacement are byte-identical to V7. No functional test result is inferred from the failed V7 runtime probe. V8 must still pass Windows PowerShell 5.1 AST, inventory/pins/destinations/staging, runtime probe, `py_compile` 3/3, all 35 Qt tests and immediate pre-transaction checks before any write. Do not repeat accepted A.3, binder V2, Godot V3, Loop22 or historical Drill authoring.

Governance remains unchanged: C11-C frozen manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; renderer OFF; dispatch/media/audio OFF; `release_authority=NONE`; operator manages commits; Git checks skipped.

### Current additions
See Authority V128, Drill Plan V16, Consumer Spec V8, Runner Style Guide V17, Implementation Findings V9, Incident Register V8 and Master/Start/First prompts V129/V129/V53. V8's only code change is the installer Qt version probe from the invalid `QT_VERSION_STR` constant to `qVersion()`; consumer/test/E1 bytes remain unchanged.

---


Current authority is `C11E_CURRENT_AUTHORITY_20261111_V128.md`. The active E4C consumer candidate is `C11E_E4C_DRILL_VISUAL_PIXEL_CONSUMER_V7_20261111.zip`; V6 failed closed in staged validation because the V15 guide omitted a literal policy anchor and retained contradictory historical Pillow guidance. V7 carries runner guide V16, which forbids new Python dependencies and supersedes the old V14/V5 Pillow instructions. V7 is not installed; no transaction occurred in V6. Current plan is E4C Drill Plan V15; current blocker register V47; backlog V101; gate matrix V125; family roadmap V73; installer incident register V7; consumer implementation findings V8; Master/Start V128 and First V52 in root `prompts/`.

---

## Latest index override — V88 / Consumer V6 (2026-11-11)

Current blocker: V4 failed because the canonical Python did not have Pillow. The assistant's V5 global Pillow installation instruction was erroneous and the user rejected environment mutation. Roll back only the newly installed Pillow package. V6 reuses already-declared PySide6 and removes every Pillow/RAQM dependency. No pip, new package, global environment changes or C11-C requirements edits. V6's rewritten 35-test Qt suite must pass on Windows before transaction. V1/V2/V4 were failed before transaction; V3 superseded; V5 superseded/do not install.

## Latest index override — 2026-11-11

Current immediate blocker: canonical Python 3.13.14 has no Pillow module. Install the D-owned pinned dependency `Pillow==12.3.0` manually into the same Python used by the existing Producer, verify RAQM, then run Consumer V5 with explicit `-PythonExe`. Dependency pin: `tools/c11d/d9/requirements-visual-consumer.txt`. V1/V2/V4 failures are pre-transaction only; no consumer files are installed.

# C11-E Current Document Index — V87 (2026-11-11)

## Current authority and exact execution state

- Current Authority: `C11E_CURRENT_AUTHORITY_20261111_V126.md`
- Gates and Acceptance Matrix: `C11E_GATES_ACCEPTANCE_MATRIX_20261111_V124.md`
- Execution Backlog: `C11E_E3_EXECUTION_BACKLOG_20261111_V100.md`
- E4C Drill Execution Plan: `C11E_E4C_DRILL_EXECUTION_PLAN_20261111_V14.md`
- Blocker Remediation Register: `C11D_E_BLOCKER_REMEDIATION_REGISTER_20261111_V46.md`
- Full-Family Roadmap: `C11D_TO_C11E_FULL_FAMILY_ROADMAP_20261111_V72.md`
- Drill Composition Decision Docket: `C11E_E4C_DRILL_COMPOSITION_DECISION_DOCKET_20261110_V8.md`
- Drill Visual Consumer Specification: `C11E_E4C_DRILL_VISUAL_CONSUMER_SPEC_20261111_V6.md`
- PowerShell Runner Style Guide: `C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261111_V15.md`
- Installer Incident Register: `docs/history/c11e/C11E_INSTALLER_INCIDENT_REGISTER_20261111_V6.md`
- Consumer Implementation Findings: `docs/history/c11e/C11E_E4C_DRILL_VISUAL_PIXEL_CONSUMER_IMPLEMENTATION_20261111_V7.md`

## Continuity prompts — canonical root `prompts/`

- Master / Overhand: `C11E_CONTINUATION_MASTER_PROMPT_20261111_V127.md`
- Next Window Start: `C11E_NEXT_WINDOW_START_PROMPT_20261111_V127.md`
- First Prompt: `C11E_FIRST_PROMPT_20261111_V51.md`

## E4C evidence and status

- A.3 Drill design-contract V5 is installed and CLOSED/PASS. Receipt SHA `d39eec2b3c1d969a3cb0d4e6aaa14b87aadcba74e42e58d283e00ea50768e881`; 3 replacements +26 additions; suites 33+5+7+10; py_compile 8/8. Do not rerun.
- E4C binder V2 active Windows PASS: 20 selectors/repeats/request manifests/lineage, 67 pins; receipt `31f631c3c23c6c1d277d67f52dd887010ee51be869798ab8db3fbdec8658fa01`.
- Godot console V3 smoke PASS; receipt `526c7d360863af8fb53707c9c83162173f4c1f1eb349ee8d767fb97665167a31`; preflight reuse `9484a8fae7382d3e25159c347a6979514256009c5d2b7bbc8d7cbb2741b12672`.
- Consumer V1/V2 failed closed before transaction; V3 was superseded before Windows use after incomplete stage-root replay; V4 is the current Windows candidate. Faithful local V121 staging passed py_compile 3/3 and tests 35/35. Windows PS5.1 AST/runtime/install receipt remain pending.
- V4 contains 19 typed operations: 1 pinned E1 service replacement +17 D-owned adds. Test-stage roots include `challenges/`, full `assets/`, and `docs/current/d/` plus all prior required source roots. These are read-only stage inputs, not transaction operations.

## Approved decisions and limits

Geometry `b22f9eb6fce39f877e432ff5f0051ecf5ab8575ecb9f580fe5f158994222fc09` and GAME timebase `44ab3b0fa09a6f7d42cd8cf2f1122cada6cbffe16a7a6b53c2af5e88d5daddc8` are approved under record SHA `eb95da188065b8ebcb2371e2a6bcff6762ce000a5ca74f8ea384ecec4ee58303`, D-owned design/contract + isolated pixel tests only. A.1/A.3/B.1/D.1 remain within their earlier decision record SHA `49efd5494f351f09d7597c4699e9c12e361b36884b6bfadacd822e6ff1480e04` and bounded scopes.

## Roadmap

Finish Consumer V5 Windows gate → existing E1 shared GUI/CLI consumer integration → actual Qt Producer/source-frame review across all 20 selectors → separately authorized Drill family A/V using native `FAMILY_MUSIC_V4`, independent seeds, FFmpeg/FFprobe and human review → close E4C → E5 → E6 Smoke18 → E7 Matrix101 (99 provisional; CH_008/009 held) → E8 historical C-to-E regression, independent acceptance, freeze and separate explicit promotion. C11-C remains production authority; renderer OFF, dispatch/media false, release NONE.
