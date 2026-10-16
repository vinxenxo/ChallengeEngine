# C11-D Timing/Review Reference Carrier — Checkpoint V1

**Status:** `PASS_PREPARATION_ONLY_REFERENCE_ENVELOPES_VERIFIED_NOT_BINDING_NOT_APPROVED`
**Date:** 2026-10-16
**Scope:** five geometric Visual Loop selectors; nine proposed shared timing/review policy references.

## Purpose

This increment specifies a deterministic, selector-scoped reference envelope that a future canonical binding contract can refer to without copying policy semantics into a request or payload. The current runner consumes the already accepted timing/review inheritance audit and the geometric request-chain gap audit as parent evidence. It is a report-only carrier, not an implementation of canonical binding V2.

## Contract and runner

- Contract: `definitions/c11d/production/D_RENDERER_VISUAL_LOOP_TIMING_REVIEW_REFERENCE_CARRIER_CANDIDATE_V1.json`
- Contract schema: `definitions/c11d/production/D_RENDERER_VISUAL_LOOP_TIMING_REVIEW_REFERENCE_CARRIER_CANDIDATE_SCHEMA_V1.json`
- Report schema: `definitions/c11d/production/D_RENDERER_VISUAL_LOOP_TIMING_REVIEW_REFERENCE_CARRIER_REPORT_SCHEMA_V1.json`
- Audit runner: `tools/c11d/d9/d_renderer_visual_loop_timing_review_reference_carrier.py`
- Tests: `tools/c11d/d9/test_d_renderer_visual_loop_timing_review_reference_carrier.py`

## Semantics

The runner prepares five ephemeral reference envelopes. Every envelope contains the exact selector identity and the same nine metadata references `(id, path, SHA-256, expected status, scope, approval-assertion count)`. The source contract body and policy values are never copied; all approval assertions must remain false. A common reference-set digest must be identical across all five selectors, while the selector-envelope digest must be unique for each selector.

This does **not** modify the canonical request, binder V1, payload or renderer input, and does not persist an envelope. The envelopes only appear in the stdout audit report.

## Evidence in reconstructed isolated tree

- Parent timing/review inheritance audit: 13/13 tests; 17/17 source pins; 19 approval assertions checked; 0 approvals granted.
- Parent request-chain gap audit: 10/10 tests; five canonical plans; one existing V1 source-binding review; four selectors still blocked by the fixed V1 timing/review guard.
- The next carrier test suite verifies strict schemas, source pins, deterministic digest behavior, selector identity, reference metadata-only semantics, fail-closed cases and all governance locks.

This is isolated evidence reconstructed from the normalized Oct. 14 snapshot plus the documented overlays; it is not active Windows evidence. The Windows checkout must execute the new tests and audit before the increment is accepted.

## Remaining gates

- Shared policy approvals remain absent (`approvals_granted=0`).
- Canonical binding remains 1/5; the other four grammars remain blocked.
- Candidate I/O completeness, exact selector payload approval and D4.8 authorization remain false/blocked.
- No Godot is invoked by this audit; no request, payload, renderer-native input or media is emitted.
- `renderer=OFF`, `media_created=false`, `D4.8=BLOCKED`, `release_authority=NONE`, D9.10=`PREPARE_ONLY`, D9.17=`BLOCKED_NO_GO`.

## Next action

Run the overlay precondition check/apply on the active Windows checkout, then run its 18-test suite and the audit. If accepted, use the resulting reference envelopes as a design artifact for the next canonical binding contract proposal. Do not modify the existing binder or admit selectors until shared policy approval and exact payload/I/O gates are independently satisfied.
