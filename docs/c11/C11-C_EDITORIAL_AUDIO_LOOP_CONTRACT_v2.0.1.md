# C11-C Editorial + Audio + Loop Contract v2.0.1

## Header

Two large lines inside the existing 468 px safe width.

Line 1: real variant data, e.g. `TOPOGRAPHIC_BASIN | 79 TRACES | PULSE 1.15`.
Line 2: user-facing hook. Around the midpoint, line 2 uses a deterministic Matrix / split-flap / airport-board character transition to show `VISUAL LOOP / FAMILY`, then returns to the hook before the loop closes.

## Footer

Small review-only telemetry: family, technobabble, seed, Body, duration, actual generation variables, palette, loop count, audio mode, signature. Production may disable footer with `-NoFooter`.

## Audio

ON by default. `-NoSound` disables audio generation and muxing. Audio is procedural, slow, deep, meditative and family-synchronized; it is not a replacement for C7 and does not modify C7.

## Duration / Loop

Review/production baseline: 18.0 s at 30 FPS = 540 frames. Each variant chooses an integer number of complete loop cycles (1..3). Visual and audio oscillators use periodic normalized time so frame 0 and the end boundary close as a loop.

## Social sidecar

Every successful video generation creates a sibling `_social.txt` containing title, description, hashtags, exact variant information and the exact PowerShell reproduction command.
