# C11-E Next Window Start Prompt — V130 (2026-11-11)

## V9 current state — 2026-11-11

Consumer V8 stopped in `STAGED_VALIDATION` before any repository transaction. The exact cause was a StrictMode ordering bug in the installer: `$testSource` was inspected for the removed `QT_VERSION_STR` token before it was assigned from the staged test file. The run's journal is empty and `rollback=NOT_NEEDED`; no rollback or repository recovery is required. V9 fixes this by loading both `$consumerSource` and `$testSource` first, validating both are non-empty, and only then inspecting their contents. This is an installer-only correction. The Qt consumer, 35-test module and E1 service replacement bytes are unchanged from V8.

V9 also corrects the run ID and receipt/failure schema identities to V9. It preserves the 18-operation scope (one exact-pinned E1 service REPLACE + 17 D-owned ADDs), all 13 support pins, 10 design/font pins, exact-hash operator decisions, frozen C11-C manifest and no-new-dependency policy. The installer uses the existing canonical Producer Python/PySide6 only; it must not invoke pip, install/uninstall packages, change requirements or mutate shared environment dependencies.

V9 is a candidate only. Windows PowerShell 5.1 AST, Qt runtime probe, py_compile 3/3, tests 35/35, immediate pre-transaction rechecks and successful receipt are still pending. No consumer V1–V8 transaction has been recorded. Stop at first failure; do not repeat A.3 V5, binder V2, Godot V3, Loop22 or historical authoring accepted gates.

Next step: verify V9 ZIP SHA and sidecar, then run the V9 installer with the existing canonical `-PythonExe`. Require the same 18 destination states and all pre-write gates. After PASS, inspect `INSTALL_RECEIPT.json`, its SHA and all 18 postimages before any E1 integration review. C11-C remains sole production authority; renderer OFF; dispatch/media/audio OFF; `release_authority=NONE`.


## V8 current state — 2026-11-11

V7 failed closed in `STAGED_VALIDATION` before transaction. Its installer imported `QT_VERSION_STR` from `PySide6.QtCore`; the canonical PySide6 runtime does not export that symbol. This is an installer probe defect, not evidence that PySide6, Qt, QImage or QPainter is missing. The preceding imports of `PySide6.__version__` succeeded. `journal=[]`; `rollback=NOT_NEEDED`; no checkout write occurred.

V8 changes the probe to `from PySide6.QtCore import qVersion` and records `qVersion()` as the Qt runtime version. It requires Qt 6.x, alongside Python 3.13.x, existing PySide6 6.8–6.x, non-null RGB888 QImage and active QPainter. The official Qt for Python API lists `qVersion()` as a QtCore function. V8 does not install, upgrade or uninstall packages, invoke pip, edit requirements, or mutate the shared Python environment.

The consumer, its 35 Qt tests and the E1 service replacement are byte-identical to V7. No functional test result is inferred from the failed V7 runtime probe. V8 must still pass Windows PowerShell 5.1 AST, inventory/pins/destinations/staging, runtime probe, `py_compile` 3/3, all 35 Qt tests and immediate pre-transaction checks before any write. Do not repeat accepted A.3, binder V2, Godot V3, Loop22 or historical Drill authoring.

Governance remains unchanged: C11-C frozen manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; renderer OFF; dispatch/media/audio OFF; `release_authority=NONE`; operator manages commits; Git checks skipped.

## Next operation
Run Consumer V8 ZIP + sidecar in the active Windows checkout. V7 failed closed before transaction due to installer import of `QT_VERSION_STR`; V8 replaces this with `qVersion()` and validates Qt 6.x. No pip, install/uninstall/upgrade or requirements edit. Require AST, all inventory/pins/destination/staging checks, Qt offscreen probe, py_compile 3/3, all 35 Qt tests, process env restoration and immediate pre-transaction checks. Review receipt and 18 postimages. Accepted A.3/binder/Godot/Loop evidence is not repeated.

---


Continue active checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`; sole authority. `ChallengeEngineV01_STATELESS-C11-E-V121-NIGHTLY.zip` is read-only evidence. Never extract over checkout. Operator commits; no Git checks. SHA pins and frozen C11-C manifest required.

## Read first

Current Authority V127, Doc Index V89, Gates V125, Backlog V101, E4C Plan V15, Blocker V47, Roadmap V73, Docket V7, Phase Audit V2, PowerShell Runner Guide V16, Incident Register V7, Consumer Findings V8, Master/Start V128 and First V52.

## Current blocker and exact next action

Consumer V6 failed closed pre-transaction in staged validation because guide V15 omitted exact `No new Python dependency` anchor; V15 also retained stale V14 Pillow provisioning text. Evidence run `E4C_DRILL_VISUAL_PIXEL_CONSUMER_V6_20261111T004628_177cd6f5`, `journal=[]`, rollback `NOT_NEEDED`. No transaction occurred.

Run Consumer V7 ZIP + sidecar. It updates guide V16 and continuity docs; Qt consumer, tests and E1 service bytes remain as V6. Reuse existing PySide6 only. Absolutely no Pillow/PIL/RAQM, pip, new package/requirements/lock file, or shared environment change. Require the complete V7 gates: PS 5.1 AST; 24 members/23 rows; 18 operations; 13 support pins; 10 design/font pins; two exact approvals; 18 destination states; complete stage roots; guide V16/docket V7/phase audit V2/incident V7; Python 3.13 + PySide6 Qt offscreen; py_compile 3/3; 35/35 Qt tests; restored `QT_QPA_PLATFORM`; immediate rechecks before writes. Inspect exact receipt and 18 postimages.

## Do not repeat / protected status

A.3 V5 CLOSED; E4B Loop22, historical Drill authoring, E4C binder V2 and Godot V3 accepted. Do not rerun absent source drift. C11-C native Drill PRE_ROLL/GAME/END_CTA/DONE, native END_CTA/header/footer and family music remain protected. Design/timebase exact-hash decisions remain limited to D-owned design/contract and isolated pixel tests. Renderer OFF; dispatch/media/audio OFF; `release_authority=NONE`.

After V7 pass: inspect integration at existing E1 shared GUI/CLI boundary, real Qt Producer frames, all 20 selectors, fonts/pixels/phase/timebase; then authorized family-native A/V, E4C closure, E5, E6 Smoke18, E7 Matrix101 (99 provisional; CH_008/009 held), E8 independent regression/freeze/separate promotion.

---

# C11-E Next Window Start Prompt — V127 (2026-11-11)

Continue active checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`, sole authority. V121 NIGHTLY ZIP read-only. Operator manages commits; skip Git checks. Enforce source pins and frozen C11-C manifest.

## Read first

Current Authority V126, Doc Index V88, Gates V124, Backlog V100, E4C Plan V14, Blockers V46, Roadmap V72, Docket V7, Phase Audit V2, Runner Guide V15, Incident V6, Findings V7 and prompts Master/Start V127 + First V51.

## Do not repeat / current blocker

A.3 V5 CLOSED; binder V2, Godot V3, Loop22 and historical Drill authoring accepted. Consumer V1/V2/V4 failed closed, V3 superseded, V5 forbidden; no transaction. Assistant's Pillow install instruction was erroneous; remove only newly installed Pillow and verify absence, preserve PySide6. V6 uses existing PySide6 Qt with no new dependency, pip, requirements edit or shared environment mutation. It is a new backend requiring fresh Windows py_compile 3/3 and Qt tests 35/35 before transaction.

# C11-E Next Window Start Prompt — V126 (2026-11-11)

Continue the active Windows checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`; it is sole authority. `ChallengeEngineV01_STATELESS-C11-E-V121-NIGHTLY.zip` is read-only evidence only and must never be extracted over the checkout. Operator manages commits. Skip Git/HEAD/status/branch/.git checks. Enforce exact SHA-256 source pins and frozen C11-C manifest.

## Read authority and roadmap

Read Current Authority V125, Current Doc Index V87, Gates Matrix V123, Backlog V99, E4C Drill Plan V13, Blocker Register V45, Family Roadmap V71, Drill Decision Docket V7, Drill Phase Ownership Audit V2, PowerShell Runner Style Guide V14, Installer Incident Register V5, Consumer Implementation Findings V6, plus Master V126 and First V50.

## Accepted gates — do not repeat absent source drift

- E4B Loop22 CLOSED/operator-approved: 44/44 A/V, 22/22 A/B, 25/25 tests and human visual/audio approval.
- Historical Drill authoring 20/20 over 24 pins.
- E4C binder V2 active Windows PASS: 20/20 selectors, repeats, request manifests and lineage; 67/67 pins; receipt `31f631c3c23c6c1d277d67f52dd887010ee51be869798ab8db3fbdec8658fa01`.
- Godot console V3 PASS; receipt `526c7d360863af8fb53707c9c83162173f4c1f1eb349ee8d767fb97665167a31`; preflight reuse `9484a8fae7382d3e25159c347a6979514256009c5d2b7bbc8d7cbb2741b12672`.
- A.3 Drill design-contract V5 installed CLOSED/PASS; receipt `d39eec2b3c1d969a3cb0d4e6aaa14b87aadcba74e42e58d283e00ea50768e881`; no rerun.

## Exact consumer installer history

- Consumer V1 failed `PACKAGE_PREFLIGHT`: guide V12 absent from payload.
- V2 failed staged validation: required rollback policy phrase absent from guide.
- V3 superseded before Windows qualification because source staging omitted `challenges/`, full `assets/`, and `docs/current/d/`.
- V4 passed ZIP/inventory/pins/rollback/AST/stage checks but stopped before writes because the canonical Python 3.13.14 interpreter lacked `PIL`; `ModuleNotFoundError: No module named 'PIL'`. Evidence archive `e4c_drill_visual_pixel_consumer.zip`; run `E4C_DRILL_VISUAL_PIXEL_CONSUMER_V4_20261111T001315_ed8f8d25`; `journal=[]`, rollback `NOT_NEEDED`.
- V5 adds D-owned `tools/c11d/d9/requirements-visual-consumer.txt` with `Pillow==12.3.0`, mandatory `-PythonExe`, and exact Pillow/RAQM runtime validation. The installer NEVER invokes pip. Consumer/E1/test sources are unchanged from V4. V5 is not installed and is not yet Windows-qualified.

## Operator prerequisite before V5

Use the same Python executable used by the existing Producer, not a test-only venv:

```powershell
$PythonExe = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python313\python.exe'
& $PythonExe -m pip install --disable-pip-version-check --only-binary=:all: 'Pillow==12.3.0'
if ($LASTEXITCODE -ne 0) { throw 'Pillow installation failed' }
& $PythonExe -c 'import sys,json; from PIL import __version__,features; r={"python":"{}.{}.{}".format(*sys.version_info[:3]),"pillow":__version__,"raqm":bool(features.check_feature("raqm"))}; print(json.dumps(r)); raise SystemExit(0 if sys.version_info[:2] == (3,13) and __version__ == "12.3.0" and r["raqm"] else 2)'
if ($LASTEXITCODE -ne 0) { throw 'Python/Pillow/RAQM verification failed' }
```

Expected Python 3.13.14, Pillow 12.3.0, RAQM true. Stop if any check fails. This is operator-managed runtime preparation; it does not edit project source or C11-C requirements. Do not run the V5 installer before this preflight passes.

## Install V5

Historical V5 instruction — superseded; use V9 below. Run `INSTALL_AND_VALIDATE_C11E_E4C_DRILL_VISUAL_PIXEL_CONSUMER_V5.ps1` in Windows PowerShell 5.1, passing `-ProjectRoot` and `-PythonExe $PythonExe`. Require 25 ZIP members, 24 contents rows, 19 typed operations (1 E1 REPLACE +18 D-owned ADD), 13 support pins, 10 design/font pins, both exact approvals, 19 destination states, all source roots, Python 3.13.x/Pillow 12.3.0/RAQM, py_compile 3/3 and staged tests 35/35 before any writes. Review receipt, SHA and all 19 postimages. Stop at the first failure; no PASS after failure.

## After successful install

Review E1 diff and receipt, then connect the consumer only at the existing E1 shared GUI/CLI service boundary. Observe the existing Qt Producer with real protected C11-C source frames over all 20 Drill selectors; inspect font shaping/glyphs, overflow/clipping/contrast, phase visibility, timebase and source/pixel identity. Separately qualify native `FAMILY_MUSIC_V4` A/V with independent gameplay/music seeds, FFmpeg/FFprobe and human review under applicable authorization.

Roadmap: E4C closure → E5 → E6 Smoke18 → E7 Matrix101 (99 provisional; CH_008/009 held) → E8 historical C-to-E regression, independent acceptance, freeze and separate explicit promotion/cutover. C11-C remains the sole production authority. Renderer OFF; dispatch/media false; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`.
