# C11-C Producer 0.9.1 — Comandos de pruebas en consola

## Objetivo

Guía operativa para validar desde Windows PowerShell el Producer, las suites lógicas del proyecto, los contratos C11-C, la cualificación histórica C11-A y el gate completo de freeze. El backend C11-C 2.16.9 permanece congelado.

## 1. Raíz del proyecto

```powershell
cd C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS
```

## 2. Batería lógica completa

El runner contractual `tests/run_all.py` descubre las 133 suites `*Test.gd` registradas y ejecuta cada una con Godot. Por defecto excluye las suites de exportación física.

```powershell
python .\tests\run_all.py
```

Para incluir también las suites físicas, después de haber generado previamente sus artefactos: 

```powershell
python .\tests\run_all.py --include-physical
```

Runner PowerShell equivalente, con log en `artifacts/tests/logs`: 

```powershell
.\tools\c11freeze\run_test_suite.ps1
```

## 3. Gate completo C11 Freeze

El gate encadenado ejecuta core, contratos C11, las 133 suites lógicas, retrocompatibilidad, exportación física y stress determinista.

```powershell
.\tools\c11freeze\run_all.ps1
```

Opciones útiles para una pasada más rápida durante diagnóstico:

```powershell
.\tools\c11freeze\run_all.ps1 -SkipPhysical -SeedLimit 2 -SeedRepeat 2 -StressRetries 1
```

La pasada de release debe hacerse con los valores por defecto, sin `-SkipPhysical` y sin limitar seeds.

## 4. Suites que componen el gate de freeze

Core mecánico/RNG/isolation:

```powershell
.\tools\c11freeze\run_core_suite.ps1
```

Contratos C11-B:

```powershell
.\tools\c11freeze\run_c11_suite.ps1
```

Retrocompatibilidad:

```powershell
.\tools\c11freeze\run_retrocompatibility.ps1
```

Exportación física C10/C6F0-6:

```powershell
.\tools\c11freeze\run_physical_export_suite.ps1
```

Stress determinista de seeds, por defecto 2 repeticiones y hasta 3 reintentos ante fallos de proceso/runtime:

```powershell
python .\tools\c11freeze\run_seed_stress.py --repeat 2 --retries 3
```

## 5. QA histórico C11-A.1 de Challenges

Cualificación histórica 9 Challenges × 6 seeds = 54 runs:

```powershell
.\tools\qa\c11\run_c11a1_challenge_bulk_qa.ps1
```

QA visual histórico C11-A:

```powershell
.\tools\qa\c11\run_c11a_visual_bulk_qa.ps1
```

Los dos comandos anteriores son QA histórica y no sustituyen las suites contractuales actuales.

## 6. Autotests específicos del Producer 0.9.1

```powershell
cd .\c11c-producer
python .\self_test.py
python .\preflight.py
python -m py_compile .\main.py .\preflight.py .\self_test.py
```

Criterio esperado:

```text
C11-C Producer 0.9.1 self-test PASS
C11-C Producer seed_probe preflight PASS
```

## 7. Lanzar el GUI

```powershell
.\run.bat
```

El arranque debe completarse sin traceback Python. El hotfix 0.9.1 corrige específicamente el `NameError` producido por la ausencia de `QFrame` en los imports de `main.py`.

## 8. Producción manual de Challenge

Desde la raíz del proyecto:

```powershell
cd ..
.\tools\prototypes\c11c_bulk\run_c11c_challenge_production.ps1 `
  -ChallengeId CHALLENGE_001 `
  -Seed 12345 `
  -DeliveryProfile REVIEW_720
```

MASTER 1080:

```powershell
.\tools\prototypes\c11c_bulk\run_c11c_challenge_production.ps1 `
  -ChallengeId CHALLENGE_004 `
  -Seed 12345 `
  -DeliveryProfile MASTER_1080
```

Sobrescritura explícita:

```powershell
.\tools\prototypes\c11c_bulk\run_c11c_challenge_production.ps1 `
  -ChallengeId CHALLENGE_004 `
  -Seed 12345 `
  -DeliveryProfile MASTER_1080 `
  -Force
```

## 9. Producción manual de Visual Loop

Ejemplo de la ruta que reproducía el error histórico de `.fps`:

```powershell
.\tools\prototypes\c11c_bulk\run_c11c_production.ps1 `
  -Family c11c_fractal_bloom_v1 `
  -Seed 12345 `
  -DeliveryProfile MIN_540
```

MASTER 1080:

```powershell
.\tools\prototypes\c11c_bulk\run_c11c_production.ps1 `
  -Family c11c_living_particles_v1 `
  -Seed 54321 `
  -DeliveryProfile MASTER_1080
```

## 10. Producción manual de Visual Drill

Tracking en MASTER 1080:

```powershell
cd .\c11c-producer
.\run_visual_drill_production.ps1 `
  -Family tracking `
  -Seed 12345 `
  -DeliveryProfile MASTER_1080
```

Contrato actual de Tracking: 3 s pre-roll + 21 s gameplay + 3 s END CTA = 27 s = 810 frames a 30 FPS.

## 11. Secuencia mínima tras cada overlay

```powershell
cd C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS\c11c-producer
python .\self_test.py
python .\preflight.py
.\run.bat
```

## 12. Secuencia recomendada de release

```powershell
cd C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS
python .\tests\run_all.py
.\tools\qa\c11\run_c11a1_challenge_bulk_qa.ps1
.\tools\qa\c11\run_c11a_visual_bulk_qa.ps1
.\tools\c11freeze\run_all.ps1
cd .\c11c-producer
python .\self_test.py
python .\preflight.py
python -m py_compile .\main.py .\preflight.py .\self_test.py
.\run.bat
```

## 13. Criterios mínimos de aceptación del hotfix 0.9.1

- `self_test.py` termina con `C11-C Producer 0.9.1 self-test PASS`.
- `preflight.py` termina con `C11-C Producer seed_probe preflight PASS`.
- `run.bat` abre el GUI sin traceback.
- La cola conserva las filas completadas y las muestra atenuadas.
- La fila activa queda realmente resaltada.
- La variación usa deslizadores + checkbox `ALEATORIO`.
- Visual Loop con `MIN_540` no lanza `PropertyNotFoundStrict` por `.fps`.
- Visual Drill Tracking mantiene 27 s / 810 frames.
- El gate global no presenta regresiones en C11-B, RNG ni mecánicas.

## Límites

Estas pruebas no autorizan a modificar C11-B, RNG, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7 ni la geometría social lógica 540×960.
