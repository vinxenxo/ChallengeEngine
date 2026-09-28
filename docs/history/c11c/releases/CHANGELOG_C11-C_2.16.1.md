# C11-C 2.16.1 — Post-Review Contract Corrections

## Scope

This is a post-freeze refinement overlay on top of C11-C 2.15.1 and 2.16.0.

### Corrections

- Registered `C11CArtDirectionProductionHygieneContractTest.gd` in `tests/run_all.py` `KNOWN_SUITES`.
- Restored the visible Header/Footer separator lines in the shared editorial layer.
- Updated common and Visual Drill presentation contracts to expect visible separator rules.
- Hardened the Visual Loop Longform contract with an explicit `transition_through_black=false` assertion.
- Ensured the Longform schedule and composer expose the no-black transition contract.

### Frozen boundaries

No changes to C11-B simulation truth, mechanics, structural RNG, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, C7 audio ownership, or C9 authoring contracts.
The C11-C 2.15.1 manufacturing milestone remains frozen.
