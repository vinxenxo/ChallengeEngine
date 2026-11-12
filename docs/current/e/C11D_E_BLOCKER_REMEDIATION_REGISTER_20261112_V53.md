# CURRENT BLOCKER REGISTER OVERRIDE — locale blocker resolved; CLI and matrix qualification open — 2026-11-12

## Resolved: D-to-C11-C locale decimal argument defect
The V1.4 invariant-culture wrapper is installed and exercised successfully in the accepted GUI A/V pilot `D99-GUI-6514F1066E79`. The tracking tier-1 speed multiplier reached the unchanged C11-C launcher as a valid value; native capture completed. Mark the previous `0.75` → `0,75000` → `75000` incident **CLOSED_PASS_GUI_SINGLE_SELECTOR**. Do not reopen absent contrary evidence or source-pin drift.

## Remaining acceptance blockers (not known code defects)
- `E4C-CLI-AV-001`: CLI-origin execution has not yet been exercised end-to-end. Run the add-only CLI smoke runner with fresh request ID; preserve its receipt.
- `E4C-AV-MATRIX-001`: full 20-selector family A/V matrix remains pending. Count GUI pilot `tracking/tier-1` as row 1; only 19 rows remain after CLI smoke.

No active GUI A/V defect is evidenced by the accepted pilot. The GUI path passed the full C11-C silent capture → D composition → FAMILY_MUSIC_V4 → FFmpeg/FFprobe → stream-isolation chain. Keep E4C OPEN until CLI and 20/20 matrix gates pass.


**Current E4C position (2026-11-12):** the first single-selector GUI A/V qualification is accepted for `visual_drills / tracking / tier-1`. The operator confirmed visual and listening review PASS. Evidence `D99-GUI-6514F1066E79-production.zip` SHA-256 `5fb910dd7515ca1f80f2fa77a0829836613e933ca7106f00852ccd31d797f8e4`; tests/plan bundle `D99-GUI-6514F1066E79-tests.zip` SHA-256 `5c94ad64666548db478a4265a71345efe28c2a346f215e7cdb477f51dc8dde91`; qualification receipt SHA-256 `d8aad7176ed99d8bc0c067cece58272c5ac44045d55d746c768ea72324d459db`; RUNNING receipt SHA-256 `2f9b388b3541548d79c254161290ad73241109349aea1f57c1ac9c10e092ab2a`. The receipt status is `PASS_E4C_DRILL_SINGLE_SELECTOR_A_V_QUALIFICATION`.

**Independent audit:** 91/91 E1 source pins are identical at pre-execution, immediately-pre-render and post-execution; GUI/CLI E1 semantic identity parity PASS; 810/810 frames composed at 30 fps; phases PRE_ROLL/GAME/END_CTA = 90/630/90 frames; GAME editorial fields are populated and D-composed. `FAMILY_MUSIC_V4` `FLOWING_VECTOR` produces 27s, 44.1 kHz stereo PCM16; A/B seed 840001 WAV SHA `e54b960c799102fb104a99ccd7b94c4a41b5b22d54665acda72106b36646f277` is identical, C seed 840002 WAV SHA `5e81b6426f7915c7cad4c658fc24b90cd17c870a4497f45136a53e43b71efd40` differs. Final A and C are 27s, H.264 High 720×1280 yuv420p TV, 30 fps, 810 frames; AAC-LC 48 kHz stereo; both start at 0. Receipt stream hashes prove video A/C identical and audio A/C different; independent extraction also confirms raw H.264 SHA `500fc010b0d39062997d73643643943d03552082d75a2b8db6c55a3bbe5ad150` matches, while AAC elementary stream SHA differs (`23162fb059ca5e215758d6bbd58b6baba0efc9bd13e94d5921fd96726e19cd67` vs `f98747cc8f408521a3d00e7f4d90a066f3adf366de46d6f89bfefb65e26e86cd`). Final A SHA `7604f69e7c28e044a4bdb7fccc76c74604495ec9bbe4b46fcbca23a62b7c49ba`; final C SHA `d93753dabcfd85f3a3e721125081a649fbfa3a033a751e77a39df4c38357bf84`. Native source SHA `d10950bca9358de4ffe8a9f4f24c8c35cdb37e25050775a9220a4d15ffb45338`; silent D-composed intermediate SHA `60fd3155e70691bb7f2e636d20539e5898554669503888ee34bb78402c9589ad`.

Governance: C11-C frozen manifest remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; `c11c_source_mutation=false`; D3 V5 not invoked; source C11-C audio remains disabled via `-NoSound`; renderer invocation is solely the explicitly authorized isolated E4C qualification scope; `production_dispatch=false`; `release_authority=NONE`. E1 stays `PREPARE_ONLY`, `family_adapter.status=NOT_CONNECTED_E1`. Do not turn these isolated test results into production dispatch or release authority.

**Next gates:** (1) CLI-origin A/V smoke through the existing CLI facade with `--execute-drill-av --origin CLI`, using the same shared D executor and a fresh request ID; (2) 20-selector family A/V matrix; count the accepted GUI `tracking/tier-1` pilot as matrix row 1 and do not rerun it for matrix coverage; (3) E4C closeout only after CLI smoke, all remaining 19 selectors, receipts, human review and source-pin integrity. Then E5 → E6 Smoke18 → E7 Matrix101 (CH_008/009 held; 99 provisional) → E8 historical C-to-E regression, independent acceptance, freeze and separately authorized promotion.

---

## Superseded prior revision content

## Active blocker
The installed shared adapter reaches the native C11-C launcher but supplies a locale-formatted decimal multiplier. In `D99-GUI-85201B7B4FF7`, tier-1 tracking profile value `0.75` became PowerShell argument `75000`; the launcher correctly rejected it against `[ValidateRange(0.1,3.0)]`. The `Resolver + Plan` run passed; this is strictly the second A/V execution step. No native capture or media was produced.

## Remediation and next gate
Use the V1.4 overlay: invariant ASCII speed string → PowerShell wrapper parses with `InvariantCulture` → typed `System.Double` reaches unchanged C11-C launcher. Installer must run an `es-ES` dummy-launcher round-trip and require recorded `0.75`, plus 16/16 Python tests, `py_compile`, exact pins and transaction preflight before writes. Preserve the failed D99 output root; retry with a fresh request ID. Do not repeat Binder/native captures/100-of-100 pixel QA.



## D99-GUI-85201B7B4FF7 — single-selector A/V pilot diagnosis — 2026-11-12

**Authoritative evidence:** `D99-GUI-85201B7B4FF7.zip` SHA-256 `0913179f9852b7b1f75c2a7e2f763a111bc8d807d08d20036a2891ae94661f56`; `D99-GUI-85201B7B4FF7-tests.zip` SHA-256 `16f0e199429deffb85025cd35d0cfd4fe2ec9fe237cf66482f6de6b14cd6ef23`.

The GUI's **Resolver + Plan** stage is successful, not a failure: E1 receipt is `PASS_E1_PREPARATION_ONLY`; GUI/CLI semantic parity is `PASS`; D9.10 bridge planning is `PASS_BRIDGE_PLANNING_ONLY`; D composition plan is valid with real GAME-visible editorial; the request is `visual_drills / tracking / tier-1`, gameplay seed `12345`, music seed `840001`, `REVIEW_720`. This remains deliberately plan-only at E1 and does not claim renderer or dispatch activation. The second GUI action, the shared D A/V executor, fails before the native C11-C producer starts.

Exact failure from `logs/c11c_drill_producer.log`: C11-C's `run_visual_drill_production.ps1` rejects `-SpeedMultiplier` because it receives `75000`, outside `[ValidateRange(0.1,3.0)]`. The pinned profile `profiles/difficulty/visual_drill_tracking.json` has tier 1 `speed_multiplier=0.75` (source SHA-256 `6de8812bd46904e122ecdd0eae22fb2979bd75399c34779248c6569e833c921e`). The adapter applied Python's host decimal separator and sent `0,75000`. On the operator's locale, Windows PowerShell 5.1 parameter binding split/coerced that comma decimal and delivered `75000`. This is a cross-locale numeric argument-boundary defect in the D adapter, not a defect in the pinned C11-C launcher or difficulty profile.

The failure occurs before a successful C11-C capture. There is no native MP4, no D frame composition, no FAMILY_MUSIC_V4 WAV generation, no mux, and no final FFprobe result in this run. The failure does not indicate an editorial, font, Qt, geometry, phase/timebase, music determinism, or A/V stream-equivalence defect. The first evidence bundle contains `RUNNING` and `FAILURE` receipts and the exact native producer log. The `-tests.zip` is a preparation/parity/contract receipt bundle; it does not show a second independent A/V failure. Do not infer additional failures from its intentionally plan-only receipts.

**V1.4 correction:** remove host-locale formatting entirely. Python emits an ASCII invariant string such as `0.75000` to a string-typed PowerShell wrapper. The wrapper parses it with `[System.Globalization.CultureInfo]::InvariantCulture`, sets the wrapper thread culture to invariant for the call, then invokes the existing pinned C11-C launcher with an already-typed `[double]$speed`. The native C11-C launcher remains byte-identical and receives `0.75`; C11-C stays silent via `-NoSound`. The wrapper is retained in the run logs and its hash/argument are written into the execution receipt. Regression tests cover invariant formatting, wrapper parse/type handoff, and absence of host-locale formatting. The V1.4 installer additionally executes this exact wrapper against a dummy parameter-compatible launcher while forcing `es-ES`, and requires the dummy to record `0.75` before any repository mutation.

The failed output root `artifacts/production/c11e/D99-GUI-85201B7B4FF7` is intentionally preserved. It must not be overwritten. The retry must use a **new unique request_id/output root** (generate a fresh GUI request and repeat Resolver + Plan); do not delete or recycle this failed evidence. After V1.4 installation PASS: audit its postimages/source pins, rerun the GUI plan stage with a fresh ID, then execute only `tracking/tier-1`. Continue only when native capture, D composition, FAMILY_MUSIC_V4 A/B/C, final A/C video/audio stream hashes, FFprobe, and human visual/listening review pass. CLI smoke/parity follows on the same shared adapter. Do not start the 20-selector A/V matrix until the single-selector result is accepted.

Governance is unchanged: E1 `PREPARE_ONLY`; `family_adapter.status=NOT_CONNECTED_E1`; `production_dispatch=false`; `release_authority=NONE`; no Git checks; commits operator-managed; C11-C frozen manifest SHA remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.


---

# CURRENT BLOCKER OVERRIDE — E4C SHARED A/V ROUTE — 2026-11-11

## Open items

- Shared execution adapter package is built as a qualification candidate; it is not yet installed on active Windows.
- Existing Producer GUI smoke and existing CLI `--execute-drill-av` smoke are pending.
- One-selector native A/V is pending: `tracking/tier-1`, C11-C silent source, D composition, FAMILY_MUSIC_V4 seed separation, FFmpeg/FFprobe and human review.
- 20-selector A/V expansion remains pending and must follow single-selector acceptance.

## Controls in the candidate

- E1 stays `PREPARE_ONLY` and `family_adapter.status=NOT_CONNECTED_E1`.
- D adapter requires visible editorial content; personalization ON alone cannot pass.
- All E1 source pins are checked before work, immediately before native C11-C capture, and after work.
- Native C11-C source capture is invoked `-NoSound`; FAMILY_MUSIC_V4 takes only `request.music_seed`; D3 V5 excluded.
- No mutation to frozen C11-C generators/mechanics/binders/timelines/audio/RNG/manifest; no sixth module or parallel Producer/binder/service.
- Renderer activation is scoped to the explicitly authorized isolated E4C qualification; general production dispatch remains false and release authority remains NONE.

Failures are fail-closed; preserve logs and receipts. E4C is not considered closed until Windows execution and operator review pass.

---

## V9 current blocker state — E4C Drill visual consumer (2026-11-11)

V8 failed before transaction because StrictMode inspected `$testSource` before initialization. V9 fixes assignment order. V8 journal was empty and rollback was not needed. Consumer acceptance remains open; no consumer package V1–V8 transaction occurred.

---

## Current blocker — V6 runner-guide policy mismatch (2026-11-11)

## V8 current state — 2026-11-11

V7 failed closed in `STAGED_VALIDATION` before transaction. Its installer imported `QT_VERSION_STR` from `PySide6.QtCore`; the canonical PySide6 runtime does not export that symbol. This is an installer probe defect, not evidence that PySide6, Qt, QImage or QPainter is missing. The preceding imports of `PySide6.__version__` succeeded. `journal=[]`; `rollback=NOT_NEEDED`; no checkout write occurred.

V8 changes the probe to `from PySide6.QtCore import qVersion` and records `qVersion()` as the Qt runtime version. It requires Qt 6.x, alongside Python 3.13.x, existing PySide6 6.8–6.x, non-null RGB888 QImage and active QPainter. The official Qt for Python API lists `qVersion()` as a QtCore function. V8 does not install, upgrade or uninstall packages, invoke pip, edit requirements, or mutate the shared Python environment.

The consumer, its 35 Qt tests and the E1 service replacement are byte-identical to V7. No functional test result is inferred from the failed V7 runtime probe. V8 must still pass Windows PowerShell 5.1 AST, inventory/pins/destinations/staging, runtime probe, `py_compile` 3/3, all 35 Qt tests and immediate pre-transaction checks before any write. Do not repeat accepted A.3, binder V2, Godot V3, Loop22 or historical Drill authoring.

Governance remains unchanged: C11-C frozen manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; renderer OFF; dispatch/media/audio OFF; `release_authority=NONE`; operator manages commits; Git checks skipped.

### V7/V8 probe incident
Root cause is the invalid `QT_VERSION_STR` import in the installer, not a missing or broken Qt runtime. Remediation uses supported `PySide6.QtCore.qVersion()` and validates Qt 6.x. Keep the gate open until Windows executes all new Qt tests.

---


V6 reached staged validation after all package, rollback, AST, pin, decision, destination and staging checks. It failed because guide V15 did not contain the exact `No new Python dependency` anchor required by the installer. The guide's top V15 rules already prohibited Pillow/RAQM and environment mutation, but an inherited V14 section still described the superseded Pillow pin/provisioning. This is a documentation/validator consistency defect, not a Qt runtime failure. Evidence run `E4C_DRILL_VISUAL_PIXEL_CONSUMER_V6_20261111T004628_177cd6f5`: `journal=[]`, `rollback=NOT_NEEDED`, no transaction.

V7 candidate advances guide V16 with the exact normative phrase and removes the contradictory active Pillow instructions by explicitly marking them superseded. No consumer, E1 service, test, pin or approval changes are made. V7 still requires active-Windows Qt probe, py_compile 3/3 and 35/35 before writes. No new Python dependency, pip, requirements edit or shared environment mutation is allowed.

---

## Current blocker — E4C consumer must reuse existing Qt runtime (2026-11-11)

**ID:** E4C-VC-QT-001  
**State:** OPEN / QT_BACKEND_REQUALIFICATION_REQUIRED.  
**Correction:** The prior Pillow remediation was rejected as an architectural mistake. The operator was instructed to install Pillow globally; Pillow==12.3.0 was installed successfully, but the subsequent Python `-c` verification failed because PowerShell stripped nested quotes. Do not retain this dependency. Remove only that accidentally added Pillow package from the canonical Python 3.13 interpreter and verify `importlib.util.find_spec('PIL')` returns `None`.

The consumer is being migrated to the existing PySide6 already declared by the Producer. No new package, pip operation, requirements edit or global environment mutation is authorized. V6 is a new Qt rendering backend; its 35 tests must run on Windows before any transaction. Existing accepted binder/A.3/Loop/Godot gates remain closed and are not repeated. Renderer OFF; dispatch/media/audio/release OFF.

## Current blocker — E4C consumer runtime dependency (2026-11-11)

**ID:** E4C-VC-PILLOW-001  
**State:** OPEN / OPERATOR_ENVIRONMENT_PREREQUISITE  
**Root cause:** the canonical project Python 3.13.14 executable starts correctly but lacks the `PIL` module. The V4 runtime probe exited with `ModuleNotFoundError: No module named 'PIL'`; RAQM was not reached.  
**Evidence:** `e4c_drill_visual_pixel_consumer.zip`, run `E4C_DRILL_VISUAL_PIXEL_CONSUMER_V4_20261111T001315_ed8f8d25`. All 18 prior operations checks passed; `journal=[]`, rollback `NOT_NEEDED`, no checkout write.  
**Remediation:** manually install exact D-owned dependency `Pillow==12.3.0` into the same Python 3.13 runtime used by Producer; verify RAQM true; then run V5 with explicit `-PythonExe`. No dependency installation is automated.  
**Protection:** do not edit C11-C/root requirements; no renderer, dispatch, media, audio or release authority.

# C11-D / C11-E Blocker Remediation Register — V45 (2026-11-11)

| ID | Gate / issue | State | Required closure |
|---|---|---|---|
| E4C-A3-LINEAGE | D9.8 lineage pointer and review-manifest bridge | CLOSED_PASS_ACTIVE_WINDOWS | A.3 V5 receipt `d39eec2b3c1d969a3cb0d4e6aaa14b87aadcba74e42e58d283e00ea50768e881`; 3 replacements +26 adds; suites 33+5+7+10; py_compile 8/8. No rerun. |
| E4C-DRILL-SOURCE | Native Drill phase and ownership | PASS_READ_ONLY | Phase audit V2, 8 exact C11-C pins /12 checks; preserve native header/footer and END_CTA CTA. |
| E4C-DRILL-GEOMETRY | D outer-band composition | APPROVED_AS_PROPOSED | Exact geometry SHA approved for D-owned design/contract and isolated pixel scope only. |
| E4C-DRILL-TIMEBASE | GAME payload → final-presentation frame mapping | APPROVED_AS_PROPOSED | Exact timebase SHA approved for D-owned design/contract and isolated pixel scope only. |
| E4C-DRILL-CONSUMER | Consumer V4 install and 35-test Windows stage | PENDING_ACTIVE_WINDOWS_V4 | Local faithful V121 stage passes py_compile 3/3 and 35/35; Windows PS5.1 AST/runtime/tests/receipt required before write. |
| E4C-GUI | Existing Qt Producer GUI runtime | OPEN | Observe actual GUI route through existing shared E1 service; verify GUI/CLI parity. |
| E4C-DRILL-AV | Native family music, mux and human review | NOT_QUALIFIED | Silent protected C11-C capture; existing `FAMILY_MUSIC_V4`; independent seeds; FFmpeg/FFprobe; human review. D.1 is envelope only. |
| E5 | Cross-family determinism/seed isolation/profile non-leakage/GUI-CLI parity | PENDING | After E4C family closeout. |
| E6 | Smoke18 | PENDING | Six complete A/V scenarios per family. |
| E7 | Matrix101 | PENDING_SCOPED | 54+27+20 target; CH_008/009 held, 99 provisional. |
| E8 | Historical C-to-E regression, independent acceptance, freeze/promotion | BLOCKED | Complete E7, independent acceptance and separate explicit authority. |

## Current package failures and control

- Consumer V1: pre-transaction fail; missing required guide V12 from package.
- Consumer V2: pre-transaction fail; exact rollback heading absent from staged guide despite equivalent semantics; empty journal, `rollback=NOT_NEEDED`.
- Consumer V3: superseded before Windows; faithful stage replay found missing read-only test roots `challenges/`, full `assets/`, `docs/current/d/`.
- Consumer V4: prepared; includes the three path-budgeted/copied roots, stage-root assertions, explicit rollback policy and implementation inspection. Windows acceptance pending. Only 18 manifest operations can transact; copied roots are staged read-only test inputs.

Operator geometry/timebase record SHA `eb95da188065b8ebcb2371e2a6bcff6762ce000a5ca74f8ea384ecec4ee58303`. C11-C 2.19.12 remains sole production authority; renderer OFF; dispatch/media false; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`.


## E4C CLI smoke installer blocker — V1.5 / V1.6 (2026-11-12)
V1.5 failed closed before transaction at staged Python tests with `PYTHON_TIMEOUT: ;`; journal empty and no project writes. V1.6 addresses argument binding and stdin lifecycle in installer only. Blocker remains OPEN until V1.6 passes actual Windows PS 5.1 installation and the CLI A/V smoke receipt is accepted.
