# C11-C.6 — Production Variation Engine v1.0

The presentation variation manifold is deterministic and isolated under `tools/prototypes/c11c_common/`. It maps `family + seed` to a bounded `Dictionary` consumed only by the Visual Loop prototypes.

The manifold deliberately varies structural presentation parameters (geometry, density, topology, field configuration, rhythm) rather than only phase offsets. Each family retains its contract identity and banned-list constraints.

## Invariants

- No changes to `core/`, `SimulationResult`, simulation math, engine RNG streams, C7, or native challenge timing.
- Same family + same seed produces the same profile.
- Seed changes are intended to be perceptible but bounded.
- Header math is built after the variation profile is resolved, so displayed parameters describe the actual render.
- Footer remains available for prototype/QA and is disabled for production exports via `-NoFooter`.

## Prototype limitation

`Living Particles` and `Invisible Forces` use analytical GPU fragment-loop proxies in this isolated prototype. Their formal production contracts remain the authority for any future high-density implementation.
