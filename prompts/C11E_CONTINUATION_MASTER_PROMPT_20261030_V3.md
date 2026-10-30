# Prompt maestro de continuidad — C11-E

Actúa sobre `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`, manteniendo activa la rama Git local `main`. C11-E es el workstream lógico; no cambies a `c11e-unified-editorial-production`, no crees/eliminés/avances refs y no hagas push salvo instrucción explícita posterior. E es la nueva línea de integración C11-E: producir MP4 reales bajo demanda desde una solicitud editorial canónica, manteniendo C como motor mecánico/generador y reutilizando los módulos D que se validen.

## Orden de autoridad

1. Checkout Windows activo y su `git status`, HEAD y hashes actuales.
2. `AGENTS.md` y `.continue/rules/CONTINUE.md`.
3. `docs/current/e/README.md`.
4. Carta, contrato de arquitectura, gates, revisión documental, runbook E0 y registro de decisiones/riesgos C11-E.
5. Contratos y baseline congelado C11-C 2.19.12.
6. Documentación/artefactos D como evidencia histórica y módulos reutilizables, cada uno sujeto a pins y validación.

## Misión

GUI y CLI deben llamar a un servicio canónico común. El request resuelve familia/selector, `seed`, `music_seed`, delivery/editorial profiles y campos allowlisted. C genera mecánica y frames. E introduce la editorial en el consumidor visual real por un adaptador explícito. D3 genera música con `music_seed`; FFmpeg muxea; FFprobe valida el MP4. Cada run entrega receipt con identidad, hashes, comandos, stdout/stderr, exit codes, outputs y validaciones.

## Estado inicial esperado

La captura histórica fijó `main` / `8f6905003a4dff979ed97dc2e721d1abc4375de8`. E0-R1 confirmó `main` / `bc8330e794fe37efe0c4f9c2bb0c0bd389f28f2c`, cuyo padre único es `8f6905003a4dff979ed97dc2e721d1abc4375de8`, con solo los dos catálogos D generados modificados por el commit `doc catalog`; árbol limpio y manifiesto C SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`, 796318 bytes. E0-R3 confirmó rama activa `main` y refs local/remota `c11e-unified-editorial-production` en el mismo HEAD; el usuario exige permanecer en `main`, por tanto no cambies ramas ni refs. V2 creó la ref en una ejecución parcial pero no instaló los ficheros. V3 debe instalar sobre `main` y crear receipt local antes de declarar E0 aplicado.

## Reglas no negociables

- C11-C permanece immutable baseline; no alterar manifest, ZIP congelado, mecánica, RNG, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector` o `RenderedFrameStream`.
- No reconstruir el motor ni duplicar rutas de producción. Reutilizar runners C y cinco superficies `c11c-suite`; no crear `c11d-control`.
- El estado D (`PREPARE_ONLY`, renderer off, media false, binding 0, gates bloqueados) se mantiene como verdad scoped del programa D. E no falsifica ni edita esos recibos. E define gates y outputs físicos de test separados.
- `request.seed` y `request.music_seed` no se mezclan. No seed generation automática.
- No leer/proyectar `FrameSnapshot.custom_data` en el primer incremento.
- `CHALLENGE_008/009` excluidos hasta resolver declared 11 s vs 12 s de fase sum.
- Windows PowerShell 5.1: bloques completos y pegables; no `&&`, `Read-Host` ni sintaxis PS7-only. Aplicar y probar por separado. Capturar exit codes reales, stdout y stderr separados.
- No sobrescribir ni borrar outputs/catálogos/evidencias existentes. Cambios aditivos, pins exactos y stop at first failure.

## Gates

E0 Foundation/bootstrap → E1 servicio/request GUI-CLI → E2 `title` visible en MP4 de Challenge 001 → E3 D3 audio/mux → E4 revalida el Challenge E2 y produce un Loop + un Drill físicos → E5 determinismo/regresión → E6 smoke 18 → E7 matriz objetivo 101 con exclusiones enumeradas → E8 aceptación/freeze/promotion formal.

No invocar renderer físico antes de E2. E2 autoriza dos renders Challenge aislados para `title` A/B; E4 añade Loop y Drill. Son pruebas de ingeniería, no release approval. El primer caso funcional usa dos valores diferentes de `title` con el mismo gameplay seed y debe demostrar que solo cambia el slot editorial.

## Siguiente acción

Si E0 V3 todavía no está ejecutado, revisar checkout `main`/receipt y completar únicamente la instalación de documentos sobre `main`, sin cambiar refs. Si E0 PASS, iniciar E1 con lectura activa de los archivos que realmente participan: `main.py`, `c11d_gui_request.py`, `shared_production_context_service.py`, universal request/model, family launchers, binder/scene exactos y D3. Fijar hashes de esos ficheros en el checkout E antes de parchear. No repetir inventario de 1.507 docs salvo cambio real de snapshot o evidencia de divergencia.
