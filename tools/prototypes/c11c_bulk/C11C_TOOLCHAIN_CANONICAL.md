# C11-C canonical toolchain map — v2.1.2

## Use these only

| Purpose | Canonical tool |
|---|---|
| PowerShell syntax validation | `validate_c11c_powershell.ps1` |
| Delivery topology validation | `validate_c11c_delivery_configuration.ps1` |
| Single-family all-loop run | `run_all_c11c_visual_loops.ps1` |
| 25-video Art Direction 2.0 review | `run_c11c_art_direction_review.ps1` |
| Multi-seed worker | `run_c11c_multiseed_bulk.ps1` |
| Review GIF/keyframes | `export_all_review_assets.ps1` |
| Manual prototype media cleanup | `clean_c11c_artifacts.ps1` |
| Explicit C11-C reset | `reset_c11c_artifacts.ps1` |
| Single final product publish | `run_c11c_production.ps1` |
| Final product bulk publish | `run_c11c_production_bulk.ps1` |

## Separation rule

Generation never cleans.
Review never cleans prototype staging.
Cleanup/reset never touches final production.
Production never writes into review assets.

## Delivery rule

Effective Movie Maker capture must be 720×1280 / 30 FPS / 540 frames for the current 18-second review baseline. The frozen project settings are not edited.
