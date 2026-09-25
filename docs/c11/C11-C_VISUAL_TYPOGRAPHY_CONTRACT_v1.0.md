# C11-C Visual Typography Contract v1.0

## Scope

This contract defines the shared typography service for the active presentation stack used by current C11-C Visual Drills and Visual Loops, and for the legacy `PresentationTheme` font entry point. It does not modify legacy C6 geometry or gameplay contracts.

## Roles

- **Header — Inter Bold** (`assets/fonts/Inter-Bold.otf`)
- **Footer — Noto Sans Mono Regular** (`assets/fonts/NotoSansMono-Regular.ttf`)

Header typography is optimized for short editorial statements, CTA copy and countdown numerals. Footer typography is intentionally monospaced so telemetry, seed and delivery data retain a compact technical rhythm.

## Implementation

`core/presentation/C11CVisualTypography.gd` is the single shared font-resolution service used by active C11-C content. `PresentationTheme.gd` delegates its active legacy presentation font to the same service, so the project no longer has Comic Sans as an active production font. Callers must request a role rather than loading a font directly. The shared editorial layer applies Header role to Header text and Footer role to Footer telemetry. The Saccade jump counter uses the Footer role because it is numeric telemetry-like information.

New C11-C renderers/prototypes must not reference Comic Sans, the previous Courier asset, or a system fallback directly. The historical Comic Sans/Courier assets remain in the repository for compatibility and audit history, but they are no longer selected by the active presentation font path.

## Distribution

Font license notices are kept in `assets/fonts/LICENSE-C11C-FONTS.txt`. The selected font packages permit embedding/redistribution with software under their respective SIL Open Font License terms.

## Regression

`tests/C11CVisualDrillTypographyContractTest.gd` verifies asset existence, role calls, absence of legacy font references in the shared C11-C path, and consumption of the shared editorial layer by the five current Visual Loop prototypes.
