# C11-E E4B Loop Current-Hash Policy Decision Docket — V2

**Fingerprint capture:** `LOOP22_R1P_POLICY_20261108T234635Z` (active-checkout read-only run)
**Current project continuation:** operator approved continuation on 2026-11-09. This is not interpreted as a hash-specific policy decision.
**R1V prerequisite:** `PASS_TEST_ONLY_OPERATOR_ACCEPTED`; ten combined slots, ten visual/editorial/layout passes and ten audio/music listening passes.

## Decision protocol

For each row, explicitly select `APPROVE AS PROPOSED`, `REQUEST CHANGES`, or `DEFER`, and confirm the complete SHA-256 shown. A general instruction to continue the project does not substitute for confirming the exact proposal fingerprint. A decision is binding only after it is recorded in a versioned D-owned record with the exact hash, rationale, operator/date and focused positive/negative tests.

## Current-hash decisions

| Group | Proposal | Active-checkout SHA-256 | Bytes | Match to R1P archived pin | Gate | Decision | SHA confirmed | Rationale / change | Operator + date |
|---|---|---|---:|---|---|---|---|---|---|
| A.1 — Shared presentation semantic regions | `definitions/c11d/production/D_RENDERER_UNIFIED_PRESENTATION_REGION_POLICY_PROPOSAL_V1.json` | `101092bb32127bb8854a501a9215c0b6cf69581594383903716907d49719c01a` | 9440 | YES | D-only Loop visual consumer | **PENDING** | **PENDING** | PENDING | PENDING |
| A.3 — Loop/Drill editorial field windows | `definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json` | `609a4d183aac07c2cbe1abaf41444160fdd137217faffbead3aef618320d57dc` | 8376 | YES | D-only Loop visual consumer | **PENDING** | **PENDING** | PENDING | PENDING |
| E4B_LOOP — E4B Loop outer editorial composition | `definitions/c11d/production/C11E_E4B_LOOP_EDITORIAL_COMPOSITION_PROPOSAL_V1.json` | `9e206704665ea85226ecc10854be9f679c32fe9ed7efb690a829f6e8456d43da` | 5528 | YES | D-only Loop visual consumer | **PENDING** | **PENDING** | PENDING | PENDING |
| B.1 — Unified delivery timebase | `definitions/c11d/production/D_RENDERER_UNIFIED_DELIVERY_TIMEBASE_POLICY_PROPOSAL_V1.json` | `41a62b0766db47cd99772f28642ef67766314f20f0f7891789d6b7497bbfee85` | 9507 | YES | A/V timebase, mux and delivery | **PENDING** | **PENDING** | PENDING | PENDING |
| D.1 — Unified audio/music delivery | `definitions/c11d/production/D_RENDERER_UNIFIED_AUDIO_MUSIC_DELIVERY_POLICY_PROPOSAL_V1.json` | `3dd4874e1b6506de6d9ddbe6ad1b567a284b94cc00ef1bac0d35d1731af05e23` | 7457 | YES | Family-native music, AAC mux and A/V delivery | **PENDING** | **PENDING** | PENDING | PENDING |

## Dependency interpretation

- A.1, A.3 and E4B_LOOP: required before implementing the D-only Loop visual consumer. These decisions do not authorize renderer-native input by themselves.
- B.1 and D.1: required before family-native audio generation, AAC mux and A/V delivery for the expanded 22-selector scope. The five-selector R1V AV approval is not silently extended.
- No decision in this docket activates D4.8, D9.10 dispatch, renderer input or production authority. D9.9/R1P request-bound materialization remains plan-only.

## R1P projection boundary

The paired projection report verifies 27/27 request-scoped parameter receipts and isolates the 22 non-pilot selectors. Their payloads were materialized in memory; no prototype Node, C11-C launcher, renderer-native input, audio generator, FFmpeg, FFprobe or media was invoked by this audit.

## Governance

- R1V closeout receipt SHA-256: `a9e1de310ba1f52bab029a6fc6f926892264dd25cfa5edd8ec90aec460a2662a`.
- Frozen C11-C manifest SHA-256: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` (796,318 bytes); immutable.
- Renderer OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`.
- No Git checks; operator-managed commits; no C11-C source writes.
