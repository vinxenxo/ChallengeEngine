# ADDENDUM — EXECUTION ADAPTER CONSUMPTION CONTRACT — 2026-11-11

The visual consumer remains unchanged and D-owned. The shared A/V adapter consumes its validated composition plan after E1 preparation; it does not promote the consumer or change its plan-only status. Execution requires `text.visible_fields` to contain one or more actual title/subtitle/call_to_action strings and the plan phase policy must be GAME=true, PRE_ROLL=false, END_CTA=false, DONE=false. Empty/UNKNOWN text is not a composition PASS. The exact original C11-C frame remains the inner source, and editorial appears only in the approved 192px outer bands during GAME.

---

## V9 current state — 2026-11-11

Consumer V8 stopped in `STAGED_VALIDATION` before any repository transaction. The exact cause was a StrictMode ordering bug in the installer: `$testSource` was inspected for the removed `QT_VERSION_STR` token before it was assigned from the staged test file. The run's journal is empty and `rollback=NOT_NEEDED`; no rollback or repository recovery is required. V9 fixes this by loading both `$consumerSource` and `$testSource` first, validating both are non-empty, and only then inspecting their contents. This is an installer-only correction. The Qt consumer, 35-test module and E1 service replacement bytes are unchanged from V8.

V9 also corrects the run ID and receipt/failure schema identities to V9. It preserves the 18-operation scope (one exact-pinned E1 service REPLACE + 17 D-owned ADDs), all 13 support pins, 10 design/font pins, exact-hash operator decisions, frozen C11-C manifest and no-new-dependency policy. The installer uses the existing canonical Producer Python/PySide6 only; it must not invoke pip, install/uninstall packages, change requirements or mutate shared environment dependencies.

V9 is a candidate only. Windows PowerShell 5.1 AST, Qt runtime probe, py_compile 3/3, tests 35/35, immediate pre-transaction rechecks and successful receipt are still pending. No consumer V1–V8 transaction has been recorded. Stop at first failure; do not repeat A.3 V5, binder V2, Godot V3, Loop22 or historical authoring accepted gates.

Next step: verify V9 ZIP SHA and sidecar, then run the V9 installer with the existing canonical `-PythonExe`. Require the same 18 destination states and all pre-write gates. After PASS, inspect `INSTALL_RECEIPT.json`, its SHA and all 18 postimages before any E1 integration review. C11-C remains sole production authority; renderer OFF; dispatch/media/audio OFF; `release_authority=NONE`.

---

## V7 policy correction — existing Qt only; no new Python dependency (2026-11-11)

## V8 current state — 2026-11-11

V7 failed closed in `STAGED_VALIDATION` before transaction. Its installer imported `QT_VERSION_STR` from `PySide6.QtCore`; the canonical PySide6 runtime does not export that symbol. This is an installer probe defect, not evidence that PySide6, Qt, QImage or QPainter is missing. The preceding imports of `PySide6.__version__` succeeded. `journal=[]`; `rollback=NOT_NEEDED`; no checkout write occurred.

V8 changes the probe to `from PySide6.QtCore import qVersion` and records `qVersion()` as the Qt runtime version. It requires Qt 6.x, alongside Python 3.13.x, existing PySide6 6.8–6.x, non-null RGB888 QImage and active QPainter. The official Qt for Python API lists `qVersion()` as a QtCore function. V8 does not install, upgrade or uninstall packages, invoke pip, edit requirements, or mutate the shared Python environment.

The consumer, its 35 Qt tests and the E1 service replacement are byte-identical to V7. No functional test result is inferred from the failed V7 runtime probe. V8 must still pass Windows PowerShell 5.1 AST, inventory/pins/destinations/staging, runtime probe, `py_compile` 3/3, all 35 Qt tests and immediate pre-transaction checks before any write. Do not repeat accepted A.3, binder V2, Godot V3, Loop22 or historical Drill authoring.

Governance remains unchanged: C11-C frozen manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; renderer OFF; dispatch/media/audio OFF; `release_authority=NONE`; operator manages commits; Git checks skipped.

### Runtime probe API
The installer uses `PySide6.QtCore.qVersion()` for Qt runtime identification. It must not import `QT_VERSION_STR`. This affects only diagnostic/preflight reporting, not rendered consumer output or pixel behavior.

---


The V6 consumer Qt backend remains the candidate implementation. V6 failed before transaction because the staged guide V15 omitted the installer's exact `No new Python dependency` policy phrase; the guide also retained superseded V14 Pillow instructions. V7 advances the guide to V16 and resolves both documentation conflicts. The code and 35-test suite remain identical to V6.

- Reuse the existing Producer PySide6/Qt runtime only (`QImage`, `QPainter`, `QFontDatabase`, `QFontMetricsF`, `QFontInfo`, `QRawFont`).
- No new Python dependency; no Pillow/PIL, RAQM, extra wheels, requirements/lock files, pip calls, installation or shared-environment mutation.
- The exact Inter-Bold and Noto Sans Mono font pins, geometry, timebase, family/phase behavior and design-decision hashes remain unchanged.
- Qt `SmoothTransformation` is the contained source interpolation. It is not Pillow Lanczos, and V4/Pillow results are not evidence of Qt pixel identity.
- Qt backend qualification remains pending on active Windows: `py_compile` 3/3, 35/35 tests and then live Producer observation are required.

V6 evidence run `E4C_DRILL_VISUAL_PIXEL_CONSUMER_V6_20261111T004628_177cd6f5` ended before transaction with empty journal and `rollback=NOT_NEEDED`; no new checkout source was installed.

---

## V6 backend contract — Qt/PySide6, no new dependencies (2026-11-11)

- The in-memory 720x1280 RGB888 consumer now uses PySide6 Qt (`QImage`, `QPainter`, `QFontDatabase`, `QFontMetricsF`, `QRawFont`). PySide6 is already an existing Producer dependency; do not add, install or upgrade any package for this consumer.
- Exact pinned Inter-Bold and Noto Sans Mono files remain unchanged and are loaded through `QFontDatabase.addApplicationFont`; family resolution and glyph coverage are checked with `QFontInfo`/`QRawFont`. Layout measurements use shaping-aware `QFontMetricsF`; drawing occurs only into D-owned in-memory `QImage`. Uniform source containment uses Qt `SmoothTransformation` at the approved 504x896 viewport. This does not claim equivalence to Pillow Lanczos and is a new backend qualification.
- Tests run with `QT_QPA_PLATFORM=offscreen` in child processes only; the installer restores the original environment variable. No `PIL`, Pillow, RAQM, pip command or dependency lock remains in the package.
- The geometry/timebase exact hashes remain unchanged. Phase gating continues to suppress D text during PRE_ROLL/END_CTA; native C11-C header/footer and native family music remain authoritative.
- V6's rewritten Qt 35-test suite is NOT yet accepted. It must pass on active Windows before any transaction.

## V5 runtime dependency contract — 2026-11-11

- The consumer uses Pillow for in-memory RGB composition, LANCZOS source containment, and FreeType/RAQM text layout. The isolated suite's known-good environment was Python 3.13.5, Pillow 12.3.0, FreeType and RAQM.
- Pin the runtime dependency in `tools/c11d/d9/requirements-visual-consumer.txt` as exactly `Pillow==12.3.0`. Keep this D-owned; do not modify `c11c-suite/requirements.txt` or any protected C11-C file.
- The active Producer's canonical interpreter is `C:\Users\vinxe\AppData\Local\Programs\Python\Python313\python.exe` (3.13.14). V4 confirmed this runtime currently lacks `PIL`. Operator must manually install the pinned wheel into the same interpreter that will run Producer, then verify RAQM. Do not use a separate venv for installer-only tests unless the Producer is also explicitly configured to use it; current architecture uses the existing shared Python runtime.
- Installer V5 takes mandatory `-PythonExe`, performs exact Python 3.13.x / Pillow 12.3.0 / RAQM validation and never invokes pip. Dependency provisioning is a separate operator step before installation.
- Consumer implementation, E1 service and 35-test source remain byte-identical to V4. No consumer suite has been newly requalified on Windows yet; V5 installer still requires 35/35 before transaction.

# C11-E E4C Drill D-Owned Composition Consumer — Specification V5

**Status:** in-memory D-owned pixel consumer; faithful reconstructed V121 stage passed py_compile 3/3 and the isolated suite 35/35 using Python 3.13.5, Pillow 12.3.0, FreeType and RAQM. V1/V2 failed closed before transaction; V3 was superseded before Windows use; V4 is prepared for active Windows but has not been installed or accepted. The 20 selector samples are synthetic, not live C11-C frames. No renderer/native-input or media-pipeline connection.

**Approved geometry:** `b22f9eb6fce39f877e432ff5f0051ecf5ab8575ecb9f580fe5f158994222fc09`  
**Approved timebase:** `44ab3b0fa09a6f7d42cd8cf2f1122cada6cbffe16a7a6b53c2af5e88d5daddc8`  
**Operator decision record:** `eb95da188065b8ebcb2371e2a6bcff6762ce000a5ca74f8ea384ecec4ee58303`

## Boundary

The consumer takes a validated E1 Visual Drill intent plus one REVIEW_720 source frame and returns one in-memory 720×1280 RGB image and phase/source mapping metadata. It does not write media, create renderer input, dispatch work, launch the C11-C engine, Godot or FFmpeg, or connect to the Producer GUI. E1 GUI/CLI routing remains the same shared service; this overlay updates its lineage precondition but does not yet connect image consumption to the UI or renderer.

## Source and authority

- E1 intent passes `c11e_production_service.validate_c11e_production_intent`.
- A.3 historical lineage resolves only through bridge V2 SHA `aec0e387f167f4b821b7d94f06a67f78f498be939fe3cda857d20ce550819cac`, proving the archived historical bytes, current review manifest, D9.8 model and single approved JSON-pointer transition.
- Geometry and timebase approvals are revalidated against the separate operator record. Proposal files remain byte-identical and retain `PROPOSED_NOT_APPROVED_NOT_RENDERER_INPUT`.
- Eight audited C11-C phase/ownership sources remain read-only and pinned by E1.

## Geometry and pixels

- Canvas: 720×1280 (`REVIEW_720`), background `#05070B`.
- Source viewport: x=108, y=192, width=504, height=896; uniform scale 0.7; Pillow `LANCZOS`; no crop, stretch, frame reordering or temporal resampling.
- Title/subtitle use approved 648px-wide top-band blocks; CTA uses approved bottom-band block. Existing repository font assets are SHA-pinned; no fonts are added/replaced.
- D editorial appears during GAME only. PRE_ROLL and END_CTA suppress D text. Native `VisualDrillEndCTA` and native C11-C header/footer ownership remain authoritative.
- Empty/missing/`UNKNOWN` fields are suppressed. Raw text is not silently truncated/ellipsized. Unsupported glyphs or text-capacity overflow fail closed. `language` remains metadata-only.
- `request.seed` and `request.music_seed` remain independent; Drill music remains native C11-C `FAMILY_MUSIC_V4`, not D3 V5.

## Timebase

`final_presentation_frame_index = pre_roll_frames + game_payload_frame_index`. PRE_ROLL and END_CTA use global player indexes; GAME uses local payload indexes. At 30fps and 630 GAME frames: PRE_ROLL `[0,90)`, GAME `[90,720)`, END_CTA `[720,810)`. No temporal resampling occurs.

## Verification and limits

The focused suite contains 35 tests over synthetic 720×1280 source frames. A faithful reconstructed V121 source stage passed py_compile 3/3 and 35/35 with Python 3.13.5, Pillow 12.3.0, FreeType and RAQM. The synthetic sample is not C11-C output, a live source-frame capture, Windows acceptance or human review. The active-Windows installer independently checks Python 3.13.x, Pillow/RAQM and exact fonts before writes.

## Installer recovery and current gate

- V1 omitted its required style guide V12 and failed at PACKAGE_PREFLIGHT; no transaction.
- V2 carried V12 but the guide's policy section lacked the literal heading `hash-guarded rollback` required by its own preflight. The guide's operational rule already described expected-postimage rollback and exact-preimage restoration; V2 failed closed in STAGED_VALIDATION with an empty journal and `rollback=NOT_NEEDED`.
- V3 added the explicit heading and checks the actual installer rollback code for postimage matching, exact-preimage backup validation and refusal to restore/delete unknown states. It was superseded before Windows after V121 source-stage replay exposed omitted roots `challenges/`, full `assets/`, and `docs/current/d/`.

## Next E4C gates

1. Install V5 and review exact receipt, postimages and Windows 35/35 evidence. V4 includes style guide V13, docket V7, phase audit V2, incident register V4, and all required stage roots.
2. Source-review the consumer connection at the existing E1/Producer boundary; preserve GUI/CLI parity. No new Producer, binder or suite module.
3. Observe Qt Producer runtime with actual C11-C source frames; inspect all 20 selectors, phase visibility, typography/shaping, glyph coverage, clipping/overflow/contrast and deterministic source/pixel identity.
4. Qualify native family A/V only under separate explicit audio authority: silent protected C11-C capture, existing `FAMILY_MUSIC_V4`, independent seeds, FFmpeg/FFprobe and human listening/visual review. D.1 is only an envelope.
5. Close E4C only after visual/pixel, GUI/CLI, separately authorized A/V and operator-review gates pass.

## Test-stage source completeness

The integration suite prepares a real E1 Drill intent and exercises the existing D9.9/D9.10 chain. Its stage must include the active pinned roots `challenges/`, full `assets/`, and `docs/current/d/` in addition to the previously staged directories. V4 validates and copies them before invoking Python, with the roots treated as read-only test inputs rather than transaction destinations.
