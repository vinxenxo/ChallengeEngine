# MASTER HANDOVER — C11-C SUITE 0.1.2

## Current state

C11-C Suite remains an operational interface layer above the frozen deterministic audiovisual backend.

### 0.1.2 hotfixes

- `c11c-test` starts correctly; `C11_COMMANDS` entries are handled as four-field records.
- `c11c-test/run_all.bat` launches the canonical logical runner from the repository root.
- `c11c-test/run_suite.bat` launches one registered Godot suite from the repository root.
- New logical `*Test.gd` entries remain driven by `tests/run_all.py` / `KNOWN_SUITES`.
- Longform segment resolution now uses the current canonical `REVIEW_720` production product, `production_manifest.json`, and prototype music output.
- Longform no longer assumes a copied `${stem}_manifest.json` exists in the production product.

## Frozen boundary

No simulation, mechanic, RNG, `SimulationResult`, `winning_frame`, `RenderedFrameStream`, renderer mathematics, or audiovisual ownership logic is changed by this phase.

## Acceptance

Run:

```powershell
.\c11c-suite\self_test.py
.\c11c-suite\c11c-test\run_all.bat
.\c11c-suite\c11c-test\run_suite.bat C11CVisualLoopLongformSourceArtifactContractTest.gd
```

Then exercise `C11-C SUITE` → `TEST` and the `ART DIRECTION LONGFORMS` command.
