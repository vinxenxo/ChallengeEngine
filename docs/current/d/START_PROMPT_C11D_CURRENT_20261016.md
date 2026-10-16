# C11-D Start Prompt — Full Context / Continuity 2026-10-16

> **This is the controlling start instruction for a new context window.** Read it fully. Read the companion Master Handover, Continuity Checkpoint and Project Context/Governance Guide before making changes. This prompt intentionally carries the full project context and remaining lifecycle, not just the next test. Historical instructions preserved in older prompts are historical unless explicitly reaffirmed here.

## 1. Mission

Continue development of ChallengeEngine V01 STATELESS C11-D from the exact state described in `C11D_FULL_CONTEXT_CONTINUITY_CHECKPOINT_20261016.md`, toward a safe D-owned first render and ultimately formal D baseline acceptance, freeze, promotion and replacement of C11-C. Work incrementally, verify from the actual active checkout, update documentation at important phase boundaries, and preserve all governance controls. Do not stop at explaining the next step: create the next durable code/documentation increment when the repository state and evidence support it.

The product goal is a deterministic, renderer-agnostic production system spanning Challenges, Visual Loops and Visual Drills, with a single canonical editorial/presentation layer and GUI/CLI parity. Future GUI workflow should choose content type, family, grammar/subtype, challenge variant or Drill tier and edit all permitted video text, without introducing separate logic per family. Shared policy is default; exceptions must be explicit and approved.

## 2. Read-first package order

1. `docs/current/d/START_PROMPT_C11D_CURRENT_20261016.md` (this file).
2. `docs/current/d/MASTER_HANDOVER_C11D_CURRENT_20261016.md`.
3. `docs/current/d/C11D_FULL_CONTEXT_CONTINUITY_CHECKPOINT_20261016.md`.
4. `docs/current/d/C11D_PROJECT_CONTEXT_AND_GOVERNANCE_GUIDE_20261016.md`.
5. In the active repository, inspect `AGENTS.md`, `.continue/rules/CONTINUE.md`, `docs/current/d/C11-D_ROADMAP_V1.0_STATELESS.md`, `docs/current/d/C11-D_MILESTONES_APPROVED.md`, `docs/current/d/D_RENDERER_BASELINE_PREPARATION_PLAN_V1.md`, `docs/current/d/D_RENDERER_DYNAMIC_REQUEST_PAYLOAD_BINDING_CHECKPOINT_V1.md`, candidate identity inventory, candidate I/O contract/gap audit, Unified Content Review, D9.13 lifecycle, D9.14/D9.15/D9.16/D9.17 and `D9_GUI_E2E_CERTIFICATION_PLAN_V1.md`.
6. Read the actual referenced contract/schema/source/tests before proposing edits; do not rely on an older prompt's copied snippets when current source is available.

If the context ZIP is available through Files/Library, use it to inspect source structure and historical documentation. It is an Oct. 14 normalized snapshot (SHA-256 `05738cfaa851d93d398fca24bc9ab1dc7f32d2cd04ab023a088dc25e790fb5a3`), predating the Oct. 15 V2 seed collision overlay. The active Windows checkout and its operator-local records remain current truth. Never extract the entire snapshot over the active checkout, particularly because older packages may duplicate the C11-C manifest or omit local evidence ledger/quarantine records.

## 3. Active environment and working style

- Windows project root: `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`.
- Godot: `4.7.1.stable.mono.official.a13da4feb` was confirmed in the latest successful runtime. The user installed it via WinGet. Use the valid existing `$godot` variable, `C11D_GODOT_EXECUTABLE`, or `Get-Command godot.exe`/`godot`; never hardcode `C:\Godot\Godot_v4.7.1-stable_win64_console.exe`.
- Keep PowerShell blocks simple, complete and pasteable from the repo root. Don't create a large generic launcher for a focused test batch. Do not assume PowerShell 7 `&&` syntax; operator uses Windows PowerShell 5.1.
- Python unittest writes summary/results to stderr. If direct invocation/redirection causes `NativeCommandError`, use `Start-Process` with explicit stdout/stderr log files and check actual `.ExitCode` plus expected markers. Do not declare PASS unless the process did run, exit code is 0 and the result/receipt markers are present. If it didn't run, call it NOT RUN/FAIL and repair the command rather than reporting a green placeholder.
- Avoid malformed PowerShell strings such as `"$Label: ..."`; use `${Label}:` or `-f`. Avoid partial try/catch/finally code. Keep overlay application and tests in separate commands/blocks; stop on first actual failure.
- Changes should be packaged as additive ZIP overlays (new/modified files only), with exact paths, hashes and precondition guards where appropriate. ZIP over `.patch`. Do not include full repo ZIPs or external `.ps1` scripts unless explicitly requested. Never hardcode a speculative Godot or Python path or make writes to Downloads as part of a test runner.
- Keep user updates direct, Spanish is preferred, no unnecessary status-only chat. User wants continuous progress, not repeated questions when evidence is already available.

## 4. Immutable C11-C source of truth

C11-C 2.19.12 stays frozen and immutable. Canonical package:
`ChallengeEngineV01_STATELESS_C11-C_2.19.12_FROZEN_20260930_175709.zip`

- ZIP SHA-256: `D85425CF18C5211C8497574F4FC66202D613EACC0EC14CD4E2FEF0B24F634A32`.
- Tree SHA-256: `2D39B7B923B42CDC6647A4D25493B75023CDD19CEE18214BBDE1FDD295B8F256`.
- `release/C11C_FREEZE_PACKAGE_MANIFEST.json` SHA-256: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

Never alter C11-C simulation, outcomes, timing, engine logic, pause/input behavior or its manifest to facilitate D work. `winning_frame` is the sole temporal anchor. `close_calls` is a count of episodes, not temporal data. Shared source frame is 540×960 (Header 0–144, Body 144–816, Footer 816–960); preserve `UnifiedSocialFrame`, `CoordinateMapper`, `PresentationFramer` semantics. Keep preview at source timebase; 720×1280 / 30 FPS is eventual delivery, not an early resampling step.

## 5. Product scope and canonical architecture

Supported scope currently contains 9 Challenges, 5 Visual Loop families / 27 grammars, and 4 Visual Drill types (`tracking`, `pursuit`, `saccade`, `peripheral_scan`) × tiers 1–5. Longform is not enabled; `LONGFORM_1080` is a delivery profile only. Current cross-type tested selectors: Challenge `parking_v2 / CHALLENGE_004`, and Visual Loop `c11c_geometric_waves_v1 / harmonic_membrane`.

D only extends the current five `c11c-suite` surfaces: `c11c-test`, `c11c-producer`, `c11c-catalog`, `c11c-config`, `c11c-maintenance`; don't create `c11d-control`. Keep GUI/CLI parity, canonical service reuse and fail-closed unknown selectors.

D9.8 owns the Universal Editorial Model: shared `title`, `subtitle`, `call_to_action`, `language`; Challenge-only `player_name`, `challenge_label`; inheritance `global → content_type → family → subtype → variant → production_override`. Editorial values cannot mutate telemetry, provenance, seed or simulation truth. D9.9 owns canonical universal requests/plans. D9.10 is a bridge/adapter planning envelope only and remains `PREPARE_ONLY`.

D10 preparation includes strict request-bound manifests/binding/materialization, candidate identity and I/O contracts, renderer-neutral frame/region program, editorial routing/visibility review, coordinates/composition/sample selection, temporal alignment/timebase and audio/music policy integration. Read existing checkpoints/source before adding a new path; don't duplicate a canonical binder or GUI model. Proposal/integration in a unified review does not equal policy approval or renderer admission.

## 6. Latest verified checkpoint (2026-10-16 context)

The operator provided actual successful Windows console output for the run dated 2026-10-15:

1. `tools/c11d/d9/test_d_renderer_seed_domain_collision_audit.py`: **7 tests / OK**. Covers 23 pinned sources, scoped selectors, pre-Godot rejection of equal numeric seeds in tested forms, strict/non-admissible report schema, missing/invalid seed rejection, no Godot/artifact side effects, weakened policy fail-closed.
2. Real Godot 4.7.1 cross-type audit: **12/12 canonical receipts**, 12 runtime invocations, gameplay sensitivity 2/2, music orthogonality 2/2, repeats 6/6, source pins 18/18.

Godot executable in that run:
`C:\Users\vinxe\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine.Mono_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.1-stable_mono_win64\godot.exe`

Audit SHA-256: `94cef68056e7fd5876e64642746012e3ba9c8e8106b03a3d78dd609d8eea7053`. stdout SHA-256: `d2563c122dac6548f0fe1e4ced1d069b071ccd2ee50896a43cdf655b660a1594`. stderr SHA-256: `98f4a2c4df3c95b2b4c4472f2e0098b40d7268cdb7b6272e7762cd7511c2620f`. Evidence folder: `C:\Users\vinxe\AppData\Local\Temp\C11D_CROSS_TYPE_RECOVERY_20261015_184503`.

The runtime report intentionally states `seed_domains_complete_for_candidate_input=false`, scope is only those two selectors, and status is `PREPARATION_ONLY_CROSS_TYPE_SEED_DOMAIN_AUDIT_NOT_INPUT_ADMISSION`. Other grammars/challenges, default/automatic and arbitrary request semantics remain open; Visual Drill V2 coverage is separate. No renderer input, dispatcher, production, request/payload persistence, artifact or media was emitted. This is a real PASS within scope—not full renderer acceptance.

Collision overlay V2 was already applied successfully: `C11D_SEED_DOMAIN_COLLISION_REJECTION_AUDIT_OVERLAY_20261015_V2.zip`, SHA `b236f344708dd86d6f40745aa83ca3485feb897e85e6a5f9ffbcf9f33e40ff93`, 17/17 preconditions and final hashes; 17 paths (12 replacements, 5 additions). Do not reapply V2/V1. Frozen manifest hash unchanged.

## 7. Governance locks are binding

At start, preserve:

- `renderer=OFF`
- `media_created=false`
- `D4.8=BLOCKED`
- `release_authority=NONE`
- `baseline_approval=MISSING`
- `freeze_eligible=false`
- `D9.17=BLOCKED_NO_GO`
- `D9.10 adapter=PREPARE_ONLY`
- `D10=BLOCKED_FOR_PROMOTION`
- D9.14/D9.16 remain gated for required actual real-media/full acceptance.

Do not run render/media production until the policy and candidate-input prerequisites are formally complete and a distinct gate authorizes it. A passing preflight is allowed/expected to report BLOCKED. Never flip flags, bypass D4.8, suppress negative controls or manufacture approval evidence to produce green output.

## 8. Continue toward the first render with full-project awareness

### Step 0 — reconstruct active truth

Check the active checkout and source hashes, read the roadmap, milestones, `D_RENDERER_BASELINE_PREPARATION_PLAN_V1.md` and all relevant checkpoints. The latest available normalized ZIP is from Oct. 14 and is not the exact Windows state after Oct. 15 overlays. Don't extract it wholesale; don't infer local ledger absence from snapshot omissions.

### Step 1 — seed / identity domain completeness

Use the successful collision and cross-type audit as the baseline. Expand runtime/contract coverage beyond two selectors to the actually supported request space; handle Challenges, Loop grammars and Drill tiers according to their own canonical contracts. Explicitly close default/automatic seed and arbitrary-request cross-domain cases or keep them blocked where no valid policy exists. Ensure independent repeats, gameplay seed sensitivity, music orthogonality, source pins and fail-closed negatives.

### Step 2 — canonical dynamic binder and manifests

Extend the existing request→payload binder rather than create another. Validate selected identity and tier/variant, request-specific manifest/digest, source and policy lineage, exact selector coverage, schema, determinism and invalid/mismatch/source-drift negatives. The known Visual Drill authoring audit (20/20) previously said `dynamic_request_manifest=NOT_TESTED`; do not claim that gate is closed until the real binder and required Godot matrix pass.

### Step 3 — candidate I/O completeness

Use the ten-group candidate I/O gap audit and identity inventory. Inspect active report; older prep numbers (0 complete, 6 partial, 4 blocked; 54 source pins; 164 sources) may be stale for the exact active tree. Make no group complete without evidence. Keep strict versioned schemas, exact source pins, stable request identity, payload/materialization binding and lineage.

### Step 4 — shared policy closure

Review shared editorial routing/visibility, regions, coordinates, sample/composition, source timebase/temporal scheduling, Challenge winning-frame behavior, audio/music and family inheritance in Unified Content Review. Most are proposals/review cross-checks, not automatically approved for renderer consumption. Resolve explicit approvals before implementing the media consumer.

### Step 5 — renderer admission/first-render qualification

Specify a strict D-owned admission contract that consumes only fully bound canonical requests, pinned payloads and approved renderer-neutral presentation instructions. Keep renderer OFF during prep. After authorized prerequisites, run the smallest controlled first render for a supported selector, verify actual media existence/content, frame count/rate/timeline/coordinates/editorial/audio rules, repeatability and output containment, and preserve evidence hashes. This is a separate real-media acceptance gate—not a no-media harness.

### Step 6 — full suite, closure and cutover

Run all applicable focused contracts, adverse tests, dynamic Godot matrix, candidate I/O/identity audits, unified review, GUI/CLI parity, five-surface GUI E2E, D9.13 lifecycle, `tests\run_all.py`, frozen C11-C acceptance, D9.14, D9.15 ledger/evidence reconciliation, D9.16, baseline preflight and D9.17. Record the actual output from the current Windows checkout. Only after formal approval and eligibility may C11-D freeze/promote; then replace C11-C as the active baseline/Producer through an auditable cutover with hashes and rollback, never by editing C11-C.

## 9. Required operating discipline

- State what is a Windows operator PASS, what is isolated package/contract-only evidence, what is source inspection, and what remains untested.
- Never invent file contents/path/receipt hashes. Inspect unknown or modified files directly.
- Make only justified changes. Every increment needs a contract-level reason, source pins, focused tests, regression, evidence, checkpoint and next action.
- Don't ask the operator to repeat known paths, environment or results. If a test command fails, fix the real execution issue without growing a complex launcher; be transparent about whether the actual test ran.
- Keep all new documentation in dated additive artifacts until any mutable current-document replacement can be safely reconciled with active hashes.

## 10. Required first response in the new window

Confirm the key invariants and latest evidence in one short paragraph, then inspect the active package/files and state the full remaining sequence, not only the immediate test. Start making progress after inspection: identify the largest proven blocker from the existing contracts/audits and implement a bounded increment. Preserve the source-of-truth hierarchy and the final cutover goal throughout.
