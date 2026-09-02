# C6-E / E3 — PRESENTATION VALIDATION

## Scope

E3 introduces a hard validation gate for presentation profiles. It does not modify simulation truth, RNG semantics, timeline semantics, winning-frame mathematics, or mechanic contracts.

## Validation contract

A presentation profile must satisfy:

- immutable source canvas: 540x960;
- immutable master output: 1080x1920;
- positive safe-area dimensions fully contained in the source canvas;
- typography scale finite and within `(0, 4]`;
- positive, bounded typography sizes;
- text width not larger than the safe-area width;
- required composition keys and supported composition tokens;
- non-empty theme id;
- loadable presentation font and valid theme sizing;
- render model contains the complete presentation contract.

## Runtime gate

`ChallengeDefinitionValidator` invokes `PresentationProfileValidator` before simulation/render when `presentation` is present. Invalid presentation configuration therefore fails Layer 0 rather than producing a render-time failure.

## Tests

`tests/C6E3PresentationValidationTest.gd` verifies:

- valid challenge profile passes;
- invalid safe area fails;
- impossible typography width fails;
- invalid composition token fails;
- invalid typography scale fails;
- Layer 0 rejects invalid presentation profiles;
- 540x960 source and 1080x1920 master contracts remain fixed;
- configured theme exposes a loadable font.
