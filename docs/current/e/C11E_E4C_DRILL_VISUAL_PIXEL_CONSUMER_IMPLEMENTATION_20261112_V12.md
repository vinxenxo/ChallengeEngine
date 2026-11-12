# IMPLEMENTATION FINDINGS ADDENDUM — D99 execution stop before Qt composition — 2026-11-12

D99's E1 and D planning evidence validate the current Qt consumer plan and visible text. Native C11-C capture did not launch because the adapter emitted a locale decimal for `SpeedMultiplier`; Windows PowerShell received `75000` and rejected it. Therefore this run provides no positive or negative evidence about Qt composition, FFmpeg raw-frame decode, the family music generator, muxing or final stream hashes. V1.4 alters only the adapter's PowerShell numeric handoff and adds `es-ES` regression coverage.



## D99-GUI-85201B7B4FF7 — single-selector A/V pilot diagnosis — 2026-11-12

**Authoritative evidence:** `D99-GUI-85201B7B4FF7.zip` SHA-256 `0913179f9852b7b1f75c2a7e2f763a111bc8d807d08d20036a2891ae94661f56`; `D99-GUI-85201B7B4FF7-tests.zip` SHA-256 `16f0e199429deffb85025cd35d0cfd4fe2ec9fe237cf66482f6de6b14cd6ef23`.

The GUI's **Resolver + Plan** stage is successful, not a failure: E1 receipt is `PASS_E1_PREPARATION_ONLY`; GUI/CLI semantic parity is `PASS`; D9.10 bridge planning is `PASS_BRIDGE_PLANNING_ONLY`; D composition plan is valid with real GAME-visible editorial; the request is `visual_drills / tracking / tier-1`, gameplay seed `12345`, music seed `840001`, `REVIEW_720`. This remains deliberately plan-only at E1 and does not claim renderer or dispatch activation. The second GUI action, the shared D A/V executor, fails before the native C11-C producer starts.

Exact failure from `logs/c11c_drill_producer.log`: C11-C's `run_visual_drill_production.ps1` rejects `-SpeedMultiplier` because it receives `75000`, outside `[ValidateRange(0.1,3.0)]`. The pinned profile `profiles/difficulty/visual_drill_tracking.json` has tier 1 `speed_multiplier=0.75` (source SHA-256 `6de8812bd46904e122ecdd0eae22fb2979bd75399c34779248c6569e833c921e`). The adapter applied Python's host decimal separator and sent `0,75000`. On the operator's locale, Windows PowerShell 5.1 parameter binding split/coerced that comma decimal and delivered `75000`. This is a cross-locale numeric argument-boundary defect in the D adapter, not a defect in the pinned C11-C launcher or difficulty profile.

The failure occurs before a successful C11-C capture. There is no native MP4, no D frame composition, no FAMILY_MUSIC_V4 WAV generation, no mux, and no final FFprobe result in this run. The failure does not indicate an editorial, font, Qt, geometry, phase/timebase, music determinism, or A/V stream-equivalence defect. The first evidence bundle contains `RUNNING` and `FAILURE` receipts and the exact native producer log. The `-tests.zip` is a preparation/parity/contract receipt bundle; it does not show a second independent A/V failure. Do not infer additional failures from its intentionally plan-only receipts.

**V1.4 correction:** remove host-locale formatting entirely. Python emits an ASCII invariant string such as `0.75000` to a string-typed PowerShell wrapper. The wrapper parses it with `[System.Globalization.CultureInfo]::InvariantCulture`, sets the wrapper thread culture to invariant for the call, then invokes the existing pinned C11-C launcher with an already-typed `[double]$speed`. The native C11-C launcher remains byte-identical and receives `0.75`; C11-C stays silent via `-NoSound`. The wrapper is retained in the run logs and its hash/argument are written into the execution receipt. Regression tests cover invariant formatting, wrapper parse/type handoff, and absence of host-locale formatting. The V1.4 installer additionally executes this exact wrapper against a dummy parameter-compatible launcher while forcing `es-ES`, and requires the dummy to record `0.75` before any repository mutation.

The failed output root `artifacts/production/c11e/D99-GUI-85201B7B4FF7` is intentionally preserved. It must not be overwritten. The retry must use a **new unique request_id/output root** (generate a fresh GUI request and repeat Resolver + Plan); do not delete or recycle this failed evidence. After V1.4 installation PASS: audit its postimages/source pins, rerun the GUI plan stage with a fresh ID, then execute only `tracking/tier-1`. Continue only when native capture, D composition, FAMILY_MUSIC_V4 A/B/C, final A/C video/audio stream hashes, FFprobe, and human visual/listening review pass. CLI smoke/parity follows on the same shared adapter. Do not start the 20-selector A/V matrix until the single-selector result is accepted.

Governance is unchanged: E1 `PREPARE_ONLY`; `family_adapter.status=NOT_CONNECTED_E1`; `production_dispatch=false`; `release_authority=NONE`; no Git checks; commits operator-managed; C11-C frozen manifest SHA remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.


---

# IMPLEMENTATION FINDINGS ADDENDUM — A/V EXECUTION SEAM — 2026-11-11

The pixel consumer source remains pinned and unchanged. A single D execution module invokes `compose_frame` per native decoded frame. Before execution it validates the E1 intent and consumer plan, rejects empty editorial fields, then checks E1 source pins. A second source-pin check is executed immediately before invoking the native C11-C silent capture; a final check occurs after audio mux and stream-hash validation. The pre/immediate-pre/post pin sets are serialized in the A/V receipt.

The adapter calls the native C11-C launcher with `-NoSound`, then invokes only the existing `C11CSafeAmbient.py` / `FAMILY_MUSIC_V4` route using `request.music_seed`. No D3 V5 call and no C11-C gameplay-seed-coupled audio. This adapter is a scoped A/V qualification consumer; the visual-consumer plan's `D_OWNED_VISUAL_CONSUMER_READY_FOR_ISOLATED_PIXEL_TESTS` status remains truthful and untouched.

---

## V9 current state — 2026-11-11

Consumer V8 stopped in `STAGED_VALIDATION` before any repository transaction. The exact cause was a StrictMode ordering bug in the installer: `$testSource` was inspected for the removed `QT_VERSION_STR` token before it was assigned from the staged test file. The run's journal is empty and `rollback=NOT_NEEDED`; no rollback or repository recovery is required. V9 fixes this by loading both `$consumerSource` and `$testSource` first, validating both are non-empty, and only then inspecting their contents. This is an installer-only correction. The Qt consumer, 35-test module and E1 service replacement bytes are unchanged from V8.

V9 also corrects the run ID and receipt/failure schema identities to V9. It preserves the 18-operation scope (one exact-pinned E1 service REPLACE + 17 D-owned ADDs), all 13 support pins, 10 design/font pins, exact-hash operator decisions, frozen C11-C manifest and no-new-dependency policy. The installer uses the existing canonical Producer Python/PySide6 only; it must not invoke pip, install/uninstall packages, change requirements or mutate shared environment dependencies.

V9 is a candidate only. Windows PowerShell 5.1 AST, Qt runtime probe, py_compile 3/3, tests 35/35, immediate pre-transaction rechecks and successful receipt are still pending. No consumer V1–V8 transaction has been recorded. Stop at first failure; do not repeat A.3 V5, binder V2, Godot V3, Loop22 or historical authoring accepted gates.

Next step: verify V9 ZIP SHA and sidecar, then run the V9 installer with the existing canonical `-PythonExe`. Require the same 18 destination states and all pre-write gates. After PASS, inspect `INSTALL_RECEIPT.json`, its SHA and all 18 postimages before any E1 integration review. C11-C remains sole production authority; renderer OFF; dispatch/media/audio OFF; `release_authority=NONE`.

---

## V7 guide correction — V6 failed before transaction (2026-11-11)

## V8 current state — 2026-11-11

V7 failed closed in `STAGED_VALIDATION` before transaction. Its installer imported `QT_VERSION_STR` from `PySide6.QtCore`; the canonical PySide6 runtime does not export that symbol. This is an installer probe defect, not evidence that PySide6, Qt, QImage or QPainter is missing. The preceding imports of `PySide6.__version__` succeeded. `journal=[]`; `rollback=NOT_NEEDED`; no checkout write occurred.

V8 changes the probe to `from PySide6.QtCore import qVersion` and records `qVersion()` as the Qt runtime version. It requires Qt 6.x, alongside Python 3.13.x, existing PySide6 6.8–6.x, non-null RGB888 QImage and active QPainter. The official Qt for Python API lists `qVersion()` as a QtCore function. V8 does not install, upgrade or uninstall packages, invoke pip, edit requirements, or mutate the shared Python environment.

The consumer, its 35 Qt tests and the E1 service replacement are byte-identical to V7. No functional test result is inferred from the failed V7 runtime probe. V8 must still pass Windows PowerShell 5.1 AST, inventory/pins/destinations/staging, runtime probe, `py_compile` 3/3, all 35 Qt tests and immediate pre-transaction checks before any write. Do not repeat accepted A.3, binder V2, Godot V3, Loop22 or historical Drill authoring.

Governance remains unchanged: C11-C frozen manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; renderer OFF; dispatch/media/audio OFF; `release_authority=NONE`; operator manages commits; Git checks skipped.

### V7 probe defect and V8 correction
The Windows V7 log proves that `from PySide6 import __version__` succeeded but the following import of `QT_VERSION_STR` raised ImportError. That localizes the fault to the selected constant, not package discovery. V8 uses QtCore `qVersion()`; the official Qt for Python QtCore reference lists it among exported functions. The Qt render backend and tests remain byte-identical; Windows still needs to execute them.

---


V6 Windows evidence `E4C_DRILL_VISUAL_PIXEL_CONSUMER_V6_20261111T004628_177cd6f5` proves the installer passed ZIP SHA, rollback implementation, PS AST, stage-root contract, inventory (23 rows/24 members), 18 typed operations, support/design pins, exact operator decisions, 18 destination states and stage source roots. It then stopped because the bundled V15 runner guide did not contain the literal `No new Python dependency` anchor. V15's current Qt section semantically disallowed Pillow/RAQM/pip/environment mutation, but an older V14 section still prescribed the Pillow pin and operator installation, so the guide was internally contradictory. `INSTALL_FAILURE.json`: `stage=STAGED_VALIDATION`, `journal=[]`, `rollback_status=NOT_NEEDED`; no transaction.

V7 corrects this documentation/validator defect. Guide V16 states the exact no-new-Python-dependency rule and explicitly supersedes the old V14/V5 Pillow guidance. V7 changes installer references/version identity and docs only. Consumer Qt module, 35 rewritten tests and E1 service postimage remain byte-identical to V6. Windows Qt runtime probe, py_compile 3/3 and 35/35 tests remain unexecuted and must pass before transaction.

---

## V6 architectural correction — reuse Qt; reject Pillow runtime mutation (2026-11-11)

The V4 evidence proved that the canonical Python process lacked `PIL`. The assistant then incorrectly directed the operator to install Pillow into the shared Producer interpreter. The installation command succeeded, but the subsequent probe failed with `SyntaxError` because PowerShell removed nested quotes from the inline Python source. This does not establish RAQM status. The user's objection to changing the shared environment is correct. Remove only the accidentally installed Pillow package; preserve PySide6 and all other packages.

V6 removes Pillow/RAQM and converts the D-owned image API and tests to PySide6 Qt, already required by the existing Producer. The new backend uses in-memory RGB888 `QImage`, `QPainter`, `QFontDatabase`, `QFontMetricsF`, `QFontInfo` and `QRawFont`. Exact font/proposal/decision pins and approved geometry/timebase remain unchanged. `Qt.SmoothTransformation` is the new contained image interpolation path; it must not be described as Pillow Lanczos. This is a new backend; all 35 tests must pass on active Windows before transaction.

## V5 dependency finding and disposition — 2026-11-11

Consumer logic is unchanged from V4. The Windows evidence shows the canonical Python 3.13.14 process can start but cannot import `PIL`; no visual test ran in that V4 attempt. The previously passing reference stage used Python 3.13.5 + Pillow 12.3.0 + RAQM. V5 declares `Pillow==12.3.0` in a D-owned requirements file and requires operator-managed installation into the same Python executable used by Producer. This avoids a test-only venv that would not be available to the real GUI. The installer only verifies the dependency; it never runs pip.

# C11-E E4C Drill visual consumer — implementation and validation findings V6

**Date:** 2026-11-10  
**Forensic baseline:** `ChallengeEngineV01_STATELESS-C11-E-V121-NIGHTLY.zip` (read-only; not extracted over checkout).  
**Active Windows checkout:** remains sole authority.

## Accepted source/design baseline

- A.3 V5 install receipt SHA `d39eec2b3c1d969a3cb0d4e6aaa14b87aadcba74e42e58d283e00ea50768e881`; 3 replacements +26 additions, 13 support pins, staged changed tests 33+5+7+10 and py_compile 8/8.
- E4C binder V2 active Windows receipt `31f631c3c23c6c1d277d67f52dd887010ee51be869798ab8db3fbdec8658fa01`; Godot console V3 receipt `526c7d360863af8fb53707c9c83162173f4c1f1eb349ee8d767fb97665167a31`.
- Geometry/timebase decisions are approved as proposed by exact record SHA `eb95da188065b8ebcb2371e2a6bcff6762ce000a5ca74f8ea384ecec4ee58303`.

## Source audit against V121-NIGHTLY

The snapshot's E1 service preimage is 77,346 bytes / SHA `5dc15d355b86758a24ff0772e75ea1a889fd59503b1632ea26821856a08935dc`, exactly the V2/V3 replacement preimage. The installed source phase audit V2 is present at its canonical `docs/current/e/` path and SHA `2a47a8db68c458c237eeceae1d35cef8bceecb9049ce5cf6067ee905190ccddc`. The A.3 V5 receipt exists inside the nightly archive and hashes to the receipt SHA above.

The E1 service successor SHA is `e5dbf9baa72d4c066ff8ba24006df954700d72a5b0f11f9f88aec653e84dce87`. Its focused diff adds exact A.3 bridge validation, includes all eight native phase/ownership sources as read-only pins, carries lineage resolution into the Drill phase contract and requires the approved bridge status before accepting the visual-consumer contract. It does not change C11-C mechanics or the frozen manifest.

## D-owned consumer and test payload — unchanged

- Consumer module SHA `e1e78a00d7d9384f7b99e9da16c7388be59a239bbcd8d1d9de44a881b68d3a03`.
- Test module SHA `15c417555382ff397991e4402dc313708ab17d29df78d4cbcd97d96b4a31609a`.
- Test suite: 35 tests; 20 E1-prepared synthetic GAME pixel samples cover all 20 selectors.
- Local isolated result: 35/35 PASS; Python 3.13.5, Pillow 12.3.0, FreeType and RAQM. Synthetic sample SHA `11cb5dbbc58c6ba9974a077aceaf8b3b9a3196e75389fe92c48558fa2e5fafbb`. This is not actual C11-C source-frame, Qt GUI, A/V or human evidence.

## Operator-reported Windows installer failures

**V1:** Run `E4C_DRILL_VISUAL_PIXEL_CONSUMER_V1_20261110T230315_e5929ed8`; ZIP/AST/inventory/support/design pins passed, then PACKAGE_PREFLIGHT failed because the guide V12 was missing. V1 omitted the required guide from its 16 operations; no transaction occurred.

**V2:** Run `E4C_DRILL_VISUAL_PIXEL_CONSUMER_V2_20261110T232426_a8472872`; ZIP SHA, AST, 23-member inventory, 18 typed operations, 13+10 pins, exact decisions, 18 destination states and short staging all passed. STAGED_VALIDATION then failed because the guide wording did not contain the exact heading `hash-guarded rollback`. The guide already specified expected-postimage matching and exact-preimage restore; the installer was stricter on literal phrase than the human-readable policy. The failure JSON records an empty journal and `rollback=NOT_NEEDED`.

## V3 corrective delta — superseded before Windows

The V3 package was rebuilt against the V121 source state, not the older V109 context. It:

1. Adds the exact explicit `Hash-guarded rollback` heading to guide V12 while preserving and clarifying its postimage/preimage/unknown-state rules.
2. Adds source-structure checks proving Rollback-Transaction still matches the expected postimage, validates the backup against exact preimage, refuses unknown destination bytes and atomically restores only a verified backup.
3. Moves current continuity prompts to the active root `prompts/` directory and updates all current docs from the V121 baseline; A.3 V5 is recorded as closed.
4. Preserves E1 service, consumer and 35-test source bytes from V2 unchanged; no accepted suites are repeated.

## V4 staged-source closure and acceptance boundary

The V4 installer has not yet been executed on active Windows. Its PowerShell 5.1 AST, Python/Pillow/RAQM probe, compile, 35-test staged suite and install receipt remain pending. The faithful replay on the complete V121 reconstructed stage passed py_compile 3/3 and tests 35/35 locally; this is not Windows acceptance, captured C11-C frames, Qt GUI evidence or human review. No E1 consumer connection, C11-C render, Godot, FFmpeg, media or audio was invoked here.

## V4 staging dependencies

The consumer test's E1 intent preparation traverses pre-existing source assets and D9.9/D9.10 contracts. The stage must mirror the required roots `challenges/`, full `assets/`, `docs/current/d/`, `docs/current/e/`, `docs/history/c11e/`, `definitions/`, `profiles/`, `release/`, `core/`, `tools/`, and `c11c-suite/c11c-producer/`. V3 had omitted the first three. V4 adds all three to source path-budget checking and read-only stage copy, asserts their existence before Python, and logs `STAGING_SOURCE_ROOTS=PASS_CHALLENGES_ASSETS_DOCS_CURRENT_D`. This changes only pre-write stage copy/verification; the 35-test module and E1/consumer source bytes remain unchanged.


## V4 package and staged validation record

V4 includes 18 typed operations (one E1 service REPLACE and 17 D-owned ADDs), 13 support pins and 10 approved design/font pins. The package identity checks style guide V13, decision docket V7, phase-ownership audit V2 and incident register V4. V4 is pending active Windows execution; do not infer installation from local replay.
