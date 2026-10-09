# C11-C Config 0.2.0 — C11-D governed configuration

D9.7 introduced the governed Config surface, and D9.10 extends its read-only contract registry; it creates no new suite.

## New surfaces

- **C11-D Contracts:** read-only D2–D9 contract browser with JSON status, SHA-256, category and authority label. At the initial D9.10 bridge checkpoint the registry contained 22 canonical JSON contracts. The current registry has grown to 30 read-only contracts, including the bridge and D-only adapter boundary; `VALIDAR TODOS LOS CONTRATOS D` checks parsing and core governance invariants.
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

Qt GUI and filesystem interactions must still be exercised on the Windows workstation before Config GUI acceptance is closed. D9.10 bridge-contract registration and static validation pass, but do not substitute for Windows Config GUI acceptance.


### D9.10 D-only render adapter boundary

The canonical contract `definitions/c11d/production/C11D_RENDER_ADAPTER_BOUNDARY_D9_10_V1.json` is registered read-only. It permits deterministic preparation of an inspectable adapter envelope only. Renderer dispatch, renderer-native input, production execution, media creation, D4.8 and release authority remain blocked. This registry entry is governance metadata; it does not grant execution permission.

## D9.10 D-only adapter boundary (2026-10-09)

Config registers `definitions/c11d/production/C11D_RENDER_ADAPTER_BOUNDARY_D9_10_V1.json` as `D9_D_ONLY_RENDER_ADAPTER_BOUNDARY`, read-only. Registry validation is 30/30. The contract allows envelope preparation but forbids renderer dispatch, renderer-native input, production/media side effects, C11-C mutation, D4.8 override and release-authority escalation. Automated tests and reports do not require screenshots; their JSON identifies `operator_gui_runtime_observed=false` when the window itself was not interactively observed.

