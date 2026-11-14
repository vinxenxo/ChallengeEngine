# C11-E INSTALLER & REQUALIFIER INCIDENT REGISTER V23 — 2026-11-13

**Latest status block; supersedes all preceding R1/earlier E4C status statements below.**


## Authoritative 2026-11-13 update — E4C V2.3 historical E1 revalidation correction R2

### Closed installation gate

- V2.2 Pin-Aligned R1 installation is **PASS**. Run: `C11E_E4C_DRILL_V2_V2_2_20261113T064019Z_4f27257a`.
- Independent post-install audit is **PASS**: package inventory 27/27; receipt and journal linked; 1 replacement + 24 additions and all 25 postimages verified; source pins 21/21; frozen C11-C manifest PASS; immutable decision record PASS.
- The receipt, transaction journal and independent audit are preserved under `artifacts/tests/c11e/e4c_v2_installer/C11E_E4C_DRILL_V2_V2_2_20261113T064019Z_4f27257a/`. Do not repeat these checks absent source-pin drift.
- The earlier failed V2.2 candidate `ecfe23...` and its pre-transaction rejection remain incident history only. R1 is installed; it is not a candidate anymore.

### Existing-media requalification failure and root cause

- The single attempt `E4C-CLI-COMPOSITION-V2-20261113T064622Z-c4d2534d` failed closed with exit 2 before FFmpeg composition. Diagnostic bundle SHA-256: `b70882a4d34e98563697fd06706e5de772174a10671f36b72030e1361f6bd674`.
- Root cause: the historical E1 intent records `output.created=false`, `overwrite_policy=DENY_EXISTING`, and `planned_root_exists=false` at preparation time. The accepted CLI smoke subsequently created that exact output root. The V2 requalifier incorrectly called the fresh-execution `c11e_production_service.validate_c11e_production_intent()` through `build_composition_plan()`, so E1 correctly rejected the now-existing root as a new dispatch overwrite.
- Do not delete, rename, replace or modify the original smoke evidence/output directory. Do not weaken E1's `DENY_EXISTING` rule and do not change `c11e_production_service.py`. The current output root is legitimate historical evidence, not a new production dispatch.
- Correct design: keep `build_composition_plan()` unchanged and strict for a normal/live E1 execution. Add a separate D-owned `build_composition_plan_for_existing_media()` entry point that validates the exact historical E1 receipt, immutable intent self-hash, D9 preparation self-hash, original `DENY_EXISTING` snapshot, exact receipt/output-root identity, and equality of all four 91-row pin inventories (intent, receipt pre, pre-renderer and post). It must not import or call the E1 new-dispatch validator. The requalifier then performs its existing fresh current-pin comparison before/after composition. This is receipt-verified historical read/requalification only.
- The exact original CLI smoke receipt remains SHA-256 `57fe829b2ae83fc16a962710b8a1ef8e4635ebf8fd4326714ed24c69c4a0f903`; intent SHA-256 `9dfe5c1c4568ed7fbc4bb4260d47da4e518b1a163811fb88f2a9f1bff55c304e`; native silent MP4 SHA `d10950bca9358de4ffe8a9f4f24c8c35cdb37e25050775a9220a4d15ffb45338` (see receipt for exact source values); A/B WAV SHA `e54b960c799102fb104a99ccd7b94c4a41b5b22d54665acda72106b36646f277`; C WAV SHA `5e81b6426f7915c7cad4c658fc24b90cd17c870a4497f45136a53e43b71efd40`. These are reused; no new capture/music generation.

### R2 corrective implementation and package

- Candidate package: `C11E_E4C_DRILL_HISTORICAL_REQUALIFIER_V2_3_R2_20261113.zip` (installer `INSTALL_C11E_E4C_DRILL_V2_3_HISTORICAL_REQUALIFIER_FIX_R2.ps1`).
- Four exact hash-guarded replacements: D V2 consumer, its Qt-offscreen test module, existing-media requalifier, and PowerShell wrapper. Thirteen versioned documentation/prompt files are ADD_ONLY. The approved decision record is not packaged or edited.
- Consumer/test code adds six focused historical-intent cases plus one regression that proves the ordinary plan builder still invokes strict E1 validation (bringing the suite expectation to 27/27); no E1 service, execution service, GUI/CLI entrypoint, C11-C source, PresentationProfile, or media is changed. Installer pins remain 21/21 and the frozen C11-C manifest remains exact.
- The wrapper now auto-creates a diagnostic ZIP on any handled requalifier failure/timeout, containing stdout/stderr, runner failure, partial output, four input evidence JSONs, and exact installed source snapshots, with inventory and SHA-256. It rethrows the original failure after attempting the bundle; a bundle failure must not mask it.
- Historical-path validation already passed directly in the build environment against the captured real 91-row E1 receipt/intent. All seven new focused test methods (six historical-intent validations plus the ordinary E1 strict-path regression) passed in isolation with import-only Qt stubs. Static `py_compile` passed 3/3. These are architect-side static/unit checks only; Windows PowerShell 5.1 AST and the complete Qt-offscreen 27/27 suite must be executed by the installer on the operator's machine.

### Current sequence and constraints

1. Install R2 once from its verified ZIP/sidecar using the new package folder; installer requires 4 REPLACE + 13 ADD_ONLY, 19 package files, 21 source pins, py_compile 3/3, Qt-offscreen tests 27/27, AST 2/2 and its own File.Replace forward/rollback probe. Path preflight from V2.2 is not repeated as a separate script; the installer performs its built-in probe.
2. Audit the R2 installer receipt, journal, all 17 postimages and 21 unchanged source pins independently. Do not run requalification until this audit is PASS.
3. Run the corrected existing-media requalifier exactly once, against the original smoke evidence root. Do not rerun GUI/CLI smoke, Godot, native capture, C11-C launcher, FAMILY_MUSIC generation or the earlier failed R1 requalifier. Any new failure must auto-create a diagnostic ZIP under its runner log root.
4. Require V2 technical contract: 630/630 GAME-body pixel identity; 180/180 PRE_ROLL + END_CTA full-frame passthrough; frame phases 90/630/90, total 810 at 30 fps; identical H.264 video streams A/B/C; A/B audio identical, C distinct; FFprobe 27 s, 720x1280, 30 fps, H.264 High/yuv420p TV and AAC-LC 48 kHz stereo; no A/V start drift; source pins unchanged.
5. Operator reviews seven extracted frames and all three final MP4s/audio. Technical PASS remains pending human visual/audio acceptance. Only then `tracking/tier-1` becomes V2 row 1/20; continue the remaining 19 selectors and close E4C at 20/20.
6. Continue E5 → E6 Smoke18 → E7 Matrix101 (54 Challenges + 27 Loops + 20 Drills; CH_008/009 remain held due 11s declared duration vs 12s phase sum; 99 provisional runnable) → E8 historical C-to-E regression, independent acceptance, immutable freeze and separately authorized promotion.

### Permanent governance and operator protocol

- C11-C 2.19.12 remains sole production authority; frozen manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- E1=`PREPARE_ONLY`; `family_adapter.status=NOT_CONNECTED_E1`; no production dispatch; `release_authority=NONE`. No E1 service edits or bypass of new-dispatch guards.
- `GIT_CHECKS=SKIPPED`; `COMMITS=OPERATOR_MANAGED`; no pip/dependency changes. Active checkout alone is source authority. ZIPs are not extracted over checkout.
- Assistant is architect, principal implementer, auditor and documentation owner. Operator executes commands and reviews A/V. No coding-agent handoff.
- Preserve all accepted receipts. Do not repeat a passing test, audit, smoke, music run or source capture unless its exact source pin has changed.


---

## Superseded document baseline (C11E_INSTALLER_INCIDENT_REGISTER_20261112_V21.md)

The following content is retained for traceability; the authoritative state and next action are defined in the update above.

# C11-E E4C V2.2 PIN-ALIGNMENT R1 — CURRENT AUTHORITATIVE STATE (2026-11-13)

**This block supersedes all earlier E4C V2 installer instructions below.** Older V1.7–V2.2 incidents remain historical evidence; do not rerun superseded packages.

## Latest installer incident: decision-record pin mismatch

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

# INSTALLER AND RUNTIME INCIDENT REGISTER OVERRIDE — V1.4 GUI A/V acceptance — 2026-11-12


## Authoritative installer correction — V1.8 package-binding failure / V1.9 consolidated recovery (2026-11-12)

The operator's V1.8 run passed the ZIP sidecar and entered the package installer, then failed closed at `OPERATION_PACKAGE_FILE_BINDING_FAIL` for `docs/current/e/C11D_E_BLOCKER_REMEDIATION_REGISTER_20261112_V54.md`. The V1.8 builder renamed physical documentation payloads to the next versioned filenames (for example V55) but failed to regenerate the matching `replacements`/`additions` destination rows; several operation destinations still referenced their predecessor names. The validator correctly rejected the mismatch before the transaction journal or destination writes. This was a package-manifest construction defect, not a Windows runtime issue. Do not rerun V1.8.

V1.9 is a complete rebuilt overlay. Its operation rows are generated directly from the physical payload tree: `payload/replace/<relative>` maps only to `REPLACE <relative>`, and `payload/add/<relative>` maps only to `ADD_ONLY <relative>`. The installer independently enforces that mapping for every operation, verifies one-to-one closure between all payload files and operation rows, rejects duplicate package paths and destination paths, and checks manifest counters against actual arrays. The V1.9 matrix is exactly one existing D-consumer replacement plus 23 add-only destinations (24 mutation operations); package inventory also includes the README and installer. All versioned current-doc and prompt destinations now match their package paths exactly.

V1.9 preserves the V2 consumer, 18 focused tests, requalifier, runner, 21 support pins and 91-pin/CLI source evidence unchanged. The only changes from V1.8 are installer/manifest construction integrity, corrected operation destinations, documentation/prompt version increments, and incident recording. The V1.8 attempt failed before transaction; no checkout destination mutation occurred. V1.9 remains `NOT_YET_INSTALLED` pending its Windows 5.1/Python 3.13/PySide6 preflight and transaction receipt.

The V1.9 installer also reports pre-transaction failures distinctly as `FAIL_CLOSED_PRE_TRANSACTION_NO_DESTINATION_WRITES` with a `%TEMP%` diagnostic, rather than labelling an empty journal as a completed rollback. No Git, pip, shared dependency, GUI/CLI, E1, C11-C, dispatch or release changes are permitted.



## Authoritative update — V1.7 installer incident and V1.8 correction (2026-11-12)

V1.7 failed closed at `DESTINATION_PREFLIGHT` because it misclassified the newly introduced `tests/test_c11e_e4c_drill_visual_composition_consumer.py` as a replacement. The destination was absent in the active checkout. The declared preimage SHA `aedeb5754d94fdbaad134a653f57ca07466c845dcef081c8774668245455a7a0` is actually the historical V9 test stored under `tools/c11d/d9/`, not a preimage at the new `tests/` path. This is a manifest/installer classification defect, not a V2 consumer failure. The failure occurred before evidence-root and transaction-journal initialization; no destination writes or repository mutations occurred. Its generic `FAIL_CLOSED_ROLLBACK_COMPLETE` message reflects a zero-entry/no-op rollback.

V1.8 supersedes V1.7 and is the only candidate permitted for installation. Its operation matrix is exactly one hash-guarded replacement (`tools/c11d/d9/c11e_e4c_drill_visual_composition_consumer.py`) plus 22 `ADD_ONLY` destinations, including the new test module. The installer asserts the exact classification, unique operation destinations, and uses manifest-resolved package paths for staged inputs. It rechecks all source pins and all destination states before journaling/writing. Do not rerun V1.7. No source, GUI/CLI, E1 service, executor, C11-C or shared dependency changes are included.

V1.8 install status: `NOT_YET_INSTALLED`. Do not claim V2 Windows qualification from package/static checks. After install PASS, reuse the already accepted CLI native MP4 and WAV A/B/C for the existing-media V2 requalification; no new C11-C capture or music generation. E4C remains open, V2 A/V acceptance pending operator review, matrix not started. C11-C remains sole production authority; E1 PREPARE_ONLY / NOT_CONNECTED_E1; dispatch false; release authority NONE.

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


**Observed:** V6 passed all package/source/decision/destination/staging preflights and stopped at staged-guide validation: `Staged PowerShell runner style guide V18 lacks required rule: No new Python dependency`.

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


## V1 visual composition defect — consumer V9 (2026-11-12)

- Evidence: `E4C-CLI-SMOKE-20261112T091253Z-5a2e96b8.zip` (17,780,165 bytes); operator screenshot `Captura de pantalla 2026-11-12 102410.png` (124,703 bytes); event/log bundle `e4c_cli_smoke.zip` (3,849 bytes).
- CLI technical receipt SHA `57fe829b2ae83fc16a962710b8a1ef8e4635ebf8fd4326714ed24c69c4a0f903`; request id `E4C-CLI-SMOKE-20261112T091253Z-5a2e96b8`.
- User review: music OK and rendering OK; visual composition REJECTED because native family header/footer are embedded inside the central video while D title/subtitle/CTA appear in additional outer regions.
- Root cause: consumer V1 full-frame `scaled(504,896,IgnoreAspectRatio,SmoothTransformation)` and draws at `(108,192)`. PRE_ROLL/END_CTA are also unnecessarily put through outer-band composition.
- Old pixel tests validated V1's 504×896 viewport; they therefore encoded the faulty behavior rather than asserting source social-body identity.
- Recovery: V2 `get_social_regions().body_rect` pixel-exact crop, full native PRE_ROLL/END_CTA passthrough, D editorial only during GAME. No C11-C changes, no new capture, no Godot, no music generation.
- Status: V1.7 candidate package, not yet installed or Windows-qualified. E4C close remains BLOCKED pending V2 install, existing-media A/V requalification and operator review.


## Authoritative update — V1.9 geometry contract test failure / V2.0 consolidated correction (2026-11-12)

The operator ran V1.9. Package SHA, 27/27 inventory, 21/21 support pins, frozen C11-C manifest and PowerShell AST 2/2 all passed. The installer then failed closed in `STAGING_AND_PYTHON_TESTS`, before transaction initialization or destination writes, because the staged consumer rejected `geometry.canvas` as a social-region mismatch; 0 tests ran. The installer created its failure diagnostic under the designated `artifacts/tests/c11e/e4c_v2_installer` evidence root; no source/destination operation was applied and the transaction journal remained empty.

Root cause is exact and localized in the V2 contract oracle. The V2 proposal's `geometry.canvas` contains five fields: `x`, `y`, `width`, `height`, and `aspect_ratio="9:16"`. Both `_verify_decision_and_proposals()` and `validate_plan()` compared it by exact dictionary equality against a four-field expectation that omitted `aspect_ratio`. The proposal is correct; the validator expectation was incomplete. It was duplicated in two independent validation sites, so both must use the same single canonical region constant.

V2.0 consolidates the correction: one `EXPECTED_SOCIAL_REGIONS` constant includes the exact 9:16 metadata and is used by proposal and plan validation; the frozen 540x960 logical `PresentationProfile.get_social_regions()` is checked against the exact 4/3 projection to 720x1280, yielding header 720x192, body 720x896 at y=192, and footer 720x192 at y=1088. Two tests are added: reject tampered aspect-ratio metadata and prove the logical-to-REVIEW_720 projection. Focused suite rises from 18 to 20 tests. No proposal, decision, timebase, C11-C, E1, GUI/CLI, execution adapter, music, binder, requalifier or runner behavior is changed.

V1.9 must not be rerun. V2.0 is a rebuilt overlay candidate; its Windows PySide6/Qt OFFSCREEN tests and transaction remain unqualified until the operator-run installer produces the complete receipt. No further installer iteration is authorized by this package record absent a new independent failure with evidence.

## V2.1 authoritative reconciliation (2026-11-12)

`E4C_OPEN_V2_REQUALIFICATION_PENDING`. Geometry V2 and the Test 04 boundary correction are accepted: `validate_plan()` now requires `source_frame_viewport == EXPECTED_SOCIAL_REGIONS["body_rect"]`. Reconciled consumer SHA-256: `e5cf97651e546ad86e2a4d46698553038e4161dc97a55da2654f197ed71f623c` (36,678 bytes); unchanged test SHA-256: `62327e32ed4c15b497efb4a93fecc1d484cebff0b79beaa7ced5099905ffb2bf`; isolated Python 3.13.14 evidence is py_compile PASS and 20/20 PASS.

V1.7 destination preflight, V1.8 operation/package binding, V1.9 geometry contract and V2.0 staging Test 04 failures are closed before transaction; none installed this correction. V2.1 is rebuilt and pending Windows installation, complete receipt and postimage review. Do not install V2.0 and do not repeat GUI, CLI smoke, native capture, music or Binder.

Preserve evidence GUI `D99-GUI-6514F1066E79`, CLI `E4C-CLI-SMOKE-20261112T091253Z-5a2e96b8`, native silent MP4, WAV A/B/C, seeds and bitstreams. V1 composition was visually rejected; `tracking/tier-1` is not yet an accepted V2 matrix row.

Required sequence: documentation; V2.1 installation; receipt/postimage audit; one existing-media requalification; seven-image/three-MP4 review; operator visual/audio acceptance; row 1/20; remaining 19; E4C close; E5, E6 Smoke18, E7 Matrix101, E8. C11-C 2.19.12 only; frozen manifest `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; E1 `PREPARE_ONLY / NOT_CONNECTED_E1`; no Git, pip, C11-C mutation, dispatch or release; operator-managed commits.


## V2.1 File.Replace MAX_PATH failure and V2.2 correction — 2026-11-12

V2.1 passed all pre-transaction validation, including 20/20 tests, then failed at transactional `File.Replace`: the generated backup path was 269 characters. The operator-provided journal confirmed the consumer preimage remained exact, no ADD_ONLY destinations were created, and rollback completed without destination changes. V2.2 changes only the backup leaf name to `000.<RunId>.preimage.bak`, preserving `relative_path` in the journal. Static path-budget calculation for the active checkout gives 213 characters for forward backup and 256 for rollback-displaced backup (Win32 limit 259 excluding NUL); max destination temp path is 195. Require the standalone exact-path File.Replace preflight and then V2.2 installation. No C11-C, E1, GUI/CLI, executor, consumer, test, media or dependency changes.


## V2.2 staged decision-record SHA mismatch — pre-transaction stop (2026-11-13)

The operator's Windows run completed the independent path-specific preflight `C11E_E4C_DRILL_V2_V2_2_20261113T061924Z_7c2e5422` with `PATH_LENGTHS=PASS`, `FILE_REPLACE_FORWARD=PASS`, `FILE_REPLACE_ROLLBACK=PASS`, and `PROBE_FILES_CLEANED=PASS`. It found the prior V2.1 temp sibling with the exact accepted consumer postimage and preserved it.

The reviewed archive `ecfe23aca3de0474c717d03b1d719195612d754f8a5cd14b039fa1179cc1b3bf` then passed archive SHA, inventory 27/27, source pins 21/21, frozen C11-C manifest, PowerShell AST 2/2 and 1+24 destination classification. It failed closed in `STAGING_AND_PYTHON_TESTS` before transaction because the documentation payload had modified the operator decision record from its approved SHA `bceef9a22c27447ccbef5487339c25626e4cb4c5d32509809b832411655914e8` to `5d77eb624b0f14079a41a83776b5f6cbf7883cc55361f407d5cf5b34ea21c242`. The consumer's hard-coded `DECISION_SHA` correctly rejected the changed bytes.

Failure run: `C11E_E4C_DRILL_V2_V2_2_20261113T061938Z_c33b887a`. `INSTALL_FAILURE.json` reports `FAIL_CLOSED_PRE_TRANSACTION_NO_DESTINATION_WRITES`; the transaction journal is empty and rollback errors are empty. No destination was written. The corrected R1 package restores the exact 2,925-byte approved record and stores runtime state only in mutable governance and continuity documents. Consumer, test and installer source bytes remain unchanged.

## R3 correction — 2026-11-14: wrapper timeout units and progress visibility

The V2.3 R2 installation and independent post-install audit are accepted. A later execution of `RUN_C11E_E4C_DRILL_AV_EXISTING_MEDIA_V2_REQUALIFICATION.ps1` reported a timeout, but inspection of its captured source proves the wrapper called `.WaitForExit(1800)`. The .NET overload interprets this argument as milliseconds; the child process was therefore terminated after 1.8 seconds, not the intended 1,800 seconds. This was a wrapper units defect, not a measured FFmpeg throughput failure.

R3 replaces only the requalification wrapper and the historical-media Python requalifier. The wrapper now declares `timeoutSeconds=1800`, converts to `timeoutMilliseconds=1800000`, polls the durable progress JSON, and terminates the child process tree only after the real 30-minute deadline. The Python requalifier atomically checkpoints stages and frame progress every 30 of 810 frames. Existing diagnostic ZIP-on-failure behavior remains enabled and now captures the progress checkpoint. No C11-C/E1 service, frozen source, producer, executor or dispatch behavior is changed.

The failed run `E4C-CLI-COMPOSITION-V2-20261113T072452Z-6fe44217` is preserved as diagnostic evidence; it wrote the V2 plan but did not start the frame compositor. Do not reuse or overwrite its output directory. R3 uses a fresh request id on each invocation.

Current gates: V2.3 R2 installation PASS; independent audit V2 PASS; R3 timeout fix installation and static target suite pending operator execution; first-selector A/V qualification remains 0/20 until a new R3 run returns a technical receipt and the operator accepts the visual/audio review. GUI/CLI smoke, source capture, music generation and the accepted 27-test V2 suite are not to be repeated.


## R3 — requalifier timeout-unit defect (2026-11-14)

The R2 wrapper used `.WaitForExit(1800)`, which .NET interprets as milliseconds (1.8 seconds), not the intended 1,800 seconds. Diagnostic request `E4C-CLI-COMPOSITION-V2-20261113T072452Z-6fe44217` proves that only the plan was written and frame composition had not started. R3 fixes the deadline conversion and adds progress checkpoints. See `docs/history/c11e/C11E_E4C_V2_3_R2_TIMEOUT_UNIT_DEFECT_AND_R3_CORRECTION_20261114_V1.md`.


## R4 addendum — 2026-11-14: FFmpeg review extraction and no-rerender recovery

R3 installation and independent audit are PASS. R3 composition reached 810/810 and all three final A/B/C MP4s were produced and mux/stream-hash operations passed; the remaining exception was solely the first review PNG extraction because FFmpeg rejected the removed `-vsync` option. R4 changes this output option to `-fps_mode passthrough` and adds a one-run recovery utility that validates the exact existing R3 outputs by bytes/SHA, FFprobe and elementary-stream hashes, then extracts only the seven PNGs. It never rerenders or remuxes. R4 install/audit/recovery remain pending until operator execution. E4C V2 accepted-selector count remains 0/20 pending visual/audio operator review.

## R4 package validation state — 2026-11-14

The R4 candidate is locally assembled and statically validated: ZIP SHA-256 `306e58edb9969d532d676cd464d694d4f48b9fa28eedc3309a33442ed4b0282c`; 21 unique ZIP entries (20 package files plus exactly one manifest), CRC PASS; manifest bindings 20/20; 21 source pins; 1 REPLACE +16 ADD_ONLY; Python compile 3/3; focused existing-output recovery tests 12/12. The Windows PowerShell 5.1 install transaction, independent audit and exact-run media recovery remain pending operator execution. R3 installation/audit are accepted; R3 output `E4C-CLI-COMPOSITION-V2-20261114T003422Z-a4d913f9` already contains all 810 composed frames and all three muxed MP4s. Recovery must only verify existing outputs and extract seven stills using `-fps_mode passthrough`; no composition, mux, music generation or capture may be repeated. E4C V2 selector acceptance remains 0/20 pending technical recovery plus operator visual/audio acceptance.

---

## Incidente R4: confusión hash canónico/bytes corregida en R5

### Estado R5 — 14 de noviembre de 2026

La instalación y auditoría independiente de R3 están cerradas: `PASS_INDEPENDENT_POST_INSTALL_AUDIT`, 17/17 postimages, 2/2 backups, 21/21 source pins y manifiesto C11-C congelado. La evidencia R4 `R4_RECOVERY_20261114T092932Z.zip` identifica un defecto de semántica SHA, no una mutación del intent: `intent_sha256=9dfe5c1c...` es el digest canónico del JSON con el campo `intent_sha256` excluido; el SHA de bytes del fichero preservado es `dfc86176...`. Ambos deben verificarse por separado y enlazarse con `receipt.e1_validation.intent_sha256`. Nunca reescribir el intent histórico para hacer coincidir ambos valores.

R5 instala la validación dual, la suite de regresión y un wrapper PowerShell integrado que captura diagnóstico automático. La documentación completa, el Authority/Roadmap/Plan/Blocker/Gates/Incident/Doc Index/Backlog y Master/Start/First prompts forman parte del propio ZIP instalador; no se distribuyen como overlays separados.

Los outputs R3 siguen siendo inmutables: request `E4C-CLI-COMPOSITION-V2-20261114T003422Z-a4d913f9`; composición 810/810, MP4 A/B/C y mux ya aceptados como medios existentes; no volver a componer, muxar, generar música, recapturar native ni lanzar CLI smoke. Solo verificar los medios existentes, extraer siete PNG y emitir recibo técnico/bundle.

R5 destino: `tools/c11d/d9/RUN_C11E_E4C_V2_3_R5_EXISTING_OUTPUT_RECOVERY.ps1`. El estado técnico seguirá pendiente de aceptación visual/auditiva humana. E1=`PREPARE_ONLY`; family adapter=`NOT_CONNECTED_E1`; production dispatch=`FALSE`; release authority=`NONE`.
