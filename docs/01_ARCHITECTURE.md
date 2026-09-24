# Architecture

## Layer model

### Capa 0 — Definitions / authoring

Canonical JSON, visual definitions, difficulty profiles and C11-C seed-authoring transforms. This layer may produce deterministic authored variation from the content seed without consuming runtime gameplay RNG.

### Capa 1 — Deterministic runtime / mechanics

Visual Drill generators consume authored parameters and emit deterministic frame state. The runtime never asks presentation to derive mechanics.

### Capa 2 — Passive presentation

`VisualDrillPresentationBinder`, `C11CVisualEditorialLayer`, `PresentationUI` and the family renderers consume render-ready state. Presentation may select color/font/background treatment from authored cosmetic variants, but it cannot calculate trajectory, event timing or answer truth.

### Capa 3 — Production orchestration

Review envelope generation, Movie Maker capture, FFmpeg/FFprobe, social sidecars, manifests and production QA.

## Visual Drill runtime flow

```text
Canonical drill definition
        ↓
Seeded authoring transform
        ↓
Review envelope / runtime payload
        ↓
VisualDrillRuntime
        ↓
VisualDrillFrameState
        ↓
VisualDrillPresentationBinder
        ↓
UnifiedSocialFrame / PresentationUI
        ↓
Passive family renderer + C11-C editorial layer
        ↓
Movie Maker / FFmpeg / FFprobe
```

## Presentation phases

The shared `VisualDrillPresentationPhaseLogic` adds presentation-only phases:

```text
PRE_ROLL → GAME → END_CTA → DONE
```

The terminal CTA is appended to the video duration and does not modify the gameplay frame stream.

## Shared presentation components

- `CTAComponent` is reused from the historical Challenge presentation.
- C11-C Visual Drill routes place that same component in Header.
- The FooterRegion is hidden for terminal CTA so the former footer background cannot remain as a gray block.
- `C11CVisualTypography` centralizes the active C11-C font and prevents duplication across editorial labels, CTA and Saccade counter.
- `C11CDrillEnvironment` centralizes low-salience procedural backgrounds across drill families.

## Determinism boundary

Seed-driven variation in Tracking, Saccade, Pursuit and Peripheral Scan is an **authoring transform**. It belongs in `VisualDrillSeedVariation`, not in family renderers.

The renderer consumes authored/runtime state. It never generates hidden answer events, trajectory samples or target positions.

## Pursuit-specific runtime boundary

Pursuit is authored as a normalized uniform cubic B-spline with arc-length lookup and frame samples. The renderer does not read `position_samples_normalized` directly; it consumes the runtime target state derived from those authored samples.

## Peripheral-specific runtime boundary

Peripheral Scan authoring owns event kind, ring, angle and frame start. Presentation only renders `active_events` and the authored central-anchor state.
