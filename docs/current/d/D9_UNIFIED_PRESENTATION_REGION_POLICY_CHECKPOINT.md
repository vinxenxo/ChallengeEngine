# D9 Unified Presentation Region Policy — Checkpoint

**Checkpoint date:** 2026-10-11  
**State:** Proposal integration prepared; canonical Windows checkout verification required after applying the overlay.

## What is now represented

The unified review contract includes proposal-only semantic region mapping across `visual_loops`, `visual_drills`, and `challenges`:

| Editorial field | Semantic region | Scope |
|---|---|---|
| `title` | `HEADER` | All three content types |
| `subtitle` | `HEADER` | All three content types |
| `call_to_action` | `FOOTER` | All three content types |
| `player_name` | `CHALLENGE_OVERLAY` | Challenges only |
| `challenge_label` | `CHALLENGE_OVERLAY` | Challenges only |
| `language` | Metadata only | All three content types |

Region names carry no coordinate, safe-area, typography, styling, animation, or compositing implication. Timing remains owned by the already separate editorial-window proposals.

## Unified gate / expected report

The integrated reviewer expects 17 cross-artifact checks, 22 pinned lineage entries, seven runtime harnesses, and ten unresolved gates. The added gate is `SHARED_PRESENTATION_SEMANTIC_REGION_POLICY_NOT_APPROVED`. The report must remain `REVIEW_CHAIN_CONSISTENT_NOT_VIDEO_READY`.

Challenge delivery duration is included as report metadata derived from the validated delivery timeline so audio/video duration parity is explicitly inspectable. No simulation data or renderer inputs are changed.

## Verification status and limitation

The proposal module, contract and strict schema were checked structurally during preparation. The unified reviewer test reached its pass marker in the preparation copy after restoring a previously existing coordinate-projection harness file. However, the available preparation copy does not carry the canonical frozen manifest bytes: its `release/C11C_FREEZE_PACKAGE_MANIFEST.json` SHA-256 is `36080b1bbfa7877d40b6ef00b8131f28d7f368072971801f5c2452b4d7cc1478`, while the only acceptable frozen value is `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. Source verification therefore must be confirmed in the user's full canonical checkout; source pinning is intentionally strict and does not permit this mismatch.

Do not interpret a preparation-copy result as proof of Godot orchestration. After overlay application, run the presentation-policy test, unified Python contract suite, Godot unified reviewer, lifecycle test, baseline-candidate preflight and C11-C self-test in the full repository.

## Governance remains locked

- Frozen C11-C 2.19.12: immutable.
- Renderer: OFF.
- Renderer-native input: not emitted.
- Media: not created.
- `D4.8`: `BLOCKED`.
- Release authority: `NONE`.
- D9.14/D9.16 acceptance: blocked; D9.17: no-go; D10: blocked.
