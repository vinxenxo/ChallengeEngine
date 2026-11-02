# C11-E E3.2 — Integración de contrato D3 V5 con E1

- **Versión:** 1.0
- **Fecha:** 2026-11-02
- **Estado:** IMPLEMENTACIÓN PREPARADA; pendiente de aplicación y ejecución de pruebas en el checkout activo.
- **Servicio:** `0.2.0-E3.2`
- **Intent schema:** `C11-E-PRODUCTION-INTENT-V1`, versión `1.1`.

## Objetivo

Conectar semánticamente el motor musical D3 V5 con el intent compartido E1 (GUI/CLI), sin ejecutar el motor desde E1, sin generar audio de producción y sin activar renderer, FFmpeg ni mux. El cambio conserva la síntesis para entradas válidas: V5 normaliza los nombres declarativos `profile_id/profile_version` a `style_profile_id/style_profile_version` y rechaza una identidad de perfil solicitada que no coincida con el perfil cargado.

## Hallazgo de reconciliación

El perfil actual declara `profile_id=challenge_8bit_v1` y `profile_version=1.0`, mientras V5 consumía los alias `style_profile_id/style_profile_version` con valores por defecto coincidentes. La coincidencia implícita queda sustituida por un mapeo explícito y comprobado. Los hashes de fuente se fijan en el contrato de E3.2.

D9.9 normaliza `music_seed`, `variation_index` y `audio_enabled`, pero no aporta `tempo_bpm` ni `duration_seconds` al intent canónico. E1 no debe inventar valores ni utilizar los defaults CLI de V5 para completar una petición semántica. Esos dos parámetros permanecen `null` y bloquean la condición `dispatchable`.

## Cambio mínimo

1. `tools/c11d/d3/c11d_music_engine_v5.py`: valida la identidad de motor del perfil, normaliza identificadores y versiones declarativas, y falla ante perfiles incompatibles. No cambia fórmulas, capas, RNG, forma de onda, frecuencia, canales ni la síntesis de entradas válidas.
2. `definitions/c11e/music/C11E_E3_2_D3_V5_E1_MUSIC_CONTRACT_V1.json`: contrato versionado y hash-pinned para motor, especificación y perfil.
3. `c11c-suite/c11c-producer/c11e_production_service.py`: el intent E1 incluye `music_contract`, añade pins de las cuatro fuentes musicales solo para Challenge, eleva el intent schema a 1.1 y el servicio a `0.2.0-E3.2`. La validación reconstruye el binding, verifica los pins requeridos y comprueba el hash semántico del intent.
4. `test_c11e_e3_2_music_contract.py`: verifica binding de Challenge, audio deshabilitado, preservación de Loop/Drill, resistencia a manipulación, repetibilidad V5, diferenciación por `music_seed` y rechazo de perfil incompatible.

## Política por familia

- Challenge con audio activado: `PLANNED_NOT_RENDERED`; enlaza `c11d_music_engine_v5` + `challenge_8bit_v1`, mantiene `music_seed` y `variation_index`, pero no es despachable porque tempo y duración siguen sin resolver.
- Challenge con audio desactivado: `DISABLED_BY_REQUEST`; no se emite petición al motor.
- Visual Loop / Visual Drill: `PROTECTED_FAMILY_NOT_REWIRED`; el servicio ni siquiera carga ni pinnea el motor/perfil V5 de Challenge en esas peticiones. Se conserva el comportamiento musical existente de C11-C sin añadir una dependencia lateral.

## Límites que permanecen cerrados

`core/audio`, generadores protegidos C11-C, C11-C freeze manifest, mecánicas/simulación/RNG de gameplay, GUI de producción, D9.10, Godot, renderer, FFmpeg y mux no se modifican ni invocan. E1 continúa sin crear directorios de producción ni medios. `release_authority=NONE`; no se concede aprobación de render, audio piloto, promoción ni release.

## Pruebas y resultados esperados

El runner ejecuta el conjunto `test_c11e*.py` desde `c11c-suite/c11c-producer`. La prueba real de V5 crea tres WAV únicamente dentro de `TemporaryDirectory` y el directorio se elimina al terminar. No se escriben archivos en `artifacts/production`, `media` ni rutas de producción.

Resultados que se deben devolver: salida completa, exit code, SHA-256 de stdout/stderr, `git diff --check`, `git status --short` y `git diff --stat`. Esta entrega no declara pruebas ejecutadas sobre el checkout Windows.

### Comprobaciones aisladas previas del paquete

- `py_compile` de motor, servicio y nuevo test: PASS.
- Un render de control con los mismos parámetros en el V5 anterior y en el modificado produjo el mismo WAV SHA-256: `909d0e5271917894da936ca72f698986290f7aa8d52d9c0456fb93fb9f0d41b2`.
- Repetición con el mismo `music_seed`, cambio de semilla y entrada CLI V5: PASS.
- Harness local temporal de `_build_music_contract` y prepare/validate con resolver/manifest sintéticos: PASS. No sustituye las pruebas contra el manifest ni los pines reales del checkout Windows.

## Pins de entrada reconciliados

- Entrada Git: `main` / `a30b63d31b2d071ebab9c67ec9f8ff7393731488`, árbol limpio.
- Motor V5 pre-cambio: `69ebcf96f47360ceea60568ec52f5ef44d2516c7aa14be8452817d7fab79a402`.
- Spec V5: `8970f4e93c878285b727697f3d269f5ee464b6029fe79eabc5fcbf4245e9dbf2`.
- Perfil Challenge: `0c877cbe6e1c288890da31fc4481a58e1051749b45a50b2290cbef5d1120d2de`.
- E1 service pre-cambio: `6f18d5fd906ff615d95d7f9d53e2e6ff0bf37c74e185efdcaf34354c888b9645`.
- E1 tests pre-cambio: `c48d50b3ee61fe152fafabfccb80ee86d7ab77449f5be2ae3e7340d2ff9dea70`.
- C11-C manifest: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

Los pins describen el punto de entrada; el contrato nuevo fija el hash del V5 resultante y los hashes de sus declaraciones. Ningún ZIP de revisión sustituye al checkout activo.

## Decisión E3.2

**Preparado para aplicación local controlada.** El resultado de las pruebas podrá acreditar la integración de contrato y determinismo de V5 en aislamiento, pero no la producción de audio integrada, el mux, ni la autoridad de producción.
