# C11-E Execution Backlog — V53

## Current immediate action: verify E4B family contract on Windows

1. Install `C11E_E4B_LOOP_FAMILY_CONTRACT_V1.zip` using the V1 PS 5.1 add-only installer. It validates the frozen C11-C manifest and 40 source pins before writing any of its payload.
2. Run `tools/c11d/d9/RUN_C11E_E4B_LOOP_FAMILY_CONTRACT_V1.ps1` once. The runner executes seven Python tests, including all 27 concrete selectors through canonical D9.9 → D9.10 → D-only adapter prepare → family-stage contract, then writes a read-only audit report and receipt with SHA-256 sidecars.
3. Upload the runner output/receipt if the run is PASS. Do not repeat the 81-case GUI/CLI plan matrix; it is already accepted.

## E4B implementation after Windows audit

- Current operator decisions are recorded for A.1/A.3/E4B composition/B.1/D.1 against the exact approved proposal fingerprints. Do not mutate proposal files or their old approval booleans.
- The new stage-contract builder is pure preparation and not wired into the existing GUI/CLI path yet. Next integrate it behind the existing D9 Loop boundary; keep all request fields unchanged and do not add `presentation_options` to Loop.
- The family static audit establishes 27 exact selector memberships, 5/5 family style signatures and launcher parameter surfaces. It does not establish 27 request-scoped Godot payloads. Geometric-only historic exact-selector proof remains scoped to its original five selectors.
- Introduce a request-scoped materialized payload receipt for each Loop selector only under a separately authorized isolated test path. Derive frame count/FPS/duration from that payload; never from D9 request or historical product manifests.
- Implement the approved D-only outer composition and actual visual consumer on the existing D boundary, using the 720×1280 bands/504×896 viewport. Test font shaping/fallback, glyph coverage, wrap and clip, suppression, full-span visibility, preservation of original C11-C frame order/count and pixel-level review. The current package does not invoke Godot or emit renderer input.

## Audio/music and timebase

- B.1 is approved as policy: REVIEW_720 30 FPS, preserve Loop frame count/order/duration, no resampling.
- D.1 is approved only as the audio technical delivery envelope. It does not authorize track selection, music synthesis/emission, silence defaults, mixing, ducking, fades, loudness or mux.
- The present C11-C family launchers call `C11CSafeAmbient.py` with the visual `$Seed`. Thus D visual stage must use `-NoSound`. A separate D-owned music-seed adapter must be proven to use `request.music_seed` and must be authorized before audio materialization. No C11-C source modification and no D3 V5 for Loop.

## Reconciliation and acceptance

D9.8 remains `ACTIVE_MODEL_ONLY` / `PENDING_D9_9_UNIVERSAL_REQUEST_ADAPTER`; D9.9 is evidenced for plan-only; D9.10 remains `PREPARE_ONLY`. Do not promote plan evidence to D4 executable compatibility. E1 remains unconsumed/not connected until separate family adapter acceptance.

## Accepted / do not rerun absent regression

- E4A Challenge full closure, including accepted visual/A/V/human review.
- E4B populated GUI/CLI parity V2.
- E4B 81-case Loop family planning matrix: 5 families, 27 grammar selectors, 81 seed-scenario cases/repeats and 81/81 GUI/CLI parity.
- E4B Windows policy-readiness audit: 11/11 tests and `PASS_AUDIT_ONLY_POLICY_APPROVAL_REQUIRED`.

## Later phases

E4B family-bound preparation → existing D-boundary integration → 27-selector payload evidence → visual composition and human review → separately approved music path/A/V review → E4B close → E4C Drill → E5 determinism/seed/profile/binder isolation → E6 Smoke18 → E7 Matrix101 (CH_008/009 held; 99 provisional) → E8 historical C-to-E regression and independent freeze/promotion decisions.

All renderer dispatch/media/production/release gates remain closed. C11-C 2.19.12 remains immutable.
