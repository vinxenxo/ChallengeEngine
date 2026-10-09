# Challenge Engine V1.0 STATELESS — C11-D Roadmap

**Current phase: D9 — Suite integration/evolution, second stage. D9.4 is a closed media checkpoint; D9 remains OPEN until the canonical C11C Suite surfaces expose and certify the D branch end-to-end. D10 is BLOCKED.**

## Governing baseline

C11-C remains an immutable certified reference:

`ChallengeEngineV01_STATELESS_C11-C_2.19.12_FROZEN_20260930_175709.zip`

- ZIP SHA-256: `D85425CF18C5211C8497574F4FC66202D613EACC0EC14CD4E2FEF0B24F634A32`
- Tree SHA-256: `2D39B7B923B42CDC6647A4D25493B75023CDD19CEE18214BBDE1FDD295B8F256`

D7.5 remains the frozen D governance baseline used to open D8/D9:

`ChallengeEngineV01_STATELESS_C11-D_7.5_V8_FROZEN_20261008_111052.zip`

SHA-256: `396d9f4bfdbb44b4878acf06db8d6c1c385103c110de537a174632e93611cd1d`

The user's later local working tree contains the post-D7.5 D8/D9 implementation and must be treated as the current development state. **Do not roll back to the D9.4 upload or any older ZIP merely because it is easier to locate.**

## Non-negotiable governance

- `master_seed=NOT_ADOPTED`.
- Gameplay seed = `request.seed`.
- Music seed = `request.music_seed`.
- Cross-domain seed sharing = `FORBIDDEN`.
- Runtime derivation = disabled.
- Automatic seed generation = disabled.
- `D4.8 = BLOCKED` until a separately authorized future checkpoint changes it.
- `runtime_authority = NONE` unless explicitly elevated by a future contract.
- GUI and CLI are co-equal operator surfaces over the same canonical backend commands.
- No C11-C simulation/mechanics/RNG/truth refactor.
- No change to `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7/C9 contracts or logical 540×960 geometry during the current D9 integration stage.

## D9 purpose — corrected interpretation

D9 is **Suite integration/evolution**, not merely another test phase. The roadmap requirement is to extend the existing operator surfaces:

- `c11c-test` → validation, QA and acceptance;
- `c11c-producer` → production, review and job orchestration;
- `c11c-maintenance` → cleanup, organization, quarantine and freeze operations;
- `c11c-catalog` → catalog, products, provenance and reproducibility;
- `c11c-config` → configuration, profiles, snapshots and controlled editing.

No sixth operational suite is to be created. Historical `c11c-studio` material is archived context only and is **not an implementation dependency or target architecture**.

## Completed D milestones

- D0–D7.5: PASS/CLOSED; D7 FROZEN.
- D8.0–D8.7: PASS/CLOSED; media state remains governed separately from release authority.
- D9.0: real-media preflight PASS.
- D9.1: first physical Challenge video pilot PASS.
- D9.2: audio-enabled A/V pilot PASS.
- D9.3: deterministic A/V repeat + negative control PASS.
- D9.4: acceptance checkpoint PASS/CLOSED.
- D9.5.1: existing `c11c-producer` extended with D4 Request/Personalization planning surface. Producer version at D9.5.1: **0.10.0**. Windows GUI bring-up passed for that checkpoint; D9.9 expanded the same application to Producer 0.11.0; the additive D9.10 bridge-planning view is Producer 0.11.1.
- D9.6: existing `c11c-catalog` extended with D branch product/provenance/reproduction view. Catalog target/version: **0.2.0**. Windows GUI bring-up passed in the current working tree.
- D9.7: existing `c11c-config` extended with D contracts and controlled operator profiles. Config target/version: **0.2.0**. Overlay is prepared; Windows bring-up is pending explicit confirmation if not yet executed in the current context.

## D9 second-stage roadmap

### D9.8 — Universal editorial model

**Implementation status: PASS — canonical declarative model, strict resolver, live inventory and 25 negative tests. D9.8 is a closed model checkpoint only; it does not close D9.**

Create one declarative editorial model spanning the content system rather than a Challenge-only personalization surface.

Coverage:

- Challenge;
- Visual Loop;
- Visual Drill;
- Longform;
- family;
- subfamily / grammar / drill type;
- individual production override.

The model must distinguish editable editorial fields from derived telemetry, provenance and simulation truth.

### D9.9 — Producer universal editorial coverage

Extend the **existing `c11c-producer`** (Producer 0.11.0 at D9.9; 0.11.1 with D9.10 additive bridge planning) with the universal editorial tab: content type → family → subfamily/grammar/variant, editable scoped editorial fields, canonical request/plan output and reproducibility evidence. Both GUI and CLI use `tools/c11d/d9/universal_producer.py`; Challenge delegates to the existing D4 request/plan adapter, while Loop/Drill produce only a deterministic editorial-intent plan until the future D renderer baseline.

Required tests:

- all supported content types;
- all current families;
- all current subfamilies/grammars where represented;
- validation and normalization;
- GUI/CLI canonical plan parity;
- unsupported-field negatives;
- unchanged gameplay/music seeds.

**Implementation status: PASS (plan-only scope).** The inventory matrix resolves all 9 Challenge IDs, 27 concrete Loop grammars plus five family-level `auto` selectors, and 20 Drill type/tier variants. Separate CLI-process parity is certified for Challenge, Loop and Drill; 20 negative controls pass. Renderer/production remain off, `release_authority=NONE`, and the operator has now confirmed Windows GUI plan generation for all currently implemented D types without errors. This does not constitute real-media GUI acceptance or close D9.

### D9.10 — Editorial-to-render bridge planning

**Implementation status: PASS — deterministic bridge planning, 3/3 CLI-process record parity cases, 15/15 negative controls, static GUI contract and operator-confirmed Windows GUI output-tab check. This is plan-only acceptance; physical renderer integration remains deferred.**

The canonical contract `definitions/c11d/production/C11D_EDITORIAL_RENDER_BRIDGE_D9_10_V1.json` and backend `tools/c11d/d9/editorial_render_bridge.py` describe mappings from the D9.9 canonical plan to a future D renderer. Producer GUI exposes the resulting `EDITORIAL → RENDER BRIDGE (PLAN ONLY)` view; the CLI emits the same record, and parity checks compare the full record and hash.

The record is **not renderer input**. It only declares content identity, the current editorial allowlist, independent gameplay/music seed ownership, delivery/presentation references, provenance identities, and prerequisites for the future D frozen baseline. Renderer input is not emitted, no adapter is invoked, no media is created, `D4.8=BLOCKED`, and `release_authority=NONE`. Do not reopen or modify the frozen C11-C renderer to materialize editorial values. Physical implementation belongs to a future D frozen baseline after all listed gates are satisfied.

Focused validation: `python .\tools\c11d\d9\test_editorial_render_bridge.py`. The operator has confirmed the GUI displays the plan-only bridge record without errors.

### D9.11 — Maintenance integration

Implementation status: **Maintenance 0.2.0 implemented; static backend, Config, Maintenance contract and full Suite regression PASS; Windows Maintenance GUI/operator acceptance is pending.** The implementation stays inside the existing `c11c-maintenance` surface and delegates GUI/CLI operations to `tools/c11d/d9/maintenance.py`.

Expose and test:

- dry-run;
- repository organization;
- cleanup allowlists;
- quarantine;
- conflict handling;
- documentation consolidation;
- freeze preparation;
- protected-root enforcement.

The canonical policy `definitions/c11d/d9/D9_11_MAINTENANCE_POLICY_V1.json` is exposed read-only in Config. Cleanup has a two-root allowlist and archives reversibly instead of permanently deleting. The unregistered `c11c-suite/c11d-control` path can only be quarantined/restored by explicit operator confirmation; its legacy manifest references are recorded in an append-only ledger while `release/C11C_FREEZE_PACKAGE_MANIFEST.json` remains byte-for-byte unchanged. Freeze preflight is read-only, creates no archive and grants no authority.

Focused validation: `python .\tools\c11d\d9\test_maintenance.py`. Windows bring-up and operator review of the preview actions remain required.

### D9.12 — Test integration

Upgrade existing `c11c-test` to target **0.2.0**.

Register D2–D9 contracts and GUI integration tests without duplicating the canonical backend. Test must provide explicit routes for:

- D request/personalization;
- seed governance;
- catalog/provenance;
- media QA;
- negative controls;
- GUI/CLI parity;
- real-media GUI certification.

### D9.13 — Cross-suite lifecycle

Prove the same production intent survives:

`Config → Producer → Test/QA → Catalog → Maintenance`

with a single identity/provenance chain and no suite-specific reinterpretation of seeds, profiles or editorial payload.

### D9.14 — Real GUI production certification

Run real Windows GUI cases. Certification is not satisfied by button reachability. A GUI production job must be observed from request through output, QA, catalog and reproduction.

Minimum end-to-end set:

1. Challenge personalised video.
2. Visual Loop personalised video.
3. Visual Drill personalised video.
4. Longform personalised video where supported by the D production contract.
5. Same configuration repeated → deterministic reproduction.
6. Changed music seed → changed audio/product identity.
7. Changed editorial text → changed editorial identity/output.
8. Invalid request → blocked.
9. Protected-root mutation → blocked.
10. Release mutation without authority → blocked.

### D9.15 — GUI operational acceptance

Verify from the GUI that an operator can inspect and operate the actual D state: configuration, production, validation, catalog, provenance, logs, maintenance and reproducibility.

### D9.16 — D9 final acceptance

Run the full Suite acceptance with GUI/CLI parity, real-media evidence, negative cases, protected-root checks and documentation closure.

### D9.17 — D9 CLOSED

Only when D9.8–D9.16 are accepted. D10 remains BLOCKED until D9.17 closes.

## Suite version/update plan

| Surface | Current/confirmed D9 version | Next target | Required acceptance |
|---|---:|---:|---|
| `c11c-suite` shell | 0.1.4 | keep 0.1.4 unless common launcher contract changes | full launcher/registry acceptance |
| `c11c-producer` | 0.11.1 | 0.11.x only for approved additive D coverage | universal request → editorial resolution → plan-only; real media remains a later authorized D gate |
| `c11c-catalog` | 0.2.0 | 0.2.x | product identity → provenance → reproduction |
| `c11c-config` | 0.2.0 | 0.2.x | profiles → validation → save/restore → protected roots |
| `c11c-maintenance` | 0.2.0 implemented; Windows acceptance pending | 0.2.0 | dry-run → reversible allowlist archive/quarantine → doc/freeze preflight |
| `c11c-test` | C11-C active baseline | 0.2.0 | D2–D9 registration + GUI E2E + negative acceptance |

Versions labelled “next target” are planning targets, not claims of current release.

## D10 gate

D10 = **BLOCKED** until:

`D9.17 PASS/CLOSED`

and the GUI has successfully demonstrated the complete operator lifecycle for the unified content/editorial model.
