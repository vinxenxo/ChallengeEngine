# FIRST PROMPT — C11-E E6 D4.8 Reconciliation V2 — 2026-11-18

Continue from the active checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`.

## Read first

1. `docs/current/e/C11E_MASTER_HANDOVER_20261118_V11.md`
2. `docs/current/e/C11E_E6_D4_8_GOVERNANCE_RECONCILIATION_20261118_V2.md`
3. `docs/current/e/C11E_E6_D4_8_HISTORICAL_CONFLICT_MATRIX_20261118_V1.md`

## Confirmed operator decision

Smoke18 scope is fixed: 18 top-level rows (6 Challenge + 6 Loop + 6 Drill), with 18 nested A/B/C subruns inside the six Challenge rows. Do not ask the scope question again.

## Current accepted E6 checkpoints

- Reuse requalification: `E6SMK18REQUAL_20261118T141200Z_BA5AC046`, 21/21; 13 candidates (CH004 + six Loop + six Drill); five fresh Challenge A/V obligations; E6 accepted zero. Receipt SHA `4d63b8caec7a975cc0362ee9d7a5924f5ab8371e8e8e1457e1d60956bf65ce33`.
- Challenge PREPARE_ONLY: `E6CHPREP_20261118T202841Z_37C6AE0E`; 6 groups, 18 A/B/C subruns, 18 E1 intents, 18 static D envelopes; 28/28 pins unchanged; receipt SHA `b54a884f1574d22fa65ea198d279d9ba84bb3967adc87885213f7659a1b1c944`; plan SHA `c645e4d34c79b1c18875d58078893ccd13838312b995bc925e0fb3b57133be8b`.

## Task

Resolve the historical D4.8 conflicts by preparing a reviewable successor-policy decision and the exact TEST_ONLY authority proposal. Do not invoke media tools.

1. Re-verify every required source hash against the active checkout. ZIPs and nightly snapshots are reference only. No extraction over checkout. No Git commands or checks.
2. Read the immutable D4.8 R1V V2 policy and all linked approval records/amendments. Do not edit or replace D4.8 V2 or the original D4.8 production activation policy.
3. Reconcile the 18-row Smoke18 ledger. Preserve the 13 reuse candidates only when all E6 evidence predicates pass; no reruns of accepted media absent a source/evidence failure. Track the five fresh Challenge selector-level A/V obligations and 18 nested Challenge A/B/C subruns separately.
4. Preserve family-specific paths: Challenge D3 V5; Loop C11C Family Music V4; each Drill family-native music profile and timeline. Do not promote the unified audio delivery proposal V1; it is still proposal-only and leaves music/mixing/loudness unresolved. Do not infer tempo, seed, duration, pixel format or audio sample rate.
5. Address the E1 adapter boundary explicitly. E1 remains PREPARE_ONLY and `family_adapter=NOT_CONNECTED_E1` unless an exact bounded test-only consumer bridge is separately designed and approved. Do not change global E1 or invoke D9.10 production dispatch.
6. Produce a clause-level successor-policy draft for one bounded Smoke18 TEST_ONLY run only. Keep production renderer OFF outside that isolated test, production dispatch/media false, release NONE and D10 blocked. No C11-C changes.
7. Produce an execution allowlist proposal specifying exact tool path/version/SHA-256/argv, environment, working/input/output roots, process count/concurrency, timeout, output count/byte ceiling, stop-on-first-failure, quarantine, hash/FFprobe checks, A/V drift and human review. No wildcard executable.
8. Ask the operator to explicitly approve or reject the successor-policy boundary and unresolved Challenge music fixture inputs before building an execution overlay.

## Prohibited now

No Godot, FFmpeg, FFprobe, D3/audio/PCM generation, mux, frame capture, media creation, renderer activation, dispatch, BatchId reservation/consumption, production writes, release/promotion, Git checks, C11-C mutation, D4.8 V2 mutation, or rerun of accepted E4A/E4B/E4C/E5 media.

## Permanent invariants

`GIT_CHECKS=SKIPPED; COMMITS=OPERATOR_MANAGED; SOURCE_FILE_PINS=ENFORCED`.
`D4.8=BLOCKED; E1=PREPARE_ONLY; FAMILY_ADAPTER=NOT_CONNECTED_E1; D9.10=PREPARE_ONLY; D9.14=BLOCKED; D9.16=BLOCKED; D9.17=BLOCKED_NO_GO; D10=BLOCKED_FOR_PROMOTION; E6_ACCEPTED=0; MATRIX_FROZEN=FALSE; RENDERER=OFF; PRODUCTION_DISPATCH=FALSE; PRODUCTION_MEDIA=FALSE; RELEASE_AUTHORITY=NONE`.
