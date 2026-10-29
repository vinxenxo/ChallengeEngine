# C11-D — Política de organización documental de raíz V1

**Fecha:** 29-10-2026. **Motivo:** el snapshot `C11D_WORKING_CONTEXT_20261029_193950.zip` contenía 120 documentos/metadata candidatos en raíz, en su mayoría README de overlays históricos. La raíz estaba actuando como acumulador de recibos de paquetes.

## Política

La auditoría histórica detallada de los 118 documentos/README D observados se encuentra en `C11D_ROOT_DOCUMENTATION_SNAPSHOT_AUDIT_20261029_V1.md`. El mapa generado por el script en el checkout activo es la decisión operativa.

- Mantener `AGENTS.md` y `README.md` como puntos de entrada convencionales de raíz.
- Archivar README históricos C11-D bajo `docs/history/d/root-documentation/`, con carpetas por familia (`challenge`, `renderer`, `visual-loops`, `visual-drills`, `v2b`, `shared-production-context`, `presentation-delivery`, `acceptance`, `d10`, `continuity`, `legacy-d9_10`, `other`). No alterar su contenido.
- Si `C11D_CONTEXT_SNAPSHOT_MANIFEST.json` o `C11D_CONTEXT_SNAPSHOT_README.md` existen como archivos sueltos en el checkout, archivarlos en `docs/history/d/snapshots/20261029_193950/`. En el ZIP anterior eran metadatos generados por el empaquetador; su presencia en el ZIP no implica que existan como archivos fuente sueltos en el checkout.
- Preservar el SHA-256 de todos los documentos movidos y registrar origen, destino, tamaño, hash, acción, referencias que bloquean movimiento y motivo en `C11D_ROOT_DOCUMENTATION_MIGRATION_MAP_GENERATED.json`.
- Ejecutar primero `-PreflightOnly`; la mutación requiere invocación explícita con `-Apply`.
- El script verifica primero `AGENTS.md`, `CONTINUE.md` y el manifiesto C11-C. Si hay pins core discrepantes, se detiene.
- Cualquier documento listado por ruta en `release/C11C_FREEZE_PACKAGE_MANIFEST.json` permanece byte-for-byte en esa ruta. En el snapshot revisado esto incluye dos README D históricos de raíz; no moverlos.
- Un documento con referencias externas aún activas queda en su ubicación original y se marca `RETAIN_REFERENCED_ROOT_PATH`. No reescribir referencias ni manifiestos históricos en esta operación.
- Los `C11D_*_OVERLAY_MANIFEST*.json` mantienen su ruta porque sirven de descriptores de paquetes históricos y pueden contener paths relativos al archivo de overlay.
- No borrar contenido divergente. Si el destino ya existe con bytes diferentes, abortar; si es byte-identical, registrar la deduplicación por hash.

## Comandos operativos

```powershell
& .\tools\c11d\documentation\organize_c11d_root_documentation.ps1 -PreflightOnly
& .\tools\c11d\documentation\organize_c11d_root_documentation.ps1 -Apply
& .\tools\c11d\documentation\organize_c11d_documentation.ps1 -PreflightOnly
& .\tools\c11d\documentation\organize_c11d_documentation.ps1
```

La operación completa y el nuevo snapshot se validan con:

```powershell
& .\tools\c11d\documentation\Test-C11DDocumentationReorganization.ps1 -ApplyRootMigration -GenerateSnapshot
```

## Resultado esperado

El árbol activo conserva todas las fuentes y los pins, pero deja de mantener cientos de README sidecar de overlays en raíz. Lo movido queda como historia searchable, el mapa muestra las excepciones no migrables, y el catálogo vivo permite recuperar documentación por tema, linaje, ruta y SHA-256. Esta política no cambia `renderer=OFF`, no materializa payload/media, no cierra D9 ni concede baseline/freeze/release authority.
