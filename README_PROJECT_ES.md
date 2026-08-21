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

En 1.0.0 FIND ha sido seleccionada como candidata para una nueva familia espacial: un escáner busca un objetivo en presencia de distractores que participan en la dificultad matemática.

El contrato FIND todavía no está congelado.

MATCH queda rechazado para 1.0.0 porque exigiría una expansión prematura del transporte multi-entidad de presentación.

## RNG y determinismo

El motor usa RNG sin estado y streams semánticos. Las fixtures históricas 001–002 permanecen en RNG 1.0; las fixtures 003–006 utilizan RNG 2.0.

El sistema no permite que la aleatoriedad cosmética modifique el resultado estructural.

## Producción actual

```text
HOOK  = 2 s
GAME  = 7 s
CTA   = 2 s
TOTAL = 11 s / 660 frames @ 60 FPS
```

La factoría 0.9.0 produce manifests de provenance version 1.0 y mantiene los artefactos aislados por challenge.

## Estado actual

```text
0.6.0  HIT v1                              FROZEN
0.7.0  Production Contract Hardening      FROZEN
0.8.0  CATCH v1                            FROZEN
0.8.1  CATCH Presentation Contract         FROZEN / VALIDATED
0.9.0  Production Contract Consolidation   FROZEN / VALIDATED
1.0.0  FIND                                CONTRACT DRAFT
```

La regla de desarrollo sigue siendo:

```text
AUDIT → CONTRACT → ISOLATION → INTEGRATION → REGRESSION → BATCH → FREEZE
```
