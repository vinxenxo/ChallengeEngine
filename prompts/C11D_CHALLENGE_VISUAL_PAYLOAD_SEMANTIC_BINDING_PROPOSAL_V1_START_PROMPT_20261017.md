# C11-D START PROMPT — Challenge Visual Payload Semantic Binding Proposal V1

Continue from `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. Read `AGENTS.md`, `.continue/rules/CONTINUE.md`, `docs/current/d/MASTER_HANDOVER_C11D_CURRENT.md`, the V2-A capability matrix checkpoint, this semantic-binding proposal checkpoint and design document.

## Authoritative evidence from the operator checkout
- V2-A static capability matrix: PASS, 15/15 tests.
- selectors 9/9; source pins 43/43; mechanic routes 9/9; asset role refs 27/27; unique assets 15/15; custom_data inventory 9/9.
- Saved report SHA-256: `36c014734892fee2d7a1beb2662cd610c6856b4ecb48d9e06bf596f826795327`.
- C11-C manifest SHA-256: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; don't modify C11-C, its manifest, canonical seed V1, or simulation sources.
- Challenge planner preflight V2 saved report SHA-256: `1e41001f83cf9b093919f46ee2f327553c93464f8369ecfb0dc3b34b0a0c9d43`.

## Current task
Validate the added semantic-binding proposal contract and tests in the active Windows checkout. This increment is static-only. It must not call Godot, materialize a payload, write payload files, activate a renderer, generate media, or unlock release/promotion gates.

The nine selectors have three source-declared static target proposals (001, 002, 004) and six source fields proposed for review only (003 `target_x`, 005/006/007 `target_position`, 008 `active_selection`, 009 `displayed_count`). Every proposal must keep `binding_authorized=false` and `renderer_projection_approved=false`. Never serialize whole `FrameSnapshot.custom_data`.

Do not project `PILOT_0X100` to 2D or 1080x1920. Preserve challenge 004's V1 preview as a regression fixture. Keep Challenge 008 and 009 out of runtime materialization until their 11s declared total / 12s phase-sum conflict receives an explicit editorial/timebase decision. Music seed orthogonality remains untested at the Challenge source-only runtime boundary.

After the static proposal tests pass, design the selector-driven Godot runtime harness as a separate overlay and prove per-selector payload repeat determinism and real gameplay-seed visual sensitivity. Do not claim those results from this static proposal.

## Governance locks
`renderer=OFF`; `media_created=false`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `release_authority=NONE`.

Use add-only overlays, explicit SHA-256 preconditions, complete PowerShell 5.1 blocks, separate apply/test blocks and short staging paths. Avoid `$PSScriptRoot`, PowerShell 7-only syntax, partial snippets and success messages that can print after an exception.
