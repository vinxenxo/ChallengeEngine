# C11E_CURRENT_AUTHORITY_20261115_V163 — authoritative update

## Current authority — Pursuit V2 failed transaction / V3 recovery — 2026-11-15

Current accepted coverage: E4C 5/20. Tracking 5/5 operator-accepted. Pursuit 0/5, Saccade 0/5, Peripheral Scan 0/5. No new Pursuit BatchId has been prepared.

Pursuit V2 run `C11E_E4C_PURSUIT_BATCH_OVERLAY_V2_20261115T130255Z_b5f15417` committed all 19 ADD_ONLY destinations and failed at `POSTINSTALL_SOURCE_PIN_RECHECK` with `FROZEN_C11C_MANIFEST_POST_FAIL`. Preserve the exact journal/failure/preflight/logs/stage. Do not rerun V2 or delete/rollback its files. V2's runner pin is independently wrong: expected digest `dcb2...` but packaged driver digest is `7164a83c882116081cda720b37c47107e9145ad2b918b759470b06c5eb3d5522`. The V3 recovery must audit the V2 19 destinations and 34 pins, replace only the runner/test by exact preimage pins, then create a new PREPARE_ONLY batch.

C11-C remains unchanged and authoritative; E1 `PREPARE_ONLY`; family adapter `NOT_CONNECTED_E1`; dispatch false; release authority NONE; no Git checks; commits operator-managed.

---

## V3 PURSUIT RECOVERY AUTHORITY — 2026-11-15

This update supersedes any V2 install-pending or next-action language below. The active project remains at E4C 5/20: tracking 5/5 operator accepted; pursuit, saccade and peripheral_scan each 0/5. C11-C 2.19.12 remains the sole production authority; frozen manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; E1 `PREPARE_ONLY`; family adapter `NOT_CONNECTED_E1`; `PRODUCTION_DISPATCH=FALSE`; `RELEASE_AUTHORITY=NONE`; `GIT_CHECKS=SKIPPED`; commits operator-managed.

Pursuit Overlay V2 failure `C11E_E4C_PURSUIT_BATCH_OVERLAY_V2_20261115T130255Z_b5f15417` is a partial ADD_ONLY transaction with all 19 operations marked `ADD_COMMITTED`, followed by `FROZEN_C11C_MANIFEST_POST_FAIL`. Preserve its failure receipt, in-progress journal, preflight, logs and stage. Never rerun V2, do not roll back or delete the 19 installed files. The installer completed its 34-pin post-check loop without recording a SOURCE_PIN_POST_FAIL, then failed on a separate second read of the frozen manifest. The failure receipt did not record the digest observed by that second read, so the supplied evidence cannot distinguish a transient second-read discrepancy from another read-path issue. Do not infer that C11-C was modified: the preflight and supplied repository snapshot both carry the frozen SHA and 796,318-byte size. V3 removes the uninstrumented second read, uses the captured frozen-manifest value from the 34-pin post-check as the authority, and persists every pre/post pin result and actual mismatch digest.

A second independent defect was found before launching the V2 runner: it pinned `c11e_e4c_pursuit_tier_batch.py` to `dcb2c035ff5aee83a673e30347617aed67c8b382bf85af68441153611964566b`, while the exact driver bytes in the same V2 package and package manifest are `7164a83c882116081cda720b37c47107e9145ad2b918b759470b06c5eb3d5522`. The V2 contract test repeated the stale value and therefore passed incorrectly. V3 pins the runner to the exact packaged driver and makes the test compute the staged driver's SHA and compare it with the runner declaration.

V3 is a recovery transaction, not a fresh installation: it audits the exact V2 run and its 19 existing destinations; verifies the original V2 package identity and 34 current source pins (the C11-C manifest is captured once); then performs exactly two pinned replacements (runner + runner test) with independently verified backups and adds the new versioned documentation. It runs the existing pursuit coordinator only in default `PREPARE_ONLY`, with separate child stdout/stderr capture and no `-Execute`. It creates no media or production dispatch.

Do not claim Pursuit installed or prepared until V3's recovery receipt, 2/2 real backups, 17/17 postimages, 34/34 pins and `PASS_PREPARE_ONLY_NO_RENDER` are independently audited. Any V3 failure after transaction start is evidence-only and must not be rerun.

--- HISTORICAL CONTENT BELOW ---

# C11-E current authority — V160 (2026-11-15)

## V160 authoritative checkpoint — Tracking closed; Pursuit V1 installer blocked pre-transaction (2026-11-15)

**E4C Visual Drill remains OPEN at 5/20 accepted.** `tracking/tier-1..tier-5` are accepted 5/5. Pursuit, saccade and peripheral_scan remain 0/5 each.

### Pursuit overlay incident

The V1 package outer SHA and embedded payload were verified, and 34 source pins were checked before staged test execution. Installer V1 failed at line 172 when it captured Python `unittest` with `& $python $stageTest1 2>&1` under `$ErrorActionPreference='Stop'`. In Windows PowerShell 5.1, native stderr becomes a terminating `NativeCommandError`; unittest writes normal test progress to stderr. The displayed test method ending `... ok` is only an individual test line. The full test suite result and exit code were not reliably collected.

The failure happened before transaction start. There is no install transaction journal, no committed ADD_ONLY destination and no installed pursuit runner. The only checkout-side artifact created by V1 was its run evidence directory; its uploaded evidence ZIP contains directory entries only because V1 did not persist a pre-transaction failure receipt. No production output, execution lock or media exists. The original V1 run `C11E_E4C_PURSUIT_BATCH_OVERLAY_V1_20261115T085956Z_6143b4e3` is historical and must not be reused.

### Current approved candidate

V2 fixes child-process capture with `Start-Process -Wait -PassThru`, separate standard-output/error files, immediate `$process.ExitCode` capture and log reads only after process exit. It adds durable `INSTALL_PROGRESS.json` and `INSTALL_FAILURE.json` for all failure stages, retains staged payload on failure, and extends the PowerShell style guide to V30. Its 19 operations are all ADD_ONLY; no replacement, deletion, E1/CLI/GUI/C11-C mutation or dispatch change is permitted.

Install V2 once using its SHA sidecar. Require all 34 source pins and frozen C11-C manifest, Python 3.13/PySide6, py_compile, 10/10 coordinator tests, 8/8 runner-contract tests, PowerShell 5.1 AST and atomic-I/O 6/6 before transaction. Embedded action is PREPARE_ONLY only. Independently audit the exact receipt/journal/postimages and the five pursuit selectors before any separate execution authorization.

Governance remains C11-C 2.19.12 frozen SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; E1 `PREPARE_ONLY`; family adapter `NOT_CONNECTED_E1`; production dispatch false; release authority NONE; Git checks skipped; commits operator-managed.


## Authoritative checkpoint — Tracking family closeout and pursuit handoff (2026-11-15)

**E4C Visual Drill remains OPEN at 5/20 accepted.** The complete tracking family segment is closed at 5/5: `tracking/tier-1` was previously accepted; `tracking/tier-2` through `tracking/tier-5` are now technically qualified and explicitly operator-accepted.

### Accepted batch

- Batch: `E4C-TRACKING-T2-5-20261115T074835Z-6239dd21`.
- V4 installer: `C11E_E4C_TRACKING_BATCH_RUNNER_V4_INSTALL_20261115T074834Z_7f33f450`, PASS; independent installation audit PASS.
- Batch status: `PASS_TECHNICAL_PENDING_OPERATOR_A_V_REVIEW`; all four selector rows passed with child exit 0.
- Evidence ZIP SHA-256: `a96fd5f7f83e51dfc667dcdc79fbf8afda3461c107fa3a78870cce1a847084c5`; 176 entries, CRC PASS.
- Full selector receipts and physical A/C MP4 + A/B/C WAV hashes verified. 810 frames at 30fps/27s, 90/630/90; 91/91 source pins pre/mid/post; A/C video elementary streams identical; A/B music same-seed identity and C changed-seed distinction; H.264 High/yuv420p TV + AAC-LC 48kHz stereo; zero A/V start drift.
- The operator explicitly approved all four video/audio/editorial/layout results. T2–T5 are `OPERATOR_ACCEPTED`.
- The small `e4c_tracking_tier_batch.zip` is the previous failed, consumed BatchId ending `a78c6c24`; preserve it. Never retry it.
- The new evidence ZIP does not include aggregate `BATCH_RESULT.json` or the four outer CLI result JSON files. Their status and claimed hashes are recorded from the supplied PowerShell console transcript, not described as independently rehashed. Per-selector full receipts and media were independently hashed from the archive.

### Current acceptance matrix

| Family | Accepted | Remaining | Required family music profile |
|---|---:|---:|---|
| tracking | 5/5 | 0 | FLOWING_VECTOR |
| pursuit | 0/5 | 5 | ORGANIC_BLOOM |
| saccade | 0/5 | 5 | CIRCUIT_PULSE |
| peripheral_scan | 0/5 | 5 | ORBITAL_RITUAL |
| **E4C total** | **5/20** | **15** | family-isolated |

### Next work

The next family is `pursuit/tier-1..tier-5`. Use only the new pursuit-family coordinator/launcher and its add-only installer. It must pin the exact R6.3A sources, V4 tracking coordinator/wrapper, accepted CLI baseline, frozen C11-C manifest and Style Guide V29; expected music profile is `ORGANIC_BLOOM`. First run installation + PREPARE_ONLY, independently audit its receipt and fresh BatchId, and only then separately authorize execution. No use of the tracking runner for a different family.

After pursuit 5/5, continue saccade, then peripheral_scan under their own family music/visual contracts. E4C closes only at 20/20 technical PASS **and** operator A/V acceptance. Only then E5 → E6 Smoke18 → E7 Matrix101 → E8. Do not start E5 early.

### Non-blocking quality note

All four native Godot shutdown logs contain one leaked `CanvasItem` RID warning and one leaked `ObjectDB` instance warning. No `ERROR`/`SCRIPT ERROR` appears; stdout records completed 810-frame capture and all full receipts, output hashes and FFprobe gates pass. Keep the warning visible in the incident register as non-blocking for this accepted batch; investigate if repeated outside these same clean-completion conditions or if it escalates.

Governance remains: C11-C 2.19.12 frozen manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; E1 `PREPARE_ONLY`; family adapter `NOT_CONNECTED_E1`; `PRODUCTION_DISPATCH=FALSE`; `RELEASE_AUTHORITY=NONE`; `GIT_CHECKS=SKIPPED`; `COMMITS=OPERATOR_MANAGED`.

---

**Historical checkpoint content follows unchanged for traceability; this update supersedes conflicting earlier status and next-action statements.**

## V3 PRE_ROLL installer authority update (2026-11-15)

- The V2.1 installer was launched after its ZIP, manifest, installer and Python preflight checks passed. It created its transaction journal, then failed on the first journal update because `System.IO.File.Replace(source, destination, $null)` supplied a null backup path. The failure occurred before the first project payload mutation. Preserve the V2.1 evidence; never rerun V1, V2 or V2.1 installers.
- The only current installer candidate is `C11E_E4C_TRACKING_PREROLL_BRIDGE_FIX_V3_20261115.zip`. Its transaction helper uses an explicit unique sibling backup path for journal/receipt updates and pinned replacements. The installer includes PowerShell 5.1 AST parsing and a six-case isolated atomic-I/O test before creating the installation transaction journal.
- V3 install remains **PENDING** until its Windows PowerShell 5.1 run returns `PASS_PINNED_REPLACEMENTS_AND_ADD_ONLY_DOCS`. Required gates remain 5 exact preimage backups, 19/19 postimages, 30/30 pre/post source pins, all focused Python tests and unchanged frozen C11-C manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- The failed batch `E4C-TRACKING-T2-5-20261115T005529Z-a78c6c24` is permanently consumed. No batch execution occurs in V3 installation. After independent install audit, create a fresh PREPARE_ONLY batch using a new BatchId; execution remains separately gated. E4C stays at 1/20 accepted.
- Governance: `production_dispatch=false`; `release_authority=NONE`; `GIT_CHECKS=SKIPPED`; `COMMITS=OPERATOR_MANAGED`; source SHA pins remain enforced.

## Current authority and acceptance

- Production baseline: C11-C 2.19.12 only; frozen package manifest 796,318 bytes / SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- R6.3A V3 technical requalification is accepted for `tracking/tier-1`; operator explicitly accepted A/B/C audio/video, editorial, layout, typography/style and review on 2026-11-15. E4C accepted coverage is 1/20.
- CLI smoke `tracking/tier-1` is already PASS and retained; do not rerun.
- Tracking batch V1 installation: PASS_ADD_ONLY_INSTALL, 17/17 additions, 30/30 source pins. PREPARE_ONLY: PASS for four rows. Its one-shot BatchId `E4C-TRACKING-T2-5-20261115T005529Z-a78c6c24` was consumed by an authorized attempt that stopped fail-closed at tier-2, child exit 2, with no CLI summary or product output. Do not retry it. The bridge correction V2 package is prepared but not yet installed. Accepted coverage remains 1/20.

## Scope of the next batch

The coordinator submits four independent canonical requests in sequence through `c11e_production_cli.py --origin CLI --execute-drill-av`, using the already-pinned `c11e_e4c_drill_execution.py`. It clones only the accepted tier-1 CLI request contract, changes the selector, request ID and tier title, and preserves gameplay seed 12345 / music A-B seed 840001 / REVIEW_720 / audio / personalization / presentation profile. The existing executor derives C's changed music seed and resolves FLOWING_VECTOR for tracking. Per-row A/B/C music generation and A/C muxing are qualification work, not release dispatch.

## Non-negotiable boundaries

No C11-C source edits, no E1 edits, no producer/binder/GUI changes, no dependency installation, no Git checks. Existing source pins and frozen manifest must match exactly before the first selector and after each successful selector. Fail closed on any pin drift, existing output path, nonzero child exit, receipt mismatch, FFprobe mismatch, audio/video isolation failure or source pin change. The one-shot authorization marker prevents retry with the same batch ID after execution starts.

All successful machine receipts remain `PENDING_OPERATOR_VISUAL_AUDIO_REVIEW`; operator approval is a separate gate. E1 remains `PREPARE_ONLY`; `family_adapter=NOT_CONNECTED_E1`; production dispatch false; `release_authority=NONE`.

---


# C11-E CURRENT AUTHORITY V152 — 2026-11-14

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

# C11-E CURRENT AUTHORITY V143 — 2026-11-13

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

## Superseded document baseline (C11E_CURRENT_AUTHORITY_20261112_V141.md)

The following content is retained for traceability; the authoritative state and next action are defined in the update above.

# C11-E E4C V2.2 PIN-ALIGNMENT R1 — CURRENT AUTHORITATIVE STATE (2026-11-13)

**This block supersedes all earlier E4C V2 installer instructions below.** Older V1.7–V2.2 incidents remain historical evidence; do not rerun superseded packages.

## Current authority and incident disposition

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

# CURRENT EXECUTION AUTHORITY — accepted GUI single-selector A/V pilot / CLI smoke pending — 2026-11-12


## Authoritative installer correction — V1.8 package-binding failure / V1.9 consolidated recovery (2026-11-12)

The operator's V1.8 run passed the ZIP sidecar and entered the package installer, then failed closed at `OPERATION_PACKAGE_FILE_BINDING_FAIL` for `docs/current/e/C11D_E_BLOCKER_REMEDIATION_REGISTER_20261112_V54.md`. The V1.8 builder renamed physical documentation payloads to the next versioned filenames (for example V55) but failed to regenerate the matching `replacements`/`additions` destination rows; several operation destinations still referenced their predecessor names. The validator correctly rejected the mismatch before the transaction journal or destination writes. This was a package-manifest construction defect, not a Windows runtime issue. Do not rerun V1.8.

V1.9 is a complete rebuilt overlay. Its operation rows are generated directly from the physical payload tree: `payload/replace/<relative>` maps only to `REPLACE <relative>`, and `payload/add/<relative>` maps only to `ADD_ONLY <relative>`. The installer independently enforces that mapping for every operation, verifies one-to-one closure between all payload files and operation rows, rejects duplicate package paths and destination paths, and checks manifest counters against actual arrays. The V1.9 matrix is exactly one existing D-consumer replacement plus 23 add-only destinations (24 mutation operations); package inventory also includes the README and installer. All versioned current-doc and prompt destinations now match their package paths exactly.

V1.9 preserves the V2 consumer, 18 focused tests, requalifier, runner, 21 support pins and 91-pin/CLI source evidence unchanged. The only changes from V1.8 are installer/manifest construction integrity, corrected operation destinations, documentation/prompt version increments, and incident recording. The V1.8 attempt failed before transaction; no checkout destination mutation occurred. V1.9 remains `NOT_YET_INSTALLED` pending its Windows 5.1/Python 3.13/PySide6 preflight and transaction receipt.

The V1.9 installer also reports pre-transaction failures distinctly as `FAIL_CLOSED_PRE_TRANSACTION_NO_DESTINATION_WRITES` with a `%TEMP%` diagnostic, rather than labelling an empty journal as a completed rollback. No Git, pip, shared dependency, GUI/CLI, E1, C11-C, dispatch or release changes are permitted.


**Current E4C position (2026-11-12):** the first single-selector GUI A/V qualification is accepted for `visual_drills / tracking / tier-1`. The operator confirmed visual and listening review PASS. Evidence `D99-GUI-6514F1066E79-production.zip` SHA-256 `5fb910dd7515ca1f80f2fa77a0829836613e933ca7106f00852ccd31d797f8e4`; tests/plan bundle `D99-GUI-6514F1066E79-tests.zip` SHA-256 `5c94ad64666548db478a4265a71345efe28c2a346f215e7cdb477f51dc8dde91`; qualification receipt SHA-256 `d8aad7176ed99d8bc0c067cece58272c5ac44045d55d746c768ea72324d459db`; RUNNING receipt SHA-256 `2f9b388b3541548d79c254161290ad73241109349aea1f57c1ac9c10e092ab2a`. The receipt status is `PASS_E4C_DRILL_SINGLE_SELECTOR_A_V_QUALIFICATION`.

**Independent audit:** 91/91 E1 source pins are identical at pre-execution, immediately-pre-render and post-execution; GUI/CLI E1 semantic identity parity PASS; 810/810 frames composed at 30 fps; phases PRE_ROLL/GAME/END_CTA = 90/630/90 frames; GAME editorial fields are populated and D-composed. `FAMILY_MUSIC_V4` `FLOWING_VECTOR` produces 27s, 44.1 kHz stereo PCM16; A/B seed 840001 WAV SHA `e54b960c799102fb104a99ccd7b94c4a41b5b22d54665acda72106b36646f277` is identical, C seed 840002 WAV SHA `5e81b6426f7915c7cad4c658fc24b90cd17c870a4497f45136a53e43b71efd40` differs. Final A and C are 27s, H.264 High 720×1280 yuv420p TV, 30 fps, 810 frames; AAC-LC 48 kHz stereo; both start at 0. Receipt stream hashes prove video A/C identical and audio A/C different; independent extraction also confirms raw H.264 SHA `500fc010b0d39062997d73643643943d03552082d75a2b8db6c55a3bbe5ad150` matches, while AAC elementary stream SHA differs (`23162fb059ca5e215758d6bbd58b6baba0efc9bd13e94d5921fd96726e19cd67` vs `f98747cc8f408521a3d00e7f4d90a066f3adf366de46d6f89bfefb65e26e86cd`). Final A SHA `7604f69e7c28e044a4bdb7fccc76c74604495ec9bbe4b46fcbca23a62b7c49ba`; final C SHA `d93753dabcfd85f3a3e721125081a649fbfa3a033a751e77a39df4c38357bf84`. Native source SHA `d10950bca9358de4ffe8a9f4f24c8c35cdb37e25050775a9220a4d15ffb45338`; silent D-composed intermediate SHA `60fd3155e70691bb7f2e636d20539e5898554669503888ee34bb78402c9589ad`.


## Authoritative update — V1.7 installer incident and V1.8 correction (2026-11-12)

V1.7 failed closed at `DESTINATION_PREFLIGHT` because it misclassified the newly introduced `tests/test_c11e_e4c_drill_visual_composition_consumer.py` as a replacement. The destination was absent in the active checkout. The declared preimage SHA `aedeb5754d94fdbaad134a653f57ca07466c845dcef081c8774668245455a7a0` is actually the historical V9 test stored under `tools/c11d/d9/`, not a preimage at the new `tests/` path. This is a manifest/installer classification defect, not a V2 consumer failure. The failure occurred before evidence-root and transaction-journal initialization; no destination writes or repository mutations occurred. Its generic `FAIL_CLOSED_ROLLBACK_COMPLETE` message reflects a zero-entry/no-op rollback.

V1.8 supersedes V1.7 and is the only candidate permitted for installation. Its operation matrix is exactly one hash-guarded replacement (`tools/c11d/d9/c11e_e4c_drill_visual_composition_consumer.py`) plus 22 `ADD_ONLY` destinations, including the new test module. The installer asserts the exact classification, unique operation destinations, and uses manifest-resolved package paths for staged inputs. It rechecks all source pins and all destination states before journaling/writing. Do not rerun V1.7. No source, GUI/CLI, E1 service, executor, C11-C or shared dependency changes are included.

V1.8 install status: `NOT_YET_INSTALLED`. Do not claim V2 Windows qualification from package/static checks. After install PASS, reuse the already accepted CLI native MP4 and WAV A/B/C for the existing-media V2 requalification; no new C11-C capture or music generation. E4C remains open, V2 A/V acceptance pending operator review, matrix not started. C11-C remains sole production authority; E1 PREPARE_ONLY / NOT_CONNECTED_E1; dispatch false; release authority NONE.

Governance: C11-C frozen manifest remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; `c11c_source_mutation=false`; D3 V5 not invoked; source C11-C audio remains disabled via `-NoSound`; renderer invocation is solely the explicitly authorized isolated E4C qualification scope; `production_dispatch=false`; `release_authority=NONE`. E1 stays `PREPARE_ONLY`, `family_adapter.status=NOT_CONNECTED_E1`. Do not turn these isolated test results into production dispatch or release authority.

**Next gates:** (1) CLI-origin A/V smoke through the existing CLI facade with `--execute-drill-av --origin CLI`, using the same shared D executor and a fresh request ID; (2) 20-selector family A/V matrix; count the accepted GUI `tracking/tier-1` pilot as matrix row 1 and do not rerun it for matrix coverage; (3) E4C closeout only after CLI smoke, all remaining 19 selectors, receipts, human review and source-pin integrity. Then E5 → E6 Smoke18 → E7 Matrix101 (CH_008/009 held; 99 provisional) → E8 historical C-to-E regression, independent acceptance, freeze and separately authorized promotion.

## Accepted pilot facts
- Request `D99-GUI-6514F1066E79`, `tracking/tier-1`, gameplay seed `12345`, music A/B `840001`, changed C `840002`, `REVIEW_720`, audio and personalization on, all three editorial strings non-empty.
- E1 `PASS_E1_PREPARATION_ONLY`; 91 source pins. GUI/CLI semantic identity equality true. The D-owned executor is shared by the existing Producer GUI and CLI facade.
- D composition plan SHA `4b69b51915509911d2a394955112b54ebaa93eced1ffaceb8a4702bcd65ec729`; composition receipt covers all 810 frames.
- Operator visual and audio review: PASS.

## CLI smoke acceptance gate
The CLI smoke is a distinct invocation from the existing `c11e_production_cli.py` with a fresh request ID and `--execute-drill-av --origin CLI`. It must call `tools/c11d/d9/c11e_e4c_drill_execution.py`, complete the same A/B/C stream-isolation and FFprobe checks, and leave all 19 critical pins unchanged before and after. Do not infer CLI execution PASS from the GUI receipt or the E1 plan-parity receipt.

The overlay V1.5 adds only an add-only CLI smoke runner, tests, history/current documentation and continuity prompts. It does not modify GUI, CLI facade, E1 service, executor, consumer or C11-C.

---

## Superseded prior revision content

V1.3 installer installation is accepted on Windows: `TRANSACTION_API_PREFLIGHT=FORWARD_AND_ROLLBACK_PASS`, `PASS_REPLACE_AND_ADD_ONLY_INSTALL`, 13/13 tests and 6/6 py_compile. This does not establish A/V acceptance.

The first GUI plan for `D99-GUI-85201B7B4FF7` passes E1 preparation, GUI/CLI parity and D editorial plan validation. Its A/V invocation fails at the existing native launcher argument binder: adapter locale formatting changes profile multiplier `0.75` into a comma decimal and PowerShell reports 75000 > 3.0. No C11-C native video, D-composed frames, family music, muxed media or final A/V evidence was generated.

V1.4 changes only the D-owned execution adapter and its tests (two replacements); adds updated current docs/history/prompts; does not replace `main.py` or CLI again. A PowerShell wrapper parses invariant ASCII decimal into a typed `System.Double` and invokes unchanged pinned C11-C script. Installer includes a staged `es-ES` wrapper-to-dummy-launcher probe that must record `0.75`, in addition to the source pins, 16/16 tests, compilation and V1.3 transactional safeguards.

Retry with a fresh request ID; preserve failed D99 evidence. The expected path is install → inspect postimages → fresh GUI plan → `tracking/tier-1` A/V → human review → CLI smoke → 20 A/V selectors → E4C close. C11-C alone remains production authority. E1 remains PREPARE_ONLY / NOT_CONNECTED_E1; dispatch false; release NONE. Git checks skipped; commits operator-managed.



## D99-GUI-85201B7B4FF7 — single-selector A/V pilot diagnosis — 2026-11-12

**Authoritative evidence:** `D99-GUI-85201B7B4FF7.zip` SHA-256 `0913179f9852b7b1f75c2a7e2f763a111bc8d807d08d20036a2891ae94661f56`; `D99-GUI-85201B7B4FF7-tests.zip` SHA-256 `16f0e199429deffb85025cd35d0cfd4fe2ec9fe237cf66482f6de6b14cd6ef23`.

The GUI's **Resolver + Plan** stage is successful, not a failure: E1 receipt is `PASS_E1_PREPARATION_ONLY`; GUI/CLI semantic parity is `PASS`; D9.10 bridge planning is `PASS_BRIDGE_PLANNING_ONLY`; D composition plan is valid with real GAME-visible editorial; the request is `visual_drills / tracking / tier-1`, gameplay seed `12345`, music seed `840001`, `REVIEW_720`. This remains deliberately plan-only at E1 and does not claim renderer or dispatch activation. The second GUI action, the shared D A/V executor, fails before the native C11-C producer starts.

Exact failure from `logs/c11c_drill_producer.log`: C11-C's `run_visual_drill_production.ps1` rejects `-SpeedMultiplier` because it receives `75000`, outside `[ValidateRange(0.1,3.0)]`. The pinned profile `profiles/difficulty/visual_drill_tracking.json` has tier 1 `speed_multiplier=0.75` (source SHA-256 `6de8812bd46904e122ecdd0eae22fb2979bd75399c34779248c6569e833c921e`). The adapter applied Python's host decimal separator and sent `0,75000`. On the operator's locale, Windows PowerShell 5.1 parameter binding split/coerced that comma decimal and delivered `75000`. This is a cross-locale numeric argument-boundary defect in the D adapter, not a defect in the pinned C11-C launcher or difficulty profile.

The failure occurs before a successful C11-C capture. There is no native MP4, no D frame composition, no FAMILY_MUSIC_V4 WAV generation, no mux, and no final FFprobe result in this run. The failure does not indicate an editorial, font, Qt, geometry, phase/timebase, music determinism, or A/V stream-equivalence defect. The first evidence bundle contains `RUNNING` and `FAILURE` receipts and the exact native producer log. The `-tests.zip` is a preparation/parity/contract receipt bundle; it does not show a second independent A/V failure. Do not infer additional failures from its intentionally plan-only receipts.

**V1.4 correction:** remove host-locale formatting entirely. Python emits an ASCII invariant string such as `0.75000` to a string-typed PowerShell wrapper. The wrapper parses it with `[System.Globalization.CultureInfo]::InvariantCulture`, sets the wrapper thread culture to invariant for the call, then invokes the existing pinned C11-C launcher with an already-typed `[double]$speed`. The native C11-C launcher remains byte-identical and receives `0.75`; C11-C stays silent via `-NoSound`. The wrapper is retained in the run logs and its hash/argument are written into the execution receipt. Regression tests cover invariant formatting, wrapper parse/type handoff, and absence of host-locale formatting. The V1.4 installer additionally executes this exact wrapper against a dummy parameter-compatible launcher while forcing `es-ES`, and requires the dummy to record `0.75` before any repository mutation.

The failed output root `artifacts/production/c11e/D99-GUI-85201B7B4FF7` is intentionally preserved. It must not be overwritten. The retry must use a **new unique request_id/output root** (generate a fresh GUI request and repeat Resolver + Plan); do not delete or recycle this failed evidence. After V1.4 installation PASS: audit its postimages/source pins, rerun the GUI plan stage with a fresh ID, then execute only `tracking/tier-1`. Continue only when native capture, D composition, FAMILY_MUSIC_V4 A/B/C, final A/C video/audio stream hashes, FFprobe, and human visual/listening review pass. CLI smoke/parity follows on the same shared adapter. Do not start the 20-selector A/V matrix until the single-selector result is accepted.

Governance is unchanged: E1 `PREPARE_ONLY`; `family_adapter.status=NOT_CONNECTED_E1`; `production_dispatch=false`; `release_authority=NONE`; no Git checks; commits operator-managed; C11-C frozen manifest SHA remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.


---

## Installer V1.3 transactional API correction — 2026-11-11

The operator's V1.2 Windows run passed staged validation and entered `TRANSACTION_START`, then failed on OP-001 at `System.IO.File.Replace` because the installer passed `$null` as the required destination backup path in this Windows PowerShell/.NET Framework environment. The diagnostic records `rollback=COMPLETE`, one journaled operation, `OP-001=ALREADY_PREIMAGE`, and no C11-C source mutation. V1.3 supplies unique non-existing backup paths in both forward replacement and rollback, journals rollback backup paths before mutation, verifies the displaced pre/post images by SHA-256, and runs a disposable forward+rollback File.Replace API probe before any repository transaction. Operation scope, Producer/CLI/adaptor bytes, E1 semantics and governance remain unchanged. V1.3 remains a candidate until the Windows installer itself passes all pre-write checks and produces a complete receipt.

## Installer V1.2 correction — 2026-11-11

V1.1 passed package inventory, source pins, destination preflight, Python 3.13/PySide6/Qt probes and staged `py_compile` on the operator's Windows PowerShell 5.1 host. It then stopped at `STAGED_UNIT_TESTS` after unittest emitted a case ending `... ok`. The failure diagnostic shows no transaction journal, `rollback=NOT_NEEDED`, and no checkout mutation. Root cause: Python unittest reports verbose progress on stderr; PowerShell 5.1 with `$ErrorActionPreference='Stop'` promoted the native stderr stream into `NativeCommandError` before exit-code evaluation. V1.2 captures stdout/stderr separately via .NET `ProcessStartInfo`, drains both asynchronously and evaluates only the actual process exit code. No E1, Producer, adapter, test or C11-C source semantics are changed. V1.2 remains pending Windows installer acceptance.

## Current installer correction — V1.1

The first Windows attempt of installer V1 reached staged Python validation and failed at the inline `python.exe -c` probe (`File "<string>", line 1`). No transaction journal was opened and no checkout write was made. V1.1 replaces both inline probes with temporary Python source files invoked by path, checks those probe files with `py_compile`, and writes a `%TEMP%` failure diagnostic containing stage and stack details on any failure. Use the V1.1 ZIP and its bundled installer only; do not run the standalone V1 installer.

# CURRENT EXECUTION OVERRIDE — E4C DRILL SHARED A/V ADAPTER V1.1 — 2026-11-11

The accepted E4C state is: Binder V2 20/20, native source capture 20/20, real-frame pixel qualification 20/20 selectors and 100/100 compositions, and operator visual review PASS. The next bounded implementation is the existing Producer GUI + existing E1 CLI facade + one shared D-owned execution adapter.

E1 remains `PREPARE_ONLY`; `family_adapter.status=NOT_CONNECTED_E1` is preserved exactly. The new D adapter consumes the E1-validated canonical intent downstream; it does not change the E1 service contract, add a Producer, binder, service, or suite module. The GUI and CLI invoke the same `tools/c11d/d9/c11e_e4c_drill_execution.py`. CLI execution is opt-in via `--execute-drill-av`; omission retains E1 preparation-only behavior.

The adapter requires at least one actual non-empty, non-`UNKNOWN` D editorial field (`title`, `subtitle`, or `call_to_action`) and verifies GAME-only visibility. It checks every E1 source pin immediately after canonical preparation, again immediately before native capture, and after execution; the three normalized pin sets must match. The frozen C11-C manifest is checked on all passes.

The isolated first A/V qualification is one selector, recommended `tracking/tier-1`, with gameplay seed `12345`, music A/B seed `840001`, changed C seed `840002`, profile `REVIEW_720`, audio and personalization enabled, and at least one real visible editorial text. C11-C capture is invoked with `-NoSound`; existing `C11CSafeAmbient.py` + `FAMILY_MUSIC_V4` receives `request.music_seed`. D3 V5 and C11-C gameplay-seed-coupled audio are excluded. Required outcome: A/B WAV hashes identical; C WAV distinct; A/C final encoded video stream hashes identical; A/C audio stream hashes different; FFprobe confirms H.264 High 720x1280 30fps yuv420p TV and AAC-LC 48kHz stereo.

This is explicitly authorized isolated engineering qualification, not general production renderer activation or dispatch. Receipt must keep `production_dispatch=false`, `release_authority=NONE`; `family_adapter.status` remains `NOT_CONNECTED_E1`. The operator's GUI runtime smoke and first real A/V run on the active Windows checkout remain pending. E4C is not closed until A/V, GUI/CLI parity, human listening/visual review and remaining 20-selector qualification criteria are accepted.

## Installer boundary

The self-contained overlay changes only `c11c-suite/c11c-producer/main.py` and `c11c-suite/c11c-producer/c11e_production_cli.py`, and adds the one D adapter plus tests/docs/prompts. It verifies source pins and exact preimages before writes, stages/compiles/tests before transaction, uses a persistent pre-mutation journal, exact SHA backups, atomic replacement, and hash-guarded rollback. It never checks Git and never installs Python packages.

---

## V9 current state — 2026-11-11

Consumer V8 stopped in `STAGED_VALIDATION` before any repository transaction. The exact cause was a StrictMode ordering bug in the installer: `$testSource` was inspected for the removed `QT_VERSION_STR` token before it was assigned from the staged test file. The run's journal is empty and `rollback=NOT_NEEDED`; no rollback or repository recovery is required. V9 fixes this by loading both `$consumerSource` and `$testSource` first, validating both are non-empty, and only then inspecting their contents. This is an installer-only correction. The Qt consumer, 35-test module and E1 service replacement bytes are unchanged from V8.

V9 also corrects the run ID and receipt/failure schema identities to V9. It preserves the 18-operation scope (one exact-pinned E1 service REPLACE + 17 D-owned ADDs), all 13 support pins, 10 design/font pins, exact-hash operator decisions, frozen C11-C manifest and no-new-dependency policy. The installer uses the existing canonical Producer Python/PySide6 only; it must not invoke pip, install/uninstall packages, change requirements or mutate shared environment dependencies.

V9 is a candidate only. Windows PowerShell 5.1 AST, Qt runtime probe, py_compile 3/3, tests 35/35, immediate pre-transaction rechecks and successful receipt are still pending. No consumer V1–V8 transaction has been recorded. Stop at first failure; do not repeat A.3 V5, binder V2, Godot V3, Loop22 or historical authoring accepted gates.

Next step: verify V9 ZIP SHA and sidecar, then run the V9 installer with the existing canonical `-PythonExe`. Require the same 18 destination states and all pre-write gates. After PASS, inspect `INSTALL_RECEIPT.json`, its SHA and all 18 postimages before any E1 integration review. C11-C remains sole production authority; renderer OFF; dispatch/media/audio OFF; `release_authority=NONE`.

---

# CURRENT EXECUTION OVERRIDE — V127 (2026-11-11)

## V8 current state — 2026-11-11

V7 failed closed in `STAGED_VALIDATION` before transaction. Its installer imported `QT_VERSION_STR` from `PySide6.QtCore`; the canonical PySide6 runtime does not export that symbol. This is an installer probe defect, not evidence that PySide6, Qt, QImage or QPainter is missing. The preceding imports of `PySide6.__version__` succeeded. `journal=[]`; `rollback=NOT_NEEDED`; no checkout write occurred.

V8 changes the probe to `from PySide6.QtCore import qVersion` and records `qVersion()` as the Qt runtime version. It requires Qt 6.x, alongside Python 3.13.x, existing PySide6 6.8–6.x, non-null RGB888 QImage and active QPainter. The official Qt for Python API lists `qVersion()` as a QtCore function. V8 does not install, upgrade or uninstall packages, invoke pip, edit requirements, or mutate the shared Python environment.

The consumer, its 35 Qt tests and the E1 service replacement are byte-identical to V7. No functional test result is inferred from the failed V7 runtime probe. V8 must still pass Windows PowerShell 5.1 AST, inventory/pins/destinations/staging, runtime probe, `py_compile` 3/3, all 35 Qt tests and immediate pre-transaction checks before any write. Do not repeat accepted A.3, binder V2, Godot V3, Loop22 or historical Drill authoring.

Governance remains unchanged: C11-C frozen manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; renderer OFF; dispatch/media/audio OFF; `release_authority=NONE`; operator manages commits; Git checks skipped.

---


## Latest result — Consumer V6 failed closed before transaction

- Windows V6 run: `E4C_DRILL_VISUAL_PIXEL_CONSUMER_V6_20261111T004628_177cd6f5`; evidence `E4C_DRILL_VISUAL_PIXEL_CONSUMER_V6_20261111T004628_177cd6f5.zip`.
- ZIP SHA, rollback implementation, PowerShell 5.1 AST, staging-root contract, 23-member inventory, 18 typed operations, 13 support pins, 10 design/font pins, exact operator decisions, 18 destination states and source staging all PASS.
- Staged validation stopped only at the exact style-guide anchor check: V15 contained the policy semantically (`reuse existing PySide6`, no Pillow/RAQM, no pip, no environment mutation) but omitted the required literal `No new Python dependency`. Its lower historical V14 section still stated the abandoned Pillow pin/provisioning instructions, creating a contradictory guide.
- `INSTALL_FAILURE.json` confirms `stage=STAGED_VALIDATION`, `journal=[]`, `rollback_status=NOT_NEEDED`, `renderer=OFF`, `media_created=false`, `release_authority=NONE`. No checkout transaction or consumer installation occurred.

## Current correction — Consumer V7 candidate

- V7 retains the V6 PySide6 Qt consumer, test module and E1 service postimage unchanged. It does not introduce Pillow, PIL, RAQM, another Python package, requirements/lock files, pip calls or global environment changes.
- V7 advances the runner guide to V16. It states the exact required `No new Python dependency` rule, explicitly retires the former V14/V5 Pillow guidance as historical/superseded, and keeps the rollback, PowerShell, staging and source-authority rules.
- The V7 installer references guide V16 and the V7 incident register; the 18-operation transaction shape remains one exact E1 service REPLACE plus 17 D-owned ADDs. All pins and exact approvals remain unchanged.
- V7 is NOT installed or Windows-qualified. Require AST, package/pin/destination/stage gates, existing PySide6 Qt offscreen probe, `py_compile` 3/3, rewritten Qt suite 35/35 and immediate pre-transaction rechecks before any write.
- V5's Pillow installation instruction was erroneous. Cleanup status is not established by the V6 failure evidence; V7 itself neither needs nor changes Pillow. Do not install or mutate any Python dependency for this phase.

## Accepted gates and immutable governance

A.3 Drill design-contract V5 remains CLOSED/PASS (receipt `d39eec2b3c1d969a3cb0d4e6aaa14b87aadcba74e42e58d283e00ea50768e881`). E4C binder V2, Godot console V3, E4B Loop22 and historical Drill authoring remain accepted; do not repeat absent source drift. C11-C frozen manifest remains 796,318 bytes / SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. Renderer OFF; dispatch/media/audio OFF; `release_authority=NONE`; C11-C remains sole production authority until E8.

## Forward path

After V7 installation PASS, review receipt and 18 postimages; then verify live Qt Producer frames and GUI/CLI parity across 20 selectors, font shaping/glyph coverage, overflow/clipping/contrast, native phase ownership and approved timebase. Only after those gates proceed to separately authorized `FAMILY_MUSIC_V4` A/V with independent seeds, FFmpeg/FFprobe and human review. Continue E4C closure → E5 → E6 Smoke18 → E7 Matrix101 (99 provisional; CH_008/009 held) → E8 independent historical regression, freeze and separate explicit cutover.

---

# CURRENT EXECUTION OVERRIDE — V126 (2026-11-11)

## Latest authoritative override — reject global Pillow; use existing Qt dependency

- The user correctly rejected installing packages into the shared Producer environment. The assistant's prior V5 instruction to install Pillow globally was an error. The `pip install Pillow==12.3.0` command succeeded; the follow-up Python probe then failed at syntax parsing because nested quotes were stripped by PowerShell. This was not a Pillow/RAQM diagnostic. Remove only the accidentally added Pillow package using the exact canonical Python 3.13 interpreter; confirm `importlib.util.find_spec('PIL')` returns `None`. Do not uninstall or modify PySide6.
- V5 is superseded and must not be installed. V6 removes Pillow/RAQM entirely and changes the D-owned consumer and its 35 tests to PySide6 Qt (`QImage`, `QPainter`, `QFontDatabase`, `QFontMetricsF`, `QRawFont`), reusing the dependency already declared by the Producer. No pip, no new requirement, no `requirements.txt` modification and no global environment mutation.
- This is a real rendering-backend change: V4/Pillow 35/35 evidence does not transfer. V6 requires Windows `PySide6` runtime probe, `py_compile` 3/3 and all 35 rewritten Qt tests before transaction. Test subprocess uses `QT_QPA_PLATFORM=offscreen` only and restores the prior process environment value.
- A.3 V5 remains CLOSED/PASS; binder V2, Godot console V3, E4B Loop22 and historical Drill authoring remain accepted. Do not rerun absent source drift.
- V1/V2/V4 failed closed pre-transaction; V3 was superseded before Windows; V5 must not be installed. No consumer transaction has occurred. Current candidate is V6, unqualified on Windows. Renderer OFF; dispatch/media/audio false; release authority NONE.

# CURRENT EXECUTION OVERRIDE

## Latest authoritative override — 2026-11-11 — Consumer V5 runtime prerequisite

- The three-run evidence archive `e4c_drill_visual_pixel_consumer.zip` confirms V1 failed in `PACKAGE_PREFLIGHT` (guide V12 omitted), V2 failed in `STAGED_VALIDATION` (literal guide anchor absent), and V4 failed in `STAGED_VALIDATION` at the Python dependency probe. V3 was superseded before Windows execution. All failed attempts have empty transaction journals, `rollback=NOT_NEEDED`, renderer OFF, `media_created=false`, and `release_authority=NONE`.
- V4 passed ZIP SHA, PowerShell 5.1 AST, rollback implementation audit, 23-member inventory, 18 operation inventory, support/design pins, exact operator-decision checks, 18 destination states, short staging, source roots and staged document dependencies. Its Python stderr is definitive: `ModuleNotFoundError: No module named 'PIL'`.
- The selected interpreter is the established project Python `C:\Users\vinxe\AppData\Local\Programs\Python\Python313\python.exe`, Python 3.13.14. Historical V121 D99 and E4C binder process receipts confirm this exact executable path/version. The interpreter is valid but Pillow is not installed; the probe never reached RAQM.
- V121 `c11c-suite/requirements.txt` and `c11c-suite/c11c-producer/requirements.txt` declare PySide6 only. Do not mutate protected/shared C11-C requirements. V5 introduces the D-owned `tools/c11d/d9/requirements-visual-consumer.txt` pin `Pillow==12.3.0`, matching the Pillow version used by the previously passing isolated 35/35 stage.
- Python dependency installation is operator-managed and is NOT performed by the overlay installer. Install Pillow 12.3.0 into the same canonical Python 3.13 runtime used by the existing Producer, then verify `features.check_feature('raqm')` is true. This is a runtime prerequisite, not a C11-C source change.
- V5 accepts an explicit `-PythonExe` path and checks Python 3.13.x + exact Pillow 12.3.0 + RAQM before any repository write. Consumer/service/test source bytes remain unchanged from V4. The 35 tests are not repeated absent consumer source drift; V5 still requires their staged Windows run before transaction.
- Current status: V1/V2/V4 FAILED_CLOSED_PRE_TRANSACTION; V3 SUPERSEDED_BEFORE_WINDOWS; V5 package awaits operator-managed Pillow preparation and then Windows installer execution. No consumer transaction has occurred.

# C11-E Current Authority — V125 (2026-11-11)

## Active authority and frozen boundaries

## Current execution state — authoritative override (2026-11-10)

- A.3 Drill design-contract V5 is already installed and CLOSED/PASS in active Windows. Receipt `d39eec2b3c1d969a3cb0d4e6aaa14b87aadcba74e42e58d283e00ea50768e881`; 3 replacements +26 adds; staged changed-source suites 33+5+7+10 and py_compile 8/8. Do not repeat.
- E4C binder V2, Godot console V3, E4B Loop22 and historical Drill authoring remain accepted; do not repeat without relevant pin drift.
- Consumer V1 failed pre-transaction because guide V12 was omitted. Consumer V2 failed pre-transaction at the literal rollback-heading check; empty journal and `rollback=NOT_NEEDED`. Consumer V3 was superseded before any Windows attempt after faithful source-stage replay exposed missing `challenges/`, full `assets/`, and `docs/current/d/` roots.
- Consumer V4 was the last candidate and failed before transaction; Consumer V5 is current, not yet installed. It has 18 typed operations (one E1 service replacement +17 D-owned adds), 13 support pins and 10 design/font pins. Its staging tree includes and path-budget-checks all three missing roots as read-only inputs. Reconstructed full V121 stage passed Python 3.13.5 / Pillow 12.3.0 / RAQM, py_compile 3/3 and tests 35/35. This does not establish Windows PS5.1 AST or active-checkout acceptance.
- Next action: verify V4 ZIP sidecar, run its bundled installer on active Windows, and require AST, inventory, all pins, exact decision checks, 18 destination states, complete stage roots, Python/Pillow/RAQM, py_compile 3/3, tests 35/35 and immediate pre-transaction rechecks. No writes before every staged check passes. Then inspect receipt and all 18 postimages.
- C11-C remains production authority. No consumer transaction has occurred. Renderer OFF; dispatch/media false; `release_authority=NONE`.

The active Windows checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS` is authoritative. ZIPs/snapshots are read-only and are never extracted over it. Operator manages commits; Git/HEAD/status/branch checks are skipped. Source SHA-256 pins and the frozen C11-C manifest are mandatory.

C11-C 2.19.12 remains the only production authority. Frozen manifest: 796,318 bytes / `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. Preserve all protected mechanics, generators, core audio, binders, timelines, RNG, simulation truth and canonical definitions. No sixth suite module, second Producer, parallel binder or `c11d-control`.

## Accepted evidence — never repeat absent pin drift

- E4A Challenge: accepted within its recorded scope.
- E4B mapping, R1P 27/27, Loop22 projection 22/22, policy fingerprints and R1V ten-output pilot: accepted.
- E4B Loop22: CLOSED/operator-approved; 44/44 A/V, 22/22 A/B, 25/25 tests. Run `L22_191801_27ABF3`; bridge receipt `009c9c4f3dfda17fd3455b0a26a427bc5cd55e78b4437e265a5b7a0a9d291b32`; report `d8f7050f952b7248b24763abde20ce52bf812c3934738f14670a0a3dc0c72068`; evidence ZIP `5ab13d933b4c4535b9cf90d417ff51d7342c7673329203d72fceaeea8b127f4f`.
- Historical Drill authoring adapter: accepted 20/20 on 24 source pins.
- E4C dynamic binder V2: **active Windows PASS**. Run `DRILLV2_20261110T151200Z_626a7d5e`; 20/20 selectors, 20/20 independent repeats, 20/20 request manifests, 20/20 lineage, 67/67 source pins. Receipt `31f631c3c23c6c1d277d67f52dd887010ee51be869798ab8db3fbdec8658fa01`.
- E4C Godot console hotfix V3: installed PASS; receipt `526c7d360863af8fb53707c9c83162173f4c1f1eb349ee8d767fb97665167a31`; exact Godot 4.7.1 Mono console smoke PASS; preflight reuse receipt `9484a8fae7382d3e25159c347a6979514256009c5d2b7bbc8d7cbb2741b12672`.

## A.1/A.3/B.1/D.1 approval reconciliation

The exact operator record `docs/current/e/C11E_E4B_OPERATOR_POLICY_DECISION_RECORD_20261106_V1.json` (SHA `49efd5494f351f09d7597c4699e9c12e361b36884b6bfadacd822e6ff1480e04`) explicitly approves A.1, A.3, E4B Loop composition, B.1 and D.1 against their recorded exact proposal hashes. Scope is D-owned design/contract implementation only. B.1 approves preservation of delivery cadence/frame order/duration without resampling. D.1 approves only a technical delivery envelope; it does **not** authorize audio asset selection, generation, mixing, mastering, silence policy or loudness. No decision authorizes renderer input, dispatch, media or release.

A.3 proposal remains SHA `609a4d183aac07c2cbe1abaf41444160fdd137217faffbead3aef618320d57dc`. The approved A.3 source lineage points to the historical review manifest `2075da9c33c689861a68d3bd8fb19b7ed593c6e76010ab200880746aa6d1a470`. Active V109 source has that same preimage. The current D review manifest successor is exactly `5702092bc1c88e4b333dd30cc150f0d383cd2006121037b0198905c75a3af795`, produced by replacing only `/source_lineage/6/sha256` from old D9.8 model hash `50655c82521a353f1db6920f4d099cad92452ae369251f9fbde45cbaee4e8c53` to current D9.8 model hash `dabb458fc2215156ddb5ebea7e8ebec811098886ce2858733ba9fb13f6075ccb`. The byte length remains 8,591 and all approval booleans remain false.

**Important installer correction:** the first prepared A.3 overlay assumed the current manifest already had the `5702092…` postimage. That assumption did not match the V109 source (preimage `2075da…`). V2 corrects this by explicitly including the manifest as a third pinned replacement, preimage `2075da…` → postimage `5702092…`, and adds the exact historical bytes as an add-only archive. It no longer treats the desired postimage as an existing source pin. The bridge V2 records this transition honestly; it does not claim the current file was never changed.

The D9.8 model itself is not asserted byte- or semantically equivalent to its predecessor. D9.9 plan-only compatibility remains distinct from D4 executable compatibility.

## New Drill operator decisions — exact-hash approvals

The explicit operator message `APPROVED AS PROPOSAL` is recorded in `C11E_E4C_DRILL_COMPOSITION_OPERATOR_DECISION_RECORD_20261110_V1.json` (SHA-256 `eb95da188065b8ebcb2371e2a6bcff6762ce000a5ca74f8ea384ecec4ee58303`). Geometry SHA `b22f9eb6fce39f877e432ff5f0051ecf5ab8575ecb9f580fe5f158994222fc09` and timebase SHA `44ab3b0fa09a6f7d42cd8cf2f1122cada6cbffe16a7a6b53c2af5e88d5daddc8` are each marked `APPROVE_AS_PROPOSED`. This grants D-owned design/contract implementation and focused isolated visual/pixel tests only. Renderer input/activation, dispatch, media/audio creation, C11-C mutation and release remain unauthorized.

## E4C Drill source findings

Read-only C11-C source audit (8 exact C11-C pins / 12 checks) confirms `PRE_ROLL` 3s → `GAME` → `END_CTA` 3s → `DONE`. `VisualContentPlayer` passes a global frame index for PRE_ROLL and END_CTA but passes `_current_frame_index` (local GAME index) to the binder during GAME. Native `VisualDrillEndCTA` owns the source-frame header during END_CTA; `C11CVisualEditorialLayer` owns native header/footer. D must remain outside the contained native frame and must suppress D editorial during PRE_ROLL/END_CTA to avoid a duplicate CTA.

The Drill outer-band geometry is approved as proposed by exact hash `b22f9eb6fce39f877e432ff5f0051ecf5ab8575ecb9f580fe5f158994222fc09`: 720×1280 REVIEW_720, 192px top/bottom bands and a 504×896 uniformly contained source viewport at x=108,y=192; no crop/stretch/resampling. D editorial is visible only during GAME and suppressed in PRE_ROLL/END_CTA.

A separate timebase proposal now states the source-derived candidate formula `final_presentation_frame_index = pre_roll_frames + game_payload_frame_index`; at 30 fps, PRE_ROLL=90, GAME=630, END_CTA=90, total=810, and GAME frames map `[0,630)` → `[90,720)`. The D fields are proposed visible only during GAME and suppressed during PRE_ROLL/END_CTA. The timebase proposal is approved as proposed by exact hash `44ab3b0fa09a6f7d42cd8cf2f1122cada6cbffe16a7a6b53c2af5e88d5daddc8`. Both decisions are recorded independently in `C11E_E4C_DRILL_COMPOSITION_OPERATOR_DECISION_RECORD_20261110_V1.json`; the proposals remain immutable and their own status fields remain `PROPOSED_NOT_APPROVED_NOT_RENDERER_INPUT`.

## A.3/Drill staged validation — historical design record; V5 now closed

Reference-tree validation against V109-derived sources plus the three pinned replacement postimages passed: field-window/lineage 33/33 (the prior 31 plus explicit positive/negative manifest-replacement disclosure tests), phase ownership 5/5, Drill composition 7/7, timebase 10/10, and py_compile for eight Python modules. This is isolated reference-tree validation, **not** a Windows active-checkout result. V4 installer repeats only these changed-source tests in a short `%TEMP%` staging root (to avoid Windows MAX_PATH) before any write. The previous V2 attempt stopped during staging at a 269-character path; it reported `rollback=NOT_NEEDED` and performed no source or overlay-destination writes; the installer did create its run-specific evidence directory and failure JSON under `artifacts/tests`. V4 retains the short-stage strategy introduced by V3 and adds the StrictMode-safe payload-only operation scope. Accepted E4C 20×2 binder, E1 32/32, D9 preflights, Loop22 and historical authoring remain reused.

## E4C remaining gates

- A.3 source lineage pointer replacement + bridge: CLOSED/PASS_ACTIVE_WINDOWS by V5 receipt `d39eec2b3c1d969a3cb0d4e6aaa14b87aadcba74e42e58d283e00ea50768e881`; postimage is installed and verified.
- Drill phase ownership audit: PASS_READ_ONLY design evidence.
- Drill outer-band geometry/composition: APPROVED_AS_PROPOSED, D-owned design/contract scope only; exact record SHA is in the V4 docket.
- GAME→final-presentation timebase: APPROVED_AS_PROPOSED, D-owned design/contract scope only; exact record SHA is in the V4 docket.
- D-owned visual consumer, typography/font shaping, clipping/overflow/contrast/pixel tests: now authorized for implementation and focused isolated testing at the existing D boundary; not renderer-native input and not media creation.
- Native Drill A/V: not qualified; preserve `FAMILY_MUSIC_V4`, silent C11-C capture, independent gameplay/music seeds, FFmpeg/FFprobe and human playback review. D.1 does not authorize audio creation.
- Existing Producer Qt GUI runtime observation: OPEN.

## Forward roadmap

Complete approved D-owned visual consumer and pixel proof → native family A/V/human/GUI acceptance → E5 cross-family determinism, seed isolation and profile/binder non-leakage plus GUI/CLI parity → E6 Smoke18 (six full A/V scenarios per family) → E7 Matrix101 (54 Challenge + 27 Loop + 20 Drill; CH_008/009 held; 99 provisional) → E8 full historical C-to-E regression map, independent acceptance, immutable freeze and separate explicit promotion/cutover.

## Permanent controls

PowerShell 5.1; Python 3.13; Godot 4.7.1 Mono console. `GIT_CHECKS=SKIPPED; COMMITS=OPERATOR_MANAGED; SOURCE_FILE_PINS=ENFORCED`. Installers verify complete package inventory, canonical frozen SHA, every pin/preimage/postimage, AST, staged tests, separate stdout/stderr, exit codes, non-null backups and rollback. Never repeat accepted evidence without drift; stop at the first failure. Renderer OFF; dispatch/media false; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/16 BLOCKED; D9.17 NO-GO; D10 blocked; `release_authority=NONE`.


## Historical A.3 / Drill overlay installation recovery — V2–V5 (closed by V5)

V2 stopped at `STAGED_VALIDATION` because a source path was 269 characters; rollback was not needed. V3 proved the short `%TEMP%` stage (55-character root), PowerShell 5.1 AST, package inventory (29 payload files), 13 supporting source pins, 29 destination states and both exact-hash operator approvals. It then stopped in `STAGED_VALIDATION` because `Set-StrictMode -Version 2.0` rejects reading a missing `.mode` property from non-payload rows in `PACKAGE_CONTENTS_MANIFEST.json` (README, correction record and package manifest). No payload transaction began; rollback remained `NOT_NEEDED`. The run-specific evidence directory and failure JSON were written under `artifacts/tests`, but no repository source or overlay destination was changed.

V4 fixes the root cause by using `$operationEntries`—the already validated `payload/` subset—for both staged replacement-postimage verification and receipt replacement enumeration. It validates required operation metadata on those 29 rows and keeps the three package metadata rows outside all mode-based operations. It retains the 55-character `%TEMP%` staging design and 240-character guard. V4 must pass PowerShell 5.1 AST, complete inventory/member hashes, 13 pins, 3 replacement preimages / 26 add-only destination states, staged 8-module `py_compile`, tests `33+5+7+10`, and pre-transaction rechecks before writes.

Both Drill proposals remain approved under exact operator record SHA `eb95da188065b8ebcb2371e2a6bcff6762ce000a5ca74f8ea384ecec4ee58303`, but only for D-owned design/contract implementation and isolated visual/pixel tests. No renderer input/activation, dispatch, media/audio creation, C11-C mutation or release authority.


## Consumer installer chronology and current handoff

Consumer V1 ZIP SHA `dfae50d5bc4d35bdcc83cfa2626222bde10559f17f9a002642692278c8c72577`: preflight failed because required guide V12 was not packaged. No transaction.

Consumer V2 ZIP SHA `6297246ceeeb616e6e66ae154cfcf37258296e6413910d74e996a831c3a0e4bb`: package, decisions, pins, 18 destinations and short stage passed; staged validation failed because the literal `hash-guarded rollback` heading was missing. Empty journal; `rollback=NOT_NEEDED`; no transaction.

Consumer V3: added explicit rollback policy and code-structure checks, but local source-stage replay against V121 showed incomplete test inputs (`challenges/`, full `assets/`, `docs/current/d/`). It was superseded before Windows use; no transaction.

Consumer V4: current candidate. It includes style guide V13, docket V7, phase audit V2 and incident register V4 checks; includes the complete source-stage roots; verifies the rollback implementation itself (expected postimage, exact preimage backup, unknown-state refusal and atomic restore). E1 successor SHA `e5dbf9baa72d4c066ff8ba24006df954700d72a5b0f11f9f88aec653e84dce87`; consumer SHA `e1e78a00d7d9384f7b99e9da16c7388be59a239bbcd8d1d9de44a881b68d3a03`; tests SHA `15c417555382ff397991e4402dc313708ab17d29df78d4cbcd97d96b4a31609a`. All three bytes are unchanged since V2.

Faithful reconstructed V121 stage including `challenges/`, full `assets/`, `docs/current/d/`, and prior roots passed py_compile 3/3 and tests 35/35 with Python 3.13.5 / Pillow 12.3.0 / RAQM. Synthetic samples are not real C11-C frames. V4 active Windows execution, PS5.1 AST, runtime, logs and install receipt remain pending. No consumer V1–V4 transaction has occurred.

After V4 install PASS: inspect exact receipt and service/add postimages; review only the existing E1 shared service seam; preserve GUI/CLI parity; observe the existing Qt Producer with real C11-C frames for all 20 selectors; qualify font/layout/phase/pixel behavior. Then, only under separate applicable audio authorization, qualify native family A/V using silent C11-C capture, existing `FAMILY_MUSIC_V4`, separate gameplay/music seeds, FFmpeg/FFprobe and human review.

Roadmap: close E4C → E5 determinism/seed isolation/profile and binder non-leakage/GUI-CLI parity → E6 Smoke18 (six full A/V cases per family) → E7 Matrix101 (54 Challenge +27 Loop +20 Drill target; CH_008/009 held, 99 provisional) → E8 row-by-row historical C-to-E regression, independent acceptance, immutable freeze and separate explicit promotion/cutover.


## V1.5 installer failure / V1.6 recovery — 2026-11-12
V1.5 passed source pins 19/19 and PS AST 2/2 but timed out in staged Python tests with `PYTHON_TIMEOUT: ;`. Diagnostic journal was empty; no transaction writes. Root cause assessment and correction are recorded in `docs/history/c11e/C11E_E4C_CLI_SMOKE_INSTALLER_TIMEOUT_ARGS_BINDING_20261112_V1.md`. V1.6 is an ADD_ONLY installer correction; it does not alter the accepted GUI A/V pilot or the D execution adapter. CLI A/V smoke remains OPEN. Do not infer its PASS from installer tests.


## 2026-11-12 V138 authoritative status

CLI smoke `E4C-CLI-SMOKE-20261112T091253Z-5a2e96b8` is technically accepted and preserved, but its V1 composition is rejected. V2 fixes the consumer at the D-owned composition boundary only. The social body is a native 1:1 crop from `get_social_regions().body_rect`; PRE_ROLL and END_CTA are full native passthrough. This changes neither E1 nor C11-C.

The previous V1.7 install failed before transaction; the immediate Windows task is install `C11E_E4C_DRILL_VISUAL_COMPOSITION_V2_REQUALIFICATION_V1_8_20261112.zip`, require 21/21 source pins, PS AST 2/2, Python/PySide6 runtime, py_compile 3/3, 18/18 Qt tests, one exact replacement preimage, 22 add-only states and transaction receipt. Then run `RUN_C11E_E4C_DRILL_AV_EXISTING_MEDIA_V2_REQUALIFICATION.ps1` against preserved CLI smoke evidence. Require V2 technical PASS and operator visual/audio acceptance. Do not repeat GUI A/V, native capture, Godot, music generation, Binder, historical 100/100 V1 pixel suite or any accepted baseline.

The prior visual acceptance of consumer V1 is superseded for the V2 spatial contract. The original GUI A/V run remains historical technical/audio evidence; it is not rerun. The corrected V2 output from the existing CLI native MP4/WAVs is the selector's new visual acceptance point. V2 matrix status is 0/20 until operator accepts that output; then tracking/tier-1 becomes 1/20 and the remaining 19 selectors follow.


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

## Autoridad actualizada R5 — 14/11/2026

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

### Current gate state — R6

R5 install + independent audit PASS. R5 review recovery was correctly fail-closed on stored V2 plan/schema mismatch; R3 visuals also failed operator title-style review. R6 is the combined fix: proper V2 output-plan semantics and D family-title bridge from PRE_ROLL through GAME. No prior R3/R5 output bundle is counted as accepted.

## R6.1 packaging correction — 2026-11-14

R6 original install was fail-closed before transaction. The accepted R2 transaction journal proves that `tests/test_c11e_e4c_drill_visual_composition_consumer.py` was replaced in run `C11E_E4C_HISTORICAL_REQUAL_V2_3_R2_20261113T072125Z_351b67d0`: preimage `62327e32ed4c15b497efb4a93fecc1d484cebff0b79beaa7ced5099905ffb2bf`, postimage `42e4cb8097ea9536dca63627e82c240ce0bb5b73baf03152269a35ac219a68eb`. R6.1 correctly uses the latter as the active REPLACE preimage. The other four R6 replacement preimages are unchanged and trace to accepted R2/R4/R5 transaction journal postimages. R6.1 adds five explicit `preimage_lineage` records to the package manifest; installer and independent auditor both require exact one-to-one lineage bindings. This is a package-manifest correction only: no protected C11-C source, frozen manifest, E1 service, canonical decision record or gameplay/media artifact is modified by this correction.

R6.1 is a new add-only package delivery identity. The previous R6 package is superseded and must not be installed. The R6 functional payload (family-title bridge, V2 plan-schema correction and R6 runner) is unchanged. On installation, the operator must capture the R6.1 `RUN_ID`, independently audit its receipt and journal, then run the new R6 family-title bridge qualification once. The old R3 outputs remain historical evidence only and must not be accepted as the new editorial result.

## R6.2 test-oracle and execution correction — 2026-11-14

R6.1 correctly passed its package/source-pin/preimage-lineage preflight, then failed closed before transaction at consumer test 10. The approved family-title gold is RGB `(235,215,161)`, while the test required all three channels to exceed 180; its blue channel is 161, so the predicate could not count even correctly rendered title pixels. R6.2 corrects the test to use a chromatic gold threshold `(180,160,110)` for the title and retains near-white thresholds for subtitle/CTA. The compositor, approved typography/color, geometry, native body and timebase are unchanged. R6.1 produced no transaction writes or R6.1 receipt. User-side audit/runner lines that later read a stale R5 run ID or missing runner are invalid and must not be cited as R6.1 evidence. The R6.2 package includes a fail-closed one-shot orchestration script: unique temporary extraction, exact package hash/inventory, install receipt identity, audit receipt identity, then runner only after both prior phases pass. All current documents and continuity prompts are included in this same ZIP. R6.2 is the sole active candidate; E4C remains 0/20 accepted pending the new seven-frame/three-video operator review.

## Latest operator review and active corrective authority — R6.2 → R6.3 (2026-11-14)

R6.2 sequence PASS: installer and independent audit PASS; technical requalification completed 810/810 frames with 7/7 review frames. Output: `E4C-CLI-COMPOSITION-V2-R6-TITLE-BRIDGE-20261114T143615Z-fba77da2`. Operator visual review: content/layout PASS and family-title bridge PASS; subtitle/CTA style FAIL because role font, alignment, size and palette colors did not inherit C11C default editorial role rules. Do not mark selector accepted or close E4C.

R6.3 corrects only D-owned subtitle/CTA role projection. Subtitle: C11C HEADER role, Inter-Bold 22px delivery fit, horizontal CENTER, vertical BOTTOM, selected-family `text_secondary` color, black outline width1 alpha0.72. CTA: C11C FOOTER role, NotoSansMono-Regular 16px, horizontal CENTER, vertical TOP, selected-family `text_data` color, black outline width1 alpha0.78. The active C11C palette is resolved from unmodified native GAME body background with unique-match fail-closed policy. Style authority source pins are `C11CVisualEditorialLayer.gd` `f8f718c067a4d7a088cc16f244cc40209e7183bec93e44d8cb66eb6dd404cf7d`, `C11CVisualTypography.gd` `9ee823a28cef721a26f66436b5b168d92f5b9d1597ed6e4e3f518debb0910633`, and `C11CDrillPaletteBank.gd` `757786a6bcc4e819fd43c1c41ea29e8b00dbe3b3f2f5c72fa19776a368b3c8ec`. These three C11C files are read-only. Family-title R6 style is unchanged.

R6.3 install/audit/requalification remains pending operator execution. On technical PASS, operator must inspect all seven frames and three A/B/C MP4s and listen to the existing A/B/C tracks. Only explicit visual+audio acceptance promotes `tracking/tier-1` from 0/20 to 1/20. Other 19 Drill selectors remain outstanding. E4C close remains 20/20. Roadmap stays E5 → Smoke18 → Matrix101 → E8.

All frozen governance persists: C11-C 2.19.12 is production authority; frozen manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; E1 PREPARE_ONLY; family adapter NOT_CONNECTED_E1; renderer/dispatch/media OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; release_authority NONE; Git checks skipped and commits operator-managed.

## R6.3 package pin-alignment correction — 2026-11-14

The initial R6.3 candidate (`74070cafbc0035de82ec6668472ad230f1bab0ce6565e83e1388cf99a50bc865`) declared an expected SHA-256 of `f22d246b4b3f768f0daf33f2adbbed0073d828595c85678a39d6ef37642d12ec` for `core/presentation/C11CVisualEditorialLayer.gd`. That value conflicts with the exact C11-C 2.19.12 frozen manifest already pinned by this project (`e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`): the frozen manifest records `f8f718c067a4d7a088cc16f244cc40209e7183bec93e44d8cb66eb6dd404cf7d` for the same source file, and the supplied R6.2 project snapshot contains that exact file hash. The candidate has been corrected to the frozen value in the D-owned consumer contract, amendment JSON, package source-pin manifest and documentation. No C11-C source, frozen manifest, E1 service or protected runtime file has been changed. Use only `C11E_E4C_DRILL_HISTORICAL_REQUALIFIER_V2_3_R6_3A_PIN_ALIGNED_20261114.zip`; the initial R6.3 ZIP is superseded and must not be installed. Windows installation, independent audit, 32 focused consumer tests and fresh R6.3 technical requalification remain pending. `tracking/tier-1` remains 0/20 until subsequent human visual AND audio acceptance.

## R6.3A current disposition — 2026-11-14

R6.3A supersedes all earlier R6.3 ZIPs and hand-written preflight commands. The initial candidate's C11C editorial-layer pin was wrong; the pin-aligned rebuild had stale package-file hashes/byte counts and an external/embedded driver mismatch; and the first radius-cardinality resolver rejected the known R6 `tracking/tier-1` sample because five tracking backgrounds fell within radius 8. R6.3A aligns the source pin to the immutable C11-C frozen manifest, recomputes inventory hashes from final bytes, ships an external orchestrator byte-identical to the embedded copy, and ranks the 24 palettes by maximum per-channel distance. It accepts only best distance <=8 with runner-up margin >=1; ties fail closed. The observed R6 sample `(1,15,12)` resolves to `AQUAMARINE_SUN` (best2, runner-up6, margin4). Tests cover that sample, tie rejection and all 96 palette rows.

The accepted native identity receipt pair records 1,112,459 bytes and SHA-256 `d10950bca9358de4ffe8a9f4f24c8c35cdb37e25050775a9220a4d15ffb45338`. The earlier manually typed 68-character digest was invalid and is withdrawn. R6.3A reads media identities from accepted receipts and verifies actual MP4/WAV files in the active checkout; no separate manual media preflight is to be run.

Windows PowerShell AST, PySide6/Qt offscreen 32-test suite, File.Replace forward/rollback, install, independent audit and new technical requalification remain pending. Use only the R6.3A one-shot orchestrator; it stops on first failure. Do not repeat accepted R6.2 recovery tests 18/18, GUI/CLI smoke, native capture, Godot or music generation. Human E4C acceptance remains `tracking/tier-1=0/20` until seven-frame visual and A/B/C audio approval. Next: E4C 20/20 → E5 → E6 Smoke18 → E7 Matrix101 (CH_008/009 held; 99 provisional) → E8.

Governance: C11-C 2.19.12 frozen manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; E1 PREPARE_ONLY; family adapter NOT_CONNECTED_E1; production dispatch false; release authority NONE; GIT_CHECKS=SKIPPED; COMMITS=OPERATOR_MANAGED.

---

## Authority update — R6.3A first-install recovery — 2026-11-14

The operator-provided evidence archive `e4b_loop_policy_readliness_AND_e4c_v2_installer.zip` was inspected. Scope was restricted to the two R6.3A execution IDs dated 2026-11-14; earlier historical test folders were not requalified.

**The first R6.3A installation transaction succeeded.** Exact run ID: `C11E_E4C_V2_3_R6_3A_20261114T163406Z_fc8436fa`. Its receipt records `PASS_REPLACE_AND_ADD_ONLY_INSTALL`, package ZIP SHA-256 `47d5a30c315365eb7a31e37fc4bc1c2ff6ca0a297d1e57eccf89c3f5a024b96e`, 25/25 source pins, 3 REPLACE +15 ADD, 18/18 postimages, 3/3 backups, PowerShell AST 3/3, Python compile 3/3, consumer tests 32/32, and unchanged frozen C11-C governance. Its journal records all three REPLACE operations as `REPLACED_POSTIMAGE_VERIFIED` and gives three non-null backup paths. Independent SHA recomputation of the three backup files matched their respective exact preimage hashes (3/3).

The first outer orchestrator failed after launching the installer because it called `[IO.File]::ReadAllText` on redirected `INSTALL.stdout.log` while the child process still held the file open. This is an orchestration log-sharing defect, not an installer transaction failure. The child installer completed and persisted the successful receipt/journal/backups before the outer wrapper stopped.

The operator then ran a second one-shot invocation: `C11E_E4C_V2_3_R6_3A_20261114T163827Z_47eab402`. It saw all three replacement destinations already equal to package postimages and correctly recorded `SKIP_IDENTICAL_POSTIMAGE` with `backup_path=null`. The receipt nevertheless reported `backups=3/3 PASS`, which is an installer accounting defect. The independent auditor correctly rejected this second run because its own journal contains no replacement backups. **Do not audit this second run and do not rerun the installer.** The second run did not undo or replace the first transaction's backup evidence.

The correct recovery is to run the independent auditor against the first transaction ID `...163406Z_fc8436fa` and the original package ZIP SHA `47d5a30c...`, then run the already-installed D-only R6.3A role-style requalification runner exactly once. The recovery utility in this kit performs those operations in that order; it does not reinstall, recapture native media, regenerate music, repeat GUI/CLI smoke, invoke Godot, or mutate C11-C/E1.

The initial R6.3A human selector remains `tracking/tier-1 = 0/20`. After technical requalification, review all seven frames and A/B/C outputs and obtain explicit visual AND audio acceptance before recording 1/20. E4C closes only at 20/20.

Governance remains unchanged: C11-C 2.19.12 sole production authority; frozen manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; E1 `PREPARE_ONLY`; family adapter `NOT_CONNECTED_E1`; no production dispatch; `release_authority=NONE`; `GIT_CHECKS=SKIPPED`; `COMMITS=OPERATOR_MANAGED`.


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


## 2026-11-15 — V3 installation audited; V4 runner reconciliation is the active next gate

V3 installation run `C11E_E4C_TRACKING_PREROLL_FIX_V3_INSTALL_20261115T073428Z_4d3049a3` installed 5 pinned replacements + 14 add-only documents, with 30/30 source pins pre/post, atomic-I/O 6/6, Python compile/focused tests PASS, and frozen C11-C manifest unchanged. The evidence ZIP's V3 journal and backup files have been independently hash-checked.

Audit found the installed wrapper still pinned an obsolete coordinator SHA (`a032f...`) instead of the installed coordinator SHA `9b868c33a705257c8343c58033e2afb44b502992dbd04d73d72a1050cdde2820`; it also required V25/V26 files not added by V3. The coordinator itself still requested V26 although V3 installed V27. Do not launch the V3 wrapper. V4 will replace only the existing coordinator, its test, and wrapper; add the V28 style guide/current docs/prompts; run static parity tests; and launch a fresh PREPARE_ONLY via the corrected wrapper.

No BatchId is yet consumed by V4 PREPARE_ONLY. Actual batch execution remains fail-closed and separate from preparation. E4C accepted coverage remains 1/20; tracking tiers 2–5 pending; other 15 selectors pending. `PRODUCTION_DISPATCH=FALSE`, `RELEASE_AUTHORITY=NONE`, no Git checks, commits operator-managed.

## Pursuit recovery V4 — authoritative installer correction (2026-11-15)

The V3 recovery package was not executed: Windows PowerShell 5.1 rejected its script at parse time because the audit-receipt hashtable declared `source_pins_post` twice (the summary key and detailed array). The parser error occurred before installer execution, so V3 made no checkout mutations. Do not run V3.

V4 is the only recovery candidate. It retains the 19/19 ADD_ONLY destinations committed by V2, audits the exact V2 run `C11E_E4C_PURSUIT_BATCH_OVERLAY_V2_20261115T130255Z_b5f15417`, corrects the duplicate key to `source_pin_results_post`, and adds an operator-side `Parser.ParseFile` gate before invoking the installer. Its transaction is bounded to two SHA-pinned replacements (pursuit runner and runner-contract test) plus 15 ADD_ONLY documentation/prompt destinations. It must pass 34/34 source pins, frozen C11-C manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` / 796318 bytes, Windows PowerShell 5.1 AST, Python 3.13 tests and atomic I/O 6/6 before mutation.

V4's default embedded pursuit action is PREPARE_ONLY. Do not pass `-Execute`. Independently audit the V4 receipt, journal, two backups, 17 postimages, 34 source pins and the resulting five-selector BatchId before authorizing a later execution. Preserve all failed evidence. C11-C/E1/dispatch boundaries remain unchanged.

## Pursuit batch V5 authority boundary — 2026-11-15

V5 is a test/qualification harness correction only. It replaces four SHA-pinned harness files and adds versioned documentation/prompts. It does not modify C11-C, the frozen manifest, the canonical Pursuit definition, family difficulty profile, execution service, D visual composition consumer, media pipeline, music generator, GUI or CLI service. The source definition SHA remains `dfe2bce9913df8ebe4f92d06eec5d22736338214e71b497dde3562a6927600bc`; C11-C frozen manifest SHA remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

The Pursuit contract is derived from the pinned canonical definition: 30 fps, 510 gameplay frames / 17.0 seconds, plus 90-frame PRE_ROLL and END_CTA = 690 total frames / 23.0 seconds. Tracking's 810-frame / 27-second example remains scoped to Tracking and is not a universal Drill constant. V5 audits the consumed V4 T1 output without re-render and limits a new execution to T2–T5. E1 remains PREPARE_ONLY; family adapter NOT_CONNECTED_E1; renderer/production dispatch remain unauthorized; `release_authority=NONE`.

## Installer authority — V5.3 (2026-11-15)

V5 and V5.1 installer packages are superseded and must not be run. V5.1 failed before `TRANSACTION_STARTED`; the log shows a missing staging path for `C11E_AtomicFileOps.ps1`. The checkout payload was not changed by that failure. V5.3 is built but remains NOT INSTALLED until the operator runs its installer and obtains a complete receipt. It uses the same four V4-pinned harness replacements and sixteen add-only documents, while correcting package-relative support paths, dot-sourcing and validating the atomic helper, and exercising the installer's JSON writer before transaction. The PowerShell 5.1 parent AST must pass before `-File` invocation.

The selector-specific Pursuit timeline remains 690 frames / 23 seconds / 90+510+90. Existing V4 T1 is audited and reused without render; a new batch may execute T2–T5 only after a separate operator decision. C11-C frozen manifest remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; E1 PREPARE_ONLY; production dispatch false; release authority NONE.

## V5.3 installer deep-hardening addendum — 2026-11-15

The first complete static review found that V5.3 still set `transaction_started=true` before making its four replacement backups. This was corrected: backup preparation/journaling now runs with `transaction_started=false`; every backup is hash/byte verified and persisted; all 20 targets are rechecked immediately before the transaction boundary; and each individual target is rechecked just before its atomic operation. The installer also scans ZIP member names and duplicate paths before extraction. The staged canonical fixture is copied to both `tests/fixtures` and `definitions`, matching the test imports and canonical path consumers. The staged suite now contains 37 Python tests. The receipt and failure record carry backup records.

Status is **BUILT, NOT INSTALLED**. The Linux build environment cannot execute Windows PowerShell 5.1, so native AST/atomic-I/O checks remain mandatory operator gates. No renderer or media generation is part of installation. V5/V5.1 remain invalid.

V5.3 refuerza además el límite transaccional: exige que existan previamente todos los directorios padre; comprueba el binding exacto de cada destino REPLACE con su payload; usa creación atómica exclusiva para ADD (no sobrescribe un destino concurrente); y limita el rollback a operaciones confirmadas o a la operación REPLACE en vuelo. Los temporales en vuelo se limpian en fallo. La suite Python se exige exactamente en 37/37 y la prueba atómica amplía a 7/7 con colisión ADD.
