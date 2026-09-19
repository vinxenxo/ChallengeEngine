# C6-E4 — Winning Frame Visual Emphasis

## Objetivo

Hacer inequívoco el instante del `winning_frame` mediante pequeños marcos verdes que circunscriben los elementos visuales afectados, sin convertir el highlight en una nueva fuente de verdad.

## Arquitectura

`SimulationResult.winning_frame` sigue siendo la única verdad matemática.

`GeneradorMaestro` conserva el consumo pasivo de `FrameSnapshot` y construye únicamente geometría visual a partir de los nodos ya renderizados.

`PresentationUI` activa `WinningHighlightComponent` cuando:

`ui_state == GAME && ui_state_frame == winning_frame_game`

El componente recibe `Array[Rect2]` y dibuja un marco por elemento.

## Garantías

- exacto en un único frame;
- invisible en `winning_frame - 1`;
- visible en `winning_frame`;
- invisible en `winning_frame + 1`;
- no aparece fuera de `GAME`;
- no calcula `winning_frame`;
- no accede a RNG;
- no modifica `SimulationResult`;
- no altera `VideoTimeline`;
- no cambia ninguna matemática de mecánica.

## Nota de integración

El archivo `WinningHighlightComponent.gd` es autocontenido y puede incorporarse sin alterar C3-C5. La integración indicada en `WinningHighlightComponent.integration.txt` usa la API actual `PresentationUI.set_state()` y los valores ya existentes `winning_frame_game` / `ui_state_frame`.
