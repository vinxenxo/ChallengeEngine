# C11-E — gates y matriz de aceptación

**Versión:** V3 · **Fecha:** 2026-10-30 · **Estado inicial:** E0 pendiente de ejecución en Windows.

## Principio de avance

Cada gate tiene entrada, alcance, artefactos, tests, resultado y receipt separados. Un PASS no se hereda a otro gate. No se invocan renderers físicos en E0–E1. E2 autoriza únicamente los dos Challenge físicos aislados para la prueba A/B de `title`; E3 incorpora audio/mux; E4 completa la cobertura física de Loop y Drill. Son pruebas de ingeniería, no producción ni release.

| Gate | Objetivo | Pruebas/artefactos mínimos | Criterio de salida |
|---|---|---|---|
| E0 — Foundation/bootstrap | Verificar checkout `main`, pines y árbol limpio; aplicar esta documentación sin cambiar ramas ni refs | Receipt del script, branch/HEAD, estado Git, hash+tamaño manifest C, hashes de overlay, diff de docs | Checkout permanece en `main` / `bc8330e794fe37efe0c4f9c2bb0c0bd389f28f2c` y conserva su commit documental padre `8f6905003a4dff979ed97dc2e721d1abc4375de8`; refs C11-E local/remota no se mueven; baseline C pin PASS; instrucciones E instaladas; no render ni cambio de código C |
| E1 — Service & request | Una única API de producción GUI/CLI | Contratos, normalizador, resolver, selector, adapters, tests unitarios y contract tests GUI/CLI | Mismo request normalizado, plan, identidad y error behavior en CLI/GUI; ninguna llamada física aún |
| E2 — Visual editorial Challenge | Primer campo editorial llega a píxeles en un Challenge excluido del conjunto 008/009 | Matriz campo-slot, adapter, render receipt, dos MP4 con `title` diferente, comparación de frames y gameplay | Campo visible en frames; el resto de gameplay/duración/semilla permanece estable; revisión visual documentada |
| E3 — Audio/mux | Conectar D3 + FFmpeg a la solicitud canónica E | `music_seed`, WAV/track receipt, mux, FFprobe, determinismo | Audio depende solo de music domain y perfil; vídeo gameplay no se altera; MP4 A/V completo validado |
| E4 — Familia real y aislamiento | Completar cobertura de familias: Challenge (evidencia E2), Loop y Drill físicos | Revalidar pines E2 y ejecutar un run aislado de Loop y otro de Drill, receipts y validaciones frame/video/audio | Challenge/Loop/Drill generan MP4 válidos y los campos permitidos llegan a sus consumidores reales |
| E5 — Determinismo/regresión | Verificar reproducibilidad y ausencia de regresiones C | Repetición exacta, seeds cruzadas, tests C antes/después, GUI/CLI parity, diff outputs | Determinismo dentro del contrato; sin cambio de verdad/frames mecánicos no justificado |
| E6 — Smoke 18 | Cobertura rápida de las rutas principales | Lista declarativa de 18 casos, resultados individualizados | 18/18 PASS; no ocultar skips ni fallos; cada test tiene receipt |
| E7 — Matrix 101 | Matriz ampliada objetivo | 54 Challenge + 27 Loop grammar + 20 Drill variants, lista exacta desde catálogo/contratos | Casos enumerados y todos los válidos PASS; exclusiones explícitas. Recalcular la cifra si 008/009 siguen excluidos y no inventar cobertura |
| E8 — C11-E acceptance & promotion | Decidir si E sustituye la línea de producción | Review independiente, congelación E, manifest/ZIP/tree hashes, release notes, migración reversible | Baseline approval explícita, freeze/acceptance formal y promoción separada. Hasta entonces C11-C manda |

## E0 — precondiciones exactas

- Root `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`.
- HEAD reconciliado para iniciar el workstream E sobre main: `bc8330e794fe37efe0c4f9c2bb0c0bd389f28f2c`; su único padre es la captura histórica `8f6905003a4dff979ed97dc2e721d1abc4375de8`.
- Branch observada: `main`.
- Árbol esperado limpio: `git status --short --branch` devolvió `## main...origin/main [ahead 1]`; el commit local adicional actualizó únicamente los catálogos D generados.
- `release/C11C_FREEZE_PACKAGE_MANIFEST.json`: SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`, 796318 bytes.
- `AGENTS.md`: preimage SHA-256 `0d4565e57b9fe9bba88a88f10babd175f3bb5e3fb437014866ed1e67d3016b37`.
- `.continue/rules/CONTINUE.md`: preimage SHA-256 `52776e55023a36e1ead71cf39a93337ca96f6097bd2c88018c3353484145ac86`.

El script aborta antes de cambiar archivos si HEAD/branch/árbol/pines/preimages no coinciden. No hace reset, clean, checkout forzado, commit, push, render ni modificación del manifiesto C.

## E2 — prueba funcional inicial

La prueba preferida es `CHALLENGE_001` con mismo selector, semilla de juego, delivery profile y todas las propiedades constantes; solo cambia el valor `title`. Requiere dos renders con distinto `title`. Comparar:

- Frame count, duración, FPS y resolución idénticos.
- Estado/resultado de simulación, hit/close-call y secuencia temporal idénticos.
- Slot editorial identificado en un subconjunto de frames; texto A visible en el render A y texto B en render B.
- Fuera de la máscara editorial, las imágenes deben ser iguales o las diferencias deben estar explicadas por una fuente de nondeterminism documentada. No comparar hashes completos de MP4 si el contenedor incluye timestamps/metadatos variables sin normalizar.
- Receipt identifica el valor resuelto y hash exacto del contexto visual aplicado; no basta con el request hash.

## E3 — prueba de audio

Separa las variables de vídeo y audio. Mismo source MP4 + mismo music seed/profile debe producir el mismo audio normalizado o explicar fuentes de nondeterminism. Cambiar music seed no puede modificar el vídeo antes del mux. `FFprobe` debe verificar al menos video stream, audio stream presente cuando pedido, duración/stream timestamps coherentes y codecs/formatos admitidos.

## E5 — regresión C

Acordar un set mínimo de regresión de mecánica/frames desde el runner existente sin mutar sus definiciones. Las comparaciones deben ejecutarse antes y después del cambio visual E con los mismos seeds y toolchain. Si el cambio E no está activo, la salida C debe permanecer byte/semánticamente inalterada según el contrato de cada test.

## 008/009

`CHALLENGE_008` y `CHALLENGE_009` se excluyen de los primeros renders y de cualquier matriz cuya duración requiera esa definición. El contrato conocido declara 11 s mientras las fases suman 12 s (3+7+0+2). No truncar, redondear ni cambiar frames sin decisión y fuente autorizada. E7 debe reflejar la exclusión en su conteo final.

## Estados permitidos

`NOT_STARTED`, `IN_PROGRESS`, `PASS`, `PASS_WITH_EXCLUSIONS`, `FAIL`, `BLOCKED`, `NOT_APPLICABLE`. Toda excepción se enumera. No usar `PASS` para un gate con tests omitidos o salida no inspeccionada.


**Política Git V3:** el usuario ha elegido `main` como rama local de trabajo. E0 y los cambios E se aplican sobre `main`; ningún gate cambia ramas, crea commits o hace push salvo instrucción explícita posterior.
