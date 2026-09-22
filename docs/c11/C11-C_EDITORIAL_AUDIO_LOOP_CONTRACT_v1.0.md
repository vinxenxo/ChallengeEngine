# C11-C v1.9 — Editorial, Audio and Seamless Loop Contract

## Header
Line 1: dominant mathematical identity + selected visual grammar + cycle/zoom indicator.
Line 2: audience-facing hook. Around the midpoint it transitions through a deterministic Matrix-style
scramble to `VISUAL LOOP / FAMILY`, remains visible as the secondary identity, then scrambles back.
The final frame always contains the primary hook for loop continuity.

## Footer
Prototype/QA only. Small telemetry: seed, grammar, palette, cycle count, family parameters,
technobabble, generation notes and black-background state. Production can disable footer with `-NoFooter`.

## Background
Header, Body and Footer are intended to share pure black (`#000000`) in this phase. Renderers expose
`background_color` as a future theme hook; the current presentation setting is black.

## Color
Palette selection is seed-driven through `C11CPaletteBank`. The bank intentionally contains strongly
separated colorways per family. Color is presentation structure, not arbitrary RGB noise.

## Loop
Exports remain 540x960, 30 FPS, 300 frames, 10.0 s. Visual motion uses integer-cycle temporal closure
through `loop_cycles` (1-3 per seed). Dominant rotational/pulse/zoom motions are adjusted to close at the
same phase at the loop boundary.

## Audio
The previous beep-test generators are replaced by restrained deep deterministic ambient synthesis:
low drones, resonant bowl-like strikes, and family-synced slow pulses. Audio is generated independently
from C7 and muxed into the product MP4.

## Social metadata
Every generated video gets a sibling `_social.txt` with title, description, hashtags, seed/grammar/palette,
loop/audio information and the exact PowerShell reproduction command.
