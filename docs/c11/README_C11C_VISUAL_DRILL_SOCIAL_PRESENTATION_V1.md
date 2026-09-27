# C11-C Visual Drill Social Presentation v1.0

## Baseline

Parent engineering baseline:

`ChallengeEngineV01_C11-C2.1.4-LATEST-FREEZE.zip`

SHA-256:

`f4ceb95fd506d1ea40e70c0f2102c91e8e29b30acc0d5c0a0b032f69765d1996`

## Scope

This overlay moves Visual Drills onto the shared C11-C social/editorial presentation path.

It does not reopen C11-B, simulation, RNG ownership, `SimulationResult`, `winning_frame`, `close_calls`, C7 or C9 contracts.

## Shared presentation

Both Visual Loops and Visual Drills use:

- logical social frame: 540x960;
- Header: 0..144;
- Body: 144..816;
- Footer: 816..960;
- physical social delivery: 720x1280, 9:16, 30 FPS;
- common typography, centered fitting, decorative rules and three-line footer;
- common presentation-only editorial layer.

Matrix / split-flap is enabled only when the family binder requests it. Visual Drills request `false`.

## Audio

`C11CSafeAmbient.py` remains the compatibility entry point used by the existing Visual Loop launchers, but now delegates to the canonical global ambient generator.

The master bed is fixed at 18 seconds. A shorter render receives the exact prefix of that master; a longer render loops the same master. Seed, family and loop count do not alter the audio waveform.

## Modern Visual Drill review

Use the new launcher:

```powershell
.\tools\prototypes\c11c_bulk\run_c11c_visual_drill_review.ps1 -ResetReviewAssets
```

Default corpus:

- Tracking × 5 seeds
- Saccade × 5 seeds
- Pursuit × 5 seeds
- Peripheral Scan × 5 seeds

Total: 20 physical renders.

Output root:

`artifacts\prototypes\c11c_visual_drills_review\`

Each render contains MP4, review GIF, five keyframes, contact sheet, social sidecar and manifest.

`-NoSound` keeps the same video-only workflow but disables audio muxing.

## Envelopes

The launcher reuses the current C11-A qualification envelopes as the input authoring corpus. This deliberately separates:

`legacy envelope generation → modern C11-C presentation capture`

The old C11-A QA output is not treated as the social product format.

## Validation

Python syntax can be validated in a non-Godot environment with:

```powershell
python -m py_compile tools\prototypes\c11c_common\generate_c11c_ambient_audio.py tools\prototypes\c11c_common\C11CSafeAmbient.py
```

The repository's Godot suites must still be run on the user's Windows/Godot 4.7.1 environment because Godot is not available in this container.
