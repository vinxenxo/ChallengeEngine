# C11-C — Editorial Text Generation Contract v1.0

## Scope

This contract defines the optional deterministic geek/technobabble editorial layer used by C11-C Visual Loop prototypes.

It is presentation/editorial content only. It does not alter `core/`, simulation, `SimulationResult`, RNG ownership, `RenderedFrameStream`, or C7.

## Determinism

The generator is a deterministic mapping:

`family_id + seed + generator revision -> exact text`

The prototype implementation uses a local integer mixing function and does not consume a production RNG stream.

## Family vocabulary

Each Visual Loop family owns its own subject vocabulary:

- Geometric Waves -> waves, Lissajous, harmonics, Voronoi, polygonal resonance.
- Fractal Bloom -> Julia, orbital traps, recursive nucleus, mycelium, analytic zoom.
- Sacred Symmetry -> astrolabe, radial symmetry, gears, orbital rings, celestial mechanism.
- Living Particles -> attractors, fluid dynamics, magnetic density, vortices, Curl Noise.
- Invisible Forces -> gravitational topography, solar wind, equipotential lines, vector fields.

## Text construction

Templates combine an action, a family-specific subject, a status, an optional synthetic numerical value and a family-compatible unit.

The dictionary mirror is stored in `tools/prototypes/c11c_common/TECHNOBABBLE_DICTIONARY_v1.0.json`. The prototype generator keeps the same vocabulary as constants so its review output is independent of runtime file parsing.

## Prototype placement

The technobabble line is rendered in the Footer during art review. It is intentionally compact and family-specific, with automatic font fitting between 8 px and 10 px against the 468 px safe width.

## Production policy

Visual Loop production exports SHALL default to `footer_enabled = false`.
The footer remains a QA/art-direction surface and is not required in social-platform delivery output.

The prototype launchers expose `-NoFooter` to preview this production mode without changing the prototype default.

## Versioning

Changing vocabulary, templates, ordering, mixing salts, family mappings, or fixture expectations constitutes a generator revision and changes the deterministic text mapping for affected seeds.
