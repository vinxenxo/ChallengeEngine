# C11-C Suite 0.1.4 — Operator Shell

C11-C Suite is the active GUI/CLI operator shell for the canonical ChallengeEngineV01_STATELESS toolchain. GUI actions and direct console commands must use the same backend launchers.

Freeze packaging is handled by `tools/maintenance/create_c11c_freeze_zip.ps1`.

# C11-C Suite — 0.1.4 — C11-C 2.19.6 consolidated repair candidate

Canonical active operator surface for the C11-C manufacturing branch. `c11c-studio` is retired and is not an operational dependency. All active suite changes belong under `c11c-suite/`.

## Surfaces

- `c11c-test` — logical regression, QA runners and operational contract checks.
- `c11c-catalog` — artifact browsing and metadata inspection.
- `c11c-maintenance` — maintenance and archive operations.
- `c11c-config` — declarative configuration inspection/editing.
- `c11c-producer` — audiovisual orchestration.

## 2.19.6 worker-isolation rule

The C11-C Art Direction batch runner keeps `Workers=7` as a real concurrent execution contract. Each worker receives an independent temporary Godot project root; `override.cfg` and `.godot` are worker-local. The review runner does **not** serialize captures behind a project-global mutex.

Static suite self-test additionally verifies that operational `.py/.ps1/.bat/.cmd` launchers do not reference `c11c-studio`.

All GUIs remain consumers/orchestrators. They do not implement mechanics, RNG or simulation truth.
