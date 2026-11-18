# C11-E E6 Smoke18 — Successor Scope and Composition Readiness V1

**Date:** 2026-11-18  
**Status:** `OPERATOR_SCOPE_APPROVED / READINESS_AUDIT_PENDING / MEDIA_NOT_AUTHORIZED`  
**Active phase:** E6 Smoke18.  
**Decision:** the operator approved preparation of a bounded D4.8 successor for Smoke18 and approved the Challenge music fixture for TEST_ONLY use. This is not an E6 media authorization or production activation.

## 1. Fixed Smoke18 scope

Smoke18 is exactly 18 top-level selector scenarios:

| Family | Rows | Scope |
|---|---:|---|
| Challenge | 6 | `CHALLENGE_001`, `002`, `004`, `005`, `006`, `007` are the current proposed six. Each has A/B/C probes nested below that scenario. |
| Visual Loop | 6 | Six selectors: `radial_bloom`, `harmonic_membrane`, `dipole_field`, `swarm`, `astrolabe`, `interference_plane`. |
| Visual Drill | 6 | Six selector/tier rows from the six E4C evidence candidates. |
| **Total** | **18** | Challenge's 18 A/B/C probes are subruns, not additional top-level scenarios. |

CHALLENGE_003 remains excluded from the present sample because its current draft repeats CH004 gameplay seed 314159. CHALLENGE_008/009 remain held because declared 11-second duration conflicts with a 12-second phase sum (3+7+0+2). Do not rewrite canonical definitions to resolve the conflict.

## 2. Operator decisions now recorded

1. Smoke18 has 18 top-level rows: six per family, with Challenge's 18 A/B/C nested probes.
2. Prepare a separate D4.8 successor policy for bounded Smoke18; preserve original D4.8 R1V V2 unchanged.
3. Challenge music fixture: `challenge_8bit_v1` v1.0, A/B music seed 840001, C music seed 840002, historical tempo 104 BPM. This is run-scoped TEST_ONLY fixture data, not a product contract or default.
4. Challenge duration is selector-specific and derived from its canonical timebase; media duration must be checked against the actual output using FFprobe. E1 `tempo_bpm` and `duration_seconds` remain null unless separately contracted.
5. Loop and Drill keep their own family-native C11-C music profiles/routes. Challenge D3 V5 does not replace them.

The current Challenge PREPARE_ONLY receipt predates the music-fixture approval and remains immutable. A new plan-only manifest revision must record the approval before any test run.

## 3. Evidence reconciliation — do not rerun accepted work

The 2026-11-18 reuse requalification is `PASS_REUSE_EVIDENCE_LINKAGE_REQUALIFIED_NOT_E6_ACCEPTANCE`, 21/21 checks, 13 linked candidates (CH004 + six Loop + six Drill), zero E6-accepted rows. Five new Challenge A/V rows remain required. Existing R1V, Loop22 and Drill outputs must not be regenerated absent a source regression or a failed exact E6 reuse predicate.

| Family | Reuse candidates | What the evidence does prove | What it does not prove |
|---|---:|---|---|
| Challenge | CH004 (1) | CH004 D-composited A/V anchor with operator review | Five other Challenge selectors' A/V route |
| Loop | 6 | C11-C source A/B and family-music evidence linked by hashes | Six D-owned post-composition outputs; E4B remains shared-service preparation only |
| Drill | 6 | E4C family-specific D composition A/V receipts are candidates | E6 row acceptance before exact predicates are evaluated |

The PREPARE_ONLY Challenge run has 6 groups, 18 E1 intents and 18 static D envelopes. Its 36 nested files are pinned. It does not render. Its editorial text fields are `UNKNOWN` and personalization is false, so it cannot alone prove visible editorial consumption.

## 4. Critical newly reconciled blocker — Loop D compositor

The Option C boundary is `PREPARE_ONLY_NOT_DISPATCHABLE`. It requires immutable C11-C silent video, exact R1V frame inventory and decoded pixel identities, canonical D9.9 plan, D9.10 bridge and R1P parameter receipt. It emits a separate D-owned video only after gates approve. It forbids source overwrite, resampling, frame drop/duplication/interpolation/padding, or using gameplay/music seeds in the wrong domains.

The V6 remediation document says Option C evidence is static PREPARE_ONLY (27/27) and the actual D compositor is not implemented. E4B V3 states no request-scoped payload has been rendered and no D-only pixel consumer is accepted. The single-selector Visual Loop dynamic binder's in-memory composite is not a `ShaderMaterial`, renderer-native input or pixel/video output; visual editorial consumption remained 0/14 in that checkpoint.

**Disposition:** the six Loop A/V candidates remain useful C11-C source/audio reuse evidence, but not D composition reuse. A D-owned Loop consumer/compositor must be implemented at the already approved Option C seam and pixel-tested before any Smoke18 row can claim D composition.

## 5. Challenge editorial fixture gap

The 18 Challenge intents currently declare title/subtitle/CTA as `UNKNOWN`, with `personalization_enabled=false`. Do not mutate the receipt or canonical defaults. Use a new, run-scoped test-only manifest revision after operator approval of the proposed Spanish strings in the scope JSON. `player_name` and `challenge_label` stay blocked/unknown. Language is metadata, not a visual text field.

## 6. Global renderer readiness remains a separate concern

The last located pinned global D-renderer I/O checkpoint reports 0/10 groups complete, six partial (`content_identity`, `source_lineage`, `payload_instance`, `seed_domains`, `editorial`, `delivery`) and four blocked (`presentation`, `timeline`, `audio`, `authorization`). It also reports candidate input inadmissible, visual editorial consumption 0/14, renderer OFF and release NONE. This older global audit is not silently promoted by an E6 scenario-specific test proposal.

## 7. Shortest safe path to audiovisual proof

1. Run the single read-only Composition Readiness Audit V1 against the active checkout. It checks live pins, the exact Challenge PREPARE_ONLY receipt and all 36 nested evidence files. No prior media is rerun.
2. Close the Loop D compositor gap using the approved Option C boundary. Add only a D-owned post-composition consumer; preserve C11-C source video and all C11-C binders/music. First qualify an isolated selector and its pixel/timebase/source-identity invariants; then expand to the six E6 Loop selectors.
3. Refresh Challenge's E6 plan-only manifest with the operator-approved music fixture and approved non-empty synthetic editorial fixture. Keep E1 tempo/duration null; run-scoped values only.
4. Evaluate the six Drill and CH004 reuse candidates against the frozen E6 acceptance predicates. Do not rerun accepted outputs.
5. Freeze the exact 18-row Smoke18 manifest and nested evidence predicates. Identify output cardinality and per-family technical profiles.
6. Reconcile the exact D4.8 clauses and issue a versioned, separate successor policy. Pin Godot/FFmpeg/FFprobe executables, versions, hashes, argv, counts, output roots, timeouts, one-shot identity and stop-on-first-failure.
7. Obtain a separate explicit E6 TEST_ONLY execution authorization before any renderer/audio/mux invocation.
8. Close E6 with technical receipts and operator visual/audio review. Then proceed E7 Matrix101 → E8 historical C-to-E regression reconciliation, independent acceptance, immutable D baseline proposal and separately authorized production cutover.

## 8. Non-negotiable governance

C11-C 2.19.12 remains sole production baseline. Do not modify frozen C11-C or original D4.8 R1V V2. E1 remains PREPARE_ONLY, family adapter NOT_CONNECTED_E1, renderer OFF, dispatch/media false and `release_authority=NONE`. No production renderer activation, media dispatch, BatchId, release or promotion is authorized by this document.

`GIT_CHECKS=SKIPPED; COMMITS=OPERATOR_MANAGED; SOURCE_FILE_PINS=ENFORCED`.
