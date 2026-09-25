# Repository Structure

C11-C 2.9.0 adds the following live presentation/production surfaces:

```text
core/presentation/
├── C11CVisualEditorialLayer.gd
├── C11CVisualTypography.gd
├── VisualDrillPresentationBinder.gd
├── VisualDrillPresentationPhaseLogic.gd
└── PresentationUI.gd

core/presentation/rendering/
├── C11CDrillEnvironment.gd
├── TrackingRenderer.gd
├── SaccadeRenderer.gd
├── PursuitRenderer.gd
└── PeripheralScanRenderer.gd

tools/prototypes/c11c_common/
├── C11CDrillPaletteBank.gd
├── C11CSafeAmbient.py
├── generate_c11c_family_music.py
├── generate_c11c_ambient_audio.py
└── write_social_metadata.py

profiles/presentation/
├── c11c_visual_family_catalog.json
├── c11c_visual_hooks.json
└── c11c_visual_music_profiles.json

tools/prototypes/c11c_bulk/
├── C11CVisualDrillReviewEnvelopeGenerator.gd
└── run_c11c_visual_drill_review.ps1

tests/
├── C11CVisualDrillTypographyContractTest.gd
├── C11CVisualDrillSocialDeliveryContractTest.gd
├── C11CDrillPaletteBankContractTest.gd
└── existing C11-C mechanic/presentation/playback suites
```

Generated Visual Drill review artifacts live below `artifacts/prototypes/c11c_visual_drills_review/` and include MP4, GIF, keyframes, contact sheet, manifest, envelope, `authoring.json` and `_social.txt`.

Historical `docs/` and previous checkpoint documents are retained. They are not silently rewritten to represent a newer contract. The current operational truth is the versioned C11-C current-state document and handover.
