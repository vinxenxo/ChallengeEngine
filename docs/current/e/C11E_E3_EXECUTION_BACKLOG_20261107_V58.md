# C11-E Execution Backlog — V58

**Date:** 2026-11-07. Reconciled to V80 evidence. This version removes already completed items from the immediate queue.

## Accepted — do not repeat absent regression

- E4A D99 GUI runtime fixture `D99-GUI-37559C528640`: E1 parity PASS, D9.10 parity PASS, lifecycle PASS_PLAN_ONLY; no renderer/dispatch/media.
- E4A.6 Challenge live-root consumer test-only runtime PASS.
- E4A.7 D-composited Challenge A/V test-only PASS; user visual review and A/B/C listening PASS.
- E4B V3 recovery receipt and V3 shared-service runner: recovery PASS; 25/25 shared-service tests; 27/27 Loop selectors; D9.8 model PASS; syntax PASS; source postimages 6/6.
- D9.15 `PASS_CLOSED`, 13/13 pairings.

Do not rerun these stages or ask the operator to locate the D99 folder; it is present in V80.

## Immediate engineering task — E4B-R1P

Create a D-owned, request-scoped parameter payload materializer for all 27 explicit Visual Loop grammars. Use the existing E1 shared service and validated D9.10 family-stage contract as the request identity and selection authority. Use the C11-C VariationProfile, PaletteBank and VisualLoopDuration deterministic APIs without instantiating prototypes/renderers or emitting media.

Deliverables: 27 unique selector receipts; exact source pins; full family-specific variation recipe; explicit grammar override; full resolved palette; duration/FPS/planned frame count; separate seed domains; repeat hash; all non-execution assertions. Validate family grammar order against the canonical producer schema and each family profile/prototype contract. The existing geometric-only V2 authoring harness is not all-family evidence.

Use `policy_seconds_for_cycles()` rather than `resolve()` for canonical timing, because `resolve()` reads the `C11C_DURATION_SECONDS` environment override. Planned timing is 30 FPS and 600/660/690 frames for 20/22/23 seconds; do not label these as rendered/captured frames.

Full plan: `C11E_E4B_R1P_REQUEST_SCOPED_FAMILY_PARAMETER_PAYLOAD_PLAN_20261107_V1.md`.

## Later — gated

1. R1V actual source-frame/pixel payload and inventory — blocked until D4.8 independently authorizes renderer execution.
2. R2 D-only pixel consumer at the existing D9.10 seam — after R1V, exact frame identity/order preservation and composition proof.
3. Five silent family pilots and Loop 27 visual acceptance — only after R1V and D4.8 authority.
4. Existing family music uses `request.music_seed` independently; visual runs use `request.seed` and `-NoSound`; then mux, FFprobe and A/V QA.
5. E4C Drill preserves its distinct timeline/binder/music contract; then E5, Smoke18, Matrix101 (CH_008/009 remain held; 99 provisional), E8 independent acceptance/freeze and separate promotion.

## Baseline reconciliation remains separate

`GeneradorMaestro.gd` is a known E4A.6 D-only postimage against a protected C11-C manifest entry. Do not restore it or change the manifest blindly. D baseline remains blocked until a formal isolation/policy decision.

## Always-on controls

C11-C 2.19.12 immutable; no C mechanics, generator, binder, RNG, simulation truth or protected frame-stream changes. One E service for GUI and CLI. Five GUI surfaces only. `request.seed` and `request.music_seed` remain independent. Renderer/dispatch/media stay OFF. `release_authority=NONE`.
