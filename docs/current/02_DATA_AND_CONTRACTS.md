# Data and Contracts — Current

## Visual Loop catalogue

| Technical family | Artistic family | Production ID | Grammars |
|---|---|---|---:|
| geometric | Geometric Waves | `c11c_geometric_waves_v1` | 5 |
| fractal | Fractal Bloom | `c11c_fractal_bloom_v1` | 5 |
| kaleidoscope | Sacred Symmetry | `c11c_sacred_symmetry_v1` | 5 |
| particle_flow | Living Particles | `c11c_living_particles_v1` | 5 |
| vector_field | Invisible Forces | `c11c_invisible_forces_v1` | 7 |

Total: 27 grammars.

## Visual Drills

- Tracking
- Saccade
- Pursuit
- Peripheral Scan

Current presentation timing is:

- Tracking: 21 s gameplay + 3 s PRE_ROLL + 3 s END_CTA = 27 s / 810 frames.
- Saccade/Pursuit/Peripheral Scan: 17 s gameplay + 3 s PRE_ROLL + 3 s END_CTA = 23 s / 690 frames.

Presentation cannot invent answer events.

## Historical Challenges

The canonical Challenge corpus contains `CHALLENGE_001` through `CHALLENGE_009`.

| Challenge | Mechanic | FPS | Canonical phase-sum duration | Frames |
|---|---|---:|---:|---:|
| 001 | key | 60 | 9 s | 540 |
| 002 | parking | 60 | 10 s | 600 |
| 003 | pilot | 60 | 12 s | 720 |
| 004 | parking_v2 | 60 | 15 s | 900 |
| 005 | hit_v1 | 60 | 7 s | 420 |
| 006 | catch_v1 | 60 | 9 s | 540 |
| 007 | find_v1 | 60 | 10 s | 600 |
| 008 | choose_v1 | 60 | 12 s | 720 |
| 009 | count_v1 | 60 | 12 s | 720 |

Challenge duration is always derived from `hook_duration + game_duration + reveal_duration + cta_duration`. A legacy `video.total_duration` field is not authoritative for production timing.

## Delivery profiles

The single delivery catalogue is `profiles/delivery/c11c_video_delivery_profiles.json`.

- `MASTER_1080`: 1080×1920, standard default.
- `REVIEW_720`: 720×1280, historical C11-C review profile.
- `MIN_540`: 540×960.
- `META_REELS_FINAL_V1`: 1080×1920.
- `LONGFORM_1080`: 1080×1920.

Delivery scaling is post-capture. It cannot change simulation or gameplay coordinates.

## Seeds

Seed choice is part of reproducibility. Production and review manifests record the exact seed. Seed variation must remain separate from frozen runtime RNG ownership.

## Contract reopening

A gameplay-semantic change requires a new checkpoint, dedicated authoring/runtime contract, focused tests and full regression evidence. Art, delivery and producer orchestration changes remain additive unless an existing contract is explicitly reopened.
