# C11-C PRODUCER — MASTER HANDOVER
## Continuidad de proyecto — 2026-09-25

### 1. OBJETIVO

Proyecto: `ChallengeEngineV01_STATELESS`

Herramienta actual: **C11-C Producer**

Objetivo inmediato: una GUI Windows pequeña y fiable para generar producción audiovisual a partir del backend C11-C existente.

Principio:
> El Producer es una capa fina de UI/orquestación. No reimplementa ni modifica la lógica del backend.

La antigua aplicación `c11c-studio` queda descartada como base de desarrollo. NO reutilizar su arquitectura.

---

## 2. FUENTES DE VERDAD DEL BACKEND

Backend principal:
`ChallengeEngineV01_STATELESS-C11-C2.9.1.zip`

Backend de referencia específico para Visual Drills:
`ChallengeEngineV01_STATELESS-C11-C2.10.1.zip`

Regla:
1. Código real del ZIP correspondiente.
2. Documentación de ese backend.
3. Documentación histórica solo como apoyo.
4. Nunca inventar APIs, parámetros, familias o launchers.
5. C11-B permanece CLOSED / CERTIFIED / FROZEN.

---

## 3. BASELINE APROBADO DEL PRODUCER

**C11-C Producer 0.4.0**

Es la interfaz aprobada por el usuario.

NO rediseñar el layout.

NO volver a crear C11-C Studio.

NO añadir dashboards complejos.

El usuario indicó expresamente:
- conservar la interfaz de Producer 0.4.0;
- theme luminoso;
- dropdowns/cajas visibles;
- priorizar controles sobre texto de ayuda;
- cambios futuros mediante overlays pequeños.

La forma de distribución preferida es:
**overlay con solo archivos nuevos/modificados**, copiable sobre la raíz del proyecto.

No entregar proyectos completos salvo petición expresa.

---

## 4. INTERFAZ CONGELADA

Flujo de formulario:

TIPO DE VÍDEO
→ FAMILIA
→ SUBFAMILIA
→ CANTIDAD
→ SEEDS
→ OPCIONES
→ PARÁMETROS
→ GENERAR

El selector superior de tipo de vídeo fue añadido sin cambiar el layout.

Tipos conceptuales:
- CHALLENGES — todavía no operativo.
- VISUAL LOOPS — operativo.
- VISUAL DRILLS — integración en progreso.

Cuando cambia el tipo, el formulario debe adaptarse, manteniendo el mismo layout base.

---

## 5. VISUAL LOOPS — MAPA CANÓNICO

Existen exactamente cinco familias.

| technical_id | artistic_name | production_id |
|---|---|---|
| geometric | Geometric Waves | c11c_geometric_waves_v1 |
| fractal | Fractal Bloom | c11c_fractal_bloom_v1 |
| kaleidoscope | Sacred Symmetry | c11c_sacred_symmetry_v1 |
| particle_flow | Living Particles | c11c_living_particles_v1 |
| vector_field | Invisible Forces | c11c_invisible_forces_v1 |

IMPORTANTE:
- `kaleidoscope = Sacred Symmetry`
- `particle_flow = Living Particles`
- `vector_field = Invisible Forces`
- Invisible Forces NO es una sexta familia.

Árbol:
VISUAL LOOPS
├── geometric → Geometric Waves
├── fractal → Fractal Bloom
├── kaleidoscope → Sacred Symmetry
├── particle_flow → Living Particles
└── vector_field → Invisible Forces

Esta tabla technical_id → artistic_name → production_id debe considerarse canónica para el Producer.

---

## 6. VISUAL LOOPS — VARIACIÓN

Fuente real:
`tools/prototypes/c11c_common/C11CVariationProfile.gd`

La seed determina de forma determinista:
- grammar / subfamilia;
- palette;
- parámetros numéricos específicos de la familia.

Por tanto:
`familia + seed` → perfil determinista.

Una seed nueva puede producir otro perfil.
La misma seed debe reproducir el mismo perfil.

Modo recomendado:
**ALEATORIO (seed)**

NO copiar las matemáticas de `C11CVariationProfile.gd` a Python.

Los launchers de producción deben seguir siendo los canónicos del backend.

Producción single:
`tools\prototypes\c11c_bulk\run_c11c_production.ps1`

Producción bulk:
`tools\prototypes\c11c_bulk\run_c11c_production_bulk.ps1`

---

## 7. VISUAL DRILLS — MAPA ACTUAL

Fuente específica:
`ChallengeEngineV01_STATELESS-C11-C2.10.1.zip`

Existen cuatro tipos/familias reales:

VISUAL DRILLS
├── Tracking
├── Saccade
├── Pursuit
└── Peripheral Scan

Controles documentados en el trabajo actual:

Tracking:
- Difficulty Tier
- Speed Multiplier
- Pacing Mode

Saccade:
- Difficulty Tier
- Speed Multiplier

Pursuit:
- Difficulty Tier
- Speed Multiplier

Peripheral Scan:
- Difficulty Tier

NO inventar parámetros adicionales.

La seed sigue participando en la variación determinista.

La documentación/versiones revisadas indican la presentación común de Visual Drills con 720×1280 y 30 FPS, incluyendo countdown y CTA final según el estado correspondiente del backend.

---

## 8. ESTADO ACTUAL DEL OVERLAY DE DRILLS

Último overlay entregado:
`C11C_PRODUCER_DRILLS_OVERLAY_v0.1.3.zip`

Aplicado sobre Producer 0.4.0.

Objetivo:
- añadir Visual Drills al selector de tipo;
- adaptar el formulario a Tracking/Saccade/Pursuit/Peripheral Scan;
- mantener el layout de 0.4.0;
- mantener theme luminoso;
- usar backend real;
- entregar solo overlay.

El overlay debe considerarse el punto de partida actual.

---

## 9. ÚLTIMO ERROR DE RUNTIME PENDIENTE

Última prueba del usuario:
Visual Drills → Tracking
Seed: `933120431`

El Producer lanzó:

`powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS\c11c-producer\run_visual_drill_production.ps1 -Family tracking -Seed 933120431 -DifficultyTier 5 -SpeedMultiplier 1.28233 -PacingMode accelerating`

Godot arrancó correctamente.

Después falló el wrapper:

`La variable '$LASTEXITCODE' no se puede recuperar porque no se ha establecido.`

`FullyQualifiedErrorId : VariableIsUndefined`

Archivo:
`c11c-producer\run_visual_drill_production.ps1`

Interpretación:
- el Producer llega al wrapper;
- Godot es invocado;
- el fallo pendiente está en el wrapper PowerShell del Producer;
- NO asumir que sea un fallo del backend 2.10.1;
- NO tocar mechanics/renderers/authoring del backend para resolverlo.

Siguiente paso obligatorio:
1. Leer el `run_visual_drill_production.ps1` real del overlay.
2. Identificar todas las consultas a `$LASTEXITCODE`.
3. Hacerlas robustas cuando no exista la variable.
4. Mantener exactamente el código/launcher backend.
5. Ejecutar self-test.
6. Entregar SOLO overlay.

---

## 10. ERRORES HISTÓRICOS A NO REPETIR

### Seed arrays
El GUI tuvo problemas pasando `-Seeds` a PowerShell mediante QProcess.

Aprendizaje:
- no pasar arrays como strings a un binder `Int32[]`;
- para producción, preferir invocar producto por producto con `-Seed` escalar;
- no inventar una sintaxis paralela al launcher canónico.

### seed_probe.gd
Hubo errores propios:
- `Constructor cannot return a value.`
- `Cannot infer the type of "n" variable because the value doesn't have a set type.`

Causa:
el Producer estaba intentando hacer demasiado parsing/reimplementación en GDScript.

Regla:
> Si el backend ya contiene la lógica, consultarlo directamente. No duplicarla.

### GUI Studio
La aplicación anterior se complicó excesivamente:
- demasiado menú;
- demasiado dashboard;
- demasiados servicios;
- múltiples bugs de cableado y argumentos.

Queda descartada como arquitectura.

---

## 11. REGLAS DE AISLAMIENTO

Producer NO modifica:
- C11-B;
- RNG;
- SimulationResult;
- winning frame;
- close_calls;
- matemáticas C11-C;
- familias;
- mechanics;
- renderers;
- C11CVariationProfile.gd;
- VisualAuthoringGenerator.gd;
- contratos C7;
- contratos C9.

Solo puede:
- leer;
- seleccionar;
- planificar;
- construir comandos;
- ejecutar launchers;
- presentar resultados.

---

## 12. DISTRIBUCIÓN DE PARCHES

Cada cambio nuevo:
- debe ser un overlay;
- solo archivos nuevos/modificados;
- rutas relativas desde la raíz del proyecto;
- README corto;
- self-test cuando proceda;
- no incluir el backend completo;
- no incluir ZIP completo del proyecto.

---

## 13. OBJETIVO INMEDIATO

Secuencia:

1. Corregir `$LASTEXITCODE` de Tracking.
2. Probar Tracking en Windows.
3. Probar Saccade.
4. Probar Pursuit.
5. Probar Peripheral Scan.
6. Verificar que Visual Loops siguen funcionando.
7. Mantener Challenges sin implementar hasta que Drills y Loops estén sólidos.

---

## 14. PRINCIPIO DE CONTINUIDAD

Siempre empezar por inspeccionar el código real del backend/overlay antes de escribir código.

Prioridad:
**backend real > documentación > inferencia**

Y:
**funcionalidad ya aprobada > rediseño**

No cambiar la interfaz aprobada salvo petición explícita.
