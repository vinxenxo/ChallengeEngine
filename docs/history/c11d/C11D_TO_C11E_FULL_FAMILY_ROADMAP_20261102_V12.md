# C11-D to C11-E Full-Family Production Roadmap — V12

**Date:** 2026-11-02
**Purpose:** Govern completion of the full production product while preserving C11-C 2.19.12 until E8.

## Product definition

C11-E is not a CHALLENGE_001-only deliverable. It must produce all three families through the existing C11-C generator/mechanics plus the D presentation/editorial layer and D3 Music V5:

1. Challenge
2. Visual Loop
3. Visual Drill

One shared production service is the execution boundary for both CLI and GUI. Final MP4 output must carry editable editorial fields and the independently seeded soundtrack, with FFmpeg mux and FFprobe validation. Existing C11-C generation logic and protected mechanics are preserved.

## Gate sequence

| Gate | Scope | Exit evidence |
|---|---|---|
| E0 | Foundation/re-entry and immutable baseline identity | Existing accepted V2 receipt; no regeneration |
| E1 | Shared production service; same service adapter for CLI and GUI | Automated contract tests and required GUI observation; no duplicate pipelines |
| E2 | D presentation/editorial rendered to pixels; title-only A/B control | Numeric/contract tests, two physical renders, gameplay-pixel invariance, title-slot differences, final delivery metadata, operator visual sign-off |
| E3 | D3 Music V5 | Independent `request.music_seed`; deterministic soundtrack selection/render; changing music seed changes audio only; FFmpeg mux; FFprobe A/V metadata/duration/offset/synchronization validation; negative cases |
| E4A | Challenge adapter | Family-level adapter contract and representative physical output through shared service |
| E4B | Visual Loop adapter | Family-level adapter contract and representative physical output through shared service |
| E4C | Visual Drill adapter | Family-level adapter contract and representative physical output through shared service |
| E5 | Cross-family determinism, seed isolation, CLI/GUI parity | Same canonical requests/plans; gameplay unaffected by music seed; repeatability and parity across all three families |
| E6 | Smoke18 | 6 Challenge + 6 Visual Loop + 6 Visual Drill |
| E7 | Matrix101 | 54 Challenge + 27 Visual Loop + 20 Visual Drill |
| E8 | Independent acceptance, freeze, promotion | Separate independent decision artifacts, source pins, final manifest/tree checks, formal approval |

## Current position

- E2 R4 automated acceptance: PASS.
- E2 independent sampled visual inspection: no obvious defects observed.
- E2 operator full-playback approval: PENDING.
- E3: PREPARE_ONLY. No audio render or mux is authorized by R4.
- E4A/B/C and later phases: BLOCKED until upstream gates close.

CH_008 and CH_009 remain excluded from the currently valid E7 set because each is declared as 11 seconds while its phase sum is 12 seconds (`3+7+0+2`). Do not silently change a duration or phase; require explicit authority. The present valid total is 99 if the discrepancy remains unresolved.

## E3 D3 Music V5 preflight — next technical work after E2 sign-off

1. Re-read active-checkout source-of-truth, D3 Music V5 specification, schema, implementation, tests, validators and existing source pins. Do not rely on filenames or prior memory alone; resolve actual current paths and hashes.
2. Establish exact contract for music seed input, deterministic selection/render, audio artifact, duration policy, mux parameters and FFprobe expectations. Preserve `request.music_seed` as an independent domain from `request.seed`; no automatic generation or cross-domain RNG consumption.
3. Write a read-only E3 preflight and acceptance matrix before changing implementation. List positive/negative cases and exact required output fields.
4. Prove repeated identical requests with the same music seed produce the same musical selection/output. Prove that changing only music seed changes the audio result while the gameplay render remains pixel-identical.
5. Mux generated audio into the existing generated video with FFmpeg using the repository's governed D3 contract. Validate video/audio codec, sample rate, channel count, stream starts, durations, offsets, end alignment and synchronization with FFprobe. Verify audio is not truncated.
6. Exercise invalid/missing seed, missing/invalid audio asset/configuration, duration/synchronization failures and other negative cases specified by the current D3 contract.
7. Keep every physical attempt on a fresh RequestId and preserve failed outputs. No baseline promotion, no release authority and no family expansion as a side effect of E3.

Do not invent music provider, file formats, codecs, sample rates, fades, or duration rules before reading the actual D3 Music V5 source contract. The above is a verification checklist, not permission to redesign D3.

## Permanent constraints

- `release_authority=NONE` before E8.
- C11-C 2.19.12 remains frozen and authoritative.
- No mutation to protected C11-C mechanics/generators or the frozen manifest.
- No `c11d-control`; work within the governed `c11c-suite` and shared production service.
- `winning_frame` remains only a temporal anchor; `close_calls` remains only an episode count.
- Do not claim all-family readiness from a single Challenge variant.
