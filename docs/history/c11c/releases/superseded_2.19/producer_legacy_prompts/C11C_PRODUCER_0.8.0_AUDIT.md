> SUPERSEDED: Producer 0.8.0 state. Current GUI: `docs/current/producer/C11C_PRODUCER_0.9.0_CURRENT_STATE.md`.

# C11-C Producer 0.8.0 — Audit and Closure Record

## Audit scope

Audited GUI code, producer schema, canonical Challenge launcher integration, Visual Loop launcher integration, Visual Drill production integration, queue state handling, delivery profile propagation, challenge timing metadata and current documentation.

## Findings resolved

### F1 — Duplicate Challenge catalogue

The GUI previously depended on duplicated Challenge metadata in the schema. It now loads the actual nine canonical files under `challenges/` and calculates duration exclusively from `hook_duration + game_duration + reveal_duration + cta_duration`.

### F2 — Seed collision risk

Challenge seed jobs now receive a unique seed-specific output root.

### F3 — Delivery drift

The GUI, Loop wrapper and Drill wrapper now read `profiles/delivery/c11c_video_delivery_profiles.json`. The five delivery IDs are centralized. `MASTER_1080` is the default standard profile.

### F4 — Drill Tracking timing drift

The active contract requires 21 s gameplay / 27 s total. The review runner and request-specific envelope generator are aligned to 21 s.

### F5 — GUI lifecycle polish

Returning from a batch/utility operation to A LA CARTA refreshes the visible content form. Queue errors leave the recipe row in ERROR state and restore the Generate control.

## Deliberate non-goals

The GUI does not become a second engine. It does not calculate Challenge mechanics, derive gameplay truth, mutate simulation RNG, or render content itself.
