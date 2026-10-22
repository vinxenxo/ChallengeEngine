# C11-D Start Prompt V20 — Allowlisted Coordinate Consumer Implementation Design

Work in `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS` using PowerShell 5.1-compatible ADD_ONLY overlays. Continue from `docs/current/d/C11D_FULL_CONTEXT_CONTINUITY_CHECKPOINT_20261022_V20.md` and the operator-confirmed V2-B consumer specification suite PASS `1038/1038` (receipt SHA-256 `c52d3f5ca276beea0482eb1ab521d163e201023f818e9448f6f7279c306b2ef0`).

The current increment defines a design contract and planned 261-case negative test matrix only. Do not claim the runtime matrix has executed. Next, implement the consumer as an isolated review-only GDScript helper after this design suite is accepted. Keep it outside production dispatch; do not create scene/render nodes, load assets, call RenderingServer, persist a payload, create media, or enable renderer.

Exact accepted pairs: `CHALLENGE_003.target_x`, `CHALLENGE_005.target_position`, `CHALLENGE_006.target_position`, `CHALLENGE_007.target_position`. `CHALLENGE_008` and `CHALLENGE_009` remain blocked.

Per source frame, perform only one exact `custom_data.get(allowlisted_key, sentinel)` lookup; never enumerate, duplicate, log, stringify, hash, or serialize the whole dictionary. Preserve source frame cardinality and ordinal; no interpolation, extrapolation, resampling, clamping, rounding, or `winning_frame` selection. On any invalid sample, reject the entire track with no partial output.

Permanent governance: C11-C manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` immutable; `renderer=OFF`; bindings zero; no payload/media; candidate input inadmissible; D4.8/D9.14/D9.16 blocked; D9.17 blocked no-go; D10 blocked for promotion; release authority none. Production wiring and render-test authorization require later explicit gate closure.
