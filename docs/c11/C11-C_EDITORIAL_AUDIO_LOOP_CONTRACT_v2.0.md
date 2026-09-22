# C11-C EDITORIAL / AUDIO / LOOP CONTRACT v2.0

Status: review-phase implementation.
Scope: presentation and media generation only.

## Header

Two large lines are displayed in the Header.

Line 1 = factual identity of the generated variant: `GRAMMAR | REAL PARAMETER | REAL PARAMETER`.
Line 2 = audience-facing hook.

Around the midpoint, line 2 performs a short deterministic Matrix / airport-board character transition
and resolves to `VISUAL LOOP / FAMILY`. It returns to the hook before the final loop boundary.

## Footer

Footer is small review telemetry and can be disabled in production with `-NoFooter`.
It contains family identity, deterministic technobabble, seed/body/duration, a real variant parameter,
palette/audio state, and a deterministic art signature.

## Background

Header, Body and Footer share one theme background. Current value: `#000000`.

## Audio

Audio is enabled by default. `-NoSound` produces a silent MP4.
Default sound is restrained deep ambient: low drone, singing-bowl resonance and slow harmonic movement
locked to the visual normalized loop. No beep test tones are used.

## Duration / loop

Current review/production candidate duration: 18.0 seconds at 30 FPS = 540 frames.
Each family profile uses an integer number of complete normalized cycles (minimum 1).
The renderer loops from frame 539 back to frame 0; no terminal partial cycle is introduced.

## Social sidecar

Every generated video gets a sibling UTF-8 `.txt` sidecar containing title, description, family, grammar,
palette, seed, duration, loop cycles, audio state, hashtags and the exact reproduction command.

## Frozen boundaries

No changes to core, simulation, SimulationResult, engine RNG ownership, winning-frame logic, C7, or
C11-B geometry are allowed by this presentation layer.
