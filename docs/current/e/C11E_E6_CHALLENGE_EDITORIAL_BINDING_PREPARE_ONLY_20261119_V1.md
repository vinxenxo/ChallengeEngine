# E6 Challenge Editorial Binding — PREPARE_ONLY V1

**Date:** 2026-11-19  
**Disposition:** `IMPLEMENTED_PREPARE_ONLY_OVERLAY / AWAITING_ACTIVE_CHECKOUT_EXECUTION`

## Operator decision: zero-second editorial intervals

Operator clarified and approved on 2026-11-19 that a Challenge mechanic may assign 0 seconds to HOOK or CTA because that mechanic does not require the associated editorial to appear. This is intentional behavior. It is not a missing field and must not be remedied by fallback to GAME.

The existing E4A approval policy V1 is unchanged:

- `title` and `subtitle`: HOOK only.
- `call_to_action`: CTA only.
- If the selector's canonical phase interval contains zero frames (`start_frame == end_frame`), the corresponding field is `OMITTED_EMPTY` with an empty effective value and SHA-256 of the empty string.
- If the interval contains one or more frames, the synthetic E6 family value is `READY_FOR_ISOLATED_TEST_PIXEL_DRAW`.
- All source phase boundaries, FPS, total frames and half-open ranges are copied unchanged. No field migrates to GAME.

## Inputs

- Family editorial fixture: `a63aeb9b97be29c716d6ab8a1f303ef66843a5eb9fb4f972a4ac6cd89f0a78aa`.
- Family editorial plan: `9ea1508c631a06d82dcedcd02c03c2481849a3b5d82a25aa70cce8077562c5ca`.
- Family editorial audit receipt: `819b953246702e0e70104bb11e00279e225f83a0a8652e123d7532a27c39fe64`.
- Challenge PREPARE_ONLY receipt: `b54a884f1574d22fa65ea198d279d9ba84bb3967adc87885213f7659a1b1c944`.
- Challenge PREPARE_ONLY plan: `c645e4d34c79b1c18875d58078893ccd13838312b995bc925e0fb3b57133be8b`.
- E4A policy approval V1: `764629384896a255cf992da89fa427c19f60f9b2e623b81ad17d909674b466b5`.
- D1.5 layout contract: `3a8e7bfc13a369acaf9d5abe9583f3e93e0990a3b1262b8a839e81ee873c6461`.
- Challenge live consumer: `eba81fff4c24ca75033c8f963665df1961136046c41fee0e88681fe55a631203`.
- Challenge adapter: `d17568882eb63ba2eb48649cb9cd46edafe122d72c0c5ed29275e79b8d6d5846`.

## Selector/timebox matrix

| Selector | HOOK | CTA | Title/subtitle | CTA |
|---|---:|---:|---|---|
| CHALLENGE_001 | 0 s | 2 s | Intentionally omitted | Visible |
| CHALLENGE_002 | 3 s | 0 s | Visible | Intentionally omitted |
| CHALLENGE_004 | 3 s | 2 s | Visible | Visible |
| CHALLENGE_005 | 0 s | 0 s | Intentionally omitted | Intentionally omitted |
| CHALLENGE_006 | 0 s | 2 s | Intentionally omitted | Visible |
| CHALLENGE_007 | 3 s | 0 s | Visible | Intentionally omitted |

The same mapping applies to A, B_REPEAT and C_CHANGED_MUSIC_SEED. Across 18 probes and 54 title/subtitle/CTA field slots, expected counts are 27 visible and 27 intentionally suppressed.

## Executable increment

`tools/c11d/d9/c11e_e6_challenge_editorial_binding_prepare_only_v1.py` and its PowerShell 5.1 runner:

1. Revalidate source pins, predecessor receipts and sidecars.
2. Revalidate the six Challenge selectors and their exact A/B/C input envelope/intent hash links.
3. Revalidate canonical phase ranges against the Challenge PREPARE_ONLY group plan.
4. Derive 18 test-only D envelopes. It updates only three D-side field rows; embedded E1 intents, outer intent hashes, source-timebase and all phase ranges remain unchanged.
5. Emit one manifest and one receipt with sidecars under `artifacts/tests/c11e/e6_challenge_editorial_binding_prepare_only/<RUN_ID>/`.

The original Challenge PREPARE_ONLY envelopes/intents and E1 canonical fields remain unchanged. `player_name` and `challenge_label` remain unknown/blocked or omitted; E1 music `tempo_bpm` and `duration_seconds` remain null. The family copy remains synthetic TEST_ONLY text.

## Expected output and limits

Expected output: `PASS_PREPARE_ONLY_18_CHALLENGE_ENVELOPES_27_VISIBLE_27_SUPPRESSED`.

This does not prove actual Godot consumer readback or pixel output. No Godot, FFmpeg, FFprobe, renderer, audio, mux, media, dispatch or BatchId is invoked. D4.8 V2 remains immutable/BLOCKED; E6 TEST_ONLY media execution is not authorized; renderer OFF; E6 accepted 0; Matrix not frozen; release authority NONE.

## Next phase after this receipt

Build an explicitly bounded Challenge live-consumer readback path using the 18 derived D envelopes. Before any engine invocation, revalidate the relevant D4.8 successor-policy and E6 runtime authorization gates. A prepare-only PASS is not permission to invoke Godot or create media.
