# C11-C Config 0.2.0 — C11-D governed configuration

D9.7 extends the existing `c11c-config` application; it creates no new suite.

## New surfaces

- **C11-D Contracts:** read-only D2–D9 contract browser with JSON status, SHA-256, category and authority label. `VALIDAR TODOS LOS CONTRATOS D` checks parsing and core governance invariants.
- **C11-D Operator Profiles:** user-owned JSON presets under `profiles/c11d/operator/` with validation, SHA-256, diff, explicit save, `.bak` and validated restore.
- **Repository Config** remains available for inspection and ordinary non-protected configuration files.

## Write boundaries

The generic Repository Config editor is read-only for `challenges/`, `definitions/`, `schemas/`, `assets/`, `core/`, `tools/`, `tests/`, all of `c11c-suite/`, and all profile paths. This prevents using a generic editor to bypass suite contracts or frozen C11-C boundaries. The dedicated Operator Profiles tab is the only write surface for validated files under `profiles/c11d/operator/`; those writes include explicit confirmation, `.bak`, schema/registry validation and validated restore. Canonical D definitions are read-only.

Profiles require explicit gameplay `seed` and independent `music_seed`, explicit mode/profile IDs, and an audio boolean. Blank profiles deliberately contain no seed or profile defaults. Unknown keys, invalid profile IDs and path traversal are rejected.

## Authority boundary

Saved operator profiles do not yet auto-feed Producer or execute a renderer; their cross-suite use is a later D9 lifecycle gate. `runtime_authority=NONE`, `renderer_activation=false`, `production_execution=false`, `release_authority=NONE`. D4.8 remains BLOCKED.

## Tests

```powershell
python .\c11c-suite\c11c-config\self_test.py
python .\c11c-suite\c11c-config\test_config_gui_contract.py
python .\c11c-suite\self_test.py
```

Qt GUI and filesystem interactions must still be exercised on the Windows workstation before D9.7 is accepted.
