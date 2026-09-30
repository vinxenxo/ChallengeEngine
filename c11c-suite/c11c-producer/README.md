# C11-C Producer 0.9.7 — Suite Member

Compact orchestration interface for single production and predefined reviews.

## Supported single production

- **Challenges:** `CHALLENGE_001` … `CHALLENGE_009`, using canonical Challenge definitions and production launcher.
- **Visual Loops:** 5 families / 27 grammars.
- **Visual Drills:** Tracking, Saccade, Pursuit and Peripheral Scan.

## Predefined reviews

- `REVIEW — 9 CHALLENGES × 6 SEEDS`
- `REVIEW — 27 VISUAL LOOPS`
- `REVIEW — 20 VISUAL DRILLS`
- `REVIEW — 5 LONGFORMS`
- combined review operations.

## Suite ownership

The live Producer is under `c11c-suite/c11c-producer/`. `c11c-studio` is retired and is not a dependency.

## Visual Drill capture

The single-Drill Producer uses temporary AVI Movie Maker capture, waits for the file to stabilize, converts video-only to MP4, then generates/muxes deterministic family music and resolves the requested delivery profile.

## Art Direction worker review

The canonical batch runner is `tools/prototypes/c11c_bulk/run_c11c_art_direction_batch_v4.ps1`. Its 2.19.6 worker model uses a private temporary Godot project root per concurrent worker; the Producer does not own or serialize that pool.

## Backend safety

The GUI remains orchestration-only. It does not implement mechanics, RNG, timing truth or rendering.
