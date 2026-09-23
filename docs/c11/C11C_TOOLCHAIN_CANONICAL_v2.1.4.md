# C11-C TOOLCHAIN CANONICAL — v2.1.4

## 1. Arquitectura de almacenamiento

```text
artifacts/
├── legacy/       PROTEGIDO
├── qa/           PROTEGIDO
├── regression/  PROTEGIDO
├── releases/    PROTEGIDO
├── production/  PROTEGIDO — productos finales
├── tests/       PROTEGIDO
├── prototypes/  REGENERABLE
└── scratch/     REGENERABLE
```

`c11c_review_assets` pertenece al workspace de review y puede regenerarse de forma explícita.

## 2. Regla fundamental

**Los launchers generan. Los cleaners limpian. Production conserva.**

Ningún launcher de review debe limpiar `artifacts` automáticamente.

## 3. Herramientas canónicas

### Validación PowerShell

```powershell
.\tools\prototypes\c11c_bulk\validate_c11c_powershell.ps1
```

### Validación de entrega

```powershell
.\tools\prototypes\c11c_bulk\validate_c11c_delivery_configuration.ps1
```

### Review Art Direction 2.0

```powershell
.\tools\prototypes\c11c_bulk\run_c11c_art_direction_review.ps1 -ResetReviewAssets
```

Este comando genera 5 seeds × 5 familias = 25 renders y no limpia prototypes generales.

### Cleaner normal

```powershell
.\tools\prototypes\c11c_bulk\clean_c11c_artifacts.ps1
```

Dry-run por defecto.

Aplicar:

```powershell
.\tools\prototypes\c11c_bulk\clean_c11c_artifacts.ps1 -Apply
```

### Reset C11-C regenerable

```powershell
.\tools\prototypes\c11c_bulk\reset_c11c_artifacts.ps1 -Apply
```

Solo para empezar de cero de forma deliberada. Nunca debe tocar evidencia C11 ni producción.

### Producción

```powershell
.\tools\prototypes\c11c_bulk\run_c11c_production.ps1 -Family c11c_invisible_forces_v1 -Seed 271828
```

## 4. Reglas de producción

Producción se almacena en:

```text
artifacts/production/audiovisual/<family>/<product>/
```

Un producto final conserva como mínimo:

- MP4 final;
- manifest;
- authoring;
- FFprobe;
- Godot log;
- social sidecar;
- PRODUCT.txt;
- production manifest.

Los intermedios de captura no se publican como producto salvo que una política concreta los requiera.

No sobrescribir un producto existente salvo mediante una operación explícita de reemplazo.

## 5. Contrato de captura audiovisual

```text
width    = 720
height   = 1280
fps      = 30/1
frames   = 540 (baseline review)
duration = 18.00 s (baseline review)
ratio    = 9:16
```

Godot Movie Maker recibe la resolución como **una sola cadena**:

```text
--resolution 720x1280
```

Nunca como dos argumentos separados.

La resolución se fuerza mediante configuración temporal de captura para no modificar `project.godot` ni reabrir C11-B.

## 6. Audio

Por defecto: audio activado.

Silencioso:

```powershell
-NoSound
```

o:

```powershell
-Silent
```

Cada ejecución debe producir un solo MP4 final. El `_silent.mp4` no forma parte del output persistente.

## 7. Social sidecar

Cada render debe poder producir:

```text
*_social.txt
```

con título, descripción, familia, seed, duración, FPS, loop, audio, parámetros y comando exacto de reproducción.

El lector JSON debe tolerar BOM UTF-8.

## 8. Criterio de review

No usar review para borrar histórico ni producción.

La review se usa para observar:

- color;
- jerarquía editorial;
- impacto móvil;
- movimiento;
- identidad de familia;
- riqueza de seed;
- sensación premium;
- audio como capa ambiental.

## 9. Dirección de Arte 2.0

La siguiente fase parte de **25 vídeos físicos**.

No se cambia duración variable todavía.

No se modifica engine ni contratos congelados.

Secuencia:

```text
25 renders
→ observación
→ diagnóstico
→ contrato DA 2.0
→ implementación
→ nuevo corpus
→ comparación
```

## 10. Principio de mantenimiento

No crear nuevas familias de launchers con sufijos de versión para cambios menores.

El nombre canónico describe la función, no el historial de parches:

- `run_c11c_art_direction_review.ps1`
- `run_c11c_multiseed_bulk.ps1`
- `run_c11c_production.ps1`
- `clean_c11c_artifacts.ps1`
- `reset_c11c_artifacts.ps1`

El historial vive en changelog/documentación y en Git, no en una proliferación de scripts `v2.0.x`.
