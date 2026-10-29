# C11-D MASTER HANDOVER — D9.10 Qt GUI Runtime Acceptance

**Estado documental:** 2026-10-09, después de la primera ejecución Windows del harness Qt offscreen. Este documento sustituye como instrucción operativa a los handovers D9.10 anteriores; los documentos históricos se conservan.

## 1. Snapshot de partida y autoridad

El operador ha congelado y subido a Library el repositorio de partida:

- Archivo: `ChallengeEngineV01_STATELESS_C11-D D9.10_20261009_220331.zip`
- SHA-256 del ZIP verificado al recuperar el archivo de Library: `fa3c4e2299ecf7ecffa81925689313c1a79b47e437edbfc539f16e10973379b2`
- Manifest C11-C protegido: `release/C11C_FREEZE_PACKAGE_MANIFEST.json`
- SHA-256 inmutable esperado del manifest C11-C: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`
- Ruta local habitual: `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`

**Trata ese ZIP como el punto de partida que el usuario identificó para esta ventana.** No reconstruyas la rama a partir de un ZIP antiguo D9.7/D9.4 ni vuelvas a aplicar overlays que ya estén dentro de este snapshot sin comprobar primero el inventario y los hashes. Los cambios de este handover son documentales; no alteran el código fuente del snapshot.

## 2. Estado resumido

- **C11-C 2.19.12:** referencia inmutable; no alterar simulación, mecánicas, RNG, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, geometría 540×960, contratos C7/C9 ni comportamiento de producción congelado.
- **D9.10 bridge y D-only adapter:** implementados en modo `PREPARE_ONLY`. Camino: GUI/CLI → request D9.9 canónica → editorial resolution → plan → bridge record → envelope D-only con hashes. No emite renderer-native input ni despacha ejecución.
- **D9.10 backend/static:** el operador obtuvo `test_editorial_render_bridge.py` PASS (content types 3/3; bridge CLI parity 3/3; adapter parity 3/3; negatives 15/15 y 9/9), Producer self-test y GUI contract PASS, Config self-test 30/30 y GUI contract PASS, Test integration contract PASS.
- **Qt runtime static contract:** `test_d910_gui_runtime_contract.py` PASS; `screenshots=NOT_REQUIRED`, `production=FORBIDDEN`. Está registrado como paso 22 de la suite.
- **Aggregate Suite:** `python -u .\c11c-suite\self_test.py` terminó `PASS` en 22/22. Esta suite ejecuta el contrato estático de Qt; no convierte el runtime offscreen opcional en PASS.
- **Qt runtime real (offscreen):** NO PASS todavía. `test_d910_gui_runtime_acceptance.py --run-id D910_QT_GUI_RUNTIME_01` devolvió `FAIL | content_types=0/3`. La salida mostró avisos Qt sobre fonts y `propagateSizeHints()`, pero esos avisos **no son causa raíz confirmada**. Leer `exception.txt` y el JSON del run para obtener la excepción real.
- **Aceptación automatizada enlazada:** `capture_d910_acceptance.py --run-id D910_QT_ACCEPTANCE_01 --include-qt-gui-runtime --include-aggregate` devolvió `FAIL | checks=6/7 | qt_gui_runtime=FAIL`. El resultado es coherente: cinco checks enfocados y el agregado pasaron; el check runtime falló. No etiquetar el run completo como PASS.
- **Candidate preflight:** último resultado Windows enviado después de restaurar los README históricos y antes de la ejecución Qt: `PASS`, 854/854 protected entries, 22/22 negatives, cinco bloqueos, `freeze_eligible=false`. Repetirlo en la siguiente sesión para confirmar el estado de este snapshot.
- **D9.14 bounded production qualification:** run Windows `D914_COLON_FIX_20261009_E` PASS; cuatro MP4 audiovisuales finales y ocho controles. Report SHA-256 `daa5e5676224d606e9d67ac7a7ed7e88c3c02a63c76ecdc579c3bc2dd320853f`. Qualification baseline SHA-256 `15343119f0f8338b13b47b0ea98546e5470d4a1a8895b65dbe1f41ee183e66d3`. Es evidencia real de cualificación acotada, no cierre de D9.14 GUI/E2E.
- **D9.15:** el operador autorizó omitir las 13 capturas para evaluación del candidato. La exención es sólo `WAIVED_NOT_EVIDENCED_FOR_CANDIDATE_ONLY`; no equivale a D9.15 PASS/CLOSED.

## 3. Diagnóstico pendiente inmediato

El primer objetivo en la ventana nueva es **diagnosticar el fallo Qt con la excepción completa**, no volver a implementar el adapter ni relajar los checks. La prueba devolvió cero tipos aceptados porque abortó antes de poder añadir un resultado PASS; hay que conocer el error exacto antes de editar código.

```powershell
$QtRoots = @(
  '.\artifacts\tests\c11d_d9\d910_gui_runtime_acceptance\D910_QT_GUI_RUNTIME_01',
  '.\artifacts\tests\c11d_d9\d910_gui_runtime_acceptance\D910_QT_ACCEPTANCE_01'
)
foreach ($QtRoot in $QtRoots) {
  if (Test-Path $QtRoot) {
    Write-Host "`n===== $QtRoot ====="
    if (Test-Path (Join-Path $QtRoot 'exception.txt')) { Get-Content (Join-Path $QtRoot 'exception.txt') -Raw }
    if (Test-Path (Join-Path $QtRoot 'D9_10_QT_GUI_RUNTIME_ACCEPTANCE_REPORT.json')) {
      Get-Content (Join-Path $QtRoot 'D9_10_QT_GUI_RUNTIME_ACCEPTANCE_REPORT.json') -Raw
    }
  }
}
$BoundRoot = '.\artifacts\tests\c11d_d9\d910_adapter_acceptance\D910_QT_ACCEPTANCE_01'
if (Test-Path (Join-Path $BoundRoot 'qt_gui_runtime.stderr.log')) { Get-Content (Join-Path $BoundRoot 'qt_gui_runtime.stderr.log') -Raw }
if (Test-Path (Join-Path $BoundRoot 'qt_gui_runtime.stdout.log')) { Get-Content (Join-Path $BoundRoot 'qt_gui_runtime.stdout.log') -Raw }
```

No asumir que la advertencia de fuentes es fatal; localizar la excepción en `exception.txt`, el campo `error` en el JSON y los logs del run enlazado. Corregir la causa con el cambio más pequeño y añadir una regresión al test si se confirma bug. No modificar los locks para que pase artificialmente.

## 4. Secuencia exacta de consolidación después del fix

Usar **run IDs nuevos** porque los directorios actuales son inmutables y el harness rechaza reutilizarlos:

```powershell
python .\tools\c11d\d9\test_d910_gui_runtime_contract.py
python .\tools\c11d\d9\test_d910_gui_runtime_acceptance.py --run-id D910_QT_GUI_RUNTIME_FIX_01
python .\tools\c11d\d9\capture_d910_acceptance.py --run-id D910_QT_ACCEPTANCE_FIX_01 --include-qt-gui-runtime --include-aggregate
python .\tools\c11d\baseline_candidate\test_d_baseline_candidate.py
python -u .\c11c-suite\self_test.py
```

Expectativas tras una reparación correcta:

- runtime directo: `content_types=3/3`, `status=PASS`;
- acceptance enlazada: siete checks (`5` enfocados + runtime Qt + agregado) y `PASS 7/7`;
- aggregate: `22/22 PASS`;
- candidate preflight: `PASS`, `negative=22/22`, cinco bloqueos, `freeze_eligible=false`, C11-C match;
- renderer OFF, `media_created=false`, D4.8 BLOCKED, `release_authority=NONE`.

Guardar los JSON y logs en `artifacts/tests/c11d_d9/`; no se requieren screenshots. La ejecución offscreen no es una observación visual humana y no prueba el GUI definitivo.

## 5. Límites del producto y de la gobernanza

- Product GUI actual (`c11c-producer`) = **GUI temporal de pruebas/operator**. No iniciar todavía el GUI definitivo; el usuario ha indicado que se abordará sólo cuando todo el baseline D esté aceptado, D9 cerrado y el baseline C11-D congelado.
- El adapter D9.10 permanece `PREPARE_ONLY`. No emitir renderer input, añadir dispatch, lanzar Godot/FFmpeg ni crear media mediante el harness Qt.
- D4.8 = BLOCKED; renderer general OFF; release authority NONE.
- D9 remains OPEN; D9.14 full GUI/E2E not closed; D9.16 blocked; D9.17 BLOCKED/NO-GO; D10 BLOCKED.
- C11-C manifest SHA permanece `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- No pedir pantallazos para estas pruebas D9.10: el harness está diseñado para generar evidencia JSON + logs. Sólo plantear observación/capturas si surge una necesidad concreta que no pueda probarse automatizadamente, y consultarlo con el operador.

## 6. Orden recomendado de lectura

1. Este documento: `docs/current/d/MASTER_HANDOVER_C11D_CURRENT.md`.
2. `docs/current/d/START_PROMPT_C11D_CURRENT.md`.
3. `docs/current/d/D9.10_QT_GUI_RUNTIME_ACCEPTANCE_CHECKPOINT.md`.
4. `docs/current/d/D9.10_EDITORIAL_TO_RENDER_BRIDGE_PLANNING_CHECKPOINT.md`.
5. `docs/current/d/D9.10_D_ONLY_RENDER_ADAPTER_ACCEPTANCE_RUNBOOK.md`.
6. `docs/current/d/C11-D_ROADMAP_V1.0_STATELESS.md` y `docs/current/d/C11-D_MILESTONES_APPROVED.md`.
7. `docs/current/d/D_BASELINE_CANDIDATE_EVALUATION_V1.md`.
8. `docs/current/suite/C11C_SUITE_CURRENT_RULES.md` y `C11C_SUITE_TOOLING_MATRIX.md`.
9. Incidentes/histórico: `docs/history/c11d/d9/D9.10_QT_GUI_RUNTIME_ACCEPTANCE_INCIDENT_20261009.md` y `D9.10_QT_GUI_RUNTIME_AUTOMATION_20261009.md`.

**Siguiente hito:** corregir el fallo de runtime Qt, lograr D9.10 runtime 3/3 y acceptance enlazada 7/7, documentar los resultados reales y seguir con los requisitos de aceptación D9.14/D9.16/D9.17 sin activar renderer.
