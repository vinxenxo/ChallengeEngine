# C11-D Visual Loop Request-Scoped Grammar Parameter Binding V2 — Additive Overlay

## Intent

Add one request-bound, in-memory 20-field grammar parameter instance for each of the five fixed `c11c_geometric_waves_v1` selectors. Each instance is bound to canonical request/plan/bridge/adapter/source hashes and the matching selector-level timing/review reference digest.

This is **not** a complete selector Visual Loop payload. It does not execute a shader, instantiate or dispatch a renderer, generate media, consume policy bodies, or grant approvals.

## Contents

- `definitions/c11d/production/D_RENDERER_VISUAL_LOOP_REQUEST_SCOPED_GRAMMAR_PARAMETER_BINDING_V2.json`
- Three strict JSON Schemas for the contract, probe input and stdout report.
- `tools/c11d/d9/d_renderer_visual_loop_request_scoped_grammar_parameter_binding_v2.py`
- `tools/c11d/d9/materialize_visual_loop_grammar_parameter_matrix_v2_in_memory.gd`
- `tools/c11d/d9/test_d_renderer_visual_loop_request_scoped_grammar_parameter_binding_v2.py`
- `docs/current/d/D_RENDERER_VISUAL_LOOP_REQUEST_SCOPED_GRAMMAR_PARAMETER_BINDING_V2_CHECKPOINT_20261016.md`
- This README and the root overlay manifest.

All repository destinations must be absent before applying. The operation is ADD_ONLY and stops if any source pin or file hash differs. No frozen C11-C file is added to the copy list or modified.

## Local checks

```powershell
python -B tools/c11d/d9/test_d_renderer_visual_loop_request_scoped_grammar_parameter_binding_v2.py
python -B tools/c11d/d9/d_renderer_visual_loop_request_scoped_grammar_parameter_binding_v2.py --root . --godot "$env:C11D_GODOT_EXECUTABLE" --timeout 120
```

The first command uses mocked subprocess receipts. It checks contracts but is not a substitute for the second command with real Godot 4.7.1. The runtime runner verifies `--version`, executes five headless in-memory probes, validates every receipt, rebuilds the parent request/reference matrix, and prints its hash-sealed report to stdout only.

## Mandatory status after PASS

- `selected_grammar_parameter_instances_bound=5/5`
- `selected_grammar_payload_instances_bound=0/5`
- `exact_selector_visual_payload_materialized=false`
- `approval_assertions_checked=19`, `approvals_granted=0`
- `candidate_input_admissible=false`
- `renderer=OFF`, `media_created=false`, `D4.8=BLOCKED`, `release_authority=NONE`
- `D9.10=PREPARE_ONLY`, `D9.17=BLOCKED_NO_GO`, `D10=BLOCKED`

Never promote parameter-instance evidence to a full payload, canonical admission, renderer readiness or production authorization.
