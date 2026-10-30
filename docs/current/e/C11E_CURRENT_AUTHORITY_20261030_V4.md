# C11-E — autoridad operativa vigente (V4)

**Fecha:** 2026-10-30 · **Rama de trabajo:** `main` · **HEAD base:** `bc8330e794fe37efe0c4f9c2bb0c0bd389f28f2c`.

Este documento es el punto de entrada vigente para C11-E y prevalece sobre cualquier estado inicial de V3 que describa E0 como no aplicado o pendiente de ejecución. Los documentos V3 se conservan sin modificación como registro de la planificación original.

## Orden de autoridad

1. `AGENTS.md` y `.continue/rules/CONTINUE.md` enrutan al conjunto vigente E.
2. Este documento fija estado y enlaces actuales.
3. `C11E_E0_REVIEW_AND_E1_SOURCE_ARCHITECTURE_20261030_V1.md` recoge la revisión independiente de E0 y el análisis E1.
4. `C11E_GATES_ACCEPTANCE_MATRIX_20261030_V4.md` gobierna el avance E0–E8.
5. `C11E_DOCUMENTATION_RECONCILIATION_20261030_V4.md` resuelve referencias V3 obsoletas y la transición D→E.
6. Charter, contrato y registro de riesgos V3 siguen siendo los contratos fundacionales, salvo aclaraciones expresas de este addendum.
7. Los contratos/freeze C11-C mantienen autoridad sobre el motor y la línea de producción C. Los registros D conservan su alcance histórico y sus bloqueos propios.

## Estado confirmado

- E0: `PASS` en aplicación e inspección independiente. Overlay V3: 12/12 hashes de instalación; instrucciones históricas pre-E: 2/2 copias verificadas; manifiesto C11-C: SHA y tamaño exactos.
- Checkout observado: `main`, HEAD `bc8330e794fe37efe0c4f9c2bb0c0bd389f28f2c`. Las refs locales/remotas `c11e-unified-editorial-production` permanecen en ese mismo commit. Ninguna ref se ha movido.
- E1: `IN_PROGRESS`. El inventario identifica que D9.9 resuelve datos editoriales y construye planes, mientras que D9.10 y la fachada compartida D siguen siendo preparación sin despacho físico. El trabajo siguiente es implementar el servicio de producción E compartido por GUI/CLI, no reactivar D9.10.
- No se ha invocado renderer desde E0. No hay MP4 E2 ni prueba de píxeles todavía.

## Objetivo invariable

Primera prueba funcional: `CHALLENGE_001`, dos MP4 con el mismo request salvo `title`; el título debe verse en un slot editorial dedicado y los frames mecánicos, semilla de juego, duración y número de frames deben permanecer iguales. `title` no se convertirá en `content.hook`, ni reemplazará CTA, telemetría o resultado de simulación.

## Límites

C11-C 2.19.12 sigue siendo el baseline de producción protegido. No modificar el manifiesto ni el ZIP congelado. No alterar simulación, `SimulationResult`, `winning_frame`, `close_calls`, RNG, definiciones de mecánica o pipeline de captura C. `request.seed` y `request.music_seed` permanecen separados. CHALLENGE_008/009 quedan excluidos hasta resolver formalmente 11 s declarados frente a 12 s por suma de fases.
