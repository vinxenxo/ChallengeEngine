# C11-E Challenge / Loop / Drill Alignment — V26

## Accepted family contracts

| Family | D9.8 canonical editable keys | Native C11-C content that must remain authoritative | Music authority |
|---|---|---|---|
| Challenge | `title`, `subtitle`, `call_to_action`, `language`, `player_name`, `challenge_label` | Challenge simulation truth, mechanics, phase/timeline, winning frame and close-call semantics; D visual presentation must not modify them | E4A Challenge D3 V5 / D3.3 isolated path, already bounded PASS_TEST_ONLY |
| Visual Loop | `title`, `subtitle`, `call_to_action`, `language` | Family + grammar identity, generated math/metrics, technobabble, seed/duration/FPS/loop-cycle telemetry, palette/family-music/version data and Matrix transitions | Existing C11-C FAMILY_MUSIC_V4; no D3 V5 |
| Visual Drill | `title`, `subtitle`, `call_to_action`, `language` | Drill identity, 4 types / 20 difficulty variants, phase and timeline semantics, END_CTA precedence, existing binder | Existing C11-C family music; no D3 V5 |

## Integration boundary

The existing D9.8 model remains the canonical editorial source. All fields stay present; blank optional strings normalize to `UNKNOWN`. Do not add per-field omission or selection semantics. Telemetry, provenance, seed domains and simulation truth are not editorial inputs.

C11-C generators, family scenes, binders, timelines, RNG, shared `C11CVisualEditorialLayer`, core audio and frozen manifest remain immutable. D integration must use the existing Producer, E1 service, D9.9 request, D9.10 bridge and existing D-only adapter boundary; no sixth module or parallel binder.

## E4A disposition

Full Challenge E4A is closed `PASS_TEST_ONLY` after E4A.6 visual review, E4A.7 A/V audit and operator listening, D99 V2 GUI correction and the new manual GUI/CLI parity run `D99-GUI-37559C528640`. Do not reopen absent actual regression.

## E4B disposition

Visual Loop is in source/contract audit. The five family producer scenes each mount the shared C11C editorial layer. The integration gap is not a missing C11C layer; it is that E1's four resolved D editorial values are not yet consumed by a Loop family adapter. The current field-window policy is proposed, not approved; it must be reconciled with the already occupied C11-C header/footer before any pixels change.

Loop family music must keep the C11-C family/grammar/profile generator. Because the current C11C prototype wrapper reuses one seed for visuals and audio, D orchestration must pass the gameplay seed to silent visual capture and the independent music seed to the same C11C audio wrapper. The C11C generator itself stays unchanged.

## E4C future boundary

Drill begins only after Loop acceptance. Preserve all four drill types / 20 difficulty variants, phase timing, END_CTA precedence, family binder and existing C11-C music route. Do not transfer Loop-specific assumptions to Drill.

## Governance

Frozen C11-C manifest remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; renderer OFF, dispatch/media OFF, and `release_authority=NONE`.
