# C11-C PRODUCER — START PROMPT
## Continuación directa del trabajo

Estamos continuando el proyecto **C11-C Producer** para:

`ChallengeEngineV01_STATELESS`

Lee y respeta todo lo siguiente antes de modificar nada.

---

## FUENTE DE VERDAD

Backend principal:
`ChallengeEngineV01_STATELESS-C11-C2.9.1.zip`

Backend de Visual Drills:
`ChallengeEngineV01_STATELESS-C11-C2.10.1.zip`

Usa el código real de esos ZIP como fuente de verdad.

No inventes APIs ni parámetros.

C11-B está congelado.

---

## BASELINE GUI

La interfaz aprobada es:

**C11-C Producer 0.4.0**

NO la rediseñes.

NO vuelvas a `c11c-studio`.

NO cambies el layout.

Mantén:
- theme luminoso;
- formulario original;
- dropdowns/cajas visibles;
- controles prioritarios sobre texto.

Todos los cambios nuevos deben entregarse como **overlay**, no como proyecto completo.

---

## TIPOS DE VÍDEO

Selector superior:

- CHALLENGES — todavía no operativo.
- VISUAL LOOPS — operativo.
- VISUAL DRILLS — en integración.

El formulario cambia según el tipo, pero el layout permanece el de 0.4.0.

---

## VISUAL LOOPS

Mapa canónico:

`geometric` → Geometric Waves → `c11c_geometric_waves_v1`

`fractal` → Fractal Bloom → `c11c_fractal_bloom_v1`

`kaleidoscope` → Sacred Symmetry → `c11c_sacred_symmetry_v1`

`particle_flow` → Living Particles → `c11c_living_particles_v1`

`vector_field` → Invisible Forces → `c11c_invisible_forces_v1`

Solo hay cinco.

No tratar Invisible Forces como sexta familia.

La variación deriva determinísticamente de:
`C11CVariationProfile.gd`

Nueva seed → posible nuevo perfil.
Misma seed → mismo perfil.

---

## VISUAL DRILLS

Familias reales:

- Tracking
- Saccade
- Pursuit
- Peripheral Scan

Parámetros actuales:

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

No inventar más.

---

## OVERLAY ACTUAL

Último overlay entregado:

`C11C_PRODUCER_DRILLS_OVERLAY_v0.1.3.zip`

Este se aplica sobre Producer 0.4.0.

---

## FALLO ACTUAL

Última prueba:

Visual Drills → Tracking
Seed `933120431`

Comando:

`run_visual_drill_production.ps1 -Family tracking -Seed 933120431 -DifficultyTier 5 -SpeedMultiplier 1.28233 -PacingMode accelerating`

Godot arranca correctamente.

Después PowerShell falla:

`La variable '$LASTEXITCODE' no se puede recuperar porque no se ha establecido.`

`FullyQualifiedErrorId : VariableIsUndefined`

Archivo:

`c11c-producer\run_visual_drill_production.ps1`

---

## TAREA INMEDIATA

Antes de tocar nada:

1. Inspecciona `c11c-producer/run_visual_drill_production.ps1`.
2. Inspecciona el launcher/generador correspondiente del backend 2.10.1.
3. Localiza todas las lecturas de `$LASTEXITCODE`.
4. Corrige únicamente el wrapper del Producer para que funcione incluso cuando PowerShell no haya establecido esa variable.
5. No modifiques el backend.
6. No modifiques mechanics.
7. No modifiques renderers.
8. No reimplementes Visual Drills.
9. Ejecuta self-test.
10. Entrega solamente un overlay con los archivos modificados.

---

## NO REPETIR ERRORES ANTERIORES

No crear otro `seed_probe.gd` complejo.

No duplicar `C11CVariationProfile.gd`.

No pasar arrays de seeds como strings a PowerShell.

No rediseñar la interfaz.

No generar un proyecto completo.

---

## OBJETIVO

Conseguir que estos cuatro flujos funcionen:

Visual Drills
→ Tracking
→ generar

Visual Drills
→ Saccade
→ generar

Visual Drills
→ Pursuit
→ generar

Visual Drills
→ Peripheral Scan
→ generar

Después comprobar que Visual Loops siguen funcionando.

Solo después se continuará con nuevas capacidades.
