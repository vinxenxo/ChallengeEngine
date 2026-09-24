# C11-C 2.7.1 — Visual Drill End CTA Hotfix

## Status
Hotfix over C11-C 2.7.0. Presentation-only. No simulation or RenderedFrameStream truth changes.

## Fixes
- Fixed `CTAComponent.gd` use of the invalid direct `VBoxContainer.separation` property by using the supported theme constant override.
- Fixed the `VisualDrillPresentationBinder.gd` duration expression referencing the nonexistent `CountdownPresentationPhaseLogic` identifier.
- Hardened `C11CVisualDrillEndCTAContractTest.gd` so failed dependent class instantiation cannot produce a false PASS.
- Preserved the 3-second terminal self-evaluation CTA and reuse of the existing `CTAComponent`.

## Expected presentation envelopes
- Tracking: 3s countdown + 21s gameplay + 3s CTA = 27s / 810 frames.
- Other current drills: 3s countdown + 17s gameplay + 3s CTA = 23s / 690 frames.
