# C11-C Producer 0.9.7 — Suite Member

Compact orchestration interface for Challenges, Visual Loops, Visual Drills and predefined reviews.

## Current C11-C state

Operational branch: C11-C 2.19.12 consolidated repair candidate. The Producer remains orchestration-only and does not implement mechanics, RNG, timing truth or rendering.

Supported content: 9 Challenges, 5 Visual Loop families / 27 grammars, 4 Visual Drill families. Predefined reviews include 9x6 Challenges, 27 Loops, 20 Drills and 5 Longforms.

Single Visual Drill production uses temporary AVI Movie Maker capture, stabilized file handling, video-only MP4 conversion, deterministic family music and central delivery profiles.

The Art Direction review runner is `tools/prototypes/c11c_bulk/run_c11c_art_direction_batch_v4.ps1`; `Workers=7` means genuine concurrent capture with private temporary Godot project roots and no mutex.

`c11c-suite/` is canonical. `c11c-studio/` is retired.
