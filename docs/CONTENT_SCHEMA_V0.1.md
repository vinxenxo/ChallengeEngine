# CONTENT_SCHEMA_V0.1.md — Arquitectura de Contenido y Versionado

## 1. Versionado de Arquitectura (Obligatorio)
Para garantizar la compatibilidad a largo plazo, cada desafío generado (`ChallengeDefinition`) debe declarar explícitamente sus versiones de contrato:


{
  "schema_version": "1.0",
  "engine_version": "0.1",
  "mechanic": "hit",
  "mechanic_version": "1.0",
  "video_profile": "pause_reel_8s",
  "video_profile_version": "1.0",
  "asset_family": "fam_001",
  "asset_family_version": "1.0"
}

## 2. Taxonomía de Contenido (5 Niveles de Abstracción)
Para evitar la creación de "50 juegos distintos", el motor utiliza un esquema jerárquico de abstracción.

### Nivel 1: Familia Matemática (Hardcoded en Engine)

Algoritmo base de resolución matemática (HIT, CATCH, DODGE/SAVE, MATCH, FIND, JACKPOT).

### Nivel 2: Mecánica (Clase GDScript)

Implementación física concreta (ArrowHit, KeyHit, CarParkDodge).

### Nivel 3: Tema Semántico (Metadatos)

Categorización para organización de producción (animals, scifi, sports, fantasy).

#### Subcategoría de Tema Semántico: `theme: "retro_8bit_arcade"`
- **Inspiración:** Estética visual y patrones de dificultad pixel-perfect de Atari 2600, Activision, Namco y Capcom (1978-1988).
- **Mapeo:** Utiliza las familias base existentes (`HIT`, `CATCH`, `DODGE`, `MATCH`, `FIND`, `JACKPOT`) recubiertas de assets gráficos pixel-art y paletas de color indexadas.
- **Impacto en Engine:** 0% cambios en Capa 1 y Capa 3. Inyección 100% pasiva en Capa 0 (JSON) y Capa 2 (Presentación).

### Nivel 4: Asset Family (Rutas Visuales)

Directorio que contiene los sprites, texturas y UI gráfica aplicable (fam_001, fam_002).

###Nivel 5: Challenge Concreto (JSON File)

El archivo instanciado único que cruza los 4 niveles anteriores junto con una semilla única (CHALLENGE_001.json).

## 3. Principio de Agnósticismo ("Social-Aware, Platform-Agnostic")
El motor conoce los conceptos de safe_area, hook, cta, vertical_canvas, pero desconoce completamente APIs, algoritmos, métricas de engagement o requisitos técnicos de Instagram, TikTok o YouTube.

## Addendum V2.0 — RNG Contract

`generation.rng_version` is supported with values `"1.0"` and `"2.0"`.

- `1.0`: frozen legacy compatibility for historical fixtures.
- `2.0`: semantic streams and capability-based RNG contexts.

Historical fixtures `CHALLENGE_001` and `CHALLENGE_002` remain on `1.0` and are not migrated.

`CHALLENGE_003` is the first controlled `2.0` fixture and exists to validate deterministic dependency isolation.

## Current V2.0 Content Contract

The five-level content model remains:

```text
Mathematical Family
    ↓
Mechanic implementation
    ↓
Semantic theme
    ↓
Asset family
    ↓
Concrete challenge JSON
```

V2.0 does not add new mathematical families. `parking_v2` is a V2 implementation of the `DODGE / SAVE / CONTROL` family. The visual theme `garage` is content metadata only.

Current V2.0 fixtures:

- `CHALLENGE_003` → `pilot` / `2.0` / laboratory DDI fixture.
- `CHALLENGE_004` → `parking_v2` / `2.0` / production-oriented fixture.

The challenge definition remains declarative; RNG stream allocation and algorithmic behavior are owned by the engine contracts, not by arbitrary JSON code.
