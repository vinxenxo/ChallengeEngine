# C11-E E6 — Reparación del adjudicador A.3 — V2

**Fecha:** 2026-11-19  
**Estado:** corrección de un defecto del runner V1; no modifica recibos fuente ni política.

## 1. Fallo observado

El recibo Windows `E6OPTCQT_20261119T204307Z_9BFC7875` conservó:

- pines C11-C, D4.8 V2, compositor V4, archivos D9/E1 y evidencias: PASS;
- benchmark evidence archive y PNG: PASS;
- Python 3.13.14, PySide6 6.11.2, Qt 6.11.2;
- A3: `BLOCKED/A3_POSTIMAGE_POINTER_MISMATCH`;
- QImage tests: 0/37, NOT_RUN; benchmark QImage: NOT_RUN;
- sin cambios de source, C11-C o D4.8 V2; sin procesos de media.

La causa está en el código del propio runner. Se comparó:

```python
transition["postimage_sha256"] == active["new_pointer_expected"]
```

El primer valor identifica el **manifiesto JSON completo** (postimage); el segundo identifica el **valor SHA almacenado en un puntero JSON concreto**. Esos hashes no pertenecen al mismo dominio.

## 2. Corrección estricta

V2 valida por separado:

1. Preimage de manifiesto completo = archivo histórico de 8,591 bytes, SHA `2075da9c33c689861a68d3bd8fb19b7ed593c6e76010ab200880746aa6d1a470`.
2. Postimage de manifiesto completo = archivo vigente de 8,591 bytes, SHA `5702092bc1c88e4b333dd30cc150f0d383cd2006121037b0198905c75a3af795`.
3. El puente V2 permite exactamente `/source_lineage/6/sha256` y el cambio instalado identifica ese único puntero.
4. El valor anterior de ese puntero se extrae del manifiesto histórico y coincide con `old_pointer_value` del puente y con expected/actual del diagnóstico.
5. El valor nuevo coincide con `new_pointer_value`, con expected/actual del diagnóstico y con SHA del archivo D9.8 `C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json` (dabb458fc2215156ddb5ebea7e8ebec811098886ce2858733ba9fb13f6075ccb).
6. Se reconstruye el manifiesto esperado copiando el histórico y reemplazando únicamente `source_lineage[6].sha256`; el JSON vigente debe ser idéntico a esa reconstrucción. Cualquier diferencia adicional bloquea.
7. Se conserva `PINNED_REPLACE`, los tamaños 8.591/8.591 bytes, el archivo histórico ADD_ONLY, el schema/status y el pin C11-C del puente, la propuesta A.3 aprobada y su archivo real, el registro operador A.3, los bloqueos D4/renderer y las incidencias históricas exactas del diagnóstico V1.
8. La fila especializada `PASS_SINGLE_POINTER_LINEAGE_RECONCILIATION` se reconoce como PASS solo tras las verificaciones anteriores. El recuento normalizado es 17 PASS literales + 1 PASS especializado = 18/18; fallos 0.

Esto es más estricto que eliminar la comparación incorrecta: incorpora reconstrucción estructural del postimage y comprueba ambos dominios de hash independientemente.

## 3. Evidencia inmutable

- Loop policy V2 SHA `5afc42ca84480ba1d025d288f2653d009e85af053fff5b62133e067a17dfb4be`; 18 checks, 17 PASS literales, 1 estado especializado, failures=0.
- A3 diagnostic V1 SHA `6a49a65b4658b119e9ed331f50296449ddb3ba248937c09eab30a3f3fc32bd4a`; se conserva sin reescritura.
- Bridge A3 SHA `aec0e387f167f4b821b7d94f06a67f78f498be939fe3cda857d20ce550819cac`.
- Historic/current manifests y modelo D9.8 fijados por el adjudicador.
- V2 genera un recibo nuevo; nunca corrige ni sobrescribe el recibo fallido V1.

## 4. Criterio de salida

A3 PASS solo habilita ejecutar los 37 tests QImage y el benchmark sintético de 7 iteraciones. Aunque QImage cumpla el presupuesto de 30 FPS, el resultado es únicamente `PASS_QIMAGE_STAGE_BENCHMARKED_NOT_END_TO_END`. No autoriza decodificación de vídeo real, Godot, FFmpeg/FFprobe, audio, mux, dispatch ni E6 acceptance.
