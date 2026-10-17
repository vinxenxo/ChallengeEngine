# Challenge Visual Payload Semantic Binding Proposal V1

## Purpose
Turn the accepted static capability inventory into a reviewable, selector-specific proposal. It is not an approval and must not be consumed as renderer input.

## Common primary track
The logical in-memory preview may use exactly these source-frame fields: `position`, `rotation`, `scale`, `opacity`, `texture_index`, `variant_id`. This field shape already exists in the CHALLENGE_004 V1 preview. Keep each source sample at 60 FPS; no coordinate projection or delivery resampling is authorized.

## Selector-specific secondary binding proposal

| Challenge | Source binding proposed | Semantic interpretation | Status |
|---|---|---|---|
| 001 / key | `presentation.static_target_position` | Static lock target | Proposal only |
| 002 / parking | `difficulty.parking.target_position` | Static parking target | Proposal only; coordinate space undeclared in source |
| 003 / pilot | `FrameSnapshot.custom_data.target_x` | Scalar target X in `PILOT_0X100` | Proposal only; do not invent Y or project |
| 004 / parking_v2 | `difficulty.parking.target_position` | Static parking target; current V1 preview regression fixture | Proposal only; preserve V1 |
| 005 / hit_v1 | `FrameSnapshot.custom_data.target_position` | Separate moving target Vector2 track | Proposal only |
| 006 / catch_v1 | `FrameSnapshot.custom_data.target_position` | Separate target track alongside catcher primary track | Proposal only |
| 007 / find_v1 | `FrameSnapshot.custom_data.target_position` | Target track alongside scanner primary track | Proposal only |
| 008 / choose_v1 | `FrameSnapshot.custom_data.active_selection` | Selected option index | Proposal only; timebase block |
| 009 / count_v1 | `FrameSnapshot.custom_data.displayed_count` | Displayed count state | Proposal only; timebase block |

The code paths cited are the mechanic implementation source pinned by V2-A. This proposal identifies candidates; it does not turn candidate values into approved rendered transforms. `custom_data` may not be serialized wholesale.

## Denylist
Never bind `success_distance`, `spatial_distance`, `velocity`, `angle_error`, `steering`, `braking`, `dodge_offset`, `save_offset`, `overshoot_dist`, `control_offset`, `base_x`, `trajectory_noise`, `target_count`, scoring outputs, `winning_frame`, or `close_calls` by default.

## Scope limitations
- This is static proposal validation, no Godot runtime calls and no payload instances.
- Candidate-field seeds and semantic mappings do not prove actual visual-payload seed sensitivity.
- Music-seed orthogonality cannot be claimed by the Challenge source-only runtime boundary; it must be tested at the actual canonical request boundary.
- CHALLENGE_008/009 declared-total conflicts remain unresolved at 11 seconds declared versus 12 seconds phase sum. Their runtime materialization remains withheld.
- Renderer, media, release, freeze and promotion gates remain unchanged.
