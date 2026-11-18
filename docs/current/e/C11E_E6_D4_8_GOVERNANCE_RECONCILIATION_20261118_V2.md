# C11-E E6 D4.8 Governance Reconciliation — V2 — 2026-11-18

**Stage:** `E6_D4_8_GOVERNANCE_RECONCILIATION_AND_TEST_ONLY_AUTHORITY`  
**Disposition:** `SCOPE_CONFIRMED; HISTORICAL_CONFLICTS_MAPPED; SUCCESSOR_POLICY_APPROVAL_PENDING`  
**Package kind:** documentation/prompt only. No runtime, media runner or authorization is included.

## 1. Operator scope decision recorded

The operator confirmed the complete Smoke18 target:

- six Challenge top-level rows;
- six Visual Loop top-level rows;
- six Visual Drill top-level rows;
- 18 A/B/C qualification subruns nested within the six Challenge rows.

The confirmed denominator is 18 top-level rows. The nested Challenge probes do not increase it to 36. This scope is now fixed and must not be asked again.

## 2. Stage result before this overlay

The Challenge PREPARE_ONLY orchestration milestone is PASS:

- Run `E6CHPREP_20261118T202841Z_37C6AE0E`.
- `PASS_PREPARE_ONLY_18_E1_INTENTS_18_D_ENVELOPES_EXECUTION_HELD`.
- Six Challenge groups; 18 A/B/C subruns; 18 E1 intents; 18 static D envelopes.
- Source pins 28/28 pre/post unchanged.
- Receipt SHA-256 `b54a884f1574d22fa65ea198d279d9ba84bb3967adc87885213f7659a1b1c944`; plan SHA-256 `c645e4d34c79b1c18875d58078893ccd13838312b995bc925e0fb3b57133be8b`.
- No Godot, FFmpeg, FFprobe, audio, media, mux, renderer, dispatch or BatchId.

Reuse requalification is also PASS as linkage requalification only:

- Run `E6SMK18REQUAL_20261118T141200Z_BA5AC046`; 21/21 checks.
- 13 reuse candidates: CH004 + six Loop + six Drill.
- Five fresh Challenge A/V obligations remain.
- `E6_ACCEPTED=0`; this is not E6 acceptance.
- Receipt SHA-256 `4d63b8caec7a975cc0362ee9d7a5924f5ab8371e8e8e1457e1d60956bf65ce33`.

## 3. Why D4.8 remains blocked

There is no single generic approval that covers the requested full Smoke18 path. The 2026-11-07 R1V approval is limited to ten silent C11-C Loop source captures. Its 2026-11-08 family-audio amendment expands only the bounded Loop A/V scope. Both exclude D compositor/consumer and general renderer dispatch. Challenge E4A approval and D3 V5 A/V evidence are isolated to CH004. Drill A/V receipts and E5 user reviews are bounded to their individual evidence rows/representatives. The unified D audio delivery proposal remains unapproved and does not select music or define mixing/loudness.

The full clause-by-clause matrix, hashes, and timeline discrepancies are recorded in `C11E_E6_D4_8_HISTORICAL_CONFLICT_MATRIX_20261118_V1.md`.

## 4. Recommended implementation path

Use the existing evidence efficiently and preserve accepted family mechanics:

1. Requalify the 13 reuse candidates by exact receipt/report/log/media hashes, pinned inputs, source pins and recorded visual/audio decisions. Do not regenerate them unless a specific predicate fails.
2. Satisfy the five fresh Challenge selector-level A/V obligations using the Challenge-native D3 V5 route, with A/B deterministic repeat and C changed-music behavior only after all seeds/tempo/timebase inputs are approved.
3. Preserve family-native Loop and Drill music, binder, grammar and timeline. Do not flatten their timebases or pixel-format/range contracts into a shared assumed profile.
4. Build one isolated E6 TEST_ONLY consumer run, not a production pipeline activation. E1 remains PREPARE_ONLY; global production renderer/dispatch and release authority remain disabled.
5. After exact successor-policy approval, create a distinct execution overlay. It must be separately installed and separately approved before any media process starts.

## 5. Open authority decisions — no implicit defaults

### Decision A — successor policy and test consumer

Approve or reject a new, separately versioned successor policy permitting only one bounded Smoke18 TEST_ONLY qualification scope. Recommended exact boundary:

- 18 top-level rows with 18 nested Challenge A/B/C probes;
- 13 evidence-backed reuse candidates, subject to requalification, and the five fresh Challenge A/V selector groups;
- D-owned test consumers/compositors only through exact pinned TEST_ONLY entrypoints;
- no E1 family-adapter global connection; E1 remains PREPARE_ONLY;
- no D9.10 production dispatch; global renderer remains OFF outside the isolated test runner;
- production dispatch/media remain false; no production roots, release, promotion or D10 transition;
- no modification to C11-C, D4.8 V2, canonical definitions, protected mechanics or frozen manifest.

This policy would be a bounded test exception, not a production renderer activation. The present operator scope confirmation does not by itself enact this policy.

### Decision B — Challenge music inputs

CH004's previous fixture used gameplay seed 314159, A/B music seed 840001, C music seed 840002, D3 V5 profile `challenge_8bit_v1`, and 104 BPM. The 104 BPM and 15-second/450-frame duration are historical CH004 facts, not product defaults. Challenge selector durations in E6 must come from each selector's canonical timebase. E1 PREPARE_ONLY currently carries unresolved tempo/duration and the music seeds are proposal-only. Before any new Challenge A/V, approve the exact A/B/C seed rule and tempo authority without allowing runtime seed generation or cross-domain seed sharing.

### Decision C — preserve reuse and family-native routes

Recommended: reuse the 13 candidates only after exact E6 evidence predicates pass; do not repeat accepted E4A/E4B/E4C/E5 media. Preserve Loop C11C Family Music V4 and each Drill family-native profile/timeline. The unified audio delivery proposal V1 is proposal-only and must not be promoted implicitly.

## 6. Execution overlay entry criteria

Do not author or run a media runner until Decisions A/B/C are explicit and the active checkout has revalidated every required source pin. A later execution overlay must separately freeze every executable/version/hash, argument vector, working/input/output path, process and concurrency ceiling, timeout, output count/bytes, stop condition, quarantine rule, media predicate, drift bound and human review step. It must have its own ADD_ONLY installer, preflight, receipts and a separate explicit TEST_ONLY authorization.

## 7. Non-negotiable current states

`D4.8=BLOCKED; E1=PREPARE_ONLY; FAMILY_ADAPTER=NOT_CONNECTED_E1; D9.10=PREPARE_ONLY; D9.14=BLOCKED; D9.16=BLOCKED; D9.17=BLOCKED_NO_GO; D10=BLOCKED_FOR_PROMOTION; E6_ACCEPTED=0; MATRIX_FROZEN=FALSE; RENDERER=OFF; PRODUCTION_DISPATCH=FALSE; PRODUCTION_MEDIA=FALSE; RELEASE_AUTHORITY=NONE`.

No Godot, FFmpeg, FFprobe, audio/PCM, D3, mux, D compositor runtime, renderer, dispatch, BatchId or media creation during this documentation gate. No Git commands/checks. Commits remain operator-managed. Source-file pins remain enforced.
