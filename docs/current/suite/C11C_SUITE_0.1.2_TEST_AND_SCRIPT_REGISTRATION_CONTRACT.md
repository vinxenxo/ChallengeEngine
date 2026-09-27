# C11-C Suite 0.1.2 — Test and Script Registration Contract

## Objetivo

Desde esta versión, cada prueba nueva o script nuevo de verificación que pase a formar parte del toolchain debe tener una vía de lanzamiento visible en la Suite correspondiente.

## Suites `*Test.gd`

La fuente canónica es `tests/run_all.py`, mediante `KNOWN_SUITES`.

`c11c-suite/c11c-test` no duplica la lista de suites individuales: la lee directamente y muestra todas las entradas registradas.

Cuando se crea un nuevo `tests/**/*Test.gd`:

1. Se registra el archivo y su marcador en `KNOWN_SUITES`.
2. La suite se puede ejecutar directamente por Godot.
3. Aparece automáticamente en la lista de `c11c-test`.
4. Queda disponible desde consola con `c11c-test\run_suite.bat`.

## Consola

Corpus lógico completo:

```powershell
.\c11c-suite\c11c-test\run_all.bat
```

Suite individual:

```powershell
.\c11c-suite\c11c-test\run_suite.bat C11CProductionReviewCopySafetyTest.gd
```

Las dos rutas usan los runners canónicos del proyecto; el GUI no contiene una implementación paralela del test.

## Scripts PS1

Los runners operativos de freeze, QA histórica, Art Direction y Longform se muestran como comandos de `c11c-test`. Cuando un nuevo `.ps1` se convierta en un punto de entrada oficial de verificación, debe añadirse a `C11_COMMANDS` para mantener paridad GUI/consola.

No se deben duplicar dentro del GUI las operaciones del script; el botón solo lanza el script canónico.

## Invariantes

Ninguna GUI modifica o reimplementa mecánicas, RNG, simulación, `SimulationResult`, `winning_frame`, `RenderedFrameStream`, matemáticas de render, ownership audiovisual o contratos de audio.

## Longform

El compositor Longform consume los productos canónicos `REVIEW_720` publicados en `artifacts/production/audiovisual/<family>/<stem>`.

El manifiesto del producto es `production_manifest.json`. La música de cada segmento permanece en la superficie canónica de prototipos (`artifacts/prototypes/<family>`). El compositor no debe asumir que el manifiesto original de prototipo está duplicado dentro del producto final.
