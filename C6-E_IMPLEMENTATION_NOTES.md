# C6-E — Step 0 / E1 Implementation Notes

## Output contract

- Simulation coordinate space remains 1080×1920.
- Godot source movie remains 540×960.
- Final MP4 master is explicitly transcoded to 1080×1920.
- FFprobe validates master resolution, codec, pixel format, FPS, duration and frames.

Historical C6-D4 MP4s stored in Git were 540×960; they are historical evidence, not the new C6-E master contract.

## Asset integrity

- Mandatory `background_path`, `target_path`, `object_path` are validated before simulation/render.
- Paths must be `res://` resources and must exist according to Godot `ResourceLoader.exists()`.
- `CHALLENGE_009` was missing `res://assets/c6/count_background.svg`; a dedicated deterministic SVG asset is now supplied.

## E1 Presentation Profile

`core/presentation/PresentationProfile.gd` is presentation-only. It holds reusable configuration for source canvas, master output, safe area, typography, composition, theme and asset family. It has no timeline, RNG, seed or simulation fields and cannot change `SimulationResult`.

Profiles are selected declaratively with `presentation.profile`; optional `profile_overrides` allow controlled variations.
