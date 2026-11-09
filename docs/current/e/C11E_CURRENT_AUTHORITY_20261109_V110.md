# C11-E Current Authority — 2026-11-09 V110

## Current checkpoint

- E4A accepted.
- E4B family/grammar mapping accepted; R1P 27/27 PASS; Loop22 projection 22/22; five exact upstream policy fingerprints approved.
- R1V five-selector / ten-output A/V pilot closed and operator-accepted. Do not rerun.
- Loop22 V1 execution package installed add-only: 30/30 source pins, 16/16 files; frozen C11-C manifest unchanged.
- Loop22 V2 process-bridge overlay installed add-only: 37/37 source pins, 11/11 files. The Windows bridge self-test passed (stdout/stderr separated; exit codes 0 and 23 preserved), PowerShell AST passed, Python AST passed, 24/24 focused tests passed and `LOOP22_MEDIA_PRELAUNCH=PASS_ALL_PRELAUNCH_GATES` was emitted.
- The pinned V1 Python runner then exited 2 before the first media launcher. Exact stderr root cause: `FileExistsError: [WinError 183]` when a later selector tried to create the already-created shared path `source/geometric/A`. There were 0 C11-C launcher invocations, 0 music generations, 0 delivery PCM conversions, 0 muxes and 0 AV outputs in this attempt. The incident is documented in `C11E_E4B_LOOP22_AV_SHARED_DIRECTORY_COLLISION_ROOT_CAUSE_V1.md`.

## Current phase and authorized scope

E4B Loop22 audiovisual qualification remains active and TEST_ONLY. The approved scope remains receipt indices 2–5, 7–10, 12–15, 17–20, 22–27: 22 selectors × A/B = 44 new silent C11-C captures and 44 AV deliveries, with 22 A/B pairs. R1V indices 1, 6, 11, 16 and 21 remain excluded.

The shared-directory repair is intentionally add-only and versioned. It adds runner V2, focused tests V2 and PowerShell wrapper V3. The V1 runner and V2 bridge wrapper are not replaced. The new runner deduplicates physical output paths by normalized Windows identity and owner tuple `(role, internal_family_id, repeat)`, demands exactly 40 unique directories, preflights every leaf absent and creates each once using `exist_ok=False`. Any cross-role/family/repeat alias fails closed.

## Authorized next action

1. Extract `C11E_E4B_LOOP22_AV_SHARED_DIRECTORY_FIX_V1_20261109.zip` into a new Downloads folder, never over the checkout.
2. Run its Windows PowerShell 5.1 add-only installer against the active checkout. Require `INSTALL_STATUS=PASS_ADD_ONLY_INSTALL`, `SOURCE_PINS_VERIFIED=37`, `PAYLOAD_FILES=13`, `ADDED_FILES=13`, and preserve the install receipt SHA.
3. After installer PASS, run only `tools/c11d/d9/RUN_C11E_E4B_LOOP22_AV_QUALIFICATION_V3.ps1`. Do not rerun V1 or V2 wrappers.
4. Require process-bridge regression PASS (exit codes 0/23 and separated streams), PowerShell AST PASS, Python AST PASS, exactly 25 focused tests, and `LOOP22_MEDIA_PRELAUNCH=PASS_ALL_PRELAUNCH_GATES` before the runner can start.
5. Accept technical Loop22 only with 44/44 captures, 44/44 native music files, 44/44 PCM48 delivery files, 44/44 AAC-LC outputs and 22/22 A/B pairs. A runner error/partial execution is not a PASS; preserve all logs and partial artifacts for diagnosis.
6. After technical PASS, operator must review visual/editorial/layout and listen to all 44 outputs. Human review remains a separate gate.

## Audio/timebase contract

Keep native C11-C FAMILY_MUSIC_V4 WAV PCM16 stereo 44.1 kHz unchanged. Create separate PCM16 stereo 48 kHz delivery copies with exact `duration_seconds × 48000` sample frames. AAC-LC is 192 kb/s, 48 kHz stereo. Preserve H.264 by stream copy. No gain, mixing, ducking, fades, crossfades, normalization, or video filters. D1 does not define post-AAC duration tolerance; record but do not invent one.

## Non-negotiable safeguards

- C11-C 2.19.12 immutable; `release/C11C_FREEZE_PACKAGE_MANIFEST.json` SHA-256 `e405d08e4d166b1ad9595358f4a088e73eea9527e6e89244beb4096eac4b953`.
- No protected mechanics/audio/RNG/binder/generator changes; no edits to `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, canonical definitions, D4.8 or D9.10 locks.
- No sixth module, parallel Producer or binder. R1P remains `PLAN_ONLY_NOT_D4_EXECUTABLE_COMPATIBILITY`.
- Renderer OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`.
- No D renderer, D3 V5, dispatch, production promotion or release. No Git checks; commits operator-managed; enforce source SHA pins and fail closed.

## Roadmap

E4C Drill follows only after Loop22 technical and human closeout; then E5 → E6 Smoke18 → E7 Matrix101 → E8. CH_008/CH_009 remain held pending authoritative reconciliation of the 11s declared duration vs 12s phase sum.
