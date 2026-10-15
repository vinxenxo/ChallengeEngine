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
- Binding preview, logical composition, neutral frame program, request-scoped binding/materialization, payload-preview components, the existing dynamic binder and the accepted Visual Drill V2 contract/harness/test are declared and pinned.
- A renderer implementation/build artifact is **not** asserted: `renderer_implementation=NOT_IMPLEMENTED`, `renderer_build_artifact=NONE`. The candidate binding preview is not a renderer.
- Review packet cannot self-approve. `renderer=OFF`, renderer input/dispatch absent, media absent, `D4.8=BLOCKED`, `release_authority=NONE`, `baseline_approval=MISSING`, `freeze_eligible=false`.
- Five candidate-preflight blockers remain: D9.14 real-media certification, D9.16 full acceptance, D9.17 closure, renderer baseline approval, and D baseline approval.
- Longform remains unsupported. Editorial region, visibility, timebase, sampling/interpolation and audio policies remain proposed where their source contracts say so.

## Artifacts

- Contract: `definitions/c11d/production/D_RENDERER_CANDIDATE_IDENTITY_INVENTORY_V1.json`.
- Strict report schema: `definitions/c11d/production/D_RENDERER_CANDIDATE_IDENTITY_INVENTORY_SCHEMA_V1.json` (Draft 2020-12).
- Read-only CLI: `tools/c11d/d9/d_renderer_candidate_identity_inventory.py`.
- Tests: `tools/c11d/d9/test_d_renderer_candidate_identity_inventory.py`.

The test verifies stable fingerprints, exact manifest linkage, governance locks, schema validity, path safety, pinned-source drift rejection, the presence and hashes of the accepted Visual Drill V2 files, and no persistence. It does not run Godot harnesses or render media.

## Next gate

Review this identity packet and the five blockers. This increment does **not** generate `D_RENDERER_BASELINE_APPROVAL_CHECKPOINT.md` as approved or `D_BASELINE_APPROVAL_CHECKPOINT.json` as approval. Do not dispatch/render until the independent renderer baseline approval/freeze and explicit D4.8 authorization exist and the remaining D9 gates are closed.
<!-- C11D_EDITORIAL_VISUAL_CONSUMPTION_PHASE_20261013_IDENTITY_INVENTORY -->


## Current continuation note — 2026-10-15

The Visual Drill V2 request-bound runtime matrix has been accepted by the operator on real Godot 4.7.1: 20/20 selector-tier pairs, 20/20 unique request IDs, 20/20 independent runtime repeats, 20/20 request manifests and 67/67 source pins. Runtime log SHA-256: `27a953d867169a3923049b07e0c3b0555867014ce8ecc51483342b222a777c53`. The follow-up reconciliation overlay adds the V2 request contract, Godot harness and focused regression to this declared identity surface and refreshes explicitly accounted source hashes after the accepted overlay chain. The target inventory size is 152 source artifacts; the active Windows output must confirm the actual count and fingerprint. Any count/fingerprint from before reconciliation is historical. Do not treat identity PASS as renderer-baseline approval.

## Parent-chain hash reconciliation — 2026-10-15 (prepared overlay; Windows confirmation pending)

The operator confirmed the focused reconciliation PASS in the active Windows checkout and reported the reconciled inventory size as `152` sources. A subsequent parent review exposed historical hashes in some downstream contracts and schema-level source declarations in the reconstructed preparation copy. The current follow-up overlay refreshes the inventory's source hashes, the runner's exact contract/schema pins, and the downstream hash chain. The prepared-copy identity-inventory test passes 10/10 and continues to report `source_count=152`; the candidate is still only an identity review packet, not an approved/frozen baseline.

These new downstream reconciliations have not yet been confirmed on the active Windows checkout. Rerun the focused inventory test and CLI after applying the follow-up overlay. Preserve the local D9.15 evidence ledger and quarantine record; neither is part of the normalized preparation export.
