# ChallengeEngineV01_STATELESS — Project Overview

## Current state

**C11-B — CLOSED / CERTIFIED / FROZEN.**

**C11-C — ACTIVE, current implementation 2.9.0.**

The C11-C Visual Drill presentation now spans four deterministic training families: Tracking, Saccade, Pursuit and Peripheral Scan. The common social frame remains 540×960 with Header 0..144, Body 144..816 and Footer 816..960.

The 2.9.0 work window consolidates the terminal CTA, typography, broader semantic palettes, procedural drill environments, shared motion-ambient audio, social sidecar guarantees and current documentation, while preserving the frozen engine boundaries.

## Frozen pillars

1. Stateless deterministic simulation.
2. Explicit semantic RNG ownership.
3. `SimulationResult` / frame snapshots as gameplay truth.
4. Passive presentation.
5. `RenderedFrameStream` as the visual runtime contract.
6. C7 audiovisual contracts.
7. C9 authoring contracts.
8. Reproducible QA and evidence under `artifacts/`.
9. C11-B Header/Body/Footer framing contract.

## Current Visual Drill presentation phases

```text
PRE_ROLL 3 s
    ↓
GAME — canonical authored/runtime drill stream
    ↓
END_CTA 3 s — self-evaluation prompt in HEADER
```

Tracking uses 21 s gameplay; Saccade, Pursuit and Peripheral Scan use 17 s gameplay. Total durations remain 27 s and 23 s respectively.

## Current route states

### Tracking

Seed controls authored Lissajous frequencies, phases, amplitudes, centre, travel cycles and controlled speed variation. Presentation retains a growing history trail, rich palettes and a procedural background without the former Tron road.

### Saccade

Seed controls polar endpoint distribution. Spatial jumps remain discrete, with no interpolation. The target contains a jump counter derived from emitted `jump_index`.

### Pursuit

Seed authoring produces a uniform cubic B-spline, arc-length LUT, per-frame normalized samples, controlled speed modulation, sizygia events and camouflage zones. The answer sheet records the sizygia count and event frame starts.

### Peripheral Scan

Seed authoring produces polar/logistic angular events, orbital rings, threat/distractor classification and a central anchor sequence. The answer sheet records both counts and exact frame starts.

## Working rule

C11-C may evolve art, typography, backgrounds, audio presentation and authoring-stage variation. It must not change C11-B simulation mathematics, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7 contracts or C9 frozen challenge authoring semantics.

## Where to start

- Current status: `docs/c11/C11-C_2.9.0_CURRENT_STATE.md`
- Architecture: `docs/01_ARCHITECTURE.md`
- Data: `docs/02_DATA_AND_CONTRACTS.md`
- Presentation: `docs/03_PRESENTATION.md`
- Testing: `docs/05_TESTING_AND_REGRESSION.md`
- Roadmap: `docs/07_ROADMAP.md`
- Current handover: `docs/master-prompts/MASTER_HANDOVER_C11-C_CURRENT_v2.9.0.md`
