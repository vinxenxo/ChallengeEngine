# C11-C Producer 0.9.7 — Master Handover (2.19.5)

## Authority

The live Producer is `c11c-suite/c11c-producer/`. The repository is C11-C 2.19.5 final repair candidate until the C11-C freeze seal passes.

## Scope

Producer remains an orchestration/UI layer. It does not implement mechanics, gameplay RNG, `SimulationResult`, `winning_frame` or renderer truth.

## Capture route

- temporary AVI Movie Maker capture;
- project-local `--path .`;
- proven Producer Drill route does not pass a divergent explicit `--resolution` CLI argument;
- wait for stable AVI;
- convert from video-only AVI source through FFmpeg;
- canonical audio is generated/muxed by the existing audiovisual layer;
- AVI is scratch/intermediate only.

## Review relationship

Art Direction review uses `tools/prototypes/c11c_bulk/run_c11c_art_direction_batch_v4.ps1`. Its `Workers=7` contract is genuine concurrency through per-worker temporary Godot project roots. The Movie Maker helper is lock-free; do not reintroduce the superseded global mutex.

## Suite ownership

All active Producer launchers are under `c11c-suite/c11c-producer/`. Retired `c11c-studio/` is not a dependency and must not be updated.

## Validation

Run:

```powershell
python .\c11c-suite\self_test.py
python .\c11c-suite\c11c-producer\self_test.py
python .\c11c-suite\c11c-producer\test_producer_gui_contract.py
```

Then validate the C11-C acceptance gate before freeze.
