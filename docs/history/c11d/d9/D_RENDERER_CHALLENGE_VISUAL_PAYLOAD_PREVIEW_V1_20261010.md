# D9 — Challenge Visual Payload Preview V1 (2026-10-10)

Introduces an in-memory source-timebase logical visual payload for `CHALLENGE_004`. The harness calls the frozen effective runtime twice, verifies deterministic source frames, rebinds presentation to `social_default_v1` on a deep copy, loads the three canonical SVG assets as `Texture2D` resources, captures resource hashes/dimensions, and constructs 420 visual transform records from the authentic GAME snapshots.

The payload deliberately excludes gameplay telemetry and does not use `winning_frame` or `close_calls` to choose samples. It preserves source coordinates, model geometry and 60 FPS frames without applying delivery resampling or a coordinate projection. It does not instantiate render nodes, dispatch renderer input, write files or create media.

Acceptance is pending the user-side Godot 4.7.1 harness run. C11-C immutability, `PREPARE_ONLY`, `D4.8=BLOCKED`, `release_authority=NONE`, and the D9.14/D9.16/D9.17/D10 gates remain unchanged.
