# C11D_TO_C11E_FULL_FAMILY_ROADMAP_20261115_V102 — authoritative update

## Roadmap authority update — 2026-11-15

E4C remains open at 5/20 accepted. Tracking is closed at 5/5 after technical qualification and explicit operator A/V approval for tiers 1–5. The next family is Pursuit (`pursuit/tier-1..tier-5`, profile `ORGANIC_BLOOM`), followed by Saccade (`CIRCUIT_PULSE`) and Peripheral Scan (`ORBITAL_RITUAL`). Each family requires five independent technical receipts and separate operator video/audio acceptance. Do not infer family acceptance from another family or from PREPARE_ONLY.

The Pursuit V2 installer partially committed 19 ADD_ONLY files and failed closed after the transaction due a redundant frozen-manifest second-read check; its runner also contained a stale driver hash. V2 is consumed. V3 is the exact-run recovery and pinned runner correction; it may only prepare a fresh pursuit batch, not execute it. E5 remains blocked until E4C reaches 20/20.

---

## V3 PURSUIT RECOVERY AUTHORITY — 2026-11-15

This update supersedes any V2 install-pending or next-action language below. The active project remains at E4C 5/20: tracking 5/5 operator accepted; pursuit, saccade and peripheral_scan each 0/5. C11-C 2.19.12 remains the sole production authority; frozen manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; E1 `PREPARE_ONLY`; family adapter `NOT_CONNECTED_E1`; `PRODUCTION_DISPATCH=FALSE`; `RELEASE_AUTHORITY=NONE`; `GIT_CHECKS=SKIPPED`; commits operator-managed.

Pursuit Overlay V2 failure `C11E_E4C_PURSUIT_BATCH_OVERLAY_V2_20261115T130255Z_b5f15417` is a partial ADD_ONLY transaction with all 19 operations marked `ADD_COMMITTED`, followed by `FROZEN_C11C_MANIFEST_POST_FAIL`. Preserve its failure receipt, in-progress journal, preflight, logs and stage. Never rerun V2, do not roll back or delete the 19 installed files. The installer completed its 34-pin post-check loop without recording a SOURCE_PIN_POST_FAIL, then failed on a separate second read of the frozen manifest. The failure receipt did not record the digest observed by that second read, so the supplied evidence cannot distinguish a transient second-read discrepancy from another read-path issue. Do not infer that C11-C was modified: the preflight and supplied repository snapshot both carry the frozen SHA and 796,318-byte size. V3 removes the uninstrumented second read, uses the captured frozen-manifest value from the 34-pin post-check as the authority, and persists every pre/post pin result and actual mismatch digest.

A second independent defect was found before launching the V2 runner: it pinned `c11e_e4c_pursuit_tier_batch.py` to `dcb2c035ff5aee83a673e30347617aed67c8b382bf85af68441153611964566b`, while the exact driver bytes in the same V2 package and package manifest are `7164a83c882116081cda720b37c47107e9145ad2b918b759470b06c5eb3d5522`. The V2 contract test repeated the stale value and therefore passed incorrectly. V3 pins the runner to the exact packaged driver and makes the test compute the staged driver's SHA and compare it with the runner declaration.

V3 is a recovery transaction, not a fresh installation: it audits the exact V2 run and its 19 existing destinations; verifies the original V2 package identity and 34 current source pins (the C11-C manifest is captured once); then performs exactly two pinned replacements (runner + runner test) with independently verified backups and adds the new versioned documentation. It runs the existing pursuit coordinator only in default `PREPARE_ONLY`, with separate child stdout/stderr capture and no `-Execute`. It creates no media or production dispatch.

Do not claim Pursuit installed or prepared until V3's recovery receipt, 2/2 real backups, 17/17 postimages, 34/34 pins and `PASS_PREPARE_ONLY_NO_RENDER` are independently audited. Any V3 failure after transaction start is evidence-only and must not be rerun.

--- HISTORICAL CONTENT BELOW ---

# C11-D to C11-E full-family roadmap — V101 authoritative update (2026-11-15)

## V101 authoritative update — pursuit overlay V1 failure and V2 recovery gate (2026-11-15)

E4C remains 5/20 accepted: tracking 5/5 is complete; pursuit, saccade and peripheral_scan remain 0/5 each. The next family is still Pursuit (`ORGANIC_BLOOM`, five independent selectors), but no pursuit selector has been prepared or executed.

Pursuit overlay V1 was verified, then failed during Python unittest output capture at installer line 172. Its `2>&1` native stderr redirection conflicts with Windows PowerShell 5.1 `$ErrorActionPreference='Stop'`; the single visible `... ok` line does not establish suite completion. The failure was before the transaction flag, journal creation and all 18 payload writes. Preserve V1 as failed/superseded and never rerun it.

Next gate is the V2 add-only installer. It uses waited child processes with separate stdout/stderr logs, immediate exit-code capture, durable progress/failure JSON even before transaction, and stage preservation on failure. It adds a V30 style guide that defines the PS 5.1 native-stderr rule. Require 34/34 source pins, frozen C11-C manifest, PS 5.1 AST, py_compile, 10 pursuit tests, 8 runner contract tests and atomic I/O 6/6 before any ADD_ONLY write. V2 adds 19 destinations and embeds PREPARE_ONLY only.

After V2 installation, independently audit its receipt, journal, 19 postimages, pre/post pins, C11-C freeze, and the five-selector PREPARE_ONLY request set before authorizing any pursuit execution. E4C closes only after tracking, pursuit, saccade and peripheral_scan all reach 5/5 with technical and operator visual/audio acceptance. Then E5 → E6 Smoke18 → E7 Matrix101 → E8.


## Current phase checkpoint — E4C Tracking family accepted

E4A Challenge and E4B Visual Loop remain closed. E4C Visual Drill remains open at **5/20 accepted**. The complete tracking family is now closed: `tracking/tier-1..tier-5` = 5/5 accepted. T2–T5 batch `E4C-TRACKING-T2-5-20261115T074835Z-6239dd21` passed all four technical qualifications, physical media hashes and the operator's A/V review.

### E4C remaining sequence

| Order | Family | Selector set | Expected family music profile | Status |
|---|---|---|---|---|
| 1 | tracking | tier-1..5 | FLOWING_VECTOR | ACCEPTED 5/5 |
| 2 | pursuit | tier-1..5 | ORGANIC_BLOOM | NEXT |
| 3 | saccade | tier-1..5 | CIRCUIT_PULSE | PENDING |
| 4 | peripheral_scan | tier-1..5 | ORBITAL_RITUAL | PENDING |

Do not close E4C before 20/20 technical and operator acceptance. Do not start E5 until E4C 20/20. The next deliverable is the pursuit-family batch overlay; it prepares `pursuit/tier-1..tier-5` in PREPARE_ONLY and requires separate audit before one-shot execution. It uses the existing CLI facade and shared D executor only; no additional Producer/binder/service.

After E4C: E5 cross-family determinism/seed isolation/adapter and profile non-leakage/GUI-CLI parity → E6 Smoke18 → E7 Matrix101 (CH_008/009 held due 11s declared versus 12s phase sum; 99 provisional runnable) → E8 full historical C-to-E regression, independent acceptance, immutable freeze and separately authorized promotion. E9/E10 remain undefined until authoritative governance specification.

### Current technical caveat

Four accepted tracking captures contain clean-completion Godot shutdown warnings for one CanvasItem RID and one ObjectDB instance. Record and investigate without invalidating those receipts unless subsequent evidence shows a capture/render error. The batch evidence archive omits the aggregate result and outer CLI result JSON files; retain the operator console transcript as aggregate evidence and improve packaging for later families.

## Current phase checkpoint

E4A Challenge and E4B Visual Loop remain closed. E4C Visual Drill is open. `tracking/tier-1` is operator-accepted (1/20). The tracking batch overlay V1 was installed (17/17 ADD_ONLY) and PREPARE_ONLY passed. Its sole authorized execution attempt failed closed at tier-2 before a CLI summary or product output; zero rows completed. The BatchId is consumed. The PRE_ROLL bridge V2 correction is prepared and awaits Windows installation; the four rows remain unaccepted. Do not call E4C closed until all 20 selector rows are technically qualified and operator-accepted under the current acceptance rule.

## E4C batch work package

The installed V1 batch adds only a D-owned sequential coordinator, one Windows PowerShell 5.1 launcher, tests, versioned documentation and continuity prompts. The separate V1 PRE_ROLL bridge correction installer did not transact because its optional manifest-field handling was defective; do not rerun it. The V2 correction fixes that installer and the D phase guard. It uses the existing CLI facade → E1 shared service → existing D execution adapter. It does not add or alter an E1 Producer, binder, C11-C launcher, C11-C mechanics, family music engine, composition consumer or GUI. It pins the R6.3A postimage D consumer and its test plus 25 source identities, the frozen C11-C manifest, V23/V24/V25 PowerShell guide lineage, and accepted tier-1 CLI template/request receipt; V26 is the next guide revision.

Execution order: tracking/tier-2 → tier-3 → tier-4 → tier-5, fail-fast. Each row has unique request ID and isolated output/evidence root. Each must produce native capture, D composition, family music A/B/C, muxed A and C, FFprobe A/C, source-pin parity and stream isolation. All four rows require operator visual/audio review before counting as accepted.

## Remaining roadmap

After E4C 20/20 acceptance: E5 cross-family determinism/seed isolation/adapter non-leakage/GUI-CLI parity; E6 Smoke18; E7 Matrix101; E8 historical C-to-E corpus reconciliation, independent acceptance, immutable freeze and separate promotion authority. CH_008/CH_009 remain held until the 11s/12s duration discrepancy is resolved; 99 remains provisional. No E9/E10 scope is inferred.

## Authority

C11-C 2.19.12 remains sole production baseline; frozen manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; `release_authority=NONE`.

---


# C11-D TO C11-E FULL FAMILY ROADMAP V95 — 2026-11-14

## Current authoritative checkpoint — R6.3A recovery continuation V3 (2026-11-14)

- Active checkout: `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. Source authority is the active checkout only; evidence ZIPs are read-only.
- R6.3A original install run: `C11E_E4C_V2_3_R6_3A_20261114T163406Z_fc8436fa`; original package SHA-256 `47d5a30c315365eb7a31e37fc4bc1c2ff6ca0a297d1e57eccf89c3f5a024b96e`.
- R6.3A install receipt and journal PASS: 18/18 operations, 3/3 real backups, 18/18 postimages, 25/25 source pins; 32/32 consumer tests PASS. Do not rerun installation or tests.
- Independent post-install audit PASS against the first run: 18/18 journal operations, 18/18 postimages, 3/3 backups, 25/25 pins, frozen C11-C and immutable decision record PASS. Do not rerun it.
- Recovery documentation transaction PASS: 14/14 ADD_ONLY, 14 added, zero skipped. These files are already installed; verify their receipt rather than adding the same files again.
- Recovery invocation root: `artifacts/tests/c11e/r6_3a_audit_recovery/20261114T192552Z_7650ad32`. Existing lock: `R6_3A_REQUALIFICATION_ATTEMPT_LOCK.json`, exact schema `C11E-R6_3A-REQUALIFICATION-ONE-SHOT-LOCK-V1`, status `ATTEMPT_RESERVED`. Preserve it.
- Root cause of last failure: the recovery script called `Tee-Object` with both `-FilePath` and `-Variable`, which are mutually exclusive parameter sets in Windows PowerShell 5.1. Failure occurred at parent pipeline parameter binding after `R6_3A_REQUALIFICATION_START=TRUE`, before the runner could emit `R6_3A_OUTPUT_ID`. This is not an FFmpeg/media failure. No new composition/mux was started according to the supplied log; continuation script must independently recheck empty/absent console, no output ID, and no matching output/diagnostic directory before resuming.
- Unissued resume V1 is superseded and must not be run: it used `$audit` instead of `$auditPath`, and an incorrect runner filename missing `_R6_`. Resume V3 is the only approved continuation; V1 and V2 drafts are unissued and superseded.
- Resume V3 does not install code, rerun audit/tests or regenerate native capture/music. It verifies exact accepted receipts and the existing lock, adds the new documentation version set ADD_ONLY, writes a separate `CreateNew` one-shot continuation marker, then invokes the exact installed runner once using `Start-Process -Wait -PassThru` with separate stdout/stderr redirection. The process exit code is captured immediately and logs are read only after process exit. Any failure after the marker prohibits retry.
- If technical requalification succeeds, it produces one fresh D-owned 810-frame output, three A/B/C muxed MP4s, technical receipt and seven-frame review bundle. Original silent native MP4 and existing FAMILY_MUSIC_V4 WAVs are reused. No new capture, music generation, Godot or GUI/CLI smoke.
- Human review is still required for seven frames and A/B/C listening. `tracking/tier-1` remains 0/20 until explicit operator visual/audio acceptance. E4C closes only at 20/20.
- Roadmap: E4C → E5 → E6 Smoke18 → E7 Matrix101 (CH_008/009 held; 99 provisional) → E8 historical C-to-E regression, independent acceptance, immutable freeze and separately authorized promotion. E9/E10 have not yet been formally defined in the supplied roadmap; define their scope and gates after E8 rather than inventing them in the recovery patch.
- Governance: C11-C 2.19.12 remains sole production authority; frozen manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; E1 PREPARE_ONLY; family adapter NOT_CONNECTED_E1; production dispatch false; release authority NONE; no Git checks; commits operator-managed; no pip/shared dependency changes.

---

# C11-D TO C11-E FULL FAMILY ROADMAP V86 — 2026-11-13

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

## Superseded document baseline (C11D_TO_C11E_FULL_FAMILY_ROADMAP_20261112_V84.md)

The following content is retained for traceability; the authoritative state and next action are defined in the update above.

# C11-E E4C V2.2 PIN-ALIGNMENT R1 — CURRENT AUTHORITATIVE STATE (2026-11-13)

**This block supersedes all earlier E4C V2 installer instructions below.** Older V1.7–V2.2 incidents remain historical evidence; do not rerun superseded packages.

## Current roadmap position

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

# ROADMAP OVERRIDE — first GUI Drill A/V pilot accepted — 2026-11-12


## Authoritative installer correction — V1.8 package-binding failure / V1.9 consolidated recovery (2026-11-12)

The operator's V1.8 run passed the ZIP sidecar and entered the package installer, then failed closed at `OPERATION_PACKAGE_FILE_BINDING_FAIL` for `docs/current/e/C11D_E_BLOCKER_REMEDIATION_REGISTER_20261112_V54.md`. The V1.8 builder renamed physical documentation payloads to the next versioned filenames (for example V55) but failed to regenerate the matching `replacements`/`additions` destination rows; several operation destinations still referenced their predecessor names. The validator correctly rejected the mismatch before the transaction journal or destination writes. This was a package-manifest construction defect, not a Windows runtime issue. Do not rerun V1.8.

V1.9 is a complete rebuilt overlay. Its operation rows are generated directly from the physical payload tree: `payload/replace/<relative>` maps only to `REPLACE <relative>`, and `payload/add/<relative>` maps only to `ADD_ONLY <relative>`. The installer independently enforces that mapping for every operation, verifies one-to-one closure between all payload files and operation rows, rejects duplicate package paths and destination paths, and checks manifest counters against actual arrays. The V1.9 matrix is exactly one existing D-consumer replacement plus 23 add-only destinations (24 mutation operations); package inventory also includes the README and installer. All versioned current-doc and prompt destinations now match their package paths exactly.

V1.9 preserves the V2 consumer, 18 focused tests, requalifier, runner, 21 support pins and 91-pin/CLI source evidence unchanged. The only changes from V1.8 are installer/manifest construction integrity, corrected operation destinations, documentation/prompt version increments, and incident recording. The V1.8 attempt failed before transaction; no checkout destination mutation occurred. V1.9 remains `NOT_YET_INSTALLED` pending its Windows 5.1/Python 3.13/PySide6 preflight and transaction receipt.

The V1.9 installer also reports pre-transaction failures distinctly as `FAIL_CLOSED_PRE_TRANSACTION_NO_DESTINATION_WRITES` with a `%TEMP%` diagnostic, rather than labelling an empty journal as a completed rollback. No Git, pip, shared dependency, GUI/CLI, E1, C11-C, dispatch or release changes are permitted.



## Authoritative update — V1.7 installer incident and V1.8 correction (2026-11-12)

V1.7 failed closed at `DESTINATION_PREFLIGHT` because it misclassified the newly introduced `tests/test_c11e_e4c_drill_visual_composition_consumer.py` as a replacement. The destination was absent in the active checkout. The declared preimage SHA `aedeb5754d94fdbaad134a653f57ca07466c845dcef081c8774668245455a7a0` is actually the historical V9 test stored under `tools/c11d/d9/`, not a preimage at the new `tests/` path. This is a manifest/installer classification defect, not a V2 consumer failure. The failure occurred before evidence-root and transaction-journal initialization; no destination writes or repository mutations occurred. Its generic `FAIL_CLOSED_ROLLBACK_COMPLETE` message reflects a zero-entry/no-op rollback.

V1.8 supersedes V1.7 and is the only candidate permitted for installation. Its operation matrix is exactly one hash-guarded replacement (`tools/c11d/d9/c11e_e4c_drill_visual_composition_consumer.py`) plus 22 `ADD_ONLY` destinations, including the new test module. The installer asserts the exact classification, unique operation destinations, and uses manifest-resolved package paths for staged inputs. It rechecks all source pins and all destination states before journaling/writing. Do not rerun V1.7. No source, GUI/CLI, E1 service, executor, C11-C or shared dependency changes are included.

V1.8 install status: `NOT_YET_INSTALLED`. Do not claim V2 Windows qualification from package/static checks. After install PASS, reuse the already accepted CLI native MP4 and WAV A/B/C for the existing-media V2 requalification; no new C11-C capture or music generation. E4C remains open, V2 A/V acceptance pending operator review, matrix not started. C11-C remains sole production authority; E1 PREPARE_ONLY / NOT_CONNECTED_E1; dispatch false; release authority NONE.

E4C has crossed the first true integrated execution milestone: existing Producer GUI → E1 canonical intent/parity → one D-owned executor → unchanged silent C11-C Drill source capture → Qt D composition → FAMILY_MUSIC_V4 A/B/C → FFmpeg/FFprobe A/C mux and bitstream isolation. Operator visual and audio review is PASS. The locale boundary failure is resolved; V1.4 did not require another adapter correction.

Next: CLI-origin A/V smoke through the existing CLI facade; then the remaining 19 selectors of the 20-selector A/V matrix (the accepted GUI `tracking/tier-1` is row 1). E4C closes only after CLI smoke and 20/20 selector evidence.


**Current E4C position (2026-11-12):** the first single-selector GUI A/V qualification is accepted for `visual_drills / tracking / tier-1`. The operator confirmed visual and listening review PASS. Evidence `D99-GUI-6514F1066E79-production.zip` SHA-256 `5fb910dd7515ca1f80f2fa77a0829836613e933ca7106f00852ccd31d797f8e4`; tests/plan bundle `D99-GUI-6514F1066E79-tests.zip` SHA-256 `5c94ad64666548db478a4265a71345efe28c2a346f215e7cdb477f51dc8dde91`; qualification receipt SHA-256 `d8aad7176ed99d8bc0c067cece58272c5ac44045d55d746c768ea72324d459db`; RUNNING receipt SHA-256 `2f9b388b3541548d79c254161290ad73241109349aea1f57c1ac9c10e092ab2a`. The receipt status is `PASS_E4C_DRILL_SINGLE_SELECTOR_A_V_QUALIFICATION`.

**Independent audit:** 91/91 E1 source pins are identical at pre-execution, immediately-pre-render and post-execution; GUI/CLI E1 semantic identity parity PASS; 810/810 frames composed at 30 fps; phases PRE_ROLL/GAME/END_CTA = 90/630/90 frames; GAME editorial fields are populated and D-composed. `FAMILY_MUSIC_V4` `FLOWING_VECTOR` produces 27s, 44.1 kHz stereo PCM16; A/B seed 840001 WAV SHA `e54b960c799102fb104a99ccd7b94c4a41b5b22d54665acda72106b36646f277` is identical, C seed 840002 WAV SHA `5e81b6426f7915c7cad4c658fc24b90cd17c870a4497f45136a53e43b71efd40` differs. Final A and C are 27s, H.264 High 720×1280 yuv420p TV, 30 fps, 810 frames; AAC-LC 48 kHz stereo; both start at 0. Receipt stream hashes prove video A/C identical and audio A/C different; independent extraction also confirms raw H.264 SHA `500fc010b0d39062997d73643643943d03552082d75a2b8db6c55a3bbe5ad150` matches, while AAC elementary stream SHA differs (`23162fb059ca5e215758d6bbd58b6baba0efc9bd13e94d5921fd96726e19cd67` vs `f98747cc8f408521a3d00e7f4d90a066f3adf366de46d6f89bfefb65e26e86cd`). Final A SHA `7604f69e7c28e044a4bdb7fccc76c74604495ec9bbe4b46fcbca23a62b7c49ba`; final C SHA `d93753dabcfd85f3a3e721125081a649fbfa3a033a751e77a39df4c38357bf84`. Native source SHA `d10950bca9358de4ffe8a9f4f24c8c35cdb37e25050775a9220a4d15ffb45338`; silent D-composed intermediate SHA `60fd3155e70691bb7f2e636d20539e5898554669503888ee34bb78402c9589ad`.

Governance: C11-C frozen manifest remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; `c11c_source_mutation=false`; D3 V5 not invoked; source C11-C audio remains disabled via `-NoSound`; renderer invocation is solely the explicitly authorized isolated E4C qualification scope; `production_dispatch=false`; `release_authority=NONE`. E1 stays `PREPARE_ONLY`, `family_adapter.status=NOT_CONNECTED_E1`. Do not turn these isolated test results into production dispatch or release authority.

**Next gates:** (1) CLI-origin A/V smoke through the existing CLI facade with `--execute-drill-av --origin CLI`, using the same shared D executor and a fresh request ID; (2) 20-selector family A/V matrix; count the accepted GUI `tracking/tier-1` pilot as matrix row 1 and do not rerun it for matrix coverage; (3) E4C closeout only after CLI smoke, all remaining 19 selectors, receipts, human review and source-pin integrity. Then E5 → E6 Smoke18 → E7 Matrix101 (CH_008/009 held; 99 provisional) → E8 historical C-to-E regression, independent acceptance, freeze and separately authorized promotion.

---

## Superseded prior revision content

E4C's visual/Binder/native-source qualifications remain accepted. The first shared A/V pilot has now exercised the GUI path: E1 preparation, GUI/CLI semantic parity and D composition planning pass; native capture is blocked by the D adapter's locale-sensitive `0.75` → `0,75000` → PowerShell `75000` argument conversion. V1.4 adds an invariant-culture PowerShell bridge and an `es-ES` pre-transaction probe.

The next work remains: (1) install V1.4 and verify all postimages; (2) fresh-ID `tracking/tier-1` A/V pilot; (3) inspect media/receipt and operator visual+audio acceptance; (4) CLI smoke against the same adapter; (5) 20-selector family A/V matrix; (6) close E4C only after the accepted matrix; then E5, E6 Smoke18, E7 Matrix101 and E8 independent regression/freeze/promotion. No roadmap promotion is inferred from a planning receipt.



## D99-GUI-85201B7B4FF7 — single-selector A/V pilot diagnosis — 2026-11-12

**Authoritative evidence:** `D99-GUI-85201B7B4FF7.zip` SHA-256 `0913179f9852b7b1f75c2a7e2f763a111bc8d807d08d20036a2891ae94661f56`; `D99-GUI-85201B7B4FF7-tests.zip` SHA-256 `16f0e199429deffb85025cd35d0cfd4fe2ec9fe237cf66482f6de6b14cd6ef23`.

The GUI's **Resolver + Plan** stage is successful, not a failure: E1 receipt is `PASS_E1_PREPARATION_ONLY`; GUI/CLI semantic parity is `PASS`; D9.10 bridge planning is `PASS_BRIDGE_PLANNING_ONLY`; D composition plan is valid with real GAME-visible editorial; the request is `visual_drills / tracking / tier-1`, gameplay seed `12345`, music seed `840001`, `REVIEW_720`. This remains deliberately plan-only at E1 and does not claim renderer or dispatch activation. The second GUI action, the shared D A/V executor, fails before the native C11-C producer starts.

Exact failure from `logs/c11c_drill_producer.log`: C11-C's `run_visual_drill_production.ps1` rejects `-SpeedMultiplier` because it receives `75000`, outside `[ValidateRange(0.1,3.0)]`. The pinned profile `profiles/difficulty/visual_drill_tracking.json` has tier 1 `speed_multiplier=0.75` (source SHA-256 `6de8812bd46904e122ecdd0eae22fb2979bd75399c34779248c6569e833c921e`). The adapter applied Python's host decimal separator and sent `0,75000`. On the operator's locale, Windows PowerShell 5.1 parameter binding split/coerced that comma decimal and delivered `75000`. This is a cross-locale numeric argument-boundary defect in the D adapter, not a defect in the pinned C11-C launcher or difficulty profile.

The failure occurs before a successful C11-C capture. There is no native MP4, no D frame composition, no FAMILY_MUSIC_V4 WAV generation, no mux, and no final FFprobe result in this run. The failure does not indicate an editorial, font, Qt, geometry, phase/timebase, music determinism, or A/V stream-equivalence defect. The first evidence bundle contains `RUNNING` and `FAILURE` receipts and the exact native producer log. The `-tests.zip` is a preparation/parity/contract receipt bundle; it does not show a second independent A/V failure. Do not infer additional failures from its intentionally plan-only receipts.

**V1.4 correction:** remove host-locale formatting entirely. Python emits an ASCII invariant string such as `0.75000` to a string-typed PowerShell wrapper. The wrapper parses it with `[System.Globalization.CultureInfo]::InvariantCulture`, sets the wrapper thread culture to invariant for the call, then invokes the existing pinned C11-C launcher with an already-typed `[double]$speed`. The native C11-C launcher remains byte-identical and receives `0.75`; C11-C stays silent via `-NoSound`. The wrapper is retained in the run logs and its hash/argument are written into the execution receipt. Regression tests cover invariant formatting, wrapper parse/type handoff, and absence of host-locale formatting. The V1.4 installer additionally executes this exact wrapper against a dummy parameter-compatible launcher while forcing `es-ES`, and requires the dummy to record `0.75` before any repository mutation.

The failed output root `artifacts/production/c11e/D99-GUI-85201B7B4FF7` is intentionally preserved. It must not be overwritten. The retry must use a **new unique request_id/output root** (generate a fresh GUI request and repeat Resolver + Plan); do not delete or recycle this failed evidence. After V1.4 installation PASS: audit its postimages/source pins, rerun the GUI plan stage with a fresh ID, then execute only `tracking/tier-1`. Continue only when native capture, D composition, FAMILY_MUSIC_V4 A/B/C, final A/C video/audio stream hashes, FFprobe, and human visual/listening review pass. CLI smoke/parity follows on the same shared adapter. Do not start the 20-selector A/V matrix until the single-selector result is accepted.

Governance is unchanged: E1 `PREPARE_ONLY`; `family_adapter.status=NOT_CONNECTED_E1`; `production_dispatch=false`; `release_authority=NONE`; no Git checks; commits operator-managed; C11-C frozen manifest SHA remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.


---

# ROADMAP OVERRIDE — E4C EXECUTION ADAPTER — 2026-11-11

E4C current state: Binder V2, 20 native silent source captures and real-frame pixel qualification 100/100 are accepted. The next implementation is one D-owned execution adapter behind the existing GUI and existing E1 CLI. First qualify one `tracking/tier-1` A/V request; expand to all 20 only after that route is accepted. E1 remains PREPARE_ONLY; C11-C remains production authority.

After full E4C closure: E5 cross-family determinism, separate gameplay/music domains, profile/binder non-leakage and GUI/CLI parity; E6 Smoke18 (six full A/V cases per family); E7 Matrix101 (54 Challenge +27 Loop +20 Drill, with CH_008/009 held pending phase-sum authority, 99 provisional runnable); E8 row-by-row historical C-to-E regression, independent acceptance, freeze and separately authorized promotion/cutover.

No stage in this roadmap itself changes renderer/dispatch/release authority.

---

## V9 current state — 2026-11-11

Consumer V8 stopped in `STAGED_VALIDATION` before any repository transaction. The exact cause was a StrictMode ordering bug in the installer: `$testSource` was inspected for the removed `QT_VERSION_STR` token before it was assigned from the staged test file. The run's journal is empty and `rollback=NOT_NEEDED`; no rollback or repository recovery is required. V9 fixes this by loading both `$consumerSource` and `$testSource` first, validating both are non-empty, and only then inspecting their contents. This is an installer-only correction. The Qt consumer, 35-test module and E1 service replacement bytes are unchanged from V8.

V9 also corrects the run ID and receipt/failure schema identities to V9. It preserves the 18-operation scope (one exact-pinned E1 service REPLACE + 17 D-owned ADDs), all 13 support pins, 10 design/font pins, exact-hash operator decisions, frozen C11-C manifest and no-new-dependency policy. The installer uses the existing canonical Producer Python/PySide6 only; it must not invoke pip, install/uninstall packages, change requirements or mutate shared environment dependencies.

V9 is a candidate only. Windows PowerShell 5.1 AST, Qt runtime probe, py_compile 3/3, tests 35/35, immediate pre-transaction rechecks and successful receipt are still pending. No consumer V1–V8 transaction has been recorded. Stop at first failure; do not repeat A.3 V5, binder V2, Godot V3, Loop22 or historical authoring accepted gates.

Next step: verify V9 ZIP SHA and sidecar, then run the V9 installer with the existing canonical `-PythonExe`. Require the same 18 destination states and all pre-write gates. After PASS, inspect `INSTALL_RECEIPT.json`, its SHA and all 18 postimages before any E1 integration review. C11-C remains sole production authority; renderer OFF; dispatch/media/audio OFF; `release_authority=NONE`.

---

## E4C current subgate status — Consumer V7 guide correction (2026-11-11)

## V8 current state — 2026-11-11

V7 failed closed in `STAGED_VALIDATION` before transaction. Its installer imported `QT_VERSION_STR` from `PySide6.QtCore`; the canonical PySide6 runtime does not export that symbol. This is an installer probe defect, not evidence that PySide6, Qt, QImage or QPainter is missing. The preceding imports of `PySide6.__version__` succeeded. `journal=[]`; `rollback=NOT_NEEDED`; no checkout write occurred.

V8 changes the probe to `from PySide6.QtCore import qVersion` and records `qVersion()` as the Qt runtime version. It requires Qt 6.x, alongside Python 3.13.x, existing PySide6 6.8–6.x, non-null RGB888 QImage and active QPainter. The official Qt for Python API lists `qVersion()` as a QtCore function. V8 does not install, upgrade or uninstall packages, invoke pip, edit requirements, or mutate the shared Python environment.

The consumer, its 35 Qt tests and the E1 service replacement are byte-identical to V7. No functional test result is inferred from the failed V7 runtime probe. V8 must still pass Windows PowerShell 5.1 AST, inventory/pins/destinations/staging, runtime probe, `py_compile` 3/3, all 35 Qt tests and immediate pre-transaction checks before any write. Do not repeat accepted A.3, binder V2, Godot V3, Loop22 or historical Drill authoring.

Governance remains unchanged: C11-C frozen manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; renderer OFF; dispatch/media/audio OFF; `release_authority=NONE`; operator manages commits; Git checks skipped.

### Roadmap position
E4C remains open at the Drill visual consumer qualification gate. After V8 installs and passes real Qt tests, continue to Producer GUI/CLI observation, real C11-C Drill frames, family-native `FAMILY_MUSIC_V4` A/V qualification, FFmpeg/FFprobe and human review. Then E5 → E6 Smoke18 → E7 Matrix101 (99 provisional; CH_008/009 held) → E8 independent historical regression and separate promotion.

---


The E4C Drill consumer remains in its isolated visual-consumer install gate. V6 failed closed before transaction solely because the staged runner guide V15 omitted the exact `No new Python dependency` anchor, while retaining a historical Pillow section that conflicted with its current Qt-only policy. V7 supplies guide V16 and reconciles the current policy. No dependency installation or environment mutation is part of the roadmap. After V7 passes Windows staged validation and installs, verify live Qt Producer output, all 20 selectors, fonts/pixels and GUI/CLI parity; only then continue native Drill A/V, E4C closure and E5 → E6 Smoke18 → E7 Matrix101 → E8. Renderer, dispatch/media and release remain blocked.

---

## E4C current subgate status — 2026-11-11 (supersedes V5 Pillow path)

The Drill visual consumer is not installed. V1/V2/V4 all failed closed before transaction; V4 reached runtime preflight and found no `PIL` module. The V5 proposal to install Pillow in the shared Producer interpreter was an error and is superseded. V6 changes the D-owned consumer renderer to the existing PySide6/Qt already required by Producer; no new Python dependency, package installation, global environment mutation or C11-C requirements edit. The Qt implementation's full 35-test Windows qualification is mandatory before installation. After E4C consumer/Qt/pixel/A/V human gates close, continue E5 → E6 Smoke18 → E7 Matrix101 (99 provisional; CH_008/009 held) → E8 independent historical regression/freeze/separate promotion.

## E4C current subgate status — 2026-11-11

The Drill visual consumer is not installed. V4's installer reached Python runtime validation and failed solely because the canonical Python 3.13.14 interpreter has no Pillow module. V5 records `Pillow==12.3.0` as a D-owned dependency and requires operator-managed installation/RAQM verification before its Windows install. After E4C consumer/Qt/pixel/A/V human gates close, continue E5 → E6 Smoke18 → E7 Matrix101 (99 provisional; CH_008/009 held) → E8 independent historical regression/freeze/separate promotion.

# C11-D → C11-E Full-Family Roadmap — V71 (2026-11-11)

## Target product

One C11-E service produces validated audiovisual outputs for Challenge, Visual Loop and Visual Drill, using D presentation/layout/editorial, family-correct music, FFmpeg mux/FFprobe QA, immutable receipts and the existing Producer GUI/CLI adapters over the same E1 service. C11-C mechanics, generators, timelines, binders and core audio remain immutable until E8 and a separate cutover decision.

## Accepted family evidence — do not repeat absent source drift

- E4A accepted in its recorded scope.
- E4B Loop22 CLOSED/operator-approved: 44/44 A/V, 22/22 A/B, 25/25 tests and human visual/audio approval.
- Historical Drill authoring 20/20 on 24 source pins.
- E4C binder V2 active Windows PASS: 20/20 selectors/repeats/request manifests/lineage and 67/67 pins; receipt `31f631c3c23c6c1d277d67f52dd887010ee51be869798ab8db3fbdec8658fa01`.
- E4C Godot console V3 smoke PASS; receipt `526c7d360863af8fb53707c9c83162173f4c1f1eb349ee8d767fb97665167a31`.
- A.3 Drill design-contract V5 CLOSED/PASS active Windows; receipt `d39eec2b3c1d969a3cb0d4e6aaa14b87aadcba74e42e58d283e00ea50768e881`; do not repeat.

## Ordered work remaining

1. Install and qualify Consumer V4 in active Windows. V1 and V2 failed closed pre-transaction; V3 was superseded before Windows use after the faithful V121 staging replay exposed missing read-only roots. V4 includes the complete test dependency roots and local reconstructed replay passed py_compile 3/3 + tests 35/35; Windows AST/runtime/receipt remain open.
2. Review receipt, E1 service diff/postimage and all 17 D-owned additions. Inspect the single shared E1 boundary; preserve existing GUI/CLI route and parity. No second Producer, binder or suite module.
3. Observe actual Qt Producer runtime with protected C11-C source frames over all 20 Drill selectors; review phase visibility, native PRE_ROLL/END_CTA ownership, fonts/shaping/glyph coverage, clipping/overflow/contrast and source/pixel identity.
4. Qualify native Drill A/V only under separate applicable authority: silent protected C11-C capture, existing `FAMILY_MUSIC_V4` (`tracking=FLOWING_VECTOR`, `pursuit=ORGANIC_BLOOM`, `saccade=CIRCUIT_PULSE`, `peripheral_scan=ORBITAL_RITUAL`), separate gameplay/music seeds, FFmpeg/FFprobe and human listening/visual review. D.1 is not audio-generation authority.
5. Close E4C only after the consumer/pixel gate, actual GUI/CLI and Qt evidence, native family A/V and operator human review all pass.
6. E5: cross-family determinism, gameplay/music seed isolation, profile/binder non-leakage, negative controls and GUI/CLI parity.
7. E6 Smoke18: six complete A/V cases per family, 18 total, with immutable receipts and operator visual/listening review.
8. E7 Matrix101: 54 Challenge +27 Loop +20 Drill target. CH_008/CH_009 stay held until authority resolves the 11s declared vs 12s phase-sum discrepancy; 99 provisional runnable cases.
9. E8: row-by-row historical C11-C to E regression map, independent acceptance, immutable freeze and separate explicit promotion/cutover.

## Exact Drill approvals and scope

Operator decision record `C11E_E4C_DRILL_COMPOSITION_OPERATOR_DECISION_RECORD_20261110_V1.json` SHA `eb95da188065b8ebcb2371e2a6bcff6762ce000a5ca74f8ea384ecec4ee58303` approves geometry SHA `b22f9eb6fce39f877e432ff5f0051ecf5ab8575ecb9f580fe5f158994222fc09` and timebase SHA `44ab3b0fa09a6f7d42cd8cf2f1122cada6cbffe16a7a6b53c2af5e88d5daddc8` as proposed, limited to D-owned design/contract and isolated pixel tests. Native phases remain PRE_ROLL 3s → GAME → END_CTA 3s → DONE; D editorial is GAME-only; native source-frame/header/footer and END_CTA CTA are preserved.

## Immutable governance

Frozen C11-C 2.19.12 manifest remains 796,318 bytes / `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. No protected mechanics, generators, binders, timelines, RNG, simulation truth or core audio changes. No sixth module/second Producer/parallel binder. `GIT_CHECKS=SKIPPED; COMMITS=OPERATOR_MANAGED; SOURCE_FILE_PINS=ENFORCED`. Renderer OFF, dispatch/media false, D4.8 BLOCKED, D9.10 PREPARE_ONLY, D9.14/16 BLOCKED, D9.17 BLOCKED_NO_GO, D10 BLOCKED_FOR_PROMOTION, `release_authority=NONE`.


## Current 2026-11-12 E4C status
GUI A/V `tracking/tier-1` is accepted as row 1/20. V1.5 CLI smoke installer failed closed before transaction; V1.6 add-only correction is next. After installation PASS, qualify the CLI A/V entrypoint with a fresh request ID, then run the remaining 19 selectors. Do not repeat accepted GUI pilot, 20 native silent captures or 100/100 pixel gate. E4C closes only after CLI smoke + 20/20 matrix + required human review.


## 2026-11-12 sequencing correction

E4C is still the current active phase. CLI A/V smoke has now technically passed, but the user's visual review rejected the V1 spatial composition. Close this defect using the D-owned V2 social-body consumer and existing-media requalification; do not start the remaining A/V matrix until V2 tracking/tier-1 output is operator-accepted. Then complete remaining 19 selectors and formal E4C closeout.

After E4C: E5 determinism/gameplay-vs-music seed isolation/profile-binder non-leakage/GUI-CLI parity → E6 Smoke18 → E7 Matrix101 (CH_008/009 held; 99 provisional) → E8 historical C-to-E regression, independent acceptance, immutable freeze and separately authorized promotion. C11-C remains sole production authority throughout.


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

## R3 correction — 2026-11-14: wrapper timeout units and progress visibility

The V2.3 R2 installation and independent post-install audit are accepted. A later execution of `RUN_C11E_E4C_DRILL_AV_EXISTING_MEDIA_V2_REQUALIFICATION.ps1` reported a timeout, but inspection of its captured source proves the wrapper called `.WaitForExit(1800)`. The .NET overload interprets this argument as milliseconds; the child process was therefore terminated after 1.8 seconds, not the intended 1,800 seconds. This was a wrapper units defect, not a measured FFmpeg throughput failure.

R3 replaces only the requalification wrapper and the historical-media Python requalifier. The wrapper now declares `timeoutSeconds=1800`, converts to `timeoutMilliseconds=1800000`, polls the durable progress JSON, and terminates the child process tree only after the real 30-minute deadline. The Python requalifier atomically checkpoints stages and frame progress every 30 of 810 frames. Existing diagnostic ZIP-on-failure behavior remains enabled and now captures the progress checkpoint. No C11-C/E1 service, frozen source, producer, executor or dispatch behavior is changed.

The failed run `E4C-CLI-COMPOSITION-V2-20261113T072452Z-6fe44217` is preserved as diagnostic evidence; it wrote the V2 plan but did not start the frame compositor. Do not reuse or overwrite its output directory. R3 uses a fresh request id on each invocation.

Current gates: V2.3 R2 installation PASS; independent audit V2 PASS; R3 timeout fix installation and static target suite pending operator execution; first-selector A/V qualification remains 0/20 until a new R3 run returns a technical receipt and the operator accepts the visual/audio review. GUI/CLI smoke, source capture, music generation and the accepted 27-test V2 suite are not to be repeated.


## R4 addendum — 2026-11-14: FFmpeg review extraction and no-rerender recovery

R3 installation and independent audit are PASS. R3 composition reached 810/810 and all three final A/B/C MP4s were produced and mux/stream-hash operations passed; the remaining exception was solely the first review PNG extraction because FFmpeg rejected the removed `-vsync` option. R4 changes this output option to `-fps_mode passthrough` and adds a one-run recovery utility that validates the exact existing R3 outputs by bytes/SHA, FFprobe and elementary-stream hashes, then extracts only the seven PNGs. It never rerenders or remuxes. R4 install/audit/recovery remain pending until operator execution. E4C V2 accepted-selector count remains 0/20 pending visual/audio operator review.

## R4 package validation state — 2026-11-14

The R4 candidate is locally assembled and statically validated: ZIP SHA-256 `306e58edb9969d532d676cd464d694d4f48b9fa28eedc3309a33442ed4b0282c`; 21 unique ZIP entries (20 package files plus exactly one manifest), CRC PASS; manifest bindings 20/20; 21 source pins; 1 REPLACE +16 ADD_ONLY; Python compile 3/3; focused existing-output recovery tests 12/12. The Windows PowerShell 5.1 install transaction, independent audit and exact-run media recovery remain pending operator execution. R3 installation/audit are accepted; R3 output `E4C-CLI-COMPOSITION-V2-20261114T003422Z-a4d913f9` already contains all 810 composed frames and all three muxed MP4s. Recovery must only verify existing outputs and extract seven stills using `-fps_mode passthrough`; no composition, mux, music generation or capture may be repeated. E4C V2 selector acceptance remains 0/20 pending technical recovery plus operator visual/audio acceptance.

---

## R5: continuidad E4C sin repetir producción

### Estado R5 — 14 de noviembre de 2026

La instalación y auditoría independiente de R3 están cerradas: `PASS_INDEPENDENT_POST_INSTALL_AUDIT`, 17/17 postimages, 2/2 backups, 21/21 source pins y manifiesto C11-C congelado. La evidencia R4 `R4_RECOVERY_20261114T092932Z.zip` identifica un defecto de semántica SHA, no una mutación del intent: `intent_sha256=9dfe5c1c...` es el digest canónico del JSON con el campo `intent_sha256` excluido; el SHA de bytes del fichero preservado es `dfc86176...`. Ambos deben verificarse por separado y enlazarse con `receipt.e1_validation.intent_sha256`. Nunca reescribir el intent histórico para hacer coincidir ambos valores.

R5 instala la validación dual, la suite de regresión y un wrapper PowerShell integrado que captura diagnóstico automático. La documentación completa, el Authority/Roadmap/Plan/Blocker/Gates/Incident/Doc Index/Backlog y Master/Start/First prompts forman parte del propio ZIP instalador; no se distribuyen como overlays separados.

Los outputs R3 siguen siendo inmutables: request `E4C-CLI-COMPOSITION-V2-20261114T003422Z-a4d913f9`; composición 810/810, MP4 A/B/C y mux ya aceptados como medios existentes; no volver a componer, muxar, generar música, recapturar native ni lanzar CLI smoke. Solo verificar los medios existentes, extraer siete PNG y emitir recibo técnico/bundle.

R5 destino: `tools/c11d/d9/RUN_C11E_E4C_V2_3_R5_EXISTING_OUTPUT_RECOVERY.ps1`. El estado técnico seguirá pendiente de aceptación visual/auditiva humana. E1=`PREPARE_ONLY`; family adapter=`NOT_CONNECTED_E1`; production dispatch=`FALSE`; release authority=`NONE`.


## R6 superseding execution state — 2026-11-14

This addendum supersedes prior R5 recovery instructions where they conflict.

- R5 install and its independent post-install audit are accepted PASS. R5 recovery failed closed with `stored composition plan schema mismatch`: the stored output plan is correctly `C11E-E4C-DRILL-VISUAL-COMPOSITION-PLAN-V2`; the R5 recovery path incorrectly treated this snapshot as V1. The historical R3 output is not eligible for operator review because it predates the new family-title bridge. Do not attempt to publish it.
- Operator human review of R3: audio PASS, editorial content PASS, body/footer layout PASS; visual title treatment FAIL. The native family default title remained during PRE_ROLL/countdown and the D editorial title appeared only in GAME with a different style/alignment.
- R6 adds a D-owned editorial-family-title amendment pinned at SHA-256 `1d0d5393368ca1e1ecb867059314e28463205fffc81e8af902909896e0ac7331`. For `visual_drills/tracking/tier-1`, the D editorial title replaces the family-default title from PRE_ROLL frame 0 and uses the observed family treatment in both PRE_ROLL and GAME: pinned Inter-Bold, 22 px, 29 px line spacing, warm-gold RGB `(235,215,161)`, centered, rect `(36,63,648,104)`. The native source was sampled at PRE_ROLL indices 0,15,30,45,60,75,89; no title animation was observed, so the amendment records a static title.
- PRE_ROLL body/countdown and footer remain pixel-identical for all 90 frames; GAME body remains pixel-identical for 630 frames; END_CTA remains full native passthrough for 90 frames. Subtitle occupies y=169..190 below the family title; CTA retains its approved lower band. Timebase remains 90/630/90 = 810 frames at 30 fps.
- R6 uses a new output ID and a fresh D-owned composition from the already-accepted native source MP4 and existing A/B/C WAV files. Recomposition and remux are limited to this new user-directed D presentation change; no native capture, Godot, C11-C generator/launcher, family music generation, E1 service mutation, production dispatch, or release promotion is performed.
- The R6 recovery path does not reuse R3/R5 MP4s as acceptable outputs. It validates the preserved E1 evidence (raw file SHA and canonical intent SHA separately), the 91 source pins, V1 source plan, frozen baseline, and new D plan amendment, then produces fresh A/B/C outputs, seven review frames, a technical receipt and an operator review ZIP.
- R6 status before Windows execution: package is prepared; installation and independent audit remain pending operator logs. E4C V2 remains 0/20 until human visual/audio acceptance of `tracking/tier-1`.
- Strict boundaries remain: E1 `PREPARE_ONLY`; family adapter `NOT_CONNECTED_E1`; C11-C frozen manifest unchanged; `production_dispatch=false`; `release_authority=NONE`. Git checks skipped; commits operator-managed.

### E4C R6 exit sequence

1. Install R6 and independently audit the 20 destination operations, 5 replacement backups, 21 source pins and frozen manifest.
2. Run the fresh R6 family-title bridge requalification once on the existing accepted smoke evidence.
3. Obtain technical receipt and 7-frame / A-B-C review bundle.
4. Operator reviews title from countdown frame 0, font/style/alignment, body/countdown identity, subtitle/CTA positions, END_CTA passthrough, audio and synchronization.
5. Count `tracking/tier-1` only after signed human acceptance; proceed with remaining 19 selectors. E5 starts only after E4C reaches 20/20.

## R6.1 packaging correction — 2026-11-14

R6 original install was fail-closed before transaction. The accepted R2 transaction journal proves that `tests/test_c11e_e4c_drill_visual_composition_consumer.py` was replaced in run `C11E_E4C_HISTORICAL_REQUAL_V2_3_R2_20261113T072125Z_351b67d0`: preimage `62327e32ed4c15b497efb4a93fecc1d484cebff0b79beaa7ced5099905ffb2bf`, postimage `42e4cb8097ea9536dca63627e82c240ce0bb5b73baf03152269a35ac219a68eb`. R6.1 correctly uses the latter as the active REPLACE preimage. The other four R6 replacement preimages are unchanged and trace to accepted R2/R4/R5 transaction journal postimages. R6.1 adds five explicit `preimage_lineage` records to the package manifest; installer and independent auditor both require exact one-to-one lineage bindings. This is a package-manifest correction only: no protected C11-C source, frozen manifest, E1 service, canonical decision record or gameplay/media artifact is modified by this correction.

R6.1 is a new add-only package delivery identity. The previous R6 package is superseded and must not be installed. The R6 functional payload (family-title bridge, V2 plan-schema correction and R6 runner) is unchanged. On installation, the operator must capture the R6.1 `RUN_ID`, independently audit its receipt and journal, then run the new R6 family-title bridge qualification once. The old R3 outputs remain historical evidence only and must not be accepted as the new editorial result.

## R6.2 test-oracle and execution correction — 2026-11-14

R6.1 correctly passed its package/source-pin/preimage-lineage preflight, then failed closed before transaction at consumer test 10. The approved family-title gold is RGB `(235,215,161)`, while the test required all three channels to exceed 180; its blue channel is 161, so the predicate could not count even correctly rendered title pixels. R6.2 corrects the test to use a chromatic gold threshold `(180,160,110)` for the title and retains near-white thresholds for subtitle/CTA. The compositor, approved typography/color, geometry, native body and timebase are unchanged. R6.1 produced no transaction writes or R6.1 receipt. User-side audit/runner lines that later read a stale R5 run ID or missing runner are invalid and must not be cited as R6.1 evidence. The R6.2 package includes a fail-closed one-shot orchestration script: unique temporary extraction, exact package hash/inventory, install receipt identity, audit receipt identity, then runner only after both prior phases pass. All current documents and continuity prompts are included in this same ZIP. R6.2 is the sole active candidate; E4C remains 0/20 accepted pending the new seven-frame/three-video operator review.

## Current E4C checkpoint — 2026-11-14 (R6.3)

R6.2 passed installer, independent audit and 810-frame existing-media requalification; 7/7 review frames were produced. The operator accepted end-to-end editorial data propagation and overall layout, including the R6 family-title bridge, but rejected subtitle/CTA role styling. R6.3 is the bounded correction: reuse the same accepted native capture and family WAVs, recompose D-owned presentation only, and carry C11C header/footer role typography and palette colors into subtitle and CTA. It must preserve the pixel-exact native GAME body, PRE_ROLL countdown/footer passthrough, END_CTA passthrough, 90/630/90 timing, H.264 video stream invariance, A/B audio identity and C distinct music. No new native capture, music generation or gameplay. E4C remains open until all 20 selectors have accepted evidence; tracking/tier-1 remains 0/20 pending R6.3 visual/audio acceptance. After E4C: E5 → E6 Smoke18 → E7 Matrix101 (CH_008/009 held; 99 provisional) → E8.

## R6.3 package pin-alignment correction — 2026-11-14

The initial R6.3 candidate (`74070cafbc0035de82ec6668472ad230f1bab0ce6565e83e1388cf99a50bc865`) declared an expected SHA-256 of `f22d246b4b3f768f0daf33f2adbbed0073d828595c85678a39d6ef37642d12ec` for `core/presentation/C11CVisualEditorialLayer.gd`. That value conflicts with the exact C11-C 2.19.12 frozen manifest already pinned by this project (`e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`): the frozen manifest records `f8f718c067a4d7a088cc16f244cc40209e7183bec93e44d8cb66eb6dd404cf7d` for the same source file, and the supplied R6.2 project snapshot contains that exact file hash. The candidate has been corrected to the frozen value in the D-owned consumer contract, amendment JSON, package source-pin manifest and documentation. No C11-C source, frozen manifest, E1 service or protected runtime file has been changed. Use only `C11E_E4C_DRILL_HISTORICAL_REQUALIFIER_V2_3_R6_3A_PIN_ALIGNED_20261114.zip`; the initial R6.3 ZIP is superseded and must not be installed. Windows installation, independent audit, 32 focused consumer tests and fresh R6.3 technical requalification remain pending. `tracking/tier-1` remains 0/20 until subsequent human visual AND audio acceptance.

## R6.3A current disposition — 2026-11-14

R6.3A supersedes all earlier R6.3 ZIPs and hand-written preflight commands. The initial candidate's C11C editorial-layer pin was wrong; the pin-aligned rebuild had stale package-file hashes/byte counts and an external/embedded driver mismatch; and the first radius-cardinality resolver rejected the known R6 `tracking/tier-1` sample because five tracking backgrounds fell within radius 8. R6.3A aligns the source pin to the immutable C11-C frozen manifest, recomputes inventory hashes from final bytes, ships an external orchestrator byte-identical to the embedded copy, and ranks the 24 palettes by maximum per-channel distance. It accepts only best distance <=8 with runner-up margin >=1; ties fail closed. The observed R6 sample `(1,15,12)` resolves to `AQUAMARINE_SUN` (best2, runner-up6, margin4). Tests cover that sample, tie rejection and all 96 palette rows.

The accepted native identity receipt pair records 1,112,459 bytes and SHA-256 `d10950bca9358de4ffe8a9f4f24c8c35cdb37e25050775a9220a4d15ffb45338`. The earlier manually typed 68-character digest was invalid and is withdrawn. R6.3A reads media identities from accepted receipts and verifies actual MP4/WAV files in the active checkout; no separate manual media preflight is to be run.

Windows PowerShell AST, PySide6/Qt offscreen 32-test suite, File.Replace forward/rollback, install, independent audit and new technical requalification remain pending. Use only the R6.3A one-shot orchestrator; it stops on first failure. Do not repeat accepted R6.2 recovery tests 18/18, GUI/CLI smoke, native capture, Godot or music generation. Human E4C acceptance remains `tracking/tier-1=0/20` until seven-frame visual and A/B/C audio approval. Next: E4C 20/20 → E5 → E6 Smoke18 → E7 Matrix101 (CH_008/009 held; 99 provisional) → E8.

Governance: C11-C 2.19.12 frozen manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; E1 PREPARE_ONLY; family adapter NOT_CONNECTED_E1; production dispatch false; release authority NONE; GIT_CHECKS=SKIPPED; COMMITS=OPERATOR_MANAGED.

## R6.3A execution status — 2026-11-14

The current E4C work remains inside the first-selector role-style correction. Recover the independent audit using first install run `C11E_E4C_V2_3_R6_3A_20261114T163406Z_fc8436fa`, then produce the fresh D-only audiovisual qualification once. Human acceptance remains 0/20 until operator review. After E4C 20/20, follow the currently documented roadmap E5 → E6 Smoke18 → E7 Matrix101 → E8 historical C-to-E regression, independent acceptance, freeze and separately authorized promotion. The reviewed roadmap version V92 formally specifies through E8; E9/E10 are an operator goal but are not defined in that reviewed roadmap artifact. Add them only through an explicit authoritative roadmap update; do not invent their gates.


## Authoritative continuation — R6.3A requalification resume (2026-11-14)

This section supersedes earlier R6.3A immediate execution instructions.

### Accepted gates (do not repeat)
- Original R6.3A install: `C11E_E4C_V2_3_R6_3A_20261114T163406Z_fc8436fa`; 3 REPLACE +15 ADD_ONLY, postimages 18/18, backups 3/3, pins 25/25, Python compile 3/3, consumer tests 32/32, File.Replace forward/rollback, immediate recheck PASS.
- Independent audit of that exact first transaction: `PASS_INDEPENDENT_POST_INSTALL_AUDIT`; journal 18/18, postimages 18/18, backups 3/3, pins 25/25, frozen C11-C manifest and immutable decision record PASS.
- Documentation recovery: 14/14 ADD_ONLY PASS; all nine current project docs, history record, PowerShell style guide V21 and Master/Start/First prompts were added.
- Second installer run `...163827Z_47eab402` is an idempotent replay that skipped all three replacements; its backup receipt claim is not audit authority. Do not rerun or use it.

### Current failure
Recovery root: `artifacts/tests/c11e/r6_3a_audit_recovery/20261114T192552Z_7650ad32`. A one-shot lock was created as `ATTEMPT_RESERVED`. The attempt then failed with the Windows PowerShell 5.1 parameter-set error because the recovery script supplied both `-FilePath` and `-Variable` to `Tee-Object`. This is not a FFmpeg failure. No successful child output ID was reported. The corrected continuation must prove no child output/diagnostic exists before reusing the reserved lock.

### Next action
The V1 continuation is superseded and must not be run. Run only `RESUME_C11E_R6_3A_REQUALIFICATION_AFTER_TEE_BINDING_FAILURE_V3.ps1` from the V3 continuation kit. It verifies the exact first install/audit receipts, prior 14/14 document transaction, existing ATTEMPT_RESERVED lock, previous parameter-binding failure, no child output ID/root/diagnostics, Python/PySide6, package identity and the exact installed runner SHA. It does not reinstall, re-audit or repeat the 32 tests. It starts the runner once with `Start-Process -Wait -PassThru` and separate stdout/stderr files; it captures the exit code before reading logs. A failure after the V3 CreateNew claim prohibits retry.

### Required result
Technical PASS means 810/810 composition frames, 90/630/90 phases, preserved GAME body and family role styling, identical A/B/C video elementary streams, identical A/B AAC and distinct C, FFprobe contract, zero drift, seven review frames, technical receipt and operator bundle. This does not count as human acceptance. `tracking/tier-1` remains 0/20 until the operator reviews seven frames and all three A/B/C MP4/audio outputs.

### Governance / roadmap
C11-C 2.19.12 frozen manifest remains SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; E1 `PREPARE_ONLY`; `family_adapter=NOT_CONNECTED_E1`; dispatch false; `release_authority=NONE`; Git checks skipped; commits operator-managed. No protected C11-C edits, new capture, music generation, Godot, GUI/CLI smoke or dependency changes. After E4C 20/20 proceed to E5 → E6 Smoke18 → E7 Matrix101 (CH_008/009 held; 99 provisional) → E8. E9/E10 have not yet been accepted as scoped phase definitions; define them from the governance/acceptance roadmap after E8 rather than inventing gates in this recovery.


## 2026-11-15 — E4C tracking tier-2 batch failed closed on stale PRE_ROLL guard

- Consumed BatchId: `E4C-TRACKING-T2-5-20261115T005529Z-a78c6c24`. It is permanently non-reusable because `EXECUTION_AUTHORIZED_ONCE.json` exists.
- First child: `tracking/tier-2` / `E4C-TRK-T2-a78c6c24`; process exit code 2; no CLI summary; no completed rows; batch progress `STOPPED_FAIL_CLOSED`.
- Exact child error: `D composition plan editorial must be hidden during PRE_ROLL`.
- Root cause: R6.3A V2 consumer plan allows the family title in PRE_ROLL and keeps subtitle/CTA GAME-only, while the older shared E4C D executor still rejected any `phase_visibility.PRE_ROLL=true`. The stale guard failed after E1 intent validation and D plan creation but before toolchain preflight, output-root creation, C11-C native launcher, Godot, FFmpeg, music or media.
- Corrective scope: update the existing D E4C executor helper to validate field-level visibility exactly; update its unit tests, tracking coordinator's executor source pin, coordinator tests, runner's V25 guide pin and documentation/prompts. Do not modify E1, CLI, GUI, C11-C, R6.3A consumer, or any music/rendering mechanics.
- Existing failure ZIPs and the consumed batch lock are retained. No rollback, output cleanup or same-BatchId retry is allowed.
- State: `tracking/tier-1` remains accepted; tracking tiers 2–5 remain pending; corrective overlay installation and a **new prepare-only** run are required before any further execution.
- Governance: C11-C frozen manifest unchanged; production dispatch false; release authority NONE; Git checks skipped; commits operator-managed.

## V2 correction — PRE_ROLL bridge installer and consumed batch (2026-11-15)

The V1 corrective package did not modify the checkout. Its installer stopped in pre-transaction manifest validation under PowerShell strict mode because `preimage_sha256` is intentionally absent from ADD operations but was dereferenced unconditionally. No staging transaction journal was created and no replacement backup/write was made. Do not rerun V1.

V2 corrects optional-property handling, validates exactly 5 REPLACE + 14 ADD operations, uses a flat ZIP root, pins all five exact active-checkout replacement preimages and checks V25 before installing V26. It stages the four Python source/test files plus read-only CLI/GUI source copies, runs compile and the two focused suites, and parses both PowerShell scripts before beginning a transaction.

The prior execution attempt `E4C-TRACKING-T2-5-20261115T005529Z-a78c6c24` remains permanently consumed. It stopped at `tracking/tier-2` with exit code 2 due to the old all-fields-hidden PRE_ROLL assertion. The failure receipt records no CLI summary, no completed selectors and no production output root. Do not retry the identifier. The V2 repair aligns only the existing D E4C executor validator/tests with the approved R6.3A title-only PRE_ROLL field contract.

No render, Godot, FFmpeg, music generation, media creation, production dispatch, E1 service change, GUI/CLI change, R6.3A consumer change, C11-C change or Git operation is performed by this installer. Following installation, run PREPARE_ONLY with a fresh BatchId and independently inspect it before any execution authorization.


## E4C current continuation — 2026-11-15

The E4C selector matrix remains 4 families × 5 tiers = 20 selectors. The sole accepted selector is `tracking/tier-1` (1/20). The tracking tier-2..tier-5 batch previously consumed its original ID and failed closed at tier-2 on the stale PRE_ROLL guard; do not reuse that ID. V3 fixed the executor field-visibility contract and installed successfully, but V3's batch wrapper/coordinator had stale SHA/style-guide dependencies. V4 reconciles those dependencies and runs only PREPARE_ONLY after installation.

After an independent PASS of the V4 prepare receipt, authorize the new tracking tier-2..tier-5 batch once; require all four technical receipts and separate visual/audio operator review before accepting those four selectors. Then continue the remaining 15 selectors under the existing family-specific grammar/timing/music contracts, without widening the tracking batch runner or introducing a new Producer, binder or executor. E4C closes only at 20/20 with all required technical and human acceptance. Next: E5 → E6 Smoke18 → E7 Matrix101 (CH_008/009 held because declared 11s conflicts with 12s phase sum; 99 provisional) → E8 independent acceptance.

Governance: frozen C11-C manifest `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; production dispatch false; release authority NONE; Git checks skipped; commits operator-managed.

## Pursuit recovery V4 — authoritative installer correction (2026-11-15)

The V3 recovery package was not executed: Windows PowerShell 5.1 rejected its script at parse time because the audit-receipt hashtable declared `source_pins_post` twice (the summary key and detailed array). The parser error occurred before installer execution, so V3 made no checkout mutations. Do not run V3.

V4 is the only recovery candidate. It retains the 19/19 ADD_ONLY destinations committed by V2, audits the exact V2 run `C11E_E4C_PURSUIT_BATCH_OVERLAY_V2_20261115T130255Z_b5f15417`, corrects the duplicate key to `source_pin_results_post`, and adds an operator-side `Parser.ParseFile` gate before invoking the installer. Its transaction is bounded to two SHA-pinned replacements (pursuit runner and runner-contract test) plus 15 ADD_ONLY documentation/prompt destinations. It must pass 34/34 source pins, frozen C11-C manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` / 796318 bytes, Windows PowerShell 5.1 AST, Python 3.13 tests and atomic I/O 6/6 before mutation.

V4's default embedded pursuit action is PREPARE_ONLY. Do not pass `-Execute`. Independently audit the V4 receipt, journal, two backups, 17 postimages, 34 source pins and the resulting five-selector BatchId before authorizing a later execution. Preserve all failed evidence. C11-C/E1/dispatch boundaries remain unchanged.
