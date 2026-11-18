# C11-E E6 D9 dependency-pin reconciliation — V1

**Date:** 2026-11-18  
**Disposition:** `STATIC_RECONCILIATION_PASS_ON_SUPPLIED_BASELINE_SNAPSHOT; ACTIVE_CHECKOUT_REVALIDATION_REQUIRED; EXECUTION_HELD`

## 1. Purpose

Reconcile the 17 November static Challenge capture-route audit with the later accepted 33-pin runtime-dependency receipt and the 18 November D9 multi-selector PREPARE_ONLY plan. This is an evidence reconciliation only. It does not edit source, rerun accepted media, invoke Godot/FFmpeg/FFprobe, generate audio, mux, reserve BatchId, dispatch production or grant renderer/release authority.

## 2. Evidence chain

- Frozen C11-C manifest: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- D4.8 R1V V2 policy: `0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07`.
- Runtime dependency pin acceptance receipt: `E6DEPPINACCEPT_20261117T141326Z_C980FF81`, 33/33 pins, status `PASS_E6_STATIC_ROUTE_DEPENDENCY_PIN_BASELINE_ACCEPTED`.
- Static capture-route audit: `E6ROUTEAUDIT_20261117T125614Z_54A34DBA`, 18/18 static route checks and 24/24 original contract pins.
- D9 plan: `E6CAPPLAN_20261118T082416Z_68342FCD`, six Challenge groups, 18 E1 intents, 18 D envelopes, status `PASS_D9_MULTISELECTOR_CAPTURE_GROUP_PLAN_READY_EXECUTION_HELD`.
- E6 hydration V2: `E6HYDRATE_20261118T073344Z_1A9D7C52`, 1,801/1,803 checks; exactly two historical CH004 nested source-pin divergences and zero other failures.

## 3. Nine route dependencies reconciled

The route audit originally recorded nine dependencies as observed but not accepted. The later 33-pin acceptance receipt contains all nine paths with exactly matching SHA-256 values. The reconciliation runner checks both the accepted receipt and every live file in the active checkout. A 9/9 subset match in a receipt alone is not enough: all 33 current file hashes must also pass.

The supplied 18 November baseline snapshot replay returned:

- fixed evidence pins and sidecars: 13/13 PASS;
- accepted source pins: 33/33 PASS;
- additional route dependencies: 9/9 PASS;
- reconciliation blockers: 0.

This is snapshot replay evidence, not a claim about the user's active checkout. Run the same audit against the active checkout before treating the reconciliation as accepted there.

## 4. CH004 historical source-pin divergences remain separate

The two failures in hydration V2 are not the CH008/009 duration discrepancy:

1. `tools/c11d/d9/universal_editorial_model.py`: historical E4A.7 nested pin differs from the current file; it is not included in the later 33-pin receipt.
2. `c11c-suite/c11c-producer/c11e_production_service.py`: historical E4A.7 nested pin differs from the current file. The current hash is included in the later accepted 33-pin receipt, but that does not retroactively prove that the old E4A.7 output was produced by the current source.

Neither divergence is auto-waived. CH004 E6 reuse remains `REUSE_CANDIDATE_NOT_ACCEPTED` until an explicit evidence-provenance adjudication accepts the old source lineage, or a fresh capture is separately authorized. Do not restore old files or rewrite historical receipts.

## 5. Historical Challenge timing context

The operator's explanation is recorded as historical design context: early Challenge definitions were authored before the HOOK/countdown, GAME, REVEAL and CTA block structure and optimal social-delivery durations had been fully settled. This is a plausible explanation for early declared-total/phase-sum mismatches, but it is not itself a canonical timing decision.

CHALLENGE_008 and CHALLENGE_009 each currently declare `total_duration=11.0` seconds while their four phase fields sum to 12.0 seconds (3 + 7 + 0 + 2). Preserve both values and the historical definitions. Do not silently choose the declaration or the phase sum, alter frames, or admit these selectors into a frozen E6/E7 matrix. A future explicit editorial/timebase decision must establish the single authoritative duration and update any affected downstream contracts through a separately reviewed change.

The CH004 source-pin divergence is a provenance issue and must not be conflated with this duration history.

## 6. Remaining blockers and next gate

The nine route dependencies are no longer a blocker when the active 33-pin audit passes. Remaining blockers are unchanged:

- E4A.6 envelope builder and E4A.7 A/V worker are CHALLENGE_004-only.
- E3 D3 V5 audio pipeline is CHALLENGE_001-pilot-only.
- E1 `tempo_bpm` and `duration_seconds` remain unresolved; fixture seeds/tempo remain proposals, not defaults or authorization.
- CH004 nested historical source-pin divergence needs explicit adjudication or fresh capture.
- D4.8 R1V V2 forbids Smoke18, D3/audio/PCM and FFmpeg mux; a separate E6 TEST_ONLY authorization and explicit governance resolution are absent.

The next permissible work is read-only source/provenance reconciliation and PREPARE_ONLY executor design. Do not invoke render or media tools until the governance conflict is explicitly resolved and a separate authorization lists exact tools, hashes, arguments, counts, output roots and stop conditions.

## 7. Permanent invariants

C11-C 2.19.12 remains the sole production baseline. Frozen manifest and D4.8 hashes above remain immutable. E1 stays PREPARE_ONLY; renderer OFF; production dispatch/media false; `release_authority=NONE`. No protected C11-C changes, no parallel Producer/binder/renderer, no Git checks, commits operator-managed, source SHA-256 pins enforced.
