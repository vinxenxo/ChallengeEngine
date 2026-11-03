# C11-E E4A.2 — real C11-C gameplay BODY pixel review increment V2

**Date:** 2026-11-03. **Status:** prepared; Windows real-gameplay run pending.

## Objective

Prove, on one real `CHALLENGE_004` C11-C output MP4, that test-only D-policy title/subtitle draws remain within the 720×1280 HEADER/HOOK region, CTA remains within FOOTER/CTA, and the actual rasterized gameplay BODY pixels remain invariant between A and B at six delivery-frame samples. The source C11-C renderer is invoked once, without editing it, into a fresh `artifacts/tests` subtree.

## Pinned sources

- Runner: `tools/c11d/d9/c11e_e4a_challenge_real_body_pixel_review.py` — SHA-256 `a852e5f4238f14b30a887f579bad3e4284c420c427dc625667a0ec60190fff1a`.
- Tests: `tools/c11d/d9/test_c11e_e4a_challenge_real_body_pixel_review.py` — SHA-256 `5e967ec3b8fd87cc9effe079356912e8f6b69f8994a368dc8f1c15cfb95dcb0c`.
- Previous E4A.1 intent helper: `939a12f369df9eaa0dbaf5b06b0635a0d4dc906e14fd7d5bdf9c12b3ec2b97a0`.
- E1 service: `f0655d8d93df3b766b157d80a76a5bfc7b514d740815646f54c88ca788f602c0`.
- D9.9 resolver: `9ad2adbf54946f2225ae2ed36b88abfc5717387f2ff03bbed684aa8bd32d87d1`.
- Producer main source: `f0adc54de884d6d812396707cd6ced49038df0f52e4a9bc516a9ca5e6a0ddcd3`.
- Frozen C11-C manifest: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

## Execution contract

The runner creates three E1 intents A/B/C through the existing service and D9.9; uses CHALLENGE_004, `parking_v2`, gameplay seed 314159, music seed 840001, audio disabled and `request_origin=TEST`. It invokes the existing PowerShell C11-C Challenge script exactly once with `-ChallengeId CHALLENGE_004 -Seed 314159 -DeliveryProfile REVIEW_720 -OutputRoot <fresh artifacts/tests root> -NoSound`.

It requires exactly one output MP4 and adjacent `production_manifest.json` with `delivery_profile=REVIEW_720`; FFprobe must report exactly one video stream (no audio), H.264, yuv420p, 720×1280, 30 fps, 450 frames and 15 seconds. It extracts delivery frames 0, 89, 90, 300, 390 and 449. It creates 18 PNGs and performs 12 comparisons, including BODY pixel equality at every sample.

D test-only composition policy: title/subtitle → HEADER/HOOK; call_to_action → FOOTER/CTA. `player_name` / `challenge_label` remain blocked for unresolved geometry; language is metadata-only. Test typography is not production art direction.

## Preparation checks

- `python -m py_compile` on runner and tests: PASS.
- Focused tests: 25/25 PASS.
- Final synthetic FFmpeg simulation from `testsrc2` (720×1280, 30 fps, 450 frames): 18/18 PNGs; 12/12 comparisons; zero BODY pixel changes; zero out-of-region changes; B/C identical. This is an implementation simulation only and is not Windows or Challenge evidence.
- E4A.2 actual Windows run: NOT YET EXECUTED.

## Evidence and acceptance

The Windows evidence directory must include generator stdout/stderr, FFprobe output, MP4 + production manifest, E1 intents, all PNGs, command logs, pixel report, receipt and SHA256SUMS. Upload its complete ZIP; verify all receipt/checksum relationships and inspect images before accepting this gate.

A successful E4A.2 proves BODY invariance for this one source render and these six sampled instants only. It does not prove the production D compositor, continuous frame invariance, all Challenge variants, full audio/mux, GUI parity or E4A closure. E4A remains open until E4A.3 actual D visual consumer integration and E4A.4 test-only A/V + operator review are complete.

## Governance

C11-C 2.19.12 stays immutable and authoritative; no C11-C source edits or baseline-manifest changes. No D9.10 dispatch, production renderer, production media or release authority. D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; release_authority NONE.
