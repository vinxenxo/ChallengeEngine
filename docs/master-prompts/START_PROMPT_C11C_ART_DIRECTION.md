# START PROMPT — C11-C ART DIRECTION

## Preconditions

Continue from the **validated and committed C11-B organized repository**. The organization checkpoint must have passed the complete runbook and been committed before C11-C work begins.

Read, in order:

1. `docs/master-prompts/MASTER_HANDOVER_C11_B_REPOSITORY_ORGANIZATION.md`
2. `docs/00_PROJECT_OVERVIEW.md`
3. `docs/01_ARCHITECTURE.md`
4. `docs/02_DATA_AND_CONTRACTS.md`
5. `docs/03_PRESENTATION.md`
6. `docs/04_REPOSITORY_STRUCTURE.md`
7. `docs/05_TESTING_AND_REGRESSION.md`
8. `docs/06_PRODUCTION_AND_DISTRIBUTION.md`
9. `docs/07_ROADMAP.md`
10. `docs/contracts/C11_ARCHITECTURE_MANIFESTO.md`
11. `docs/checkpoints/C11_FREEZE.md`
12. `artifacts/tests/reports/C11_FREEZE_CERTIFICATE.json`
13. `artifacts/tests/reports/C11_FREEZE_SHA256_MANIFEST.json`

## Mission

Define and implement the product's visual language from the reference images supplied by the project owner.

The purpose of C11-C is visual quality, not architectural reinvention.

## First phase: reference inventory

Before changing presentation code:

1. inventory every supplied reference image;
2. record dimensions and major visual regions;
3. identify common traits across families;
4. separate common design-system tokens from mechanic-specific art;
5. convert subjective observations into measurable design constraints.

Owner references belong in `assets/reference/`. Generated comparisons belong under `artifacts/`.

## Allowed

- backgrounds and visual assets;
- typography;
- palette, gradients and surfaces;
- borders, shadows, badges and icons;
- visual hierarchy;
- passive renderer styling;
- presentation-only emphasis and animation that does not alter gameplay timing truth.

## Frozen

Do not change without a new checkpoint:

- simulation mathematics;
- RNG algorithm, version or ownership;
- canonical challenge/visual definitions;
- `SimulationResult`;
- winning-frame detection;
- `RenderedFrameStream` semantics;
- canonical visual envelope semantics;
- C7 audio contracts;
- C9 authoring contracts;
- C11-B Header/Body/Footer structural geometry.

## Working method

```text
REFERENCE
   ↓
VISUAL INVENTORY
   ↓
DESIGN TOKENS / CONSTRAINTS
   ↓
ONE REPRESENTATIVE ROUTE
   ↓
PHYSICAL RENDER
   ↓
OWNER REVIEW
   ↓
VISUAL REGRESSION
   ↓
PROPAGATION
   ↓
C11-C FREEZE
```

Never solve a visual mismatch by changing verified gameplay data merely to make the frame look better.
