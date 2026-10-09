# C11-D Renderer Editorial Review Manifest — Checkpoint V1

**Status: implementation and local preparation tests PASS; Windows operator acceptance pending.** This manifest bridges the canonical D9.9 editorial chain to the existing temporal reference without emitting renderer input or creating a media artifact.

## Canonical review chain

`D9.9 canonical request/plan → D9.10 bridge record → PREPARE_ONLY D adapter envelope → candidate binding preview → logical composition → renderer-neutral frame program → source-bound temporal reference → editorial review manifest`

The manifest revalidates the upstream products rather than trusting their supplied hashes. Exact strings and SHA-256 values are copied from the verified frame-program instructions and compared against `plan.editorial`. `language` is a locale attribute rather than a visible text element. Proposed target-region IDs remain `PROPOSED_NOT_APPROVED`, geometry stays unresolved, and field-specific frame ranges stay null.

## Three distinct timing relationships

- **Challenge:** the test fixture is explicitly `CHALLENGE_004`, so its timing reference binds to the same challenge source and validates the `parking_v2` mechanic. Its authored temporal source is 60 FPS, whereas the selected `REVIEW_720` delivery target is 30 FPS. The manifest flags `MISMATCH_REQUIRES_EXPLICIT_NORMALIZATION`; it does not resample.
- **Visual Loop:** the selected grammar must belong to the current Producer family and that family's internal identity must match the canonical `geometric` timing reference. The timing source is family-level only; the grammar-specific rendered payload is not bound.
- **Visual Drill:** the selected `tracking` type and `tier-2` must match the canonical timing source and its `difficulty_tier`. The generated request-specific visual payload is not bound.

These distinctions intentionally prevent the manifest from overstating what has been proven. The manifest permits a person to review the exact copy and source timing; it never reports that a video is ready to render.

## Focused implementation

- Contract: `definitions/c11d/production/D_RENDERER_EDITORIAL_REVIEW_MANIFEST_V1.json`
- Output schema: `definitions/c11d/production/D_RENDERER_EDITORIAL_REVIEW_MANIFEST_SCHEMA_V1.json`
- Implementation: `tools/c11d/d9/d_renderer_editorial_review_manifest.py`
- Focused test: `tools/c11d/d9/test_d_renderer_editorial_review_manifest.py`

The focused matrix exercises 3 content types, determinism, exact editorial parity, temporal-source alignment, strict JSON Schema Draft 2020-12, 28 negative cases, source-lineage path/order enforcement (25 pinned inputs including the delivery-profile registry), and hashes for the review contract, schema, implementation and source lineage. The frozen C11-C manifest digest is named explicitly as `frozen_c11c_manifest_sha256` to avoid confusing it with the review manifest’s own digest.

## Acceptance command

```powershell
python -m py_compile .\tools\c11d\d9\d_renderer_editorial_review_manifest.py .\tools\c11d\d9\test_d_renderer_editorial_review_manifest.py
python .\tools\c11d\d9\test_d_renderer_editorial_review_manifest.py
```

## Governance

This checkpoint does not approve editorial layout, temporal topology, the D renderer baseline, or D4.8. It does not turn renderer dispatch on. C11-C remains an immutable reference. Baseline preflight, full D acceptance and explicit governance approval are still required before any controlled video test.

## Follow-up — delivery timebase projection (2026-10-10)

The identified Challenge source/delivery FPS mismatch is now expressed by separate contract `D_RENDERER_DELIVERY_TIMEBASE_PROJECTION_V1`. Its cumulative-boundary mapping is review-only and unapproved; the editorial review manifest's open simulation sampling and per-field visibility decisions remain unresolved. This does not promote `video_render_ready`.
