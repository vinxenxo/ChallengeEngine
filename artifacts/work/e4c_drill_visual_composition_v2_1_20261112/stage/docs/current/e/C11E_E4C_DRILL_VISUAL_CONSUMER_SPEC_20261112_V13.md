# C11-E E4C Drill visual consumer specification — V13 (2026-11-12)


## Authoritative installer correction — V1.8 package-binding failure / V1.9 consolidated recovery (2026-11-12)

The operator's V1.8 run passed the ZIP sidecar and entered the package installer, then failed closed at `OPERATION_PACKAGE_FILE_BINDING_FAIL` for `docs/current/e/C11D_E_BLOCKER_REMEDIATION_REGISTER_20261112_V54.md`. The V1.8 builder renamed physical documentation payloads to the next versioned filenames (for example V55) but failed to regenerate the matching `replacements`/`additions` destination rows; several operation destinations still referenced their predecessor names. The validator correctly rejected the mismatch before the transaction journal or destination writes. This was a package-manifest construction defect, not a Windows runtime issue. Do not rerun V1.8.

V1.9 is a complete rebuilt overlay. Its operation rows are generated directly from the physical payload tree: `payload/replace/<relative>` maps only to `REPLACE <relative>`, and `payload/add/<relative>` maps only to `ADD_ONLY <relative>`. The installer independently enforces that mapping for every operation, verifies one-to-one closure between all payload files and operation rows, rejects duplicate package paths and destination paths, and checks manifest counters against actual arrays. The V1.9 matrix is exactly one existing D-consumer replacement plus 23 add-only destinations (24 mutation operations); package inventory also includes the README and installer. All versioned current-doc and prompt destinations now match their package paths exactly.

V1.9 preserves the V2 consumer, 18 focused tests, requalifier, runner, 21 support pins and 91-pin/CLI source evidence unchanged. The only changes from V1.8 are installer/manifest construction integrity, corrected operation destinations, documentation/prompt version increments, and incident recording. The V1.8 attempt failed before transaction; no checkout destination mutation occurred. V1.9 remains `NOT_YET_INSTALLED` pending its Windows 5.1/Python 3.13/PySide6 preflight and transaction receipt.

The V1.9 installer also reports pre-transaction failures distinctly as `FAIL_CLOSED_PRE_TRANSACTION_NO_DESTINATION_WRITES` with a `%TEMP%` diagnostic, rather than labelling an empty journal as a completed rollback. No Git, pip, shared dependency, GUI/CLI, E1, C11-C, dispatch or release changes are permitted.



## Authoritative update — V1.7 installer incident and V1.8 correction (2026-11-12)

V1.7 failed closed at `DESTINATION_PREFLIGHT` because it misclassified the newly introduced `tests/test_c11e_e4c_drill_visual_composition_consumer.py` as a replacement. The destination was absent in the active checkout. The declared preimage SHA `aedeb5754d94fdbaad134a653f57ca07466c845dcef081c8774668245455a7a0` is actually the historical V9 test stored under `tools/c11d/d9/`, not a preimage at the new `tests/` path. This is a manifest/installer classification defect, not a V2 consumer failure. The failure occurred before evidence-root and transaction-journal initialization; no destination writes or repository mutations occurred. Its generic `FAIL_CLOSED_ROLLBACK_COMPLETE` message reflects a zero-entry/no-op rollback.

V1.8 supersedes V1.7 and is the only candidate permitted for installation. Its operation matrix is exactly one hash-guarded replacement (`tools/c11d/d9/c11e_e4c_drill_visual_composition_consumer.py`) plus 22 `ADD_ONLY` destinations, including the new test module. The installer asserts the exact classification, unique operation destinations, and uses manifest-resolved package paths for staged inputs. It rechecks all source pins and all destination states before journaling/writing. Do not rerun V1.7. No source, GUI/CLI, E1 service, executor, C11-C or shared dependency changes are included.

V1.8 install status: `NOT_YET_INSTALLED`. Do not claim V2 Windows qualification from package/static checks. After install PASS, reuse the already accepted CLI native MP4 and WAV A/B/C for the existing-media V2 requalification; no new C11-C capture or music generation. E4C remains open, V2 A/V acceptance pending operator review, matrix not started. C11-C remains sole production authority; E1 PREPARE_ONLY / NOT_CONNECTED_E1; dispatch false; release authority NONE.

## Purpose

Define D-owned consumption of the unchanged C11-C Visual Drill frame stream in `REVIEW_720`. This version supersedes V9 only for the consumer's spatial composition and phase ownership. It does not alter C11-C output or its source.

## Authoritative geometry

Use `core/presentation/PresentationProfile.gd::get_social_regions()` with the exact source pin SHA-256 `187b1cf8ab96b9031785a0f36b0054a60383c97cb3d81906c7d9bbcd373bef24` (8,837 bytes). `get_composition_geometry()` is a safe-area compatibility geometry and is not the Drill body viewport.

At 720×1280, the canonical full-width regions are:

| Region | Rectangle | Ownership |
|---|---:|---|
| Header | `(0,0,720,192)` | D editorial title/subtitle during GAME only |
| Body | `(0,192,720,896)` | Exact native C11-C social-body pixels during GAME |
| Footer | `(0,1088,720,192)` | D editorial CTA during GAME only |

Source logical social canvas is 540×960, header/body/footer ratios 0.15/0.70/0.15; device scale is 4/3.

## Phase ownership

- PRE_ROLL: return the complete native C11-C frame, unchanged; no D bands, no D text.
- GAME: allocate 720×1280 D canvas; copy only source rectangle `(0,192,720,896)` to the identical destination rectangle; no scale, interpolation, resampling, stretch, or translation. Draw D title and subtitle in header and CTA in footer. Native family header/footer must not enter the GAME body.
- END_CTA: return the complete native C11-C frame unchanged; native C11-C CTA/header remains authoritative; no D overlay.
- DONE: no delivery frame.

## Timebase

The already approved V1 timebase proposal remains immutable: 90 PRE_ROLL + 630 GAME + 90 END_CTA = 810 frames at 30fps (27s). Frame order and indices remain identity; no resampling.

## Pixel invariants

1. For every GAME frame, RGB888 source crop bytes at `(0,192,720,896)` equal destination body bytes at the same coordinates.
2. For every PRE_ROLL and END_CTA frame, complete RGB888 output bytes equal source frame bytes.
3. Source QImage is not mutated.
4. D editorial is visible only in GAME; fields remain title/subtitle/call_to_action and raw source editorial/hash are unchanged.
5. Font coverage and layout overflow fail closed; no truncation or unsupported glyph substitution.
6. The test oracle must explicitly reject V1 centered contain viewport `(108,192,504,896)`.

## Execution boundary

Only D-owned consumer and test replacement. Existing E1 service, GUI, CLI facade, D shared A/V executor, C11-C sources, launchers, binders, music and dependencies remain unchanged. Existing-media isolated requalification may use the preserved CLI native MP4 and existing WAV A/B/C; do not invoke Godot, C11-C launcher, new native capture or music generation. E1 remains PREPARE_ONLY / NOT_CONNECTED_E1, production dispatch false, release NONE.


## Authoritative update — V1.9 geometry contract test failure / V2.0 consolidated correction (2026-11-12)

The operator ran V1.9. Package SHA, 26/26 inventory, 21/21 support pins, frozen C11-C manifest and PowerShell AST 2/2 all passed. The installer then failed closed in `STAGING_AND_PYTHON_TESTS`, before transaction initialization or destination writes, because the staged consumer rejected `geometry.canvas` as a social-region mismatch; 0 tests ran. The installer created its failure diagnostic under the designated `artifacts/tests/c11e/e4c_v2_installer` evidence root; no source/destination operation was applied and the transaction journal remained empty.

Root cause is exact and localized in the V2 contract oracle. The V2 proposal's `geometry.canvas` contains five fields: `x`, `y`, `width`, `height`, and `aspect_ratio="9:16"`. Both `_verify_decision_and_proposals()` and `validate_plan()` compared it by exact dictionary equality against a four-field expectation that omitted `aspect_ratio`. The proposal is correct; the validator expectation was incomplete. It was duplicated in two independent validation sites, so both must use the same single canonical region constant.

V2.0 consolidates the correction: one `EXPECTED_SOCIAL_REGIONS` constant includes the exact 9:16 metadata and is used by proposal and plan validation; the frozen 540x960 logical `PresentationProfile.get_social_regions()` is checked against the exact 4/3 projection to 720x1280, yielding header 720x192, body 720x896 at y=192, and footer 720x192 at y=1088. Two tests are added: reject tampered aspect-ratio metadata and prove the logical-to-REVIEW_720 projection. Focused suite rises from 18 to 20 tests. No proposal, decision, timebase, C11-C, E1, GUI/CLI, execution adapter, music, binder, requalifier or runner behavior is changed.

V1.9 must not be rerun. V2.0 is a rebuilt overlay candidate; its Windows PySide6/Qt OFFSCREEN tests and transaction remain unqualified until the operator-run installer produces the complete receipt. No further installer iteration is authorized by this package record absent a new independent failure with evidence.


## Authoritative update — V1.9 geometry contract test failure / V2.0 consolidated correction (2026-11-12)

The operator ran V1.9. Package SHA, 26/26 inventory, 21/21 support pins, frozen C11-C manifest and PowerShell AST 2/2 all passed. The installer then failed closed in `STAGING_AND_PYTHON_TESTS`, before transaction initialization or destination writes, because the staged consumer rejected `geometry.canvas` as a social-region mismatch; 0 tests ran. The installer created its failure diagnostic under the designated `artifacts/tests/c11e/e4c_v2_installer` evidence root; no source/destination operation was applied and the transaction journal remained empty.

Root cause is exact and localized in the V2 contract oracle. The V2 proposal's `geometry.canvas` contains five fields: `x`, `y`, `width`, `height`, and `aspect_ratio="9:16"`. Both `_verify_decision_and_proposals()` and `validate_plan()` compared it by exact dictionary equality against a four-field expectation that omitted `aspect_ratio`. The proposal is correct; the validator expectation was incomplete. It was duplicated in two independent validation sites, so both must use the same single canonical region constant.

V2.0 consolidates the correction: one `EXPECTED_SOCIAL_REGIONS` constant includes the exact 9:16 metadata and is used by proposal and plan validation; the frozen 540x960 logical `PresentationProfile.get_social_regions()` is checked against the exact 4/3 projection to 720x1280, yielding header 720x192, body 720x896 at y=192, and footer 720x192 at y=1088. Two tests are added: reject tampered aspect-ratio metadata and prove the logical-to-REVIEW_720 projection. Focused suite rises from 18 to 20 tests. No proposal, decision, timebase, C11-C, E1, GUI/CLI, execution adapter, music, binder, requalifier or runner behavior is changed.

V1.9 must not be rerun. V2.0 is a rebuilt overlay candidate; its Windows PySide6/Qt OFFSCREEN tests and transaction remain unqualified until the operator-run installer produces the complete receipt. No further installer iteration is authorized by this package record absent a new independent failure with evidence.
