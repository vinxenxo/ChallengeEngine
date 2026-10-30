# C11-E — prompt maestro de continuidad (V4)

Continúa C11-E en `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`, sobre la rama local `main`. La última captura revisada observó HEAD `bc8330e794fe37efe0c4f9c2bb0c0bd389f28f2c`; no cambies rama, refs, commit ni remoto.

## Fuente de autoridad

Lee `AGENTS.md`, `.continue/rules/CONTINUE.md`, `docs/current/e/README.md` V4, `C11E_CURRENT_AUTHORITY_20261030_V4.md`, `C11E_GATES_ACCEPTANCE_MATRIX_20261030_V4.md`, `C11E_E0_REVIEW_AND_E1_SOURCE_ARCHITECTURE_20261030_V1.md`, `C11E_DOCUMENTATION_RECONCILIATION_20261030_V4.md`, el charter/contrato y registro de riesgos V3. La transición D→E está en `docs/history/c11d/C11D_TO_C11E_ROADMAP_TRANSITION_20261030_V1.md`.

E0 está PASS en instalación y revisión. E1 sigue IN_PROGRESS. No repetir bootstrap, no recrear snapshots y no rehacer gates D cuyos source pins no hayan cambiado.

## Objetivo de ingeniería

Un único servicio de producción E dentro del módulo existente `c11c-suite/c11c-producer` debe servir GUI y CLI. Reutiliza la normalización/resolución D9.9 cuando sus contratos lo permitan; no reutilices `shared_production_context_service.py` ni D9.10 como dispatcher, porque son fachadas/bridges de preparación D.

Después, construye un consumidor E aditivo de Challenge que dibuje `editorial.title` en un slot específico de Header. No conviertas `title` en `content.hook`; no sustituyas CTA. Primera prueba E2: dos MP4 físicos `CHALLENGE_001`, mismo request salvo title; mismas mecánicas, `request.seed`, duración y frames; cambio verificable dentro de la máscara del título y ninguna diferencia mecánica no explicada fuera de ella.

## Límites

C11-C 2.19.12 sigue siendo baseline protegido. Su manifiesto `release/C11C_FREEZE_PACKAGE_MANIFEST.json` debe permanecer en SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` y tamaño 796318 bytes. No mutar simulación, `SimulationResult`, `winning_frame`, `close_calls`, RNG, definiciones de mecánica ni runners C congelados. `request.seed` y `request.music_seed` son independientes. D3/mux es E3, no E2. No alterar receipts ni bloqueos históricos D. `CHALLENGE_008/009` quedan excluidos hasta resolver 11 s declarados frente a 12 s de fases.

## Próxima acción obligatoria

Coteja desde el checkout activo los hashes del grupo de fuentes C especificado en el informe E0/E1 (GeneradorMaestro, Main.tscn, PresentationUI, SocialUIBinder, HookComponent, TypographyLabel, PresentationTheme, runner C, CHALLENGE_001 y manifiesto). Cualquier mismatch es hard stop. Después implementa E1 como el cambio mínimo, acompañado de contract tests GUI/CLI; no invoques render físico en E1. E2 queda reservado a la pareja A/B cuando su adapter y receipt estén listos.
