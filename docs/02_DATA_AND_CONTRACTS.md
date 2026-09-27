# Data and Contracts

## Challenge corpus

Historical Challenge definitions remain independently testable and are not normalized for Visual Drill convenience.

## Visual Drill canonical presentation data

| Family | Gameplay | Total with phases | Primary authored response |
|---|---:|---:|---|
| Tracking | 21 s | 27 s | trajectory/optional future cognitive variants |
| Saccade | 17 s | 23 s | jump sequence / `jump_index` |
| Pursuit | 17 s | 23 s | `answer_sheet.sizygia_count` + event frames |
| Peripheral Scan | 17 s | 23 s | threat/distractor counts + event frames |

## Authoring answer sheets

The request-specific Visual Drill envelope generator writes `authoring.json`. Its `authored.answer_sheet` is the study answer key and remains separate from presentation styling.

### Pursuit

```json
{
  "sizygia_count": 4,
  "event_frame_starts": [ ... ]
}
```

The number is deterministic for the seed and difficulty tier. It is not recomputed by the renderer.

### Peripheral Scan

```json
{
  "threat_count": 4,
  "distractor_count": 8,
  "threat_frame_starts": [ ... ],
  "distractor_frame_starts": [ ... ]
}
```

## Seed variation

`VisualDrillSeedVariation/2.9.0` is the active authoring variation layer for all four drill families.

It changes family-specific authored data from the content seed while preserving deterministic repeatability. Runtime presentation variants remain separate cosmetic inputs.

## Frozen boundaries

Presentation additions must not alter:

- `SimulationResult`;
- `winning_frame`;
- `close_calls`;
- `WinningFrameDetector`;
- `RenderedFrameStream`;
- C7 audio contracts;
- C9 challenge authoring contracts;
- C11-B logical/physical social geometry.

## Contract reopening rule

A semantic engine change requires an explicit checkpoint with a new contract revision, focused tests, regression evidence and acceptance. C11-C art/presentation work must remain on the presentation side of that boundary.
