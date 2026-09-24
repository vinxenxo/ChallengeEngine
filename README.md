# C11-C Studio

Windows desktop control surface for `ChallengeEngineV01_STATELESS` and the C11-C toolchain.

## Scope

C11-C Studio is a frontend/orchestrator. It does not reimplement rendering math, RNG, simulation, C7 audio contracts, C9 authoring contracts or frozen C11-B logic.

Current backend baseline: C11-C v2.1.4 (discovered dynamically when possible).
Current Visual Loop social delivery baseline: 720x1280, 30 FPS, 18.00 s, 540 frames.
Logical C11-B canvas remains 540x960.

## First run

```text
run.bat
```

or:

```text
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py --project "C:\Path\To\ChallengeEngineV01_STATELESS"
```

## CLI

```text
python main.py --project <path>
python main.py --validate
python main.py --review-5x5
python main.py --production-25
```

## Canonical workflows

Review 5x5 uses the canonical `run_c11c_art_direction_review.ps1` when available.
Production single uses `run_c11c_production.ps1`.
Production 5x5 prefers `run_c11c_production_25.ps1` because it is the current dedicated final-product batch tool; if absent, the GUI can expose the family-bulk operation instead of inventing an incompatible fallback.

Generation never performs cleanup.
Production is protected from review cleanup.
Every job retains the exact command and raw log.
