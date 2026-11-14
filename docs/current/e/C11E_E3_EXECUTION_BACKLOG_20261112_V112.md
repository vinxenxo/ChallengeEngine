# C11-E E4C V2.2 PIN-ALIGNMENT R1 — CURRENT AUTHORITATIVE STATE (2026-11-13)

**This block supersedes all earlier E4C V2 installer instructions below.** Older V1.7–V2.2 incidents remain historical evidence; do not rerun superseded packages.

## Active backlog and next actions

- The V2 design/consumer/test contract remains accepted in isolated qualification. Consumer SHA-256 `e5cf97651e546ad86e2a4d46698553038e4161dc97a55da2654f197ed71f623c` (36,678 bytes); unchanged test SHA-256 `62327e32ed4c15b497efb4a93fecc1d484cebff0b79beaa7ced5099905ffb2bf` (12,263 bytes); Python 3.13.14 compilation and the Qt-offscreen suite previously passed 20/20.
- The approved operator decision record is an immutable, content-pinned approval input: `docs/current/e/C11E_E4C_DRILL_COMPOSITION_OPERATOR_DECISION_RECORD_20261112_V2.json`, 2,925 bytes, SHA-256 `bceef9a22c27447ccbef5487339c25626e4cb4c5d32509809b832411655914e8`. The consumer constant `DECISION_SHA` is exactly this value. Do not edit or append execution state to this record. Put mutable execution state in the Authority, Gates, Backlog, Execution Plan, Incident Register and continuity prompts.
- The first reviewed package `ecfe23aca3de0474c717d03b1d719195612d754f8a5cd14b039fa1179cc1b3bf` was defective because its documentation update appended `latest_execution_state` to that pinned decision record, changing its SHA to `5d77eb624b0f14079a41a83776b5f6cbf7883cc55361f407d5cf5b34ea21c242`. This was correctly rejected by the staged consumer before tests or transaction. Do not use or rerun that ZIP.
- Operator installation attempt `C11E_E4C_DRILL_V2_V2_2_20261113T061938Z_c33b887a` failed closed at `STAGING_AND_PYTHON_TESTS`: `approved V2 design/source pin mismatch` for the decision record. Diagnostic: `artifacts/tests/c11e/e4c_v2_installer/C11E_E4C_DRILL_V2_V2_2_20261113T061938Z_c33b887a/INSTALL_FAILURE.json`. Transaction journal was empty (`[]`), rollback errors were empty, and the failure explicitly reports `FAIL_CLOSED_PRE_TRANSACTION_NO_DESTINATION_WRITES`. No replacement/addition destination was written; no C11-C source was changed; no dispatch or release authority was granted.
- The independent Windows path-specific preflight `C11E_E4C_DRILL_V2_V2_2_20261113T061924Z_7c2e5422` passed: path lengths 139/213/256/195 (evidence root/forward backup/rollback backup/max operation temp), Win32 limit 259; forward and rollback `File.Replace` PASS; probe cleanup PASS. It detected the old V2.1 temp sibling as `FOUND_EXPECTED_POSTIMAGE_PRESERVED`; that file was verified against the accepted consumer postimage and deliberately left untouched. Do not delete it.
- Corrective action: restore the decision record byte-for-byte from the approved V2.2 source (`bceef9a22c27447ccbef5487339c25626e4cb4c5d32509809b832411655914e8`), retain the consumer/test/installer payloads unchanged, and keep operational state exclusively in mutable documentation. No functional consumer, test, installer, or source-pin change is authorized by this correction.

## Corrected package and next action

Use **`C11E_E4C_DRILL_VISUAL_COMPOSITION_V2_REQUALIFICATION_V2_2_PIN_ALIGNED_R1_20261113.zip`** and its adjacent `.sha256` sidecar only. Extract to the new directory `C11E_E4C_DRILL_VISUAL_COMPOSITION_V2_REQUALIFICATION_V2_2_PIN_ALIGNED_R1_20261113` in Downloads; never extract over the active checkout. The installer remains `22f097f672fffcc855e0080ed590bffc8fbe6b3142f3ca57bb270ec2f1883414`. Package shape remains one exact consumer replacement + 24 ADD_ONLY additions, 21 source pins, 27 package files, and the unchanged 20-test suite.

The separate path-specific `File.Replace` probe has already passed against the exact V2.2 installer/path strategy. This pin-alignment correction changes only the decision-record payload and documentation/manifest hashes; it does not alter the installer or any destination path. Do not rerun the standalone probe. The installer itself still performs its own staged checks and its built-in forward/rollback `File.Replace` preflight before any transaction write.

1. Verify the new ZIP using its sidecar, extract to the new package directory, and run the V2.2 installer once with `-PackageZip` set to this exact ZIP.
2. Require package inventory 27/27, source pins 21/21, frozen C11-C manifest PASS, PowerShell AST 2/2, 1 REPLACE + 24 ADD_ONLY, Python runtime/PySide6/Qt-offscreen PASS, py_compile 3/3, staged tests 20/20, built-in File.Replace preflight PASS, immediate recheck PASS, and final `PASS_REPLACE_AND_ADD_ONLY_INSTALL`.
3. On any failure, stop and preserve the full `INSTALL_FAILURE.json`, transaction journal and console output. Do not repeat the installer blindly. Since this failure was pre-transaction, no rollback/recovery work is needed.
4. After install success, audit the receipt, journal, 25 destination postimages and 21 unchanged source pins. Only then run the existing-media V2 A/V requalification once.
5. Do not repeat the accepted GUI/CLI smoke, native captures, music generation, E4B Loop22, Binder or pixel qualifications. Reuse the preserved CLI native MP4 and WAV A/B/C.

## E4C gate state and forward roadmap

- V2 isolated consumer/tests: **PASS**.
- V2.2 path-specific forward/rollback `File.Replace`: **PASS**.
- V2.2 Windows installation: **BLOCKED / NOT INSTALLED** by the pinned decision-record mismatch in the superseded ZIP; corrected pin-alignment R1 candidate prepared, Windows execution pending.
- Existing-media A/V V2 requalification: **NOT RUN / PENDING INSTALL PASS**.
- V2 operator visual/audio acceptance: **PENDING**; `tracking/tier-1` remains 0/20 V2 rows.
- After V2 acceptance, run remaining 19 selectors, close E4C at 20/20, then E5 → E6 Smoke18 → E7 Matrix101 (CH_008/009 held; 99 provisional) → E8 historical C-to-E regression, independent acceptance, immutable freeze and separately authorized promotion.

## Permanent governance

Active checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS` is sole source authority. `GIT_CHECKS=SKIPPED`; `COMMITS=OPERATOR_MANAGED`; no pip or shared dependency changes. C11-C 2.19.12 remains sole production authority; frozen manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. E1 `PREPARE_ONLY`; `family_adapter.status=NOT_CONNECTED_E1`; no C11-C mutation, no production dispatch, `release_authority=NONE`.

---

# CURRENT BACKLOG OVERRIDE — GUI pilot accepted; CLI smoke → 19 remaining A/V selectors — 2026-11-12


## Authoritative installer correction — V1.8 package-binding failure / V1.9 consolidated recovery (2026-11-12)

The operator's V1.8 run passed the ZIP sidecar and entered the package installer, then failed closed at `OPERATION_PACKAGE_FILE_BINDING_FAIL` for `docs/current/e/C11D_E_BLOCKER_REMEDIATION_REGISTER_20261112_V54.md`. The V1.8 builder renamed physical documentation payloads to the next versioned filenames (for example V55) but failed to regenerate the matching `replacements`/`additions` destination rows; several operation destinations still referenced their predecessor names. The validator correctly rejected the mismatch before the transaction journal or destination writes. This was a package-manifest construction defect, not a Windows runtime issue. Do not rerun V1.8.

V1.9 is a complete rebuilt overlay. Its operation rows are generated directly from the physical payload tree: `payload/replace/<relative>` maps only to `REPLACE <relative>`, and `payload/add/<relative>` maps only to `ADD_ONLY <relative>`. The installer independently enforces that mapping for every operation, verifies one-to-one closure between all payload files and operation rows, rejects duplicate package paths and destination paths, and checks manifest counters against actual arrays. The V1.9 matrix is exactly one existing D-consumer replacement plus 23 add-only destinations (24 mutation operations); package inventory also includes the README and installer. All versioned current-doc and prompt destinations now match their package paths exactly.

V1.9 preserves the V2 consumer, 18 focused tests, requalifier, runner, 21 support pins and 91-pin/CLI source evidence unchanged. The only changes from V1.8 are installer/manifest construction integrity, corrected operation destinations, documentation/prompt version increments, and incident recording. The V1.8 attempt failed before transaction; no checkout destination mutation occurred. V1.9 remains `NOT_YET_INSTALLED` pending its Windows 5.1/Python 3.13/PySide6 preflight and transaction receipt.

The V1.9 installer also reports pre-transaction failures distinctly as `FAIL_CLOSED_PRE_TRANSACTION_NO_DESTINATION_WRITES` with a `%TEMP%` diagnostic, rather than labelling an empty journal as a completed rollback. No Git, pip, shared dependency, GUI/CLI, E1, C11-C, dispatch or release changes are permitted.



## Authoritative update — V1.7 installer incident and V1.8 correction (2026-11-12)

V1.7 failed closed at `DESTINATION_PREFLIGHT` because it misclassified the newly introduced `tests/test_c11e_e4c_drill_visual_composition_consumer.py` as a replacement. The destination was absent in the active checkout. The declared preimage SHA `aedeb5754d94fdbaad134a653f57ca07466c845dcef081c8774668245455a7a0` is actually the historical V9 test stored under `tools/c11d/d9/`, not a preimage at the new `tests/` path. This is a manifest/installer classification defect, not a V2 consumer failure. The failure occurred before evidence-root and transaction-journal initialization; no destination writes or repository mutations occurred. Its generic `FAIL_CLOSED_ROLLBACK_COMPLETE` message reflects a zero-entry/no-op rollback.

V1.8 supersedes V1.7 and is the only candidate permitted for installation. Its operation matrix is exactly one hash-guarded replacement (`tools/c11d/d9/c11e_e4c_drill_visual_composition_consumer.py`) plus 22 `ADD_ONLY` destinations, including the new test module. The installer asserts the exact classification, unique operation destinations, and uses manifest-resolved package paths for staged inputs. It rechecks all source pins and all destination states before journaling/writing. Do not rerun V1.7. No source, GUI/CLI, E1 service, executor, C11-C or shared dependency changes are included.

V1.8 install status: `NOT_YET_INSTALLED`. Do not claim V2 Windows qualification from package/static checks. After install PASS, reuse the already accepted CLI native MP4 and WAV A/B/C for the existing-media V2 requalification; no new C11-C capture or music generation. E4C remains open, V2 A/V acceptance pending operator review, matrix not started. C11-C remains sole production authority; E1 PREPARE_ONLY / NOT_CONNECTED_E1; dispatch false; release authority NONE.

1. Run the new add-only V1.5 installer (docs + CLI smoke runner only), verify `PASS_ADD_ONLY_INSTALL` and all pins.
2. Execute CLI-origin A/V smoke for `tracking/tier-1` using a fresh request ID and the existing `c11e_production_cli.py --origin CLI --execute-drill-av`; preserve its receipt.
3. Once CLI smoke passes, run the remaining 19 A/V selectors across `tracking`, `pursuit`, `saccade`, `peripheral_scan` × `tier-1..tier-5`. The accepted GUI `tracking/tier-1` result is matrix row 1; do not rerun it.
4. Verify every row's A/B repeat determinism, changed-C audio, A/C identical video, A/C different audio, D frame count/phase mapping, family-music binding and per-run pre/post source pins. Operator visual/audio review per family and exception rows.
5. Close E4C only after CLI smoke and 20/20 matrix rows PASS; then begin E5 determinism/seed separation/profile-binder non-leakage/GUI-CLI parity. E6 Smoke18, E7 Matrix101 (99 provisional; CH_008/009 held), E8 regression/independent acceptance/freeze/separate promotion follow.


**Current E4C position (2026-11-12):** the first single-selector GUI A/V qualification is accepted for `visual_drills / tracking / tier-1`. The operator confirmed visual and listening review PASS. Evidence `D99-GUI-6514F1066E79-production.zip` SHA-256 `5fb910dd7515ca1f80f2fa77a0829836613e933ca7106f00852ccd31d797f8e4`; tests/plan bundle `D99-GUI-6514F1066E79-tests.zip` SHA-256 `5c94ad64666548db478a4265a71345efe28c2a346f215e7cdb477f51dc8dde91`; qualification receipt SHA-256 `d8aad7176ed99d8bc0c067cece58272c5ac44045d55d746c768ea72324d459db`; RUNNING receipt SHA-256 `2f9b388b3541548d79c254161290ad73241109349aea1f57c1ac9c10e092ab2a`. The receipt status is `PASS_E4C_DRILL_SINGLE_SELECTOR_A_V_QUALIFICATION`.

**Independent audit:** 91/91 E1 source pins are identical at pre-execution, immediately-pre-render and post-execution; GUI/CLI E1 semantic identity parity PASS; 810/810 frames composed at 30 fps; phases PRE_ROLL/GAME/END_CTA = 90/630/90 frames; GAME editorial fields are populated and D-composed. `FAMILY_MUSIC_V4` `FLOWING_VECTOR` produces 27s, 44.1 kHz stereo PCM16; A/B seed 840001 WAV SHA `e54b960c799102fb104a99ccd7b94c4a41b5b22d54665acda72106b36646f277` is identical, C seed 840002 WAV SHA `5e81b6426f7915c7cad4c658fc24b90cd17c870a4497f45136a53e43b71efd40` differs. Final A and C are 27s, H.264 High 720×1280 yuv420p TV, 30 fps, 810 frames; AAC-LC 48 kHz stereo; both start at 0. Receipt stream hashes prove video A/C identical and audio A/C different; independent extraction also confirms raw H.264 SHA `500fc010b0d39062997d73643643943d03552082d75a2b8db6c55a3bbe5ad150` matches, while AAC elementary stream SHA differs (`23162fb059ca5e215758d6bbd58b6baba0efc9bd13e94d5921fd96726e19cd67` vs `f98747cc8f408521a3d00e7f4d90a066f3adf366de46d6f89bfefb65e26e86cd`). Final A SHA `7604f69e7c28e044a4bdb7fccc76c74604495ec9bbe4b46fcbca23a62b7c49ba`; final C SHA `d93753dabcfd85f3a3e721125081a649fbfa3a033a751e77a39df4c38357bf84`. Native source SHA `d10950bca9358de4ffe8a9f4f24c8c35cdb37e25050775a9220a4d15ffb45338`; silent D-composed intermediate SHA `60fd3155e70691bb7f2e636d20539e5898554669503888ee34bb78402c9589ad`.

Governance: C11-C frozen manifest remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; `c11c_source_mutation=false`; D3 V5 not invoked; source C11-C audio remains disabled via `-NoSound`; renderer invocation is solely the explicitly authorized isolated E4C qualification scope; `production_dispatch=false`; `release_authority=NONE`. E1 stays `PREPARE_ONLY`, `family_adapter.status=NOT_CONNECTED_E1`. Do not turn these isolated test results into production dispatch or release authority.

**Next gates:** (1) CLI-origin A/V smoke through the existing CLI facade with `--execute-drill-av --origin CLI`, using the same shared D executor and a fresh request ID; (2) 20-selector family A/V matrix; count the accepted GUI `tracking/tier-1` pilot as matrix row 1 and do not rerun it for matrix coverage; (3) E4C closeout only after CLI smoke, all remaining 19 selectors, receipts, human review and source-pin integrity. Then E5 → E6 Smoke18 → E7 Matrix101 (CH_008/009 held; 99 provisional) → E8 historical C-to-E regression, independent acceptance, freeze and separately authorized promotion.

---

## Superseded prior revision content

1. Install the V1.4 locale-safe adapter overlay on the active Windows checkout. Require PowerShell 5.1 AST; staged Python 3.13/PySide6; 16/16 tests; `py_compile`; `INVARIANT_SPEED_WRAPPER=PASS` under forced `es-ES`; immediate pins/destination rechecks; complete transaction receipt.
2. Verify all replacements/additions and source pins after installation. Preserve D99 failed run.
3. Create a fresh GUI request ID, run Resolver + Plan, then one `tracking/tier-1` A/V execution with gameplay 12345, music A/B 840001, C 840002, REVIEW_720, audio/personalization ON, real editorial.
4. Inspect native manifest/MP4, per-frame D receipt, A/B/C music, mux, FFprobe, A/C video/audio stream hashes and human visual/listening review.
5. Run CLI opt-in smoke against same adapter. Only then qualify 20 selectors and close E4C.

Do not repeat accepted 20 native source captures, 100/100 visual composition tests, Binder V2, E4B Loop22, or historical Drill authoring without source-pin drift.



## D99-GUI-85201B7B4FF7 — single-selector A/V pilot diagnosis — 2026-11-12

**Authoritative evidence:** `D99-GUI-85201B7B4FF7.zip` SHA-256 `0913179f9852b7b1f75c2a7e2f763a111bc8d807d08d20036a2891ae94661f56`; `D99-GUI-85201B7B4FF7-tests.zip` SHA-256 `16f0e199429deffb85025cd35d0cfd4fe2ec9fe237cf66482f6de6b14cd6ef23`.

The GUI's **Resolver + Plan** stage is successful, not a failure: E1 receipt is `PASS_E1_PREPARATION_ONLY`; GUI/CLI semantic parity is `PASS`; D9.10 bridge planning is `PASS_BRIDGE_PLANNING_ONLY`; D composition plan is valid with real GAME-visible editorial; the request is `visual_drills / tracking / tier-1`, gameplay seed `12345`, music seed `840001`, `REVIEW_720`. This remains deliberately plan-only at E1 and does not claim renderer or dispatch activation. The second GUI action, the shared D A/V executor, fails before the native C11-C producer starts.

Exact failure from `logs/c11c_drill_producer.log`: C11-C's `run_visual_drill_production.ps1` rejects `-SpeedMultiplier` because it receives `75000`, outside `[ValidateRange(0.1,3.0)]`. The pinned profile `profiles/difficulty/visual_drill_tracking.json` has tier 1 `speed_multiplier=0.75` (source SHA-256 `6de8812bd46904e122ecdd0eae22fb2979bd75399c34779248c6569e833c921e`). The adapter applied Python's host decimal separator and sent `0,75000`. On the operator's locale, Windows PowerShell 5.1 parameter binding split/coerced that comma decimal and delivered `75000`. This is a cross-locale numeric argument-boundary defect in the D adapter, not a defect in the pinned C11-C launcher or difficulty profile.

The failure occurs before a successful C11-C capture. There is no native MP4, no D frame composition, no FAMILY_MUSIC_V4 WAV generation, no mux, and no final FFprobe result in this run. The failure does not indicate an editorial, font, Qt, geometry, phase/timebase, music determinism, or A/V stream-equivalence defect. The first evidence bundle contains `RUNNING` and `FAILURE` receipts and the exact native producer log. The `-tests.zip` is a preparation/parity/contract receipt bundle; it does not show a second independent A/V failure. Do not infer additional failures from its intentionally plan-only receipts.

**V1.4 correction:** remove host-locale formatting entirely. Python emits an ASCII invariant string such as `0.75000` to a string-typed PowerShell wrapper. The wrapper parses it with `[System.Globalization.CultureInfo]::InvariantCulture`, sets the wrapper thread culture to invariant for the call, then invokes the existing pinned C11-C launcher with an already-typed `[double]$speed`. The native C11-C launcher remains byte-identical and receives `0.75`; C11-C stays silent via `-NoSound`. The wrapper is retained in the run logs and its hash/argument are written into the execution receipt. Regression tests cover invariant formatting, wrapper parse/type handoff, and absence of host-locale formatting. The V1.4 installer additionally executes this exact wrapper against a dummy parameter-compatible launcher while forcing `es-ES`, and requires the dummy to record `0.75` before any repository mutation.

The failed output root `artifacts/production/c11e/D99-GUI-85201B7B4FF7` is intentionally preserved. It must not be overwritten. The retry must use a **new unique request_id/output root** (generate a fresh GUI request and repeat Resolver + Plan); do not delete or recycle this failed evidence. After V1.4 installation PASS: audit its postimages/source pins, rerun the GUI plan stage with a fresh ID, then execute only `tracking/tier-1`. Continue only when native capture, D composition, FAMILY_MUSIC_V4 A/B/C, final A/C video/audio stream hashes, FFprobe, and human visual/listening review pass. CLI smoke/parity follows on the same shared adapter. Do not start the 20-selector A/V matrix until the single-selector result is accepted.

Governance is unchanged: E1 `PREPARE_ONLY`; `family_adapter.status=NOT_CONNECTED_E1`; `production_dispatch=false`; `release_authority=NONE`; no Git checks; commits operator-managed; C11-C frozen manifest SHA remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.


---

# CURRENT BACKLOG OVERRIDE — 2026-11-11

1. Install the shared E4C Drill GUI/CLI overlay only after its PS5.1 installer completes all pre-write gates.
2. Inspect install receipt and exact postimages; then perform a GUI launch/resolver/plan smoke on active Windows without rendering.
3. Run one fully populated `tracking/tier-1` A/V qualification: gameplay seed 12345; music A/B 840001; changed C 840002; REVIEW_720; audio ON; personalization ON; at least one visible title/subtitle/CTA.
4. Review receipt, source pin pre/immediate-pre/post equality, source frame identity, phase counts, native FAMILY_MUSIC_V4 A/B/C, final FFprobe streams, A/C video identity/audio change, listening and visual review.
5. Only after one selector is accepted, schedule 20-selector A/V matrix; do not repeat the 20 native source captures or 100/100 pixel qualification absent pin drift.
6. Close E4C only after shared GUI/CLI, single-selector and matrix A/V acceptance, and operator review. Then E5 determinism/seed isolation/profile/binder non-leakage; E6 Smoke18; E7 Matrix101 (99 provisional, CH_008/009 held); E8 independent historical regression, freeze and separate promotion.

---

## V9 current state — 2026-11-11

Consumer V8 stopped in `STAGED_VALIDATION` before any repository transaction. The exact cause was a StrictMode ordering bug in the installer: `$testSource` was inspected for the removed `QT_VERSION_STR` token before it was assigned from the staged test file. The run's journal is empty and `rollback=NOT_NEEDED`; no rollback or repository recovery is required. V9 fixes this by loading both `$consumerSource` and `$testSource` first, validating both are non-empty, and only then inspecting their contents. This is an installer-only correction. The Qt consumer, 35-test module and E1 service replacement bytes are unchanged from V8.

V9 also corrects the run ID and receipt/failure schema identities to V9. It preserves the 18-operation scope (one exact-pinned E1 service REPLACE + 17 D-owned ADDs), all 13 support pins, 10 design/font pins, exact-hash operator decisions, frozen C11-C manifest and no-new-dependency policy. The installer uses the existing canonical Producer Python/PySide6 only; it must not invoke pip, install/uninstall packages, change requirements or mutate shared environment dependencies.

V9 is a candidate only. Windows PowerShell 5.1 AST, Qt runtime probe, py_compile 3/3, tests 35/35, immediate pre-transaction rechecks and successful receipt are still pending. No consumer V1–V8 transaction has been recorded. Stop at first failure; do not repeat A.3 V5, binder V2, Godot V3, Loop22 or historical authoring accepted gates.

Next step: verify V9 ZIP SHA and sidecar, then run the V9 installer with the existing canonical `-PythonExe`. Require the same 18 destination states and all pre-write gates. After PASS, inspect `INSTALL_RECEIPT.json`, its SHA and all 18 postimages before any E1 integration review. C11-C remains sole production authority; renderer OFF; dispatch/media/audio OFF; `release_authority=NONE`.

---

## Immediate — close V6 guide mismatch with Consumer V7 (2026-11-11)

## V8 current state — 2026-11-11

V7 failed closed in `STAGED_VALIDATION` before transaction. Its installer imported `QT_VERSION_STR` from `PySide6.QtCore`; the canonical PySide6 runtime does not export that symbol. This is an installer probe defect, not evidence that PySide6, Qt, QImage or QPainter is missing. The preceding imports of `PySide6.__version__` succeeded. `journal=[]`; `rollback=NOT_NEEDED`; no checkout write occurred.

V8 changes the probe to `from PySide6.QtCore import qVersion` and records `qVersion()` as the Qt runtime version. It requires Qt 6.x, alongside Python 3.13.x, existing PySide6 6.8–6.x, non-null RGB888 QImage and active QPainter. The official Qt for Python API lists `qVersion()` as a QtCore function. V8 does not install, upgrade or uninstall packages, invoke pip, edit requirements, or mutate the shared Python environment.

The consumer, its 35 Qt tests and the E1 service replacement are byte-identical to V7. No functional test result is inferred from the failed V7 runtime probe. V8 must still pass Windows PowerShell 5.1 AST, inventory/pins/destinations/staging, runtime probe, `py_compile` 3/3, all 35 Qt tests and immediate pre-transaction checks before any write. Do not repeat accepted A.3, binder V2, Godot V3, Loop22 or historical Drill authoring.

Governance remains unchanged: C11-C frozen manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; renderer OFF; dispatch/media/audio OFF; `release_authority=NONE`; operator manages commits; Git checks skipped.

### Immediate backlog
1. Execute Consumer V8 with exact ZIP and sidecar.
2. Require `QT_VERSION_API=PASS_QVERSION_FUNCTION`, existing PySide6/Qt 6 runtime, `py_compile` 3/3 and Qt tests 35/35 before writes.
3. Audit installation receipt and all 18 postimages.
4. Continue GUI/CLI and real-frame verification; do not enter A/V qualification until authorized and prior consumer gates pass.

---


V6 failed at `STAGED_VALIDATION` only because guide V15 lacked the literal `No new Python dependency` rule expected by the installer. The guide also retained an old V14 section with Pillow 12.3.0 provisioning instructions, contrary to the accepted Qt-only architecture. Evidence confirms empty journal and `rollback=NOT_NEEDED`; no write occurred.

Next: execute Consumer V7, which updates guide V16 and the V7 incident/continuity docs while retaining the Qt code and 18-operation contract. No pip, package install, requirements edit or environment mutation. Require PowerShell 5.1 AST, all pins and destination states, Qt runtime probe, py_compile 3/3, 35/35 Qt tests and pre-transaction rechecks before writing. Then review receipt/postimages and proceed to live Producer observation.

---

## Immediate — restore no-new-dependency policy and qualify Qt consumer V6

1. Do not install V5. The prior Pillow global install was an assistant error. Remove only `Pillow==12.3.0` from the canonical Python 3.13 interpreter and verify `find_spec('PIL')` returns `None`; do not modify PySide6.
2. V6 consumer uses existing Producer PySide6. No pip, requirements file, wheel, new dependency, global environment mutation or C11-C requirements modification.
3. Review V6 package inventory/pins and run Windows PowerShell 5.1 AST, canonical Python/PySide6/Qt offscreen probe, `py_compile` 3/3 and the complete rewritten 35-test Qt suite. These are new backend tests and must not be inherited from Pillow V4 evidence.
4. Only after all staged checks and immediate pre-transaction rechecks PASS may V6 install its single E1 replacement +17 D-owned additions. Review the receipt and all 18 postimages.

## Immediate — Consumer V5 Python prerequisite then Windows install

1. Use the exact canonical executable `C:\Users\vinxe\AppData\Local\Programs\Python\Python313\python.exe` (Python 3.13.14; historical D99/E4C process receipts confirm it). Manually install the D-owned pin `Pillow==12.3.0` into this same interpreter with `-m pip install --disable-pip-version-check --only-binary=:all: Pillow==12.3.0`. The installer never installs dependencies.
2. Probe Python version, Pillow version and `PIL.features.check_feature('raqm')`; require 3.13.x, 12.3.0 and RAQM true. Stop if RAQM is false.
3. Run Consumer V5 with explicit `-PythonExe` set to that path. Require PowerShell AST, full inventory/hashes, 19 operations (1 E1 replacement +18 D-owned adds), pins, 19 destination states, complete stage roots, py_compile 3/3, tests 35/35 and immediate pre-transaction rechecks.
4. Review receipt and 19 postimages. No source/overlay writes occur before every check passes.

No C11-C requirements file is modified. The dependency lock is D-owned at `tools/c11d/d9/requirements-visual-consumer.txt`.

# C11-E Execution Backlog — V99 (2026-11-11)

## Immediate — Consumer V4 Windows qualification (E4C)

1. Verify `C11E_E4C_DRILL_VISUAL_PIXEL_CONSUMER_V4_20261110.zip.sha256`, then run its bundled installer against the active Windows checkout only. Do not extract the payload over the checkout.
2. Require PowerShell 5.1 AST, complete 24-member ZIP / 23-row content-manifest validation, 18 typed operations (one E1 service replacement +17 D-owned adds), frozen C11-C manifest size/SHA, 13 support pins, 10 design/font pins, exact operator decisions, 18 destination states and hash-guarded rollback implementation inspection.
3. Require short `%TEMP%` staging, staged guide V13, decision docket V7, phase audit V2 and incident register V4; require complete read-only test roots `challenges/`, full `assets/`, `docs/current/d/`, definitions, profiles, release, core, tools, docs/current/e, docs/history/c11e and c11c-suite/c11c-producer. Confirm `STAGING_SOURCE_ROOTS=PASS_CHALLENGES_ASSETS_DOCS_CURRENT_D`.
4. Require direct Python 3.13 + Pillow/RAQM probe, `py_compile` 3/3, consumer suite 35/35, captured stdout/stderr hashes and immediate pre-transaction pin/destination rechecks. No writes before all staged checks pass. Inspect exact receipt and all 18 postimages after PASS.

## Consumer failure chronology — retain, do not repeat

- V1: pre-transaction `PACKAGE_PREFLIGHT` failure because guide V12 was required but omitted; no transaction.
- V2: pre-transaction `STAGED_VALIDATION` failure because guide V12 lacked the literal `hash-guarded rollback` heading; empty journal and `rollback=NOT_NEEDED`.
- V3: no Windows attempt; superseded after faithful V121 stage replay found `challenges/`, full `assets/`, and `docs/current/d/` missing. This was installer staging incompleteness, not a consumer-code failure.
- V4: current candidate; incorporates guide V13, docket V7, phase audit V2 and incident register V4 checks plus complete source-stage closure. Reconstructed V121 stage locally passed py_compile 3/3 and tests 35/35. Windows acceptance is pending.

## Accepted A.3 and evidence — no reruns

A.3 V5 is installed and CLOSED/PASS: receipt SHA `d39eec2b3c1d969a3cb0d4e6aaa14b87aadcba74e42e58d283e00ea50768e881`; three replacements +26 adds; suites 33+5+7+10; py_compile 8/8. Do not repeat A.3, E4C binder V2, Godot console V3, E4B Loop22, E1 historical suite or historical Drill authoring without relevant source-pin drift.

## E4C work after Consumer V4 install

5. Review only the approved E1 service diff and connect the D-owned image consumer at the existing E1 boundary; preserve the existing Qt Producer and the shared GUI/CLI service route.
6. Observe real C11-C source frames across all 20 Drill selectors; test fonts/shaping/glyph coverage, long/empty/UNKNOWN text, overflow/clipping/contrast, phase suppression, source-frame identity and pixel determinism. Synthetic samples do not count as real-frame evidence.
7. Qualify native Drill family A/V only with separate applicable audio authority: silent protected C11-C capture; existing `FAMILY_MUSIC_V4` profiles (`tracking=FLOWING_VECTOR`, `pursuit=ORGANIC_BLOOM`, `saccade=CIRCUIT_PULSE`, `peripheral_scan=ORBITAL_RITUAL`); gameplay and music seeds independent; FFmpeg/FFprobe; human listen/visual review. Do not use D3 V5 for Drill. D.1 is only a technical envelope.
8. Close E4C only after consumer/pixel, existing Qt Producer GUI, GUI/CLI parity, native family A/V and operator human acceptance.

## Remaining product roadmap

9. E5: cross-family deterministic repeats, gameplay/music seed isolation, adapter/profile/binder non-leakage, GUI/CLI parity and negative controls.
10. E6 Smoke18: six complete A/V cases per family (18 total), receipts and operator visual/listening review.
11. E7 Matrix101: 54 Challenge +27 Loop +20 Drill target. CH_008/009 stay held until authority resolves the 11s/12s phase-sum discrepancy; 99 provisional runnable rows.
12. E8: row-by-row historical C-to-E regression map, independent acceptance, immutable freeze and separate explicit promotion/cutover. C11-C remains sole production authority until then.

## Governance and non-repeat controls

Do not repeat E1 32/32, accepted D9 preflights, E4C binder V2 20×2, Loop22, R1V, historical Drill authoring 20/20 or A.3 V5 suites absent relevant source drift. Never modify the frozen C11-C manifest, mechanics, binders, timelines, core audio, RNG or simulation truth. `GIT_CHECKS=SKIPPED; COMMITS=OPERATOR_MANAGED; SOURCE_FILE_PINS=ENFORCED`. Renderer OFF; dispatch/media false; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`.


## Immediate next action
Install V1.6 ADD_ONLY correction after V1.5 staged Python timeout. Verify package hashes, 19 source pins, PS AST, 12 staged contract tests, py_compile, immediate pin recheck and add-only receipt. Then run CLI A/V smoke with fresh request ID. GUI tracking/tier-1 remains matrix row 1/20 and must not be rerun.


## Priority 0 — E4C V2 visual consumer correction

1. Do not rerun V1.7. Install only V1.8 on the active Windows checkout; require 21/21 source pins, one exact replacement preimage, 22 add-only destination states, PS AST, existing Python 3.13/PySide6, py_compile 3/3, tests 18/18 and hash-guarded transaction PASS.
2. Audit the one replacement, all 22 added postimages and all 21 source pins post-install.
3. Run the V2 requalifier once with the preserved `E4C-CLI-SMOKE-20261112T091253Z-5a2e96b8` root. No new native capture, no Godot, no CLI re-execution, no music generation.
4. Inspect seven review frames and A/B/C video/audio; operator must accept visual composition and listening before row 1/20.
5. After acceptance, prepare the remaining 19 selector A/V matrix against the same V2 consumer. Reuse existing accepted binder and native/pixel qualification evidence where provenance allows; do not rerun the V1 pixel suite.

Keep E1 PREPARE_ONLY, no dispatch, no Git, no pip, no C11-C changes and release NONE. E5 does not start until E4C is formally closed.


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
