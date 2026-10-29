# C11-D Dynamic Request → Payload Binding Overlay V1

## Purpose

This additive, preparation-only overlay binds canonical D9.9 request identity and gameplay seed to deterministic in-memory visual-state evidence for three explicitly pinned representative selectors. It is a bounded contract/probe, not renderer activation or approval of a renderer baseline.

## Files

- `definitions/c11d/production/D_RENDERER_DYNAMIC_REQUEST_PAYLOAD_BINDING_V1.json` — D-owned contract, fixed selector matrix, source pins and governance locks.
- `definitions/c11d/production/D_RENDERER_DYNAMIC_REQUEST_PAYLOAD_INPUT_SCHEMA_V1.json` — strict input envelope schema (JSON Schema Draft 2020-12).
- `definitions/c11d/production/D_RENDERER_DYNAMIC_REQUEST_PAYLOAD_BINDING_SCHEMA_V1.json` — strict stdout receipt schema (JSON Schema Draft 2020-12).
- `tools/c11d/d9/materialize_dynamic_request_payload_in_memory.gd` — Godot headless harness, two deterministic in-memory passes per request; stdout only.
- `tools/c11d/d9/d_renderer_dynamic_request_payload_binding.py` — canonical D9.9/D9.10/source binding, invokes Godot per request, validates summary and emits hash-bound receipts to stdout.
- `tools/c11d/d9/test_d_renderer_dynamic_request_payload_binding.py` — Python contract tests; subprocess is deliberately mocked here, so this test is not runtime proof of the new GDScript harness.
- `docs/current/d/D_RENDERER_DYNAMIC_REQUEST_PAYLOAD_BINDING_CHECKPOINT_V1.md` — scope, limits and next gate.

## Acceptance matrix

Default runner evaluates ten requests in a fixed 3-selector matrix:

- Challenge: `challenges / parking_v2 / CHALLENGE_004`.
- Visual Loop: `visual_loops / c11c_geometric_waves_v1 / harmonic_membrane`.
- Visual Drill: `visual_drills / tracking / tier-2`.

For each content type, it compares a base request with one changing only gameplay seed. For Visual Loop it additionally varies only `music_seed`, `variation_index`, delivery-profile identity, or editorial title. Actual `visual_state_sha256` evidence must change on gameplay-seed changes and stay unchanged for those orthogonal metadata-only changes. Request/payload hashes must remain bound and deterministic.

The Visual Loop case intentionally reports `exact_selector_payload_materialized=false`: the authoring envelope still says subtype `geometric`; the `harmonic_membrane` grammar instance is not proven consumed. Do not reclassify this as exact grammar materialization.

## Apply and run

1. Verify the downloaded ZIP SHA-256 shown in the hand-off message.
2. Extract the ZIP into the repository root, after ensuring none of its eight paths already exists. Do not overwrite differing files.
3. Run the new Python contract test:

   `python -B .\tools\c11d\d9\test_d_renderer_dynamic_request_payload_binding.py`

4. Verify the configured Godot executable and run its actual harness matrix:

   `& $env:C11D_GODOT_EXECUTABLE --version`

   `python -B .\tools\c11d\d9\d_renderer_dynamic_request_payload_binding.py --godot $env:C11D_GODOT_EXECUTABLE --timeout 120`

5. Continue with the targeted regressions listed in the checkpoint.

A passing Python test alone is insufficient. The runner must pass against the real Godot 4.7.1 console executable on Windows.

## Invariants

- Frozen C11-C manifest SHA-256 remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- Longform, unknown selectors/variants, unapproved presentation profiles and Longform delivery profile are rejected.
- `music_seed` is excluded from visual payload state; `variation_index` is metadata-only; delivery profile is identity only and no resampling/projection occurs.
- Editorial text remains in the canonical request/editorial lineage and is not injected into visual payload (`visual_payload_consumed=0/14` remains authoritative).
- No request, payload or receipt is persisted by these new tools; the Godot input crosses as one base64 command-line argument. No renderer input, renderer dispatch or media output is created.
- `renderer=OFF`, `media_created=false`, `D4.8=BLOCKED`, `release_authority=NONE`; D9.14/D9.16 remain blocked, D9.17 remains NO-GO, D10 remains blocked. Candidate input remains inadmissible and freeze eligibility is not conferred.
