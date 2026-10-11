# C11-D — Unified delivery timebase policy proposal checkpoint

Date: 2026-10-11
State: `PROPOSED_NOT_APPROVED` — integrated into the unified content review for consistency checking only.

## Purpose

Define one shared *delivery-timebase policy* for Visual Loops, Visual Drills and Challenges. This is not yet the unified production pipeline: presentation composition, audio/music, text layout, renderer execution, and production/release authority remain distinct gates.

## Proposal matrix

| Content type | Source timeline | Proposed delivery timeline | Rule |
|---|---:|---:|---|
| Visual Loop | 600 frames @ 30 FPS (20 s) | 600 frames @ 30 FPS | Identity timebase; preserve frame count and order; no resampling |
| Visual Drill | 630 frames @ 30 FPS (21 s) | 630 frames @ 30 FPS | Identity timebase; preserve frame count and order; no resampling |
| Challenge (`CHALLENGE_004`) | 900 frames @ 60 FPS (15 s) | 450 frames @ 30 FPS | Project cumulative half-open phase boundaries; reference the separately proposed 2:1 GAME snapshot selection; no interpolation |

Target profile metadata is explicitly `REVIEW_720` (720x1280, 30 FPS). It is resolved once for this review case. The profile metadata is not proof that an encoder has executed.

Challenge source phase boundaries `[0,180,600,780,900]` map to delivery boundaries `[0,90,300,390,450]`. GAME source snapshots `420 -> 210` are still proposal references only; no delivery candidate is materialized. `winning_frame` is read-only and is not used as a selection input; `close_calls` remains count-only.

## Audio/music boundary

At this milestone, audio/music resampling, soundtrack selection, mixing and loudness were explicitly `OUT_OF_SCOPE_NOT_DEFINED_NOT_EMITTED`. The separate checkpoint `D9_UNIFIED_AUDIO_MUSIC_DELIVERY_POLICY_CHECKPOINT.md` now adds a review-only technical audio-delivery envelope and pre-encode timeline arithmetic, sourced from the same pinned `REVIEW_720` profile. It still does not define soundtrack selection, mixing, loudness, or a materialization/encoding procedure.

## Follow-on milestone — 2026-10-11

A separate audio/music delivery proposal is now integrated into the unified review as `unified_audio_music_policy`. The combined review has 16 cross-artifact checks and 9 unresolved gates, including `AUDIO_MUSIC_DELIVERY_AND_EDITORIAL_POLICY_NOT_APPROVED`. This does not change the timebase policy state (`PROPOSED_NOT_APPROVED`) or its original exclusions.

## Verification contract

- The proposal has a source-pinned JSON contract and strict schema.
- The unified review cross-checks request-scoped Loop/Drill payload timing against identity-preservation rules and Challenge delivery boundaries against the 60-to-30 FPS proposal.
- Unified review records `unified_delivery_policy_parity=true` but keeps `unified_delivery_timebase_policy_approved=false`.
- Canonical C11-C sources and manifest remain byte-for-byte immutable.
- Renderer activation, renderer-native input, dispatch, production, media creation and persistent reports remain false; `D4.8=BLOCKED`; `release_authority=NONE`.

## Commands

```powershell
python .\tools\c11d\d9\test_d_renderer_unified_delivery_timebase_policy.py
python .\tools\c11d\d9\test_d_renderer_unified_content_review.py
python .\tools\c11d\d9\run_d_renderer_unified_content_review.py --godot godot
```

The policy stays a proposal even when tests pass. No acceptance result grants renderer/baseline approval or authorizes the first video run.
