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
