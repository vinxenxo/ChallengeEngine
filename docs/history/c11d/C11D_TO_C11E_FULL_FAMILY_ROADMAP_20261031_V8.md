# C11-D → C11-E complete-family delivery roadmap — V8

## Product acceptance target

The target is a production-capable service that creates finished MP4s on demand for all three C11-C families: Challenge, Visual Loop and Visual Drill. Preserve existing C generators, mechanics, timing and frame stream. Add the approved D presentation/editorial surface and D3 Music V5, use the correct family binders/adapters, independent gameplay/music seed domains, FFmpeg mux and FFprobe validation. GUI and CLI share one production service. CHALLENGE_001 A/B validates an initial seam; it is not the product.

## Current E2 checkpoint (2026-11-01 handover)

- E2 V7 physical A render failed with Godot exit 40 during sidecar validation. Failure evidence retained; no acceptance.
- E2 V8 numeric preflight did not emit required PASS markers; not accepted.
- E2 V9 V1 installer failed before writes because the GDScript in the checkout matched the V9 target postimage, but the installer required the V8 preimage. V9 V2 fixes installer idempotence via strict preimage/postimage/unknown-state classification.
- Do not start a physical render before the standalone Godot test produces a structured 30/30 PASS.

## Ordered delivery gates

1. **E2:** two isolated CHALLENGE_001 A/B renders without audio; prove editorial title affects only the intended title slot, gameplay/body remains pixel-identical, regions outside slot remain stable, output media metadata and source provenance are valid; perform independent human visual review.
2. **E3:** implement Challenge D3 Music V5 using `request.music_seed`, independent from gameplay `request.seed`; FFmpeg mux, FFprobe stream validation; verify gameplay invariance when only music seed changes.
3. **E4A Challenge:** integrate approved presentation/editorial fields through the real Challenge binder; keep title, subtitle, call_to_action and language as editorial fields; Challenge-only player_name/challenge_label where approved.
4. **E4B Visual Loop:** implement family adapter and `VisualLoopPresentationBinder` integration with `C11CVisualEditorialLayer`/render model, correct editorial slots and music.
5. **E4C Visual Drill:** implement family adapter and `VisualDrillPresentationBinder` integration with `C11CVisualEditorialLayer`/VisualContentPlayer, correct editorial slots and music.
6. **E5:** deterministic output, independent seed domains, controlled variation, shared CLI/GUI request/result parity.
7. **E6 Smoke18:** six complete audiovisual production cases per family, 18 total.
8. **E7 Matrix101:** 54 Challenges + 27 Loop grammars + 20 Drill variants. CH_008 and CH_009 remain held while declared 11 s conflicts with phase sum 12 s; do not claim 101 runnable until timing is authority-corrected.
9. **E8:** independent acceptance, complete freeze package and explicit production promotion. Until E8, C11-C 2.19.12 remains the release baseline.

## Editorial/music constraints

Common enabled D9.8 fields: `title`, `subtitle`, `call_to_action`, `language`. Challenge-only: `player_name`, `challenge_label`. Reserved hook/preparation/final/header/footer fields and visibility flags remain disabled. Never map title to hook or CTA. Music seed is independent from gameplay seed; all final outputs must be FFprobe-checked for expected streams, codec, dimensions, frame rate, duration and audio/video presence.

## Architecture/governance

Work within existing five `c11c-suite` modules; no `c11d-control`. One canonical C11-E production service handles GUI and CLI. Do not alter frozen C11-C manifest or protected generator/mechanics paths. No bypass of D locks or E acceptance. Installers/runtime runners require source hashes, ancestry, receipts, immutable evidence and exact per-gate results. User local commits every iteration are expected.
