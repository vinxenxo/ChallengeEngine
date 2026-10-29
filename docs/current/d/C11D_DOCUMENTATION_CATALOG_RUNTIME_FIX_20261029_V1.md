# C11-D — Corrección del generador de catálogo documental V1

**Fecha:** 2026-10-29  
**Ámbito:** corrección localizada de `tools/c11d/documentation/organize_c11d_documentation.ps1`.

## Incidencia reproducida por el operador

El modo `-PreflightOnly` terminaba con `C11D_DOCUMENTATION_CATALOG_PREFLIGHT=PASS_NO_FILES_WRITTEN`, catalogando 791 documentos. La ejecución normal fallaba después de imprimir los pins y los contadores, con `System.ArgumentException: Los tipos de argumentos no coinciden`.

## Causa

El script creaba `$pinResults` como `System.Collections.Generic.List[object]` a través de `New-Object`, y al construir la estructura JSON la envolvía con el operador `@($pinResults)`. Windows PowerShell 5.1 presenta un fallo conocido al convertir ciertas `List[object]` así creadas con el operador de subexpresión de array. La excepción sucede antes de escribir los archivos de catálogo.

## Corrección

La propiedad `source_pins` ahora se materializa con `$pinResults.ToArray()`. Es un cambio de una sola expresión; no modifica categorización, documentos fuente, hashes, pins, ni reglas de autoridad. No mueve, renombra o elimina documentos.

## Identidad y límites

- SHA-256 del script anterior: `54edc362ffc1c98ffee75576e3c57a2842517f7f0a1a95dcef97fcd7d2303c08`.
- SHA-256 del script corregido: `b2f837d987b8b8ee37d50b6eb1f897fb57e342049d9c7ece46878396941b1575`.
- El instalador exige el hash anterior exacto o, en una segunda ejecución, el hash nuevo exacto. Un contenido diferente bloquea la sustitución.
- Los pins core de `AGENTS.md`, `.continue/rules/CONTINUE.md` y `release/C11C_FREEZE_PACKAGE_MANIFEST.json` se verifican como hard blockers; también se verifican los cinco pins de continuidad conocidos.
- No se modifican `AGENTS.md`, `CONTINUE.md`, el manifiesto canónico C11-C ni los documentos congelados.

## Verificación Windows requerida

Después de aplicar el overlay, ejecutar:

```powershell
& .\tools\c11d\documentation\organize_c11d_documentation.ps1 -PreflightOnly
& .\tools\c11d\documentation\organize_c11d_documentation.ps1
```

El resultado final esperado incluye `C11D_DOCUMENTATION_CATALOG=PASS_CATALOG_ONLY_NO_SOURCE_MOVES` y hashes para ambos catálogos. El preflight anterior fue PASS, pero la generación normal debe volver a ejecutarse para verificar la corrección. La ejecución real en Windows es la validación de aceptación de esta reparación.
