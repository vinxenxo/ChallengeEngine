# ChallengeEngineV01_STATELESS — C11-C Visual Drills

## Estado vigente

**C11-C 2.9.0 — Visual Drill polish + shared usability layer + Pursuit/Peripheral completion.**

C11-B permanece **CLOSED / CERTIFIED / FROZEN**. C11-C trabaja exclusivamente en authoring/presentation/production layers compatibles con los contratos congelados.

### Visual Drill families

| Familia | Estado mecánico | Presentación vigente |
|---|---|---|
| Tracking | seeded Lissajous + growing history | 21 s gameplay / 27 s total |
| Saccade | seeded polar jumps + counter | 17 s gameplay / 23 s total |
| Pursuit | uniform cubic B-spline + arc-length authoring + sizygia/camouflage | 17 s gameplay / 23 s total |
| Peripheral Scan | polar/logistic event schedule + threat/distractor answer sheet | 17 s gameplay / 23 s total |

Todas usan 540×960 lógico → 720×1280 físico a 30 FPS, countdown 3 s y END_CTA 3 s.

## C11-C terminal CTA

Visual Drills reutilizan el `CTAComponent` común de Challenge, pero lo montan en **Header**. Durante `END_CTA` se oculta el `FooterRegion` completo para evitar el fondo residual de la fase de gameplay.

Texto vigente:

```text
¿LO CONSEGUISTE?
¿HASTA DÓNDE LLEGASTE?
```

## C11-C visual system

- Tipografía nueva para texto C11-C: `assets/fonts/courier-regular.ttf`.
- 18 paletas semánticas por familia.
- Entorno procedural común, dependiente de seed pero subordinado al estímulo.
- Tracking: sin Tron; conserva la estela histórica.
- Saccade: entorno de constelación muy ligero, sin líneas de salto.
- Pursuit: campo estelar/niebla espacial + DOF radial.
- Peripheral Scan: polvo espacial + radar orbital + flare angular.
- No se añaden assets externos ni PNG generados para estos fondos.

## Audio

El review runner genera un único master global `drill_motion_ambient_v2` para todos los Visual Drills. Es determinista, móvil-seguro y no codifica el timing de eventos mecánicos.

## Sidecars

Cada render de Visual Drill debe producir:

```text
VisualDrill_<family>_seed_<seed>_social.txt
```

junto con `authoring.json`, `envelope.json`, manifest, MP4, GIF y contact sheet.

## Validación

La última ejecución del usuario sobre 2.8.1 produjo render real de Pursuit y Peripheral correctamente. 2.9.0 añade tres nuevas suites de regresión y aún requiere la validación runtime final en Windows/Godot 4.7.1.

### Entrada documental

- `docs/00_PROJECT_OVERVIEW.md`
- `docs/01_ARCHITECTURE.md`
- `docs/02_DATA_AND_CONTRACTS.md`
- `docs/03_PRESENTATION.md`
- `docs/05_TESTING_AND_REGRESSION.md`
- `docs/07_ROADMAP.md`
- `docs/c11/C11-C_2.9.0_CURRENT_STATE.md`
- `docs/master-prompts/MASTER_HANDOVER_C11-C_CURRENT_v2.9.0.md`
