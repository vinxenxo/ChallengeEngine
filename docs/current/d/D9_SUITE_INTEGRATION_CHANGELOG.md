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
- Config 0.2.0 registers the bridge contract read-only and validates the non-execution/governance locks; its registry now contains 22 canonical contracts. See `docs/current/d/D9.10_EDITORIAL_TO_RENDER_BRIDGE_PLANNING_CHECKPOINT.md`.
