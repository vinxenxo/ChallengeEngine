# C11-E E4C DRILL EXECUTION PLAN V31 — 2026-11-13

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

## Superseded document baseline (C11E_E4C_DRILL_EXECUTION_PLAN_20261112_V29.md)

The following content is retained for traceability; the authoritative state and next action are defined in the update above.

# C11-E E4C V2.2 PIN-ALIGNMENT R1 — CURRENT AUTHORITATIVE STATE (2026-11-13)

**This block supersedes all earlier E4C V2 installer instructions below.** Older V1.7–V2.2 incidents remain historical evidence; do not rerun superseded packages.

## Operational execution plan

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

# E4C DRILL EXECUTION PLAN OVERRIDE — GUI A/V pilot PASS; CLI smoke and matrix remaining — 2026-11-12


## Authoritative installer correction — V1.8 package-binding failure / V1.9 consolidated recovery (2026-11-12)

The operator's V1.8 run passed the ZIP sidecar and entered the package installer, then failed closed at `OPERATION_PACKAGE_FILE_BINDING_FAIL` for `docs/current/e/C11D_E_BLOCKER_REMEDIATION_REGISTER_20261112_V54.md`. The V1.8 builder renamed physical documentation payloads to the next versioned filenames (for example V55) but failed to regenerate the matching `replacements`/`additions` destination rows; several operation destinations still referenced their predecessor names. The validator correctly rejected the mismatch before the transaction journal or destination writes. This was a package-manifest construction defect, not a Windows runtime issue. Do not rerun V1.8.

V1.9 is a complete rebuilt overlay. Its operation rows are generated directly from the physical payload tree: `payload/replace/<relative>` maps only to `REPLACE <relative>`, and `payload/add/<relative>` maps only to `ADD_ONLY <relative>`. The installer independently enforces that mapping for every operation, verifies one-to-one closure between all payload files and operation rows, rejects duplicate package paths and destination paths, and checks manifest counters against actual arrays. The V1.9 matrix is exactly one existing D-consumer replacement plus 23 add-only destinations (24 mutation operations); package inventory also includes the README and installer. All versioned current-doc and prompt destinations now match their package paths exactly.

V1.9 preserves the V2 consumer, 18 focused tests, requalifier, runner, 21 support pins and 91-pin/CLI source evidence unchanged. The only changes from V1.8 are installer/manifest construction integrity, corrected operation destinations, documentation/prompt version increments, and incident recording. The V1.8 attempt failed before transaction; no checkout destination mutation occurred. V1.9 remains `NOT_YET_INSTALLED` pending its Windows 5.1/Python 3.13/PySide6 preflight and transaction receipt.

The V1.9 installer also reports pre-transaction failures distinctly as `FAIL_CLOSED_PRE_TRANSACTION_NO_DESTINATION_WRITES` with a `%TEMP%` diagnostic, rather than labelling an empty journal as a completed rollback. No Git, pip, shared dependency, GUI/CLI, E1, C11-C, dispatch or release changes are permitted.



## Authoritative update — V1.7 installer incident and V1.8 correction (2026-11-12)

V1.7 failed closed at `DESTINATION_PREFLIGHT` because it misclassified the newly introduced `tests/test_c11e_e4c_drill_visual_composition_consumer.py` as a replacement. The destination was absent in the active checkout. The declared preimage SHA `aedeb5754d94fdbaad134a653f57ca07466c845dcef081c8774668245455a7a0` is actually the historical V9 test stored under `tools/c11d/d9/`, not a preimage at the new `tests/` path. This is a manifest/installer classification defect, not a V2 consumer failure. The failure occurred before evidence-root and transaction-journal initialization; no destination writes or repository mutations occurred. Its generic `FAIL_CLOSED_ROLLBACK_COMPLETE` message reflects a zero-entry/no-op rollback.

V1.8 supersedes V1.7 and is the only candidate permitted for installation. Its operation matrix is exactly one hash-guarded replacement (`tools/c11d/d9/c11e_e4c_drill_visual_composition_consumer.py`) plus 22 `ADD_ONLY` destinations, including the new test module. The installer asserts the exact classification, unique operation destinations, and uses manifest-resolved package paths for staged inputs. It rechecks all source pins and all destination states before journaling/writing. Do not rerun V1.7. No source, GUI/CLI, E1 service, executor, C11-C or shared dependency changes are included.

V1.8 install status: `NOT_YET_INSTALLED`. Do not claim V2 Windows qualification from package/static checks. After install PASS, reuse the already accepted CLI native MP4 and WAV A/B/C for the existing-media V2 requalification; no new C11-C capture or music generation. E4C remains open, V2 A/V acceptance pending operator review, matrix not started. C11-C remains sole production authority; E1 PREPARE_ONLY / NOT_CONNECTED_E1; dispatch false; release authority NONE.

## Accepted single-selector GUI A/V execution
Request `D99-GUI-6514F1066E79` is the accepted pilot for `tracking/tier-1`. Evidence hashes and the complete audit are recorded in `docs/history/c11e/C11E_E4C_DRILL_GUI_SINGLE_SELECTOR_AV_ACCEPTANCE_20261112_V1.md`. The operator visual and audio review is explicitly PASS. Independent stream extraction confirms identical H.264 A/C and different AAC A/C; 91 pins remained unchanged at all three checkpoints.

## Next action: CLI A/V smoke
Use `tools/c11d/d9/RUN_C11E_E4C_DRILL_CLI_SMOKE_V1.ps1`. Baseline request: `artifacts/production/c11e/D99-GUI-6514F1066E79/request.json`. The runner clones it to a new request ID, changes provenance origin to CLI, preserves selector/seeds/editorial, checks 19 source pins pre/post, and invokes the already-installed `c11c-suite/c11c-producer/c11e_production_cli.py` with explicit `--origin CLI --execute-drill-av`. It calls the same `c11e_e4c_drill_execution.py`; there is no second execution engine. Do not overwrite the accepted GUI run.

Require CLI receipt status `PASS_E4C_DRILL_SINGLE_SELECTOR_A_V_QUALIFICATION`, `request_origin=CLI`, shared executor identity, E1 semantic parity PASS, 91 source pins unchanged, A/B WAV equality, C WAV distinct, H.264 A/C equality, AAC A/C difference, final FFprobe and `release_authority=NONE`. Operator visual/audio review is required for the CLI artifact.

## 20-selector matrix policy
The accepted GUI `tracking/tier-1` run counts as matrix selector 1/20. The CLI smoke is an entrypoint gate, not an additional unique selector. After CLI smoke, run only the remaining 19 combinations: four families (`tracking`, `pursuit`, `saccade`, `peripheral_scan`) × five tiers (`tier-1` through `tier-5`), excluding the already accepted tracking/tier-1 row. Each row needs a fresh request ID and isolated output root. Keep gameplay/music seed domains separate; family-specific FAMILY_MUSIC_V4 mapping must match the pinned registry; do not use D3 V5 or embedded gameplay-seeded C11-C audio.

A matrix row passes only when native capture, D composition, editorial phase visibility, source-frame/timebase identity, FAMILY_MUSIC_V4 A/B/C, final A/C stream isolation, FFprobe and source pins pass. Preserve every receipt and failed artifact. Do not batch-delete or overwrite any prior output. Human review must cover all 20 final outputs or a formally documented sampling strategy accepted by the operator; absent that acceptance, require full review.


**Current E4C position (2026-11-12):** the first single-selector GUI A/V qualification is accepted for `visual_drills / tracking / tier-1`. The operator confirmed visual and listening review PASS. Evidence `D99-GUI-6514F1066E79-production.zip` SHA-256 `5fb910dd7515ca1f80f2fa77a0829836613e933ca7106f00852ccd31d797f8e4`; tests/plan bundle `D99-GUI-6514F1066E79-tests.zip` SHA-256 `5c94ad64666548db478a4265a71345efe28c2a346f215e7cdb477f51dc8dde91`; qualification receipt SHA-256 `d8aad7176ed99d8bc0c067cece58272c5ac44045d55d746c768ea72324d459db`; RUNNING receipt SHA-256 `2f9b388b3541548d79c254161290ad73241109349aea1f57c1ac9c10e092ab2a`. The receipt status is `PASS_E4C_DRILL_SINGLE_SELECTOR_A_V_QUALIFICATION`.

**Independent audit:** 91/91 E1 source pins are identical at pre-execution, immediately-pre-render and post-execution; GUI/CLI E1 semantic identity parity PASS; 810/810 frames composed at 30 fps; phases PRE_ROLL/GAME/END_CTA = 90/630/90 frames; GAME editorial fields are populated and D-composed. `FAMILY_MUSIC_V4` `FLOWING_VECTOR` produces 27s, 44.1 kHz stereo PCM16; A/B seed 840001 WAV SHA `e54b960c799102fb104a99ccd7b94c4a41b5b22d54665acda72106b36646f277` is identical, C seed 840002 WAV SHA `5e81b6426f7915c7cad4c658fc24b90cd17c870a4497f45136a53e43b71efd40` differs. Final A and C are 27s, H.264 High 720×1280 yuv420p TV, 30 fps, 810 frames; AAC-LC 48 kHz stereo; both start at 0. Receipt stream hashes prove video A/C identical and audio A/C different; independent extraction also confirms raw H.264 SHA `500fc010b0d39062997d73643643943d03552082d75a2b8db6c55a3bbe5ad150` matches, while AAC elementary stream SHA differs (`23162fb059ca5e215758d6bbd58b6baba0efc9bd13e94d5921fd96726e19cd67` vs `f98747cc8f408521a3d00e7f4d90a066f3adf366de46d6f89bfefb65e26e86cd`). Final A SHA `7604f69e7c28e044a4bdb7fccc76c74604495ec9bbe4b46fcbca23a62b7c49ba`; final C SHA `d93753dabcfd85f3a3e721125081a649fbfa3a033a751e77a39df4c38357bf84`. Native source SHA `d10950bca9358de4ffe8a9f4f24c8c35cdb37e25050775a9220a4d15ffb45338`; silent D-composed intermediate SHA `60fd3155e70691bb7f2e636d20539e5898554669503888ee34bb78402c9589ad`.

Governance: C11-C frozen manifest remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; `c11c_source_mutation=false`; D3 V5 not invoked; source C11-C audio remains disabled via `-NoSound`; renderer invocation is solely the explicitly authorized isolated E4C qualification scope; `production_dispatch=false`; `release_authority=NONE`. E1 stays `PREPARE_ONLY`, `family_adapter.status=NOT_CONNECTED_E1`. Do not turn these isolated test results into production dispatch or release authority.

**Next gates:** (1) CLI-origin A/V smoke through the existing CLI facade with `--execute-drill-av --origin CLI`, using the same shared D executor and a fresh request ID; (2) 20-selector family A/V matrix; count the accepted GUI `tracking/tier-1` pilot as matrix row 1 and do not rerun it for matrix coverage; (3) E4C closeout only after CLI smoke, all remaining 19 selectors, receipts, human review and source-pin integrity. Then E5 → E6 Smoke18 → E7 Matrix101 (CH_008/009 held; 99 provisional) → E8 historical C-to-E regression, independent acceptance, freeze and separately authorized promotion.

---

## Superseded prior revision content

## D99-GUI result
The plan/prepare GUI path passed (E1 PREPARE_ONLY, GUI/CLI semantic parity, D composition plan, visible editorial and 91 source pins). The A/V path failed before C11-C capture because Python localized speed multiplier `0.75` to `0,75000`; PowerShell's launcher binder surfaced `75000` and rejected it. No later composition/music/mux/FFprobe stage ran.

## V1.4 fix
Do not forward numeric text directly to the typed C11-C launcher. Generate and retain `invoke_c11c_drill_launcher.ps1`; pass invariant ASCII `0.75000` to a `[string]` parameter; parse with `InvariantCulture`; invoke unchanged launcher with typed `[double]`; set wrapper thread culture invariant for call; restore original culture in `finally`. The installer must run that exact wrapper against a dummy launcher in forced `es-ES` and confirm capture `0.75`. Tests 16/16, py_compile 7/7 and PowerShell AST must pass before transaction.

## Retry rule
D99 failed output root is non-overwritable and remains evidence. Generate a fresh unique request ID; do not rerun into `artifacts/production/c11e/D99-GUI-85201B7B4FF7`.

## Next execution sequence
V1.4 install and postimage audit → fresh GUI Resolver + Plan → single `tracking/tier-1` A/V → operator visual/listening review → CLI smoke → 20-selector A/V family matrix → E4C close. E1 remains PREPARE_ONLY; family adapter NOT_CONNECTED_E1; C11-C frozen; dispatch false; release NONE.



## D99-GUI-85201B7B4FF7 — single-selector A/V pilot diagnosis — 2026-11-12

**Authoritative evidence:** `D99-GUI-85201B7B4FF7.zip` SHA-256 `0913179f9852b7b1f75c2a7e2f763a111bc8d807d08d20036a2891ae94661f56`; `D99-GUI-85201B7B4FF7-tests.zip` SHA-256 `16f0e199429deffb85025cd35d0cfd4fe2ec9fe237cf66482f6de6b14cd6ef23`.

The GUI's **Resolver + Plan** stage is successful, not a failure: E1 receipt is `PASS_E1_PREPARATION_ONLY`; GUI/CLI semantic parity is `PASS`; D9.10 bridge planning is `PASS_BRIDGE_PLANNING_ONLY`; D composition plan is valid with real GAME-visible editorial; the request is `visual_drills / tracking / tier-1`, gameplay seed `12345`, music seed `840001`, `REVIEW_720`. This remains deliberately plan-only at E1 and does not claim renderer or dispatch activation. The second GUI action, the shared D A/V executor, fails before the native C11-C producer starts.

Exact failure from `logs/c11c_drill_producer.log`: C11-C's `run_visual_drill_production.ps1` rejects `-SpeedMultiplier` because it receives `75000`, outside `[ValidateRange(0.1,3.0)]`. The pinned profile `profiles/difficulty/visual_drill_tracking.json` has tier 1 `speed_multiplier=0.75` (source SHA-256 `6de8812bd46904e122ecdd0eae22fb2979bd75399c34779248c6569e833c921e`). The adapter applied Python's host decimal separator and sent `0,75000`. On the operator's locale, Windows PowerShell 5.1 parameter binding split/coerced that comma decimal and delivered `75000`. This is a cross-locale numeric argument-boundary defect in the D adapter, not a defect in the pinned C11-C launcher or difficulty profile.

The failure occurs before a successful C11-C capture. There is no native MP4, no D frame composition, no FAMILY_MUSIC_V4 WAV generation, no mux, and no final FFprobe result in this run. The failure does not indicate an editorial, font, Qt, geometry, phase/timebase, music determinism, or A/V stream-equivalence defect. The first evidence bundle contains `RUNNING` and `FAILURE` receipts and the exact native producer log. The `-tests.zip` is a preparation/parity/contract receipt bundle; it does not show a second independent A/V failure. Do not infer additional failures from its intentionally plan-only receipts.

**V1.4 correction:** remove host-locale formatting entirely. Python emits an ASCII invariant string such as `0.75000` to a string-typed PowerShell wrapper. The wrapper parses it with `[System.Globalization.CultureInfo]::InvariantCulture`, sets the wrapper thread culture to invariant for the call, then invokes the existing pinned C11-C launcher with an already-typed `[double]$speed`. The native C11-C launcher remains byte-identical and receives `0.75`; C11-C stays silent via `-NoSound`. The wrapper is retained in the run logs and its hash/argument are written into the execution receipt. Regression tests cover invariant formatting, wrapper parse/type handoff, and absence of host-locale formatting. The V1.4 installer additionally executes this exact wrapper against a dummy parameter-compatible launcher while forcing `es-ES`, and requires the dummy to record `0.75` before any repository mutation.

The failed output root `artifacts/production/c11e/D99-GUI-85201B7B4FF7` is intentionally preserved. It must not be overwritten. The retry must use a **new unique request_id/output root** (generate a fresh GUI request and repeat Resolver + Plan); do not delete or recycle this failed evidence. After V1.4 installation PASS: audit its postimages/source pins, rerun the GUI plan stage with a fresh ID, then execute only `tracking/tier-1`. Continue only when native capture, D composition, FAMILY_MUSIC_V4 A/B/C, final A/C video/audio stream hashes, FFprobe, and human visual/listening review pass. CLI smoke/parity follows on the same shared adapter. Do not start the 20-selector A/V matrix until the single-selector result is accepted.

Governance is unchanged: E1 `PREPARE_ONLY`; `family_adapter.status=NOT_CONNECTED_E1`; `production_dispatch=false`; `release_authority=NONE`; no Git checks; commits operator-managed; C11-C frozen manifest SHA remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.


---

## Installer V1.3 transaction correction

Do not run V1.2 again. Its Windows failure occurred at `TRANSACTION_START`, OP-001, when `File.Replace` was called with a null destination backup path. The diagnostic shows the target remained the exact preimage and rollback completed. V1.3 supplies unique backup paths to both forward replacement and rollback, records those paths in the transaction journal, verifies backup hashes, and runs a disposable same-volume forward/rollback API probe in staging before any project-file write. The existing A/V execution adapter, E1 PREPARE_ONLY contract, A/B 840001 and C 840002 design are unchanged.

## Installer V1.1 correction

PowerShell 5.1 must not receive quote-bearing Python source via `python.exe -c`. The V1.1 installer creates `_installer_python_version_probe.py` and `_installer_pyside6_qt_probe.py` under its isolated temporary stage, invokes each as a script path, includes both in staged `py_compile`, and persists stage/stack diagnostics in `%TEMP%` if a pre-transaction validation fails. This is an installer-only correction; both GUI/CLI postimages, the common D adapter, and E1 semantics remain unchanged.

# CURRENT E4C EXECUTION PLAN OVERRIDE — SHARED A/V ADAPTER V1.1 — 2026-11-11

## Architecture

Modify only existing `c11c-suite/c11c-producer/main.py` and `c11c-suite/c11c-producer/c11e_production_cli.py`; add one D-owned `tools/c11d/d9/c11e_e4c_drill_execution.py`. GUI and CLI call precisely the same adapter. Do not alter `c11e_production_service.py`, the consumer, E1 service semantics, C11-C or any binder. E1 remains PREPARE_ONLY; its `family_adapter.status=NOT_CONNECTED_E1` remains unchanged. CLI's default invocation remains preparation-only; the new execution route requires explicit `--execute-drill-av --origin CLI`.

## Fail-closed request contract

- Canonical `visual_drills`, one of tracking/pursuit/saccade/peripheral_scan × tier-1..5; mode PRODUCTION; REVIEW_720; audio ON; personalization ON; gameplay/music seeds valid and numerically distinct.
- Require at least one visible editorial field from title/subtitle/CTA, with real non-whitespace value other than `UNKNOWN`; reject empty editorial before output creation. D editorial visible in GAME only, hidden in PRE_ROLL/END_CTA/DONE.
- Verify all E1 `source_identity.source_pins` and frozen C11-C manifest at pre-execution, immediately pre-renderer, and post-execution. Require normalized pin sets equal.

## Execution contract

1. E1 prepares GUI and CLI intents; validate both and require semantic identity/parity. Keep adapter state NOT_CONNECTED_E1.
2. Preflight Python 3.13, existing PySide6/Qt, FFmpeg/FFprobe, PowerShell and exact Godot 4.7.1 Mono before creating output root.
3. Invoke existing C11-C `run_visual_drill_production.ps1` with `-NoSound`, gameplay seed, selected tier, `constant` pacing, REVIEW_720, and isolated `artifacts/production/c11e/<request_id>` output.
4. Apply approved D outer-band composition to every decoded native frame; preserve the agreed frame count/FPS/timebase and phase window.
5. Generate A and B FAMILY_MUSIC_V4 WAVs using `C11CSafeAmbient.py` with music_seed 840001; generate C using 840002; never route gameplay seed into music generator. No D3 V5.
6. Verify A/B WAV identical and C distinct; mux A and C as AAC-LC 48kHz stereo; verify final A/C video stream SHA identical and audio stream SHA different. FFprobe validates H.264 High 720x1280 30fps yuv420p TV, frame count, duration and A/V start alignment.
7. Emit durable JSON receipts, logs, hashes and explicit isolated-qualification governance. dispatch=false; release authority NONE.

## First run

Use one request only: `tracking/tier-1`, gameplay seed `12345`, music seed `840001`, changed C `840002`, REVIEW_720, audio/personalization ON, non-empty visible editorial. Do not launch the 20-selector A/V matrix until the operator accepts the first MP4 and audio.

## Installation / validation

Installer enforces exact preimages/postimages, support pins, complete payload inventory, PowerShell 5.1 AST, Python 3.13 + PySide6 probe, staged py_compile/tests, immediate pre-transaction rechecks, transaction journal and hash-guarded rollback. No Git checks, pip or shared package changes. Active Windows GUI smoke and A/V execution remain required after installation.

---

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


## Installer execution boundary V1.2

The V1.1 active-Windows failure at `STAGED_UNIT_TESTS` was a PowerShell native stderr handling defect, not a failing adapter test. Python unittest emitted its first verbose case line (`... ok`) to stderr, and PowerShell 5.1 `$ErrorActionPreference='Stop'` terminated the invocation before the process exit code was read. V1.2 replaces `& python.exe ... 2>&1` with .NET ProcessStartInfo, separate asynchronous stdout/stderr capture, and exit-code-only success evaluation. Require 13/13 tests and the immediate pre-transaction gates to pass on Windows. This is a gate repair, not test relaxation.


## V1.5 CLI smoke installer incident and recovery
V1.5 failed in `STAGING_AND_PYTHON_TESTS` before transaction (`journal=[]`) due an empty/ineffective Python argument invocation. V1.6 changes only the add-only installer and its contract tests: explicit `$PythonArguments`, named argument binding, nonempty command validation, closed stdin, command logging. The CLI runner and its contract remain otherwise unchanged. Install V1.6, require PS 5.1 AST 2/2, staged Python tests 12/12, py_compile 1/1, immediate 19-pin recheck and `PASS_ADD_ONLY_INSTALL`; then run CLI A/V smoke once with a new request ID.


## E4C V2 consumer corrective override — 2026-11-12

### Accepted and preserved

- GUI pilot `D99-GUI-6514F1066E79`: historical technical/A/V PASS with operator visual/audio acceptance under the earlier consumer. Do not rerun GUI A/V.
- CLI smoke `E4C-CLI-SMOKE-20261112T091253Z-5a2e96b8`: technical PASS; music and render quality accepted by operator, but V1 composition visually rejected. Receipt SHA `57fe829b2ae83fc16a962710b8a1ef8e4635ebf8fd4326714ed24c69c4a0f903`; intent SHA `9dfe5c1c4568ed7fbc4bb4260d47da4e518b1a163811fb88f2a9f1bff55c304e`.
- Reuse source MP4 SHA `d10950bca9358de4ffe8a9f4f24c8c35cdb37e25050775a9220a4d15ffb45338`; WAV A/B SHA `e54b960c799102fb104a99ccd7b94c4a41b5b22d54665acda72106b36646f277`; WAV C SHA `5e81b6426f7915c7cad4c658fc24b90cd17c870a4497f45136a53e43b71efd40`.
- Do not rerun D99, CLI facade, C11-C capture, Godot, FAMILY_MUSIC_V4, FFmpeg music creation or accepted binder/native capture/pixel V1 suites.

### V2 implementation contract

Replace only `tools/c11d/d9/c11e_e4c_drill_visual_composition_consumer.py` and its test module. The V2 consumer pins the exact 8,837-byte `PresentationProfile.gd` source hash and uses `get_social_regions()`. GAME crops `(0,192,720,896)` and pastes at the same coordinates without scaling, interpolation or resampling; D title/subtitle/CTA render only in full-width header/footer. PRE_ROLL and END_CTA return full native source frames unchanged. DONE emits no frame. Timebase remains PRE_ROLL 90 + GAME 630 + END_CTA 90 = 810 at 30fps.

### Immediate operator sequence

1. Do not run V1.7. Verify V1.8 ZIP against its sidecar; extract to a fresh Downloads directory (never into checkout).
2. Run the included Windows PowerShell 5.1 installer with canonical Python 3.13. Require 21/21 support pins; one exact replacement preimage; 22 add-only destination states; PowerShell AST 2/2; existing PySide6/Qt offscreen probe; `py_compile=3/3`; staged Qt tests `18/18`; immediate pin/destination rechecks; durable journal; atomic replacement/backups; postimages and postpins.
3. Inspect install receipt, the replacement postimage, all 22 add postimages and all pins.
4. Run `RUN_C11E_E4C_DRILL_AV_EXISTING_MEDIA_V2_REQUALIFICATION.ps1` using the preserved CLI smoke root. New output ID is generated by the runner. It must never invoke Godot, C11-C launcher, CLI facade, native capture or music generator.
5. Require all 630 GAME body crops byte-exact and all 180 PRE_ROLL/END_CTA frames full-frame byte-exact; unchanged 90/630/90; H.264 A/B/C identical; WAV A/B exact and C distinct; AAC A/B exact and C distinct; final FFprobe 27s/810 frames/720×1280/30fps/H.264 High yuv420p TV/AAC-LC 48k stereo/sync start zero; source pins unchanged.
6. Operator visually inspects seven frames and full final A/B/C media and confirms listening. Do not count row 1/20 until this V2 review is PASS.
7. After row 1/20 acceptance, proceed with the remaining 19 selectors only. Each row needs the same V2 frame assertions, A/B/C stream controls, receipts/pins and operator review. Then close E4C.

Do not create an adapter patch, GUI A/V retry, new CLI smoke execution, or regenerate music. E1 remains PREPARE_ONLY / NOT_CONNECTED_E1; production dispatch false; C11-C sole authority; release NONE.


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

## Plan de ejecución R5 — recuperación de output R3

### Estado R5 — 14 de noviembre de 2026

La instalación y auditoría independiente de R3 están cerradas: `PASS_INDEPENDENT_POST_INSTALL_AUDIT`, 17/17 postimages, 2/2 backups, 21/21 source pins y manifiesto C11-C congelado. La evidencia R4 `R4_RECOVERY_20261114T092932Z.zip` identifica un defecto de semántica SHA, no una mutación del intent: `intent_sha256=9dfe5c1c...` es el digest canónico del JSON con el campo `intent_sha256` excluido; el SHA de bytes del fichero preservado es `dfc86176...`. Ambos deben verificarse por separado y enlazarse con `receipt.e1_validation.intent_sha256`. Nunca reescribir el intent histórico para hacer coincidir ambos valores.

R5 instala la validación dual, la suite de regresión y un wrapper PowerShell integrado que captura diagnóstico automático. La documentación completa, el Authority/Roadmap/Plan/Blocker/Gates/Incident/Doc Index/Backlog y Master/Start/First prompts forman parte del propio ZIP instalador; no se distribuyen como overlays separados.

Los outputs R3 siguen siendo inmutables: request `E4C-CLI-COMPOSITION-V2-20261114T003422Z-a4d913f9`; composición 810/810, MP4 A/B/C y mux ya aceptados como medios existentes; no volver a componer, muxar, generar música, recapturar native ni lanzar CLI smoke. Solo verificar los medios existentes, extraer siete PNG y emitir recibo técnico/bundle.

R5 destino: `tools/c11d/d9/RUN_C11E_E4C_V2_3_R5_EXISTING_OUTPUT_RECOVERY.ps1`. El estado técnico seguirá pendiente de aceptación visual/auditiva humana. E1=`PREPARE_ONLY`; family adapter=`NOT_CONNECTED_E1`; production dispatch=`FALSE`; release authority=`NONE`.
