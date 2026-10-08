# C11-C Suite — Current Operator Rules

**Suite:** 0.1.4  
**C11-C:** 2.19.12  
**Producer:** 0.10.0  
**Estado:** C11-C 2.19.12 FROZEN; C11-D D9 Suite Integration/Evolution ACTIVE.

## Modelo operativo

La GUI y la línea de comandos son superficies co-iguales. La GUI debe ser una capa fina que invoque los mismos scripts canónicos que se ejecutan desde PowerShell/BAT. No se admite lógica exclusiva de GUI para generar, validar o cambiar la semántica del producto.

Superficies activas:

- `c11c-suite/c11c-test` — pruebas y QA.
- `c11c-suite/c11c-producer` — producción y review.
- `c11c-suite/c11c-maintenance` — limpieza, organización, consolidación documental y freeze.
- `c11c-suite/c11c-catalog` — catálogo e inspección de productos/artefactos.
- `c11c-suite/c11c-config` — configuración declarativa y perfiles.

`c11c-studio` está retirado. El alias mal escrito `c11c-suite/c11c-maintenace` es histórico y debe quedar archivado antes del freeze.

## Rutas canónicas actuales

Complete review:
`tools/qa/c11/run_c11c_complete_video_review.ps1 -Workers 7`

La operación normal no fuerza `-Reset`: si existe un corpus `COMPLETE`, se conserva; si falta, el propio flujo genera lo necesario.

Acceptance:
`FULL_ACCEPTANCE_C11C_2.19.12.ps1`

Freeze dry-run:
`tools/maintenance/create_c11c_freeze_zip.ps1 -DryRun`

Freeze real:
`c11c-suite/c11c-maintenance/run_freeze_package.bat`

## Limpieza

La limpieza rutinaria de media C11-C es:
`tools/prototypes/c11c_bulk/clean_c11c_artifacts.ps1`

Es allowlist-based y solo actúa sobre roots de prototype C11-C explícitos y extensiones de media regenerable. Conserva metadatos y no entra en `legacy`, `qa`, `regression`, `releases`, `production` ni `tests`.

`reset_c11c_artifacts.ps1` es destructivo y queda separado del flujo normal. No debe formar parte de Test, Review ni Freeze.

`tools/maintenance/clean-videos.ps1`, `clean-godot.ps1` y `Make_zip.ps1` son herramientas manuales/legacy y no son la autoridad de freeze.

## Freeze

`create_c11c_freeze_zip.ps1` es la única autoridad de empaquetado de C11-C. Antes de crear el archivo verifica acceptance, documentación actual, higiene de raíz, la identidad estructural de `build_factory.py` y las exclusiones de residuos/caches/archives.

El ZIP incluye dos evidencias compactas bajo `release/evidence/`: el acceptance report y el complete video review report. El árbol pesado `artifacts/` se mantiene fuera del release y permanece en la workstation como evidencia de fabricación.

## Versiones

`0.1.4` es la versión runtime de Suite. `0.10.0` es la versión activa de Producer; añade la pestaña D4 request/personalization en modo plan-only, sin activar D4.8. Una referencia como `2.16.9` en Producer puede identificar la lineage del backend certificado y no debe interpretarse como versión activa del Suite.

## D

En C11-D cada capacidad debe existir en CLI y GUI con los mismos inputs, provenance y resultados reproducibles. La paridad GUI/CLI es un invariante transversal de todos los hitos D, no un trabajo reservado para D9.

## Estado C11-D / D9

D0–D8 están PASS/CLOSED (D7 FROZEN). D9.4 PASS es un checkpoint de medios real, no el cierre global de D9. D9 sigue ACTIVE hasta actualizar y probar cada superficie existente (`c11c-producer`, `c11c-catalog`, `c11c-config`, `c11c-maintenance`, `c11c-test`) y certificar producción/reproducción real desde GUI. D10 permanece BLOCKED.

## Inventario canónico

La matriz `docs/current/suite/C11C_SUITE_TOOLING_MATRIX.md` es la referencia única para distinguir rutas activas de compatibilidad histórica y comprobar la paridad GUI/CLI.
