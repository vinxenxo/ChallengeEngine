# C11-C Studio v0.4.0

Windows desktop control surface for `ChallengeEngineV01_STATELESS` and the canonical C11-C toolchain.

## UX
The application is split into two operational areas:

- **PRODUCCIÓN**: Generar, Resultados, Jobs, Logs, Reproducir.
- **CONFIGURACIÓN**: Dirección de arte, Familias, Seeds, Artifacts, Validación, Ajustes, Juegos/Drills, Diagnóstico.

The default screen is **Generar**, designed as the daily control panel for video, Review 5x5 and final production.

## Command integrity
C11-C Studio is an orchestrator. It does not reimplement render mathematics or change C11-B/C contracts. PowerShell is launched from the project root, matching the documented canonical invocation. Review 5x5 uses `run_c11c_art_direction_review.ps1`; production 5x5 is a sequential GUI queue over the documented `run_c11c_production_bulk.ps1` launcher for the five canonical families.

## First run
```powershell
.\run.bat --project "C:\Path\To\ChallengeEngineV01_STATELESS"
```

## CLI
```text
python main.py --project <path>
python main.py --validate
python main.py --review-5x5
python main.py --production-25
```
