# C11-C 2.18.8 — PNG Capture + C11-A.1 Isolation

Apply this overlay on top of the already-applied C11-C 2.18.7 Producer AVI hotfix.

## Repairs

1. Single Visual Drill Producer no longer captures AVI. Godot Movie Maker writes a temporary PNG sequence and FFmpeg encodes it to MP4.
2. Producer GUI no longer exposes the obsolete AVI retention control.
3. C11-A.1 quarantines any root `override.cfg` before invoking the historical factory, removes leaks, and restores the original file afterward.
4. New contract coverage is registered in `tests/run_all.py`, so console and Suite GUI regression use the same canonical test registry.

## Frozen boundary

No C11-B simulation truth, RNG ownership, SimulationResult, winning_frame, close_calls, WinningFrameDetector, RenderedFrameStream, C7 ownership, C9 semantics, or logical 540x960 social geometry are modified.
