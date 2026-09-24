# C11-C Studio v0.4.0

UX production/configuration split.

## UI
- Primary screen is Generar.
- Production navigation contains Generar, Resultados, Jobs, Logs, Reproducir.
- Configuration navigation contains Art Direction, Families, Seeds, Artifacts, Validation, Settings, Games/Drills, Diagnostics.
- Review and production options are consolidated into the Generar control surface.
- Review 5x5 is fixed to the canonical five families and five unique seeds; unsupported family/count controls were removed.

## Command adapter
- Canonical PowerShell working directory is the project root, matching documented invocation.
- Review calls run_c11c_art_direction_review.ps1 with -Seeds and optional -ResetReviewAssets only.
- Production 5x5 uses the documented run_c11c_production_bulk.ps1 loop as a GUI queue; the non-canonical run_c11c_production_25.ps1 is not used.
- Added prototype, review export and legacy-retirement command builders.
- Manual seeds are persisted through SeedManager for traceability.

## Canonical command audit
The GUI adapter now covers the v2.1.4 operational commands: PowerShell validation, delivery validation, preflight, Art Direction Review, one-family prototype, all-families prototype, single production, family production bulk, review GIF export, review keyframe export, all review asset export, cleanup dry-run/apply, reset dry-run/apply, and legacy-tool retirement dry-run/apply. `run_c11c_production_25.ps1` is intentionally not used as the primary production-5x5 launcher; the documented five-family bulk loop is used instead.

## Frozen boundary
No changes to C11-B simulation, RNG, SimulationResult, WinningFrameDetector, rendering mathematics, audio contracts, or canonical backend scripts.
