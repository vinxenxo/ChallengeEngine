# C11-C CHANGELOG — v2.10.1

## Scope

Runtime repair of the 2.10.0 presentation/audio foundation after workstation validation. No frozen engine truth or C7/C9 ownership was changed.

## Root causes discovered on workstation

1. `C11CVisualEditorialLayer.gd` referenced `HEADER_BOLD_EMBOLDEN` without declaring it. Godot therefore rejected the shared editorial layer at parse time. Because `VisualContentPlayer` preloads that layer, its dependent runtime scripts also failed to initialize. The physical result was a grey/empty gameplay body with countdown and terminal CTA still visible.
2. `SaccadeRenderer.gd` still called the generic typography helper even though the C11-C contract requires the Saccade counter to use the footer role.

## Repairs

- Restored `const HEADER_BOLD_EMBOLDEN := 0.70` in the editorial layer, matching the previous 2.9.1 measurement behavior.
- Changed the Saccade jump counter to `apply_footer_to_label()`.
- Extended `C11CVisualDrillTypographyContractTest.gd` to preload and instantiate `C11CVisualEditorialLayer`.

## Retained 2.10.0 foundations

- Header-owned `CTAComponent` with Footer telemetry visible during END_CTA.
- Inter Bold / Noto Sans Mono Regular role-based C11-C typography.
- 24 semantic palette worlds per Drill family.
- `FAMILY_MUSIC_V3` deterministic semantic music profiles and Drill/Loop pairings.

## Validation status

This checkpoint is intentionally **open** until workstation focused tests, aggregate corpus and physical render review are green.
