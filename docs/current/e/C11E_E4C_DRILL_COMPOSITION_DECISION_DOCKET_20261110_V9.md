## V9 current state — 2026-11-11

Consumer V8 stopped in `STAGED_VALIDATION` before any repository transaction. The exact cause was a StrictMode ordering bug in the installer: `$testSource` was inspected for the removed `QT_VERSION_STR` token before it was assigned from the staged test file. The run's journal is empty and `rollback=NOT_NEEDED`; no rollback or repository recovery is required. V9 fixes this by loading both `$consumerSource` and `$testSource` first, validating both are non-empty, and only then inspecting their contents. This is an installer-only correction. The Qt consumer, 35-test module and E1 service replacement bytes are unchanged from V8.

V9 also corrects the run ID and receipt/failure schema identities to V9. It preserves the 18-operation scope (one exact-pinned E1 service REPLACE + 17 D-owned ADDs), all 13 support pins, 10 design/font pins, exact-hash operator decisions, frozen C11-C manifest and no-new-dependency policy. The installer uses the existing canonical Producer Python/PySide6 only; it must not invoke pip, install/uninstall packages, change requirements or mutate shared environment dependencies.

V9 is a candidate only. Windows PowerShell 5.1 AST, Qt runtime probe, py_compile 3/3, tests 35/35, immediate pre-transaction rechecks and successful receipt are still pending. No consumer V1–V8 transaction has been recorded. Stop at first failure; do not repeat A.3 V5, binder V2, Godot V3, Loop22 or historical authoring accepted gates.

Next step: verify V9 ZIP SHA and sidecar, then run the V9 installer with the existing canonical `-PythonExe`. Require the same 18 destination states and all pre-write gates. After PASS, inspect `INSTALL_RECEIPT.json`, its SHA and all 18 postimages before any E1 integration review. C11-C remains sole production authority; renderer OFF; dispatch/media/audio OFF; `release_authority=NONE`.

---

# C11-E E4C Drill composition and timebase decision docket — V7 (2026-11-10)

## V8 current state — 2026-11-11

V7 failed closed in `STAGED_VALIDATION` before transaction. Its installer imported `QT_VERSION_STR` from `PySide6.QtCore`; the canonical PySide6 runtime does not export that symbol. This is an installer probe defect, not evidence that PySide6, Qt, QImage or QPainter is missing. The preceding imports of `PySide6.__version__` succeeded. `journal=[]`; `rollback=NOT_NEEDED`; no checkout write occurred.

V8 changes the probe to `from PySide6.QtCore import qVersion` and records `qVersion()` as the Qt runtime version. It requires Qt 6.x, alongside Python 3.13.x, existing PySide6 6.8–6.x, non-null RGB888 QImage and active QPainter. The official Qt for Python API lists `qVersion()` as a QtCore function. V8 does not install, upgrade or uninstall packages, invoke pip, edit requirements, or mutate the shared Python environment.

The consumer, its 35 Qt tests and the E1 service replacement are byte-identical to V7. No functional test result is inferred from the failed V7 runtime probe. V8 must still pass Windows PowerShell 5.1 AST, inventory/pins/destinations/staging, runtime probe, `py_compile` 3/3, all 35 Qt tests and immediate pre-transaction checks before any write. Do not repeat accepted A.3, binder V2, Godot V3, Loop22 or historical Drill authoring.

Governance remains unchanged: C11-C frozen manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; renderer OFF; dispatch/media/audio OFF; `release_authority=NONE`; operator manages commits; Git checks skipped.

### V8 implementation note
No operator decision or approved hash is changed by V8. The installer runtime probe now obtains Qt's version via `PySide6.QtCore.qVersion()`; geometry, timebase, containment, native END_CTA/header/footer ownership, phase suppression and all D/C11-C boundaries remain as previously approved.

---


**State:** `BOTH_NEW_DRILL_DECISIONS_APPROVED_AS_PROPOSED_FOR_D_OWNED_DESIGN_AND_CONTRACT_IMPLEMENTATION_ONLY`.

## Prior exact-hash decisions retained

The operator policy record `49efd5494f351f09d7597c4699e9c12e361b36884b6bfadacd822e6ff1480e04` already approves A.1, A.3, E4B Loop composition, B.1 and D.1 within their recorded limits. B.1 preserves cadence/frame order/duration without resampling but did not itself decide the Drill phase offset. D.1 is only a technical delivery envelope; it does not authorize audio selection, generation, mixing, mastering or loudness behavior.

## New operator record

The explicit operator decision message `APPROVED AS PROPOSAL` is recorded in:

- `docs/current/e/C11E_E4C_DRILL_COMPOSITION_OPERATOR_DECISION_RECORD_20261110_V1.json`
- SHA-256: `eb95da188065b8ebcb2371e2a6bcff6762ce000a5ca74f8ea384ecec4ee58303`

The record binds each decision to its exact proposal and schema hashes. Both proposal files remain byte-identical and continue to carry `PROPOSED_NOT_APPROVED_NOT_RENDERER_INPUT`; approval is represented only in the separate decision record.

## Decision 1 — Drill outer-band geometry — APPROVED_AS_PROPOSED

- Proposal: `definitions/c11d/production/C11E_E4C_DRILL_EDITORIAL_COMPOSITION_PROPOSAL_V1.json`
- SHA-256: `b22f9eb6fce39f877e432ff5f0051ecf5ab8575ecb9f580fe5f158994222fc09`
- Schema SHA-256: `3684316e98ab2054bd913df17c6e398d8040d047027de36332690cfd2be517bc`
- Geometry: 720×1280 REVIEW_720; 192px top/bottom bands; 504×896 uniformly-contained original C11-C viewport at x=108,y=192; no crop/stretch/resampling.
- Visibility: D editorial visible only during GAME; suppressed during PRE_ROLL and END_CTA. Native `VisualDrillEndCTA` and C11-C source frame ownership remain intact.

## Decision 2 — GAME payload to final-presentation timebase — APPROVED_AS_PROPOSED

- Proposal: `definitions/c11d/production/C11E_E4C_DRILL_PRESENTATION_TIMEBASE_PROPOSAL_V1.json`
- SHA-256: `44ab3b0fa09a6f7d42cd8cf2f1122cada6cbffe16a7a6b53c2af5e88d5daddc8`
- Schema SHA-256: `c5cedcd749a6702dc47b1de0bd67c57721bb9a06cee5cb3709cdc1b17d8a6806`
- Mapping: `final_presentation_frame_index = pre_roll_frames + game_payload_frame_index`.
- At 30fps / 630 GAME frames: PRE_ROLL `[0,90)`, GAME `[90,720)`, END_CTA `[720,810)`.
- No frame-rate resampling, frame reordering or C11-C source mutation. D editorial remains GAME-only; native END_CTA is preserved.

## Authorization boundary and next gate

The two approvals authorize D-owned design/contract implementation and focused isolated visual/pixel tests only. They do **not** authorize renderer-native input, renderer activation, production dispatch, media creation, audio selection/generation/materialization, C11-C source/mechanics modification, release promotion or cutover. `release_authority=NONE`; D4.8 remains BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION.

Next: the A.3 V5 reconciliation overlay is already installed and CLOSED/PASS (receipt `d39eec2b3c1d969a3cb0d4e6aaa14b87aadcba74e42e58d283e00ea50768e881`). Install Consumer V4, then verify receipt/postimages and prove phase visibility, font shaping/coverage, clipping/overflow/contrast and deterministic pixel/source identity across all 20 selectors. Native A/V remains a later separate gate using silent protected C11-C capture and existing `FAMILY_MUSIC_V4`; these approvals do not grant audio-generation authority.


Installer recovery note: A.3 V5 is already installed and CLOSED/PASS. Consumer V1/V2 failed before transaction; V3 was superseded before Windows use because faithful V121 staging exposed missing read-only roots `challenges/`, full `assets/`, and `docs/current/d/`. Consumer V4 closes the staging dependency gap and remains the next active-checkout test gate.


## E4C consumer status update — 2026-11-10

A.3 V5 installation is CLOSED/PASS with receipt SHA `d39eec2b3c1d969a3cb0d4e6aaa14b87aadcba74e42e58d283e00ea50768e881`. Consumer V1/V2 both failed before transaction; V1 omitted the guide, V2 had a literal anchor mismatch on semantically correct rollback wording. V4 bundles style guide V13 and enforces the actual expected-postimage/exact-preimage/unknown-state rollback implementation; it also stages `challenges/`, full `assets/`, and `docs/current/d/` read-only. This does not broaden the two geometry/timebase approvals or authorize renderer, dispatch, media/audio, C11-C changes or release. V4 local reconstructed V121 staging passes py_compile 3/3 and 35/35; active Windows PS5.1 AST/runtime/install receipt remain pending.

## Consumer staging note

The geometry and timebase approvals remain unchanged. Consumer V4's expanded test-stage roots are read-only inputs only and do not expand design approval into renderer, dispatch, media, audio, C11-C mutation or release authority.


## Consumer V4 current staging closure

The stage includes the complete pinned E1 → Drill binder → D9.9/D9.10 dependency closure: `challenges/`, full `assets/`, `docs/current/d/`, `docs/current/e/`, `docs/history/c11e/`, `definitions/`, `profiles/`, `release/`, `core/`, `tools/`, and `c11c-suite/c11c-producer/`. All stage roots are read-only test inputs; only one E1 replacement and 17 D-owned adds are transaction operations.
