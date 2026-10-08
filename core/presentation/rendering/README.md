# rendering

Presentation-only framing, components and rendering logic. It must not alter simulation truth.

## Directory contents

### Subdirectories
- `shaders/`

### Representative files
- `C11CDrillEnvironment.gd` — Godot/GDScript runtime or test code.
- `ContentRendererHost.gd` — Godot/GDScript runtime or test code.
- `FractalRenderer.gd` — Godot/GDScript runtime or test code.
- `GeometricRenderer.gd` — Godot/GDScript runtime or test code.
- `KaleidoscopeRenderer.gd` — Godot/GDScript runtime or test code.
- `ParticleFlowRenderer.gd` — Godot/GDScript runtime or test code.
- `PeripheralScanRenderer.gd` — Godot/GDScript runtime or test code.
- `PursuitRenderer.gd` — Godot/GDScript runtime or test code.
- `PursuitTargetLayer.gd` — Godot/GDScript runtime or test code.
- `SaccadeRenderer.gd` — Godot/GDScript runtime or test code.
- `TrackingRenderer.gd` — Godot/GDScript runtime or test code.
- `TrackingTargetLayer.gd` — Godot/GDScript runtime or test code.
- `VectorFieldRenderer.gd` — Godot/GDScript runtime or test code.
- `VisualContentPlayer.gd` — Godot/GDScript runtime or test code.
- … 3 additional files.

## Lifecycle / authority

Protected implementation boundary. Changes require an explicit checkpoint and focused regression.

This README is a navigation aid. The files referenced above remain authoritative according to their own contracts, schemas, tests and handover documents.
