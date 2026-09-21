# C11-C.3 / C11-C.4 — v1.6 Implementation Notes

The physical review packages show the previous weakness clearly:

- Living Particles: seeds remained visually close to a sparse bioluminescent cloud.
- Sacred Symmetry: seeds remained visually close to one golden concentric astrolabe.

v1.6 changes the macro grammar selected by the seed. This is not a cosmetic randomizer.

## Physical review coverage seeds

Living Particles: `424242`, `112358`, `161803`, `314159`, `246802` cover all five grammar modes with the deterministic variation mixer.

Sacred Symmetry: `314159`, `271828`, `161803`, `577215`, `8675309` cover all five grammar modes. Their symmetry orders are not forced: the N parameter remains seed-controlled and must stay inside `{4,6,8,12}`.

## Production boundary

The new v1.6 shaders are still isolated prototypes. The formal production requirement of 10,000–50,000 GPU micro-particles for Living Particles remains a production target and is not weakened by the lightweight analytic benchmark.
