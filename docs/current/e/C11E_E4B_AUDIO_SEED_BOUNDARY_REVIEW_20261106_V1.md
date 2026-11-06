# C11-E E4B Audio / Seed Boundary Review — V1

## Finding

The current family launchers are visual+optional-audio wrappers. Their default audio branch calls `C11CSafeAmbient.py` with the launcher `$Seed`, which is the visual/gameplay seed supplied as `request.seed`. The frozen music registry maps profiles by visual family and declares semantic inputs `seed` and `visual_grammar`; that registry declaration does not change the actual launcher argument wiring.

## Required D visual stage

The D visual-stage family contract sets `-NoSound` for every family. It carries `request.seed` as the C11-C visual seed and retains `request.music_seed` only in the D request identity. `request.music_seed` is not passed to the visual launcher, and the family music generator is not invoked.

## Why this is not an A/V implementation

The approved D.1 proposal is a technical audio delivery envelope only. It explicitly does not select a soundtrack, define music editorial, generate audio, infer silence, mix/duck/fade, normalize loudness or authorize audio payload materialization. Therefore a `music_seed`-bound audio call cannot be added by assumption. It needs a D-owned audio routing decision, proof that the selected existing family profile is invoked with `request.music_seed`, and the required selection/mix policy scope before audio emission/mux.

## Hard requirements

- Keep gameplay and music seeds distinct in the request and in every adapter identity.
- No audio path is allowed to consume the visual seed by accident.
- No D3 V5 for Loop.
- No C11-C code modifications.
- No audio sample emission, asset generation, materialization, mux or media creation in this phase.
