# C11-D Start Prompt V19 — Allowlisted Coordinate Consumer Specification

Work in `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS` with PowerShell 5.1-compatible additive overlays. Start from the latest operator-confirmed state in `docs/current/d/C11D_FULL_CONTEXT_CONTINUITY_CHECKPOINT_20261021_V19.md`.

The coordinate-policy decision gate is closed with `2756/2756` tests; receipt SHA-256 `b61fb3403e0ad5725937be05f8a7153c3cf35ccde167306f45151ece0f1cc4cb`. Continue by validating `definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_ALLOWLISTED_COORDINATE_PROJECTION_CONSUMER_SPECIFICATION_V1.json` and its closed schema/regression suite. This is specification-only: no production consumer code, renderer-native input, render test, or media.

Maintain the exact allowlist: CHALLENGE_003.target_x; CHALLENGE_005/006/007.target_position. Keep CHALLENGE_008 and CHALLENGE_009 blocked. Read only the one allowlisted `FrameSnapshot.custom_data` key per frame; never serialize the dictionary. Preserve source order/cardinality, no interpolation/extrapolation, validate finite/in-domain samples, and fail closed on the entire track.

Do not modify C11-C, challenge JSON files, CoordinateMapper, source frame timeline, simulation or RNG. Keep `renderer=OFF`, candidate input inadmissible, bindings zero, D4.8 blocked and D10 blocked for promotion. Next engineering step after tests: implementation design plus negative tests in an isolated review-only surface; do not enable renderer until its formal gate unlocks.
