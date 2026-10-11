# D9 — Unified audio/music delivery proposal integration record

Date: 2026-10-11

## Change

Added `D_RENDERER_UNIFIED_AUDIO_MUSIC_DELIVERY_POLICY_PROPOSAL_V1` with a strict schema and deterministic Python preview/test. The proposal reads the pinned `REVIEW_720` delivery-registry audio envelope and cross-checks its exact 48 kHz pre-encode sample-count arithmetic against the existing unified delivery-timebase proposal for all three content types.

Integrated the preview into the unified review as `unified_audio_music_policy`, added `unified_audio_music_policy_parity`, expanded source lineage from 18 to 19 pinned contracts, and recorded a new open gate for audio delivery/music editorial decisions.

## Core proposal facts

- Loops: 20 s, 960,000 pre-encode PCM samples at 48 kHz.
- Drills: 21 s, 1,008,000 pre-encode PCM samples at 48 kHz.
- Challenges: 15 s, 720,000 pre-encode PCM samples at 48 kHz.
- Delivery-registry envelope: AAC-LC, 192 kb/s, 48 kHz, stereo.
- No music asset selected, no assumption of silence, no audio payload, no PCM samples and no encoded media.

## Deliberate boundary

Music asset selection/licensing, family-specific music, SFX, mixing, ducking, fades/loops/crossfades, loudness/normalization, encoder priming and post-encode duration tolerance remain undefined. The new contract is not renderer input and is not an approval.

## Governance stays locked

C11-C and its freeze manifest are unchanged. Renderer remains OFF; media remains absent; D4.8 remains blocked; renderer baseline approval/freeze, D9.14/D9.16 acceptance, D9.17 closure and D10 remain blocked; release authority remains NONE.
