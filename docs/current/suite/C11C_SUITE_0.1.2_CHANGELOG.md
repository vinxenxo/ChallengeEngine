# C11-C Suite 0.1.2 — Changelog

## 2026-09-27

### Fixed

- `c11c-test` ya no falla al iniciar por desempaquetado incorrecto de `C11_COMMANDS`.
- La salida del proceso del GUI usa saltos de línea reales.
- La ejecución individual de una suite comprueba primero que el archivo exista.
- `c11c-test/run_all.bat` permite ejecutar todo el corpus lógico desde consola.
- `c11c-test/run_suite.bat` permite ejecutar una suite registrada desde consola.
- El compositor Longform deja de buscar el antiguo `${stem}_manifest.json` dentro del producto de producción.
- Longform consume el `production_manifest.json` que publica el productor canónico y localiza la música en `artifacts/prototypes`.

### Added

- `C11CVisualLoopLongformSourceArtifactContractTest.gd`.
- Comando `LONGFORM BULK` visible en `c11c-test`.
- Contrato documental obligatorio para mantener paridad entre scripts de consola y GUIs de Suite.

### Preserved

No se han cambiado mecánicas, RNG, simulación, `SimulationResult`, `winning_frame`, `RenderedFrameStream`, matemáticas de render ni ownership audiovisual.
