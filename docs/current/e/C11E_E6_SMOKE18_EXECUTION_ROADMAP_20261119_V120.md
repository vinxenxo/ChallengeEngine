# C11-E E6 Smoke18 Execution Roadmap — V120

**Date:** 2026-11-19  
**Disposition:** `CONTINUATION_AUTHORIZED_TEST_ONLY_PREPARATION_AND_GATED_EXECUTION`  
**Target:** Smoke18 visual composition with editorial, music and layout, followed by A/V qualification and operator review.  
**Source authority:** active checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS` only.

## 1. Operator direction recorded

On 2026-11-19 the operator explicitly authorized continuing the C11-E work through the Smoke18 visual render with editorial, music and layout. This authorizes preparation and implementation of the bounded E6 TEST_ONLY path and its successor governance package. It does **not** authorize production promotion, C11-C changes, or an unbounded renderer/dispatch/media transition.

The execution route must preserve the original D4.8 V2 policy byte-for-byte and create a separately versioned, narrowly scoped Smoke18 successor. The successor and its execution manifest must enumerate executable paths, versions, SHA-256 values, argv allowlists, invocation counts, output roots and fail-closed stop rules before any media process starts.

## 2. Latest evidence checkpoint

### 2.1 Smoke18 evidence reuse linkage

`PASS_REUSE_EVIDENCE_LINKAGE_REQUALIFIED_NOT_E6_ACCEPTANCE` — 21/21 checks, zero failed references.

- Receipt: `artifacts/tests/c11e/e6_smoke18_reuse_requalification/E6SMK18REQUAL_20261119T141719Z_A5555D34/E6_SMOKE18_REUSE_REQUALIFICATION_RECEIPT_V1.json`
- SHA-256: `2071d276429fa102c080018ee1421f5397cc3c5be74a7b0451e2ccad2ced494d`
- 18 top-level rows: six Challenge, six Loop, six Drill.
- 13 reuse candidates; five fresh Challenge A/V groups required; E6 accepted remains zero.
- Challenge A/B/C are 18 nested probes under the six Challenge rows, not additional top-level rows.

### 2.2 Loop policy reconciliation V2

- Package ZIP SHA-256: `dd8b549741be86829f694532dc68d450ce83026191897bbbc76b759231ee297f`.
- PowerShell 5.1 AST: PASS; package members 9/9; payload pins 7/7; Python 3.13.14; focused tests 32/32; all five exact operator policy decisions printed as pinned/approved; Loop D source modules 3/3 compiled in memory.
- Receipt: `artifacts/tests/c11e/e6_loop_policy_pin_reconciliation_v2/E6LOOPPOLICYV2_20261119T184655Z_9466C358/E6_LOOP_POLICY_PIN_RECONCILIATION_RECEIPT_V2.json`
- Receipt SHA-256: `5afc42ca84480ba1d025d288f2653d009e85af053fff5b62133e067a17dfb4be`.
- **Important unresolved reporting inconsistency:** console output says `LOOP_POLICY_AUDIT_STATUS=PASS...`, `17/18 PASS; FAIL=0`, while the same output says `A3_LINEAGE=BLOCKED`. These statements do not establish a complete A.3 PASS. The exact JSON check row and current A.3 pointer/model pins must be inspected using the post-run receipt diagnostic; do not rerun the V2 runner or proceed to compositor implementation on the basis of the overall PASS line alone.

The V1 false comparator issue is closed as a runner defect. V2's 32 focused tests prove the corrected nested-transition schema in its fixtures; they do not waive a failed/missing active-checkout A.3 check.

### 2.3 Challenge runtime readback attempt

The bounded Challenge runtime Apply V1 failed in preflight before transaction start; no project payload mutation occurred. Its separate diagnostic showed equal expected/actual printed values in a binding-manifest comparator. Preserve that failed receipt and stage; do not rerun the same Apply or attempt to repair by changing historical evidence.

## 3. Fixed Smoke18 scenario matrix

Exactly 18 top-level rows:

| Family | Rows | Identity set | Evidence posture |
|---|---:|---|---|
| Challenge | 6 | `CHALLENGE_001`, `002`, `004`, `005`, `006`, `007` | CH004 is a reuse candidate; five groups require fresh A/V. Three nested A/B/C probes per group. |
| Visual Loop | 6 | `fractal_bloom/radial_bloom`; `geometric_waves/harmonic_membrane`; `invisible_forces/dipole_field`; `living_particles/swarm`; `sacred_symmetry/astrolabe`; `geometric_waves/interference_plane` | Six accepted predecessor A/B evidence candidates; all six require D-owned Option C post-composition evidence for E6. |
| Visual Drill | 6 | `tracking/tier-2`; `pursuit/tier-1`; `saccade/tier-1`; `peripheral_scan/tier-1`; `tracking/tier-5`; `peripheral_scan/tier-5` | Six exact E4C receipts and their nested output evidence are reuse candidates; no E4C media reruns. |

Challenge selectors 008/009 remain excluded due the 11-second declaration versus 12-second phase-sum conflict. Selector 003 remains excluded from the six-row proposal because of gameplay-seed duplication with CH004.

## 4. Execution sequence and gates

### Gate G0 — reconcile current receipts and source authority

1. Inspect the exact Loop Policy V2 receipt JSON: compare `status`, `check_count`, each check status, `passed_checks`, `failed_checks`, `failures`, and the A.3 row. A contradictory or non-PASS A.3 row is a hard stop.
2. Read-only rehash the active A.3 bridge, historical and current review manifests, D9.8 model, A.3 proposal and E4B decision record. Require the exact pointer transition `/source_lineage/6/sha256` and no other manifest changes.
3. Keep C11-C frozen manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` unchanged.

### Gate G1 — D-owned Loop Option C post-compositor

After G0 is genuinely PASS:

1. Implement only at the existing D boundary, downstream of the accepted D9.9/D9.10 plan/bridge and D-only adapter envelope.
2. Keep the C11-C visual output/frame content immutable. The D compositor places the original frame inside the approved outer presentation bands; no crop, non-uniform stretch, re-timing, re-binding or C11-C modification.
3. Use the existing E1 shared GUI/CLI service and existing request-scoped family binding. No parallel Producer, sixth module, duplicate binder or geometric-only hard-coding.
4. Add focused positive/negative static tests for all six Smoke18 Loop family/grammar identities, A/B gameplay repeatability, independent music seed provenance, field-presence/blank semantics, exact region geometry, clipping, opacity and one-owner semantics.
5. Static tests and contract receipts do not enable renderer input or dispatch.

### Gate G2 — Challenge E6 editorial successor

1. Preserve E4A policy/consumer/adapter V1 unchanged as the predecessor.
2. Reconcile the E6-only successor window proposal: primary HOOK/CTA window when it has frames; GAME fallback only when that primary window is zero frames.
3. Enforce native hook migration only when the native render model actually exposes `show_hook=true`; GAME fallback must not migrate or suppress a nonexistent native hook.
4. Preserve native Challenge phase order/timebase and selector-canonical gameplay seed. Keep music seed as a separate input. `tempo_bpm` and `duration_seconds` remain null in E1.
5. The E6 Spanish fixture and the 18 PREPARE_ONLY envelopes remain separate from canonical defaults. Keep player identity and `challenge_label` UNKNOWN/BLOCKED and personalization false.
6. Require successor policy SHA pin, D-owned source pins and the complete static suite before runtime authorization.

### Gate G3 — freeze Smoke18 acceptance matrix

Freeze only after all evidence identities and per-row predicates are exact. Each row must carry family, selector, canonical definition hash, gameplay seed, music profile/seed, source and output paths, source/receipt/media SHA-256, timebase, FFprobe facts where applicable, editorial/layout contract ID, visual/A/V acceptance criteria, predecessor/reuse rationale and operator review state.

Reuse is conditional. A candidate becomes E6-accepted only when its exact receipt, nested media hashes, profile, timebase, visual/editorial/layout review, audio QA and relevant source pins meet the frozen row predicate. Missing evidence stays `REUSE_CANDIDATE_NOT_ACCEPTED`; never regenerate an already accepted E4 output merely to repair a ledger.

### Gate G4 — scoped Smoke18 TEST_ONLY successor and execution manifest

Preserve D4.8 V2 unchanged and globally blocked. Prepare a new versioned successor scoped only to the approved Smoke18 tests. It must explicitly enumerate:

- exact Godot/headless/editor-import/renderer executables and versions;
- exact FFmpeg/FFprobe binaries and hashes where required;
- D3/D3.3 and family-native audio paths, profiles and hashes;
- exact command arguments and maximum process counts;
- exact 18-row manifest digest and any nested Challenge A/B/C probe identities;
- exact output roots, sidecar scheme and one-shot batch identity rules;
- stop-on-first-failure, no retries, no overwrite, no production dispatch and no release;
- no use of tools/processes not listed in the successor.

The operator's 2026-11-19 instruction authorizes preparation of this successor and its bounded TEST_ONLY path. The actual process allowlist cannot be finalized until the active tool paths/versions/hashes are checked against the machine and the output matrix is frozen.

### Gate G5 — visual render and A/V work

1. First render the bounded visual-only outputs after G0–G4 are satisfied, with D editorial/layout composed at the approved boundary and C11-C source frame identity preserved.
2. Apply family-native Loop/Drill music rules; Challenge uses only its approved test fixture and separate music-seed variant. Never route Loop through Challenge D3 V5.
3. For every final A/V output, prove exact video/audio stream profile, video stream-copy identity where required, A/B audio repeatability, C changed-music-seed difference, non-silence, AAC-LC 48 kHz stereo, duration and A/V drift threshold.
4. Conduct operator visual/editorial/layout review and audio listening against exact media hashes.
5. Close each row independently; do not infer all 18 accepted from a successful batch process.

## 5. Protected invariants

- C11-C 2.19.12 and its frozen manifest remain immutable.
- D4.8 V2 SHA-256 `0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07` remains unchanged. A scoped successor is separate and may not silently alter global policy.
- `E1=PREPARE_ONLY` until its exact TEST_ONLY boundary is formally versioned and pinned.
- `D9.10=PREPARE_ONLY`; `D9.14/D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`.
- No production dispatch, renderer activation, BatchId consumption, release authority or promotion.
- No C11-C canonical definitions, binders, timelines, mechanics, winning frame, metrics, music generators or frozen manifest changes.
- `GIT_CHECKS=SKIPPED; COMMITS=OPERATOR_MANAGED; SOURCE_FILE_PINS=ENFORCED`.
- Runners must not inspect Git HEAD/status/branch. Evidence ZIPs are read-only references and must never be extracted over the active checkout.

## 6. Exit criterion

The E6 target is the 18-row Smoke18 acceptance matrix plus required visual and A/V evidence. This roadmap is a sequence of TEST_ONLY preparation, implementation, qualification and review gates; it does not declare Smoke18 rendered or accepted. E7 Matrix101 and E8 independent acceptance/freeze/production transition remain downstream phases.
