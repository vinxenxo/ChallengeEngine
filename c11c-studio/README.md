# C11-C Studio (v0.1.0)

Desktop orchestrator for the C11-C Visual Loops toolchain
(ChallengeEngineV01_STATELESS). Frontend only - never reimplements render
math, RNG, or frozen C11-B contracts.

## Quick start (Windows)

    run.bat

First launch creates .venv, installs PySide6, starts the app.

## Manual launch

    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    python main.py --project "D:\Path\To\ChallengeEngineV01_STATELESS"

## CLI

    python main.py --project <path>
    python main.py --validate
    python main.py --review-5x5
    python main.py --production-25

## What works

- Project discovery + environment validation (Godot/Python/FFmpeg/FFprobe/PowerShell)
- Dashboard with live status cards and recent jobs
- Family registry (5 canonical + dynamic discovery)
- Review Lab: select individual families, per-family details, live log
- Production: single + 5x5, random seed generator, grammar selector (gated)
- Families page: REVIEW preselects and jumps; OPEN FOLDER opens explorer
- Artifacts browser with protected/regenerable classification
- Log Center (live + raw + parsed)
- Validation Center
- Settings (persisted to %APPDATA%\C11CStudio\config.json)
- JobManager: async subprocess, stdout/stderr capture, cancel

## Contract compliance

- Delivery: 720x1280 / 30 FPS / 18 s baseline shown as defaults, not laws.
- Logical canvas 540x960 always displayed separately.
- One canonical MP4 per product enforced at validation level.
- Production never deleted by review cleanup.
- No hard-coded absolute paths.
- PowerShell arrays (-Seeds, -Families) passed as separate args (never
  comma-joined) because -File mode does not evaluate the comma operator.

## Canonical tool paths expected in the repo

    tools\prototypes\c11c_bulk\validate_c11c_powershell.ps1
    tools\prototypes\c11c_bulk\validate_c11c_delivery_configuration.ps1
    tools\prototypes\c11c_bulk\run_c11c_art_direction_review.ps1
    tools\prototypes\c11c_bulk\run_c11c_production.ps1
    tools\prototypes\c11c_bulk\run_c11c_production_bulk.ps1
    tools\prototypes\c11c_<family>\run_prototype.ps1

If a tool is missing, the job returns non-zero and the Log Center shows
the real cause - the raw log is never hidden.
