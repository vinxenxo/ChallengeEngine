# C11-D / C11-E — Family Presentation and Editorial Alignment — V2

## Product intent

Bring the mature C11-C Visual Loop / Visual Drill presentation, editorial/layout and music foundations to Challenge. The eventual D+E result is one production factory, not three parallel renderers. C11-C 2.19.12 remains production authority until E8 and explicit promotion.

## Shared orchestration, distinct family semantics

- **Shared E1:** request normalization, D9.8 editorial resolution, request-scoped presentation options, provenance, intent sealing, result receipt and GUI/CLI semantic parity.
- **Challenge:** retain the C Challenge HOOK/GAME/REVEAL/CTA timeline and countdown truth; use D-owned editorial presentation and D3 Music V5.
- **Visual Loop:** retain the Loop binder, grammar/variant timing and current C11-C family-aware music.
- **Visual Drill:** retain the Drill binder, type/tier timing, PRE_ROLL/GAME/END_CTA precedence, existing editorial semantics and C11-C family music.

## Challenge request option

E1 schema version 1.1 remains compatible. Challenge requests may carry `presentation_options: { show_hook_countdown: boolean }`; omission defaults to true. The existing GUI checkbox is scoped to Challenge and is serialized through E1. The canonical D9.9 planner receives a sanitized request without the E1-only option; E1 CLI receives the full request. GUI/CLI parity compares the sealed option. Older E1 Challenge intents without the field remain valid under their original semantic hash. Loop/Drill requests omit the field and preserve their prior semantics.

This option is currently a sealed request contract. Pixel consumption by the D visual adapter remains a separate E4A task; do not claim the checkbox changes rendered pixels until the isolated consumer test proves it.

## Editorial fields and presentation policy

Common fields: `title`, `subtitle`, `call_to_action`, `language` (metadata-only). Challenge mapping is title/subtitle → HEADER/HOOK and call_to_action → FOOTER/CTA. Empty/unset values are omitted. Challenge-only `player_name` and `challenge_label` remain blocked until geometry authority exists. Countdown/hook ON with editorial is an intentional supported arrangement.

## Protected boundary

Do not modify C11-C binders, mechanics, RNG, `SimulationResult`, `winning_frame`, `close_calls`, `RenderedFrameStream`, `FrameSnapshot.custom_data`, `core/audio`, the frozen manifest or D governance locks. Do not add a parallel binder/renderer or sixth suite surface. Preserve `release_authority=NONE` until E8 and separate approval.
