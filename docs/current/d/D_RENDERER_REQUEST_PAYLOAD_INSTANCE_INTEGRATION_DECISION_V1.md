# C11-D — Request→Payload Integration Decision V1

**Date:** 2026-10-27  
**Decision status:** `ACCEPTED_FOR_BOUNDED_NONPRODUCTION_INTEGRATION_IMPLEMENTATION_AND_RUNTIME_REVIEW_ONLY`

## Basis

The operator supplied the Windows result for `test_d_renderer_candidate_request_payload_instance_integration_proposal.py`: exit code 0, strict Draft 2020-12 schema validation, 54/54 proposal source pins and 6/6 schema-negative cases. The previously refreshed candidate I/O report remains 10/10 groups assessed, 0 complete, 6 partial and 4 blocked. This decision records technical acceptance of the proposal for the next bounded engineering gate; it does not convert a test result into I/O readiness.

Pinned proposal artifacts:

- Proposal contract SHA-256: `3e65d03532417502ff9a957bc9a6efca01a974641aeaa1b9b00a11b1bdad4e81`
- Proposal schema SHA-256: `f75a98b9e666a2d668bdbc1f5c5605fb12851b704e0f5ee9df0bd798b0385cba`
- Proposal checkpoint SHA-256: `66bacf230f0b6e931802f9f4eba15b0b73783b8e45989e6731fc6ba3f5a19958`
- Proposal test SHA-256: `965619065a41a609c84a8dabc7302e4d87c4e9e157b0966ef0ba1990faeb3280`
- Frozen C11-C manifest SHA-256: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` (796,318 bytes)

## Decision

Accept preparation and actual bounded runtime review of a **D-only successor V2** to the existing request-scoped materialization-binding interface for exactly the already-contractual fixed review fixtures:

1. Challenge `parking_v2 / CHALLENGE_004`, seed `314159`.
2. Visual Loop `c11c_geometric_waves_v1 / harmonic_membrane`, seed `12345`.
3. Visual Drill `tracking / tier-2`, seed `12345`.

The new path must consume the existing canonical request and dynamic binder, existing fixed materialization-binding V1 and existing editorial sidecar contract. It must hash-join request identity, selector, seeds, profiles, request/plan/bridge/adapter/binding lineage, the dynamic request-specific manifest and editorial values. The dynamic payload digest and the legacy fixture materialization digest are different contract namespaces; the implementation must retain them as separate fields and **must not falsely claim digest equality**. If identity or provenance differs, it must fail closed and emit no joined receipt.

## Limits

This decision authorizes only a stdout-only/in-memory review receipt. It authorizes no persistent payload, output manifest, renderer input, dispatch, pixels, media, or policy approval. It does not expand selector support to the 20-pair Visual Drill matrix. It leaves editorial text in a sidecar and the count of visual-payload text consumption at 0/14. All four blocked I/O groups remain blocked and all six partial groups remain partial until independently evidenced.

## Immutable governance

C11-C 2.19.12 and the frozen manifest remain immutable. `renderer=OFF`, `media_created=false`, `payload_materialized=false`, `candidate_input_admissible=false`, `approved_bindings=0`, `D4.8=BLOCKED`, `D9.10=PREPARE_ONLY`, `D9.14/D9.16=BLOCKED`, `D9.17=BLOCKED_NO_GO`, `D10=BLOCKED_FOR_PROMOTION`, `baseline_approval=MISSING`, `freeze_eligible=false`, and `release_authority=NONE`.

**Decision record SHA-256 (JSON companion):** `68d1e6e992f5d426c9553cbc0ae4da360e94a0cad3363b9b7c89a43e77c34711`
