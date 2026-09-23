# C11-C 2.2.1 — Visual Presentation Overlay Contract

## Scope

This overlay changes only the C11-C presentation/art layer. C11-B, simulation mathematics, RNG ownership, SimulationResult, winning_frame, close_calls, C7 audio contracts, C9 authoring contracts and mechanic timing remain untouched.

## Common header

The former first header text is no longer rendered. Its upper space remains intentionally empty. The existing double-line header block remains in its logical position at `y=74..138`.

The header separator moves below that double-line block to `y=140`.

The double-line header block is the only header text block and uses the Matrix/airport-board animator. The animator cycles deterministically through four editorial states, spread over the full video:

1. Former header line 2 (the existing double-line text).
2. Former header line 1.
3. Former footer line 2.
4. Former footer line 3.

Each state holds for 84% of its quarter-slot; the remaining 16% performs a deterministic character scramble into the next state. Multiline text is preserved during transitions.

## Common footer

The footer retains only its first text line. The former footer lines 2 and 3 are no longer rendered as footer labels; they are consumed by the header Matrix sequence. The footer separator remains the leading separator at `y=14`.

Footer text size increases from the previous 12 logical px to 14 logical px. Header Matrix text increases to 21 logical px, with fitting down to 14 logical px when necessary.

## Physical delivery

The logical Social Frame remains `540x960`. Physical C11-C social delivery remains `720x1280` at `30 FPS`. Scaling remains a single `4/3` presentation-boundary operation.

## Visual Drills

Visual Drill Matrix is now enabled and consumes the same common presentation layer. No drill mechanic or simulation data is changed.

## Living Particles

`Living Particles` gains a presentation-only deterministic perspective road/grid behind the particles. It uses a palette-derived complementary tint for stronger contrast, a vanishing point, perspective rails and moving transverse grid rows. The motion simulates forward travel toward the viewer and is synchronized to the family renderer phase.

The road does not modify particle positions, particle counts, RNG, simulation state or mechanic timing.
