# C11-C Visual Drills — Gameplay / Cognitive Load Bible v1.0

## Product model
Visual Drills are pre-rendered MP4 challenges. The user performs the visual task mentally (and may record an answer). The generator produces a deterministic problem instance and an auditable hidden answer sheet in authoring output.

## Tracking — Agudeza Dinámica y Predicción
Core task: smooth visual tracking.

Expansion A — Predictive Tracking / Occlusion:
- authored occlusion density and width;
- target path continues deterministically behind an obstruction;
- renderer only masks/reveals authored target state.

Expansion B — Dynamic Morphing:
- authored allowed target shapes/colors;
- authored morph events and count;
- terminal prompt can ask how many target state changes were observed.

## Saccade — Memoria de Trabajo y Discriminación Balística
Core task: discrete eye relocation.

Expansion A — N-Back:
- authored `n_back_level`;
- authored endpoint sequence;
- answer sheet records exact matches.

Expansion B — Flash Recognition:
- authored short-lived internal symbol;
- authored symbol set and orientation;
- answer sheet records qualifying events.

## Pursuit — Convergencia Ocular y Sobrecarga Foveal
Core task: sustained pursuit under cognitive load.

Expansion A — Depth / Scale Simulation:
- authored bounded scale modulation;
- background parallax can respond visually but cannot redefine path truth.

Expansion B — Flanker Interference:
- authored satellite count and congruency;
- central payload remains the only answer-bearing stimulus.

## Peripheral Scan — Conciencia Holística y Ritmo
Core task: central fixation plus peripheral discrimination.

Expansion A — Spatial Binning:
- authored active quadrants;
- answer sheet contains target quadrant/time records.

Expansion B — Rhythmic Asynchrony:
- authored anchor BPM;
- authored peripheral rhythm mode (`sync`, `offbeat`, `chaotic`);
- answer sheet remains time-addressable.

## Authoring rule
Every cognitive mechanic that affects the answer must be represented as deterministic authoring/runtime data before presentation. Never make the renderer decide whether an event counts.
