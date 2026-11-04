# C11-D / C11-E — Family presentation and editorial alignment — V1

## Product intent

C11-D/C11-E exists to bring the mature C11-C presentation, editorial/layout and music advances already used by Visual Loops and Visual Drills to the Challenge mechanics. It is not a project to invent three new, unrelated rendering stacks. D+E will become the replacement video-production factory only after E8 and explicit governance promotion; until then C11-C 2.19.12 remains production authority.

## Shared and family-specific responsibilities

**Shared E1 service:** request normalization, D9.8 editorial resolution, selected presentation options, provenance, family dispatch, result receipt and GUI/CLI semantic parity.

**Family-specific visual layer:**
- Challenge keeps Challenge HOOK/GAME/REVEAL/CTA phase truth and countdown semantics; add the D-owned editorial consumer.
- Visual Loop keeps its grammar/variant-aware presentation binder and existing footer/editorial omission behavior.
- Visual Drill keeps its type/tier binder, PRE_ROLL/GAME/END_CTA precedence and terminal CTA behavior.

**Family-specific music:**
- Challenge uses D3 Music V5.
- Visual Loop and Visual Drill retain their existing C11-C family-aware music routes. Do not substitute the Challenge 8-bit profile for them.

## Editorial field rules

Common editable fields: `title`, `subtitle`, `call_to_action`, `language` (metadata-only). Challenge-only fields `player_name`, `challenge_label` remain blocked until geometry/region authority exists. Mapping approved in Challenge policy V1: title/subtitle → HEADER/HOOK; call_to_action → FOOTER/CTA. Empty/unset text is omitted, not replaced by placeholders or old phase text. Text values are flexible per request and per Challenge; the system must render supplied values correctly without requiring every field to be populated.

## Visibility and test rules

Hook/countdown visibility is a separate presentation option. Countdown ON may intentionally display the historical hook together with D editorial. Countdown OFF suppresses that hook; it does not change gameplay frames, mechanics, phase timings or music. The future GUI checkbox serializes a request-level option consumed by E1.

Test a compact, evidence-grounded matrix rather than a Cartesian product. At minimum include countdown ON/OFF; the operator-reviewed hook + CTA only case; title/subtitle present with CTA omitted; CTA present with title/subtitle omitted; and other historical Challenge arrangements only where source definitions/binders/profiles/receipts prove they exist. Verify phase-specific visibility, field omission, body/source identity and determinism.

## Protected boundary

Do not modify C11-C binders, mechanics, RNG, `SimulationResult`, `winning_frame`, `close_calls`, `RenderedFrameStream`, `FrameSnapshot.custom_data`, `core/audio`, frozen manifest or D governance locks. Add only a D-owned adapter/consumer once its live call site is source-pinned. One service, no parallel binder, no second renderer or sixth suite module.