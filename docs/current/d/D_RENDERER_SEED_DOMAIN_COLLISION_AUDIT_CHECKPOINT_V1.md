# CURRENT OPERATOR ACCEPTANCE UPDATE — 2026-10-16 (supersedes pending Windows-confirmation wording below)

**Active Windows result:** `SEED COLLISION REGRESSION: PASS`; 7/7 tests passed, `Ran 7 tests in 0.722s`, `OK`.

The accepted test includes 23 source pins, preservation of the frozen C11-C reference, both pinned selector types, rejection of 20 invalid/implicit request forms and four equal numeric gameplay/music collisions before Godot, strict non-admissibility reporting, no Godot invocation by the rejection runner, and fail-closed policy checks. This is an operator-confirmed regression result, not renderer input admission.

The bounded cross-type runtime audit also passed on the active Windows checkout: Godot `4.7.1.stable.mono.official.a13da4feb`, 12/12 canonical V1 receipts, 18/18 source pins, gameplay sensitivity 2/2, music-seed orthogonality 2/2 and independent repeats 6/6. Selector scope is only Challenge `parking_v2/CHALLENGE_004` and Visual Loop `c11c_geometric_waves_v1/harmonic_membrane`. Audit SHA `94cef68056e7fd5876e64642746012e3ba9c8e8106b03a3d78dd609d8eea7053`; stdout SHA `d2563c122dac6548f0fe1e4ced1d069b071ccd2ee50896a43cdf655b660a1594`; stderr SHA `98f4a2c4df3c95b2b4c4472f2e0098b40d7268cdb7b6272e7762cd7511c2620f`. Full evidence and limitations: `C11D_OPERATOR_EVIDENCE_20261016.md`.

The cross-type report explicitly retains `seed_domains_complete_for_candidate_input=false`; automatic/default/arbitrary request coverage and selectors beyond the two representatives remain open. The last candidate I/O assessment is still 0/10 complete, 6 partial and 4 blocked. Renderer OFF; no renderer input/dispatch/media; D4.8 BLOCKED; release authority NONE; baseline approval missing; D9.14/D9.16 blocked; D9.17 NO-GO; D10 blocked.

The original 2026-10-15 content below is preserved as historical context, but any prior “active Windows confirmation pending” statement for this bounded rejection/cross-type result is superseded by the operator evidence above.

---

# Seed-domain explicitness and collision rejection — Checkpoint V1

**Date:** 2026-10-15  
**State:** `PREPARATION_TREE_PASS_ACTIVE_WINDOWS_CONFIRMATION_REQUIRED`  
**Authority:** Read-only preflight rejection audit. This checkpoint is not request admission, renderer-baseline approval, freeze, production, or render authorization.

## Gate objective

The preceding Visual Drill seed-domain audit is operator-reported PASS for 20 canonical type/tier selectors. The bounded cross-type runtime audit is also operator-reported PASS for Challenge `parking_v2/CHALLENGE_004` and Visual Loop `c11c_geometric_waves_v1/harmonic_membrane`: `selectors=2`, `gameplay_seed_sensitivity=2/2`, `music_seed_orthogonality=2/2`, `independent_repeats=6/6`, `source_pins=18/18`, `runtime_invocations=12`. The supplied PowerShell wrapper failed to retain a valid runtime log (the file was absent when hashing was attempted); its exact runtime evidence digest is therefore **not available** and is not fabricated. This evidence-capture defect is distinct from the user's reported test result and must be repaired for future runtime gates.

This gate closes only the next narrow question: does the canonical request planner reject implicit/invalid seed inputs and equal-valued gameplay/music seeds before any Godot invocation? The D9.10 adapter deliberately rejects equal numeric values across the two semantic domains (`Gameplay and music seed values must remain isolated`). The test therefore verifies rejection, not acceptance, of a collision.

## Source-bound policy

- Contract: `definitions/c11d/production/D_RENDERER_SEED_DOMAIN_COLLISION_AUDIT_V1.json`.
- Strict report schema: `definitions/c11d/production/D_RENDERER_SEED_DOMAIN_COLLISION_AUDIT_SCHEMA_V1.json` (Draft 2020-12).
- Read-only runner: `tools/c11d/d9/d_renderer_seed_domain_collision_audit.py`.
- Focused tests: `tools/c11d/d9/test_d_renderer_seed_domain_collision_audit.py`.
- Source pins: **23/23**; C11-C freeze manifest checked against `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- Preparation-tree result: **7/7 unit tests PASS**; **20/20** invalid/implicit seed forms rejected across the two pinned selector types; **4/4** equal-seed collision attempts rejected before Godot; `runtime_invocations=0` by design.
- The CLI prints a summary and then, if `--full-report` is used, JSON; use separate stdout/stderr capture files instead of parsing the combined console stream as pure JSON.

## Interpretation and remaining scope

The 20 negative cases exercise 10 invalid/implicit request forms per selector: missing, null, string, boolean, zero and out-of-range gameplay seed; missing and null music seed; automatic seed mode; and `master_seed` alias. The four collision cases pair equal numeric values `12345` and `840001` across both selectors. All must fail in canonical request planning before Godot.

This does not prove automatic seed generation (which remains disabled), master-seed support (not adopted), arbitrary numeric-domain combinations, all Challenge variants, all Visual Loop grammars, or complete seed-domain behavior for candidate input. Equal numeric values across domains remain prohibited. Candidate input admission remains false.

## Next safe increment

Confirm this new static gate on the active Windows checkout. Then expand canonical Challenge selectors and Visual Loop grammars incrementally using the same binder, including explicit rejection cases, and preserve full logs from any future runtime test with the corrected PowerShell capture pattern. Policy approvals for editorial windows/visibility, regions/coordinates, delivery timebase/timeline and audio/music remain separate prerequisites.

## PowerShell execution and evidence-capture guardrails

1. Paste complete balanced `function`/`try`/`catch` blocks in one go. Do not run a `finally` token as a separate console command; avoid `finally` in operator-facing snippets when cleanup can be expressed in the success and failure branches.
2. Resolve Godot from an explicitly supplied existing path or from `Get-Command`/known executables. Execute `--version` with stdout/stderr redirected to files, check the exit code and non-empty version text, and require `4.7.1` before using it.
3. For Python or Godot run logs, redirect stdout and stderr directly to distinct files (`1> $stdoutPath 2> $stderrPath`) instead of piping native stderr through `Tee-Object` under `$ErrorActionPreference='Stop'`. Capture `$LASTEXITCODE` immediately after the process, confirm the files exist, combine/hash them only after that, and validate the PASS summary before printing an acceptance line.
4. Never continue to hash a nonexistent log, never turn an output-capture exception into a presumed test failure or pass, and never print PASS unconditionally after an earlier failed guard.

## Governance locks

`renderer=OFF`; `media_created=false`; `D4.8=BLOCKED`; `release_authority=NONE`; `baseline_approval=MISSING`; `freeze_eligible=false`; D9.10=`PREPARE_ONLY`; D9.14/D9.16 blocked; D9.17=`BLOCKED_NO_GO`; D10 blocked. The audit creates no renderer input, media, receipt, or persistent report. The immutable C11-C manifest is not modified.
