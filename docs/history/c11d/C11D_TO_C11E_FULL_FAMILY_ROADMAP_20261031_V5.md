# C11-D → C11-E — full-family production roadmap (V5)

## Product outcome

Deliver three complete production families—Challenge, Visual Loop and Visual Drill—as final, playable, reviewable MP4s with the C presentation, D9.8 enabled editorial fields in the correct family binder, D3 Music V5 generated from an independent music seed, FFmpeg mux and FFprobe validation. GUI and CLI remain front ends to one shared C11-E production service. Existing C11-C generators and mechanics remain authoritative; C11-C stays production baseline until E8 formally accepts and promotes E.

## Family work

- Challenge: existing Challenge generator, `ChallengePresentationBinder`, `UnifiedSocialFrame`, `PresentationProfile`.
- Visual Loop: existing grammar/generator, `VisualLoopPresentationBinder`, `C11CVisualEditorialLayer` and render model.
- Visual Drill: existing type/tier/generator, `VisualDrillPresentationBinder`, `C11CVisualEditorialLayer` / VisualContentPlayer.
- Common enabled editorial fields: title, subtitle, call_to_action and language. Challenge-only: player_name and challenge_label. Reserved hook/preparation/final/header/footer fields and show flags remain disabled. Loop/Drill require E adapters; do not pretend D9.9 universal request support already exists.
- Audio is a separate D3 Music V5 lane: `request.music_seed` is independent from `request.seed`; final FFmpeg mux and FFprobe A/V check.

## Gates

E0 baseline/governance reconciliation APPLIED; E1 shared GUI/CLI service code and automated tests PASS, GUI operator observation pending. E2 currently validates Challenge title-to-pixels using two CHALLENGE_001 A/B renders, no audio. V5 failed at a summary/receipt property lookup. V6 passed pair tests but generated a uniform grey AVI because Godot failed GDScript compilation. V7 V2 corrects the Variant parse issue, adds fatal script-load detection and pixel-content probes, and fixes commit-per-iteration identity handling. Installation/physical E2 retry are pending.

After E2 acceptance: E3 D3 audio/mux; E4A Challenge integration; E4B Loop adapter/integration; E4C Drill adapter/integration; E5 determinism, seed isolation and GUI/CLI parity; E6 Smoke18 (six per family); E7 Matrix101 (54 Challenges +27 Loops +20 Drills). CH_008/009 remain held while declared 11 s conflicts with 12 s summed phases; runnable population 99, do not label it 101 complete. E8 independent acceptance, freeze and explicit promotion.

## Governance

Do not modify protected C generators, mechanics, Challenge definitions, RNG domains, structural fields, C11-C manifest or D release locks. No `c11d-control` or sixth module. Renderer/media authority remains gate-scoped. Every package pins current local HEAD/parent. Operator local commits each iteration are expected; subsequent runners record active HEAD/parent, validate E1/E0 ancestry and exact code pins. Never reset/clean/checkout/rebase/amend/push to satisfy a gate. Each later installer is rebuilt against the latest committed identity.
