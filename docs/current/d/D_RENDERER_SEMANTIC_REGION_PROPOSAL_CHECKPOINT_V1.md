# C11-D Renderer Semantic Region Proposal — Checkpoint V1

**State:** `PREPARATION_ONLY_NOT_APPROVED_NOT_FROZEN`  
**Purpose:** independent review of the proposed semantic region vocabulary and normalized bounds before temporal scheduling.  
**Owner boundary:** C11-D only. The C11-C 2.19.12 source and historical manifest are immutable.

## Why this increment exists

The operator has confirmed Windows PASS for the neutral frame program (3/3 content types, determinism 3/3, editorial flow 3/3, negative controls 19/19, structural schema 3/3; optional `jsonschema` is not installed in Windows). The program carries semantic text declarations but deliberately has no pixel geometry or schedule.

This increment proposes a D-owned normalized layout for independent review. It is still non-executable; all mappings and bounds remain `PROPOSED_NOT_APPROVED`. It must not be used to render, derive pixel coordinates or dispatch any renderer.

## Proposed regions

All bounds use independent normalized per-mille axes (`0..1000`), relative to the resolved delivery canvas; they are not pixel coordinates and do not reuse C11-C's frozen geometry.

| Region | Proposed normalized bounds (x, y, width, height) | Purpose | Intended overlap |
|---|---|---|---|
| `HEADER` | `(50, 40, 900, 140)` | Editorial title and subtitle | No overlap with content/footer |
| `CONTENT_STAGE` | `(35, 200, 930, 610)` | Primary Challenge / Loop / Drill visual payload | Unresolved; visual payload contract is not bound |
| `CHALLENGE_OVERLAY` | `(70, 705, 860, 85)` | Player name and challenge label | Intentional, contained overlap over `CONTENT_STAGE` |
| `FOOTER` | `(50, 850, 900, 100)` | Editorial call to action | No overlap with header/content |

These bounds are design proposals only. Review for hierarchy, visual safe areas, cross-platform font behavior, and compatibility with the actual D-owned simulation visuals. No region has approval status.

## Artifacts

- `definitions/c11d/production/D_RENDERER_SEMANTIC_REGION_PROPOSAL_V1.json` — semantic vocabulary, normalized bounds, field targets, locks and non-approval state.
- `definitions/c11d/production/D_RENDERER_SEMANTIC_REGION_PROPOSAL_SCHEMA_V1.json` — strict Draft 2020-12 output schema.
- `tools/c11d/d9/d_renderer_semantic_regions.py` — pure in-memory proposal builder and independent validator, source-bound to the frame program.
- `tools/c11d/d9/test_d_renderer_semantic_regions.py` — 3 content types, determinism, editorial-field routing, schema and 20 fail-closed negatives.

## Test boundary

The focused test must confirm the exact proposed regions, valid normalized bounds, field-to-region mapping, no self-approval, source-lineage continuity, and no schedule/pixel/media/render/dispatch authority. It writes no files and launches no external process. Keep this test separate from the 22-step aggregate until focused Windows acceptance and review.

## Gate to the first video

This is the final layout-review prerequisite, not the video test itself. The next stages are: (1) operator/technical approval or revision of this D-owned semantic layout; (2) a duration/frame schedule contract derived from an explicit, supported content-duration input; (3) an isolated test renderer candidate and deterministic visual/audio test plan; (4) source fingerprint and independent renderer-baseline review; and (5) separate explicit D4.8 governance authorization before any governed real-media D9.14 execution. No local code or passing test may grant that authorization.

## Invariants

C11-C 2.19.12/manifest immutable; D9.10 adapter `PREPARE_ONLY`; renderer OFF; no media created; D4.8 BLOCKED; `release_authority=NONE`; D9 OPEN; D10 BLOCKED. The five candidate blockers remain. This checkpoint does not approve/freeze the renderer baseline or C11-D baseline.
