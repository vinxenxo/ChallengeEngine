# C11-E Continuation Master Prompt — V111 (2026-11-09)

Continue from the sole active checkout: `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. Evidence ZIPs are read-only inputs and must never be extracted over the checkout. The operator manages commits. Do not run Git/HEAD/status/branch checks. Use SHA-256 source pins and fail closed. Windows PowerShell 5.1; Python 3.13.

## Current phase / exact state

E4A accepted. E4B family mapping accepted. R1P 27/27, Loop22 projection 22/22 and five policy fingerprints approved. R1V five-selector/ten-output A/V pilot is closed and operator-accepted; do not repeat.

Loop22 V1 execution install succeeded (16/16 files, 30/30 source pins). V1 wrapper stopped at PowerShell line 26 because normal Python unittest stderr became a terminating native-command error under `$ErrorActionPreference=Stop`; no media launch. The V2 add-only .NET process bridge install succeeded (11/11 files, 37/37 source pins). On Windows, its stream/exit-code self-test passed, PS AST and Python AST passed, all 24 focused tests passed and the prelaunch marker was emitted.

The pinned V1 Loop22 runner then exited 2 during output-directory bootstrap, before the first media launcher. Exact error: WinError 183 for the already-created shared path `source/geometric/A`. The 44 logical jobs share physical directories by family/repeat and role; V1 attempted to create all 176 logical directory references rather than the 40 unique physical directories. The evidence archive has an empty `processes` directory, empty output skeleton, empty runner stdout and only the FileExistsError in stderr. This attempt has zero C11-C launches, music generations, PCM conversions, muxes and AV outputs. Do not recover or repeat any capture from that attempt.

Read `C11E_E4B_LOOP22_AV_SHARED_DIRECTORY_COLLISION_ROOT_CAUSE_V1.md` and `C11E_E4B_LOOP22_AV_PS_NATIVE_STDERR_ROOT_CAUSE_V1.md` for incident histories.

## Immediate action — shared directory fix

Install `C11E_E4B_LOOP22_AV_SHARED_DIRECTORY_FIX_V1_20261109.zip` from a new Downloads folder, never over the checkout. Require `PASS_ADD_ONLY_INSTALL`, 37/37 inherited V2 pins, 13/13 payload files and 13 added files. It adds only a new Python runner V2, test V2, PS wrapper V3 and versioned docs. It does not overwrite the original V1 runner, V1 tests, support V1 or V2 bridge wrapper.

Then run only:

`powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\tools\c11d\d9\RUN_C11E_E4B_LOOP22_AV_QUALIFICATION_V3.ps1" -ProjectRoot "C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS"`

V3 must verify the V1 and V2 installation receipts, the V2 bridge wrapper SHA, all 37 inherited source pins, frozen C11-C manifest and R1P archive. It runs the native-process bridge self-test (stdout/stderr separation and exit codes 0/23), PS5.1 AST, Python 3.13 AST and exactly 25 focused tests. Test 25 proves 44 jobs yield exactly 40 unique directories; it creates each directory once with `exist_ok=False` and confirms duplicate exclusive creation still fails. No media process may start before every gate passes.

## Loop22 fixed scope and contract

22 selectors: R1P receipt indices 2–5, 7–10, 12–15, 17–20, 22–27; family distribution 4/4/4/4/6. Two repeats A/B per selector = 44 new C11-C silent capture invocations, 44 native FAMILY_MUSIC_V4 PCM16 stereo 44.1 kHz WAVs, 44 separate exact-sample PCM16 stereo 48 kHz delivery WAVs, 44 AAC-LC 192 kb/s / 48 kHz stereo MP4 outputs with H.264 stream copy, and 22 deterministic A/B comparisons. Keep gameplay_seed and music_seed separate. No gain, mix, normalization, fades, crossfades or video filters. No D3 V5 or D renderer.

Technical acceptance only: `PASS_E4B_LOOP22_AV_QUALIFICATION_44_OF_44_PENDING_OPERATOR_VISUAL_AUDIO_REVIEW`. Then operator visual/editorial/layout review and listening acceptance for all 44 remain mandatory. E4B closes only after both.

## Roadmap

After Loop22 technical + human closeout: E4C Drill → E5 cross-family determinism/seed isolation/GUI-CLI parity → E6 Smoke18 → E7 Matrix101 (CH_008/CH_009 held until authoritative 11s-vs-12s resolution) → E8 full historical C-to-E regression, independent acceptance, immutable freeze and separate explicit promotion.

## Permanent safeguards

C11-C 2.19.12 immutable; frozen manifest SHA `e405d08e4d166b1ad9595358f4a088e73eea9527e6e89244beb4096eac4b953`. No protected mechanics/audio/RNG/binder/generator/SimulationResult/winning_frame/close_calls/WinningFrameDetector/RenderedFrameStream changes. R1P stays `PLAN_ONLY_NOT_D4_EXECUTABLE_COMPATIBILITY`. Renderer OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`. No dispatch, production promotion or release. No Git checks; commits operator-managed.
