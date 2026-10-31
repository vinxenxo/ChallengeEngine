# C11-E — matriz de gates y aceptación (V9)

| Gate | Alcance | Estado |
|---|---|---|
| E0 | Fundación documental, reconciliación D→E, instrucciones archivadas | PASS |
| E1 | Servicio compartido de preparación GUI/CLI, tests Windows | PASS automatizado 2/2; observación GUI manual pendiente |
| E2 | Challenge_001 title-to-pixels A/B, dos MP4 sin audio | V3 bloqueado pre-write por bug de ruta; V4 pendiente Windows |
| E3 | Motor D3, audio y mux | NOT STARTED |
| E4 | Un vídeo físico por familia Challenge/Loop/Drill | BLOCKED BY E2/E3 |
| E5 | Determinismo y regresiones | NOT STARTED |
| E6 | Smoke 18 | NOT STARTED |
| E7 | Matrix 101 | NOT STARTED |
| E8 | Aceptación formal/promoción | NOT STARTED |

## Condiciones transversales

- `main` es el checkout de trabajo. Nunca cambiar a `c11e-unified-editorial-production` ni mover refs.
- C11-C 2.19.12 y su manifiesto congelado permanecen inmutables.
- GUI y CLI consumen el mismo servicio canónico E1. D9.9 se reutiliza como resolver; D9.10 sigue `PREPARE_ONLY`.
- Gameplay seed y music seed permanecen dominios separados.
- `winning_frame`, `close_calls`, `SimulationResult`, detectores, stream de frames, RNG y mecánicas C no se modifican para presentar valores editoriales.
- Los recibos E deben diferenciar preparación, dispatch, captura, mux, aceptación visual y autorización de release.
- No hay autorización general de producción, release o promoción por el mero hecho de superar E2.

## Reglas de no falso PASS

E2 V3: `BLOCKED_BEFORE_WRITE_AND_RENDER`; el path guard falló durante preflight. No hubo render. La línea manual `Write-Host ... PASS` que siguió a un exit code 1 no tiene valor probatorio.

E2 V4: PASS requiere código de salida cero del runner, receipt `E2_AUTOMATED_TITLE_TO_PIXELS_AND_GAMEPLAY_INVARIANCE_PASS_HUMAN_REVIEW_PENDING`, hashes/archivos A/B, 540/540 frames de cuerpo idénticos, 540/540 title slot diferentes, 540/540 header exterior idéntico y 270/270 frames MP4 diferentes. La revisión humana sigue separada.
