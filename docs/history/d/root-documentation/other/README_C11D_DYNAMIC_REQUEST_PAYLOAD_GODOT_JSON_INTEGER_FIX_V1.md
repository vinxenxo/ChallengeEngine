# C11-D Dynamic Request Payload — Godot JSON Integer Validation Repair V1

## Finding
The first real Windows Godot 4.7.1 run stopped before materialization because the harness checked JSON numbers with a strict `TYPE_INT` comparison. The canonical Python request and schema had already passed. Godot may represent JSON integer literals as `TYPE_FLOAT`, so the GDScript boundary rejected valid canonical values for `seed`, `music_seed`, and `variation_index`.

## Fix
The harness now accepts only numeric Variants of type `TYPE_INT` or `TYPE_FLOAT` that are finite, within the canonical field bounds, and mathematically integral. Booleans, fractional values, out-of-range values and non-finite values fail closed. The contract's explicit harness SHA-256 was refreshed. A Python contract test checks that this validation stays present.

## Modified files
- `tools/c11d/d9/materialize_dynamic_request_payload_in_memory.gd`
- `definitions/c11d/production/D_RENDERER_DYNAMIC_REQUEST_PAYLOAD_BINDING_V1.json`
- `tools/c11d/d9/test_d_renderer_dynamic_request_payload_binding.py`
- `docs/current/d/D_RENDERER_DYNAMIC_REQUEST_PAYLOAD_BINDING_CHECKPOINT_V1.md`

## Apply and test
See the separate `APPLY_C11D_DYNAMIC_REQUEST_PAYLOAD_GODOT_JSON_INTEGER_FIX_V1.ps1` and `TEST_C11D_DYNAMIC_REQUEST_PAYLOAD_GODOT_JSON_INTEGER_FIX_V1.ps1` helper scripts. The apply script checks the exact pre-fix hashes before replacing these four known files. The test script runs the focused Python contract test, the real ten-request Godot matrix, and targeted regressions one by one.

## Limits
This repair does not admit new selectors or approve any policy. `renderer=OFF`; `media_created=false`; `D4.8=BLOCKED`; `release_authority=NONE`; D9.14/D9.16 remain blocked; D9.17 remains NO-GO; D10 remains blocked.
