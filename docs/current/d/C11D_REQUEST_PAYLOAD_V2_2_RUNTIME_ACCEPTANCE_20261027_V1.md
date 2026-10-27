# C11-D — Aceptación Windows runtime V2.2 y siguiente puerta de auditorías

**Fecha:** 27-10-2026  
**Estado:** `V2_2_WINDOWS_RUNTIME_PASS; IO_IDENTITY_REFRESH_PENDING`  
**Workstream:** enlace canónico solicitud → instancia de payload → evidencia de revisión

## Resultado aceptado

El checkout operativo confirmó la aplicación del overlay V2.2 con siete destinos verificados, `16/16` pruebas focalizadas y runtime Godot 4.7.1 Mono real con exit code `0`. El recibo V2 quedó validado por las guardas del pipeline y conserva todos los límites de gobernanza.

### Evidencia de aplicación y test

- Overlay: `C11D_REQUEST_PAYLOAD_V2_EDITORIAL_HASH_NAMESPACE_FIX_OVERLAY_20261027_V1.zip`
- Overlay SHA-256: `b7ee45e2060258381d240b4aa5dfd14ff00f84c56fb2e65e84589fd546e37b5a`
- `C11D_V2_2_EDITORIAL_HASH_FIX_APPLY=PASS`, replacements `5/5`, additions `2/2`, V2.2 pins `7/7`, C11-C manifest unchanged.
- Test exit `0`; `Ran 16 tests ... OK`; `C11D_REQUEST_PAYLOAD_V2_2_UNIT_TEST=PASS`.
- Test stdout SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- Test stderr SHA-256: `3183ebabac73872621e28e140dc029fb9875826166ab85b7a0fe2687f6b7215f`.
- Test folder: `%TEMP%\C11D_REQUEST_PAYLOAD_V2_2_TEST_20261027_46ad02316d824c46884fc1a6ec6f4a01`.

### Evidencia de runtime

- Godot: `4.7.1.stable.mono.official.a13da4feb`; ruta ejecutable WinGet comprobada mediante captura redirigida; versión exit `0`.
- Runtime exit `0`; `C11D_REQUEST_PAYLOAD_V2_2_RUNTIME_VALIDATION=PASS`; `C11D_V2_2_PIPELINE=PASS`.
- Stdout SHA-256: `00a0d51627618ae3ee167a7d2ca029f6ed5cd05ecf369f8d816ef5774d99051a`.
- Stderr SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (vacío).
- Recibo SHA-256: `1a2a729137458f633cf520c211180ce5a3fff2d21ed441e866ae0e1c946169af`.
- Carpeta: `%TEMP%\C11D_V2_2_RUNTIME_20261027_d2425963e21448bd9d04c2a044a7bea9`; `runtime_validation_evidence.json` se conserva allí.

### Matriz aceptada

| Comprobación | Resultado |
|---|---:|
| Fixtures fijos | 3/3 |
| Joins de request canónico y selector | 3/3 |
| Payload manifest digests | 3/3 |
| Editorial sidecar joins | 3/3 |
| Campos sidecar | 14/14 |
| Consumo visual editorial | 0/14 |
| Source pins | 60/60 |
| Equivalencia entre namespaces de payload | No afirmada |

Los fixtures son Challenge `parking_v2/CHALLENGE_004` (gameplay seed 314159), Loop `c11c_geometric_waves_v1/harmonic_membrane` (seed 12345) y Drill `tracking/tier-2` (seed 12345), con music seed 840001. El digest editorial compuesto `CANONICAL_SELECTION_PLUS_EDITORIAL_MAP` y el digest `EDITORIAL_MAP_ONLY` se mantienen independientes y se verifican mediante reconstrucción exacta.

## Qué no demuestra este PASS

Este resultado demuestra el join determinista de identidad, manifest, linaje y sidecar editorial para tres fixtures fijos en memoria. No demuestra consumo del texto editorial por el payload visual, render, píxeles, vídeo final ni admisibilidad de candidato. Los harnesses anteriores indican que la proyección de coordenadas y el resampling de delivery permanecen sin aplicar; la telemetría permanece sin enlazar.

## Siguiente puerta: refresco I/O + identidad

El helper `tools/c11d/d9/refresh_d_renderer_candidate_io_and_identity_after_v2_2.ps1` se incorpora como herramienta add-only. Ejecutarlo **una sola vez** después de aplicar el overlay de aceptación. Validará los hashes actuales, ejecutará únicamente los dos auditores read-only y capturará stdout/stderr y hashes en `%TEMP%`. La salida real se añadirá a un nuevo checkpoint/ledger; no se adivinarán los nuevos resultados ni se usará el PASS V2.2 para marcar grupos de I/O como completos.

## Gobernanza inmutable

`renderer=OFF`; `media_created=false`; `candidate_input_admissible=false`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`. El manifiesto congelado C11-C mantiene SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` y 796318 bytes.
