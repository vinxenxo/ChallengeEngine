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