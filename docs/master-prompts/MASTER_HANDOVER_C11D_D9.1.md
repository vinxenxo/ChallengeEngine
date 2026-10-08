# C11-D D9.1 — Master Handover

Continue from D8.7 PASS_NO_MEDIA.

D9.1 is the first explicit physical media pilot.

Pilot: `CHALLENGE_001`, seed `12345`, music_seed `840001`, `REVIEW_720`, mode `REVIEW`, audio OFF.

Use the existing C11-C challenge production runner only as a physical renderer bridge:
`tools/prototypes/c11c_bulk/run_c11c_challenge_production.ps1`

The bridge must never alter C11-C simulation truth, RNG, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7/C9 or logical 540x960 geometry.

Physical output belongs only under `artifacts/tests/c11d_d9/d9_1/pilot_media/`.

This pilot is not a release. `release_authority=NONE`. General production remains disabled. Bulk execution is forbidden.
