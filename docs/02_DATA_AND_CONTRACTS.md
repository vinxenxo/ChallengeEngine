# Data and Contracts

## Challenge corpus

| ID | Mechanic | RNG | Notes |
|---|---|---|---|
| `CHALLENGE_001` | key | 1.0 | historical fixture |
| `CHALLENGE_002` | parking | 1.0 | legacy parking route |
| `CHALLENGE_003` | pilot | 2.0 | native current route |
| `CHALLENGE_004` | parking_v2 | 2.0 | native V2 parking |
| `CHALLENGE_005` | hit_v1 | 2.0 | native hit route |
| `CHALLENGE_006` | catch_v1 | 2.0 | native catch route |
| `CHALLENGE_007` | find_v1 | 2.0 | native find route |
| `CHALLENGE_008` | choose_v1 | 2.0 | native choose route |
| `CHALLENGE_009` | count_v1 | 2.0 | native count route |

Historical versions remain independently testable. Do not normalize their native durations or silently remap one mechanic to another implementation.

## Truth flow

```text
Definition
   → deterministic simulation
   → SimulationResult / FrameSnapshot
   → passive presentation
   → RenderedFrameStream
   → physical production artifact
```

## Visual content

The canonical C6-F0.8 visual loop/drill content envelope remains visual-only. C11-B adds the social presentation frame around the established runtime output; it does not turn social UI text into a canonical gameplay/content field.

## Schemas

The normative challenge schema is `schemas/challenge_schema.json`.

`tests/fixtures/` contains compatibility fixtures that may intentionally represent older contracts. Their existence is part of the regression surface and they must not be "modernized" merely for cosmetic consistency.

## Contract reopening rule

A frozen contract is changed only through a named checkpoint with an explicit contract revision, focused tests, regression evidence and a final acceptance decision.
