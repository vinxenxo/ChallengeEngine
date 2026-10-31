# C11-D → C11-E — full-family production roadmap (V6)

## Product outcome — mandatory

Deliver three complete production families—Challenge, Visual Loop and Visual Drill—as final, playable, reviewable audiovisual MP4s with existing C mechanics/generators and correct C presentation, enabled D9.8 editorial fields in each real family binder, D3 Music V5 generated from an independent music seed, FFmpeg mux, FFprobe validation and hash-bound provenance. GUI and CLI remain front ends to one shared C11-E production service. The CHALLENGE_001 title A/B case is the first technical control, not the final deliverable.

## Family work

- **Challenge:** existing generator, `ChallengePresentationBinder`, `UnifiedSocialFrame`, `PresentationProfile`; E-owned editorial sidecar/adaptor to independent visual slots.
- **Visual Loop:** existing grammar/generator, `VisualLoopPresentationBinder`, `C11CVisualEditorialLayer` and render model; an explicit E family adapter must pass enabled editorial fields to the existing binder.
- **Visual Drill:** existing type/tier/generator, `VisualDrillPresentationBinder`, `C11CVisualEditorialLayer` / VisualContentPlayer; preserve variant identity and the real visual model.
- Common enabled D9.8 fields: `title`, `subtitle`, `call_to_action`, `language`; Challenge-only: `player_name`, `challenge_label`. Reserved hook/preparation/final/header/footer fields and show flags remain disabled.
- D3 Music V5 is a separate seed domain: `request.music_seed` must not alias or derive from gameplay `request.seed`. FFmpeg creates the final muxed copy; FFprobe verifies streams and delivery metadata.

## Current gate state — 2026-10-31

E0 applied; E1 shared GUI/CLI service automated tests 2/2 pass, manual GUI observation pending. E2 V7 physical A/B failed at `C11EChallenge001E2.gd:62`: Godot `JSON.parse_string()` produces float Variants for JSON numbers while the E2 validator demanded integer Variants for both seeds. The failure archive documents one renderer invocation and a one-frame AVI fragment; media is not accepted and no success receipt exists. Python pair tests passed 9/9 but do not override the physical failure. V8 corrects the numeric contract and adds a Godot-native preflight before any renderer call. Installation and physical V8 execution remain pending.

## Ordered gates

1. **E2:** two isolated CHALLENGE_001 title A/B renders, without audio. Require Godot JSON numeric preflight, nonblank source AVI pair, delivery MP4 pair, FFprobe, gameplay/body identity, title-slot differences, header isolation, provenance and human review.
2. **E3:** Challenge D3 Music V5, independent music seed, FFmpeg mux and FFprobe A/V; gameplay frames must remain invariant when only the music seed changes.
3. **E4A:** complete Challenge presentation + enabled editorial + music.
4. **E4B:** complete Visual Loop presentation + enabled editorial + music.
5. **E4C:** complete Visual Drill presentation + enabled editorial + music.
6. **E5:** cross-family determinism, seed isolation, regressions and GUI/CLI parity.
7. **E6:** Smoke18, six real A/V cases per family.
8. **E7:** Matrix101: 54 Challenges + 27 Loop grammars + 20 Drill variants. CH_008/009 remain held pending explicit resolution of declared 11-second duration versus 12-second summed phases; runnable population remains 99 and must not be mislabelled 101 complete.
9. **E8:** independent acceptance, immutable freeze package and explicit promotion decision.

## Governance and engineering hygiene

C11-C 2.19.12 and its manifest remain immutable production authority until E8. Do not modify protected C generators, mechanics, simulation truth, RNG domains, source definitions, timing, C11-C manifest or D release locks. Keep only the five existing `c11c-suite` modules. No sixth module or `c11d-control`. Installer pins exact current local HEAD/parent; operator commits each iteration; runtime runners may accept descendants only with E0/E1 ancestry and exact source pins. Never reset/clean/switch/rebase/amend/push. A process exit code or manually printed PASS is not product acceptance; every physical gate needs a truthful receipt and separate content review.
