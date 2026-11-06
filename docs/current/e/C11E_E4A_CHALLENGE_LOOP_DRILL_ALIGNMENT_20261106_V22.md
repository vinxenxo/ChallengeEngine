# C11-E Challenge / Visual Loop / Visual Drill Alignment — V22

The deliverable remains one GUI+CLI C11-E factory serving Challenge, Visual Loop and Visual Drill without flattening family-specific mechanics, binders, timelines or music ownership.

## Challenge (current priority)

- E4A.6 visual/reserved-band subgate: PASS_TEST_ONLY from Recovery V1.2; user-reviewed black reserved bands, HOOK/HEADER title/subtitle and CTA/FOOTER behavior.
- E4A.7 A/V test: ready for execution; final outcome is governed by the runtime receipt. It adds D3 V5 Challenge music and D3.3 mastering to the already-composited silent Challenge MP4; video H.264 must remain stream-copy identical. A/B music seed repeated; C music seed changed; gameplay seed unchanged.
- Challenge E1 intents use explicit `presentation_options.show_hook_countdown=true`; this remains a request-scoped option, not a sixth operational surface or a new renderer.
- Full E4A acceptance additionally requires operator listening review and GUI/CLI parity through the shared E1 service.

## Visual Loop

Retain the existing C11-C Loop grammar/variant timeline, binder and family-specific music path. D editorial/layout integration is carried through the correct Loop consumer; do not route Loop audio through Challenge D3 V5.

## Visual Drill

Retain C11-C Drill phase timeline, binder, END_CTA precedence and family-specific music path. Do not flatten Drill into the Challenge consumer or replace existing Drill music with D3 V5.

## Shared editorial and delivery

Shared optional fields remain `title`, `subtitle`, `call_to_action`; empty values remain omitted by their consumers; language is metadata-only. Challenge-only `player_name` and `challenge_label` remain blocked pending geometry authority. Header/footer reserved-black behavior is scoped to the enabled D envelope; BODY and no-envelope legacy C behavior remain unchanged.

## Ordered progression

Complete E4A.7 D-composited A/V → operator audio review + E1 GUI/CLI parity → full E4A acceptance → E4B Loop → E4C Drill → E5 → E6 Smoke18 → E7 Matrix101 → E8 independent historical regression/freeze/separate promotion. C11-C remains immutable production authority until E8 and separate approval.
