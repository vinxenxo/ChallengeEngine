# C11-D — Índice documental y política de archivo V3

**Fecha:** 29-10-2026. **Objetivo:** cerrar la limpieza documental de raíz y entregar el siguiente contexto directamente a ingeniería de integración de render. **Este documento navega; no cambia contratos, pins ni autoridad.**

## 1. Fuentes y artefactos de continuidad

La fuente de verdad para cambios es el checkout Windows activo `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`, no un ZIP subido ni su manifiesto interno. El snapshot verificado de referencia inmediatamente anterior a esta reorganización es `C11D_WORKING_CONTEXT_20261029_193950.zip`, commit declarado `be5d04c64080723e5f53d651109e45db07c43054`, SHA-256 `5b8d06ad82bca798c94db03f943a85afb309d91484d4499ed40fed36056ca774`.

El paquete anterior es estructuralmente válido como contexto: 9.190.399 bytes, CRC limpio, 3.721 entradas únicas, inventario interno conciliado, y `release/C11C_FREEZE_PACKAGE_MANIFEST.json` una sola vez con 796.318 bytes y SHA-256 canónico `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. Es antecedente, no el snapshot final de la siguiente ventana. La nueva ventana debe usar el nuevo snapshot generado por `Test-C11DDocumentationReorganization.ps1 -ApplyRootMigration -GenerateSnapshot` y validar su `.sha256` y `.report.json`.

## 2. Orden de autoridad y lectura

1. Checkout activo, evidencia operador local y hashes actuales.
2. `AGENTS.md` y `.continue/rules/CONTINUE.md`.
3. Manifiesto congelado C11-C `release/C11C_FREEZE_PACKAGE_MANIFEST.json`, siempre inmutable.
4. Ledger V18, Checkpoint V41 y paquete de decisión AD (closeout, receipt y operator authority decision gate); verificar hashes contra el checkout, no sobrescribir versiones más recientes desde el snapshot.
5. Este índice V3, el catálogo vivo, el mapa generado de migración de raíz, el plan funcional V3 y el orden de lectura V3.
6. Contratos D por dependencia funcional: D9.8 modelo/resolver editorial; D9.9 request/plan y productor universal; D9.10 bridge/adapter `PREPARE_ONLY`; binder/materialización request-scoped; payload/frame-program/composición; identidad y semántica visual; región y timebase; D3 música y delivery/mux.
7. Entrypoints de producción C en `tools/qa/c11/`, `tools/prototypes/c11c_bulk/` y `c11c-suite/`; seguir los comandos reales sin suponer que una ruta D plan-only genera vídeo.
8. `docs/history/d/root-documentation/`, `docs/history/d/snapshots/`, `docs/history/c11d/`, `docs/history/master-prompts/c11d/` y documentación versionada antigua: contexto histórico, nunca autoridad por el simple hecho de tener una versión más alta o más reciente.

## 3. Catálogo vivo y organización de raíz

`docs/current/d/C11D_ROOT_DOCUMENTATION_SNAPSHOT_AUDIT_20261029_V1.md` inventaría los 118 README/documentos D que se observaron en raíz en el snapshot anterior, sus familias de destino y excepciones. El preflight de la herramienta operativa vuelve a comprobar el estado del checkout actual; el informe histórico no sustituye ese resultado.

`tools/c11d/documentation/organize_c11d_documentation.ps1` genera:

- `docs/current/d/C11D_DOCUMENTATION_CATALOG_GENERATED.md`
- `docs/current/d/C11D_DOCUMENTATION_CATALOG_GENERATED.json`

El catálogo cubre `docs/current/d`, los árboles históricos D relevantes, `prompts`, `docs/master-prompts` y la documentación/metadata C11-D que permanezca en raíz. Incluye ruta, título, categoría, linaje, tamaño y SHA-256. No afirma supersesión por nombre o versión.

`tools/c11d/documentation/organize_c11d_root_documentation.ps1` ejecuta una migración física conservadora de los README de overlay y documentos C11-D heredados de raíz a `docs/history/d/root-documentation/<categoría>/`, además de los metadatos de snapshot previo a `docs/history/d/snapshots/20261029_193950/`. Tiene preflight sin escritura y ejecución explícita con `-Apply`; preserva byte por byte los archivos que mueve y genera:

- `docs/current/d/C11D_ROOT_DOCUMENTATION_MIGRATION_MAP_GENERATED.md`
- `docs/current/d/C11D_ROOT_DOCUMENTATION_MIGRATION_MAP_GENERATED.json`

No se mueven `AGENTS.md` ni `README.md`. No se mueven archivos incluidos por ruta en el manifiesto C11-C; dos README históricos de D permanecen por esta restricción. También permanecen en raíz los archivos cuya ruta aún es referenciada por fuentes/manifiestos del checkout. Son excepciones explícitas que aparecen en el mapa, no una migración incompleta encubierta. Los JSON `C11D_*_OVERLAY_MANIFEST*.json` se conservan en sus rutas originales porque describen paquetes históricos con rutas relativas propias.

No se reescribe el contenido de los documentos históricos para hacerlos encajar en la nueva estructura. Una futura migración de referencias, si llega a ser necesaria, es una operación distinta y debe preservar los pins y los registros de decisión.

## 4. Situación de gobernanza que sigue activa

- El manifiesto C11-C sigue inmutable: SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`, 796.318 bytes.
- Phase AD: paquete de decisión verificado 60/60 y verificador estructural PASS, pero la decisión de operador sigue `PENDING_EVIDENCE_OR_KEEP_BLOCKED`; evidencias de autoridad = 0, decisiones adjudicadas = 0, adopción de política = NONE.
- `renderer=OFF`; D9.10 `PREPARE_ONLY`; D4.8, D9.14 y D9.16 bloqueados; D9.17 `BLOCKED_NO_GO`; D10 bloqueado; baseline approval ausente; freeze ineligible; `release_authority=NONE`.
- R-08/R-09: 11 s declarados frente a suma de fases de 12 s. `CHALLENGE_008/009` continúan excluidos hasta resolución explícita.

La autorización general para avanzar hacia render significa que el análisis/código/test permitidos deben continuar sin pausas de aprobación rutinarias. No reemplaza una decisión de política/autoridad requerida por el gate concreto y no concede permiso para producir un MP4 D mientras las compuertas sigan bloqueadas.

## 5. Qué es y no es el snapshot

El snapshot generado por `tools/c11d/packaging/New-C11DWorkingSnapshot.ps1` es una copia filtrada del árbol activo, con inventario interno, hash de árbol definido por el script, SHA-256 externo y reporte. Excluye `artifacts` salvo evidencia compacta allowlisted, cachés/builds, medios binarios, temporales, credenciales y archivos comprimidos anidados; límite por archivo y por ZIP. No es freeze, release, backup restaurable ni autorización de render. La prueba independiente es `tools/c11d/packaging/Test-C11DWorkingSnapshot.ps1`.

Para preparar el siguiente contexto, el flujo de test debe ejecutar, en este orden, migración de raíz, catálogo, preflight de snapshot, generación del snapshot y validación independiente del ZIP. El archivo final que se suba a la nueva ventana debe acompañarse de `.sha256` y `.report.json`.

## 6. Próximo paso funcional; no más preparación documental

La siguiente ventana debe validar el snapshot nuevo, verificar los pins del checkout y continuar la inspección técnica del seam C→D. Debe seguir `C11D_RENDER_INTEGRATION_READ_ORDER_20261029_V3.md`, consultar el catálogo solo para navegar y producir un mapa breve con paths/hashes reales de:

`GUI/CLI → servicio canónico → request/perfil/selector → resolución editorial → binding/materialización → visual payload/frame program → compositor → renderer → D3 music → delivery/mux → MP4/receipt`.

Contrastar ese grafo con los runners C reales y el método `GENERAR` de Producer; escoger el primer consumer visual ausente y el cambio mínimo D-only. No abrir otra fase genérica de preparación, no reabrir AD rutinariamente ni derivar aceptación física de un PASS estático.

## 7. Invariantes inmutables

No modificar C11-C congelado; no alterar `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, RNG ni las mecánicas. `winning_frame` es el ancla temporal; `close_calls` cuenta episodios. `request.seed` y `request.music_seed` son dominios separados. Conservar cinco superficies (`c11c-test`, `c11c-producer`, `c11c-catalog`, `c11c-config`, `c11c-maintenance`); no crear `c11d-control`, `c11c-studio` ni una sexta superficie. Registrar comandos, versión de herramientas, exit codes reales y hashes de logs/evidencia.
