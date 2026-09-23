# C11-C 2.3.2 — Test runner / Tracking playback hotfix

## Test runner

- `tests/run_all.py` now drains Godot output with `communicate()` instead of iterating directly over the pipe.
- A per-suite timeout of 120 seconds prevents a non-terminating Godot test from blocking the complete logical corpus indefinitely.
- UTF-8 decode errors are replaced rather than terminating the runner.
- Fatal-pattern scanning is preserved after process completion and timeout diagnostics print the final output lines.

## Tracking playback test

- `C6F08TrackingPlaybackValidationTest.gd` now has a 180-process-frame watchdog.
- A playback that never reaches `playback_finished` becomes a normal test failure instead of an infinite wait.

## Tracking scope

- No Tracking mechanic change.
- Current baseline remains one-target `tracking/smooth_pursuit` with bounded analytic Lissajous motion.
- A future pre-drawn guided-path Tracking variant is explicitly deferred; it is not implemented in this hotfix.

## Frozen boundaries

No changes to Challenge simulation, `SimulationResult`, `winning_frame`, `close_calls`, structural RNG ownership, C7 audio contracts, C9 authoring contracts, or C11-B logical geometry.
