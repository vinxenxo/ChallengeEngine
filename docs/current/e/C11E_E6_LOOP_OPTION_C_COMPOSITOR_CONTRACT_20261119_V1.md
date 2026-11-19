# C11-E E6 Visual Loop — D-owned Option C Post-Compositor Contract V1

**Status:** `CONTRACT_FOR_STATIC_IMPLEMENTATION_AFTER_A3_RECEIPT_RECONCILIATION`  
**Date:** 2026-11-19  
**Scope:** six E6 Smoke18 Loop rows; visual/editorial/layout post-composition only. No renderer or media authority is created here.

## 1. Existing approved architecture boundary

Use one D-owned post-compositor at the existing D boundary:

`Producer GUI/CLI -> E1 shared service -> D9.9 resolver -> D9.10 editorial bridge -> D-only adapter envelope -> existing request-scoped family binding -> unmodified C11-C family visual output -> D-owned Option C outer compositor`.

Do not add a Producer, sixth family module, second binder, geometric-only binder, alternate renderer, or parallel GUI/CLI path. The existing `c11e_production_service.py` is the shared GUI/CLI entry. Its E4B Loop path already checks the five exact operator decisions and builds the D9.10 bridge, D-only adapter envelope and family-stage contract in PREPARE_ONLY.

A.1, A.3, E4B composition, B.1 and D.1 approvals are recorded against their exact proposal hashes in the E4B decision record. The active A.3 lineage transition still requires a genuine PASS in the V2 receipt diagnostic before compositor implementation.

## 2. Immutable source-frame rule

The compositor receives the completed C11-C visual frame as an input image. It must:

- preserve original source bytes/decoded pixel identity in the image area; do not paint editorial text into the source frame;
- avoid crop, stretch, time remap, FPS conversion or frame reordering in the compositor;
- place the frame in a separate outer presentation canvas, using a uniform transform only;
- emit one deterministic D-owned composition record bound to the request, family-stage contract and input frame hash;
- keep source frame identity, grammar, metrics, palette, cycles, Matrix transition, mechanics, timeline and source frame order unchanged.

No C11-C source, generator, binder, family scene, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, canonical definition or frozen manifest may be changed.

## 3. Candidate 9:16 presentation geometry

The approved D semantic regions and E4B proposal define an outer 720×1280 canvas. The candidate source-frame placement is the uniformly scaled 504×896 rectangle at x=108, y=192. This leaves a 192-pixel top band, 192-pixel bottom band and 108-pixel side gutters. The original frame aspect ratio remains 9:16.

- `HEADER`: top band; title/subtitle ownership.
- `BODY`: the complete original source frame, uniformly contained.
- `FOOTER`: bottom band; CTA ownership.

These are logical semantic roles. Exact typography, font, line breaking, padding and any text-specific constraints must come from the current approved D1.5/region/field-window contracts; do not invent a new font or move fields across regions. Do not assume geometry arithmetic proves raster legibility.

## 4. Editorial data contract

Preserve all four canonical Loop editorial values and their explicit blank/UNKNOWN semantics in the D9.10 envelope. Do not omit a key because it is blank. Language is metadata, not a free-form layout field. Title/subtitle/CTA render only in their approved regions/windows. Ownership must be singular: no native C11-C duplicate text may be suppressed unless the exact approved adapter contract says it is migrated into the D shared band.

## 5. Smoke18 Loop identities

| Row | Family / grammar | Gameplay seed | Music seed | Prior timebase |
|---|---|---:|---:|---|
| L-01 | `fractal_bloom / radial_bloom` | 100006 | 500006 | 30 fps / 22 s |
| L-02 | `geometric_waves / harmonic_membrane` | 100001 | 500001 | 30 fps / 23 s |
| L-03 | `invisible_forces / dipole_field` | 100021 | 500021 | 30 fps / 22 s |
| L-04 | `living_particles / swarm` | 100016 | 500016 | 30 fps / 20 s |
| L-05 | `sacred_symmetry / astrolabe` | 100011 | 500011 | 30 fps / 23 s |
| L-06 | `geometric_waves / interference_plane` | 100002 | 500002 | 30 fps / 23 s |

These are evidence-reuse candidates, not E6-accepted rows. Preserve the original A/B media and exact family-native profile/timebase; do not normalize `interference_plane` to the CH004 color-range profile or re-encode predecessor media merely to create uniformity.

## 6. Family-native music and seed separation

Visual output is driven by `request.seed`; music provenance is driven separately by `request.music_seed`. Keep each Loop family/profile and its native C11-C family music generator. Do not route Loop through the Challenge `challenge_8bit_v1` fixture or Challenge D3 V5. B.1 and D.1 decisions are recorded, but media/audio tool use still requires the scoped Smoke18 TEST_ONLY successor and exact process pins.

## 7. Required static test suite before any visual render

1. Exact current A.1/A.3/E4B/B.1/D.1 decision hashes and A.3 single-pointer lineage attestation.
2. All six family/grammar identities resolve through the existing request-scoped family binding; no selector-specific fallback and no geometric-only path leak.
3. D9.9 intent, D9.10 bridge, adapter envelope and family-stage contract hashes cross-reference consistently.
4. All four canonical editorial keys remain present; blank/UNKNOWN/language semantics are exact; no implicit defaults.
5. Geometry checks: canvas 720×1280, body rect x=108/y=192/w=504/h=896, aspect ratio preserved, no crop or overflow outside canvas.
6. Source-frame pixel/hash invariance before and after composition; only the outer canvas/bands differ.
7. Text box bounds, clipping, overflow, contrast, Unicode NFC and deterministic wrapping. Static tests are not a substitute for actual font availability/shaping/legibility review.
8. No duplicate native/editorial ownership of title, subtitle or CTA.
9. A/B visual repeatability for equal `request.seed`; music seed changes do not perturb visual output; family-native music provenance remains separate.
10. PREPARE_ONLY governance assertions: no renderer-native input, process launch, audio generation, mux, media write, BatchId or release authority.

## 8. Render gate

A successful static suite permits only preparation of the scoped visual TEST_ONLY render manifest. Before rendering, the scoped D4.8 successor and E6 TEST_ONLY manifest must pin executable paths, versions/hashes, exact invocations/counts, input/output roots, output naming, one-shot identity, stop-on-first-failure and visual acceptance criteria. Original D4.8 V2 remains immutable and globally BLOCKED.
