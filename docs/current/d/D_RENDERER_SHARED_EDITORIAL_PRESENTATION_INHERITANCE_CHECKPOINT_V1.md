# D9 shared editorial/presentation inheritance checkpoint V1

Status: `ARCHITECTURE_CONTRACT_PROPOSAL_NOT_RENDERER_INPUT`.

## Decision

C11-D will keep one canonical editorial model and one common presentation contract across supported content types and registered families. A family adapter adds family-specific identity and visual parameters; it does not duplicate the editorials or redefine the shared presentation contract.

## Future producer GUI contract

The canonical D9.9 selector dimensions remain `content_type`, `family_id`, `subtype_id`, and `variant_id`; editorial settings remain `editorial_profile` and `production_override`. The future GUI and CLI use the same canonical backend. Unknown selector tuples and fields reject without silent fallback.

The shared editorial inheritance order is the current D9.8 order: `global → content_type → family → subtype → variant → production_override`. The enabled shared fields are `title`, `subtitle`, `call_to_action`, and `language` (metadata, not display text). `player_name` and `challenge_label` remain enabled only for Challenges. Reserved fields and show/hide flags remain disabled.

## New family default

A family must be registered before its selector is accepted. Once registered, it inherits the common editorial and presentation contracts by default. A family-specific exception is permitted only through a separately versioned, hash-bound declaration with explicit approval. An exception cannot silently enable reserved fields, rewrite global field semantics, or change seed/simulation/provenance identity.

## Current evidence boundary

- Challenges: canonical D4 subplan/preview route only; no renderer payload.
- Visual Loops: `c11c_geometric_waves_v1 / harmonic_membrane` has a verified parameter instance, but its exact selector visual payload and family authoring envelope remain unresolved.
- Visual Drills: canonical editorial-intent plan only; family visual adapter is not certified here.
- The presentation profile is passed as a canonical reference. Geometry, semantic regions, frame program, and editorial windows remain unapproved or unapplied.

## Guardrails

This is a static, read-only architecture audit. It does not create renderer input, instantiate a renderer, execute shaders, create media, approve policy, or mutate C11-C. `renderer=OFF`, `media_created=false`, `D4.8=BLOCKED`, `release_authority=NONE`, D9.17 NO-GO, D10 BLOCKED.
