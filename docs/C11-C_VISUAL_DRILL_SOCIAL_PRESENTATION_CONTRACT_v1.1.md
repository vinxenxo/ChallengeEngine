

## Physical composition scaling

The logical `UnifiedSocialFrame` remains exactly `540×960`. Visual Drill presentation coordinates, typography sizes, header/footer positions and Body coordinates remain authored in that logical space.

For the C11-C social delivery target, the complete Visual Drill presentation root is scaled uniformly by `4/3`, mapping `540×960` to `720×1280` without rewriting individual coordinates. This is the same composition-scaling strategy used by the accepted Visual Loop physical prototypes.

No individual family renderer may compensate for this scale. Mechanical coordinates remain logical; physical scaling belongs to the shared presentation/capture boundary.

## Social metadata

The review artifact may include a social sidecar containing title, description, family, seed, dimensions, duration, FPS, audio state and hashtags. This metadata is editorial/delivery information and does not define drill mechanics.
