# C11-C Visual Drill Social Presentation Contract v1.4

## Scope

This revision extends the existing Visual Drill social presentation without modifying the canonical gameplay stream. The presentation host adds a terminal self-evaluation phase after the complete gameplay stream.

## Temporal envelope

The effective presentation order is:

```text
PRE_ROLL (3 s) → GAME (canonical gameplay) → END_CTA (3 s)
```

The 3-second PRE_ROLL continues to reuse the shared Challenge countdown logic. The END_CTA is a presentation-only phase and never enters `VisualDrillRuntime`, `RenderedFrameStream` or mechanic calculations.

At 30 FPS:

```text
countdown_frames = 90
end_cta_frames   = 90
total_frames     = 90 + gameplay_frames + 90
```

Current canonical durations therefore become:

| Family | Gameplay | PRE_ROLL | END_CTA | Total | Frames |
|---|---:|---:|---:|---:|---:|
| Tracking | 21 s | 3 s | 3 s | 27 s | 810 |
| Saccade | 17 s | 3 s | 3 s | 23 s | 690 |
| Pursuit | 17 s | 3 s | 3 s | 23 s | 690 |
| Peripheral Scan | 17 s | 3 s | 3 s | 23 s | 690 |

The common 20–30 second Visual Drill delivery contract remains enforced.

## Reuse of Challenge CTA architecture

The implementation deliberately reuses the historical Challenge `CTAComponent` through `PresentationUI`. It does not create a second CTA widget or duplicate label rendering. Visual Drills provide their own terminal copy through the existing render-model binder:

```text
¿LO CONSEGUISTE?
¿HASTA DÓNDE LLEGASTE?
```

A small presentation-only entry animation is driven by the phase progress. This animation does not modify or infer gameplay state.

## Terminal state

During `END_CTA` the last emitted Visual Drill frame remains available to the presentation host. Shared telemetry/footer text is suppressed and the editorial Matrix transition is disabled so the self-evaluation prompt is visually unambiguous. The structural Header/Body/Footer geometry remains unchanged.

## Color application

Tracking and Saccade palette variants now flow through the shared editorial layer into header text, footer telemetry, rules, section backgrounds and terminal CTA colors. The palette bank remains presentation-only and deterministic.

## Frozen boundaries

No change is permitted to C11-B simulation truth, `SimulationResult`, `winning_frame`, `close_calls`, `RenderedFrameStream`, mechanical frame generation, structural RNG, C7 audio ownership, or C9 schema semantics.
