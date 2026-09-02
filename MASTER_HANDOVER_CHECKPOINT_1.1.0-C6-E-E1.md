# MASTER HANDOVER CHECKPOINT — 1.1.0-C6-E-E1

## Status

C6-D4 remains CLOSED / CERTIFIED.

C6-E Step 0 and E1 are IMPLEMENTED but require Godot 4.7.1 runtime certification before E1 is formally closed.

## Frozen baseline

Simulation truth remains sovereign.
RNG streams and seeds remain frozen.
`SimulationResult` and winning-frame mathematics remain frozen.
`VideoTimeline` remains the sole temporal boundary source.

## Step 0 — Output contract

```text
Logical simulation canvas : 1080 × 1920
Godot source movie        : 540 × 960
Master MP4               : 1080 × 1920
Master codec             : H.264
Master pixel format      : YUV420-compatible
Transcode                : scale=1080:1920:flags=lanczos
```

The factory and manifest now encode this explicitly and FFprobe validates it.

## Step 1 — Asset integrity

Layer 0 rejects missing/empty/non-`res://` mandatory assets before simulation/render.
`CHALLENGE_009` received the missing `count_background.svg` asset.

## Step 2 — Presentation Profile

`PresentationProfile.gd` is presentation-only and selected declaratively with `presentation.profile`.
It supports source/master canvas contract, safe area, typography scale, composition hints, theme and asset family identity.

## Tests

Added:

```text
C6EAssetIntegrityTest.gd
C6EPresentationProfileIsolationTest.gd
c6e_output_contract_test.py
```

Registered in `tests/run_all.py`.

Python contract tests pass in the current environment.
Godot GDScript execution is pending only because Godot is not installed in this environment.

## Next step

E2 — presentation componentization and layout contract, after E1 Godot certification.
