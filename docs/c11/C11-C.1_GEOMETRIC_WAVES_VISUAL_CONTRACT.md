# C11-C.1 — GEOMETRIC WAVES v1
## Visual Contract — Closed for Isolated Prototype

**Project:** ChallengeEngineV01_STATELESS  
**Family:** `VisualLoop / geometric`  
**Checkpoint:** `C11-C.1`  
**Contract version:** `1.0`  
**Status:** `APPROVED / CLOSED FOR PROTOTYPE`  
**Prototype status:** `C11-C.1-P / NOT IMPLEMENTED YET`  
**Scope:** presentation/art direction only

---

## 0. Contract Intent

`Geometric Waves v1` establishes the first visual gold standard for the `Visual Loop` family.

The target is not a generic animated background and not a screensaver. It is a deterministic generative composition in which geometry, colour, light and motion arise from mathematical relationships that remain visually elegant at every frame.

The contract is closed enough to be implemented without inventing visual decisions during coding.

The contract does **not** freeze a particular Godot implementation technique. A shader, `CanvasItem`, procedural mesh, line renderer, CPU-generated geometry or a combination of these may be used internally, provided the externally visible contract is satisfied.

---

# 1. Hard Architectural Boundary

## 1.1 Allowed scope

The prototype may modify or introduce only isolated presentation/art-direction code and prototype assets/configuration required to render `VisualLoop / geometric`.

The prototype may introduce:

- a dedicated geometric visual generator;
- a dedicated geometric visual renderer;
- shader code if useful;
- mathematical helper functions;
- prototype-only definitions/configuration;
- visual QA helpers that do not alter frozen runtime contracts.

## 1.2 Explicitly frozen and out of scope

The prototype MUST NOT modify:

- `SimulationResult`;
- simulation mechanics;
- `WinningFrameDetector`;
- `WinningFrameVisibilityGate`;
- simulation RNG streams;
- mechanic RNG streams;
- `RenderedFrameStream` contract;
- C7 audio contracts;
- C9 authoring contracts;
- C11-B `UnifiedSocialFrame` geometry;
- `HeaderRegion`, `BodyRegion` or `FooterRegion` dimensions;
- challenge mechanics or challenge assets.

The prototype must consume the frozen presentation boundary; it must not redefine it.

## 1.3 Renderer architecture rule

`GeometricWaves` is a **generative visual family**, not a shader.

A shader may be one implementation component, but the product unit is the deterministic family specification:

`seed + temporal position + visual parameters -> mathematical visual state -> rendered frame`.

No contract requirement may be introduced solely because a particular rendering technology makes it convenient.

---

# 2. Social Frame and Coordinate Contract

The prototype renders inside the existing C11-B social frame.

## 2.1 Physical canvas

- Width: `540 px`
- Height: `960 px`
- Target export rate: `30 FPS`

## 2.2 Frozen regions

- `HeaderRegion`: `x=0..540`, `y=0..144`
- `BodyRegion`: `x=0..540`, `y=144..816`
- `FooterRegion`: `x=0..540`, `y=816..960`

Body dimensions:

`540 × 672 px`

## 2.3 Optical centre

Social canvas centre:

`C = (270, 480)`

Body-relative centre:

`C_body = (270, 336)`

The primary geometric mass is centred on `C`.

A visual composition may breathe around the centre, but the hero structure must not develop a sustained translational drift away from it.

## 2.4 Primary safety envelope

Maximum hero radius:

`R_safe = 216 px`

Equivalent horizontal limits:

`x = 54 .. 486`

Equivalent vertical limits:

`y = 264 .. 696`

Therefore the hero geometry has:

- `54 px` horizontal safety margin inside the Body;
- `120 px` vertical clearance from the Body top/bottom boundaries.

This safety envelope applies to intentional geometry. Glow, anti-aliasing and optical halos are also expected to remain visually contained inside the Body; clipping into Header/Footer is not an acceptable way to pass containment.

---

# 3. Temporal Contract

## 3.1 Canonical duration

`LOOP_DURATION = 10.0 s`

No alternative duration is permitted for the C11-C.1 benchmark.

## 3.2 Sampling

`FPS = 30`

`FRAME_COUNT = 300`

Exported frame indices:

`f = 0 .. 299`

Continuous normalized loop position:

`u = f / 300`

The mathematical closure state at `u = 1` is the implicit successor of frame `299`; it is not exported as an additional frame.

## 3.3 Seamless loop definition

Every animated quantity that affects the visible result MUST satisfy:

`P(0) = P(1)`

and the first derivative with respect to normalized time SHOULD satisfy:

`P'(0) = P'(1)`

For the canonical prototype, this is a hard requirement for every primary phase, rotation, scale, morph, colour phase and opacity envelope.

The preferred construction is a periodic Fourier/harmonic basis with integer temporal frequencies:

`P(u) = P0 + Σ[A_k sin(2πku + φ_k) + B_k cos(2πku + φ_k)]`

with `k ∈ {1,2,3,...}`.

This guarantees periodic closure by construction.

## 3.4 No piecewise seam hack

The prototype MUST NOT implement:

- a special final-frame correction;
- a manual jump at `u >= 0.99`;
- a duplicate first frame appended to the export;
- a hidden reset of state at the seam.

The loop must close because the mathematics is periodic, not because the exporter hides the discontinuity.

---

# 4. Visual Identity

## 4.1 Core statement

> **A complex mathematical system becoming visible as a living geometric object.**

The viewer should perceive:

- mathematical precision;
- transformation rather than rotation-only motion;
- controlled complexity;
- high optical cleanliness;
- premium generative design;
- depth produced from structure and light rather than from photographic assets.

## 4.2 Anti-screensaver rule

The visual fails the art benchmark when the dominant impression is:

- “rotating polygon”;
- “generic neon background”;
- “random particles”;
- “stock VJ effect”;
- “psychedelic rainbow animation”.

The motion must express an evolving system: deformation, interference, convergence, divergence and phase relationships.

---

# 5. Mathematical Grammar

## 5.1 Canonical primitive families

`Geometric Waves v1` may use the following mathematical families:

1. regular `N`-gons;
2. sinusoidal radial deformation;
3. parametric Lissajous curves;
4. two- or three-layer wave interference;
5. phase offsets;
6. harmonic scale modulation;
7. intersection/node extraction from curve proximity or crossing.

## 5.2 Allowed polygon orders

`N ∈ {4, 5, 6, 7, 8, 10, 12}`

Triangle and 3-gon forms are intentionally excluded from the first gold-standard prototype to keep the visual language mature and architectural.

## 5.3 Hero radial formulation

The canonical hero may be represented as a regular-polygon radius function with harmonic deformation:

`P(θ,u) = C + R(θ,N) · [1 + A1·sin(k1θ + ψ1(u)) + A2·sin(k2θ + ψ2(u))] · S(u) · [cos θ, sin θ]`

where:

- `C` is the fixed optical centre;
- `R(θ,N)` is the regular-polygon radial distance;
- `A1` and `A2` are bounded deformation amplitudes;
- `k1`, `k2` are integer spatial harmonics;
- `ψ1(u)` and `ψ2(u)` are periodic phases;
- `S(u)` is a periodic scale envelope.

No implementation is required to use this exact algebraic decomposition if the resulting geometry is equivalent in visual behaviour.

## 5.4 Lissajous secondary formulation

A secondary curve may use:

`x(θ) = A·sin(aθ + δx)`

`y(θ) = B·sin(bθ + δy)`

with rational frequency ratios from:

`a:b ∈ {3:2, 2:1, 5:2, 3:1, 4:1, 5:1}`

### Important closure rule

The golden ratio `φ ≈ 1.618` MUST NOT be used as a direct temporal or curve-closure frequency ratio in the canonical loop because it is irrational and would prevent exact periodic closure over a finite common cycle.

`φ` MAY be used as a static proportion, scale relationship or non-temporal layout ratio.

---

# 6. Morphology and Complexity

## 6.1 Canonical transformation arc

The 10-second loop expresses a continuous complexity arc:

`simple geometry -> wave deformation -> interference -> complex geometric state -> decompression -> simple geometry`

The four visual phases are descriptive, not discrete runtime states.

## 6.2 Canonical morph envelope

A valid default envelope is:

`M(u) = 0.5 - 0.5·cos(2πu)`

Properties:

- `M(0) = 0`
- `M(0.5) = 1`
- `M(1) = 0`
- `M'(0) = M'(1) = 0`

This gives an exact open–climax–return cycle without an endpoint snap.

## 6.3 Layer structure

Exactly three perceptual depth layers are defined for the benchmark:

### Layer 0 — Background Mathematics

Purpose: establish depth and scale.

Target properties:

- 2–3 fine traces or interference contours;
- scale around `1.10–1.20×` hero scale;
- opacity target `0.18–0.28`;
- reduced line weight;
- slowest harmonic motion;
- must never dominate the hero.

### Layer 1 — Hero Geometry

Purpose: carry the visual identity.

Target properties:

- 1 primary closed structure;
- optionally 1 secondary crossing structure;
- opacity target `0.72–1.00`;
- primary line weight `1.5–2.0 px` at final 540×960 render;
- maximum visual density occurs near the middle of the loop;
- centred on `C`.

### Layer 2 — Accent Mathematics

Purpose: expose intersections, phase events and high-energy nodes.

Target properties:

- nodes, short traces or localized interference accents;
- opacity target `0.45–0.75`;
- secondary line weight `0.75–1.0 px`;
- frequency/harmonic complexity above the hero;
- sparse enough to preserve negative space.

---

# 7. Density and Negative Space

The visual must preserve deliberate breathing room.

Hard prohibitions:

- full-canvas line saturation;
- continuous edge-to-edge clutter;
- uniform density everywhere;
- filling the Body merely because empty space exists.

The intended composition is:

**low-density field -> concentrated mathematical event -> low-density field**

Aesthetic acceptance requires visible negative space in the Body at all times. The visual centre may become dense, but the outer safe envelope must retain substantially lower visual energy than the hero core.

---

# 8. Colour System

## 8.1 Base background

Canonical background:

`#080B10`

Pure flat black `#000000` is prohibited as the base background.

A subtle mathematical/radial luminance variation is allowed, provided it does not read as texture from an external image.

## 8.2 Canonical palette

- Dominant: `#00F0FF`
- Secondary: `#F72585`
- Highlight: `#FFFFFF`

## 8.3 Parametric colour interpolation

Colour variation must be driven by a deterministic scalar such as phase, local speed or intersection energy.

Canonical conceptual model:

`C(θ,u) = OklabLerp(C1, C2, clamp(0.5 + 0.5·sin(φ(θ,u)), 0, 1))`

The highlight channel is reserved for high-energy intersections, focal nodes and the strongest local maxima.

## 8.4 Colour prohibitions

- no uncontrolled rainbow cycling;
- no hue roulette per frame;
- no independent random colour flicker;
- no saturated multicolour gradients whose sole purpose is spectacle.

A palette variation derived from the seed is allowed only when it remains inside the established cold/neon family.

---

# 9. Light and Optical Treatment

## 9.1 Blend hierarchy

The benchmark expects a restrained additive hierarchy:

- background traces: primarily normal/low-energy compositing;
- hero traces: luminous compositing;
- accents/intersections: additive contribution preferred.

The contract is visual, not shader-specific.

## 9.2 Bloom

Bloom/glow is allowed and expected to be subtle.

Canonical target:

- threshold reference: approximately `0.80` normalized luminance;
- target intensity reference: approximately `0.30`;
- halo must remain subordinate to the underlying geometry.

These numbers are implementation references, not permission to replace sharp geometry with glow.

## 9.3 Intersection light

When several mathematical traces cross or approach one another, local energy may increase.

The intended effect is:

`clean line -> convergence -> local luminous node -> clean line`

not:

`clean line -> entire image blown out`.

## 9.4 Highlight ceiling

Pure white is a scarce resource.

Only the highest-energy points may approach full white. Large continuous white surfaces are prohibited.

---

# 10. Motion Grammar

## 10.1 Allowed motion

Motion may arise from:

- sinusoidal phase evolution;
- harmonic deformation;
- periodic scale breathing;
- periodic rotation with integer loop count;
- interference phase shifts;
- smooth morph envelopes;
- damping-like envelopes that are analytically wrapped to the loop.

## 10.2 Banned motion

- `rotation += constant * delta` as the dominant visual motion;
- constant-speed camera/orbit motion with no evolving geometry;
- frame-local random jitter;
- non-periodic noise added directly to visible coordinates;
- hard state switches.

## 10.3 Rotational motion

Rotation is allowed only as one component of a larger mathematical transformation.

A canonical rotational phase may be:

`θ_rot(u) = θ0 + 2π·k·u`

where `k` is an integer.

The visible result must remain interesting if the viewer mentally removes the global rotation.

---

# 11. Determinism and Seed Contract

## 11.1 Seed role

The seed controls **presentation variation only**.

It must never alter simulation results or consume simulation RNG state.

## 11.2 Seed-derived properties

For the benchmark, the seed deterministically selects:

1. polygon order `N`;
2. rational frequency ratio `a:b`;
3. initial phase `δ0 ∈ [0, 2π)`;
4. deformation amplitude set;
5. phase offsets between layers;
6. dominant colour anchor inside the approved cold/neon range;
7. secondary layer scale relationship.

## 11.3 Static vs temporal randomness

Seed-derived variation is resolved once for the sequence.

The runtime MUST NOT call an unconstrained random function independently at every frame to alter visible state.

No runtime event, wall-clock value, process identifier, GPU timing or machine-specific entropy may change the mathematical result.

## 11.4 State equivalence

For fixed:

`seed + visual parameters + frame index + frame count + implementation version`

there must be exactly one defined mathematical visual state.

Conceptually:

`VisualState = F(seed, visual_parameters, frame_index, frame_count)`

A second evaluation of the same inputs must produce the same state.

---

# 12. Asset Policy

`Geometric Waves v1` contains no artistic image assets.

Allowed:

- mathematical primitives;
- vectors generated at runtime;
- procedural shader operations;
- mathematical colour fields;
- procedural glow.

Prohibited:

- PNG/JPG artwork as the source of the geometry;
- sprite sheets containing the visual effect;
- pre-rendered animation frames;
- AI-generated artwork used as the actual visual content;
- photographic textures used to manufacture the effect.

The visual must be reconstructible from the mathematical definition and deterministic parameters.

---

# 13. Prototype Output Contract

C11-C.1-P must produce exactly one benchmark render for visual review.

## 13.1 Required output

- one physical `MP4`;
- one `GIF` preview;
- one manifest/metadata record sufficient to identify seed, duration, fps and renderer version.

## 13.2 Canonical render settings

- `540 × 960`
- `30 FPS`
- `10.0 s`
- `300 frames`
- social frame enabled
- audio not required for the visual benchmark

## 13.3 Review target

The GIF is the primary human-facing art-direction artifact.

The MP4 is the primary physical-render artifact.

The mathematical state is the primary technical artifact.

---

# 14. Acceptance Gates

Acceptance is divided into machine-verifiable requirements and human visual review.

## Gate A — Contract Integrity

**PASS requires:**

- no modifications to frozen C11-B/C7/C9/simulation contracts;
- no simulation RNG consumption;
- no external image asset dependency;
- correct `540×960 / 30 FPS / 10 s / 300 frames` contract.

## Gate B — Mathematical Determinism

**PASS requires:**

- fixed seed maps to fixed seed-derived parameters;
- frame state at sampled frames is reproducible;
- all loop functions satisfy endpoint equality;
- primary animated parameters satisfy derivative continuity at the seam;
- no frame-local uncontrolled entropy.

Recommended sampled frames for QA:

`0, 75, 150, 225, 299`

and the implicit closure state at `u=1`.

## Gate C — Spatial Integrity

**PASS requires:**

- intentional geometry remains inside `BodyRegion`;
- hero geometry remains inside the `216 px` radial safety envelope;
- no intentional geometry enters Header/Footer;
- optical treatment does not visually bleed into the social frame chrome.

## Gate D — Render Quality

**PASS requires:**

- primary lines are visually sharp at 540 px render width;
- no visible subpixel shimmer caused by unstable sampling;
- secondary traces remain legible but subordinate;
- glow does not erase the mathematical structure;
- intersections produce controlled luminous nodes;
- negative space remains intentional.

## Gate E — Art Direction Benchmark

Manual evaluation against these seven questions:

1. Does it immediately read as mathematical generative art?
2. Does it avoid the screensaver/VJ-effect impression?
3. Does the geometry feel precise enough to justify the “premium” label?
4. Does the motion communicate transformation rather than simple rotation?
5. Does the colour remain controlled and sophisticated?
6. Does the 10-second loop feel naturally self-contained?
7. Does the visual look like it belongs to the same product family that will later contain Fractal Bloom, Sacred Symmetry, Living Particles and Invisible Forces?

A technical PASS does not override a visual FAIL.

---

# 15. Explicit BANNED List

The following are hard failures for C11-C.1:

- pure-black flat background;
- uncontrolled rainbow colour cycling;
- random per-frame colour flicker;
- jitter/noise used as a substitute for animation design;
- simple constant-speed polygon rotation as the main effect;
- geometry drifting persistently away from the optical centre;
- edge-to-edge clutter;
- clipping into Header/Footer;
- pre-rendered image assets as the primary geometry;
- AI-generated artwork used as the effect itself;
- special end-frame correction to fake seamless looping;
- duplicate terminal frame used to hide a discontinuity;
- any change to frozen simulation/maths/RNG contracts.

---

# 16. Prototype Parameter Envelope

The first isolated prototype SHOULD use parameters within this envelope:

| Parameter | Canonical envelope |
|---|---|
| Duration | `10.0 s` |
| FPS | `30` |
| Frames | `300` |
| Polygon order | `{4,5,6,7,8,10,12}` |
| Lissajous ratios | `{3:2, 2:1, 5:2, 3:1, 4:1, 5:1}` |
| Hero line | `1.5–2.0 px` |
| Secondary line | `0.75–1.0 px` |
| Hero radius | `≤ 216 px` |
| Background opacity | `0.18–0.28` |
| Hero opacity | `0.72–1.00` |
| Accent opacity | `0.45–0.75` |
| Base background | `#080B10` |
| Dominant | `#00F0FF` |
| Secondary | `#F72585` |
| Highlight | `#FFFFFF` |
| Visual layers | `3` |
| Primary sampling | `≥ 256` points/curve recommended |

These are benchmark envelopes, not an excuse to use the maximum of every range simultaneously.

---

# 17. Implementation Decision Log

The following decisions are now closed for the prototype:

### D1 — Duration

`10 s` exactly. No 12-second alternative in the gold-standard prototype.

### D2 — Seamless closure

Closure is mathematical and periodic. No exporter seam correction.

### D3 — Golden ratio

`φ` is allowed as a static proportion only, not as a direct non-rational loop frequency.

### D4 — Architecture

`Geometric Waves` is the visual family. A shader is optional implementation detail, not the architectural abstraction.

### D5 — Frozen systems

C11-B frame geometry, simulation, RNG, challenge mechanics and established downstream contracts remain untouched.

### D6 — Visual authority

The physical GIF/MP4 is the authoritative art-direction review surface; technical correctness alone cannot declare the prototype artistically accepted.

---

# 18. C11-C.1-P Build Rule

The first implementation must be the **smallest isolated renderer capable of satisfying this contract**.

Do not introduce:

- new engine abstractions unrelated to Geometric Waves;
- generalized visual-framework refactors;
- new simulation features;
- challenge feature work;
- asset pipelines;
- production-wide renderer rewrites.

The purpose of C11-C.1-P is to answer one question:

> **Can the existing product framework produce a genuinely beautiful, deterministic mathematical visual at premium-product quality?**

Only after the benchmark GIF passes visual review should the family be considered for productive hardening.

---

# 19. Next Checkpoint

`C11-C.1-P — ISOLATED GEOMETRIC WAVES PROTOTYPE`

Required sequence:

`contract -> isolated implementation -> one physical render -> MP4 + GIF -> visual review -> accept/reject -> productive hardening decision`

No second implementation is justified before the first physical render has been reviewed.

---

**End of Contract — C11-C.1 v1.0**  
**Status: APPROVED / CLOSED FOR ISOLATED PROTOTYPE**
