# C11-D final closeout handover master prompt V24 — 2026-10-26

## Mission

Close C11-D only with evidence-backed, separately governed gates so a formally approved and frozen C11-D baseline can eventually replace the immutable C11-C production baseline. Do not optimize for a green console at the expense of provenance, source pins, determinism or governance.

## Source-of-truth order

1. Active Windows checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS` for current execution results.
2. `docs/current/d/C11D_FULL_CONTEXT_CONTINUITY_CHECKPOINT_20261026_V24.md` for state.
3. `docs/current/d/C11D_SOURCE_SNAPSHOT_RECONCILIATION_REPORT_20261026_V1.md` for ZIP and historical/current-source reconciliation.
4. `docs/current/d/C11D_V2B_ALLOWLISTED_COORDINATE_SOURCE_COMPOSITION_RUNTIME_REVIEW_20261026_V1.md` and its V2 evidence receipt/schema/validator.
5. Existing contracts, pin lists, D4/D9 gate definitions and dated predecessor checkpoints for their declared scope.
6. `AGENTS.md` and `.continue/rules/CONTINUE.md` for execution controls.

Do not extract or copy the snapshot ZIP over the working checkout. Do not assume a ZIP or old checkpoint is the execution truth. If a hash differs, stop and reconcile; do not weaken the test or silently refresh a pin.

## Current evidence

- Reference ZIP `ChallengeEngineV01_STATELESS_C11-D_20261026_013616.zip` SHA `3e48ee2d815593137f5863139e05c1aa04eb40b4a58ddfb3bed4507125c96874`, 8,001,498 bytes, 3,378 entries, CRC scan clean.
- Frozen C11-C manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- Implementation design static receipt SHA `9148ad3dfc21857d7decf5885a3fb0e10a839234ba7672040cfdfa86b57c7bd2`, 235/235.
- Runtime static V1 `113/113`, stdout `ca63239a81d23fd3bef046db02c67d7565aa4b24aefef4c1b849af71d1ecef8e`, empty stderr `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- Runtime static V2 `115/115`, stdout `bbf030cb4aa8319d007eae259a7dac52294a29fc9cddd1d242b09306b25548df`, empty stderr `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- Source-composition static `132/132`, stdout `74aad0a3ef62052e211932328d0a7d780c00ea1bb1bc1c118c2ff01a4e30a84f`, empty stderr `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- Godot `4.7.1.stable.mono.official.a13da4feb`, exit 0; four source candidates and 1,680 source frames / 1,680 marker frames; stdout `b5e1465894a9d5ad5a26715f10459bf578809d4a3fadce7fc030b4964aa2c3bb`, empty stderr `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

The 26-Oct evidence record is `CAPTURED_OPERATOR_RUNTIME_PASS_PENDING_FORMAL_REVIEW`, intentionally separate from the pre-run composition contract. V1 source-composition receipt SHA `a4684fdb7b3ea4b85f68b561d9aaa64981517f65530ba8a8787f820eb5e3960f` and its decision remain immutable; those artifacts bind old contract/harness/static-suite hashes. The current hashes are pinned by V2, not grafted into the old receipt.

## First task when resuming

Before any validation or repository change, verify that the active checkout `release/C11C_FREEZE_PACKAGE_MANIFEST.json` hashes to `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` and has `796318` bytes. The uploaded ZIP copy does not: it hashes to `f6b2fc6ce36973eb620738c8446d529d98da0fb79892132cf4708e6f453051b5` and has `1070256` bytes, while its own self-entry declares the canonical values. Never restore or replace the frozen manifest from the ZIP. If the active checkout check fails, stop and reconcile provenance. Only after it passes, run the current evidence validator against the exact runtime temp directory:

```powershell
$Repo = "C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS"
$EvidenceDir = Join-Path $env:TEMP "C11DCOORDCOMPOSITIONRUNTIME_79683278984b40d7b4fae0209ec4eee2"
$Python = "C:\Users\vinxe\AppData\Local\Programs\Python\Python313\python.exe"
$Validator = Join-Path $Repo "tools/c11d/d9/test_d_renderer_challenge_visual_payload_v2b_source_composition_runtime_evidence_v2.py"
$ValidatorOut = Join-Path $EvidenceDir "receipt_validator_stdout.txt"
$ValidatorErr = Join-Path $EvidenceDir "receipt_validator_stderr.txt"
$Process = Start-Process -FilePath $Python -ArgumentList @($Validator, $Repo, $EvidenceDir) -Wait -PassThru -NoNewWindow -RedirectStandardOutput $ValidatorOut -RedirectStandardError $ValidatorErr
if (Test-Path -LiteralPath $ValidatorOut) { Get-Content -LiteralPath $ValidatorOut }
if (Test-Path -LiteralPath $ValidatorErr) { Get-Content -LiteralPath $ValidatorErr }
Write-Host ("EVIDENCE_VALIDATOR_EXIT_CODE=" + $Process.ExitCode)
if ($Process.ExitCode -ne 0) { throw "Evidence validation failed; stop and inspect the first failing pin or evidence marker." }
if (-not (Select-String -LiteralPath $ValidatorOut -SimpleMatch "C11D_V2B_SOURCE_COMPOSITION_RUNTIME_EVIDENCE_VALIDATION_STATUS=PASS_RECEIPT_AND_CURRENT_SOURCE_PINS" -Quiet)) { throw "Required validation PASS marker missing; stop." }
```

Expect `C11D_V2B_SOURCE_COMPOSITION_RUNTIME_EVIDENCE_VALIDATION_STATUS=PASS_RECEIPT_AND_CURRENT_SOURCE_PINS`. That gate checks the temp stdout/stderr/summary, the current contract still in its pending pre-run state, all 81 parent source pins and 6 runtime-input pins declared by the contract, current composition/runtime source hashes, historic V1 evidence hashes and all governance locks. A failure must be investigated; no fallback to a permissive validation is allowed.

## Required next process after validator PASS

1. Independently inspect the source V2 receipt, its SHA, current-source lineage and captured operator output.
2. Record the review as a distinct, versioned operator decision artifact. Leave V1 historical receipt/decision untouched and do not update the current contract's pre-run status merely to make it look accepted.
3. Only after that review, decide whether to draft a separate *proposal* for a future non-production integration gate. The current task does not authorize that proposal implicitly, does not write a production call site and must not connect this consumer to any renderer or adapter.

## Exact scope of the PASS

This is an in-memory source-composition test over exactly `CHALLENGE_003`, `CHALLENGE_005`, `CHALLENGE_006` and `CHALLENGE_007`. Each contributes 420 source frames and 420 closed logical marker frames. The review-only consumer performs one allowlisted `Dictionary.get` per source frame. The harness reads custom data zero times; raw values are not logged. No renderer invocation, production calls, Resource/Node creation, payload materialization or media output occurs. It demonstrates neither visual pixel output nor the final 720×1280/30 FPS video delivery.

## Immutable production authority

C11-C 2.19.12 remains authoritative. The frozen manifest must remain `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. Do not change C11-C implementation, canonical seed V1, simulation truth, RNG ownership, `SimulationResult`, frozen geometry or source `winning_frame`. `winning_frame` is the only temporal anchor; `close_calls` is only an episode count.

The following lock values are hard invariants:

- `renderer=OFF`; `media_created=false`; `payload_materialized=false`.
- `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`.
- `automatic_seed_generation=false`; `master_seed=NOT_ADOPTED`.
- `approved_bindings=0`; `approved_custom_data_bindings=0`; `approved_renderer_projection_bindings=0`.
- `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`.
- `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`.

## Full closeout dependencies (do not skip)

After current receipt review, track independently and against the latest contracts:

1. Proposed integration contract and negative tests, if review authorizes preparing them; no production dispatch by default.
2. Fresh candidate I/O gap audit and exact request-to-payload identity inventory from the active checkout.
3. Binding review and explicit source-field-to-region/visibility/timebase/coordinate/sample/audio-policy decisions, each bound to exact proposal hashes. Cross-reference consistency is not an approval.
4. Seed-domain completeness, gameplay visual sensitivity and music-seed orthogonality; no automatic seed or `master_seed`.
5. Resolve the 11-second declared total vs 12-second phase sum for `CHALLENGE_008/009` under explicit shared temporal authority; do not normalize the data unilaterally.
6. D-owned renderer candidate schemas/provenance, deterministic tests, negative tests and identity pins.
7. Separate reviewed renderer-baseline approval and independent D4.8 authorization before any real render/media execution.
8. Only after authorization: D9.14 real-media certification, D9.16 full acceptance, D9.17 closure adjudication and D10 baseline acceptance/freeze/promotion.
9. Cut over C11-C only after formal C11-D acceptance, approval and freeze, preserving the frozen C11-C package as historical baseline.

## Windows execution protocol

PowerShell 5.1; one complete block wrapped in `& { ... }`; no `&&`, no `Read-Host`, no PS7-only syntax. Capture native stdout and stderr separately through `Start-Process -Wait -PassThru` and inspect `ExitCode`. Test and apply must be separate blocks. Add new versioned records without overwriting old ones. Any replacement requires exact pre-hash, backup and post-hash check. Stop on first error and never print success after a failure.
