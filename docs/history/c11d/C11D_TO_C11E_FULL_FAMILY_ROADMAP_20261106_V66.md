# C11-D to C11-E Full Family Roadmap — V66

Supersedes V65. C11-C 2.19.12 remains the immutable compatibility baseline until C11-E independently passes all family and release gates.

## Phase map

| Phase | Status | Closure condition |
|---|---|---|
| E4A Challenge | CLOSED `PASS_TEST_ONLY` | Accepted GUI/CLI, visual, A/V and operator review |
| E4B Loop request/editorial planning | CLOSED for plan-only | 27 concrete grammars, 81 cases/repeats, GUI/CLI parity |
| E4B policy decisions | APPROVED AS PROPOSED | Five current proposal SHA values bound by operator record V1 |
| E4B family contract | PASS_STATIC 27/27, Windows verification pending | Canonical D9.9/D9.10 and D adapter records → exact C11-C family launcher plan, silent visual stage, approved composition plan |
| E4B family payload | NOT YET ACCEPTED | Request-scoped materialized payload receipt for all 27 selectors |
| E4B visual consumer | NOT YET IMPLEMENTED/VERIFIED | D-only compositor at existing boundary; Godot pixel/typography test and operator review |
| E4B A/V/music | BLOCKED ON MUSIC ROUTE | `music_seed`-correct existing family music call plus required selection/mix scope; no C11-C modification |
| E4C Drill | WAITING E4B | Apply the accepted shared contracts to drill-specific payload/variant binding; no inherited Loop assumptions |
| E5 | WAITING E4C | Seed/profile/binder determinism and separation |
| E6 | WAITING E5 | Smoke18 |
| E7 | WAITING E6 | Matrix101; CH_008/009 held, 99 provisional until independently resolved |
| E8 | WAITING E7 | Historical C-to-E regression and separately authorized freeze/promotion decision |

## E4B architecture boundary

The flow remains: existing Producer GUI/CLI → canonical D9.9 universal plan → D9.10 plan-only bridge → existing D-only adapter preparation envelope → D-only family-stage preparation contract → request-scoped C11-C payload receipt → D-only visual composition/consumer. The family-stage module is currently a pure in-memory preparation tool, not yet wired into the GUI/CLI call path. No new Producer, surface or binder is allowed.

The family-stage contract routes one exact grammar through its own existing `run_prototype.ps1` signature and sets `-NoSound`. This is deliberate: all five legacy launchers pass the visual seed into their optional ambient music branch. The music seed must remain isolated. D.1's approved technical output envelope does not define soundtrack selection or authorize audio generation/mux.

## Invariants

- C11-C manifest pinned and all protected generator/RNG/binder/renderer/shared audio sources immutable.
- `request.seed` only on visual generation; `request.music_seed` reserved for a future separately approved family music route.
- Source frame count/order/duration and 30 FPS preserved; no frame interpolation or cadence resampling for Loop.
- A.1/A.3 map editorial values and full-span windows; actual frame count comes from request-scoped materialized payload only.
- The accepted Loop composition is a D-owned outer frame; original source frame stays intact and is uniformly contained.
- Renderer-native input, dispatch, media and release remain blocked until their gates are separately satisfied.
