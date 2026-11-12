# C11-E CONTINUATION MASTER / OVERHAND PROMPT V140 — 2026-11-12

## Project and current source authority

Continue ChallengeEngine C11-E from the active Windows checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. The active checkout is the only source authority. Evidence ZIPs and snapshots are read-only evidence; never extract them over the checkout. The operator manages commits. `GIT_CHECKS=SKIPPED`; never inspect Git/HEAD/status/branch. No pip or shared dependency changes. Runtime: Windows PowerShell 5.1, existing Python 3.13 and installed PySide6; Godot 4.7.1 Mono is not needed for the immediate V2 correction.

## Frozen authority and permanent locks

C11-C 2.19.12 remains the only production authority. Frozen manifest is 796,318 bytes and SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. Do not modify C11-C generators, mechanics, binders, RNG, timebase, core audio, canonical definitions, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, launchers or frozen manifest. No sixth suite module, second Producer, new binder or parallel service.

E1 remains `PREPARE_ONLY`; `family_adapter.status=NOT_CONNECTED_E1`. No production dispatch. `release_authority=NONE`. D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION. Isolated E4C test-only composition is not a production renderer/release grant.

## E4C facts accepted and retained

- E4C Drill binder V2 and 20 native silent source captures: accepted. Do not repeat absent pin drift.
- Earlier 100/100 real-frame V1 pixel check: accepted only for V1's tested consumer, now historical; it does not prove V2 body geometry.
- GUI A/V pilot `D99-GUI-6514F1066E79`, selector `tracking/tier-1`: accepted historically under V1; do not rerun GUI A/V.
- CLI smoke `E4C-CLI-SMOKE-20261112T091253Z-5a2e96b8`: technical A/V execution PASS, shared D executor and GUI/CLI parity PASS, 91 E1 pins pre/pre-render/post identical, 810 frames 90/630/90, A/B WAV identical, C changed, final H.264 A/C identical and AAC A/C different, 27s 720×1280 30fps H.264 High + AAC-LC 48k stereo. Receipt SHA `57fe829b2ae83fc16a962710b8a1ef8e4635ebf8fd4326714ed24c69c4a0f903`.
- Operator review of CLI final media: music and render quality OK; composition V1 REJECTED because native tracking header/footer are embedded inside the central viewport while D editorial is also painted in outer bands.
- Preserve all CLI artifacts, failed V1 media and GUI media; don't rerun CLI facade, GUI A/V, C11-C capture, Godot, binder, or music generation for the correction.

## Proven V1 cause and authoritative V2 spatial contract

V1 consumed the complete native 720×1280 frame by scaling it to 504×896 and drawing at `(108,192)`. It duplicated native family header/footer inside the body and composited D text separately; PRE_ROLL and END_CTA were also wrapped in D outer-band composition. Old V1 pixel tests checked this faulty viewport instead of native social-body identity.

Use the frozen `core/presentation/PresentationProfile.gd` pin `187b1cf8ab96b9031785a0f36b0054a60383c97cb3d81906c7d9bbcd373bef24` (8,837 bytes), function `get_social_regions()`, not safe-area `get_composition_geometry()`:
- Header `(0,0,720,192)`.
- Body `(0,192,720,896)`.
- Footer `(0,1088,720,192)`.
- GAME: crop only body rectangle and paste to the same coordinates, pixel-exact RGB888; no scaling/interpolation/resampling. D title/subtitle in header; D CTA in footer.
- PRE_ROLL and END_CTA: complete native frame passthrough, byte exact; native C11-C END_CTA stays authoritative.
- DONE: no frame.
- Keep timebase exactly 90/630/90 at 30fps, 810 frames, no frame order/index change.

## V2.0 corrective overlay candidate

Package: `C11E_E4C_DRILL_VISUAL_COMPOSITION_V2_REQUALIFICATION_V2_0_20261112.zip`.
It replaces only D-owned `tools/c11d/d9/c11e_e4c_drill_visual_composition_consumer.py`. The focused test module `tests/test_c11e_e4c_drill_visual_composition_consumer.py` is a new `ADD_ONLY` destination; it did not exist in the active checkout. The 23 `ADD_ONLY` payloads also include the V2 proposal/schema/decision, requalifier and runner, versioned docs, incident history and this prompt set. It does not touch GUI `main.py`, CLI facade, E1 service, shared D A/V executor or C11-C.

The installer must verify the external ZIP sidecar and complete package inventory, 21/21 support/source pins, one exact replacement preimage or exact postimage, 23 add-only destination states, PowerShell 5.1 AST 2/2, existing Python 3.13/PySide6 runtime, py_compile 3/3, focused tests 18/18, immediate rechecks, durable journal, atomic replacement with exact backups and hash-guarded rollback. No writes until every preflight passes. Stop at first unknown state. Inspect all postimages and source pins after installation.

## Immediate operator task

1. Verify package SHA-256 sidecar. Extract package to a fresh Downloads folder; never extract into checkout.
2. Run Windows PowerShell 5.1 installer:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\INSTALL_C11E_E4C_DRILL_VISUAL_COMPOSITION_V2_V2_0.ps1" `
  -ProjectRoot "C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS" `
  -PythonExe "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe" `
  -PackageZip "$env:USERPROFILE\Downloads\C11E_E4C_DRILL_VISUAL_COMPOSITION_V2_REQUALIFICATION_V2_0_20261112.zip"
```

3. Verify install receipt: `INSTALL_STATUS=PASS_REPLACE_AND_ADD_ONLY_INSTALL`, `SOURCE_PINS=21/21`, `PY_COMPILE=3/3`, `STAGED_TESTS=20/20`, `POWERSHELL_AST=2/2`, the replacement postimage and every add postimage exact, no unknown journal state. Confirm E1/CLI/service/executor pins unchanged.
4. Run `tools/c11d/d9/RUN_C11E_E4C_DRILL_AV_EXISTING_MEDIA_V2_REQUALIFICATION.ps1` with active ProjectRoot, existing Python 3.13 and the preserved CLI evidence root `artifacts/production/c11e/E4C-CLI-SMOKE-20261112T091253Z-5a2e96b8`.
5. Require V2 requalification technical PASS: 630/630 GAME body crops byte-exact, 180/180 full-frame passthrough, timebase 90/630/90, pins unchanged, reused native MP4 and WAV hashes, H.264 A/B/C exact, WAV/AAC A/B exact and C distinct, FFprobe 27s 810 frames 720×1280 30fps H.264 High yuv420p TV + AAC-LC 48k stereo, A/V start aligned. Receipt remains pending human review.
6. Inspect seven PNGs and complete A/B/C MP4s. Operator visually verifies no native family header/footer inside GAME body; D title/subtitle only in top band; D CTA only footer; PRE_ROLL/END_CTA full native frames; listen to A/C. Only explicit review PASS counts `tracking/tier-1` as V2 matrix row 1/20.
7. After row 1 accepted, run remaining 19 unique selectors through the V2 composition/A/V matrix. Reuse accepted binder and native evidence where exact provenance allows; don't repeat old V1 pixel suite. Close E4C only with 20/20 V2 selector A/V, receipts/pins and required operator review.

## Full roadmap after E4C

E5 cross-family determinism, gameplay/music seed isolation, profile/binder non-leakage, GUI/CLI parity and negative controls → E6 Smoke18 (6 per family) → E7 Matrix101 (54 Challenge + 27 Loop + 20 Drill; CH_008/009 held due 11s declared vs 12s phase sum, 99 provisional runnable) → E8 historical C-to-E regression mapping, independent acceptance, immutable freeze and a separately authorized promotion. C11-C remains authoritative until E8 and separate promotion approval.

## Working discipline

Review the logs, full evidence and the relevant current/older docs before decisions. Reuse accepted gates; don't rerun without source/test pin drift or an explicit new contract. Update Authority, Gates, Backlog, Blocker, Roadmap, Plan, Incident Register, Doc Index and all three prompts on each material handoff. Work several safe steps per iteration but stop on uncertainty or unknown transaction state. Never claim Windows PASS before the operator's actual output.


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
