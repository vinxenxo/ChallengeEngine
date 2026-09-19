# Presentation

## Unified social frame

All content uses a common 540x960 structure:

```text
HEADER  0..144
----------------
BODY    144..816
----------------
FOOTER  816..960
```

`UnifiedSocialFrame` provides the regions and safe structure. It is passive.

## Coordinate mapping

The simulation may operate on a 1080x1920 logical canvas. `CoordinateMapper` projects that geometry into the social Body rectangle while preserving aspect ratio. This is a presentation transform, not a gameplay transform.

## Framing

C11-B.0.2 establishes the framing contract. The current modes distinguish structural presentation from the mechanics themselves. Any later visual polish must preserve entity positions derived from the same simulation snapshots.

## Winning-frame visibility

Visibility is evaluated on actual screen geometry after mapping into the Body. The visibility gate must not remap logical coordinates.

## Art direction after freeze

C11-C may refine typography, hierarchy, assets, visual language, emphasis, background treatment and other presentation concerns. Reference images may be used to drive those changes. The simulation mathematics remains frozen.
