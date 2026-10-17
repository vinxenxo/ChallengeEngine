# C11-D Challenge Visual Payload Capability Matrix V1 — Checkpoint (2026-10-17)

## State
The Challenge Seed-Domain Planner Preflight V2 was operator-confirmed PASS: 9/9 selectors, 27/27 variant cases, 27/27 repeat consistency, 27/27 D4 parity, request/plan seed sensitivity 9/9 each, editorial invariance 9/9, negatives 5/5; 54 plan invocations, zero Godot invocations, zero payloads. Saved report SHA-256: `1e41001f83cf9b093919f46ee2f327553c93464f8369ecfb0dc3b34b0a0c9d43`.

This overlay introduces V2-A static capability/lineage audit, not the visual payload implementation. It pins nine Challenge source JSON files, the nine mechanic implementations and canonical registry, runtime bridge/timeline/presentation/frame contracts, 15 unique assets and the existing Challenge_004 V1 preview pathway.

## Important findings encoded into the executable contract
- The static inventory covers all nine source selectors and 27 asset-role references.
- `FrameSnapshot.custom_data` is an inventory only. No wholesale serialization or automatic use of scoring/telemetry fields is permitted.
- Potential visible data such as `target_position`, `target_x`, `active_selection`, and `displayed_count` require explicit per-mechanic semantic review; none is approved for binding yet.
- The V1 Godot visual-payload preview remains Challenge_004-only. V2-A must not imply the other eight are runtime validated.
- `CHALLENGE_008` and `CHALLENGE_009` have an explicit 11-second total and phase components summing to 12 seconds. The contract reports both as unresolved.

## Next acceptance sequence
1. Run this overlay's Python unit suite in the Windows checkout.
2. Run the read-only V2-A capability matrix with `--full-report`, capture stdout/stderr, saved report and SHA-256 evidence.
3. Review the resulting per-selector field inventory before designing a V2 Godot materializer. Do not implement bindings from raw `custom_data` until a per-mechanic allowlist exists.
4. Resolve the two duration contradictions through an explicit editorial/timebase decision, separately from payload code.
5. Only then design a selector-driven Godot harness using the canonical `ChallengeRuntimeBridge.run_effective_pipeline`, per-selector source pins, repeat determinism, gameplay-seed sensitivity and music-seed orthogonality.

## Locked governance
`renderer=OFF`; `media_created=false`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `release_authority=NONE`; no promotion/freeze eligibility. C11-C manifest SHA remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
