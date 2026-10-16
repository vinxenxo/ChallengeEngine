# C11-D Request-Bound Timing/Review Reference Carrier V1 — Overlay Instructions

This is an additive preparation-only overlay. It adds a strict contract, report schema, runner, regression test and dated checkpoint that join canonical D9.9 request/plan hashes to the already verified metadata-only timing/review reference envelopes. It does not edit the canonical binder.

## Overlay properties

- Operation: `ADD_ONLY`; 22 direct source pins.
- Seven repository content files plus the overlay manifest.
- Frozen C11-C manifest SHA-256: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- Approval remains zero; candidate input remains inadmissible; renderer remains off.

## Validation on Windows

Run from `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`, only after applying the ZIP with its manifest guards:

```powershell
python -B .\tools\c11d\d9\test_d_renderer_visual_loop_timing_review_request_bound_reference_carrier.py
python -B .\tools\c11d\d9\d_renderer_visual_loop_timing_review_request_bound_reference_carrier.py --root .
```

Expected summary markers include `request_identity_joins=5/5`, `policy_reference_pairs=45/45`, `canonical_binding=1/5`, `blocked_by_fixed_v1_scope=4/4`, `approvals_granted=0`, `candidate_input_admissible=false`, `renderer=OFF`, and `D4.8=BLOCKED`.

The audit is a request-identity join, not payload binding or policy approval. It never emits renderer-native input or media.
