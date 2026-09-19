# C11 Freeze — Repository Layout Contract

## Principles

The repository contains source, deterministic tests, QA evidence, generated production artifacts and historical evidence. These are different lifecycles and must not share a flat namespace.

### Canonical source

Keep at repository root:

- `GeneradorMaestro.gd`
- `Main.tscn`
- `project.godot`
- `build_factory.py`
- `core/`
- `mechanics/`
- `challenges/`
- `definitions/`
- `profiles/`
- `assets/`
- `tests/`
- `tools/`
- `docs/`

### Generated material

All new generated material goes below `artifacts/`.

No new test, QA or production script should create a root-level `output*`, `export*`, `qa*`, `*_generated_configs` or `*/production` directory.

### Historical material

Existing legacy output remains evidence until migration is validated. It is indexed below `artifacts/legacy/` rather than mixed into active production.

## Canonical meanings

| Area | Meaning |
|---|---|
| `artifacts/production` | Current production exports and authoritative manifests |
| `artifacts/qa` | Qualification runs, contacts sheets, keyframes, seed-matrix videos |
| `artifacts/regression` | Machine-readable compatibility baselines and comparison reports |
| `artifacts/tests` | Test logs and aggregate reports |
| `artifacts/scratch` | Disposable local working material |
| `artifacts/legacy` | Historical evidence migrated from old roots |

## No destructive cleanup during consolidation

The first migration pass must be copy/index only. Delete historical source folders only after a freeze manifest records every migrated path and all required regression evidence is green.
