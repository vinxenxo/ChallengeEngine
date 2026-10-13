# C11-D — Request-Specific Payload Manifest Checkpoint V1

**State:** `PREPARATION_ONLY_HASH_CLOSED_REQUEST_BOUND_MANIFEST_NOT_RENDERER_INPUT`  
**Purpose:** consolidate the request identity, payload identity and pinned lineage already produced by the D-only dynamic binder. This is an additive extension of the existing binder, not a second resolver or dispatch path.

## What is newly covered

Every one of the ten bounded dynamic-matrix receipts now carries a strict `payload_manifest` with four sections:

- `request_identity`: request ID/type, canonical selection and request hash, plan/editorial hashes, separate gameplay/music seeds, variation index and presentation/delivery profile IDs.
- `source_lineage`: D9.10 bridge, PREPARE_ONLY adapter, request binding, binding preview, logical composition, neutral frame program, timebase preview, delivery projection, editorial review manifest, selected definition/registry and source-lineage identities.
- `payload_identity`: payload and visual-state hashes, bounded scope, selector materialization flag, memory-only materialization mode, and optional Loop grammar-instance hash.
- `governance`: candidate input inadmissible, not render-ready, no renderer-native input/dispatch/media, D4.8 BLOCKED and release authority NONE.

`manifest_sha256` is the SHA-256 of canonical JSON excluding only the `manifest_sha256` field itself. Its digest is cross-bound by the receipt's `source_identity`, `payload_evidence`, and `request_binding_sha256`. Strict-schema and semantic validation reject altered lineage, request identity mismatch, stale digests, self-approval, renderer admission, or altered governance locks.

## Preparation validation recorded here

The isolated preparation tree's updated Python contract currently passes 12/12 checks, 46/46 source pins, 2/2 schemas, 10/10 mocked cases, 10/10 manifest closures and 22 fail-closed negatives. The gap audit contract also passes 8/8 with 38/38 pins. These values describe the isolated preparation tree only until the operator confirms the corresponding updated outputs from the active Windows checkout.

Earlier operator-confirmed runtime results remain valid for the prior binder version: actual Godot 4.7.1 dynamic matrix 10 cases and the independent Visual Loop grammar/parameter gates passed, with `HARMONIC_MEMBRANE_COMPOSITE_MATERIALIZED`. The newly added manifest envelope is emitted after the existing harness summaries and must be revalidated on Windows by rerunning the Python contract test plus the ten-case runner; capture all ten `request_payload_manifest_sha256` receipt lines and check their uniqueness/closure. No need to rerun unrelated base GUI tests for this focused data-contract change unless a regression fails.

## Current I/O assessment

The most recent reconciled contract continues to report 0/10 input groups complete, 6 partial (`content_identity`, `source_lineage`, `payload_instance`, `seed_domains`, `editorial`, `delivery`) and 4 blocked (`presentation`, `timeline`, `audio`, `authorization`). The exact payload manifest closes lineage for only the three pinned selector representatives. It does not provide catalogue-wide selection/variant coverage or supply approved region, visibility, timebase, coordinate, audio, renderer input, baseline or release policy.

## Next work in parallel after Windows acceptance

1. Re-run dynamic binder contract tests and the real ten-case Godot runner; preserve the complete stdout receipts.
2. Refresh the source-pinned I/O gap audit and candidate identity inventory, then run unified review, cross-suite lifecycle and baseline-candidate preflight.
3. Reconcile the policy proposal set in `D_RENDERER_POLICY_APPROVAL_DECISION_PACKET_V1.md`. The packet organizes decisions only; every proposal stays unapproved until the operator explicitly chooses or revises the policy.
4. Expand selector/family/tier coverage only where the canonical catalog and D-owned authoring/adapter path prove support. Do not claim that three representative selectors cover the full catalog.

## Governance locks

Frozen C11-C manifest SHA-256: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. C11-C 2.19.12 and its freeze package stay immutable. `renderer=OFF`; `media_created=false`; `D4.8=BLOCKED`; `release_authority=NONE`; baseline approval missing; `freeze_eligible=false`; D9.14/D9.16 remain blocked as required; D9.17 NO-GO; D10 blocked. Visual editorial consumption remains 0/14 until separate policy approval and implementation. This checkpoint authorizes no renderer input, dispatch, shader execution, media generation, freeze or promotion.

## Long-term cutover target

Only after all C11-D gates close, formal baseline approval and freeze are completed, and the promotion/cutover is explicitly accepted, the D branch and its Producer are intended to replace frozen C11-C as the authoritative baseline and Producer. This target is not current authority and does not change the frozen C11-C files or manifest.
