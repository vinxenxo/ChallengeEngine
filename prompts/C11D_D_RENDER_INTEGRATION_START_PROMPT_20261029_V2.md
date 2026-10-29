# C11-D Render Integration — Start Prompt V2 (29-10-2026)

Active source of truth: `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. The uploaded snapshot is context only. Do not generate another snapshot or extract it over the checkout.

## Read first

1. `AGENTS.md` and `.continue/rules/CONTINUE.md`.
2. `docs/current/d/C11D_DOCUMENTATION_INDEX_AND_ARCHIVE_POLICY_20261029_V2.md`.
3. `docs/current/d/C11D_SNAPSHOT_VALIDATION_AND_DOCUMENTATION_REORGANIZATION_20261029_V1.md`.
4. `docs/current/d/C11D_DOCUMENTATION_CATALOG_GENERATED.md` after running the new organizer, if it exists.
5. `docs/current/d/C11D_FUNCTIONAL_RECOVERY_AND_MEDIA_ACCEPTANCE_PLAN_20261029_V2.md` and `C11D_RENDER_INTEGRATION_READ_ORDER_20261029_V2.md`.
6. Ledger V18, Checkpoint V41, Phase AD closeout/receipt, and the existing AD decision packet JSON + Markdown.
7. `docs/current/c11c/C11-C_2.19.12_ACCEPTANCE_EVIDENCE.md`, `C11-C_2.19_CONSOLIDATED_ACCEPTANCE_GATE.md` and the C freeze packaging command sheet.

## Starting state

- Filtered snapshot validated: ZIP SHA `5b8d06ad82bca798c94db03f943a85afb309d91484d4499ed40fed36056ca774`, 9,190,399 bytes, 3,721 unique entries; per-file inventory and canonical C-manifest hash passed.
- Phase AD tests 60/60 and the verifier pass; do not repeat them unless pinned inputs changed.
- AD operator decision: pending; evidence records 0; adjudications 0; policy adoption NONE.
- Renderer OFF, candidate input inadmissible, seed domains incomplete, master seed not adopted, approved bindings 0, D4.8/D9.14/D9.16 blocked, D9.17 NO-GO, D10 blocked, no baseline approval/freeze/release authority.
- The principal technical gap is that D9.9/9.10 plans/envelopes remain non-renderable and no proven D visual consumer connects editable fields to the final compositor.

## First actions

1. Verify active-checkout hashes for `AGENTS.md`, `.continue/rules/CONTINUE.md`, the canonical C manifest, Ledger V18, Checkpoint V41 and Phase AD packet. If the active checkout has newer versions, reconcile and use the newer verified state; never overwrite from the snapshot.
2. Run `& .\tools\c11d\documentation\organize_c11d_documentation.ps1 -PreflightOnly`, inspect the category/count output, then run it without the switch to generate the live Markdown/JSON catalog. It creates navigation files only and moves no existing documents.
3. Inspect actual C physical-production runners and the Producer `GENERAR` path. Then trace D9.9 canonical request/plan → D9.10 bridge/adapter → request-scoped payload/binder → source-frame/composition consumer → actual renderer → D3 music/mux. Record source hashes.
4. Implement the smallest allowed D-only source integration increment when the contracts permit it; add focused tests. Do not rerun broad audits just because the docs are numerous.
5. Keep Godot D renderer/media execution blocked until the existing AD authority packet and downstream gates explicitly permit it. A general request to continue toward rendering is not policy adoption.

## Completion expected

Report the concrete C→D call graph, the missing consumer/integration point, the minimum code change and focused tests. Do not stop at a generic design proposal. When, and only when, renderer execution is authorized, generate and validate one physical A/V MP4 for Challenge, Loop and Drill, then smoke 18 and matrix 101. Preserve C11-C unchanged.
