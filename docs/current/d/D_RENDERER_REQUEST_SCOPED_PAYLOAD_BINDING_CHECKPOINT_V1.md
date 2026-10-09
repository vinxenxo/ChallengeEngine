# C11-D Request-Scoped Payload Binding — V1 checkpoint

**Status:** preparation-only source-resolution audit; no request-scoped visual payload is materialized.

## What this closes

This increment binds the exact D9.9 selection identity to a canonical source-definition reference and verifies the full D9.9 → D9.10 bridge → PREPARE_ONLY envelope → D renderer-neutral binding/composition/frame-program → temporal/timebase → editorial-review chain. It hashes the selected definition and registry inputs, and rejects detached or altered upstream handoffs.

## Representative matrix

- Challenge: `parking_v2 / CHALLENGE_004` resolves to its exact challenge definition and passing D4 subordinate plan. Runtime/simulation visual payload is not materialized by this review chain.
- Visual Loop: `c11c_geometric_waves_v1 / harmonic_membrane` resolves the concrete grammar in the canonical producer registry and the `geometric` family-level payload definition. The definition does **not** prove that a grammar-specific generated instance exists.
- Visual Drill: `tracking / tier-2` resolves the drill type and requested tier. The canonical tracking example carries tier 2 and seed 12345, but a matching example definition is not a generated request-scoped instance.

V1 deliberately covers only these representative pairs because the current temporal/editorial references are pinned to them. Any other pair fails closed instead of borrowing a family-level timing fixture.

## Deliberately unresolved

`payload_instance_id`, payload-instance SHA-256 and output path remain null. This contract does not invoke the Godot generator, derive visual parameters, run simulation, choose frame samples, assign per-field editorial frame windows, approve regions, emit renderer-native input, dispatch a renderer or create media. It is an honest, machine-readable seam before the future request-specific payload materializer.

## Validation

Run `python -m py_compile .\tools\c11d\d9\d_renderer_request_scoped_payload_binding.py .\tools\c11d\d9\test_d_renderer_request_scoped_payload_binding.py` then `python .\tools\c11d\d9\test_d_renderer_request_scoped_payload_binding.py`. The test covers three representative canonical requests, exact chain parity, source binding, deterministic hashes, 51 negative cases and Draft 2020-12 schema validation when `jsonschema` is installed.

## Governance

C11-C 2.19.12 remains frozen and immutable. `PREPARE_ONLY`, renderer OFF, media_created=false, D4.8 BLOCKED, release authority NONE. This checkpoint is not baseline approval and does not authorize video production.
