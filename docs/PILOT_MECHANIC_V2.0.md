# PILOT_MECHANIC_V2.0.md — Controlled RNG Isolation Fixture

## Purpose

`PilotMechanic` is not a product mechanic. It is a laboratory fixture for proving that V2.0 structural determinism is isolated from presentation determinism.

## Capability

- `consumer_id`: `PilotMechanic`
- `allowed_streams`: `STREAM_TRAJECTORY (10)`, `STREAM_CONTROL (20)`
- `rng_version`: `2.0`
- semantic index: `frame_number`

## Mathematical Contract

For `f` in `[0, game_frames - 1]`:

```text
f_norm = f / (game_frames - 1)
base_x(f) = start_x + (end_x - start_x) * f_norm
trajectory_noise(f) = (S_traj(f) * 2 - 1) * trajectory_amplitude
control_offset(f) = (S_ctrl(f) * 2 - 1) * control_amplitude
x(f) = base_x(f) + trajectory_noise(f) + control_offset(f)
target_x(f) = target_start + target_velocity * f
success_distance(f) = abs(x(f) - target_x(f))
velocity(f) = 0, if f = 0
velocity(f) = abs(x(f) - x(f-1)), otherwise
```

`S_traj(f)` and `S_ctrl(f)` are obtained from the corresponding structural streams at `index = f`.

## Frame Output

Each `FrameSnapshot` contains:

- `position = Vector2(x(f), 0)`;
- `rotation = 0`;
- `scale = Vector2.ONE`;
- `opacity = 1`;
- `custom_data.success_distance`;
- `custom_data.velocity`;
- `custom_data.target_x`;
- `custom_data.base_x`;
- `custom_data.trajectory_noise`;
- `custom_data.control_offset`.

Exactly `game_frames` snapshots are required.

## Isolation Contract

The mechanic has no access to `CosmeticRNG`, `PresentationRNGContext`, `VideoTimeline`, or visual assets.

Presentation calls must not modify `SimulationResult`. Structural stream mutation must be observable.

## Fixture

`challenges/CHALLENGE_003.json` is the controlled V2.0 fixture used by the Pilot tests.