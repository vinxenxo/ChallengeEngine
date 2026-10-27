# C11-D — Candidate Request → Payload Instance Integration Proposal V1

**Date:** 2026-10-27  
**State:** `PROPOSAL_ONLY_NON_PRODUCTION_INTEGRATION_NOT_IMPLEMENTED_NOT_APPROVED`

## Decision boundary

The active Windows read-only audits report I/O conformance `groups=10/10`, `complete=0/10`, `partial=6`, `blocked=4`, `source_pins=54/54`, and `input_instance_emitted=false`. The candidate identity inventory reports 164 candidate-review source files, fingerprint `0b4168bddac991ac03ea45d424f5af4fa2316c275dc31c1866c5cf8baf532d25`, and report SHA-256 `74e518b620d297c5e09cf6e9495864dbe96e9394b6520e9a5e492775642b92bf`. The identity fingerprint is a declared review-surface fingerprint, not a complete repository-tree fingerprint.

This proposal treats the successful audits as evidence that the report and source identity checks executed correctly—not as input readiness. It creates no runtime implementation and makes no governance transition.

## Actual integration gap

The existing D-owned dynamic request→payload binder already creates hash-closed in-memory manifests for its admitted selector scope, including the Visual Drill V2 matrix. The separate request-scoped materialization-binding V1 remains explicitly fixed-fixture-oriented and says dynamic request transport is not implemented. The missing step is an explicit, validated handoff/join between those two existing interfaces and the candidate I/O contract. Do **not** introduce a second binder.

## Proposed single path

1. Resolve canonical request identity through the existing D9.9 shared request/facade path.
2. Pass the exact request to the existing dynamic request→payload binder version appropriate to its pinned selector scope. Reject unknown or mismatched content type, family, subtype/grammar, variant, tier, profile, seed, and request hash.
3. Propose a versioned successor of the existing request-scoped materialization-binding interface (V2 only if needed) that accepts exactly one verified binder receipt, compares every join key, and returns a **review-only in-memory receipt** joining canonical request, payload manifest/digest, source and policy lineage, and editorial sidecar hashes. It must not materialize persistent payloads or output files.
4. Re-audit all ten candidate I/O groups. An integration receipt does not itself make the candidate input admissible.

## Digest and data-domain rules

`request_hash` identifies the canonical request. `payload_instance_sha256` identifies visual payload state derived under the canonical source/policy and gameplay seed—not merely the seed label. `request_payload_manifest_sha256` closes the exact request-specific manifest under the manifest schema's declared self-hash rule. `music_seed` remains in a separate domain as request metadata and must not enter visual payload generation or its digest. No automatic seed generation or adopted master seed.

Editorial values remain a separate hash-bound sidecar: the observed contract state is 14/14 sidecar values and 0/14 visual-payload consumption. `language` is metadata only. No text injection, visibility evaluation, geometry or layout is inferred from this proposal.

## Refreshed gap ledger

| Group | Current state | Exit requirement (summary) |
|---|---|---|
| `content_identity` | Partial | Close exact identity for explicitly supported selectors; unknown scope fails closed. |
| `source_lineage` | Partial | Join request/plan/bridge/adapter/binder/manifest/policy with exact hashes. |
| `payload_instance` | Partial | Prove equality and independent repeat through the existing materialization interface. |
| `seed_domains` | Partial | Re-capture a verifiable SHA-256-bound cross-type Challenge/Loop seed log; preserve separate gameplay/music domains. |
| `editorial` | Partial | Bind sidecar hash to request lineage; consumption remains a separately gated activity. |
| `delivery` | Partial | Bind selected delivery-profile identity; timebase/projection remain blocked pending approval. |
| `presentation` | Blocked | Separate approval for regions, field visibility and coordinate projection. |
| `timeline` | Blocked | Separate delivery-timebase, temporal alignment and sample-selection approvals; resolve CHALLENGE_008/009 duration conflict under authority. |
| `audio` | Blocked | Separate hash-bound audio/music policy approval and request-specific timeline evidence. |
| `authorization` | Blocked | Independent renderer-baseline approval/freeze and explicit D4.8 authorization. |

## Gates

- **G0 — evidence refreshed:** current I/O audit, all 54 pins and candidate identity inventory (operator result supplied 2026-10-27).
- **G1 — review proposal only:** review this strict schema and integration boundary. No implementation is authorized by writing or applying the proposal artifact.
- **G2 — future bounded runtime receipts:** only after a separate acceptance decision; use the current real Godot 4.7.1 path and preserve complete per-selector receipt rows.
- **G3 — re-audit:** rebuild the ten-group gap report; do not infer completeness from a PASS.
- **G4 — policies and authorization:** separate source-hash-bound approvals. Renderer baseline approval and D4.8 remain missing/blocked.

## Hard locks

C11-C 2.19.12 and its frozen manifest remain immutable at `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` (796,318 bytes). `renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; `approved_bindings=0`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14/D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`. No renderer-native input, dispatch, output manifest, persistent receipt, pixels, media, freeze or promotion is authorized.

## Source binding

The proposal contract embeds the 54 source pins in the latest read-only I/O audit contract and is paired with a strict Draft 2020-12 schema. The application preflight must reject the overlay if the frozen manifest, renderer policy docket, audit contract, or any of the 54 pinned source files differs. Do not refresh pins implicitly.
