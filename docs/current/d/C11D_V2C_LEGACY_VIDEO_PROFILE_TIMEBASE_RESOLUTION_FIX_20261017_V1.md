# C11-D V2-C Legacy Video Profile Timebase Resolution Fix V1 — 2026-10-17

## Purpose

Correct a source-frame harness defect discovered in the first Windows Godot smoke process. `ChallengeRuntimeBridge.run_effective_pipeline` supports both (a) native-V2 inline `runtime_input.video` dictionaries containing `fps` and `game_duration`, and (b) legacy `runtime_input.video` strings naming a VideoProfile. The original V2-C harness accepted only dictionaries and therefore incorrectly blocked the first two legacy-fallback mechanics before examining their effective timebase.

## Change

The in-memory harness now resolves string profile IDs through the same pinned `VideoProfileRegistry.gd` path that the runtime bridge uses. It requires a valid profile, `fps`, and `phases.game_duration`; it then compares effective FPS and game duration with the selected challenge's pinned `source_timebase` before validating frame cardinality. Missing profiles, invalid profile shapes, unsupported binding types, and timebase drift fail closed with distinct reasons. No source config/profile is edited or synthesized.

A Python regression checks both declared legacy profile mappings (`f4_legacy_60_h0_g7_r0_c2` for CHALLENGE_001 and `f4_legacy_60_h3_g7_r0_c0` for CHALLENGE_002) against the pinned selector timebase, and requires the source-drift guard.

## Scope limits

- This change does not modify Challenge JSON, mechanic code, RNG, simulation input/results, the bridge, or the profile JSON files.
- The CHALLENGE_004 V1 harnesses remain untouched.
- No `FrameSnapshot.custom_data` values or map are serialized.
- `approved_bindings=0`; renderer remains OFF; payload/media are not created.
- CHALLENGE_008/009 declared-total-vs-phase conflicts remain unresolved and timeline acceptance remains out of scope.
- This guard fix is not runtime acceptance. It must pass the added Python regression and a real Godot 4.7.1 Mono `CHALLENGE_001` smoke before the V2-C nine-selector runner is resumed.

## Verification

The source profile mapping in the pinned `ChallengeRuntimeBridge.gd` maps the two legacy challenge source timebases to the two named profiles above. Each profile has 60 FPS and 7 seconds of game duration, matching the selected challenge's pinned frame timebase. The runtime frame count should therefore be 420 for either profile; any divergent runtime profile is rejected before receipt emission.

## Governance

All V2-C and C11-D governance locks remain unchanged. This document is a distinct add-only fix note; it does not replace the V6 continuity checkpoint or claim a V7 checkpoint is installed.
