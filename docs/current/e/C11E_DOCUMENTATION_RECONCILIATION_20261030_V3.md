# C11-E — reconciliación de documentación y autoridad

**Versión:** V3 · **Fecha de revisión:** 2026-10-30.

## 1. Material revisado y procedencia

La revisión disponible se apoya en tres artefactos distintos:

1. `C11D_WORKING_CONTEXT_20261029_203557.zip`, SHA-256 `b6acdc0ecff427acd90b64d41cf9f295af722114d55f907ac89267411b65d987`, 9.454.969 bytes, snapshot de 3.750 entradas. Es la base del inventario documental y de la inspección de código de arquitectura.
2. `C11D_RENDER_ACTIVE_EVIDENCE_20261029_211351.zip`, SHA-256 `18c6507d38b6ae65be6298a8b5807ed4e74329c117ebe90f2dba5f6daed1f928`, 1.233.382 bytes. Es la captura histórica previa al commit local `doc catalog`; fijó `main`, HEAD `8f6905003a4dff979ed97dc2e721d1abc4375de8`, árbol limpio (`## main...origin/main`) y manifiesto C correcto. No es el HEAD actual reconciliado para E0 V2.
3. `C11D_FULL_DOCS_AND_C_TO_D_REVIEW_20261030_V1.zip`, SHA-256 `5e0d8dfa56e0ff08047bc21a70319843c1367961b4534f615b974a04ae1ee876`, 1.370.630 bytes. Contiene informe gap, índice, inventario y resumen de deduplicación.

La revisión estructural inventarió 1.507 Markdown bajo `docs/`, en 83 carpetas, 5.512.612 bytes; detectó 1.385 contenidos únicos por hash y 122 instancias de rutas duplicadas. Había 511 Markdown bajo `docs/current/d/`, 684 bajo `docs/history/` y 9 documentos raíz en el inventario. Esto es un inventario completo del snapshot, no una lectura humana palabra por palabra de los 1.507 documentos.

Se hizo lectura profunda del conjunto crítico que condiciona arquitectura C, composición/presentación, rutas físicas Challenge/Loop/Drill, Producer GUI/CLI, D9.1/D9.2, D9.5.1/D9.5.2, D9.9/D9.10, D9.14/D9.17/D10, fases de autoridad, manifests y reglas de continuación. Los documentos históricos contradictorios se conservan como historia y no prevalecen sobre los contratos más nuevos aceptados.

## 1A. Reconciliación activa E0-R1 del 2026-10-30

El usuario ejecutó la reconciliación directamente en Windows. El resultado establece:

- Checkout: `C:/Users/vinxe/Projects/ChallengeEngineV01_STATELESS`.
- Rama actual: `main`.
- HEAD actual: `bc8330e794fe37efe0c4f9c2bb0c0bd389f28f2c`.
- Único padre: `8f6905003a4dff979ed97dc2e721d1abc4375de8`; `git merge-base` devolvió `8f6905003a4dff979ed97dc2e721d1abc4375de8` y `git merge-base --is-ancestor` confirmó que la captura anterior es ancestro directo.
- Commit adicional: `doc catalog`, fechado `2026-10-30T00:57:00+01:00`.
- Únicos paths cambiados por ese commit: `docs/current/d/C11D_DOCUMENTATION_CATALOG_GENERATED.json` y `docs/current/d/C11D_DOCUMENTATION_CATALOG_GENERATED.md` (2 archivos, 4 inserciones, 4 eliminaciones).
- Árbol de trabajo y staging limpios; `main` está `ahead 1` respecto a `origin/main`.
- Manifiesto C: 796318 bytes y SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- En E0-R1 todavía no se había observado una ref E; E0-R3 posterior confirmó refs local/remota C11-E en el mismo HEAD.

Conclusión: el nuevo commit es un avance documental local esperado, no una divergencia de código. E debe partir exactamente de `bc8330e794fe37efe0c4f9c2bb0c0bd389f28f2c` para conservarlo; no hacer reset, cherry-pick ni push. El instalador V1 abortó antes de modificar el checkout, debido a su igualdad estricta con el HEAD histórico. V2 corrige la precondición y fija tanto el HEAD reconciliado como su único padre.

## 2. Clasificación de la evidencia

| Clase | Qué prueba | Qué no prueba |
|---|---|---|
| Captura activa 2026-10-29 21:14 | HEAD/branch/status, pin manifiesto C, `AGENTS.md`, `CONTINUE.md`, `main.py`, `c11d_gui_request.py`, Test BUILD_MANIFEST y fuentes incluidas en slice | Estado del checkout después de la captura; todos los core files no incluidos en el slice |
| Snapshot 20:35 | Contenido completo del repo/documentación de ese snapshot, source hashes y estructura | Que todos sus archivos sigan iguales en el disco Windows a 21:14 o después |
| Inventario Markdown | Cobertura de rutas, tamaños, hashes, duplicados, títulos y headings del snapshot | Revisión semántica manual integral de cada línea |
| Histórico de pilotos | Que existieron pilotos físicos D9.1/D9.2/D9.14 reportados en su evidencia | Que el formulario universal D9.9 alimente píxeles en la ruta actual |

### Pines fuente inspeccionados

La siguiente tabla conserva los SHA-256 del informe de gap anterior. `ACTIVO` significa cotejado contra el slice capturado; `SNAPSHOT` significa que el hash pertenece al snapshot 20:35 y debe recalcularse en el checkout E antes de usarlo como pin de parche.

| Ruta | SHA-256 | Bytes | Clase |
|---|---|---:|---|
| `core/presentation/C11CVisualEditorialLayer.gd` | `f8f718c067a4d7a088cc16f244cc40209e7183bec93e44d8cb66eb6dd404cf7d` | 19047 | SNAPSHOT |
| `core/presentation/rendering/VisualContentPlayer.gd` | `58d86d56ebd7507c9e800c83010103b9be12f1b5dca9356da61ca623e4cf0145` | 13876 | SNAPSHOT |
| `core/presentation/ChallengePresentationBinder.gd` | `755ecfc9cc6e1ee51738938583217ab8a470c1a1f290bb107e91e19990d74b47` | 6954 | SNAPSHOT |
| `core/presentation/VisualLoopPresentationBinder.gd` | `96abc0fe4361f88ba9b388a7bce18541a65c9b7334549ebb7c707e1cb76c513b` | 1895 | SNAPSHOT |
| `core/presentation/VisualDrillPresentationBinder.gd` | `cb6acc408252b8b794177d8f5923a3b151646eebdfd1efe9a30fdd6221de82c0` | 11830 | SNAPSHOT |
| `core/presentation/UnifiedSocialFrame.gd` | `d80c07103f56a2abfe34be60547285e61b0d03b50a5ed93c3c72d4241f6585ba` | 2087 | SNAPSHOT |
| `core/presentation/PresentationProfile.gd` | `187b1cf8ab96b9031785a0f36b0054a60383c97cb3d81906c7d9bbcd373bef24` | 8837 | SNAPSHOT |
| `tools/c11d/d9/universal_producer.py` | `9ad2adbf54946f2225ae2ed36b88abfc5717387f2ff03bbed684aa8bd32d87d1` | 19692 | SNAPSHOT |
| `tools/c11d/d9/universal_editorial_model.py` | `5c575be1942ba0613d66579d14db5cf9d7786e7062dfb001bd7be8a2e9c18ae5` | 26574 | SNAPSHOT |
| `tools/c11d/d9/editorial_render_bridge.py` | `fe9d40052b0f4ff6f1c862c010ae7b3b13070b6ce935be6d62f9dcaec63a644a` | 10868 | SNAPSHOT |
| `tools/c11d/d9/d_render_adapter.py` | `222742677cd498368429a3ec0dcdd922c44197bb5ada3638081138fb77c31bf1` | 15051 | SNAPSHOT |
| `tools/c11d/d9/shared_production_context_service.py` | `9726bf3ceeb3f567da350789f70750f9206caaf707523e4d53217e16f73f0aac` | 17069 | SNAPSHOT |
| `tools/c11d/d3/c11d_music_engine_v5.py` | `69ebcf96f47360ceea60568ec52f5ef44d2516c7aa14be8452817d7fab79a402` | 4373 | SNAPSHOT |
| `c11c-suite/c11c-producer/main.py` | `1af78a2199f404276d0a459d9e6daec8b3cceb0d1d325b79a7d41840bc6c241e` | 96257 | ACTIVO |
| `c11c-suite/c11c-producer/c11d_gui_request.py` | `0e95109ffd3ba5655d28292309196349470ab7958a467f096543a2c98c22976e` | 9183 | ACTIVO |
| `c11c-suite/c11c-test/BUILD_MANIFEST.json` | `b56fe484858a8a8fca04ba6a5f197c56160bd4ee6d0170b104855f829c9b7e36` | 10125 | ACTIVO |
| `tools/c11d/d9/run_d9_2_audio_enabled_pilot.ps1` | `b1fe158cf80c83825bcdd819cb92b595f18473d1cdce9fad6f57a70e830d1364` | 16263 | ACTIVO |

Hashes verificados por coincidencia entre slice activo y snapshot: `AGENTS.md` (`0d4565e...d3016b37`), `.continue/rules/CONTINUE.md` (`52776e...4145ac86`), `c11c-suite/c11c-producer/main.py` (`1af78a...c6c241e`), `c11d_gui_request.py` (`0e9510...22976e`) y `c11c-suite/c11c-test/BUILD_MANIFEST.json` (`b56fe4...9b7e36`). El manifiesto C está verificado directamente por el reporte de captura: SHA `e405d0...b4b953`, bytes 796318.

Los core binders y varias fuentes D fueron inspeccionados en el snapshot; no se presentan aquí como hashes verificados contra el slice vivo de 21:14. E0 y los gates posteriores vuelven a fijar los pins desde el checkout activo.

## 3. Diagnóstico documental/arquitectónico heredado

- C ya proporciona generadores y rutas físicas por familia, binders, perfiles, compositor social, Godot Movie Maker y tooling FFmpeg/FFprobe.
- D separó formularios/requests, modelo universal, resolver, bridge y adapter, pero el bridge/adapter investigado emite envelope `PREPARE_ONLY` y declara `renderer_input_emitted=false` y `renderer_dispatch_invoked=false`.
- El gap principal no es falta de motor: es la ausencia del transporte comprobado de campos editoriales desde la solicitud normalizada hasta el slot/modelo visual consumido en los frames físicos.
- La auditoría anterior detectó 14 campos editoriales declarados en plan/review y 0/14 consumidos en el payload visual auditado. E debe volver a medir la matriz campo×familia×fase; ese 0/14 es hallazgo D del scope revisado, no un número universal de cualquier future branch.
- Los módulos `shared_production_context_service.py` y adapters GUI/CLI ya existen en el snapshot; su presencia no prueba que el Producer actual los invoque ni que despachen render. No aplicar el ZIP histórico `C11D_SHARED_PRODUCER_PREPARATION_SERVICE_20261030_V2.zip` sin reconciliación; la recomendación técnica previa fue no duplicar este servicio.

## 4. Nueva jerarquía documental E

En el workstream C11-E ejecutado sobre la rama local `main`:

1. `AGENTS.md` y `.continue/rules/CONTINUE.md` dirigen a E.
2. `docs/current/e/README.md` fija el orden de lectura.
3. Carta E, contrato de arquitectura, gates, registro de decisiones/riesgos y runbook E0 son autoridad activa del desarrollo E.
4. Contratos C11-C congelados y documentos vigentes C continúan siendo autoridad de C para motor, mecánica, composición y entrega donde se reutilizan.
5. Documentación D no editada constituye evidencia histórica/scoped de lo que D hizo, no una prohibición operativa universal para E.
6. Documentos en `docs/history/` y snapshots permanecen inmutables. No se borran duplicados por suposición, porque pueden estar referenciados por manifests/receipts.

## 5. Qué se actualiza ahora

El overlay crea el árbol `docs/current/e/` con carta, arquitectura, gates, revisión documental, runbook y registro de decisiones; añade prompt de continuidad; conserva copia pre-E de `AGENTS.md` y `CONTINUE.md` en `docs/history/c11d/`; y reemplaza esos dos archivos de enrutamiento para que el checkout `main` enrute al workstream E sin perder las instrucciones históricas D.

No reescribe los 1.507 documentos históricos, no reubica el inventario D, no cambia C11-C ni el catálogo de artefactos previos. Esta decisión evita destruir referencias y evita presentar como verificados contra el checkout actual documentos cuyos hashes solo se conocen del snapshot.

## 6. Conflictos resueltos para E

| Conflicto histórico | Resolución E |
|---|---|
| D renderer OFF / media_created=false | Se conserva como estado histórico D. E podrá crear dos outputs Challenge bajo E2 y outputs Loop/Drill bajo E4, siempre con roots de prueba aislados y recibos propios. |
| D9.10 PREPARE_ONLY | No se eleva a renderer. E construye/invoca su propia ruta de producción después de probar el servicio y el consumidor. |
| C11-C inmutable mientras D se aprueba | C11-C permanece protegido también durante E. El trabajo C11-E sobre `main` no altera el freeze package; reemplazo solo tras aceptación formal E8. |
| Reutilizar D3 ya probado vs audio no integrado en request universal | Se reutiliza motor D3 tras validar API; audio y mux tienen gate E3 separado. |
| Contradicción de CH_008/009 11 s vs 12 s | Se excluyen de las primeras pruebas/matrices que dependan de su duración hasta resolverla explícitamente. |
| Cinco superficies suite y una API GUI/CLI | Se conservan; E no crea sexto módulo ni productores paralelos. |

## 7. Límites de esta revisión

No se dispone de acceso directo al disco Windows en esta sesión. Los artefactos fueron materializados y leídos; no se aplicó el overlay. Los hashes de código snapshot-only no sustituyen una verificación activa de los ficheros antes de modificar código. El primer paso ejecutable es E0 sobre el checkout Windows.


## Addendum V3 — E0-R2/R3 y política de rama local

La ejecución V2 mostró preflight PASS y `git switch -c c11e-unified-editorial-production`, pero no una aplicación del overlay. E0-R2 encontró el checkout en `main`/`bc8330e`, sin documentos E, copias históricas ni receipt. E0-R3 confirmó refs local y remota `c11e-unified-editorial-production` en `bc8330e`, con `main` activa y árbol limpio. El usuario eligió explícitamente continuar localmente en `main`. Por tanto, C11-E se trata como workstream lógico aplicado en `main`; no se cambian ramas ni refs. El V3 instala los documentos de forma add-only y deja los cambios locales sin commit, con receipt externo.
