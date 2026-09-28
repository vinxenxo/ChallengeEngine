# C11-C Producer 0.9.7 — Suite Member

Compact cyberpunk orchestration interface for single production and predefined reviews.

## Supported single production

- **Challenges:** `CHALLENGE_001` … `CHALLENGE_009`, using canonical Challenge definitions and production launcher.
- **Visual Loops:** 5 families / 27 grammars.
- **Visual Drills:** Tracking, Saccade, Pursuit and Peripheral Scan.

## Predefined reviews

- `REVIEW — 9 CHALLENGES × 6 SEEDS` — historical C11-A.1 qualification/review matrix.
- `REVIEW — 27 VISUAL LOOPS`
- `REVIEW — 20 VISUAL DRILLS`
- `REVIEW — 5 LONGFORMS`
- existing combined review operations.

The Challenge review is deliberately routed to `tools/qa/c11/run_c11a1_challenge_bulk_qa.ps1`; it does not reinterpret historical Challenge mechanics as C11-C mechanics.

## Queue isolation

A failed seed is recorded on the recipe and the remaining seeds continue. A failed batch/utility item is removed from the active queue and the next queued item starts automatically. The Producer does not use a modal error dialog for per-seed failures.

## Drill generation

Visual Drill envelope generation uses a direct `ProcessStartInfo` path so the Godot user argument after `--` is passed reliably on Windows PowerShell. Generator stdout/stderr are retained in the temporary producer stage when an envelope launch fails.

## Backend safety

The GUI remains orchestration-only. It does not implement mechanics, RNG, timing truth or rendering.

## Visual Drill capture

The single-Drill Producer does not depend on AVI or PNG sequences. Godot Movie Maker writes one temporary OGV container in the scratch directory; the runner waits for the container to stabilize, then FFmpeg converts its video stream into the canonical source MP4. The OGV is removed with the temporary stage after production.
