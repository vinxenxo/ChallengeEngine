# C11-C 2.19.12 — Maintenance and Freeze Packaging

## Estado

`C11-C 2.19.12 - FINAL CONSOLIDATED ACCEPTANCE PASS` ha sido observado en la workstation Windows. El runtime y las mecánicas están cerrados. El trabajo restante es exclusivamente de organización documental, Suite/QA de operador y sellado del archivo.

## Autoridad de freeze

Usar únicamente:

`tools/maintenance/create_c11c_freeze_zip.ps1`

La Maintenance GUI expone el mismo flujo y además un botón independiente **FREEZE C11-C · DRY RUN**. El launcher de consola es:

`c11c-suite/c11c-maintenance/run_freeze_package.bat`

## Dry-run

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\maintenance\create_c11c_freeze_zip.ps1 -DryRun
```

Valida los gates sin crear ZIP ni receipt. Comprueba acceptance 2.19.12, documentación actual, raíz limpia, `build_factory.py` histórico estructuralmente válido, alias obsoletos ausentes y exclusiones de contenido. La comprobación estructural exige los marcadores reales de la implementación histórica (`FACTORY_VERSION`, `MANIFEST_VERSION`, `argparse.ArgumentParser`, `run_factory`, `run_batch` y el bloque `if __name__ == "__main__"`).

## Higiene del paquete

El freeze excluye `artifacts/`, caches de Godot/Python/editor, temporales, backups, swap/crash dumps, archives y los árboles retirados `c11c-studio` / `c11c-maintenace`.

El paquete conserva evidencia suficiente para identificarse de forma autónoma:

- `release/C11C_FREEZE_PACKAGE_MANIFEST.json`
- `release/evidence/C11C_2.19.12_ACCEPTANCE_REPORT.json`
- `release/evidence/C11-C_COMPLETE_VIDEO_REVIEW_REPORT.json`

El manifest registra hashes por archivo, SHA-256 del árbol fuente, SHA-256 de `build_factory.py` y las reglas de exclusión.

## Orden obligatorio

1. Root organization: dry-run y revisión de todas las acciones.
2. Root organization: apply, archivando y no eliminando evidencia.
3. Consolidación documental: dry-run y apply.
4. Suite/QA enfocado, parse/layout/launcher y tests afectados por la modificación de tooling.
5. `FULL_ACCEPTANCE_C11C_2.19.12.ps1` nuevamente.
6. Freeze dry-run.
7. Freeze real desde Maintenance.
8. Verificar SHA-256 del archivo y el receipt.
9. Abrir C11-D exclusivamente desde ese archivo sellado.

## Límite de seguridad

Ninguna operación pre-freeze puede cambiar mecánicas, simulación, RNG, timing truth, renderer, presentación probada, contratos C7/C9 ni la geometría lógica 540x960.

## V35.1 dry-run semantics

The documentation consolidator is filesystem-neutral during `-DryRun`: no history directory is created and no file is moved.

Before applying root organization, verify that different-SHA collisions are reported as `WOULD_ARCHIVE_CONFLICT`. This preserves both evidence copies and clears the root-cleanliness gate without overwriting canonical documentation.

