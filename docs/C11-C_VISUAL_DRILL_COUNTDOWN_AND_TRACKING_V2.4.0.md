# C11-C 2.4.0 — Visual Drill countdown + Tracking production baseline

## Common Visual Drill presentation

All Visual Drills use the existing Challenge presentation countdown component and the extracted shared `CountdownPresentationLogic`. The countdown is presentation-only and emits `3`, `2`, `1` at 30 FPS across frames `0..89`. It is centered in the Body UI envelope.

The gameplay stream is not rewritten to contain countdown frames. `VisualContentPlayer` presents logical gameplay frame `0` during the countdown and starts the canonical gameplay stream after frame 90.

Current C11-C physical contract for Visual Drills: **3 seconds countdown + 17 seconds gameplay = 20 seconds total**, 30 FPS, 600 physical presentation frames.

The authoring adapter remains generic; its historic short-duration tests and contracts are not modified. The C11-C review/production presentation pipeline supplies the 17-second gameplay envelope.

## Editorial intro

During the 3-second pre-roll the shared header double-line area displays a family-specific instruction. For Tracking the text is:

`¿ERES CAPAZ DE SEGUIR EL OBJETO CON LA VISTA SIN PERDERLO?`

At gameplay start the instruction disappears and the existing Matrix sequence resumes.

## Tracking

Tracking remains the `smooth_pursuit` mechanic: one target moves continuously along a deterministic bounded Lissajous trajectory. The current baseline uses a 2:3 Lissajous shape over 17 seconds. The presentation trail is a growing history only; it never reveals future path information.

The Body renderer occupies the complete logical width `540 px` inside `y=144..816`. A presentation-only Tron depth background provides perspective and forward travel. Palette variants are deterministic and chosen for high mobile contrast.

## Difficulty

The existing five canonical difficulty tiers remain intact. Their C11-C presentation bands are:

- tiers 1–2: EASY
- tier 3: MEDIUM
- tiers 4–5: HARD

The existing tier speed multipliers are preserved; C11-C does not reinterpret historic authoring semantics.

## Frozen boundaries

No changes are made to C11-B simulation mathematics, RNG ownership, `SimulationResult`, `winning_frame`, `close_calls`, C7 audio contracts, C9 authoring contracts, or logical Social Frame geometry.

## Future Tracking variants

The current C11-C baseline is `smooth_pursuit`: the target moves without disclosing its future route. A future independent Tracking variant may expose a pre-drawn geometric route (`guided_path`) and have the target follow that route. That variant is intentionally outside C11-C 2.4.0.

## Historical baseline superseded by C11-C 2.7.0

The 2.4.0 duration examples above predate the terminal self-evaluation CTA. The current shared presentation contract is `docs/C11-C_VISUAL_DRILL_SOCIAL_PRESENTATION_CONTRACT_v1.4.md`: PRE_ROLL + GAME + END_CTA, with a 3-second terminal CTA appended after gameplay.
