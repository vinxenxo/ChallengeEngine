# Testing and Regression

## Current corpus

The current C11-C 2.10.1 repair tree contains **122 registered logical suites** in `tests/run_all.py`. The 2.10.1 checkpoint retains the family-aware music binding suite to the 2.9.1 corpus and preserves the existing historical compatibility suites.

The user has confirmed that the previous 2.9.1 corpus and physical review are green. The 2.10.1 repair requires a fresh runtime pass before closure is claimed; focused tests must also prove the shared editorial layer can load.

## Required first command

```powershell
python .\tests\run_all.py
```

## Targeted C11-C validation

```powershell
godot --headless --path . --script .\tests\C11CVisualDrillEndCTAContractTest.gd
godot --headless --path . --script .\tests\C11CVisualDrillTypographyContractTest.gd
godot --headless --path . --script .\tests\C11CVisualDrillSocialDeliveryContractTest.gd
godot --headless --path . --script .\tests\C11CDrillPaletteBankContractTest.gd
godot --headless --path . --script .\tests\C11CVisualMusicProfileContractTest.gd
```

Family contracts:

```powershell
godot --headless --path . --script .\tests\C11CTrackingMechanicContractTest.gd
godot --headless --path . --script .\tests\C11CTrackingPresentationContractTest.gd
godot --headless --path . --script .\tests\C11CSaccadeMechanicContractTest.gd
godot --headless --path . --script .\tests\C11CSaccadePresentationContractTest.gd
godot --headless --path . --script .\tests\C11CPursuitMechanicContractTest.gd
godot --headless --path . --script .\tests\C11CPursuitPresentationContractTest.gd
godot --headless --path . --script .\tests\C11CPeripheralScanMechanicContractTest.gd
godot --headless --path . --script .\tests\C11CPeripheralScanPresentationContractTest.gd
```

Playback:

```powershell
godot --headless --path . --script .\tests\C6F08TrackingPlaybackValidationTest.gd
godot --headless --path . --script .\tests\C6F08SaccadePlaybackValidationTest.gd
godot --headless --path . --script .\tests\C6F08PursuitPlaybackValidationTest.gd
godot --headless --path . --script .\tests\C6F08PeripheralScanPilotTest.gd
```

## Physical review

For a one-seed focused render across multiple families:

```powershell
.\tools\prototypes\c11c_bulk\run_c11c_visual_drill_review.ps1 `
    -Seeds 314159 `
    -Families pursuit,peripheral_scan `
    -Smoke `
    -ResetReviewAssets
```

For the full review matrix, provide five unique seeds without `-Smoke`.

## Social sidecar QA

Every successful physical review render must produce:

```text
VisualDrill_<family>_seed_<seed>_social.txt
```

The runner fails closed if the file is missing or unexpectedly small.

## Regression discipline

A physical video succeeding does not excuse a logical test failure. A logical suite returning `PASS` after a script load error is also a failure. New suites must register explicit PASS markers in `tests/run_all.py`.
