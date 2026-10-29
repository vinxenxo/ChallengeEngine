# C11-D Request-Scoped Editorial Value Carrier Overlay V1

This additive overlay contains only new D-owned contract/schema/tool/test/checkpoint files. Apply at the existing repository root; no source file is overwritten by this overlay.

## Scope

- Hash-bound, in-memory sidecar of canonical D9.9 editorial values for the three established review fixtures.
- Optional JSON overrides limited to enabled editorial string fields, re-resolved through the current D9.9 canonical request chain.
- No edits to C11-C, existing payload harnesses, simulation truth, temporal anchors or visual payload bytes.
- No renderer-native input, renderer dispatch, media creation, persisted receipt, release authority or gate change.

## Verify

```powershell
python -B .\tools\c11d\d9\test_d_renderer_request_scoped_editorial_value_carrier.py
python -B .\tools\c11d\d9\d_renderer_request_scoped_editorial_value_carrier.py --godot "C:\PATH\TO\Godot_v4.7.1-stable_win64_console.exe"
```

The focused Python test uses mocked materializer summaries. The console runner command is the real Godot 4.7.1 gate. For detailed semantics and optional input schema see `docs/current/d/D_RENDERER_REQUEST_SCOPED_EDITORIAL_VALUE_CARRIER_CHECKPOINT_V1.md`.
