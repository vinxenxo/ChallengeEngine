# C11-C Visual Presentation Overlay Contract — v2.2.2

## Scope

Common presentation-only overlay for Visual Loops and Visual Drills. C11-B functional and structural contracts remain frozen.

## Header

- Logical region: `540x960`, Header `y=0..144`.
- Former first header text is no longer rendered, but its upper vertical space is retained.
- The visible double-line header block remains centered at logical `y=74..138`.
- Header separator is at `y=140`, immediately below the visible double-line block.
- Header font target: `23` logical px, deterministically reduced only when required to stay inside the logical content width `468px` (36px side margins).
- Matrix/split-flap animation affects only this visible double-line block.
- During the full video, the block rotates deterministically through four editorial states: current double-line header, former header line 1, former footer line 2, former footer line 3.

## Footer

- Logical region: Footer `y=816..960`.
- Visible content is separator + first footer text line.
- Footer lines 2 and 3 are not rendered as separate footer labels; they are consumed by the header Matrix sequence.
- Footer font target: `14` logical px with deterministic fit-down.

## Visual Drills

- Uses the same common Matrix presentation mechanism as Visual Loops.
- Matrix changes presentation only; it does not modify drill timing, stimulus state, frame truth or mechanic output.

## Living Particles

- Body composition order is: separate background → perspective Tron road → procedural particles.
- Tron road uses a saturated complementary hue derived from the particle palette, with a deterministic fallback for low-saturation palettes.
- Road includes perspective rails, lane geometry, transverse depth grid and forward travel synchronized to the existing visual phase.
- Road remains subordinate to the particle field and never alters simulation state.

## Frozen boundaries

No changes to simulation mathematics, mechanics, RNG ownership, `SimulationResult`, `winning_frame`, `close_calls`, `RenderedFrameStream`, C7 audio contracts, C9 authoring contracts or C11-B logical Header/Body/Footer geometry.
