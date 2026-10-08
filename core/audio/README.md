# audio

Audio contracts, generators and renderers. C7 ownership remains protected; C11-D music work is additive and isolated.

## Directory contents

### Subdirectories
- `generators/`
- `renderers/`

### Representative files
- `AudioAssetRegistry.gd` — Godot/GDScript runtime or test code.
- `AudioBuffer.gd` — Godot/GDScript runtime or test code.
- `AudioEvent.gd` — Godot/GDScript runtime or test code.
- `AudioEventStream.gd` — Godot/GDScript runtime or test code.
- `AudioExportBridge.gd` — Godot/GDScript runtime or test code.
- `AudioGenerationResult.gd` — Godot/GDScript runtime or test code.
- `AudioGeneratorRegistry.gd` — Godot/GDScript runtime or test code.
- `AudioProfile.gd` — Godot/GDScript runtime or test code.
- `AudioProfileAdapter.gd` — Godot/GDScript runtime or test code.
- `AudioRNGContext.gd` — Godot/GDScript runtime or test code.
- `AudioTimelineResolver.gd` — Godot/GDScript runtime or test code.

## Lifecycle / authority

Protected implementation boundary. Changes require an explicit checkpoint and focused regression.

This README is a navigation aid. The files referenced above remain authoritative according to their own contracts, schemas, tests and handover documents.
