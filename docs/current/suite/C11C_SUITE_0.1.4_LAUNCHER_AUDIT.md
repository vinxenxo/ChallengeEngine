# C11-C Suite 0.1.4 — Launcher Audit / 2.19.6 Final Repair

Date: 2026-09-28

## Canonical ownership

All active Suite launcher surfaces are under `c11c-suite/`. `c11c-studio/` is retired and is not an operational dependency.

## Audited launchers

- `c11c-suite/c11c-catalog/run.bat`
- `c11c-suite/c11c-config/run.bat`
- `c11c-suite/c11c-maintenace/run.bat`
- `c11c-suite/c11c-maintenance/run.bat`
- `c11c-suite/c11c-producer/run.bat`
- `c11c-suite/c11c-producer/test_gui_contract.bat`
- `c11c-suite/c11c-test/run.bat`
- `c11c-suite/c11c-test/run_all.bat`
- `c11c-suite/c11c-test/run_suite.bat`
- `c11c-suite/run.bat`
- `c11c-suite/test_retro_reference_contract.bat`

- `c11c-suite/c11c-producer/run_visual_drill_production.ps1` is the active Producer Drill production launcher and is also normalized to UTF-8 without BOM.

## Result

- Repository root is resolved through `C11C_PROJECT_ROOT` on the canonical BAT launchers.
- Exit codes are propagated.
- `c11c-maintenace/run.bat` is a compatibility delegate to `c11c-maintenance/run.bat`.
- No active BAT/CMD/PS1 under `c11c-suite/` references `c11c-studio`.
- BAT/CMD files included in the final-repair overlay are UTF-8 without BOM.

No command semantics were intentionally changed by this audit.
