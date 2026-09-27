# C11-C Suite 0.1.2

Operator interface layer for ChallengeEngineV01_STATELESS. The Suite consolidates tooling without moving or reimplementing engine truth.

## Launch

```powershell
cd .\c11c-suite
.\run.bat
```

## Test console entry points

```powershell
.\c11c-test\run_all.bat
.\c11c-test\run_suite.bat C11CProductionReviewCopySafetyTest.gd
```

## Members

- `c11c-test` — full logical regression, freeze gates, historical QA, art-direction operations, longforms and individual `*Test.gd` suites.
- `c11c-catalog` — recursive artifact browser with image/video preview and ffprobe metadata.
- `c11c-maintenance` — safe cleanup, repository/delivery validation, docs dry-run and project ZIP creation.
- `c11c-config` — low-level JSON/config/contracts view with JSON validation and backup-before-write.
- `c11c-producer` — existing C11-C Producer 0.9.1, relocated as a Suite member.

The former `c11c-producer/` remains as a compatibility launcher only. The historical requested spelling `c11c-maintenace/` is an alias to `c11c-maintenance/`.

## Test/script registration rule

`tests/run_all.py` + `KNOWN_SUITES` is the canonical logical test registry. `c11c-test` reads it dynamically, so a newly registered `*Test.gd` appears in the GUI without copying the suite list into another file.

Operational PS1 test/QA entry points are exposed by `c11c-test` through their canonical script paths. When a new PS1 becomes an official verification entry point, add its launcher to `C11_COMMANDS` in `c11c-test/main.py` rather than duplicating the underlying logic.

## Boundary

The Suite is forbidden from implementing mechanics, RNG, simulation truth, `SimulationResult`, `winning_frame`, `RenderedFrameStream`, C7 ownership, or renderer mathematics. It calls the canonical project scripts and reads declared repository data.

## Dependencies

Python + PySide6 are required for the GUI. FFmpeg/FFprobe are required for media preview and delivery inspection where applicable. Godot is required for test/production commands.
