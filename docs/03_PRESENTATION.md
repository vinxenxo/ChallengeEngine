# Presentation

## Unified social frame

```text
540 × 960 logical
HEADER  0..144
BODY    144..816
FOOTER  816..960
```

Physical social delivery remains 720×1280 at 30 FPS with one uniform 4/3 scale at the presentation boundary.

## Visual Drill phase envelope

All four drill families use:

```text
PRE_ROLL  = 3 s
GAME      = canonical drill gameplay
END_CTA   = 3 s
```

Current totals:

- Tracking: 21 + 3 + 3 = 27 s / 810 physical frames.
- Saccade: 17 + 3 + 3 = 23 s / 690 physical frames.
- Pursuit: 17 + 3 + 3 = 23 s / 690 physical frames.
- Peripheral Scan: 17 + 3 + 3 = 23 s / 690 physical frames.

## Terminal CTA

Visual Drills reuse the historical `CTAComponent` implementation used by Challenge.

Placement:

```text
Visual Drill END_CTA
    └── HEADER
```

Message:

```text
¿LO CONSEGUISTE?
¿HASTA DÓNDE LLEGASTE?
```

During END_CTA the `FooterRegion` remains visible. The CTA is Header-owned; the Footer continues to show its normal telemetry text. The former Footer CTA surface is not rendered.

## Typography

C11-C Visual content uses the shared role service `C11CVisualTypography`:

- Header → `assets/fonts/Inter-Bold.otf` (Inter Bold).
- Footer → `assets/fonts/NotoSansMono-Regular.ttf` (Noto Sans Mono Regular).

The bundled fonts are distributed under SIL Open Font License 1.1 and are documented in `assets/fonts/LICENSE-C11C-FONTS.txt`. The legacy `PresentationTheme` remains available for C6/Challenge compatibility; it is not part of the active C11-C typography path.

## Background language

`C11CDrillEnvironment` is a shared low-salience background layer:

- Tracking: atmospheric contour arcs + sparse particles; no Tron road and no future trajectory.
- Saccade: sparse constellation haze; no edge connects or predicts target jumps.
- Pursuit: star field + soft nebular masses under radial DOF.
- Peripheral Scan: sparse space dust + outer atmospheric ring beneath orbital radar.

The environment is presentation-only and stays subordinate to the drill stimulus.

## Visual Drill family renderers

### Tracking

Hero target + growing history trail. Seed variation is authored, not generated in presentation.

### Saccade

Discrete target relocation, scale/opacity/flash transitions and a counter driven by emitted `jump_index`.

### Pursuit

Complex internal Euler-like target structure, authored arc-length movement, sizygia response and radial depth-of-field treatment.

### Peripheral Scan

Fixed central fixation anchor, orbital rings and luminosity-only peripheral flares, with authored threat/distractor event timing.

## Visual Loop presentation

The five active C11-C Loop identities use the same shared editorial typography layer as Visual Drills. Their visual renderer remains family-specific; presentation changes never alter loop simulation/data contracts.
