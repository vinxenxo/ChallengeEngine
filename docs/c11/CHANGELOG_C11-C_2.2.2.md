# C11-C 2.2.2 — Presentation hotfix: review envelopes, typography and Tron contrast

## Common presentation

- Header target font increased from 21 to 23 logical px.
- Header fitting now measures each rendered line independently against the 468px logical content width, preserving the 36px side margins.
- Existing double-line header placement and Matrix sequence remain unchanged.
- Footer target remains 14 logical px.
- Visual Drill review metadata now correctly declares Matrix ON.

## Visual Drill review toolchain

- Fixed the null `-LiteralPath` failure caused by requesting seeds not present in the fixed C11-A qualification matrix.
- The reviewer no longer depends on the fixed 54-run C11-A matrix for requested Drill seeds.
- Added `C11CVisualDrillReviewEnvelopeGenerator.gd` to generate review-only envelopes for the exact requested seeds through the canonical authoring generator.
- Added `-Smoke` to support a single-seed, all-four-family review run.
- Five-seed review remains the default contract.
- Review catalog and sidecars now report Matrix ON and revision 2.2.2.

## Living Particles

- Fixed composition ordering so the Tron road is actually behind the particles instead of being hidden by the particle shader's opaque background.
- Added a dedicated Body background layer.
- Particle shader now renders transparent particle content over the background/road.
- Tron road uses a saturated complementary hue derived from the effective particle palette, with a deterministic fallback for low-saturation references.
- Increased road/grid visibility while preserving the existing forward-travel perspective motion.

## Frozen boundaries

No changes to simulation mathematics, mechanics, RNG ownership, `SimulationResult`, `winning_frame`, `close_calls`, `RenderedFrameStream`, C7 audio contracts, C9 authoring contracts or C11-B logical Header/Body/Footer geometry.
