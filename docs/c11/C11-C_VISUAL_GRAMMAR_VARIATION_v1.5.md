# C11-C — VISUAL GRAMMAR & VARIATION MODEL v1.5

Status: ART-DIRECTION LOCK CANDIDATE
Scope: presentation-only; no core/simulation/RNG changes.

## 1. Problem diagnosed from the five physical prototypes

The current multi-seed stage proves deterministic variation plumbing, but several seeds still read as
"the same composition with altered parameters".

C11-C v1.5 therefore changes the variation model:

    family + seed
        -> visual grammar mode
        -> macro composition
        -> motion grammar
        -> palette variant
        -> scale/density variant
        -> editorial variant

The seed MUST choose between visibly different constructions, not only phase/speed/intensity.

## 2. Diversity rule

A seed must change at least:
- one macro-structural choice;
- one motion choice;
- one secondary treatment choice (palette OR scale/density OR glow).

The result must remain unmistakably inside its family.

No runtime randomness. No changes to core, simulation, SimulationResult, frozen RNG ownership,
winning-frame logic, challenge durations or C11-B geometry.

## 3. Family grammar menus

### C11-C.1 — GEOMETRIC WAVES

Family identity: harmonic / geometric wave mechanics.

Allowed visual grammar modes:
1. HARMONIC MEMBRANE — projected 3D standing-wave surface.
2. INTERFERENCE PLANE — crossing wave fields producing moiré-like nodal geometry.
3. PARAMETRIC RIBBON — folded ribbon / strip with sinusoidal depth illusion.
4. LATTICE WAVE — geometric mesh deforms as a coherent field.
5. ORBITAL WAVE — concentric/elliptic wave fronts with phase-shifted propagation.

Composition:
- center may remain central, but the dominant silhouette MUST NOT default to a circle.
- macro silhouette can be planar, ribbon-like, lattice-like, elliptic or orbital.
- depth is optical: perspective scale, brightness falloff, line convergence, parallax-like layer offsets.

Motion:
- travelling wave;
- counter-propagating wave;
- standing wave;
- fold/unfold;
- phase interference.
No "flag waving" as the default motion.

Palette families:
- cyan/magenta;
- electric blue/lilac;
- turquoise/orchid;
- white/spectral blue;
- controlled warm-cold harmonic variant.

Scale:
- seed can change line density, amplitude, grid resolution and hero scale within safe limits.

BANNED:
- repeated circular blob as universal template;
- default single-axis undulation;
- random noise used as a substitute for wave structure.

### C11-C.2 — FRACTAL BLOOM

Family identity: infinite branching universe / mycelium / neural filaments.

Allowed visual grammar modes:
1. RADIAL BLOOM — central branching nucleus.
2. DENDRITIC TUNNEL — apparent forward descent through branching structures.
3. SPIRAL FRACTAL — logarithmic/Julia-like spiral expansion.
4. FRACTAL FILIGREE — extremely fine branching lace.
5. NESTED WORLDS — multiple recursive scales appearing inside one another.

The "infinite" requirement is perceptual:
- new detail must emerge as the camera enters the mathematical domain;
- avoid simple texture scaling;
- vary the zoom trajectory per seed;
- vary branching density and detail frequency;
- allow some variants to pause/expand before the next recursive reveal.

Palette families:
- indigo/violet/cyan;
- blue-night/electric violet;
- teal/indigo;
- ultraviolet/magenta with cyan highlights;
- restrained monochrome-indigo.

Glow:
- secondary treatment, not protagonist.
- at least some seeds must be filament-first with restrained bloom.

BANNED:
- same zoom envelope for every seed;
- illumination-heavy presentation where fractal detail becomes secondary.

### C11-C.3 — SACRED SYMMETRY

Family identity: perfect celestial mechanism / precision astrolabe.

Allowed visual grammar modes:
1. ASTROLABE — rings, axes, orbital markers.
2. GEAR TRAIN — nested mechanical rotational ratios.
3. POLYGON ORRERY — regular polygons orbiting a central mechanism.
4. ORIGAMI MANDALA — mathematical folds opening/closing symmetrically.
5. CELESTIAL CHART — radial axes, sectors, nodes and orbital paths.

N remains in {4,6,8,12}.
Symmetry MUST remain exact.

Motion:
- gear ratios such as 2:1, 3:-2, 5:3;
- stepped opening;
- synchronized lock/alignment;
- radial scaling.

Palette:
- liquid gold;
- gold + copper;
- amber + laser white;
- bronze + pale gold;
- warm obsidian monochrome.

Scale:
- seed varies ring radii, core scale, node count/density and stroke hierarchy.

BANNED:
- always the same circular dial;
- psychedelic kaleidoscope spinning;
- asymmetrical decoration.

### C11-C.4 — LIVING PARTICLES

Family identity: synthetic life / matter responding to invisible forces.

Allowed visual grammar modes:
1. SWARM — collective migrating cloud.
2. VORTEX — particles spiral into/around an attractor.
3. COLLISION CLOUD — two soft populations meet, compress and separate.
4. ORGANIC PULSE — dense core contracts and breathes.
5. MAGNETIC FILAMENT CLOUD — density creates temporary soft strands without hard vector lines.

Morphology:
- no hard geometric glyphs;
- particles remain soft/translucent;
- visual structure comes from density and interaction.

Motion:
- attraction;
- repulsion;
- curl/turbulence;
- collision-like deflection;
- inertia and dissolution.

Color:
- emerald/sea-green;
- turquoise/aqua;
- jade/teal;
- cyan-green with spectral core;
- restrained green-blue monochrome.

Seed can vary:
- attractor topology;
- cloud density;
- particle size distribution;
- collision energy;
- color phase;
- glow threshold.

BANNED:
- visible straight-line trajectories;
- Pong-like edge bounces;
- identical two-cloud composition for every seed.

Production note:
The formal 10,000–50,000 micro-particle GPU target remains the production implementation target.
A lightweight shader benchmark is not considered a waiver of that contract.

### C11-C.5 — INVISIBLE FORCES

Family identity: visible evidence of an invisible physical field.

Allowed visual grammar modes:
1. DIPOLE FIELD — attraction/repulsion around two poles.
2. VORTEX FIELD — rotational flow around a singularity.
3. SADDLE FIELD — crossing attraction/repulsion axes.
4. QUADRUPOLE FIELD — four interacting poles.
5. GRAVITATIONAL LENS — field bends rails around a central mass.
6. TOPOGRAPHIC BASIN — nested equipotential valleys.

The field MUST NOT default to a circular ring.

Composition:
- rails can span the whole Body;
- the dominant force structure stays safely inside the Body;
- the storm/pulse can be central, offset, elongated or multi-polar.

Motion:
- field deformation;
- travelling measurement pulse;
- accelerating pulse in dense valleys;
- slow drift in sparse regions.

Palette:
- crimson/cadmium/orange/gold;
- crimson + orange;
- deep red + amber;
- hot orange + yellow;
- warm monochrome.

BANNED:
- disconnected floating lights;
- cold palette;
- static glowing circle used as the universal force field;
- pulse detached from rails.

## 4. Production variation hierarchy

Recommended influence hierarchy:

40% — macro grammar / silhouette
25% — motion grammar
15% — palette variant
10% — scale / density
10% — optical treatment / glow / texture

These are design weights, not numeric scoring. A seed may bias several categories together,
but must not select combinations that violate the family contract.

## 5. Color variation principle

Color is now explicitly part of production variation.

The seed selects a palette family first, then controlled intra-palette anchors.
No arbitrary RGB noise.

This keeps each family recognizable while avoiding:
"every video is exactly the same color".

## 6. Scale variation principle

Scale now has two meanings:
- macro hero scale / occupation of Body;
- micro scale such as line width, particle size, branch density or node size.

Scale changes MUST respect safe margins and the family-specific stroke/morphology contract.

## 7. Artistic gate before production

For each family, at least 8 seeds should be reviewed.

PASS requires:
- at least 3 clearly different macro constructions;
- at least 3 motion grammars visibly represented;
- multiple palette variants;
- no BANNED-list violations;
- family identity preserved.

Only then open the production bulk.
