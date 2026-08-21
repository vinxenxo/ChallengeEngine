# PARKING_MECHANIC_V2.0.md — CHALLENGE_004 Production DDI Contract

## 0. Status

**Status:** FROZEN — MATHEMATICAL CONTRACT / IMPLEMENTATION VALIDATED IN ISOLATION

**Checkpoint:** 0.3.1–0.3.5

**Historical integration note:** This document records the 0.3.x isolation phase. Global `MechanicRegistry` / `GeneradorMaestro` integration was subsequently completed and is now part of the frozen 0.9.0 production baseline.

**Baseline oracle:** `core/mechanics/ParkingMechanic.gd` V1.0.

`ParkingMechanic.gd` remains frozen. V2 is a parallel implementation and must not overwrite the legacy class.

---

## 1. Identity

| Property | Value |
|---|---|
| Mechanic ID | `parking_v2` |
| Mechanic version | `2.0` |
| RNG version | `2.0` |
| Fixture | `CHALLENGE_004` |
| Family | `DODGE / SAVE / CONTROL` |
| Seed | `314159` |
| FPS | `60` |
| GAME frames | `420` |

---

## 2. Production RNG Streams

| Stream | ID | Domain | Index semantics | Consumer |
|---|---:|---|---|---|
| `PARKING_DODGE_OFFSET` | 30 | `STRUCTURAL_MAIN` | `0` | `ParkingMechanic` |
| `PARKING_SAVE_OFFSET` | 40 | `STRUCTURAL_MAIN` | `0` | `ParkingMechanic` |
| `PARKING_OVERSHOOT` | 50 | `STRUCTURAL_MAIN` | `0` | `ParkingMechanic` |
| `PARKING_STEERING_NOISE` | 60 | `STRUCTURAL_MAIN` | `f*2`, `f*2+1` | `ParkingMechanic` |

There is no `PARKING_TRAJ` stream. The trajectory is the deterministic composition of the three generation parameters plus per-frame steering noise.

---

## 3. Capability Contract

`ParkingMechanicV2` receives:

```text
consumer_id = "ParkingMechanic"
rng_version = "2.0"
allowed_streams = [30, 40, 50, 60]
```

The mechanic has no dependency on `CosmeticRNG`, presentation contexts, visual nodes, or assets.

---

## 4. Mathematical Model

### 4.1 Configuration

Inputs are read from `difficulty.parking` and `difficulty.tolerance`:

- `start_position`
- `target_position`
- `target_angle_deg`
- `max_speed_px` (currently a configured parameter retained from V1; it does not alter the extracted trajectory equations)
- `steering_noise`
- `distance_px`
- `angle_deg`

### 4.2 Geometry

```text
P0 = start_pos
target_center = target_pos
mid_vector = target_center - P0
perp_vector = Vector2(-mid_vector.y, mid_vector.x).normalized()
```

Generation parameters are sampled once:

```text
D = sample_float_range(30, 0, -140, 140)
S = sample_float_range(40, 0,  -50,  50)
O = sample_float_range(50, 0,   60, 120)
```

Control points:

```text
P1 = P0 + mid_vector * 0.30 + perp_vector * D
P2 = P0 + mid_vector * 0.65 + perp_vector * S
P3 = target_center + mid_vector.normalized() * O
```

### 4.3 Timeline coordinate

For frame `f` and `N = 420`:

```text
t_anim = f / (N - 1)
```

`t_curve` is piecewise:

```text
if t_anim <= 0.4:
    t_curve = t_anim

if 0.4 < t_anim < 0.8:
    local_t = (t_anim - 0.4) / 0.4
    t_curve = 0.4 + smoothstep(0, 1, local_t) * 0.35

if t_anim >= 0.8:
    t_curve = 0.75 + (t_anim - 0.8) * 1.25
```

### 4.4 Steering noise

For every frame:

```text
Nx = sample_float_range(60, f*2,   -8*sigma, 8*sigma)
Ny = sample_float_range(60, f*2+1, -8*sigma, 8*sigma)
```

where `sigma = steering_noise`.

```text
noise_factor = sin(PI * t_anim)
Noise = Vector2(Nx * noise_factor, Ny * noise_factor)
```

The noise is modulated by `t_anim`, not `t_curve`.

### 4.5 Bézier position

The cubic Bézier position is:

```text
B(t) =
  (1-t)^3 P0
  + 3(1-t)^2 t P1
  + 3(1-t)t^2 P2
  + t^3 P3
```

Therefore:

```text
Position(f) = B(t_curve) + Noise
```

### 4.6 Tangent and rotation

The cubic Bézier derivative is evaluated at `t_curve`. The current angle is its `angle()` when the tangent magnitude is sufficient; otherwise the previous angle is retained.

### 4.7 Derived metrics

No additional RNG is consumed for these metrics.

```text
velocity(f) = distance(Position(f), Position(f-1))
             with velocity(0) = 0

spatial_distance(f) = distance(Position(f), target_center)

angle_error(f) = abs(angle_difference(current_angle, target_angle_rad))

steering(f) = clamp(
    angle_difference(current_angle, prev_angle) * 10,
    -1,
    1
)

braking(f) = smoothstep(180, 0, spatial_distance)
             if t_anim > 0.4
             else 0
```

The effective success metric is:

```text
effective_distance(f) = spatial_distance(f)
                       + max(0, angle_error(f) - tolerance_angle_rad) * 100
```

This preserves the V1 formula including the non-negative angular penalty.

---

## 5. FrameSnapshot Contract

Each valid simulation must produce exactly `420` snapshots.

Required presentation-neutral fields:

```text
position
rotation
scale = Vector2.ONE
opacity = 1.0
```

Required `custom_data`:

```text
success_distance
spatial_distance
velocity
angle_error
steering
braking
dodge_offset
save_offset
overshoot_dist
```

`custom_data` contains structural/derived data only. Visual effects such as dust, tire smoke, camera shake and decorative particles are not part of the simulation contract.

---

## 6. SimulationResult Contract

Metadata includes:

```text
seed_used
mechanic = "parking_v2"
rng_version = "2.0"
dodge_offset
save_offset
overshoot_dist
```

The mechanic does not calculate `winning_frame`. The normal downstream detector and validator remain responsible for winner selection and validation.

If an RNG context error occurs, the mechanic returns an empty `SimulationResult` and the Composition Root must reject the result before detector/validator processing.

---

## 7. V1.0 → V2.0 Mapping

| V1.0 | V2.0 treatment |
|---|---|
| `_rng_index` | eliminated |
| legacy RNG calls | replaced with stateless context samples |
| `dodge_offset` | stream 30, index 0 |
| `save_offset` | stream 40, index 0 |
| `overshoot_dist` | stream 50, index 0 |
| `noise_x` | stream 60, `f*2` |
| `noise_y` | stream 60, `f*2+1` |
| Bézier equations | preserved |
| `success_distance` | derived |
| `velocity` | derived |
| `steering` | derived |
| `braking` | derived |
| presentation effects | excluded |

Equivalence is defined against **the same effective structural RNG values and the same mathematical inputs**, not necessarily the same seed. This permits the legacy and V2 implementations to be compared without forcing artificial RNG stream equivalence.

---

## 8. Isolation and DDI Requirements

1. Cosmetic RNG consumption must not change the simulation result.
2. Structural streams must be independent of call order.
3. Replacing/reordering presentation execution must not change structural output.
4. Mutating stream 60 must alter structural output while streams 30/40/50 remain unchanged.
5. RNG capability failures must bubble to the Composition Root.
6. No partial simulation may proceed to downstream winner detection.

---

## 9. Validation Evidence

`tests/ParkingMechanicV2IsolationTest.gd` is the isolated certification suite.

The working environment has already produced:

```text
[PARKING_V2_ISOLATION_SUITE] PASS
```

The suite covers P1–P7, including the corrected interception of `sample_float_range()` for structural mutation and runtime RNG failure tests.

This sentence is historical: later checkpoints certified global pipeline integration.

---

## 10. CHALLENGE_004

`CHALLENGE_004.json` declares:

```text
mechanic = parking_v2
mechanic_version = 2.0
rng_version = 2.0
seed = 314159
```

Temporal configuration:

```text
HOOK = 120
GAME = 420
CTA = 120
TOTAL = 660
```

The preceding sentence is historical and refers to the pre-integration 0.3.5 state.

---

## Current Live Status — CHECKPOINT 0.9.0

`parking_v2` is a frozen production fixture. Its streams 30/40/50/60 are governed by the semantic RNG architecture and its production result participates in the validated 001–006 batch.
