# C11-E Continuation Master / Overhand Prompt — V59

Continue the project in the live Windows checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. It is the only working source authority. Never extract a ZIP/snapshot over it. The operator controls commits; never stage, commit, reset, clean, switch branch, rebase, amend or push.

## Read first

1. `AGENTS.md`
2. `.continue/rules/CONTINUE.md`
3. `README.md`
4. `docs/current/e/C11E_CURRENT_AUTHORITY_20261105_V61.md`
5. `docs/current/e/C11E_GATES_ACCEPTANCE_MATRIX_20261105_V59.md`
6. `docs/current/e/C11E_E3_EXECUTION_BACKLOG_20261105_V36.md`
7. `docs/history/c11d/C11D_TO_C11E_FULL_FAMILY_ROADMAP_20261105_V49.md`
8. `docs/current/e/C11E_E4A_CHALLENGE_LOOP_DRILL_ALIGNMENT_20261105_V16.md`
9. V4 postmortem, V6 postprocess plan and the V1 source-divergence record listed in the current documentation index.

Root docs are V18-era and contain a malformed 63-character manifest SHA. Canonical frozen manifest: 796,318 bytes / SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

## Immediate position and action

The existing Movie Maker AVI is complete and immutable: SHA-256 `135dae5c21e6a459cefce7a1bacafe5d4aeec0886b6acda88652de81515abf0b`, 540x960, 60 FPS, 900 frames, 15 seconds. Do not launch Godot or Movie Maker again.

Postprocess history: V1 stopped at preflight due to a 63-character SHA literal. V2 surfaced an empty process ExitCode at SOURCE_FFPROBE. V3 fixed process capture and generated/probed the silent normalized MP4, but boundary extraction failed because the operator's FFmpeg rejects `-vsync`; its second run refused to overwrite the MP4. V3 is not PASS and has no complete receipt. Immediate action is the V4 runner from Downloads. V4 must revalidate/reuse the existing V3 MP4 if it meets the H.264 High 720x1280/30 FPS/450-frame/15-second/`yuv420p`/`tv`/zero-audio contract. Otherwise it encodes a temporary candidate, verifies before promotion, and preserves invalid prior output. It uses `-fps_mode vfr`, not `-vsync`, to extract the eight selected boundary PNGs into a fresh workspace, then creates the contact sheet and writes the versioned docs add-only. Do not rerender.

## Critical source divergence — do not ignore

The frozen C11-C manifest pins original `GeneradorMaestro.gd` SHA `4f10144c62c7bc149bd46aa37494b1df40c7185544b8477153150eec71c1aaf9`; the active D-only postimage is `d42782e8f5bb94ff0ede653a1c4624dc91541cc8203abf136b09a8fc288a7d82`. The manifest/frozen artifact remain unchanged, but this active file does not match that manifest entry. Do not modify or restore the file blindly. Resolve the D/E source-isolation decision before further runtime edits.

## Ordered gates

1. Run V4 postprocess once using the existing AVI/MP4; no capture rerun.
2. Resolve the C11-C/D-E source-isolation boundary.
3. Complete full E4A D-composited A/V with D3 V5, D3.3 mastering, accepted mux/FFprobe, exact duration, independent gameplay/music seeds, A/B same music seed and C changed seed, identical video elementary stream, AAC 48 kHz stereo, non-silent audio, <=0.15 s A/V drift, human listening/visual review and GUI/CLI parity.
4. Only after full E4A acceptance open E4B Loop, then E4C Drill; then E5 determinism/seed/family isolation and GUI/CLI parity; E6 Smoke18; E7 Matrix101; E8 historical regression, independent acceptance, freeze and separate promotion.

CH_008/CH_009 remain held because the declared duration is 11s while phases sum to 12s (3+7+0+2).

## Permanent invariants

C11-C 2.19.12 frozen artifact and manifest immutable. Do not change mechanics, RNG ownership, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, protected binders, core audio or canonical definitions. `request.seed` and `request.music_seed` independent; automatic seed generation disabled; no `FrameSnapshot.custom_data` serialization. No sixth Suite module, second Producer or parallel binder. Production renderer/dispatch/media OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`.

## Engineering behavior

Avoid unnecessary launchers, installers and repeated accepted tests. Read live source/docs before decisions. Use one purpose-built runner and only essential checks. Make reruns resumable where safe; never overwrite an existing deliverable without validating it or preserving it first. Any accepted transition updates authority, matrix, backlog, roadmap, alignment, master prompt, start prompt and first prompt. Do not claim PASS until a Windows receipt exists.
