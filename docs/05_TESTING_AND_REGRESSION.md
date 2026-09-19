# Testing and Regression

## Test families

| Family | Purpose |
|---|---|
| CORE | mechanics, RNG, DDI and deterministic simulation |
| PRESENTATION | C6 runtime and presentation contracts |
| AUDIO | C7 deterministic audio and mux contracts |
| AUTHORING | C9 productive authoring and adapters |
| C10/C11 | integration, social frame and freeze contracts |
| PHYSICAL | Movie Maker + FFmpeg/FFprobe validation |
| STRESS | deterministic seed reproducibility |

## C11 evidence

- 103/103 logical suites PASS
- 54/54 C11-A visual qualification
- 54/54 C11-A.1 challenge qualification
- 54/54 retrocompatibility telemetry comparisons plus A/B rerun checks
- 576 stress executions across 288 cases, repeated twice
- 2/2 physical smoke exports
- 54/54 QA video renders

## PASS semantics

A test is PASS only when its declared success condition is met. A warning about an optional output marker does not override an exit code of zero when the test itself reports successful artifact validation.

The C7-A2 mixed-audio rule remains authoritative and is intentionally not redefined by C11 video-only QA.

## Retrocompatibility scope

C11 compares gameplay telemetry, not presentation hashes. This is deliberate because the social framing layer changed while simulation truth remained stable.
