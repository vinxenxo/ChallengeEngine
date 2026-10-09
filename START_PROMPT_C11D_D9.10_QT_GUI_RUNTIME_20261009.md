# START PROMPT — C11-D D9.10 Qt GUI Runtime (2026-10-09)

Continúa el proyecto **ChallengeEngineV01_STATELESS** desde el snapshot congelado por el operador:

- `Library: ChallengeEngineV01_STATELESS_C11-D D9.10_20261009_220331.zip`
- SHA-256: `fa3c4e2299ecf7ecffa81925689313c1a79b47e437edbfc539f16e10973379b2`
- Repo local Windows: `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`
- C11-C manifest inmutable SHA-256: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`

Lee primero `docs/current/d/MASTER_HANDOVER_C11D_CURRENT.md` y `docs/current/d/D9.10_QT_GUI_RUNTIME_ACCEPTANCE_CHECKPOINT.md`. Este prompt y el handover son la autoridad de estado más reciente; los bloques antiguos dentro de documentos históricos no deben prevalecer sobre ellos.

## Estado real — no confundir contrato estático con runtime

- D9.10 bridge/adapter prepare-only: implementado; Challenge/Loop/Drill, parity bridge 3/3, adapter 3/3, negatives 15/15 + 9/9.
- `python .\tools\c11d\d9\test_d910_gui_runtime_contract.py`: PASS.
- `python -u .\c11c-suite\self_test.py`: PASS 22/22; el step 22 es el contrato estático libre de dependencias Qt.
- `test_d910_gui_runtime_acceptance.py --run-id D910_QT_GUI_RUNTIME_01`: **FAIL 0/3**.
- `capture_d910_acceptance.py --run-id D910_QT_ACCEPTANCE_01 --include-qt-gui-runtime --include-aggregate`: **FAIL 6/7** porque el runtime opcional falla; no declarar todo PASS.
- Salida Qt incluye avisos de font database y `propagateSizeHints()`, pero no se ha establecido que sean la causa raíz. Revisar `exception.txt` y el JSON del run antes de cambiar código.
- La última comprobación D candidate suministrada antes de estos runs pasó con cinco bloqueos y `freeze_eligible=false`; repetir el preflight en la sesión nueva.
- D9.14 bounded qualification anterior: PASS, cuatro A/V MP4; report SHA `daa5e5676224d606e9d67ac7a7ed7e88c3c02a63c76ecdc579c3bc2dd320853f`, baseline SHA `15343119f0f8338b13b47b0ea98546e5470d4a1a8895b65dbe1f41ee183e66d3`. No es cierre full D9.14.

## Tu primera tarea

Inspecciona estos artefactos y devuelve la excepción real, no una hipótesis:

```powershell
$QtRoots = @(
  '.\artifacts\tests\c11d_d9\d910_gui_runtime_acceptance\D910_QT_GUI_RUNTIME_01',
  '.\artifacts\tests\c11d_d9\d910_gui_runtime_acceptance\D910_QT_ACCEPTANCE_01'
)
foreach ($QtRoot in $QtRoots) {
  if (Test-Path $QtRoot) {
    Write-Host "`n===== $QtRoot ====="
    if (Test-Path (Join-Path $QtRoot 'exception.txt')) { Get-Content (Join-Path $QtRoot 'exception.txt') -Raw }
    if (Test-Path (Join-Path $QtRoot 'D9_10_QT_GUI_RUNTIME_ACCEPTANCE_REPORT.json')) { Get-Content (Join-Path $QtRoot 'D9_10_QT_GUI_RUNTIME_ACCEPTANCE_REPORT.json') -Raw }
  }
}
$BoundRoot = '.\artifacts\tests\c11d_d9\d910_adapter_acceptance\D910_QT_ACCEPTANCE_01'
Get-Content (Join-Path $BoundRoot 'qt_gui_runtime.stderr.log') -Raw -ErrorAction SilentlyContinue
Get-Content (Join-Path $BoundRoot 'qt_gui_runtime.stdout.log') -Raw -ErrorAction SilentlyContinue
```

Diagnostica a partir del traceback/log. Corrige sólo la causa, conserva las aserciones, añade test de regresión si procede y no desactives `fail-closed`, parity o los locks del adapter.

## Verificación esperada tras la reparación

Usa run IDs nuevos:

```powershell
python .\tools\c11d\d9\test_d910_gui_runtime_contract.py
python .\tools\c11d\d9\test_d910_gui_runtime_acceptance.py --run-id D910_QT_GUI_RUNTIME_FIX_01
python .\tools\c11d\d9\capture_d910_acceptance.py --run-id D910_QT_ACCEPTANCE_FIX_01 --include-qt-gui-runtime --include-aggregate
python .\tools\c11d\baseline_candidate\test_d_baseline_candidate.py
python -u .\c11c-suite\self_test.py
```

Debe quedar runtime 3/3 PASS, acceptance 7/7 PASS (5 focos + runtime + agregado), Suite 22/22 PASS y candidate preflight PASS/freeze bloqueado. Actualiza los documentos current + changelog/historial tras confirmar los resultados reales.

## Reglas que no puedes romper

- No modificar C11-C 2.19.12 ni su manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- D9.10 adapter = `PREPARE_ONLY`; no renderer input/dispatch, no producción/media en el test Qt.
- D4.8 `BLOCKED`, renderer OFF, `release_authority=NONE`.
- D9 permanece OPEN; full D9.14, D9.16 y D9.17 siguen sin cerrar; D10 BLOCKED.
- D9.15 waiver vale sólo para la evaluación del candidato; no declararla canonical PASS/CLOSED.
- No hacer screenshots manuales por defecto: el harness produce JSON y logs. El GUI actual es **test/operator GUI**, no el GUI final.
- El GUI definitivo sólo se abordará cuando el baseline D completo esté validado y frozen.

No des por completada la fase sólo porque la suite agregada sea verde: la aceptación Qt runtime es opcional y falló por separado. La tarea inmediata consiste en convertir ese FAIL 0/3 en PASS 3/3 con evidencia de ejecución real.
