# Visual Loop Geometric Grammar Matrix V2 — Seed Runtime Fix Overlay

This guarded overlay repairs the JSON numeric seed-array validation that fails in the Godot 4.7.1 runtime. The grammar field-level comparison added by the preceding runtime fix is preserved.

## Scope and non-goals

- Accept exactly four seed values, numerically equal and ordered as `1`, `12345`, `54321`, `2147483646`.
- Accept Godot JSON decoding of integral JSON numbers as either integer or float, only when finite and numerically equal to the exact pinned value.
- Reject strings, booleans, non-finite values, fractional/altered values, missing values and extra values.
- Keep the audit PREPARATION_ONLY. It does not admit a canonical request or payload, enable the renderer, create media or change any governance gate.

## Replacement preconditions

- Previous probe SHA-256: `7b4c35b9c87fdfdd41e89971077d3376a5a8df451f91f59083f85e3901a495c7`
- Previous test SHA-256: `5f6eab104135d873f7e4242bbb415ff28309127f430f0061d51e840df955f625`
- Previous contract SHA-256: `e787b45843ff5c1642e9e1374d59869ef11fdc70620cfdda81606652aef5d17a`
- Frozen C11-C manifest SHA-256 must remain `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

## New file hashes

- `tools/c11d/d9/probe_visual_loop_geometric_grammar_matrix_v2.gd` — `91bc179b9a6db2a8bbcde54e08f05b91d6dd47abc7d12c5904742df4cb5a70e7`
- `tools/c11d/d9/test_d_renderer_visual_loop_geometric_grammar_matrix_v2.py` — `331834916e72e5dac71d9f74ea79c8a758f399da4a719a985da0515b74cd5471`
- `definitions/c11d/production/D_RENDERER_VISUAL_LOOP_GEOMETRIC_GRAMMAR_MATRIX_V2.json` — `e2118dd2e25005913bfe418a001e24c20d0929a395171a172a6ac9c88e1d13a2`

After applying, run the focused Python tests and then the real Godot 4.7.1 runtime audit independently. Python contract tests alone are not a runtime PASS.
