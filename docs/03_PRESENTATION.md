# Presentation

## Unified social frame

All social renders use a common 540×960 structural frame:

```text
HEADER  0..144
BODY    144..816
FOOTER  816..960
```

`UnifiedSocialFrame` is structural and passive. Content roles are bound by the appropriate presentation binder/UI layer.

## Coordinate mapping

Simulation continues to use the established logical coordinate system. `CoordinateMapper` projects logical geometry into the social Body region while preserving aspect ratio. This is a presentation transform only.

## Framing

`PresentationFramer` owns presentation framing decisions. It cannot redefine simulation geometry, calculate the winning frame or alter RNG consumption.

## Winning-frame visibility

The visibility gate evaluates mapped screen-space geometry. A presentation validation failure must be repaired in presentation mapping/binding, not by changing the underlying winning-frame mathematics.

## C11-C art direction

The frozen structural frame is the starting boundary for visual design. Art direction can evolve:

- palette and typography
- asset treatment
- backgrounds and foregrounds
- visual hierarchy
- badges and text styling
- motion language and emphasis

The first implementation should be validated on one representative route before propagation to the wider corpus.
