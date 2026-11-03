# C11-D to C11-E Full-Family Production Roadmap — V14

**Date:** 2026-11-03
**Supersedes:** V13 as the current sequencing and GUI-operation roadmap.
**Production baseline:** C11-C 2.19.12 until E8.

## Product acceptance target

Create finished audiovisual MP4s on demand for Challenge, Visual Loop and Visual Drill. Preserve the C generators, mechanics, timing, frame stream, simulation truth and source assets. Add D presentation and editable editorial values in the correct family-specific visual consumer, music generated from a separate music seed, FFmpeg A/V assembly, FFprobe QA and hash-bound E receipts.

Producer GUI is the only manual operational workflow from this implementation onward. GUI and CLI continue to call one shared C11-E production service; CLI is retained as a thin separate-process compatibility/test interface only. Do not build parallel business logic or a sixth suite module.

## Gate sequence

| Gate | Scope | Exit evidence |
|---|---|---|
| E0 | Foundation, ancestry and immutable C baseline | Accepted E0 V2 receipt; reuse only |
| E1 | Shared service / GUI-CLI common semantics | Automated service tests accepted; record live GUI bring-up separately |
| E2 | Challenge title-to-pixels A/B | R4 receipt, read-only reconciliation, full 540-frame decoded visual audit and separate closure V1; accepted only for CH001 title slot |
| E3 | Challenge audio integration | D3 V5 raw WAV, separate music seed, D3.3 mastering, FFmpeg mux, FFprobe, deterministic/negative cases, unchanged visual stream, GUI runtime and CLI compatibility |
| E4A | Challenge presentation/editorial | Allowlisted Challenge fields through real Challenge binder and verified slots/layout |
| E4B | Visual Loop | Loop adapter/binder, editorial slots and existing family/grammar music generation |
| E4C | Visual Drill | Drill adapter/binder, phase-aware editorial slots and existing Drill music generation |
| E5 | Cross-family determinism and parity | Independent seeds, repeatability, output/receipt parity through GUI and CLI shared service |
| E6 | Smoke18 | Six full audiovisual cases per family, all with GUI-origin jobs and machine receipts |
| E7 | Matrix101 | 54 Challenge + 27 Loop + 20 Drill; resolve CH008/009 timing first |
| E8 | Independent final acceptance, freeze and promotion | Complete receipts, provenance, visual/audio QA, hashes, formal freeze and explicit promotion authority |

## Music strategy by family

- **Challenge:** D3 Music Engine V5 + `challenge_8bit_v1`; E3 proves raw determinism, D3.3 delivery mastering and mux.
- **Visual Loop:** preserve C11-C family/grammar-aware generator and its declarative music profile. The E adapter may invoke its existing audio-only entry point with the independent `request.music_seed`; do not edit or fork the generator.
- **Visual Drill:** preserve the C11-C Drill family profile, global harmonic bed, phase/end-CTA envelope and existing generator. The E adapter may invoke its existing audio-only entry point with `request.music_seed`; do not alter the generator or its phase/timing semantics.

This is one shared **orchestration contract**, not one forced waveform for every family. D3.0/D3.1's non-interference clauses and C11-C family profiles take precedence over any assumption that V5's Challenge 8-bit profile should replace all family music. The broader product-scope statement that mentions D3 for all families remains a recorded ambiguity; no family migration to V5 is permitted without a new versioned style profile, comparative listening/QA and explicit decision.

## Editorial and layout

D9.8 common enabled fields: `title`, `subtitle`, `call_to_action`, `language`; Challenge-only: `player_name`, `challenge_label`. Reserved hooks, preparation/final fields, header/footer lines and `show_*` flags remain disabled. Never map `title` to `hook` or CTA.

Logical layout remains 540×960 with Header 0–144, Body 144–816, Footer 816–960. Delivery target REVIEW_720 is 720×1280 at 30 fps. The E2 CH001 title slot is proven only for CH001. Challenge, Loop and Drill each require verified mappings, text fit/safe-area checks and frame-level regression. Preserve Loop's production footer omission and Drill's phase/END_CTA precedence.

## Matrix qualification

Target: 54 Challenge + 27 Loop + 20 Drill = 101. CH_008 and CH_009 are two held Challenge cases because each declares 11 seconds while the phase sum is 12 seconds (`3+7+0+2`). Provisional runnable population: 52 Challenge + 27 Loop + 20 Drill = 99. V13's `54+27+18` parenthetical is inconsistent with the declared inventory and is treated as a documentation arithmetic error, pending confirmation against the live catalog before E7.

## Permanent governance

- Frozen C11-C manifest: 796,318 bytes / `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; immutable.
- Keep five `c11c-suite` modules. No `c11d-control`, sixth surface or second Producer.
- No protected C source, mechanics, RNG, media contracts or release manifest mutation.
- `request.seed` and `request.music_seed` remain separate. No automatic seed creation or cross-domain RNG consumption.
- Every physical E run gets a fresh RequestId, isolated output root, immutable receipt and exact source/media hashes.
- `release_authority=NONE`, `baseline_promotion=false`, `freeze_eligible=false` until E8.
