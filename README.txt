C11-C 2.17.8 — CHALLENGE VIDEO DELIVERY STANDARD + CAPTURE VALIDATION REPAIR

Apply over the installed 2.17.x Challenge-production state.

Fixes and contract work:
- Challenge Movie Maker source capture remains native 540x960.
- FFprobe of the real source AVI is authoritative for width/height/FPS/frame count; log text is telemetry only.
- Godot stdout/stderr are decoded as UTF-8 to preserve Unicode diagnostics.
- Windows custom arguments remain single native arguments: --config=<path> and --audio-output=<path>.
- Delivery is post-capture FFmpeg scaling: 540x960 -> 720x1280, 1080x1920 or 540x960.
- MASTER_1080 (1080x1920) is the default product delivery profile; REVIEW_720 remains C11-C review evidence.
- Challenge timing derives only from hook+game+reveal+cta phase durations; stale total_duration is ignored.
- Detailed current and historical docs are included under docs/current/ and docs/history/.
- Frozen mechanics, RNG, SimulationResult, winning_frame, close_calls, C11-B geometry, C7 and C9 are untouched.

Do not run the 54-run Challenge bulk QA until the single CHALLENGE_001 smoke passes.
