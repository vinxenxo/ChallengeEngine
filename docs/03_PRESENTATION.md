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

During END_CTA the entire `FooterRegion` is hidden. This removes the background box from the former Footer presentation state while preserving C11-B structural geometry.

## Typography

C11-C Visual content uses `C11CVisualTypography` → `assets/fonts/courier-regular.ttf`.

The legacy `PresentationTheme` remains available for C6/Challenge compatibility; the C11-C utility prevents a global theme mutation solely to satisfy the new drill typography.

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
