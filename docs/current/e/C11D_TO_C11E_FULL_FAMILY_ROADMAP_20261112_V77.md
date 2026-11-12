# ROADMAP OVERRIDE — D99 single-selector locale failure and recovery — 2026-11-12

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
