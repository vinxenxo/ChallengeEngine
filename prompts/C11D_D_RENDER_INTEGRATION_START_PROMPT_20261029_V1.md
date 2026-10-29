# C11-D Render Integration — Start Prompt V1 (29-10-2026)

Active checkout (source of truth): `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`.

## Read first

1. `AGENTS.md`
2. `.continue/rules/CONTINUE.md`
3. `docs/current/d/C11D_DOCUMENTATION_INDEX_AND_ARCHIVE_POLICY_20261029_V1.md`
4. `docs/current/d/C11D_FUNCTIONAL_RECOVERY_AND_MEDIA_ACCEPTANCE_PLAN_20261029_V1.md`
5. `docs/current/d/C11D_FULL_CONTEXT_CONTINUITY_CHECKPOINT_20261029_V41.md`
6. `docs/current/d/C11D_ENGINEERING_PHASE_LEDGER_20261029_V18.md`
7. `docs/current/d/C11D_PHASE_AD_EXECUTION_CLOSEOUT_20261029_V1.md`
8. `docs/current/d/C11D_PHASE_AD_OPERATOR_AUTHORITY_DECISION_GATE_20261029_V1.json` and companion Markdown
9. `docs/current/c11c/C11-C_2.19.12_ACCEPTANCE_EVIDENCE.md` and `docs/current/c11c/C11-C_2.19_CONSOLIDATED_ACCEPTANCE_GATE.md`
10. `docs/current/d/D9.14_PRODUCTION_QUALIFICATION_RUNBOOK_V1.md`
11. D9.8/D9.9/D9.10, current candidate I/O gap, request-scoped payload instance/binding, editorial field-consumption and temporal/presentation checkpoints named in the index.

## Start state

- Phase AD closeout: PASS; its 60/60 tests do not need repeating unless their sources change.
- User authorized render testing on 2026-10-29; this is test intent, not release/freeze/promotion authority.
- C11-C manifest must remain SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`, size 796318.
- Renderer status/gates must be read from the current checkout, not copied from an old ZIP.
- The current main functional gap is the transition from canonical D request/editorial values to the visual composition actually used in final video. Historic audit was 0/14 visual editorial fields consumed; verify whether subsequent source changed this.

## First task — do not create another generic preparation phase

1. Confirm the active-checkout pins and C-manifest immutability. To create the uploadable filtered snapshot in one command, run `tools/c11d/packaging/New-C11DWorkingSnapshot.ps1`; it writes the ZIP plus `.sha256` and `.report.json` outside the checkout. Use `-PreflightOnly` only when you want counts/exclusions without creating files. Do not upload/extract an old full freeze ZIP.
2. Inspect, without modifying, the actual production entrypoints called by `tools/qa/c11/run_c11c_challenge_bulk_qa.ps1` and `tools/qa/c11/run_c11c_complete_video_review.ps1`; map the Producer/GUI/CLI route and final compositor/renderer entrypoint. Also inspect `c11c-suite/c11c-test/BUILD_MANIFEST.json`.
3. Compare those inputs to the D9.9 canonical request/plan, D9.10 envelope, request-scoped binder, editorial sidecar, visual payload and D3 audio/mux chain. Reuse the canonical components; no parallel binder.
4. Implement the smallest D-only consumer/composition slice that makes a canonical editable field visibly affect frames while leaving C core/mechanics/RNG untouched. If the exact gate contract blocks a real run, state the specific field/decision/checkpoint and avoid bypassing it; do not reopen already-passed generic audits.
5. Run a real test-only MP4 for one supported selector in each family, with unique output root and full stdout/stderr/exit evidence. Validate video/audio properties and visible editable-field changes. Then expand the family smoke to 18 and full matrix to 101 videos.

## Output expected from this window

Report the exact C→D call graph, the source paths/hashes and minimal missing implementation, then make the first code increment as soon as the inspected contracts allow it. Deliver focused tests and three physical MP4 results; do not stop at a document-only proposal or static plan. Preserve C11-C and its manifest byte-for-byte.
