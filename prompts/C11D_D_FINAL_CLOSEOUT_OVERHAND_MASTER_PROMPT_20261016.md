# OVERHAND / MASTER CONTINUITY PROMPT — ChallengeEngine C11-D final closeout

**Current reference date:** 2026-10-16. **Active repository:** `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`.

This document carries project intent, current verified evidence, architecture and execution rules into a new context. When conflicting historical prompt text is encountered, use the newest source-pinned contracts/checkpoints and active operator evidence; do not let a historical README grant authority that current governance denies.

## 1. Role and objective

Act as a precise engineering partner. Continue C11-D toward a controlled, deterministic first D-only candidate render and final branch closure, then eventual safe replacement of C11-C by D only after explicit approval, freeze and promotion. Do not equate passing a subtest with a closed phase. Each meaningful increment must leave an accurate source-pinned checkpoint and additive overlay.

Long-term product intention: a renderer-agnostic production system usable from the existing GUI and CLI. The operator should be able to choose content type/family/subfamily or tier and edit all on-video text. Shared editorial and presentation behavior is the default across Challenges, Visual Loops and Visual Drills; exceptions are explicit and family-scoped, not implicit forked implementations. GUI and CLI must use the same canonical D contracts and deterministic request binding.

## 2. Immutable reference and architectural constraints

Frozen C11-C source: `ChallengeEngineV01_STATELESS_C11-C_2.19.12_FROZEN_20260930_175709.zip`.
Frozen manifest path: `release/C11C_FREEZE_PACKAGE_MANIFEST.json`.
Frozen manifest SHA-256: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

C11-C 2.19.12 is immutable. Do not modify its simulation logic, RNG, `SimulationResult`, `winning_frame`, `close_calls`, frozen geometry or manifest. `winning_frame` is the sole temporal anchor; `close_calls` is an episode count, not a timing input. The D layer may prepare and bind outputs but must not change simulation truth.

The C11-D architecture remains renderer-agnostic during preparation. Do not turn the D9.10 adapter into a dispatcher. `D9.10=PREPARE_ONLY`; renderer is OFF; candidate renderer input is not admitted; no dispatch, no media, D4.8 BLOCKED, `release_authority=NONE`; baseline approval is missing and freeze eligibility is false. D9.14 and D9.16 remain blocked; D9.17 remains `BLOCKED_NO_GO`; D10 remains blocked. These conditions change only through explicit canonical evidence and authority, never by a script or self-authored report.

Do not add a parallel `c11d-control` surface. Existing GUI/suite surfaces are `c11c-test`, `c11c-producer`, `c11c-catalog`, `c11c-config`, and `c11c-maintenance`. Future GUI changes should extend the current Producer and shared production context rather than duplicate it.

## 3. Latest actual operator evidence

### Seed collision rejection

Active Windows regression returned 7/7 tests and `OK`. It verifies invalid/implicit seed rejection and equal numeric gameplay/music seed collision rejection before invoking Godot, strict report schema/non-admissibility and that this rejection runner creates no artifacts.

### Cross-type runtime

The operator confirmed a real Godot 4.7.1 runtime audit with 12/12 independent canonical V1 receipts. Version: `4.7.1.stable.mono.official.a13da4feb`. Last verified local path:

`C:\Users\vinxe\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine.Mono_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.1-stable_mono_win64\godot.exe`

Summary: two selectors, gameplay sensitivity 2/2, music orthogonality 2/2, independent repeat checks 6/6, source pins 18/18, runtime invocations 12. Audit internal SHA-256 `94cef68056e7fd5876e64642746012e3ba9c8e8106b03a3d78dd609d8eea7053`; captured stdout SHA-256 `d2563c122dac6548f0fe1e4ced1d069b071ccd2ee50896a43cdf655b660a1594`; captured stderr SHA-256 `98f4a2c4df3c95b2b4c4472f2e0098b40d7268cdb7b6272e7762cd7511c2620f`. Operator evidence directory: `%TEMP%\C11D_CROSS_TYPE_RECOVERY_20261015_184503`.

Exact selector coverage is limited to Challenge `parking_v2 / CHALLENGE_004` and Visual Loop `c11c_geometric_waves_v1 / harmonic_membrane`. The report keeps `seed_domains_complete_for_candidate_input=false`; do not expand its claims. It emitted no renderer-native input, did not dispatch/activate a renderer, persisted no request, wrote no payload/receipt files and created no media. This output is authoritative evidence for that bounded experiment, not for general input admissibility.

Separate Visual Drill seed coverage remains its own operator-confirmed 20-selector / 120-invocation matrix. It is not a replacement for completing Challenge/Loop selector coverage.

## 4. Current technical state and immediate work

The candidate I/O assessment last reports 10 groups: zero complete, six partial (`content_identity`, `source_lineage`, `payload_instance`, `seed_domains`, `editorial`, `delivery`) and four blocked (`presentation`, `timeline`, `audio`, `authorization`). The source-pinned identity inventory tracks 164 source files. Reconcile these source pins to the real active checkout before claiming a changed count.

First establish whether the separately prepared `C11D_VISUAL_LOOP_GEOMETRIC_GRAMMAR_MATRIX_V2_OVERLAY_20261016.zip` has already been applied. SHA-256: `b97572705a77c1dc2f0a2e6e37d820037448fee44e59cdd042d85a71a24608ac`. Its preparation-tree tests reportedly passed 11/11; the actual Godot runtime was not run in the preparation environment. It maps five C11-C geometric grammar identifiers across four seeds but does not admit those four non-harmonic grammars through canonical D9.9/D9.10 binding. Do not silently assume it's in the active checkout or report it as runtime-accepted. If applied, run and validate its real runtime; if unapplied, consider applying only after its own preconditions and addition-only path checks pass.

Then follow `docs/current/d/C11D_RENDERER_CLOSEOUT_GATE_MAP_20261016.md`:

1. Complete the deterministic seed-domain matrix for every *supported/admitted* canonical selector, including explicit negative/default behavior, while preserving fail-closed collision policy.
2. Close content identity, source lineage and selector-bound payload identity with canonical D bindings and independent Godot runtime receipts where required.
3. Obtain actual policy decisions for editorial visibility/windows, presentation regions/coordinates, delivery timebase/timeline and audio/music. Proposals stay unapproved until explicitly approved.
4. Prove approved editorial text is actually consumed by payload/presentation (last known review says 0/14 visual editorial sidecar values consumed) and resolve all candidate I/O groups rather than describing open groups as green.
5. Implement and independently review a renderer-agnostic D candidate behind the authorized boundary. Do not instantiate/dispatch from D9.10 or alter C11-C.
6. Only after prerequisite review, obtain explicit D4.8/test-run authorization before any minimal isolated D-only candidate render. Capture exit code, logs, hashes, output existence, deterministic repeats and visual/audio QA. Such a render is qualification evidence, not release.
7. Complete D9.14, D9.16, D9.17 and D10 closure in canonical dependency order, obtain formal baseline approval/freeze, and get explicit promotion/cutover acceptance before D replaces C11-C as authority.

## 5. PowerShell/test-run rules — mandatory

Read `docs/current/d/C11D_POWERSHELL_EXECUTION_POLICY_20261016.md`.

- Stay in repository root. Do not re-extract a full repo ZIP over the live checkout.
- Use small additive overlays with exact precondition/after-hash guards and frozen manifest verification.
- Don't invent a Godot path. The path above is the last confirmed path on the current machine; if it no longer exists, stop and resolve the environment using project-supported PATH discovery. Never default to `C:\Godot\Godot_v4.7.1-stable_win64_console.exe`.
- Discover Python from `Get-Command python.exe`.
- In PowerShell 5.1, prefer `Start-Process` with separate stdout/stderr files for Python unittest commands whose output to stderr can trigger `NativeCommandError`. Capture actual `.ExitCode` and validate files, markers, test count/version/pins/receipt count before PASS.
- Keep apply and tests separate. Stop on first failed condition. Don't use a brittle generic runner or complicated launcher framework when a direct block suffices.
- Never output a PASS line unconditionally; do not hash a missing file. Keep report audit SHA separate from stdout/stderr hashes.

## 6. Documentation/overlay discipline

For every new context, verify which current artifacts are in the active checkout; don't rely on reconstructed or preparation trees as though they were Windows runtime. Distinguish: static test; mocked subprocess test; preparation-tree real probe; active Windows real runtime; operator-reported result; formally accepted gate. Quote the correct category.

For each meaningful phase, add/update a concise checkpoint, current handover/start prompt, and roadmap next action. ZIP should contain only new or changed files. Include a manifest, exact before/after SHA values, frozen-manifest precondition, target-absence checks for additions, a human-readable README and an archive SHA-256 sidecar. Avoid packaging a whole repo or changing unrelated paths.

## 7. Definition of done for eventual C11-D replacement

D is not done until: all candidate input groups needed for the supported catalogue close; seed domains and identity/lineage/payload are deterministic and complete; editorial/presentation/timebase/audio decisions are approved and implemented with end-to-end evidence; a D-only candidate render passes authorized reproducibility and visual/audio/media QA; D9.14 production qualification and D9.16 full acceptance pass; D9.17 closure is explicitly adjudicated; D10 is reconciled; the renderer baseline is formally approved/frozen; and cutover is explicitly accepted. Until then, C11-C remains the immutable authoritative reference and producer baseline.
