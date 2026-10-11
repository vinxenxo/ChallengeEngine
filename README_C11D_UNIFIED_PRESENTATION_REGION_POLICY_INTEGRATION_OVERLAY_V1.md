# C11-D Unified Presentation Region Policy Integration Overlay V1

## Purpose

Integrate a proposal-only semantic presentation-region policy into the C11-D unified content reviewer for Visual Loops, Visual Drills, and Challenges. This increment reconciles existing logical-composition and renderer-neutral frame-program declarations; it does not define rendering geometry or style.

## Shared field-region proposal

- `title` and `subtitle` -> `HEADER` for all three content types.
- `call_to_action` -> `FOOTER` for all three content types.
- `player_name` and `challenge_label` -> `CHALLENGE_OVERLAY` for Challenges only.
- `language` remains metadata-only.
- Semantic region labels are not coordinates. Region geometry, safe areas, margins, typography, colors/contrast, animation, compositing and family-specific variants remain unresolved and unapproved.
- Visibility timing remains the responsibility of separate editorial-window proposals; this policy infers no new windows.

## Unified review integration

Expected when run from the canonical, correctly pinned repository:

- Content types: 3/3.
- Existing runtime harnesses: 7/7.
- Cross-artifact checks: 17/17.
- Source lineage and declared source files: 22/22.
- Negative/guard checks: 30/30.
- A tenth unresolved gate explicitly records that shared semantic presentation-region policy is not approved.
- Review remains `REVIEW_CHAIN_CONSISTENT_NOT_VIDEO_READY`.

The Challenge summary now publishes delivery `duration_seconds` from the already-validated temporal-alignment proposal, allowing the audio/video duration-parity check to read an explicit delivery duration. This is report metadata only; it does not change simulation time, snapshots, `winning_frame`, `close_calls`, source frames or rendering.

## Governance

This overlay does not approve any policy and does not emit renderer-native input, activate a renderer, create media, alter C11-C, or grant release authority. The frozen C11-C manifest must match SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. All source-pin mismatches are rejected.

`D4.8` remains blocked, renderer remains OFF, `media_created=false`, and `release_authority=NONE`. A successful contract review is not video readiness or authorization to render.
