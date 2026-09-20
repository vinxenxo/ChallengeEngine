# C11-C — VISUAL TEXT PLACEMENT POLICY v1.0

## Rule

For all five Visual Loop families:

- Former Footer mathematical/technical lines move to Header.
- Former Header eyebrow + hook move to Footer.
- Family signature remains in Footer as the editorial closing mark.

## Render layout

- Header math line: `y≈40`
- Header data line: `y≈66`
- Footer eyebrow: `y≈34`
- Footer hook: `y≈54`
- Footer signature: `y≈101`

This is presentation-only. It does not alter simulation, RNG, `SimulationResult`, timing contracts, or frozen engine boundaries.

## Production export rule

Prototype/review renders retain the footer for art-direction inspection. Production Visual Loop exports MUST omit the footer so social-platform UI cannot compete with or obscure the artwork. Header mathematical metadata remains the prototype review treatment; production export may use the finalized product metadata policy.
