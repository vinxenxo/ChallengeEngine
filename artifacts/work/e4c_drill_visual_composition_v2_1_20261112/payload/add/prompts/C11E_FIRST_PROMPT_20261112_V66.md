# C11-E FIRST PROMPT V64 — 2026-11-12

Continue C11-E in the active Windows checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS` from the latest accepted E4C CLI smoke and the V2 visual-composition correction. The active checkout is authoritative; ZIP snapshots are evidence only and must never be extracted over it. Operator manages commits. `GIT_CHECKS=SKIPPED`; do not inspect Git/HEAD/status/branch. No pip or shared environment changes.

## Frozen production baseline

C11-C 2.19.12 is the sole production authority. `release/C11C_FREEZE_PACKAGE_MANIFEST.json` is 796,318 bytes, SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. Do not edit frozen C11-C generators, mechanics, binder, timelines, RNG, core audio, canonical definitions, launchers or manifest. No sixth suite module, parallel Producer, new binder or service. E1 stays `PREPARE_ONLY`, `family_adapter.status=NOT_CONNECTED_E1`; production dispatch false; release NONE.

## Latest accepted CLI technical evidence

CLI smoke request `E4C-CLI-SMOKE-20261112T091253Z-5a2e96b8`, selector `visual_drills/tracking/tier-1`, gameplay seed 12345, music seeds A/B 840001 and C 840002, REVIEW_720, audio/personalization enabled, title/subtitle/CTA populated. Runner outputs: `SOURCE_PINS_PRE=PASS/19`, `SOURCE_PINS_POST=PASS/19`, CLI entrypoint/shared executor/E1 GUI-CLI parity/A-V bitstream isolation/family music seed isolation PASS, `CLI_SMOKE=PASS_E4C_DRILL_CLI_SINGLE_SELECTOR_AV_SMOKE`. Receipt SHA-256 `57fe829b2ae83fc16a962710b8a1ef8e4635ebf8fd4326714ed24c69c4a0f903`; E1 intent SHA `9dfe5c1c4568ed7fbc4bb4260d47da4e518b1a163811fb88f2a9f1bff55c304e`.

The receipt has 91/91 identical E1 pins pre/pre-render/post; 810 frames at 30fps, phases 90/630/90; FAMILY_MUSIC_V4 WAV A/B identical and C changed; final H.264 A/C identical and AAC A/C different; 27s, 720×1280, H.264 High, AAC-LC 48kHz stereo. User confirmed music and render quality OK, but rejected composition V1 because the native family header/footer were fitted into the central image while D editorial was drawn in additional outer bands.

## V1 defect and V2 contract

V1 scales the whole native source frame to 504×896 and draws at `(108,192)`. V1 tests validated that incorrect viewport. V2 must use `core/presentation/PresentationProfile.gd::get_social_regions()` (8,837 bytes, SHA `187b1cf8ab96b9031785a0f36b0054a60383c97cb3d81906c7d9bbcd373bef24`):
- header `(0,0,720,192)`;
- GAME body `(0,192,720,896)` pixel-exact, same coordinates, no scale/interpolation/resampling;
- footer `(0,1088,720,192)`;
- PRE_ROLL and END_CTA full native frame passthrough; DONE no frame;
- D title/subtitle in header and CTA in footer only during GAME;
- retain timebase 90/630/90, total 810 frames, 27s.

## Immediate work package

Use `C11E_E4C_DRILL_VISUAL_COMPOSITION_V2_REQUALIFICATION_V2_0_20261112.zip`, not an older consumer or an AV adapter patch. It replaces only the D-owned visual composition consumer; the test module is `ADD_ONLY` at the new `tests/` path; adds V2 proposal/schema/decision, 18 tests, a requalifier reusing existing CLI native MP4 and WAV A/B/C, a PowerShell runner, documentation and updated Master/Start/First prompts. No GUI/CLI/E1/executor/C11-C change.

Install on Windows PowerShell 5.1 with existing Python 3.13 and PySide6. Require 21/21 source pins, one exact replacement preimage, 23 add-only destination checks, AST 2/2, py_compile 3/3, 18/18 tests, immediate pre-write rechecks, journaled atomic transaction, postimages and unchanged pins. Then run the V2 existing-media requalifier, never a new native capture/music generation. Require 630/630 GAME body identity, 180/180 full-frame passthrough, A/B/C AV isolation, FFprobe and unchanged pins. Receipt is pending operator visual/audio review; visually inspect seven frames and full final media. Only after explicit PASS count tracking/tier-1 as V2 row1/20.

After row1, complete the remaining 19 A/V selectors and E4C close. Then E5 → E6 Smoke18 → E7 Matrix101 (CH_008/009 held, 99 provisional) → E8 historical C-to-E regression, independent acceptance, freeze and separately authorized promotion.

Do not rerun accepted GUI A/V, CLI smoke facade, Binder, native capture, V1 100/100 pixel tests or music generation. No Git, no pip, no C11-C edits, no production dispatch, `release_authority=NONE`.


## V1.7 installer failure and V2.0 authoritative recovery

V1.7 failed closed in `DESTINATION_PREFLIGHT` with `REPLACEMENT_DESTINATION_MISSING: tests/test_c11e_e4c_drill_visual_composition_consumer.py`. Root cause: the path is new; the declared preimage SHA `aedeb5754d94fdbaad134a653f57ca07466c845dcef081c8774668245455a7a0` actually belongs to the historical test at `tools/c11d/d9/`, not this new `tests/` destination. The new module is `ADD_ONLY`, not a replacement. The failure occurred before evidence-root/journal initialization and before any destination write; the reported rollback was a zero-entry no-op. Do not rerun V1.7.

Use only `C11E_E4C_DRILL_VISUAL_COMPOSITION_V2_REQUALIFICATION_V2_0_20261112.zip` (SHA-256 in adjacent `.sha256`). V2.0 has one replacement (existing D-owned consumer) and 23 add-only destinations (including the new test file). Installer asserts exact operation classification and unique destinations, resolves staged files from manifest rows, and fully preflights all states before transaction. It keeps all Python/Qt, pins, AST, tests, journal, atomic replace, backup and rollback requirements. This is one consolidated correction; do not request or run incremental installer patches after it without a newly demonstrated, independently diagnosed failure.

V2.0 is not yet installed or Windows-qualified until the operator supplies its complete install receipt.


## V1.8 failure and V2.0 single consolidated recovery — 2026-11-12

V1.8 passed its ZIP sidecar but failed operation/package binding for `docs/current/e/C11D_E_BLOCKER_REMEDIATION_REGISTER_20261112_V54.md`. Root cause is systematic: payload files had been renamed to next-version filenames (V55 and other next versions) while operation rows still carried old destination/package paths. This was caught before destination preflight and before transaction journal/writes. No checkout destination changed. Do not rerun V1.8.

Use only `C11E_E4C_DRILL_VISUAL_COMPOSITION_V2_REQUALIFICATION_V2_0_20261112.zip` and its adjacent SHA sidecar. V2.0 rebuilds every operation row directly from the physical payload tree; each `payload/add/<relative>` maps to `ADD_ONLY <relative>` and `payload/replace/<relative>` maps to `REPLACE <relative>`. Its installer checks exact prefix-to-destination mapping, uniqueness, payload-to-operation closure and manifest counters. Matrix: one replacement + 23 add-only = 24 mutation destinations. Do not hand-edit the manifest or extract over checkout.

V2.0 keeps the V2 consumer, 18 test assertions, requalifier and runner unchanged from V1.8. Windows validation remains mandatory: PS 5.1 AST 2/2, source pins 21/21, frozen C11-C manifest, Python 3.13/PySide6/Qt offscreen, py_compile 3/3, tests 18/18, File.Replace round-trip, full rechecks and transaction receipt. A preflight failure must report `FAIL_CLOSED_PRE_TRANSACTION_NO_DESTINATION_WRITES` plus a `%TEMP%` diagnostic, with no transaction rollback attempted when the journal is empty.

After install PASS, run the existing-media V2 requalification once against `artifacts/production/c11e/E4C-CLI-SMOKE-20261112T091253Z-5a2e96b8`. Reuse the accepted native MP4 and A/B/C WAVs; no GUI/CLI smoke, native C11-C capture, Godot or music generation. Require 630/630 GAME body pixels exact, 180/180 PRE_ROLL/END_CTA complete-frame passthrough, unchanged 90/630/90 timebase, 91/91 source pins, identical H.264 A/B/C and audio A/B identical/C distinct. Operator review of seven frames and A/B/C output is still required; E4C stays open until the V2 visual acceptance and 20/20 A/V matrix.


## Authoritative continuation — V1.9 staged geometry failure / V2.0 correction (2026-11-12)

V1.9 passed package SHA, 26/26 inventory, 21/21 source pins, frozen C11-C manifest, PowerShell AST 2/2 and Python py_compile 3/3, then failed closed during `STAGING_AND_PYTHON_TESTS`: the staged Qt test class failed in setup with `V2 social-region geometry mismatch: canvas`; 0 tests ran. It created an installer failure diagnostic in the designated artifacts evidence root, but the transaction journal remained empty and no source/destination operations were written. Do not rerun V1.9.

Cause: the pinned proposal canvas includes `aspect_ratio: "9:16"`; both proposal verification and plan validation used strict dictionary equality against an incomplete expectation lacking that field. V2.0 uses one canonical geometry constant including the aspect ratio in both places and verifies the 540x960 logical social regions scale exactly 4/3 into the 720x1280 REVIEW_720 canvas: header 720x192, body (0,192,720,896), footer 720x192. It adds two regressions, bringing the focused suite to 20 tests.

Use only `C11E_E4C_DRILL_VISUAL_COMPOSITION_V2_REQUALIFICATION_V2_0_20261112.zip` and its sidecar. V2.0 has one replacement and 24 add-only operations. The installer must show package inventory 27/27, operation classification `1_REPLACE+24_ADD_ONLY`, PowerShell AST 2/2, 21/21 pins, Python 3.13/PySide6/Qt offscreen, py_compile 3/3 and `STAGED_TESTS=20/20 PASS` before any transaction. No additional installer patches are part of this handoff.

After installation PASS only, inspect the receipt/postimages and use the existing-media V2 requalifier once. Do not repeat GUI/CLI smoke, native capture, audio generation, binder or already accepted visual pixel qualifications. C11-C remains sole production authority; E1 PREPARE_ONLY / NOT_CONNECTED_E1; release NONE.

## V2.1 authoritative reconciliation (2026-11-12)

`E4C_OPEN_V2_REQUALIFICATION_PENDING`. Geometry V2 and the Test 04 boundary correction are accepted: `validate_plan()` now requires `source_frame_viewport == EXPECTED_SOCIAL_REGIONS["body_rect"]`. Reconciled consumer SHA-256: `e5cf97651e546ad86e2a4d46698553038e4161dc97a55da2654f197ed71f623c` (36,678 bytes); unchanged test SHA-256: `62327e32ed4c15b497efb4a93fecc1d484cebff0b79beaa7ced5099905ffb2bf`; isolated Python 3.13.14 evidence is py_compile PASS and 20/20 PASS.

V1.7 destination preflight, V1.8 operation/package binding, V1.9 geometry contract and V2.0 staging Test 04 failures are closed before transaction; none installed this correction. V2.1 is rebuilt and pending Windows installation, complete receipt and postimage review. Do not install V2.0 and do not repeat GUI, CLI smoke, native capture, music or Binder.

Preserve evidence GUI `D99-GUI-6514F1066E79`, CLI `E4C-CLI-SMOKE-20261112T091253Z-5a2e96b8`, native silent MP4, WAV A/B/C, seeds and bitstreams. V1 composition was visually rejected; `tracking/tier-1` is not yet an accepted V2 matrix row.

Required sequence: documentation; V2.1 installation; receipt/postimage audit; one existing-media requalification; seven-image/three-MP4 review; operator visual/audio acceptance; row 1/20; remaining 19; E4C close; E5, E6 Smoke18, E7 Matrix101, E8. C11-C 2.19.12 only; frozen manifest `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; E1 `PREPARE_ONLY / NOT_CONNECTED_E1`; no Git, pip, C11-C mutation, dispatch or release; operator-managed commits.
