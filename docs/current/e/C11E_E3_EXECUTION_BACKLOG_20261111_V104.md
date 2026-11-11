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
