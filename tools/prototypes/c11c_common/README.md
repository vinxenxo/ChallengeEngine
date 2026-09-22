# C11-C common presentation layer — v2.1.4

Presentation-only helpers used by the five Visual Loop families.

- `C11CEditorialAnimator.gd`: deterministic Matrix/airport-board header transition.
- `C11CEditorialColors.gd`: palette-derived editorial text/rule colors.
- `C11CColorBoost.gd`: deterministic mobile-vivid color transform; explicitly typed to avoid Godot warning-as-error inference.
- `C11CMovieCapture.ps1`: temporary 720×1280 Movie Maker override; restores prior `override.cfg` state.
- `C11CSafeAmbient.py`: compatibility wrapper for the single shared deterministic, restrained mobile-safe ambient bed used across all C11-C visual content.
- `generate_c11c_ambient_audio.py`: canonical fixed 18-second master bed; shorter renders receive an exact prefix and longer renders loop the same master.
- `write_social_metadata.py`: writes per-video social sidecars; accepts UTF-8 BOM and non-BOM JSON.

These helpers do not modify C11-B engine semantics or C7 contracts.
