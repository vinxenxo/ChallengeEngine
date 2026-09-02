# ChallengeEngineV01 — ¿Qué estamos construyendo?

Estamos construyendo una **fábrica automática de vídeos de retos de precisión**: el vídeo ejecuta una situación matemática y el espectador intenta pausar en el frame ganador.

No es un videojuego tradicional. La lógica del reto, la presentación y la producción están separadas para poder generar situaciones repetibles y escalables.

## Familias matemáticas actuales

```text
HIT
CATCH
DODGE / SAVE / CONTROL
```

El motor también contiene fixtures de laboratorio como `pilot` y `key`, que sirven para preservar y validar contratos históricos.

### HIT

Problemas de convergencia o impacto respecto de un objetivo. `hit_v1` es matemáticamente soberano.

### CATCH

Dos trayectorias móviles convergen sin feedback reactivo. `catch_v1` es matemáticamente soberano y utiliza el contrato de presentación:

```text
FrameSnapshot.position
    → catcher
FrameSnapshot.custom_data["target_position"]
    → target
```

### DODGE / SAVE / CONTROL

Familia de trayectoria continua. `parking_v2` es su implementación de producción actual.

### FIND — siguiente familia

FIND se integró como la quinta familia matemática activa en el checkpoint 1.0.0 y dispone de fixture productivo (`CHALLENGE_007`) y suite de aislamiento.

Además, el repositorio C6 incorpora fixtures/puntos de integración experimentales para `choose_v1` y `count_v1` (`CHALLENGE_008` y `CHALLENGE_009`). Estos no deben confundirse con nuevos contratos matemáticos congelados: su presencia actual certifica disponibilidad de pipeline/presentación, no una nueva congelación de core.

## RNG y determinismo

El motor usa RNG sin estado y streams semánticos. Las fixtures históricas 001–002 permanecen en RNG 1.0; las fixtures 003–006 utilizan RNG 2.0.

El sistema no permite que la aleatoriedad cosmética modifique el resultado estructural.

## Producción actual

La composición temporal es declarativa por challenge:

```text
HOOK / GAME / REVEAL / CTA
0 s  = fase omitida
>0 s = fase activa
GAME > 0 siempre
```

El perfil histórico `2 + 7 + 2 = 11 s` sigue siendo un fixture de referencia, pero ya no es una restricción global. C6-D4 permite generar vídeos de distinta composición temporal sin alterar la simulación.

La factoría 0.10.0 mantiene manifests de provenance 1.0, calcula `total_frames` desde el JSON y valida físicamente el resultado con FFprobe.

## Estado actual

```text
0.6.0  HIT v1                              FROZEN
0.7.0  Production Contract Hardening      FROZEN
0.8.0  CATCH v1                            FROZEN
0.8.1  CATCH Presentation Contract         FROZEN / VALIDATED
0.9.0  Production Contract Consolidation   FROZEN / VALIDATED
1.0.0  FIND v1 + CHALLENGE_007              FROZEN / VALIDATED
1.1.0-C6-D4 Phase Duration Control         CODE COMPLETE / E2E PENDING
```

La regla de desarrollo sigue siendo:

```text
AUDIT → CONTRACT → ISOLATION → INTEGRATION → REGRESSION → BATCH → FREEZE
```


## Documentación viva

La continuidad y el estado de release se encuentran en `MASTER_HANDOVER_CHECKPOINT_1.1.0-C6-D4.md`. El mapa de documentación vigente está en `docs/DOCUMENTATION_STATUS_1.1.0-C6-D4.md` y el roadmap en `docs/ROADMAP_PHASES.md`.
