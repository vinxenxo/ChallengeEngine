## V9 current state — 2026-11-11

Consumer V8 stopped in `STAGED_VALIDATION` before any repository transaction. The exact cause was a StrictMode ordering bug in the installer: `$testSource` was inspected for the removed `QT_VERSION_STR` token before it was assigned from the staged test file. The run's journal is empty and `rollback=NOT_NEEDED`; no rollback or repository recovery is required. V9 fixes this by loading both `$consumerSource` and `$testSource` first, validating both are non-empty, and only then inspecting their contents. This is an installer-only correction. The Qt consumer, 35-test module and E1 service replacement bytes are unchanged from V8.

V9 also corrects the run ID and receipt/failure schema identities to V9. It preserves the 18-operation scope (one exact-pinned E1 service REPLACE + 17 D-owned ADDs), all 13 support pins, 10 design/font pins, exact-hash operator decisions, frozen C11-C manifest and no-new-dependency policy. The installer uses the existing canonical Producer Python/PySide6 only; it must not invoke pip, install/uninstall packages, change requirements or mutate shared environment dependencies.

V9 is a candidate only. Windows PowerShell 5.1 AST, Qt runtime probe, py_compile 3/3, tests 35/35, immediate pre-transaction rechecks and successful receipt are still pending. No consumer V1–V8 transaction has been recorded. Stop at first failure; do not repeat A.3 V5, binder V2, Godot V3, Loop22 or historical authoring accepted gates.

Next step: verify V9 ZIP SHA and sidecar, then run the V9 installer with the existing canonical `-PythonExe`. Require the same 18 destination states and all pre-write gates. After PASS, inspect `INSTALL_RECEIPT.json`, its SHA and all 18 postimages before any E1 integration review. C11-C remains sole production authority; renderer OFF; dispatch/media/audio OFF; `release_authority=NONE`.

---

# CURRENT E4C EXECUTION OVERRIDE — V15 (2026-11-11)

## V8 current state — 2026-11-11

V7 failed closed in `STAGED_VALIDATION` before transaction. Its installer imported `QT_VERSION_STR` from `PySide6.QtCore`; the canonical PySide6 runtime does not export that symbol. This is an installer probe defect, not evidence that PySide6, Qt, QImage or QPainter is missing. The preceding imports of `PySide6.__version__` succeeded. `journal=[]`; `rollback=NOT_NEEDED`; no checkout write occurred.

V8 changes the probe to `from PySide6.QtCore import qVersion` and records `qVersion()` as the Qt runtime version. It requires Qt 6.x, alongside Python 3.13.x, existing PySide6 6.8–6.x, non-null RGB888 QImage and active QPainter. The official Qt for Python API lists `qVersion()` as a QtCore function. V8 does not install, upgrade or uninstall packages, invoke pip, edit requirements, or mutate the shared Python environment.

The consumer, its 35 Qt tests and the E1 service replacement are byte-identical to V7. No functional test result is inferred from the failed V7 runtime probe. V8 must still pass Windows PowerShell 5.1 AST, inventory/pins/destinations/staging, runtime probe, `py_compile` 3/3, all 35 Qt tests and immediate pre-transaction checks before any write. Do not repeat accepted A.3, binder V2, Godot V3, Loop22 or historical Drill authoring.

Governance remains unchanged: C11-C frozen manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; renderer OFF; dispatch/media/audio OFF; `release_authority=NONE`; operator manages commits; Git checks skipped.

### V8 Windows gate
V7 failed at runtime probe because `QT_VERSION_STR` is not exported by `PySide6.QtCore`. V8 uses documented `qVersion()` and also requires returned Qt version `6.x`. It makes no Python environment changes. Only after runtime PASS run `py_compile` 3/3 and the 35 Qt tests; all must pass before transaction. V7 did not reach these checks.

---


## V6 outcome and current V7 action

V6 passed ZIP SHA, rollback implementation, PowerShell 5.1 AST, inventory, operation typing, pins, exact decisions, destination states and complete staging. It failed in `STAGED_VALIDATION` on the guide text anchor `No new Python dependency`. The top of V15 guide had semantically equivalent no-Pillow/no-RAQM/no-pip/no-environment-mutation rules, but omitted that exact phrase; its inherited V14 section still prescribed Pillow, creating contradictory policy text. Evidence run `E4C_DRILL_VISUAL_PIXEL_CONSUMER_V6_20261111T004628_177cd6f5` confirms empty journal and `rollback=NOT_NEEDED`; no repository writes occurred.

V7 updates only installer identity/references and documentation. Runner guide V16 states `No new Python dependency` as an explicit binding rule and retires the V14/V5 Pillow path. Qt consumer, rewritten tests and E1 service bytes are unchanged from V6. No Pillow, PIL, RAQM, pip, dependency lock, new requirements file or shared Python environment mutation is permitted.

V7 Windows acceptance remains pending. Require exact SHA, PS 5.1 AST, 24/23 package inventory, 18 operations (1 REPLACE +17 ADD), 13 support pins, 10 design/font pins, exact decisions, 18 destination states, complete read-only staging, guide V16/docket V7/phase audit V2/incident V7, canonical Python 3.13 + existing PySide6/Qt offscreen probe, py_compile 3/3, 35/35 Qt tests, restored original `QT_QPA_PLATFORM` and immediate pre-transaction rechecks before any write. Review exact receipt and all 18 postimages.

## Boundaries

Do not repeat A.3 V5, binder V2, Godot V3, Loop22 or historical Drill authoring. Preserve C11-C and native Drill PRE_ROLL/GAME/END_CTA/DONE behavior, including native END_CTA/header/footer and family music. Do not activate renderer, dispatch, media, audio creation or release.

---

# CURRENT E4C EXECUTION OVERRIDE — V14 (2026-11-11)

- V4 passed package, pins, rollback audit and staging but failed Python runtime probe because `PIL` was absent. No transaction occurred.
- The assistant's V5 recommendation to install Pillow in the shared Producer Python was incorrect. The user's concern is accepted. Pillow was installed; the nested-quote verification failed at Python syntax, not at RAQM. Remove only the accidental Pillow addition and verify absence. Do not uninstall PySide6.
- V6 replaces the Pillow renderer with Qt using the Producer's existing PySide6. No new dependency, no `pip`, no new requirements file, no shared environment mutation, and no protected requirements edits.
- V6 is a true backend migration. Require Windows PS 5.1 AST, PySide6/Qt/QImage/QPainter offscreen probe, py_compile 3/3 and rewritten Qt tests 35/35 before any repository write. The installer sets `QT_QPA_PLATFORM=offscreen` only for child test processes and restores the original process value.
- Current consumer status: NOT INSTALLED. V1/V2/V4 failed closed before transaction; V3 superseded; V5 superseded and forbidden; V6 candidate pending Windows.

# CURRENT E4C EXECUTION OVERRIDE

## Latest authoritative override — 2026-11-11 — Consumer V5 runtime prerequisite

- The three-run evidence archive `e4c_drill_visual_pixel_consumer.zip` confirms V1 failed in `PACKAGE_PREFLIGHT` (guide V12 omitted), V2 failed in `STAGED_VALIDATION` (literal guide anchor absent), and V4 failed in `STAGED_VALIDATION` at the Python dependency probe. V3 was superseded before Windows execution. All failed attempts have empty transaction journals, `rollback=NOT_NEEDED`, renderer OFF, `media_created=false`, and `release_authority=NONE`.
- V4 passed ZIP SHA, PowerShell 5.1 AST, rollback implementation audit, 23-member inventory, 18 operation inventory, support/design pins, exact operator-decision checks, 18 destination states, short staging, source roots and staged document dependencies. Its Python stderr is definitive: `ModuleNotFoundError: No module named 'PIL'`.
- The selected interpreter is the established project Python `C:\Users\vinxe\AppData\Local\Programs\Python\Python313\python.exe`, Python 3.13.14. Historical V121 D99 and E4C binder process receipts confirm this exact executable path/version. The interpreter is valid but Pillow is not installed; the probe never reached RAQM.
- V121 `c11c-suite/requirements.txt` and `c11c-suite/c11c-producer/requirements.txt` declare PySide6 only. Do not mutate protected/shared C11-C requirements. V5 introduces the D-owned `tools/c11d/d9/requirements-visual-consumer.txt` pin `Pillow==12.3.0`, matching the Pillow version used by the previously passing isolated 35/35 stage.
- Python dependency installation is operator-managed and is NOT performed by the overlay installer. Install Pillow 12.3.0 into the same canonical Python 3.13 runtime used by the existing Producer, then verify `features.check_feature('raqm')` is true. This is a runtime prerequisite, not a C11-C source change.
- V5 accepts an explicit `-PythonExe` path and checks Python 3.13.x + exact Pillow 12.3.0 + RAQM before any repository write. Consumer/service/test source bytes remain unchanged from V4. The 35 tests are not repeated absent consumer source drift; V5 still requires their staged Windows run before transaction.
- Current status: V1/V2/V4 FAILED_CLOSED_PRE_TRANSACTION; V3 SUPERSEDED_BEFORE_WINDOWS; V5 package awaits operator-managed Pillow preparation and then Windows installer execution. No consumer transaction has occurred.

# C11-E E4C Visual Drill Execution Plan — V13 (2026-11-11)

## Accepted gates retained

- Dynamic binder V2 active-Windows PASS: run `DRILLV2_20261110T151200Z_626a7d5e`; 20/20 selectors, 20/20 independent runtime repeats, 20/20 request manifests, 20/20 lineage, 67/67 source pins. Receipt `31f631c3c23c6c1d277d67f52dd887010ee51be869798ab8db3fbdec8658fa01`.
- Godot console runtime hotfix V3 and headless smoke: PASS; receipt `526c7d360863af8fb53707c9c83162173f4c1f1eb349ee8d767fb97665167a31`. Preflight reuse receipt `9484a8fae7382d3e25159c347a6979514256009c5d2b7bbc8d7cbb2741b12672`.
- E1 service 32/32, existing D9 regressions and Loop22/authoring proofs are reusable; no repeat absent pin drift.

## A.1/A.3/B.1/D.1 policy scope

Operator decision record SHA `49efd5494f351f09d7597c4699e9c12e361b36884b6bfadacd822e6ff1480e04` explicitly approves A.1, A.3, E4B Loop composition, B.1 and D.1 by exact proposal hashes. Its scope is D-owned design/contract implementation and technical delivery-envelope review only. D.1 does not authorize selecting/generating/mixing/mastering audio or loudness policy. Renderer, media and release remain unauthorized.

A.3 stale dependency was reconciled as one exact D9.8 pointer change and is now CLOSED/PASS in active Windows by A.3 V5. The installed V5 receipt SHA is `d39eec2b3c1d969a3cb0d4e6aaa14b87aadcba74e42e58d283e00ea50768e881` (3 replacements +26 additions; changed-source tests 33+5+7+10; py_compile 8/8). The following preimage→postimage statement is the historical A.3 design record, not an instruction to reinstall it: current editorial review manifest preimage `2075da9c33c689861a68d3bd8fb19b7ed593c6e76010ab200880746aa6d1a470` → postimage `5702092bc1c88e4b333dd30cc150f0d383cd2006121037b0198905c75a3af795`; the sole JSON Pointer delta is `/source_lineage/6/sha256`, updated to D9.8 model `dabb458fc2215156ddb5ebea7e8ebec811098886ce2858733ba9fb13f6075ccb`. The archived historical bytes are added separately. The bridge V2 truthfully marks the current manifest replacement and confirms approval booleans unchanged.

## Source phase / ownership facts

Pinned C11-C source confirms PRE_ROLL 3s → GAME → END_CTA 3s → DONE. During PRE_ROLL, the player passes the global presentation index; during GAME it passes `_current_frame_index` (local GAME payload index); during END_CTA it passes the global presentation index. Native `VisualDrillEndCTA` owns the C11-C source-frame header during END_CTA; the C11-C shared editorial layer owns native header/footer. D fields must not occupy those source-frame slots and are proposed suppressed during PRE_ROLL/END_CTA.

## Two new exact-hash decisions — approved

1. Outer-band geometry/composition proposal, exact SHA `b22f9eb6fce39f877e432ff5f0051ecf5ab8575ecb9f580fe5f158994222fc09`, approved as proposed in the exact-hash operator decision record. Candidate: REVIEW_720 720×1280, 192px top and bottom bands, 504×896 uniform-contained original C11-C frame. Preserve source frame order/FPS/count; no crop/stretch. Approved as proposed for D-owned design/contract implementation and focused isolated visual tests only.
2. GAME payload → final presentation timebase proposal, exact SHA `44ab3b0fa09a6f7d42cd8cf2f1122cada6cbffe16a7a6b53c2af5e88d5daddc8`, approved as proposed in the exact-hash operator decision record. Candidate formula: `final_presentation_frame_index = pre_roll_frames + game_payload_frame_index`; at 30fps and 630 GAME frames, PRE_ROLL=90, GAME maps `[0,630)` to `[90,720)`, END_CTA `[720,810)`. D editorial suppressed during PRE_ROLL/END_CTA; native CTA remains. Approved as proposed for D-owned design/contract implementation only; no renderer input or media creation.

A.3's approved field span is `[0, actual_GAME_payload_frame_count)`; this proposal maps that window to the correct final stream interval without resampling or altering C11-C. B.1 cadence approval is not itself approval of this phase-specific offset.

## Historical A.3 overlay V2–V5 pre-write acceptance (closed by V5)

V4 installer must verify full package file inventory/bytes/SHA; canonical frozen C11-C hash; 13 supporting source pins; all three replacement pre/post states; all 26 add-only destinations; PowerShell 5.1 AST; stage active source plus payload; compile eight Python modules; run only changed suites 33+5+7+10; recheck support pins/replacement states immediately before writes. Use journal-before-mutation, non-null backups, atomic replacement, hash-guarded reverse rollback and separate stdout/stderr. No Git.

## Next implementation and family closeout

With both exact-hash decisions recorded: source-pin the D-owned consumer, implement at the existing family boundary, and prove all 20 selectors with phase-specific text visibility, long/empty/UNKNOWN cases, font shaping/coverage, clipping/overflow/contrast and deterministic source-frame identity. Do not mutate C11-C. Then native Drill A/V using silent protected C11-C capture, existing `FAMILY_MUSIC_V4` (not D3 V5), separate gameplay/music seeds, FFmpeg/FFprobe and human listen/review. Observe existing Producer GUI through E1 shared service.

E4C full closure → E5 cross-family determinism/seed isolation/profile non-leakage/GUI-CLI parity → E6 Smoke18 → E7 Matrix101 (99 provisional; CH_008/009 held) → E8 historical regression map/independent acceptance/freeze/separate promotion.

Renderer OFF; dispatch/media false; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/16 BLOCKED; D9.17 NO-GO; D10 blocked; release NONE.


The explicit operator approval record is `eb95da188065b8ebcb2371e2a6bcff6762ce000a5ca74f8ea384ecec4ee58303`. It does not authorize renderer-native input, renderer activation, dispatch, media/audio creation or release.


## V4 installer recovery test

V2 path-length failure was corrected by V3: stage root now uses `%TEMP%` (55 chars) with a 240-character projected-path ceiling. V3 then exposed a PowerShell StrictMode bug: two replacement-mode filters traversed all content-manifest rows, including three package metadata rows without a `.mode` property. V4 limits both filters to `$operationEntries` (payload-only), adds a required-field guard, and keeps package metadata outside operation-state logic. Both failures occurred before the payload transaction, so no repository source or overlay destination was changed. The installers did create their run-specific evidence directories and failure JSON under `artifacts/tests`.


## V5 Python runtime correction

V4 reached `STAGED_VALIDATION` and stopped at `py_compile` with `Unknown option: -3`. The selected executable was `Python313\python.exe`, not the `py.exe` launcher. V5 resolves an actual `python.exe`, runs a `-c` version probe, requires `sys.version_info[:2] == (3,13)`, then invokes `python.exe -m py_compile` and `python.exe <test.py>` without `-3.13`. This is the correct invocation for the executable path present on the operator's Windows machine. The V4 failure was pre-transaction; no repository writes occurred.


## Consumer V1–V4 installation recovery — current status

A.3 V5 is installed PASS (receipt SHA `d39eec2b3c1d969a3cb0d4e6aaa14b87aadcba74e42e58d283e00ea50768e881`); do not rerun its four changed-source suites or 8-module compile.

- V1 failed pretransaction because its installer required guide V12 without bundling it.
- V2 bundled guide V12 and passed initial package/pin/destination checks, but failed staged validation because the exact `hash-guarded rollback` heading was absent; the described operational rule already used expected-postimage and exact-preimage semantics. Empty journal, `rollback=NOT_NEEDED`.
- V3 added the explicit `Hash-guarded rollback` policy heading and source inspection of the rollback function. It was superseded before Windows use when the faithful V121 stage replay exposed missing read-only test roots `challenges/`, full `assets/` and `docs/current/d/`.
- V4 is the current active-Windows candidate. It includes those three roots in the path budget and read-only stage copy, validates their existence before Python, and checks the actual rollback implementation (expected-postimage match, exact-preimage backup hash, refusal of unknown state, atomic restore and restored-preimage verification). The 18-operation transaction remains one pinned E1 replacement +17 D-owned additions; stage roots are never transaction operations. E1 successor SHA `e5dbf9baa72d4c066ff8ba24006df954700d72a5b0f11f9f88aec653e84dce87`; consumer SHA `e1e78a00d7d9384f7b99e9da16c7388be59a239bbcd8d1d9de44a881b68d3a03`; test SHA `15c417555382ff397991e4402dc313708ab17d29df78d4cbcd97d96b4a31609a`.

V1, V2 and V3 all stopped before the consumer payload transaction. No consumer V1–V4 transaction has occurred. V4's reconstructed V121 stage passed Python 3.13.5 / Pillow 12.3.0 / RAQM, py_compile 3/3 and tests 35/35; the selector samples are synthetic. Active Windows PowerShell 5.1 AST, package/dependency checks, staged runtime/tests, immediate pre-transaction rechecks and install receipt are still required. Run V4 (not a prior installer), stop on first failure, and inspect its exact receipt and 18 postimages only after a successful installation.

## V4 staging correction

V3 was superseded before Windows use after local replay against V121 proved three E1 test source roots were missing from its temporary tree: `challenges/`, full `assets/` and `docs/current/d/`. V4 adds these roots to both path-length preflight and read-only staging copy and validates their existence before Python. The exact 35-test suite passes with the reconstructed complete source tree. Windows acceptance remains pending.
