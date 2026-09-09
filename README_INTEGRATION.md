# ChallengeEngineV01 — Integración y validación

## Estado de la foundation C6-F0.3

```text
C6-F0.3.1  CLOSED
C6-F0.3.2  CLOSED / CERTIFIED
C6-F0.3.3  CLOSED / CERTIFIED
C6-F0.3.4  CLOSED / CERTIFIED
C6-F0.3.5  IMPLEMENTED / TARGETED RUNTIME PASS / FULL CERTIFICATION PENDING
```

Godot objetivo: `4.7.1-stable (official)`
Factory: `0.10.0`
Manifest schema: `1.0`

## Runtime boundary

```text
Domain-specific definition
   ↓
ContentRuntimeRegistry
   ↓
exact (kind, subtype) / fail-closed
   ↓
ContentRuntime
   ├── ChallengeRuntime
   ├── VisualLoopRuntime
   └── VisualDrillRuntime
   ↓
RenderedFrameStream
   ↓
Presentation / Rendering
   ↓
Export
```

No se introduce un `ContentDefinition` universal. `ContentEnvelope` continúa siendo visual-only.

## Suite de F0.3.5

```text
godot --headless --path . --script tests/C6F035ContentRuntimeBoundaryTest.gd
```

La suite también está registrada en `tests/run_all.py`.

## Validación global

```text
godot --headless --path . --editor --quit
python tests/run_all.py
```

## Producción batch

```text
python build_factory.py --batch ./challenges --output ./output --workers 1
```

Cuando el cambio afecta render/export, el cierre exige inspección del artefacto físico y verificación con FFprobe.

## Evidencia de ejecución y reparación

La ejecución externa del runtime boundary de F0.3.5 dio `PASS`. La integración posterior expuso una regresión CTA causada por la recuperación de una versión antigua de `ChallengePresentationBinder.gd`; este paquete restaura los defaults históricos y registra/incluye la suite CTA. Deben ejecutarse de nuevo la suite CTA, el corpus completo y la factoría antes de cerrar F0.3.5.

## Evidencia heredada

El baseline inmediatamente anterior aportó:

```text
CTA regression suite  PASS
Global corpus         53/53 PASS
Factory batch         9/9 PASS
```

Estas cifras permanecen como evidencia del baseline certificado anterior; no se etiquetan como certificación de F0.3.5.

## Fuente de continuidad

```text
docs/C6-F0.3_MULTI-CONTENT-TEMPORAL-RUNTIME-FOUNDATION.md
docs/MASTER_HANDOVER_CHECKPOINT_C6-F0.3.5_IMPLEMENTED_PENDING_EXECUTION.md
```
