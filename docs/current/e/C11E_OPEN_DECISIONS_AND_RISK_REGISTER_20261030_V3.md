# C11-E — registro de decisiones abiertas y riesgos

**Versión:** V3 · **Fecha:** 2026-10-30.

## Decisiones fijadas para esta fundación

| ID | Decisión | Motivo / límite |
|---|---|---|
| E-DEC-001 | Rama Git de trabajo `main` (decisión del usuario, 2026-10-30) | C11-E opera como workstream lógico en el checkout local `main`; mantener las refs `c11e-unified-editorial-production` local/remota sin modificarlas. Los gates/receipts y paths E proporcionan trazabilidad sin forzar un cambio de rama. |
| E-DEC-002 | C mantiene mecánica y generación por familia | Los runners y compositores físicos existen; no se crea otro engine. |
| E-DEC-003 | Un servicio canónico compartido por GUI/CLI | Evita divergencia de normalización, semillas, dispatch y receipts. |
| E-DEC-004 | Challenge primero, `CHALLENGE_001`, campo `title` | Reduce superficie de prueba y excluye 008/009. El slot exacto aún debe confirmarse en source activo. |
| E-DEC-005 | `seed` y `music_seed` son dominios separados | Evita acoplar gameplay y generación musical. |
| E-DEC-006 | Pruebas físicas E solo en gates explícitos y roots aislados | Rompe el bloqueo circular de D sin convertir test PASS en release approval. |
| E-DEC-007 | Cinco módulos `c11c-suite`, sin `c11d-control` | Conserva estructura operativa existente. |
| E-DEC-008 | C11-C 2.19.12 permanece inmutable hasta E8 | Protege la producción actual y permite rollback. |

## Abiertos — se resuelven mirando código/contratos, no por intuición

1. API final y ubicación/nombre del servicio E (revisar la clase D shared service preexistente y el layout real del repo antes de añadir módulo paralelo).
2. Slot y fase visual exacta para `title` en Challenge 001, sin reinterpretarlo como hook/CTA.
3. Lista exacta de campos admitidos para Challenge, Loop y Drill y sus ventanas temporales.
4. Adaptación compatible de escenas/scripts Godot: decidir si el contexto se inyecta antes del binder o se aplica como overlay después; cada familia puede requerir distinto seam.
5. Qué partes de D9.9 pueden reutilizarse sin acoplar E a un bridge `PREPARE_ONLY`.
6. API exacta y control de versiones de D3; codecs/mezcla/normalización final de audio.
7. Catálogo exacto de los 18 casos smoke y de los 101 casos de matriz (o cifra revisada por exclusiones reales).
8. Harness de diff visual y cómo normalizar timestamps/metadatos que hacen variar el contenedor MP4.
9. Compatibilidad con profiles/config disponibles en el checkout E activo.

## Riesgos y mitigaciones

- **R1 — cambio en código fuente desde el snapshot:** no usar hashes snapshot-only como pines actuales. Mitigar con E0, luego hash activo de los ficheros afectados antes de cada parche.
- **R2 — duplicación de servicio D:** inspeccionar los adapters existentes, reusar o extender con nombre/contrato versionado; no crear un servicio competidor.
- **R3 — editorial visual sobrescribe mecánica/phase UI:** aplicar solo slots permitidos, preservar precedencia CTA/intro/reveal y probar frames sin/ con contexto.
- **R4 — escritura en output C:** root temporal exclusivo por run ID, no overwrite, manifest por run.
- **R5 — seeds acopladas:** contrato y tests de aislamiento `seed` vs `music_seed`.
- **R6 — nondeterminism de Godot/FFmpeg:** comparar frames/streams normalizados y documentar versiones, no basarse solo en hash MP4.
- **R7 — matriz 101 cuenta escenarios bloqueados:** enumerar las 101 filas desde catálogo/contratos; mantener 008/009 excluidos sin alterar la matemática de la matriz.
- **R8 — docs contradictorias de D:** mantener D histórico scoped y enrutar la rama E desde AGENTS/CONTINUE; no reescribir o borrar artefactos D.

## Stop conditions

Detener el gate afectado si cambia el manifiesto C, cualquier mecánica/seed/timing protegida, el consumidor visual no puede distinguir el contexto E del estado C por hash, el selector no está autorizado, el request pierde identidad, o el output no está aislado. Un fallo visual no se corrige cambiando el gameplay ni reinterpretando el contrato de duración.


## Decisión operativa E0-R3

La ejecución V2 no llegó a instalar documentos (R2) aunque creó una ref local C11-E. El usuario eligió expresamente trabajar localmente en `main`. V3 se limita a instalar el overlay sobre `main`, sin cambiar refs. Riesgo: los cambios E estarán inicialmente sin commit dentro de `main`; mitigación: gates con receipts, diff exacto y no realizar cambios de código hasta cerrar/revisar E0.
