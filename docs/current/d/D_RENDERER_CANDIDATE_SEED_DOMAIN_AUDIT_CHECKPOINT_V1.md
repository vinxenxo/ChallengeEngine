# Candidate cross-type seed-domain audit — Checkpoint V1

**Date:** 2026-10-15  
**State:** `OPERATOR_REPORTED_RUNTIME_PASS_EVIDENCE_CAPTURE_DEFECT_REQUIRES_RECAPTURE`  
**Scope:** One canonical Challenge selector plus one explicitly pinned Visual Loop grammar only.  
**Authority:** Read-only source-pinned experiment; not renderer input, baseline approval, freeze, production or render authorization.

## Why this is the next bounded gate

The operator reports the separate Visual Drill V2 seed-domain experiment PASS on the active Windows checkout: 20 canonical type/tier pairs, gameplay-seed sensitivity 20/20, music-seed orthogonality 20/20, source pins 70/70 and 120 Godot invocations. The exact log SHA-256 for that seed-specific run was not restated with the confirmation and is not invented or replaced by the distinct V2 payload-binding log digest.

The next uncovered cross-type check reuses the existing canonical V1 request-to-payload binder. It creates no parallel binder and tests only these two current supported selector representatives:

- Challenge: `parking_v2 / CHALLENGE_004`.
- Visual Loop: `c11c_geometric_waves_v1 / harmonic_membrane`.

It deliberately does not claim all Challenge variants, all Visual Loop grammars, arbitrary requests, automatic/default seeds, or collision/cross-domain behavior.

## Experiment matrix

For each of the two selectors, all non-seed request fields and selector identity remain constant across:

| Variant | `gameplay_seed` | `music_seed` |
|---|---:|---:|
| `BASELINE` | 12345 | 840001 |
| `GAMEPLAY_SEED_ONLY_CHANGED` | 54321 | 840001 |
| `MUSIC_SEED_ONLY_CHANGED` | 12345 | 840002 |

Every variant must be executed in two independent Godot 4.7.1 headless processes. Total expected runtime invocations: **2 selectors × 3 variants × 2 independent runs = 12**.

For each selector, the gameplay-only mutation must change the request-binding SHA-256, payload SHA-256 and visual-state SHA-256. The music-only mutation must change request-binding identity while preserving payload hash, visual-state hash and grammar-parameter evidence. Each independent repeat must preserve the source request hash, request-binding identity and all payload/visual evidence. Any mismatch or missing receipt fails the entire audit closed.

## Source contract and preparation verification

- Contract: `definitions/c11d/production/D_RENDERER_CANDIDATE_SEED_DOMAIN_AUDIT_V1.json`.
- Strict report schema (Draft 2020-12): `definitions/c11d/production/D_RENDERER_CANDIDATE_SEED_DOMAIN_AUDIT_SCHEMA_V1.json`.
- Runner: `tools/c11d/d9/d_renderer_candidate_seed_domain_audit.py`.
- Focused regression: `tools/c11d/d9/test_d_renderer_candidate_seed_domain_audit.py`.
- Cross-type source pins: **18/18** in the contract; immutable C11-C manifest is explicitly pinned.
- Deterministic unit/regression test: **12/12 PASS** in the reconstructed preparation tree using a mocked process runner. This is not a live Godot execution and cannot close this checkpoint's runtime gate.
- Candidate I/O audit integrates the new contract/schema/runner/test at **49 source pins** and retains **0 complete / 6 partial / 4 blocked** required groups.
- Candidate identity inventory integrates **160 declared source artifacts**; it remains identity-only and does not mean a renderer baseline is approved.

## Operator-reported Windows Godot 4.7.1 gate and evidence-capture issue

The operator reports the runtime matrix PASS, but the transcript attached to the prior wrapper did not preserve a valid log. For any evidence-grade rerun, first resolve the actual console executable via `Get-Command`/known paths; capture stdout and stderr directly to files; capture `$LASTEXITCODE` immediately; verify the summary and log; only then compute and record SHA-256. Do not reuse the Visual Drill seed log digest or prior V2 binder log digest.

> Historical wrapper example retained below for audit context only; do not use it for a new evidence-grade run because its shell capture did not reliably preserve stdout/stderr.

```powershell
python -B .\tools\c11d\d9\test_d_renderer_candidate_seed_domain_audit.py
python -B .\tools\c11d\d9\d_renderer_candidate_seed_domain_audit.py --godot $env:C11D_GODOT_EXECUTABLE --timeout 120 --full-report
```

Acceptance summary must report all of the following:

`selectors=2 | gameplay_seed_sensitivity=2/2 | music_seed_orthogonality=2/2 | independent_repeats=6/6 | source_pins=18/18 | runtime_invocations=12 | seed_domains_complete_for_candidate_input=false`.

Preserve full console stdout/stderr and record the SHA-256 of the exact cross-type audit log in the next checkpoint update. Do not reuse either the Visual Drill seed-audit log digest or the earlier V2 binder digest for this run.

## Next steps after runtime acceptance

After this bounded cross-type matrix passes on Windows, the next engineering scope is to broaden selectors only after confirming canonical binder support and adding explicit source pins and fail-closed tests. Recommended order: add a small source-approved Challenge variant matrix; then expand Visual Loop grammar coverage by one canonical grammar at a time; then design explicit tests for automatic/default seeds, collision handling and prohibited cross-domain reuse. Do not claim catalog-wide completeness based on these representatives.

In parallel, policy decisions remain prerequisites to the first render: approve editorial field windows/visibility, presentation regions/coordinates, delivery timebase/timeline and audio/music rules; only then implement and verify an authorized payload-side editorial consumer, re-audit the prospective input, and proceed through independent renderer baseline approval/freeze, D4.8 and required D9.14/D9.16/D9.17 gates.

## Governance and immutable controls

`renderer=OFF`; `media_created=false`; `D4.8=BLOCKED`; `release_authority=NONE`; `baseline_approval=MISSING`; `freeze_eligible=false`; D9.10=`PREPARE_ONLY`; D9.14/D9.16 blocked; D9.17=`BLOCKED_NO_GO`; D10 blocked. The I/O audit has `0/10` complete groups, `6/10` partial and `4/10` blocked. The cross-type experiment creates no input instance, payload file, report file, receipt file, renderer dispatch or media. C11-C 2.19.12 and the frozen manifest remain immutable at SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
