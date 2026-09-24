# C11-C Visual Drill Audio Direction v2.0

## Objective

Create a single global ambient language that accompanies eye-movement training without becoming distracting on phone speakers or revealing mechanical event timing.

## Canonical profile

`drill_motion_ambient_v2`

One master is shared by all four Visual Drill families.

## Sound design rules

- soft harmonic bed;
- low-mid focus;
- no kick/snare or sharp transient layer;
- limited high-frequency content;
- slow breathing modulation that is not synchronized to authored events;
- correlated stereo movement only;
- gentle harmonic settling in the final 3 s for END_CTA;
- deterministic PCM generation;
- `-NoSound` remains a hard disable.

## Mobile safety target

The review master intentionally avoids extreme sub-bass and harsh upper-band energy. The musical motion is perceived primarily as a continuous harmonic field rather than as a beat.

## Relationship to C7

C7 audiovisual contracts remain frozen. This document specifies the C11-C review-layer ambient generator and its production profile; it does not reopen C7 deterministic audio schemas or gates.
