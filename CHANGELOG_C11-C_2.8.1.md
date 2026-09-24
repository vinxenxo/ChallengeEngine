# C11-C 2.8.1 — Pursuit / Peripheral Runtime Hotfix

## Fixed
- Explicitly typed `PeripheralScanGenerator` active event dictionaries to satisfy Godot 4.7 warning-as-error rules.
- Explicitly typed `PeripheralScanRenderer` anchor state dictionaries.
- Fixed `C11CVisualDrillEndCTAContractTest.gd` to use the instantiated `UnifiedSocialFrame` and guard nullable CTA access.
- Hardened `C11CPeripheralScanMechanicContractTest.gd` so generator load/instantiation failures cannot report PASS.
- Updated the Visual Drill review runner banner/revision to 2.8.1 for traceability.

## Scope
- No changes to Challenge simulation, RNG architecture, RenderedFrameStream, or frozen C11-B contracts.
