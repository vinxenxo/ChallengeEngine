# C11-C Visual Drill Audio Direction v1.0

## Goal

Create an ambient bed that is audible on small mobile speakers without masking the visual task, introducing fatigue, or competing with the target stimulus. Audio remains a shared global master across all Visual Drills rather than a family-specific music track.

## Design principles

- Low-frequency foundation is restrained; the audio must not depend on sub-bass that inexpensive phones cannot reproduce.
- Mid-band information carries most of the audible identity so the bed remains present at low device volume.
- No sharp transients, aggressive sidechain pumping, stereo phase tricks or high-frequency hiss that could become distracting on earbuds/phone speakers.
- Slow envelopes and long harmonic cycles should support sustained attention rather than impose a metronomic task cue.
- The shared master is deterministic and reproducible; render duration may exceed the base loop and is safely looped by the review/export pipeline.

## Motion accompaniment

The bed can suggest movement through slow amplitude/harmonic swells, but visual mechanics remain the sole source of task timing. Audio must never reveal the target trajectory, saccade endpoint or event timing.

## Current hardening in 2.7.0

The review pipeline generates a 27-second master so Tracking's full presentation envelope is covered without relying on an audio-file truncation. The underlying audio generator retains its shared, family-independent deterministic bed and safe looping behavior.

## Future audio v2 candidate

A later audio pass may add three extremely subtle synchronized layers—air, harmonic pulse and low-mid movement bed—whose phase is driven by the global presentation clock, not by the mechanic/RNG stream. That keeps the sonic identity shared while making the visual motion feel more intentional.
