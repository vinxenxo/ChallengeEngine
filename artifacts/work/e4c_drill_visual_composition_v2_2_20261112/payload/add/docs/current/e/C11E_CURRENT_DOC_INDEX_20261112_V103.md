# DOCUMENT INDEX OVERRIDE — GUI single-selector A/V accepted; CLI smoke next — 2026-11-12


## Authoritative installer correction — V1.8 package-binding failure / V1.9 consolidated recovery (2026-11-12)

The operator's V1.8 run passed the ZIP sidecar and entered the package installer, then failed closed at `OPERATION_PACKAGE_FILE_BINDING_FAIL` for `docs/current/e/C11D_E_BLOCKER_REMEDIATION_REGISTER_20261112_V54.md`. The V1.8 builder renamed physical documentation payloads to the next versioned filenames (for example V55) but failed to regenerate the matching `replacements`/`additions` destination rows; several operation destinations still referenced their predecessor names. The validator correctly rejected the mismatch before the transaction journal or destination writes. This was a package-manifest construction defect, not a Windows runtime issue. Do not rerun V1.8.

V1.9 is a complete rebuilt overlay. Its operation rows are generated directly from the physical payload tree: `payload/replace/<relative>` maps only to `REPLACE <relative>`, and `payload/add/<relative>` maps only to `ADD_ONLY <relative>`. The installer independently enforces that mapping for every operation, verifies one-to-one closure between all payload files and operation rows, rejects duplicate package paths and destination paths, and checks manifest counters against actual arrays. The V1.9 matrix is exactly one existing D-consumer replacement plus 23 add-only destinations (24 mutation operations); package inventory also includes the README and installer. All versioned current-doc and prompt destinations now match their package paths exactly.

V1.9 preserves the V2 consumer, 18 focused tests, requalifier, runner, 21 support pins and 91-pin/CLI source evidence unchanged. The only changes from V1.8 are installer/manifest construction integrity, corrected operation destinations, documentation/prompt version increments, and incident recording. The V1.8 attempt failed before transaction; no checkout destination mutation occurred. V1.9 remains `NOT_YET_INSTALLED` pending its Windows 5.1/Python 3.13/PySide6 preflight and transaction receipt.

The V1.9 installer also reports pre-transaction failures distinctly as `FAIL_CLOSED_PRE_TRANSACTION_NO_DESTINATION_WRITES` with a `%TEMP%` diagnostic, rather than labelling an empty journal as a completed rollback. No Git, pip, shared dependency, GUI/CLI, E1, C11-C, dispatch or release changes are permitted.



## Authoritative update — V1.7 installer incident and V1.8 correction (2026-11-12)

V1.7 failed closed at `DESTINATION_PREFLIGHT` because it misclassified the newly introduced `tests/test_c11e_e4c_drill_visual_composition_consumer.py` as a replacement. The destination was absent in the active checkout. The declared preimage SHA `aedeb5754d94fdbaad134a653f57ca07466c845dcef081c8774668245455a7a0` is actually the historical V9 test stored under `tools/c11d/d9/`, not a preimage at the new `tests/` path. This is a manifest/installer classification defect, not a V2 consumer failure. The failure occurred before evidence-root and transaction-journal initialization; no destination writes or repository mutations occurred. Its generic `FAIL_CLOSED_ROLLBACK_COMPLETE` message reflects a zero-entry/no-op rollback.

V1.8 supersedes V1.7 and is the only candidate permitted for installation. Its operation matrix is exactly one hash-guarded replacement (`tools/c11d/d9/c11e_e4c_drill_visual_composition_consumer.py`) plus 22 `ADD_ONLY` destinations, including the new test module. The installer asserts the exact classification, unique operation destinations, and uses manifest-resolved package paths for staged inputs. It rechecks all source pins and all destination states before journaling/writing. Do not rerun V1.7. No source, GUI/CLI, E1 service, executor, C11-C or shared dependency changes are included.

V1.8 install status: `NOT_YET_INSTALLED`. Do not claim V2 Windows qualification from package/static checks. After install PASS, reuse the already accepted CLI native MP4 and WAV A/B/C for the existing-media V2 requalification; no new C11-C capture or music generation. E4C remains open, V2 A/V acceptance pending operator review, matrix not started. C11-C remains sole production authority; E1 PREPARE_ONLY / NOT_CONNECTED_E1; dispatch false; release authority NONE.

Latest authority: `C11E_CURRENT_AUTHORITY_20261112_V135.md`; gates V130; backlog V106; blocker V52; roadmap V78; E4C plan V23; installer incidents V15; continuity prompts V136/V136/V60.

New E4C history: `docs/history/c11e/C11E_E4C_DRILL_GUI_SINGLE_SELECTOR_AV_ACCEPTANCE_20261112_V1.md` and `docs/history/c11e/C11E_E4C_DRILL_CLI_SMOKE_PROCEDURE_20261112_V1.md`. CLI smoke runner: `tools/c11d/d9/RUN_C11E_E4C_DRILL_CLI_SMOKE_V1.ps1`; contract tests: `tests/test_c11e_e4c_cli_smoke_runner_contract.py`.

Current status: GUI `tracking/tier-1` A/V PASS with operator visual/audio acceptance and independent hashes; CLI-origin A/V execution pending; 20-selector matrix pending with this GUI pilot counted as row 1 (19 remaining). E4C is not yet closed.


**Current E4C position (2026-11-12):** the first single-selector GUI A/V qualification is accepted for `visual_drills / tracking / tier-1`. The operator confirmed visual and listening review PASS. Evidence `D99-GUI-6514F1066E79-production.zip` SHA-256 `5fb910dd7515ca1f80f2fa77a0829836613e933ca7106f00852ccd31d797f8e4`; tests/plan bundle `D99-GUI-6514F1066E79-tests.zip` SHA-256 `5c94ad64666548db478a4265a71345efe28c2a346f215e7cdb477f51dc8dde91`; qualification receipt SHA-256 `d8aad7176ed99d8bc0c067cece58272c5ac44045d55d746c768ea72324d459db`; RUNNING receipt SHA-256 `2f9b388b3541548d79c254161290ad73241109349aea1f57c1ac9c10e092ab2a`. The receipt status is `PASS_E4C_DRILL_SINGLE_SELECTOR_A_V_QUALIFICATION`.

**Independent audit:** 91/91 E1 source pins are identical at pre-execution, immediately-pre-render and post-execution; GUI/CLI E1 semantic identity parity PASS; 810/810 frames composed at 30 fps; phases PRE_ROLL/GAME/END_CTA = 90/630/90 frames; GAME editorial fields are populated and D-composed. `FAMILY_MUSIC_V4` `FLOWING_VECTOR` produces 27s, 44.1 kHz stereo PCM16; A/B seed 840001 WAV SHA `e54b960c799102fb104a99ccd7b94c4a41b5b22d54665acda72106b36646f277` is identical, C seed 840002 WAV SHA `5e81b6426f7915c7cad4c658fc24b90cd17c870a4497f45136a53e43b71efd40` differs. Final A and C are 27s, H.264 High 720×1280 yuv420p TV, 30 fps, 810 frames; AAC-LC 48 kHz stereo; both start at 0. Receipt stream hashes prove video A/C identical and audio A/C different; independent extraction also confirms raw H.264 SHA `500fc010b0d39062997d73643643943d03552082d75a2b8db6c55a3bbe5ad150` matches, while AAC elementary stream SHA differs (`23162fb059ca5e215758d6bbd58b6baba0efc9bd13e94d5921fd96726e19cd67` vs `f98747cc8f408521a3d00e7f4d90a066f3adf366de46d6f89bfefb65e26e86cd`). Final A SHA `7604f69e7c28e044a4bdb7fccc76c74604495ec9bbe4b46fcbca23a62b7c49ba`; final C SHA `d93753dabcfd85f3a3e721125081a649fbfa3a033a751e77a39df4c38357bf84`. Native source SHA `d10950bca9358de4ffe8a9f4f24c8c35cdb37e25050775a9220a4d15ffb45338`; silent D-composed intermediate SHA `60fd3155e70691bb7f2e636d20539e5898554669503888ee34bb78402c9589ad`.

Governance: C11-C frozen manifest remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; `c11c_source_mutation=false`; D3 V5 not invoked; source C11-C audio remains disabled via `-NoSound`; renderer invocation is solely the explicitly authorized isolated E4C qualification scope; `production_dispatch=false`; `release_authority=NONE`. E1 stays `PREPARE_ONLY`, `family_adapter.status=NOT_CONNECTED_E1`. Do not turn these isolated test results into production dispatch or release authority.

**Next gates:** (1) CLI-origin A/V smoke through the existing CLI facade with `--execute-drill-av --origin CLI`, using the same shared D executor and a fresh request ID; (2) 20-selector family A/V matrix; count the accepted GUI `tracking/tier-1` pilot as matrix row 1 and do not rerun it for matrix coverage; (3) E4C closeout only after CLI smoke, all remaining 19 selectors, receipts, human review and source-pin integrity. Then E5 → E6 Smoke18 → E7 Matrix101 (CH_008/009 held; 99 provisional) → E8 historical C-to-E regression, independent acceptance, freeze and separately authorized promotion.

---

## Superseded prior revision content

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


## V1.6 update — 2026-11-12
This index supersedes V97 for the V1.5 CLI smoke installer incident and its V1.6 recovery. New history: `C11E_E4C_CLI_SMOKE_INSTALLER_TIMEOUT_ARGS_BINDING_20261112_V1.md`. Updated Authority V136, Gates V131, Backlog V107, Blocker V53, Roadmap V79, E4C Plan V24, Incident Register V16 and continuity prompts Master/Start V137, First V61. V1.6 is add-only and installer correction only; CLI A/V remains open.


## V100 additions — 2026-11-12 E4C V2

- `C11E_E4C_DRILL_VISUAL_CONSUMER_SPEC_20261112_V10.md` — authoritative V2 social-body geometry and phase ownership.
- `C11E_E4C_DRILL_VISUAL_CONSUMER_V2_IMPLEMENTATION_20261112_V1.md` — implementation and focused test design.
- `C11E_E4C_DRILL_V1_COMPOSITION_ROOT_CAUSE_20261112_V1.md` — evidence-based incident/root-cause record.
- `C11E_E4C_DRILL_V2_EXISTING_MEDIA_REQUALIFICATION_20261112_V1.md` — no-capture/no-music requalification procedure.
- `C11E_E4C_DRILL_EDITORIAL_COMPOSITION_PROPOSAL_V2.json`, its schema, and exact user-direction record V2.
- `REQUALIFY_C11E_E4C_DRILL_AV_FROM_EXISTING_EVIDENCE_V2.py` and `RUN_C11E_E4C_DRILL_AV_EXISTING_MEDIA_V2_REQUALIFICATION.ps1`.
- `C11E_CONTINUATION_MASTER_PROMPT_20261112_V138.md`, `C11E_NEXT_WINDOW_START_PROMPT_20261112_V138.md`, `C11E_FIRST_PROMPT_20261112_V62.md`.

The CLI smoke package, original 91 E1 pins, native MP4 and A/B/C WAVs remain retained evidence. New V2 files are additive except the two explicitly hash-guarded D consumer/test replacements.

## V1.8 installer disposition and latest handoff

- Current Authority: `C11E_CURRENT_AUTHORITY_20261112_V138.md`.
- Gates: `C11E_GATES_ACCEPTANCE_MATRIX_20261112_V133.md`.
- Backlog: `C11E_E3_EXECUTION_BACKLOG_20261112_V109.md`.
- Blocker: `C11D_E_BLOCKER_REMEDIATION_REGISTER_20261112_V55.md`.
- Roadmap: `C11D_TO_C11E_FULL_FAMILY_ROADMAP_20261112_V81.md`.
- E4C Plan: `C11E_E4C_DRILL_EXECUTION_PLAN_20261112_V26.md`.
- Consumer specification: `C11E_E4C_DRILL_VISUAL_CONSUMER_SPEC_20261112_V11.md`.
- Installer incidents: `C11E_INSTALLER_INCIDENT_REGISTER_20261112_V18.md`.
- History: `C11E_E4C_DRILL_V1_7_INSTALLER_DESTINATION_CLASSIFICATION_20261112_V1.md`.
- Prompts: Master/Overhand V139, Start V139, First V63.

V1.7 is superseded and must not be rerun. V1.8 corrects the manifest classification to one replacement plus 22 add-only destinations. Windows installation and V2 existing-media qualification remain open.


## V1.9 consolidated package-binding recovery

- Current Authority: `C11E_CURRENT_AUTHORITY_20261112_V140.md`.
- Gates: `C11E_GATES_ACCEPTANCE_MATRIX_20261112_V135.md`.
- Backlog: `C11E_E3_EXECUTION_BACKLOG_20261112_V111.md`.
- Blocker: `C11D_E_BLOCKER_REMEDIATION_REGISTER_20261112_V57.md`.
- Roadmap: `C11D_TO_C11E_FULL_FAMILY_ROADMAP_20261112_V83.md`.
- E4C Plan: `C11E_E4C_DRILL_EXECUTION_PLAN_20261112_V28.md`.
- Consumer specification: `C11E_E4C_DRILL_VISUAL_CONSUMER_SPEC_20261112_V13.md`.
- Installer incidents: `C11E_INSTALLER_INCIDENT_REGISTER_20261112_V20.md`.
- New history: `C11E_E4C_DRILL_V1_8_INSTALLER_PACKAGE_BINDING_INCIDENT_20261112_V1.md`.
- Prompts: Master/Overhand V140, Start V140, First V64.

V1.8 is superseded. V1.9 package operation destinations are generated from actual payload paths and validated one-to-one. The installer remains not installed until a Windows receipt proves all checks and postimages.


## Authoritative update — V1.9 geometry contract test failure / V2.0 consolidated correction (2026-11-12)

The operator ran V1.9. Package SHA, 26/26 inventory, 21/21 support pins, frozen C11-C manifest and PowerShell AST 2/2 all passed. The installer then failed closed in `STAGING_AND_PYTHON_TESTS`, before transaction initialization or destination writes, because the staged consumer rejected `geometry.canvas` as a social-region mismatch; 0 tests ran. The installer created its failure diagnostic under the designated `artifacts/tests/c11e/e4c_v2_installer` evidence root; no source/destination operation was applied and the transaction journal remained empty.

Root cause is exact and localized in the V2 contract oracle. The V2 proposal's `geometry.canvas` contains five fields: `x`, `y`, `width`, `height`, and `aspect_ratio="9:16"`. Both `_verify_decision_and_proposals()` and `validate_plan()` compared it by exact dictionary equality against a four-field expectation that omitted `aspect_ratio`. The proposal is correct; the validator expectation was incomplete. It was duplicated in two independent validation sites, so both must use the same single canonical region constant.

V2.0 consolidates the correction: one `EXPECTED_SOCIAL_REGIONS` constant includes the exact 9:16 metadata and is used by proposal and plan validation; the frozen 540x960 logical `PresentationProfile.get_social_regions()` is checked against the exact 4/3 projection to 720x1280, yielding header 720x192, body 720x896 at y=192, and footer 720x192 at y=1088. Two tests are added: reject tampered aspect-ratio metadata and prove the logical-to-REVIEW_720 projection. Focused suite rises from 18 to 20 tests. No proposal, decision, timebase, C11-C, E1, GUI/CLI, execution adapter, music, binder, requalifier or runner behavior is changed.

V1.9 must not be rerun. V2.0 is a rebuilt overlay candidate; its Windows PySide6/Qt OFFSCREEN tests and transaction remain unqualified until the operator-run installer produces the complete receipt. No further installer iteration is authorized by this package record absent a new independent failure with evidence.

## V2.1 authoritative reconciliation (2026-11-12)

`E4C_OPEN_V2_REQUALIFICATION_PENDING`. Geometry V2 and the Test 04 boundary correction are accepted: `validate_plan()` now requires `source_frame_viewport == EXPECTED_SOCIAL_REGIONS["body_rect"]`. Reconciled consumer SHA-256: `e5cf97651e546ad86e2a4d46698553038e4161dc97a55da2654f197ed71f623c` (36,678 bytes); unchanged test SHA-256: `62327e32ed4c15b497efb4a93fecc1d484cebff0b79beaa7ced5099905ffb2bf`; isolated Python 3.13.14 evidence is py_compile PASS and 20/20 PASS.

V1.7 destination preflight, V1.8 operation/package binding, V1.9 geometry contract and V2.0 staging Test 04 failures are closed before transaction; none installed this correction. V2.1 is rebuilt and pending Windows installation, complete receipt and postimage review. Do not install V2.0 and do not repeat GUI, CLI smoke, native capture, music or Binder.

Preserve evidence GUI `D99-GUI-6514F1066E79`, CLI `E4C-CLI-SMOKE-20261112T091253Z-5a2e96b8`, native silent MP4, WAV A/B/C, seeds and bitstreams. V1 composition was visually rejected; `tracking/tier-1` is not yet an accepted V2 matrix row.

Required sequence: documentation; V2.1 installation; receipt/postimage audit; one existing-media requalification; seven-image/three-MP4 review; operator visual/audio acceptance; row 1/20; remaining 19; E4C close; E5, E6 Smoke18, E7 Matrix101, E8. C11-C 2.19.12 only; frozen manifest `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; E1 `PREPARE_ONLY / NOT_CONNECTED_E1`; no Git, pip, C11-C mutation, dispatch or release; operator-managed commits.
