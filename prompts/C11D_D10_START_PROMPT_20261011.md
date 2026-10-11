# START PROMPT — ChallengeEngine C11-D — 2026-10-11

You are continuing an existing engineering project, not starting a new one. Work in Spanish. Be precise, evidence-driven and incremental. Do not ask me to repeat constraints that are documented in the attached repository.

## Attachment
I am attaching the project ZIP named:

`ChallengeEngineV01_STATELESS_C11-D10_LATEST_20261011_203730.zip`

This is the expected filename for the latest locally verified source. Verify that the attachment actually exists, calculate its SHA-256, check archive integrity, inspect the tree and read the repository's current roadmap/checkpoint docs before making changes. Do not infer contents, hashes, or test results from the filename.

## Mission
Continue C11-D after the user-reported green state for the unified review integrations covering Visual Loops, Visual Drills and Challenges, including delivery timebase and technical audio/music delivery timing proposals. First establish the exact state from the attached ZIP and then continue the roadmap with the next smallest, highest-value increment.

The broader goal is to normalize shared presentation, editorial, delivery and review standards across the three content types; preserve deterministic GUI/CLI parity; explicitly resolve every policy and gate; and only then proceed through separately authorized renderer-baseline and acceptance steps.

## Absolute freeze / release rules
1. C11-C 2.19.12 is immutable. Frozen package:
   `ChallengeEngineV01_STATELESS_C11-C_2.19.12_FROZEN_20260930_175709.zip`
2. Its frozen manifest SHA-256 must remain:
   `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`
3. Do not change C11-C mechanics, RNG, `SimulationResult`, `winning_frame`, `close_calls`, frozen geometry or `release/C11C_FREEZE_PACKAGE_MANIFEST.json`.
4. `winning_frame` is a read-only temporal anchor. `close_calls` is an episode count, never a time value.
5. D9.10 is `PREPARE_ONLY`: no renderer-native input and no dispatch.
6. Keep `renderer=OFF`, `media_created=false`, `D4.8=BLOCKED`, `release_authority=NONE`.
7. D9.14 and D9.16 full acceptance remain blocked until there is a separately approved/frozen D renderer baseline and explicit D4.8 authorization. D9.17 remains BLOCKED/NO-GO; D10 remains blocked as a production/release gate.
8. A green test, consistent review, source hash pin, or clean ZIP does not grant approval to render, create media, freeze a D baseline or release.

## Current known proposals (verify in the attachment)
- Delivery profile metadata proposal: `REVIEW_720`, 720×1280, 30 FPS.
- Loop: 600 frames at 30 FPS = 20 s, no resampling.
- Drill: 630 frames at 30 FPS = 21 s, no resampling.
- Challenge `CHALLENGE_004`: 900 frames at 60 FPS = 15 s → 450 frames at 30 FPS. Proposed cumulative half-up phase boundaries `[0,180,600,780,900]` → `[0,90,300,390,450]`.
- Challenge GAME snapshots: 420 → 210 by even-local-index selection, proposal only; no interpolation.
- Proposed audio delivery metadata: AAC-LC, 192 kb/s, 48 kHz, stereo, with pre-encode audio timeline matching the proposed video duration. This does not choose music, secure rights, mix, normalize loudness or generate audio.
- Shared editorial/semantic-region mapping is not approved unless the repository has a newer explicit decision record.

These values are proposals, not authorized renderer behavior. Confirm current schemas, markers, unresolved gate counts and test names from the attachment rather than relying on historical summaries.

## Immediate work plan
1. Verify attachment SHA-256 and archive integrity; extract to a fresh working directory without modifying the original ZIP.
2. Read `AGENTS.md`, `README.md`, current roadmap, `docs/current/d` checkpoints, latest D9 history, baseline candidate records and frozen manifest.
3. Inventory source changes, documentation changes and latest test evidence. Identify contradictions or stale docs.
4. Confirm the latest unified-review marker and all unresolved gates.
5. Continue with shared presentation/editorial policy parity across Loop, Drill and Challenge. Derive field mappings/semantic regions only from real repository artifacts; do not invent coordinates, typography, colors or animation.
6. Keep technical audio delivery separate from music selection, licensing, sound design, mixing, loudness and encode behavior.
7. Implement the smallest isolated overlay; include only new/modified files. Add source hash pins, schema validation, positive/negative tests and cross-artifact checks.
8. Run focused tests, then integrated Godot unified review, lifecycle, baseline-candidate preflight and C11-C regressions as applicable. Record exact output and exit codes.
9. Update checkpoint, history, roadmap and prompts from verified results.
10. Report the next exact step, ZIP name, SHA-256 and PowerShell apply/test commands.

## Working conventions
- Local project path: `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`.
- I run commands in Windows PowerShell and provide outputs. Do not claim you executed my local tests.
- Prefer small ZIP overlays, not `.patch` files or full repository ZIPs unless requested.
- Never fabricate sandbox links, SHA values, test markers, or approval states.
- Do not pause to ask me to choose among ordinary engineering steps. Inspect the repository and proceed with the safest logical next step; ask only when an explicit product/approval decision is genuinely required.
- Be transparent when the available archive or environment is incomplete.
