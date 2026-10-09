# D9 Suite Integration — Change Log

## D9.5.1 — Producer 0.10.0

- Added a C11-D Production Request + Personalization tab to the existing `c11c-producer` GUI.
- Kept all current C11-C Producer screens and launchers; no new app/suite.
- Added toolkit-independent D9 helper for D4 request mapping, the existing delivery profile alias resolver, D4.6 planning, and D4.5 exact parity comparison.
- Added evidence output per unique request under `artifacts/tests/c11d_d9/producer_gui/`.
- Added 90-case core matrix, 12-case personalization matrix and four negative checks.
- Updated Producer/Suite current tests, manifests and active docs; C11-C backend fingerprint and schema version unchanged.
- Runtime authority NONE; D4.8 BLOCKED; this increment creates plans only, not media.
- Operator confirms the GUI request/plan tab opens and creates plans in Windows. The tab remains plan-only; actual D text-to-render integration is deferred until the future C11-D production baseline is frozen.

## D9.6 — Catalog 0.2.0 overlay

- Preserved the existing artifact browser and added a C11-D Products/Provenance tab inside `c11c-catalog`.
- Added explicit D7.3/D7.4 canonical-intent projection, D9.4 manifest/hash-backed validation pilot rows and D9.5.1 Producer GUI plan rows.
- Added canonical D4.5 plan replay command copy for persisted plan-only requests; copying is not execution.
- Added pure-standard-library data projection tests and a static GUI contract test; wired both into `c11c-suite/self_test.py`.
- Version target delivered: Catalog 0.2.0. Renderer/production execution remain false; release authority remains NONE.
- Operator confirms Catalog works in Windows. The D9.4-listed pilot media remains validation-only and is not release-eligible.

## D9.7 — Config 0.2.0 overlay prepared

- Extended the existing `c11c-config`; no new suite/application.
- Added read-only D2–D9 contract inspection, SHA-256 and invariants validation.
- Added explicit operator presets with profile validation, required independent seeds, diff/hash, explicit save, backup and validated restore.
- Added seven configuration/seed/path negatives, an executable generic-editor protected-root contract, and isolated save/backup/validated-restore lifecycle tests; wired these into consolidated Suite self-test.
- The generic editor protects all profiles and project/suite roots; only the dedicated allowlisted Operator Profiles tab can write operator profiles. No renderer/production/release authority; Windows GUI acceptance pending.


## D9.8 — Universal Editorial Model V1

- Registered the canonical editorial model and strict resolver across the supported Challenge, Visual Loop and Visual Drill identities; Longform remains explicitly disabled.
- Added live inventory coverage and 25 negative controls. Editable editorial content remains separate from derived telemetry, provenance, seed governance and simulation truth.
- Model checkpoint only; no renderer or production activation.

## D9.9 — Producer universal coverage / Windows GUI smoke check

- Producer 0.11.0 adds universal editorial selection, scoped editing, canonical request/plan output and GUI/CLI parity to the existing Producer.
- The operator applied the UTF-8 CLI fix and Qt scope-handler fix, ran the focused and aggregate tests successfully, and confirmed Windows GUI plan generation for all currently implemented D content types.
- Longform remains disabled; Loop/Drill stay editorial-intent plans. No physical renderer or release authority.

## D9.10 — Editorial-to-render bridge planning

- Added canonical contract `definitions/c11d/production/C11D_EDITORIAL_RENDER_BRIDGE_D9_10_V1.json` and the pure plan-only mapping builder `tools/c11d/d9/editorial_render_bridge.py`.
- Producer 0.11.1 exposes a read-only bridge-planning output tab in the existing universal editorial view. The canonical CLI emits the same bridge record; GUI/CLI parity includes the record and record hash.
- Tested Challenge/Loop/Drill route planning, 3/3 CLI process parity cases and 15 negative controls. Tests are registered in Producer and consolidated Suite self-tests.
- Each planning record includes SHA-256 identities for the canonical bridge contract and the D9.8 editorial model in addition to request/editorial/plan identity. The bridge emits no renderer input, invokes no renderer, creates no media, and has no output artifact path. D4.8 remains BLOCKED and `release_authority=NONE`.
- The operator should confirm the newly added D9.10 output tab launches and shows the bridge record in Windows before this GUI addition is considered interactively accepted.
- Config 0.2.0 registers the bridge contract read-only and validates the non-execution/governance locks; its registry contained 22 canonical contracts at D9.10; D9.11 adds the maintenance policy and brings it to 23. See `docs/current/d/D9.10_EDITORIAL_TO_RENDER_BRIDGE_PLANNING_CHECKPOINT.md`.


## D9.11 — Maintenance 0.2.0 implementation

- Added `D9_11_MAINTENANCE_POLICY_V1.json` and registered it read-only in Config (23/23 contracts).
- The existing Maintenance GUI calls `tools/c11d/d9/maintenance.py` for dry-run plan, documentation audit, freeze preflight, allowlisted reversible cleanup, quarantine/restore and recovery operations.
- Only `c11c-suite/c11d-control` is eligible for legacy quarantine. The operation is not performed when applying the overlay; it requires explicit GUI/CLI confirmation and records the original tree and historical manifest file references in an append-only ledger.
- The historical C11-C manifest is never rewritten. Cleanup has exactly two allowed transient roots and archives rather than permanently deleting. Freeze preflight never creates a release archive.
- Static backend, Maintenance GUI-contract, prior cleanup/organization and aggregated Suite tests pass. Windows Maintenance GUI/operator acceptance remains pending; D9 stays OPEN and D10 BLOCKED.

## D9.10 addendum — D-only render-adapter envelope (2026-10-09)

- Added `definitions/c11d/production/C11D_RENDER_ADAPTER_BOUNDARY_D9_10_V1.json` and `tools/c11d/d9/d_render_adapter.py`.
- Canonical request + allowlisted editorial + production plan + bridge record now map to a versioned, hash-bound binding-preview envelope for Challenge, Visual Loop and Visual Drill.
- CLI includes the envelope; the existing Producer test GUI shows a `D-ONLY RENDER ADAPTER (PREPARED / OFF)` view and writes per-request `d_render_adapter_envelope.json`; GUI/CLI compares envelope identity.
- Adapter-specific negatives cover forged hash/fields, activation/dispatch/media claims, C11-C mutation and seed-domain violations. Adapter preparation is enabled, but no renderer input is emitted and there is no dispatch control.
- Config registers the adapter boundary read-only; canonical registry validation is 30/30.
- `tools/c11d/d9/capture_d910_acceptance.py` automates report/log generation for backend, CLI and static GUI-contract checks. It does not require screenshots and does not claim interactive Qt launch.
- Preserve the earlier plan-only checkpoint at `docs/history/c11d/d9/D9.10_EDITORIAL_TO_RENDER_BRIDGE_PLANNING_CHECKPOINT_SUPERSEDED_20261009.md`.

## D9.14 addendum — bounded production qualification passed (2026-10-09)

- Operator run `D914_COLON_FIX_20261009_E` generated and audited four final A/V MP4 outputs; eight qualification checks passed.
- Report SHA-256 `daa5e5676224d606e9d67ac7a7ed7e88c3c02a63c76ecdc579c3bc2dd320853f`; qualification-only baseline SHA-256 `15343119f0f8338b13b47b0ea98546e5470d4a1a8895b65dbe1f41ee183e66d3`.
- Challenge D3 Music Engine V5 mux, deterministic same-seed Loop replay and changed-music-seed isolation passed.
- This is qualification-only using proven generators; full D9.14 GUI/E2E remains blocked, D4.8 is BLOCKED, general D renderer dispatch remains OFF, D9.16/D9.17 remain blocked and release authority is NONE.


## D9.10 acceptance readme restoration fix (2026-10-09)

- Restored the two historical root README files exactly as specified by the immutable C11-C source manifest after a candidate preflight found them absent in the active checkout.
- This was a repository-inventory defect. No C11-C manifest rewrite, protected-code change, D adapter dispatch or renderer activation was performed.
- Prepared-workspace validation: candidate preflight PASS; 854/854 protected entries; 22/22 negative controls; five candidate blockers retained; freeze eligibility false. Automated D9.10 acceptance returns 5/5 with the default five focused checks.
- `operator_gui_runtime_observed=false` remains an accurate scope annotation, not an acceptance failure. Backend/CLI/static GUI checks need no screenshots. This does not claim the live GUI was launched by the acceptance runner.
- See `docs/history/c11d/d9/D9.10_ACCEPTANCE_README_MANIFEST_REPAIR_20261009.md`.
