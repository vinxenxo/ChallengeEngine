# C11-E Master Handover — V6 (2026-11-18)

## Sole source authority

Active Windows checkout: `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. Never extract ZIPs over it. The active checkout is authoritative; ZIPs are read-only comparison/evidence. Operator manages commits. Do not invoke Git or inspect HEAD/status/branch. Enforce SHA-256 pins and the frozen C11-C manifest.

## Read first

1. `docs/current/e/C11E_E6_CH004_SEMANTIC_NONINTERFERENCE_REVIEW_20261118_V2.md`
2. `docs/current/e/C11E_E6_D9_DEPENDENCY_PIN_RECONCILIATION_20261118_V1.md`
3. `docs/current/e/C11E_E6_CH004_HISTORICAL_SOURCE_PIN_ADJUDICATION_20261118_V2.md`
4. `docs/current/e/C11E_E6_SMOKE18_SCOPE_AND_EVIDENCE_AUDIT_20261116_V2.md`
5. `docs/current/e/C11E_E6_SMOKE18_TEST_ONLY_AUTHORIZATION_PROPOSAL_20261116_V2.md`
6. `docs/current/e/C11E_E5_CROSS_FAMILY_AV_CLOSEOUT_20261116_V1.md`
7. `docs/current/e/C11E_GATES_ACCEPTANCE_MATRIX_20261116_V171.md`
8. `docs/current/e/C11D_TO_C11E_FULL_FAMILY_ROADMAP_20261116_V117.md`

## Accepted and retained — do not repeat

- E4A Challenge, E4B Loop, E4C Drill 20/20 and E5 representative A/V are accepted in their declared scopes.
- E5 visible Qt GUI D99 runtime is accepted 3/3. The omitted `language=es` in one GUI test was an operator input omission, not a product defect.
- R1V human closeout 10/10 and Loop22 human closeout 44/44 are accepted. Do not rerun accepted A/V batches.
- Six Drill E4C receipts remain evidence-reuse candidates; do not rerun them.
- E6 D9 dependency reconciliation V2 passed: 13/13 focused tests, 13/13 fixed evidence pins, 33/33 source pins, 9/9 route dependencies, 2/2 observed historical hashes, zero failures.
- CH004 V1 adjudication recovered two E4A.7 Python preimages; V2 semantic review includes the third transitive D9.8 JSON preimage.

## Latest execution and defect

The operator ran the V2 apply package. PowerShell 5.1 AST, Python version, six add-only copies and frozen C11-C/D4.8 anchors passed. The installer then raised `NativeCommandError` at the capture of `python -m unittest -v`; verbose unittest progress is emitted to native stderr and PowerShell 5.1 promoted it to an ErrorRecord under `$ErrorActionPreference='Stop'`. This is an invocation/capture defect, not a demonstrated failed test. The semantic audit did not run in that attempt.

V3 changes only the installer and adds versioned documentation. The existing read-only audit runner and its 26 unit tests are byte-identical to V2. V3 captures Python stdout/stderr using `System.Diagnostics.Process`, validates exit codes and output, and probes create/write/delete permission in each payload destination directory, report output directory and Python temp directory before copying.

## Immediate action

Run `C11E_E6_CH004_SEMANTIC_NONINTERFERENCE_REVIEW_V3` once from Windows PowerShell 5.1. Its add-only payloads include the unchanged audit/test files (which should be `SKIPPED_IDENTICAL`) plus four new versioned docs. Do not rerun V2. A V3 installer error should be diagnosed from its first explicit `*_FAILED` token; do not loop by repeatedly reinstalling.

Expected next outcomes:
- `CH004_FOCUSED_TESTS=26/26_PASS`.
- `CH004_REPORT_STATUS=PASS` and report+sidecar verification, or a preserved semantic BLOCKED report with exact blockers.
- On semantic PASS, CH004 becomes `ELIGIBLE_FOR_E6_LEDGER_REQUALIFICATION_NOT_ACCEPTED` only.

## E6 continuation and render target

After CH004 semantic PASS, do not jump straight to media. Requalify CH004 against every E6 reuse predicate; hydrate exact per-selector receipts/media hashes for all six Loop candidates, all six Drill candidates and CH004 A/B/C without rerunning accepted batches. Missing evidence remains a reuse candidate, not a pass.

Freeze the proposed six Challenge selectors only from canonical authority (`001, 002, 004, 005, 006, 007` is still a proposal); `003` is excluded from the current sample due duplicate gameplay seed 314159, and `008/009` remain held by the duration conflict. Music seeds 840001/840002 are proposal-only, not approved execution values.

Prove the D-owned Challenge six-selector execution path in PREPARE_ONLY, including 18 E1 intent sub-probes and 18 D envelopes, and prove the runtime seam for the five fresh Challenge selectors. E4A.6/E4A.7 are CH004-specific; E3 audio is CH001-pilot-specific. Do not repurpose them as generic workers. Then freeze the 18 top-level rows (six Challenge, six Loop, six Drill) with exact nested evidence hashes and reuse predicates.

Finally prepare a separate E6 TEST_ONLY D4.8 resolution for the controlled Smoke18 render. It must resolve the existing D4.8 BLOCKED policy and list pinned tools/binaries, argv, process counts, output roots, expected artifacts, one-shot BatchId rules and stop conditions. No media process may run until this is explicitly approved.

## Historical timing context

CH_008/009 remain held because their declared 11-second duration conflicts with the 12-second phase sum (3+7+0+2). Do not rewrite canonical Challenge definitions or waive the discrepancy without an explicit duration decision.

## Permanent invariants

C11-C 2.19.12 and frozen manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` remain immutable. D4.8 R1V V2 remains BLOCKED. E1 PREPARE_ONLY; family adapter NOT_CONNECTED_E1; renderer OFF; dispatch/media false; `release_authority=NONE`.

No Godot, Movie Maker, D3/audio, FFmpeg, FFprobe or mux until separate E6 TEST_ONLY authorization resolves D4.8. No Git checks; commits operator-managed; source-file SHA-256 pins enforced.
