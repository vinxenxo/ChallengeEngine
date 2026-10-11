# D Renderer Candidate Identity Inventory — Checkpoint V1

**State:** `IDENTITY_ONLY_REVIEW_PACKET_NOT_BASELINE_READY`  
**Date:** 2026-10-11  
**Scope:** read-only identity packet for the declared D-owned renderer preparation surface.  
**Approval:** none; this checkpoint is not a renderer baseline approval, C11-D baseline approval, freeze, production, or release authorization.

## Result

The inventory contract pins the exact SHA-256 of every declared source artifact and derives a deterministic `source_fingerprint` from sorted `{path, role, sha256, size_bytes}` rows. It also reports the exact pinned C11-C freeze manifest, review-context document hashes, Python/runtime host version, the Godot project-declared features, and (when `godot`/`godot4` is on `PATH`) its version obtained only through `--version`. The report is generated in memory; the CLI defaults to a concise fingerprint/toolchain summary and `--full-report` emits the complete JSON packet to stdout. It never persists the report.

`fingerprint_scope` is explicitly the declared renderer candidate review surface, not the full repository tree. The full-tree candidate evaluator remains separately authoritative for overall source integrity and the operator’s live evidence/maintenance ledgers remain local operational inputs.

## Candidate identity facts

- Candidate identity: `D-RENDERER-CANDIDATE-IDENTITY-REVIEW-0.1`.
- Binding preview, logical composition, neutral frame program, request-scoped binding/materialization, and payload-preview components are present and pinned.
- A renderer implementation/build artifact is **not** asserted: `renderer_implementation=NOT_IMPLEMENTED`, `renderer_build_artifact=NONE`. The candidate binding preview is not a renderer.
- Review packet cannot self-approve. `renderer=OFF`, renderer input/dispatch absent, media absent, `D4.8=BLOCKED`, `release_authority=NONE`, `baseline_approval=MISSING`, `freeze_eligible=false`.
- Five candidate-preflight blockers remain: D9.14 real-media certification, D9.16 full acceptance, D9.17 closure, renderer baseline approval, and D baseline approval.
- Longform remains unsupported. Editorial region, visibility, timebase, sampling/interpolation and audio policies remain proposed where their source contracts say so.

## Artifacts

- Contract: `definitions/c11d/production/D_RENDERER_CANDIDATE_IDENTITY_INVENTORY_V1.json`.
- Strict report schema: `definitions/c11d/production/D_RENDERER_CANDIDATE_IDENTITY_INVENTORY_SCHEMA_V1.json` (Draft 2020-12).
- Read-only CLI: `tools/c11d/d9/d_renderer_candidate_identity_inventory.py`.
- Tests: `tools/c11d/d9/test_d_renderer_candidate_identity_inventory.py`.

The test verifies stable fingerprints, exact manifest linkage, governance locks, schema validity, path safety, pinned-source drift rejection and no persistence. It does not run Godot harnesses or render media.

## Next gate

Review this identity packet and the five blockers. This increment does **not** generate `D_RENDERER_BASELINE_APPROVAL_CHECKPOINT.md` as approved or `D_BASELINE_APPROVAL_CHECKPOINT.json` as approval. Do not dispatch/render until the independent renderer baseline approval/freeze and explicit D4.8 authorization exist and the remaining D9 gates are closed.
