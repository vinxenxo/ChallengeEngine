# C11-D Renderer Region Hierarchy Reconciliation — Checkpoint V1

**State:** `PREPARATION_ONLY_RECONCILIATION_NOT_RENDERER_INPUT`  
**Date:** 2026-10-10  
**Depends on:** D1.5 existing platform layout contract; C11-C 2.19.12 frozen presentation source  
**Scope owner:** C11-D; no frozen C11-C source or manifest is changed.

## Decision

Do not create a second canonical layout by replacing the existing shared frame with the previous normalized-permille proposal. The current repository already has two related, deliberately distinct presentation concepts:

1. **Shared social frame:** D1.5 records a 540×960 logical canvas and the existing full-width regions `HEADER=(0,0,540,144)`, `BODY=(0,144,540,672)`, `FOOTER=(0,816,540,144)`.
2. **Content/profile composition:** `PresentationProfile.get_social_regions()` describes the full shared frame, while `PresentationProfile.get_composition_geometry()` derives canvas/safe/header/content/footer geometry from the selected profile and safe area. These methods are intentionally not equivalent.
3. **Family/mechanic presentation:** `VisualLoopPresentationBinder` carries existing composition geometry and the generated visual frame state; `VisualLoopRenderer` routes to the five existing generator/rendering paths. The family catalog resolves identity and routing names; it does not, by itself, declare five sets of normalized region rectangles.
4. **Overlay role:** D1.5 reserves `BodyUIOverlay` for presentation overlays. A Challenge-specific semantic overlay does not thereby become a fixed global rectangle. Use the existing content/presentation contract when a particular overlay has supported layout semantics.

The previous `D_RENDERER_SEMANTIC_REGION_PROPOSAL_V1` is retained because its focused contract/test have already been accepted as a **proposal-generation and fail-closed test**. Its coordinates `(50,40,900,140)`, `(35,200,930,610)`, `(70,705,860,85)`, `(50,850,900,100)` are not approved, not canonical, and must not be used as the temporal schedule's spatial source. This reconciliation does not approve geometry; it identifies the existing source-of-truth hierarchy for future D work.

## Explicit layout hierarchy

| Level | Authority | Responsibility | Rule |
|---|---|---|---|
| Delivery profile | Existing metadata | Output dimensions/FPS/encoding | Metadata is not renderer permission |
| Shared social frame | Existing D1.5 contract | `HEADER` / `BODY` / `FOOTER` partition | Preserve 540×960 logical geometry |
| Presentation profile | Existing profile resolution | Safe area, content geometry, composition policy | Resolve per selected profile; do not hard-code a replacement |
| Content family/mechanic | Existing binder and renderer route | Family-specific visual payload and composition | Preserve identity/routing; no generic family boxes inferred from names |
| Presentation overlay | Existing binder/overlay contracts | Editorial and content-specific text/overlay roles | No invented fixed `CHALLENGE_OVERLAY` rectangle |

## Files

- `definitions/c11d/production/D_RENDERER_REGION_HIERARCHY_RECONCILIATION_V1.json` — current D-owned reconciliation contract and immutable C11-C manifest pin.
- `definitions/c11d/production/D_RENDERER_REGION_HIERARCHY_RECONCILIATION_SCHEMA_V1.json` — strict Draft 2020-12 schema for the in-memory report.
- `tools/c11d/d9/d_renderer_region_hierarchy.py` — read-only contract/source validator and deterministic in-memory reconciliation report builder.
- `tools/c11d/d9/test_d_renderer_region_hierarchy.py` — 3 supported content types, determinism, five-family identity/routing catalog, schema and 21 negative controls.

The test reads existing D1.5/profile/renderer sources and checks the exact immutable manifest hash; it writes no files and launches no engine or media tool. The focused test is not registered in the 22-step aggregate until Windows acceptance.

## Next step after focused acceptance

Prepare the temporal schedule as a separate proposal only after confirming that its phase order and durations come from explicit, supported content-duration/timeline contracts. The schedule must consume the current layout hierarchy, not the old normalized region boxes. If the canonical duration for a content type is unknown, preserve `UNKNOWN` and fail closed rather than infer it. No frame indices or durations are emitted by this checkpoint.

## Invariants

- C11-C 2.19.12 and `release/C11C_FREEZE_PACKAGE_MANIFEST.json` remain immutable; required manifest SHA-256 is `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- D9.10 adapter remains `PREPARE_ONLY`.
- No renderer-native input, dispatch, activation, production, media, or output path.
- `D4.8=BLOCKED`, `release_authority=NONE`; D9 OPEN; D9.14/D9.16 gated; D9.17 `BLOCKED_NO_GO`; D10 BLOCKED.
- No geometry/schedule approval, renderer-baseline approval/freeze, or C11-D baseline freeze is created here.

## Temporal-topology follow-up (2026-10-10)

The next isolated increment is documented in `D_RENDERER_TEMPORAL_SCHEDULE_PROPOSAL_CHECKPOINT_V1.md`. It derives topology strictly from the existing C11-C timing sources: Challenge phase order is `HOOK → GAME → REVEAL → CTA`; Visual Loops and Visual Drills remain continuous spans without invented subphases. No concrete durations or frame coordinates/ranges are emitted. The earlier normalized-permille proposal remains noncanonical and is not a temporal source.
