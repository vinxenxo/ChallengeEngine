# C11-D Project Context and Governance Guide

**Revision:** 2026-10-16 (Europe/Madrid)  
**Purpose:** durable project-level context for a fresh assistant window; this is a documentation add-on, not a code change or an approval.  
**Authority rule:** this guide is subordinate to the frozen C11-C artifacts and the active Windows checkout. For C11-D continuity, the dated 2026-10-16 continuity checkpoint and its paired start/handover documents supersede older context wording when it conflicts. Historical documents remain useful evidence of lineage, not necessarily current instructions.

## 1. Product and engineering intent

ChallengeEngine V01 STATELESS is a deterministic Godot 4.7.1 content/challenge-video factory intended to produce vertical short-form video material for TikTok, Reels and Shorts. The long-term direction is not just a renderer: it is a production system that can select a supported content type, family, subtype/grammar, variant/tier and editorial configuration through the existing Producer workflow, then bind those choices to deterministic simulation/visual inputs and a shared, renderer-agnostic presentation layer.

The C11-D design must scale across three current content classes:

- **Challenges:** the existing nine challenge IDs / families / variants.
- **Visual Loops:** five families and 27 concrete grammars in the currently recognized catalog.
- **Visual Drills:** four drill types (`tracking`, `pursuit`, `saccade`, `peripheral_scan`) with five tiers each (20 authoring selectors).

Longform is not an enabled content type. `LONGFORM_1080` is a delivery profile only; it is not evidence of a supported Longform type. Unsupported/unknown types and selectors must fail closed.

The user’s stated end goal is robustly moving from the frozen C11-C implementation to a formally accepted C11-D implementation/Producer. The cutover is conditional: C11-D may replace C11-C as authority **only after** all required gates have closed, the D baseline has formal approval, freeze/promotion are explicitly completed, and the final acceptance evidence supports that decision. Do not perform a premature replacement.

## 2. Frozen C11-C baseline and non-negotiable boundary

Canonical C11-C release: **C11-C 2.19.12**, represented by the frozen package named:

`ChallengeEngineV01_STATELESS_C11-C_2.19.12_FROZEN_20260930_175709.zip`

Frozen ZIP SHA-256:

`D85425CF18C5211C8497574F4FC66202D613EACC0EC14CD4E2FEF0B24F634A32`

Frozen tree SHA-256:

`2D39B7B923B42CDC6647A4D25493B75023CDD19CEE18214BBDE1FDD295B8F256`

Canonical `release/C11C_FREEZE_PACKAGE_MANIFEST.json` SHA-256:

`e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`

Treat the baseline, its manifest and freeze package as immutable source-of-truth artifacts. Do not repair a D defect by editing C11-C, re-running its generation, replacing its manifest, or using an extracted D context ZIP to overwrite it. Any snapshot containing duplicate manifest entries must be inspected and normalized in a separate workspace; never extract the whole context ZIP over the active checkout.

C11-C product/presentation invariants retained by D:

- Simulation/gameplay truth remains separate from presentation. No new mechanics, changed outcome, modified challenge logic or hidden simulation mutation as part of renderer preparation.
- `winning_frame` is the sole temporal anchor for outcome-aligned Challenge presentation.
- `close_calls` means an episode count, not a timing signal or frame index.
- The existing shared frame reference is 540 × 960, with Header 0–144, Body 144–816, Footer 816–960; `UnifiedSocialFrame`, `CoordinateMapper` and `PresentationFramer` are established C11-C presentation concepts. Delivery scaling to 720 × 1280 / 30 FPS is a later output concern and must not be applied during source-timebase previews.
- No AI or external creative assets are part of the currently approved content generation scope; visual treatments should follow the established premium mathematical/visual language and the project’s source-driven palettes/assets.

## 3. C11-D architecture and operational surfaces

C11-D extends the existing five `c11c-suite` operational surfaces. It must not create a sixth `c11d-control` operational surface:

- `c11c-test`
- `c11c-producer`
- `c11c-catalog`
- `c11c-config`
- `c11c-maintenance`

Existing GUI surfaces are D-compatible adapters over canonical D services, not independent logic engines. Preserve GUI/CLI parity and add tests at service, CLI and GUI-facing boundaries as appropriate. Avoid duplicating canonical model/binder/review behavior in GUI code.

Architectural layers to keep distinct:

1. **Catalog and selectors** — defines supported content types, families, grammars/subtypes, challenge variants and drill tiers.
2. **Canonical editorial model (D9.8)** — field allowlist, normalization, scopes and inheritance.
3. **Universal Producer/plan adapter (D9.9)** — canonical requests and plans; deterministic, shared GUI/CLI intent generation.
4. **Editorial-to-render bridge (D9.10)** — planning/adapter envelope only; it remains `PREPARE_ONLY` until the required D baseline and gates authorize more.
5. **Renderer-candidate request→payload binder** — request-scoped selection, schema/identity/source pins, manifest and lineage checks. This is still not renderer input admission.
6. **Renderer-neutral candidate I/O boundary** — a versioned, source-pinned, strict contract for an eventual renderer. Candidate identity inventory and I/O gap audit assess completeness but do not grant authority.
7. **Shared presentation/editorial policy** — regions, field routing/visibility, coordinates/samples/composition, timebase/temporal schedule and audio/music delivery. Policies have been proposed and cross-checked in review; this is not equivalent to approval to consume them in media.
8. **Future D-owned renderer and actual media production** — prohibited until the required acceptance and governance gates are closed and explicitly authorized.

The shared editorial/presentation layer is the default across Challenges, Visual Loops and Visual Drills. Family-specific exceptions require explicit documentation and review; a new family should inherit common policy unless it carries an explicitly approved exception.

## 4. Editorial model and GUI expectations

D9.8 establishes the canonical Universal Editorial Model. Known user-facing editable fields are:

- Shared across Challenge / Loop / Drill: `title`, `subtitle`, `call_to_action`, `language`.
- Challenge-only: `player_name`, `challenge_label`.
- Reserved presentation/renderer fields stay disabled until their request/binder contracts and policy approvals exist.

Inheritance order: `global → content_type → family → subtype → variant → production_override`. Unknown scope/field, invalid values and unsupported selectors must be rejected. Editorial overrides must not mutate telemetry, provenance, seeds, simulation outputs or other runtime truth.

Canonical draft lifecycle already designed for the GUI/service boundary:

- Overrides are request-scoped and in memory.
- Shared editorial overrides survive content type/family/selector changes when those fields remain applicable.
- Challenge-only fields are deleted when leaving Challenges.
- Clearing an override returns resolution to canonical D9.8 profile values.
- Explicit empty strings normalize to `UNKNOWN` rather than silently bypassing the model.

The GUI editorial view model is composition over the established services. It must not fork their implementation. Existing Loop/Drill production restrictions remain in force; a UI choice or a view-model PASS does not make a restricted type producible.

## 5. Determinism, seeds and request identity

Current required rules:

- `master_seed=NOT_ADOPTED`.
- Gameplay uses `request.seed`.
- Music uses `request.music_seed`.
- Cross-domain seed sharing is forbidden; runtime/automatic seed derivation is disabled.
- Equal numeric seed values are rejected for paired cross-domain input where the collision policy applies; missing/invalid seed forms reject before Godot for each tested content type.
- Request identity, selected variant/tier, source provenance, visual state, visual payload and editorial values must not be conflated. A gameplay seed change must affect the appropriate Challenge/Loop/Drill state; a music seed change must not perturb the visual/gameplay payload.
- Reproducibility must be established through independent repeats and preserved receipts. Source pins, schemas, reports and request-specific manifests must be hash-bound.

The most recent cross-type audit is deliberately narrow: one Challenge selector (`parking_v2 / CHALLENGE_004`) plus one Visual Loop selector (`c11c_geometric_waves_v1 / harmonic_membrane`). It is a useful proven slice—not proof that every challenge, grammar and request shape is covered.

## 6. Renderer candidate preparation status

D10 is a preparation track for the future D-owned renderer baseline. It is not a live renderer or production authority. Work completed/planned to date includes:

- Renderer-neutral frame program candidate and region hierarchy reconciliation.
- Source-bound temporal preview and temporal schedule proposal.
- Delivery timebase projection proposal (keep source timebase distinct from delivery resampling).
- Profile identity separation.
- Challenge runtime output and visual payload previews.
- Visual Loop grammar binding audit and composite payload integration.
- Request-scoped payload binding/materialization previews and request-specific payload manifest work.
- Editorial field-window proposal, field-consumption audit, routing/visibility reconciliation and Unified Content Review integration.
- Candidate identity inventory and strict candidate I/O contract/gap audit.
- Visual Drill authoring selector coverage.
- Cross-type seed-domain sensitivity/orthogonality runtime audit and collision rejection regression.

These components form evidence and contracts for a future renderer; they do not mean that a complete renderer exists. Keep these categories separate:

- **Authoring coverage** is not request-bound payload acceptance.
- **Payload materialization/binding** is not renderer-input admission.
- **A candidate I/O contract PASS** is not candidate I/O completeness.
- **A preparation-only audit PASS** is not production acceptance.
- **A preflight that correctly reports BLOCKED** is a passing preflight, not a passed gate.
- **A no-media test** cannot be used as proof that real media production works.

The existing candidate I/O gap audit currently has ten assessed groups and has been described in preparation evidence as 0 complete, 6 partial and 4 blocked. Verify the current active Windows report before relying on those counts, because they were observed in an isolated/preparation workspace and source-pin totals changed across iterations.

## 7. D9/D10 governance state

Historical/accepted development sequence: D0–D8.7 are recorded PASS/CLOSED; D9.8–D9.13 contain accepted canonical model, universal Producer, bridge planning, Maintenance, Test and lifecycle integration. D9.14 introduces real GUI/media production certification and remains a hard gate; D9.15 contains operator/GUI evidence and its local ledger/quarantine lineage; D9.16 is full acceptance; D9.17 closure adjudication is the final D9 closure decision. D10 tracks D-baseline/renderer-candidate preparation in parallel and is blocked from promotion until the governance decisions close.

At this handover boundary, do not relabel any of the following as PASS/closed merely because focused audits pass:

- `renderer=OFF`
- `media_created=false`
- `D4.8=BLOCKED`
- `release_authority=NONE`
- `baseline_approval=MISSING`
- `freeze_eligible=false`
- D9.14 / D9.16 blocked for actual acceptance/real media as required
- D9.17 `BLOCKED_NO_GO`
- D10 blocked from final baseline approval, freeze, promotion and cutover
- D9.10 adapter `PREPARE_ONLY`

The latest frozen-manifest comparison must remain equal to the exact SHA above. Never change the governance state solely to make a preflight green.

## 8. Latest operator-confirmed Windows evidence — 2026-10-15

The operator provided the following actual console output in the prior context and explicitly confirmed it was green:

### Seed collision regression

`test_d_renderer_seed_domain_collision_audit.py`: **7 tests PASS**. The seven checks cover 23 pinned sources, selector scope, equal numeric seed rejection before Godot for each tested selector/value, strict-schema/non-admissible status, missing/invalid seed forms, no Godot invocation/no artifacts, and fail-closed behavior when collision policy is weakened.

### Cross-type seed-domain runtime audit

Godot used in the operator's environment was:

`C:\Users\vinxe\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine.Mono_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.1-stable_mono_win64\godot.exe`

Auditor-confirmed engine version: `4.7.1.stable.mono.official.a13da4feb`.

Console summary:

`C11-D CROSS-TYPE SEED DOMAIN AUDIT PASS | selectors=2 | gameplay_seed_sensitivity=2/2 | music_seed_orthogonality=2/2 | independent_repeats=6/6 | source_pins=18/18 | runtime_invocations=12 | seed_domains_complete_for_candidate_input=false | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE`

- Runtime invocations: 12.
- Independent canonical receipts: 12/12.
- Gameplay sensitivity: 2/2.
- Music orthogonality: 2/2.
- Independent repeats: 6/6.
- Source pins: 18/18 for this audit.
- Audit SHA-256 field: `94cef68056e7fd5876e64642746012e3ba9c8e8106b03a3d78dd609d8eea7053`.
- stdout SHA-256: `d2563c122dac6548f0fe1e4ced1d069b071ccd2ee50896a43cdf655b660a1594`.
- stderr SHA-256: `98f4a2c4df3c95b2b4c4472f2e0098b40d7268cdb7b6272e7762cd7511c2620f`.
- Operator evidence directory: `C:\Users\vinxe\AppData\Local\Temp\C11D_CROSS_TYPE_RECOVERY_20261015_184503`.

The audit report explicitly remains `PREPARATION_ONLY_CROSS_TYPE_SEED_DOMAIN_AUDIT_NOT_INPUT_ADMISSION`, `seed_domains_complete_for_candidate_input=false`. Open requirements include other Challenge selectors, other Visual Loop grammars, automatic/default seed behavior, arbitrary-request cross-domain behavior, and continued separate Visual Drill V2 coverage. No renderer dispatch, renderer input, production execution, receipt-file write, payload persistence, output artifact or media creation was performed. The run is a true runtime evidence point, but intentionally not a promotion gate.

### Baseline integrity

The collision audit and the cross-type audit preserved the canonical C11-C manifest hash:
`e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

The overlay previously applied by the operator is `C11D_SEED_DOMAIN_COLLISION_REJECTION_AUDIT_OVERLAY_20261015_V2.zip` (SHA-256 `b236f344708dd86d6f40745aa83ca3485feb897e85e6a5f9ffbcf9f33e40ff93`), with 17 paths (12 replacements and 5 additions), applied successfully with 17/17 preconditions and 17/17 final hashes. Backup reported at `C:\Users\vinxe\AppData\Local\Temp\C11D_SEED_COLLISION_V2_BACKUP_20261015_182856`.

Do not reapply that overlay or any older V1; it is already installed in the operator's active checkout.

## 9. Repository, package and evidence handling

- Active Windows checkout is the authority for current files and local evidence. User runs PowerShell from `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`.
- The latest source snapshot available in the context library at the time of this handover is `ChallengeEngineV01_STATELESS_C11-D10-NORMALIZED-NIGHTLY_20261014(1).zip` (Oct. 14 context package; SHA-256 of the exact materialized file: `05738cfaa851d93d398fca24bc9ab1dc7f32d2cd04ab023a088dc25e790fb5a3`); it predates the Oct. 15 seed-audit V2 overlay and therefore is not the active checkout or a complete export of the latest Windows state.
- Earlier context ZIPs may be normalized snapshots, have duplicate `release/C11C_FREEZE_PACKAGE_MANIFEST.json` entries or omit operator-local D9.15 ledger/quarantine evidence. Inspect them in a scratch location; never extract them wholesale over the active checkout. Missing-from-export does not imply missing-from-Windows.
- Keep raw runtime receipts, stdout/stderr and report hashes. When evidence is in `%TEMP%`, it is ephemeral; archive it into the repository's approved evidence location only if the applicable contract authorizes evidence copies. Do not invent receipts from report summaries.
- Keep every claim tagged as one of: operator-confirmed Windows runtime; isolated normalized-package/Python validation; source inspection; planned/not tested. These are not interchangeable evidence classes.

## 10. PowerShell/runtime discipline (important lessons)

User's preferred workflow is direct, additive ZIP overlays and practical pasted PowerShell from the repository root. Do not spend a development iteration on an elaborate launcher.

- Resolve Python as the user's existing Python/runtime setup dictates; do not hardcode a guessed Python path if `$pythonExe` already exists in the session. Keep commands short and explicit.
- Resolve Godot from the already-established `$godot` variable, `C11D_GODOT_EXECUTABLE`, or `Get-Command godot.exe`/`Get-Command godot` as suitable. Do not hardcode `C:\Godot\Godot_v4.7.1-stable_win64_console.exe`; that path is not present on the user's system.
- The actual Windows installation path above may be used as corroborating past evidence, but do not make it a permanent hardcoded dependency.
- PowerShell 5.1 may convert Python `unittest` stderr output into `NativeCommandError` despite the test passing. For cases where redirection is needed, use `Start-Process` with explicit stdout/stderr paths and check the real `$process.ExitCode`; independently check the expected summary markers before printing PASS. Avoid direct native redirection under `$ErrorActionPreference='Stop'` when that behavior masks exit status.
- Do not print PASS if the command did not run, if exit code is unknown/nonzero, or if expected report/receipt markers are absent. No hand-typed PASS placeholders.
- Avoid malformed interpolated strings such as `"$Label: ..."` in PowerShell 5.1; use `${Label}` or `-f` formatting. Avoid partial `try/catch/finally` fragments. One complete, pasteable block is preferable.
- Separate overlay integrity/apply from tests/regressions, and tests from any evidence archival action. Stop on first genuine failure. Do not silently set global preferences or modify the user's shell for convenience.

## 11. Path toward the first D render — gated engineering sequence

The destination is a D-owned first-render capability that is deterministic, reviewable, safely bounded, and replaceable without mutating C11-C. Work toward it in this order; adjust only after the active repository proves a prerequisite has already been completed.

1. **Reconstruct the live truth.** Read this guide, the paired checkpoint, current renderer preparation plan, dynamic request→payload binder checkpoint, candidate I/O contract/gap and identity inventory, unified content review, D9 gate checkpoints and milestone/roadmap. Diff active files against the current source snapshot and overlays; record source hashes. Do not duplicate existing functionality.
2. **Close deterministic identity and seed-domain coverage.** Preserve the proven collision policy; expand cross-type matrices beyond the current two selectors where required by source/I/O contracts. Keep Challenge, Loop and Drill coverage distinct where their contracts differ. Verify explicit, missing, invalid and automatic/default seed behavior according to current request contracts. Require repeatability, seed sensitivity/orthogonality, source pinning, exact selectors, lineage and fail-closed negatives.
3. **Close request-scoped binding/materialization.** The existing binder is canonical; extend it rather than introducing a parallel binder. Every accepted request must bind canonical selector/type/family/subtype/variant/tier, source and policy lineage, content-specific payload, stable manifest/digest and deterministic identity. Unknown/mismatch/schema/source-drift cases fail closed. Run full supported matrices through the real Godot 4.7.1 harness where the contract demands runtime evidence.
4. **Close candidate I/O gaps.** Use the gap audit to identify actual missing invariants across its ten groups. Do not simply label partial/blocked groups complete. Require a source-pinned identity inventory, exact schema/payload boundary, stable provenance and report/receipt chain. A binder PASS must not be mistaken for an I/O completeness PASS.
5. **Unify shared visual policy.** Reconcile shared frame/regions, editorial field routing/visibility, coordinate mapping/projection, sample/temporal alignment, `winning_frame`, delivery timebase, audio/music and policy inheritance. Most policy artifacts are proposals or review cross-checks. Obtain explicit policy approvals before implementing consumption in a media-producing path. No family exception by assumption.
6. **Define the renderer admission boundary.** D-owned renderer input must only be constructible from fully admitted canonical request/payload + reviewed frame/presentation instructions. Strict schema, provenance, deterministic identifiers, inputs and output containment must be testable. The renderer remains OFF while candidate/contract tests are developed.
7. **Execute controlled first-render acceptance only after authorization.** The first media-producing action is a separately approved gate, scoped to a minimal supported selector, with exact command/version, bounded output paths, reproducibility, actual media inspection, frame/timeline/audio checks, no mutation of source truth, negative tests and retained evidence. Do not make a render just to turn a test green. No artificial waiver of D4.8/D9.14/D9.16/D9.17.
8. **Close full application acceptance.** Verify all five existing GUI operational surfaces, GUI/CLI parity, lifecycle, supported content and selector coverage, all regression suites (`tests\run_all.py`, plus the frozen C11-C suite), baseline preflight, operator acceptance receipts and governance/lineage requirements. Every failed/blocked gate remains explicit.
9. **Formal D baseline acceptance and cutover.** Only after all required gates PASS and an authorized human decision exists may the D baseline become approved/freeze-eligible; complete release/freeze/promotion steps with signed hashes/evidence and rollback/recovery instructions. Then and only then replace the frozen C11-C baseline and Producer as active authority. Preserve C11-C unchanged as historical rollback/reference.

## 12. What a useful engineering increment must include

For each increment, report: (a) source files/contract changed and why the gap is real; (b) preconditions/hash-pins; (c) focused contract/unit tests, adversarial negatives and real runtime cases as required; (d) regression tests; (e) source/report/evidence hashes; (f) what remains blocked; (g) whether the work is source inspection, isolated validation or Windows acceptance; and (h) next checkpoint. Package code changes as additive overlays (ZIP rather than `.patch`, changed/new files only), unless the operator explicitly asks for a full snapshot. Documentation overlays may add versioned artifacts without overwriting mutable continuity files.
