# C11-C common presentation/audio layer — 2.13.0

Presentation/delivery-only helpers shared by the five Visual Loop production identities and the four Visual Drill families.

- `C11CEditorialAnimator.gd`: deterministic Matrix/airport-board header transition.
- `C11CEditorialColors.gd`: palette-derived editorial text/rule colors.
- `C11CColorBoost.gd`: deterministic mobile-vivid color transform.
- `C11CMovieCapture.ps1`: temporary 720×1280 Movie Maker override.
- `C11CSafeAmbient.py`: compatibility launcher for family-aware deterministic music. It resolves a semantic music profile and delegates to the current generator.
- `generate_c11c_family_music.py`: A-minor pentatonic pad generator with soft envelopes, slow deterministic modulation, bounded stereo movement and mobile-safe low-pass filtering.
- `generate_c11c_ambient_audio.py`: compatibility wrapper for older fixed-master invocation paths; it now delegates to the same family-aware generator.
- `write_social_metadata.py`: writes publication-ready social copy from a render manifest.

Music inputs are limited to seed, visual family/grammar and approved presentation metadata. Gameplay truth is never consumed.
These helpers do not modify C11-B engine semantics, C7 ownership/contracts or C9 authoring semantics.


Duration is resolved by `C11CVisualLoopDuration.gd` for Visual Loop renderers. Audio generation receives the resolved duration so visual and audio periods remain aligned. Long-form production composes canonical rendered segments rather than duplicating family renderers.

## Current D7/D8 state

C11-C 2.19.12 is frozen. C11-D D7 is PASS/CLOSED and FROZEN; D8.0 is the next phase. The active C11-D baseline is `ChallengeEngineV01_STATELESS_C11-D_7.5_V8_FROZEN_20261008_111052.zip` (SHA-256 `396d9f4bfdbb44b4878acf06db8d6c1c385103c110de537a174632e93611cd1d`).

## Directory contents

### Subdirectories
- None.

### Representative files
- `C11CColorBoost.gd`
- `C11CDrillPaletteBank.gd`
- `C11CEditorialAnimator.gd`
- `C11CEditorialColors.gd`
- `C11CHeaderAnimatorV2.gd`
- `C11CMovieCapture.ps1`
- `C11CPaletteBank.gd`
- `C11CSafeAmbient.py`
- `C11CTheme.gd`
- `C11CTronDepthBackground.gd`
- `C11CVariationProfile.gd`
- `C11CVisualLoopDuration.gd`
- `C11C_VARIATION_PROFILE_SPEC_v1.0.json`
- `C11C_VISUAL_GRAMMAR_SPEC_v1.5.json`
- … 10 additional files.
