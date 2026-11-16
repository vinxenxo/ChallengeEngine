# C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261116_V34 — authoritative update

## V34 addendum — Saccade family one-shot runner and ADD_ONLY overlay

This version supplements V33. V23/V27/V28/V29/V30/V31/V33 material remains historical and binding where not superseded.

### PowerShell 5.1 syntax and invocation

- Target Windows PowerShell 5.1. Parse every installer and runner with `[System.Management.Automation.Language.Parser]::ParseFile` before invocation; emit a PASS only in the successful branch. Never place `else` in a separate interactive submission after its `if` block.
- Quote variable interpolation before punctuation: use `${Phase}:` rather than `$Phase:`. Do not rely on a later runtime failure to discover parser errors.
- Native child output must be captured with `Start-Process -Wait -PassThru -RedirectStandardOutput ... -RedirectStandardError ...`; read logs only after the process exits and check the actual `ExitCode`. Never merge native stderr into a PowerShell pipeline under `$ErrorActionPreference='Stop'` to run unittest.
- PowerShell source shipped in packages must be ASCII, BOM-free, AST parsed, and fully covered by package manifest hashes.

### ADD_ONLY installer discipline

- Validate outer ZIP SHA sidecar, archive member paths (reject absolute paths, traversal, backslashes, drive prefixes, duplicate names), exact member inventory, embedded manifest sidecar, installer identity, file byte counts and SHA-256 before any write to the checkout.
- Validate all destination parent directories already exist and every ADD destination is absent before starting a transaction. Do not create destination directories as part of the write loop.
- Stage test sources and canonical fixtures in the exact project-relative structure used by the tests. Run `py_compile` and the exact declared `unittest` count from the staged tree before any checkout write.
- Verify source pins and the frozen C11-C manifest before the transaction and immediately at its boundary. Persist the transaction journal before the first add. Use the atomic create helper for ADD; never a replace primitive. Recheck destination absence immediately before each create.
- Roll back only files that were successfully added by this transaction and still match the exact package postimage. Never delete a concurrent/conflicting file. Preserve all evidence on any failure; do not automatically rerun.

### Family runner and batch execution

- The runner defaults to PREPARE_ONLY. Only a separate explicit `-Execute` may pass `--execute` to the Python coordinator. The installer always invokes the runner without `-Execute`.
- A batch is sequential, fail-fast and one-shot. Generate a new BatchId for a new attempt. Once ATTEMPT_RESERVED/EXECUTION_AUTHORIZED_ONCE is persisted, any child, timeout, receipt, source pin, or media audit failure consumes that BatchId. Preserve lock, progress, requests, outputs, logs and receipts; never retry with the same ID.
- Never copy a result from another family to satisfy a tier. A request-shape template is not qualification evidence. Every Saccade tier 1–5 is independently executed and reviewed.
- Child media verification must bind actual files to receipt hashes; validate FFprobe/timebase, A/C video identity, A/B same-seed audio identity, C changed-seed difference, family profile and the pre/mid/post 91-source physical inventory.
- Keep `GIT_CHECKS=SKIPPED`, commits operator-managed, production dispatch false, release authority NONE. Do not introduce Git bookkeeping.

---

## Superseded historical content retained for traceability

# C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261115_V33 — authoritative update

## V33 addendum — Pursuit V5.3 hardened installer rules

This release requires ZIP member path validation before extraction, package-relative helper resolution under `payload\support`, explicit dot-source and helper export checks, fixture staging to both `tests\fixtures` and `definitions`, four verified backup records before `transaction_started=true`, and destination rechecks at the transaction boundary and immediately before each file operation. See the final V5.3 hardening section below. The V31 and V32 material remains historical guidance.

## V31 addendum — Recovery of an ADD_ONLY transaction after all writes

When an ADD_ONLY installer reports `committed_count == operation_count` but fails in a post-commit verification, do not rerun it and do not delete destinations. Bind recovery to the exact failed RUN_ID, package ZIP SHA, manifest SHA, journal and failure receipt. Before any further mutation, independently verify every journal destination against its package manifest payload hash/size and verify every protected source pin. Preserve the failed journal unchanged; write a separate recovery audit receipt.

For a frozen manifest that is already a member of the protected source-pin set, compute its SHA exactly once during the post-pin pass, store the path→digest result, and compare that captured value with the expected frozen digest and byte size. Do not perform a redundant second read/hash after the post-pin loop. If it mismatches, write both expected and actual digest before failing.

A runner's hard-coded driver SHA must equal the SHA of the exact coordinator bytes delivered by the same package. Contract tests must compute the coordinator's actual staged bytes and compare them to the runner declaration; merely searching for the same hard-coded digest in both test and runner is insufficient.

For Python `unittest` or nested PowerShell tests that write successful progress to stderr, use `Start-Process -Wait -PassThru` with separate stdout/stderr paths. Capture exit code immediately after wait, then read logs; non-empty stderr alone is not a failure. Preserve logs and staging on failure.

For any recovery after a partially completed ADD_ONLY transaction, use exact-run receipts and journal, durable backups for subsequent REPLACE operations, source pins pre/post, PS 5.1 AST, atomic I/O 7/7 and separate prepare-only authorization. Never use Git checks; operator commits remain managed externally.

---

## V3 PURSUIT RECOVERY AUTHORITY — 2026-11-15

This update supersedes any V2 install-pending or next-action language below. The active project remains at E4C 5/20: tracking 5/5 operator accepted; pursuit, saccade and peripheral_scan each 0/5. C11-C 2.19.12 remains the sole production authority; frozen manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; E1 `PREPARE_ONLY`; family adapter `NOT_CONNECTED_E1`; `PRODUCTION_DISPATCH=FALSE`; `RELEASE_AUTHORITY=NONE`; `GIT_CHECKS=SKIPPED`; commits operator-managed.

Pursuit Overlay V2 failure `C11E_E4C_PURSUIT_BATCH_OVERLAY_V2_20261115T130255Z_b5f15417` is a partial ADD_ONLY transaction with all 19 operations marked `ADD_COMMITTED`, followed by `FROZEN_C11C_MANIFEST_POST_FAIL`. Preserve its failure receipt, in-progress journal, preflight, logs and stage. Never rerun V2, do not roll back or delete the 19 installed files. The installer completed its 34-pin post-check loop without recording a SOURCE_PIN_POST_FAIL, then failed on a separate second read of the frozen manifest. The failure receipt did not record the digest observed by that second read, so the supplied evidence cannot distinguish a transient second-read discrepancy from another read-path issue. Do not infer that C11-C was modified: the preflight and supplied repository snapshot both carry the frozen SHA and 796,318-byte size. V3 removes the uninstrumented second read, uses the captured frozen-manifest value from the 34-pin post-check as the authority, and persists every pre/post pin result and actual mismatch digest.

A second independent defect was found before launching the V2 runner: it pinned `c11e_e4c_pursuit_tier_batch.py` to `dcb2c035ff5aee83a673e30347617aed67c8b382bf85af68441153611964566b`, while the exact driver bytes in the same V2 package and package manifest are `7164a83c882116081cda720b37c47107e9145ad2b918b759470b06c5eb3d5522`. The V2 contract test repeated the stale value and therefore passed incorrectly. V3 pins the runner to the exact packaged driver and makes the test compute the staged driver's SHA and compare it with the runner declaration.

V3 is a recovery transaction, not a fresh installation: it audits the exact V2 run and its 19 existing destinations; verifies the original V2 package identity and 34 current source pins (the C11-C manifest is captured once); then performs exactly two pinned replacements (runner + runner test) with independently verified backups and adds the new versioned documentation. It runs the existing pursuit coordinator only in default `PREPARE_ONLY`, with separate child stdout/stderr capture and no `-Execute`. It creates no media or production dispatch.

Do not claim Pursuit installed or prepared until V3's recovery receipt, 2/2 real backups, 17/17 postimages, 34/34 pins and `PASS_PREPARE_ONLY_NO_RENDER` are independently audited. Any V3 failure after transaction start is evidence-only and must not be rerun.

--- HISTORICAL CONTENT BELOW ---

# C11-E PowerShell Runner Style Guide — V30 (2026-11-15)

**Authority:** V30 extends V29 and preserves the complete V28/V29 safety rules. It adds the Pursuit native-stderr installer correction and durable failure-evidence contract. No earlier PowerShell 5.1 safety rule is relaxed.

## E4C family-isolated batch contract

The E4C selector matrix contains exactly four families and five tiers each. A batch coordinator must bind one declared family only; it must not be presented as a general matrix runner unless it explicitly validates and implements all family-specific data contracts.

The next batch after the accepted tracking 5/5 segment is pursuit/tier-1 through pursuit/tier-5. Its required family music profile is `ORGANIC_BLOOM`. Its native and D-owned family mechanics remain those already defined by C11-C; the batch may not introduce a new binder, producer, timeline, renderer, compositor, music engine, or E1 service.

### Pursuit request contract

- Select only `visual_drills / pursuit / tier-1..tier-5`.
- Set `mode=PRODUCTION`, `delivery_profile_id=REVIEW_720`, `audio_enabled=true`, `personalization_enabled=true`, `variation_index=0`.
- Retain gameplay seed `12345` and A/B music seed `840001` for this scoped qualification; the existing executor must derive the changed C seed. Never use gameplay seed as music seed.
- Use `ORGANIC_BLOOM` as the expected family profile; do not silently fall back to `FLOWING_VECTOR`.
- Editorial copy is family-specific and selector-bound: title `PERSECUCIÓN VISUAL · NIVEL N`, subtitle `Sigue la trayectoria del objetivo en movimiento`, CTA `Mantén el objetivo a la vista`.
- Keep each tier in its own request ID, product root and evidence root. The coordinator is orchestration only and must call the existing CLI facade and shared `c11e_e4c_drill_execution.py` entrypoint.

### Prepare/execute and acceptance gates

1. Default mode is `PREPARE_ONLY`. It verifies exact source pins, the C11-C frozen manifest, the accepted baseline request/receipt, Python 3.13/PySide6, the exact installed style guide and output collisions. It must not create an execution lock, one-shot authorization marker, media or output directory, nor invoke Godot/FFmpeg.
2. `-Execute` is a separate invocation and a single explicit authorization. The coordinator creates its lock and authorization marker with exclusive creation only after all non-mutating preflight gates pass. Any failure after the marker permanently consumes that BatchId.
3. Sequential execution is fail-fast. Preserve every request, stdout/stderr, partial output, failure receipt, lock and progress checkpoint. Never retry a consumed BatchId or clean evidence to make a new attempt appear fresh.
4. Every selector needs its own full receipt, exact file SHA verification, A/C video stream identity, A/B same-seed music identity, C changed-seed music distinction, FFprobe contract, 810 frames at 30fps / 27 seconds / 90-630-90 phases, 91 source pins pre/post, E1 GUI/CLI semantic parity and frozen C11-C manifest proof.
5. Machine PASS remains `PASS_TECHNICAL_PENDING_OPERATOR_A_V_REVIEW`. E4C acceptance requires both the full selector-specific technical receipt and explicit operator visual/audio approval. Family subtotal acceptance does not close E4C before 20/20.

### Runtime shutdown warning handling

Godot shutdown messages such as leaked `CanvasItem` RID or `ObjectDB instance` are not to be suppressed or silently discarded. Record the exact stderr text. They may be classified as non-blocking for a given selector only when the process exits successfully, capture stdout confirms the complete expected frame count, no `ERROR`/`SCRIPT ERROR` appears, and the complete qualification receipt and media/hash/FFprobe contracts pass. A repeated or newly escalated warning becomes an investigation item.

### Evidence package completeness

A selector-level evidence ZIP must include its four native/D receipts, E1 intent/validation, all final media and WAV assets, per-selector logs and source evidence. If the aggregate `BATCH_RESULT.json`, wrapper output or CLI summaries are outside the ZIP, state that limitation and bind the aggregate conclusion to the exact operator console result; do not claim the missing files were independently rehashed.

---

**V28 baseline and prior addenda follow unchanged for historical traceability.**

# C11-E PowerShell runner style guide — V28 baseline (heading corrected; 2026-11-15)

## E4C R6.3A field-scoped PRE_ROLL editorial contract incident

The R6.3A D visual consumer intentionally makes only `title` visible during `PRE_ROLL`; subtitle and call-to-action remain `GAME` only. The global `phase_visibility.PRE_ROLL` value is therefore `true` exactly when a non-empty family title exists. This does **not** mean all D editorial is visible in PRE_ROLL. `d_editorial_visible` remains false during PRE_ROLL for the body/editorial slot while the independent family-title bridge paints the family title in the reserved native title footprint.

The previous `c11e_e4c_drill_execution.require_visible_editorial` rejected every `PRE_ROLL=true` plan. That stale all-fields-hidden assertion contradicted the accepted R6.3A consumer and stopped the first tracking tier before toolchain preflight/native launcher. It must be replaced by a field-scoped contract check:

- `phase_visibility.PRE_ROLL == (non-empty title exists)`;
- `phase_visibility.GAME == true`; `END_CTA` and `DONE` are false;
- `field_phase_visibility.title == [PRE_ROLL, GAME]` only when title exists;
- subtitle and call-to-action each have `[GAME]` only, or `[]` when absent;
- no editorial field is visible during `END_CTA` or `DONE`;
- D PRE_ROLL title replacement must keep native body/footer pixel identity and `d_editorial_visible=false` for non-title editorial.

Do not resolve this conflict by clearing title/subtitle/CTA, disabling personalization, blanking the title, or reverting the accepted R6.3A visual consumer. The correct repair belongs to the existing D E4C executor's validation helper and tests. Do not modify C11-C, E1 service, GUI, CLI facade, the R6.3A consumer, the native phase binder, or media generators.

## Cross-layer regression obligation

Any D consumer phase-visibility change must be represented in the consumer contract tests **and** the existing E4C execution helper tests. The execution helper suite must accept the exact R6.3A V2 field-scoped plan; reject title visibility inconsistent with title presence; reject subtitle/CTA PRE_ROLL exposure; and keep END_CTA/DONE hidden. The tracking-batch source pin must pin the repaired executor postimage. A batch coordinator's synthetic receipt tests alone are not sufficient integration coverage.

## Fail-closed recovery rule

A batch that writes `EXECUTION_AUTHORIZED_ONCE.json` has consumed its BatchId. A child failure, even before the native launcher, permanently prohibits reuse of that BatchId. Preserve the lock, request, CLI logs, failure receipt and progress file. Any continuation gets a new BatchId only after the exact failed child and source contract have been diagnosed and corrected. Never print or infer a later PASS after a failed child; execute saved scripts with `-File`, and stop on the first nonzero exit.

## Required source and test gate for this remediation

The remediation installer pins the exact V1 preimages for the existing D E4C executor, its tests, the tracking batch coordinator, its tests and the PowerShell runner. Before the first checkout write it stages only the changed Python sources plus the read-only current CLI/GUI source text required by the tests; it runs `py_compile` and both focused stdlib test modules. It preserves exact replacement backups, adds all documentation/prompt versions without overwriting, verifies all replacement postimages and the full 30-source postimage pin set, and checks the frozen C11-C manifest identity.

---

# C11-E PowerShell runner style guide — V24 addendum (2026-11-15)

## E4C matrix-batch orchestration controls

These rules extend V23 and do not relax any prior rule.

1. **Batch coordinator is not a new executor.** It must invoke the current CLI facade (`--origin CLI --execute-drill-av`) and retain the existing D shared execution entrypoint. Never copy renderer, D compositor, E1 service, music generator, C11-C launcher or Producer logic into a matrix runner.
2. **One request and output namespace per selector.** Precompute unique request IDs and confirm all four `artifacts/production/c11e/<request_id>` paths are absent before starting. Store each canonical request, CLI result, stdout/stderr and row result in a distinct batch evidence directory. Never recycle a tier-1 ID/root.
3. **Sequential, fail-fast matrix execution.** Execute in declared order. On nonzero child exit, timeout, invalid receipt, media/FFprobe failure or source-pin drift, preserve current and prior evidence and stop. Do not auto-continue or auto-retry a partially started child.
4. **One-shot authorization.** Create the batch root, `ATTEMPT_RESERVED` lock and `EXECUTION_AUTHORIZED_ONCE` using exclusive creation only after every non-mutating preflight has passed. A failure after authorization forbids retry with the same batch ID. A continuation must have a new, separately reviewed ID and inspect all partial outputs first.
5. **Machine acceptance is not operator acceptance.** Batch result status must explicitly say `PASS_TECHNICAL_PENDING_OPERATOR_A_V_REVIEW`. Maintain a per-selector review state. Do not close E4C or increment accepted coverage from technical receipts alone.
6. **Source pin discipline.** Validate the frozen manifest, exact R6.3A source postimages, request template and accepted baseline receipt before the first row and after each successful row. Preserve the E1 91-pin pre/post equality proof produced by the executor. Never use Git/HEAD/status/branch checks.
7. **No output fabrication.** A/B same-seed music equality and C changed-seed distinction must be read from the full family music receipt and verified against files. Final A/C MP4s must be verified by FFprobe and elementary stream hashes. Do not infer a tier's timing or assets from a different tier.
8. **PowerShell child process contract.** Retain V23's `Start-Process -Wait -PassThru` / redirected log discipline, immediate exit-code assignment and after-exit log reads. The runner must self-parse through the PowerShell 5.1 AST API before launching the Python coordinator.
9. **Preparation mode.** Default launch is prepare-only: source pin/runtime/base-receipt/output-collision checks, with zero Godot, FFmpeg, renderer or media activity. Actual execution requires an explicit `-Execute` switch.
10. **Evidence is immutable.** A failed row's request, log, partial output and failure receipt remain in place. Do not clean, overwrite, or rename them to make a rerun appear fresh.

## V24 evidence/build requirement

Any future `.ps1` authoring must read this V24 file from the active checkout, not merely the V23 predecessor, and record the current exact path/version/SHA in build verification. V1's installer itself pins V23 as its pre-install prerequisite because V24 is one of its ADD_ONLY postimages.

---



# Previous style guide V23 — retained unchanged below

# C11-E PowerShell Runner Style Guide — V22 Addendum (2026-11-14)

## Mandatory pre-authoring checklist

Before authoring or revising any `.ps1`, read this complete guide from the active checkout and record its exact path/version/hash in the package build verification. This is a required build gate, not optional context. Re-read the latest file after every meaningful update. Do not assume an earlier model/session has complied.

## R6.3A incident rules — process output and idempotent recovery

1. **Never read redirected stdout/stderr while the child process is still running or may still own the file handle.** The R6.3A V54 driver called `[IO.File]::ReadAllText()` on `INSTALL.stdout.log` while its child still held the redirected handle. Windows raised a sharing violation after the installer had completed its transaction. Either use `System.Diagnostics.Process` with asynchronous `BeginOutputReadLine`/`BeginErrorReadLine`, or wait for process exit before reading redirected files. A temporary `IOException` must never be converted to empty output and then treated as successful completion; after exit, read the final streams and check the real process exit code.
2. **Process exit is authoritative.** Capture `$LASTEXITCODE` immediately after a native child command, before any other native command can overwrite it. Do not infer success from a final `Write-Host`, a non-empty log, or an outer wrapper's stage label. Require the exact child receipt and its schema/status/run ID.
3. **Do not rerun an installer because its outer orchestrator failed after the child transaction.** Inspect the exact run's `INSTALL_RECEIPT.json`, `TRANSACTION_JOURNAL.json`, postimages and backups first. If the receipt says installation PASS and the journal records `REPLACED_POSTIMAGE_VERIFIED`, resume at the independent audit for that same run ID. Preserve the original backup evidence.
4. **`SKIP_IDENTICAL_POSTIMAGE` is not a new REPLACE.** It has no new backup (`backup_path=null`). Never report 3/3 backups for a run that skipped all three replacements. `backup_count` must be computed from real non-null backup paths whose bytes hash to exact preimages. An independent auditor must reject a same-run backup claim that is not supported by that run's journal/files; use the original successful transaction as the audit target instead of fabricating a backup.
5. **One-shot means one saved script, not a long interactive paste.** Deliver a `.ps1` and run it using `powershell.exe -NoProfile -ExecutionPolicy Bypass -File <path>`. Do not paste multi-stage blocks into an interactive prompt: after a `throw`, separately pasted commands may still execute. The script must stop at the first failed gate and return nonzero.
6. **No success statements after failure.** A stage failure writes a failure receipt and exits nonzero. Do not continue to later commands, print a PASS marker, start a requalifier, or create a human-acceptance marker after failure.
7. **Exact package/run binding.** An audit invocation must bind the package SHA recorded in the install receipt to the exact run ID and its transaction journal. Never use a later idempotent run ID merely because it is newest.
8. **Preserve transaction evidence.** Do not delete logs, backups, temporary package roots or failed output directories while diagnosing. Any retry must use a new output ID; never recompose or remux an accepted output just to recover a review receipt.

## R6.3A-specific current lesson

The first install `C11E_E4C_V2_3_R6_3A_20261114T163406Z_fc8436fa` succeeded with three actual backups. Its outer driver failed while reading a locked stdout file. The second run `C11E_E4C_V2_3_R6_3A_20261114T163827Z_47eab402` skipped identical postimages and correctly created no backups, but its receipt incorrectly claimed 3/3. Audit the first run; do not reinstall. The package recovery script binds the exact first run and original package SHA.

---

# ADDENDUM — invariant numeric arguments across PowerShell locale — 2026-11-12

Never localize a decimal string when forwarding it to a typed PowerShell script parameter across a process boundary. For D→C11-C, use an ASCII invariant string only for a `[string]` wrapper parameter; parse using `CultureInfo.InvariantCulture`; pass the resulting typed `[double]` within the same PowerShell process; save the wrapper and hash in execution evidence. Regression must force `es-ES`, invoke a dummy launcher with the same typed parameter contract, and verify an invariant serialization of exactly `0.75`. Never edit the source-pinned C11-C launcher to hide a D-owned conversion defect.



## D99-GUI-85201B7B4FF7 — single-selector A/V pilot diagnosis — 2026-11-12

**Authoritative evidence:** `D99-GUI-85201B7B4FF7.zip` SHA-256 `0913179f9852b7b1f75c2a7e2f763a111bc8d807d08d20036a2891ae94661f56`; `D99-GUI-85201B7B4FF7-tests.zip` SHA-256 `16f0e199429deffb85025cd35d0cfd4fe2ec9fe237cf66482f6de6b14cd6ef23`.

The GUI's **Resolver + Plan** stage is successful, not a failure: E1 receipt is `PASS_E1_PREPARATION_ONLY`; GUI/CLI semantic parity is `PASS`; D9.10 bridge planning is `PASS_BRIDGE_PLANNING_ONLY`; D composition plan is valid with real GAME-visible editorial; the request is `visual_drills / tracking / tier-1`, gameplay seed `12345`, music seed `840001`, `REVIEW_720`. This remains deliberately plan-only at E1 and does not claim renderer or dispatch activation. The second GUI action, the shared D A/V executor, fails before the native C11-C producer starts.

Exact failure from `logs/c11c_drill_producer.log`: C11-C's `run_visual_drill_production.ps1` rejects `-SpeedMultiplier` because it receives `75000`, outside `[ValidateRange(0.1,3.0)]`. The pinned profile `profiles/difficulty/visual_drill_tracking.json` has tier 1 `speed_multiplier=0.75` (source SHA-256 `6de8812bd46904e122ecdd0eae22fb2979bd75399c34779248c6569e833c921e`). The adapter applied Python's host decimal separator and sent `0,75000`. On the operator's locale, Windows PowerShell 5.1 parameter binding split/coerced that comma decimal and delivered `75000`. This is a cross-locale numeric argument-boundary defect in the D adapter, not a defect in the pinned C11-C launcher or difficulty profile.

The failure occurs before a successful C11-C capture. There is no native MP4, no D frame composition, no FAMILY_MUSIC_V4 WAV generation, no mux, and no final FFprobe result in this run. The failure does not indicate an editorial, font, Qt, geometry, phase/timebase, music determinism, or A/V stream-equivalence defect. The first evidence bundle contains `RUNNING` and `FAILURE` receipts and the exact native producer log. The `-tests.zip` is a preparation/parity/contract receipt bundle; it does not show a second independent A/V failure. Do not infer additional failures from its intentionally plan-only receipts.

**V1.4 correction:** remove host-locale formatting entirely. Python emits an ASCII invariant string such as `0.75000` to a string-typed PowerShell wrapper. The wrapper parses it with `[System.Globalization.CultureInfo]::InvariantCulture`, sets the wrapper thread culture to invariant for the call, then invokes the existing pinned C11-C launcher with an already-typed `[double]$speed`. The native C11-C launcher remains byte-identical and receives `0.75`; C11-C stays silent via `-NoSound`. The wrapper is retained in the run logs and its hash/argument are written into the execution receipt. Regression tests cover invariant formatting, wrapper parse/type handoff, and absence of host-locale formatting. The V1.4 installer additionally executes this exact wrapper against a dummy parameter-compatible launcher while forcing `es-ES`, and requires the dummy to record `0.75` before any repository mutation.

The failed output root `artifacts/production/c11e/D99-GUI-85201B7B4FF7` is intentionally preserved. It must not be overwritten. The retry must use a **new unique request_id/output root** (generate a fresh GUI request and repeat Resolver + Plan); do not delete or recycle this failed evidence. After V1.4 installation PASS: audit its postimages/source pins, rerun the GUI plan stage with a fresh ID, then execute only `tracking/tier-1`. Continue only when native capture, D composition, FAMILY_MUSIC_V4 A/B/C, final A/C video/audio stream hashes, FFprobe, and human visual/listening review pass. CLI smoke/parity follows on the same shared adapter. Do not start the 20-selector A/V matrix until the single-selector result is accepted.

Governance is unchanged: E1 `PREPARE_ONLY`; `family_adapter.status=NOT_CONNECTED_E1`; `production_dispatch=false`; `release_authority=NONE`; no Git checks; commits operator-managed; C11-C frozen manifest SHA remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.


---

# ADDENDUM — E4C OVERLAY INSTALLER V1

The overlay installer uses Windows PowerShell 5.1, strict mode, ASCII-only source, exact SHA-256 source pins and no Git commands. It stages patched Python sources and stdlib-only contract tests under a short `%TEMP%` root, then performs AST parse, Python 3.13/PySide6 probe, py_compile, tests and an immediate pre-transaction recheck before the first repository mutation. It must not call pip or modify requirements/shared dependencies.

Transaction journaling is persisted before every mutation. REPLACE operations back up exact non-empty preimages; rollback is permitted only when the current destination matches the expected postimage and the backup matches the exact preimage. ADD operations are removed only when their current hash matches the package postimage. Unknown or changed states are never overwritten.

---

# C11-E PowerShell Runner Style Guide — V18 (2026-11-11)

## V8 current state — 2026-11-11

V7 failed closed in `STAGED_VALIDATION` before transaction. Its installer imported `QT_VERSION_STR` from `PySide6.QtCore`; the canonical PySide6 runtime does not export that symbol. This is an installer probe defect, not evidence that PySide6, Qt, QImage or QPainter is missing. The preceding imports of `PySide6.__version__` succeeded. `journal=[]`; `rollback=NOT_NEEDED`; no checkout write occurred.

V8 changes the probe to `from PySide6.QtCore import qVersion` and records `qVersion()` as the Qt runtime version. It requires Qt 6.x, alongside Python 3.13.x, existing PySide6 6.8–6.x, non-null RGB888 QImage and active QPainter. The official Qt for Python API lists `qVersion()` as a QtCore function. V8 does not install, upgrade or uninstall packages, invoke pip, edit requirements, or mutate the shared Python environment.

The consumer, its 35 Qt tests and the E1 service replacement are byte-identical to V7. No functional test result is inferred from the failed V7 runtime probe. V8 must still pass Windows PowerShell 5.1 AST, inventory/pins/destinations/staging, runtime probe, `py_compile` 3/3, all 35 Qt tests and immediate pre-transaction checks before any write. Do not repeat accepted A.3, binder V2, Godot V3, Loop22 or historical Drill authoring.

Governance remains unchanged: C11-C frozen manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; renderer OFF; dispatch/media/audio OFF; `release_authority=NONE`; operator manages commits; Git checks skipped.

### Qt version API rule
For PySide6 runtime reporting, import `qVersion` from `PySide6.QtCore` and call `qVersion()`. Do not import or reference `QT_VERSION_STR`; it is not a guaranteed exported PySide6 binding symbol. Validate returned Qt major version `6`. This probe must remain read-only and must not call pip or mutate shared dependencies.

---


## Current E4C Drill visual-consumer policy — Qt reuse, no dependency additions

- **No new Python dependency** is permitted for the D-owned Drill visual consumer. Reuse only the existing PySide6 dependency declared by the existing Producer; do not add a wheel, package, requirements file, lockfile or environment prerequisite.
- Do not introduce Pillow, PIL, RAQM, FreeType bindings, or another imaging/text dependency for this consumer. Do not run `pip`, `ensurepip`, package managers or dependency installers from the overlay installer, its setup instructions or its tests.
- Do not install, uninstall, upgrade, downgrade or otherwise mutate the shared Python environment as part of this phase. Do not modify either C11-C requirements file.
- Require the canonical explicit `-PythonExe` path and validate Python 3.13.x plus the existing Producer PySide6 `>=6.8,<7`, Qt version, `QGuiApplication`, RGB888 `QImage` creation and active `QPainter`.
- Use `QT_QPA_PLATFORM=offscreen` only as a temporary process-scoped value while launching staged Qt test subprocesses. Preserve and restore the exact prior process value on success and failure; never write user/machine environment settings.
- The Qt backend is a new renderer implementation. Require fresh active-Windows `py_compile` 3/3 and all 35 rewritten Qt tests before any checkout transaction. Pillow-suite results do not transfer.

## Historical dependency guidance — superseded

The earlier V14 generic exact-dependency-pin guidance and the interim V5 Pillow proposal are historical only. They are superseded for the E4C Drill visual consumer by this V16 no-new-dependency policy. Do not apply the former Pillow 12.3.0 / RAQM installation instructions, do not create `requirements-visual-consumer.txt`, and do not treat that abandoned proposal as current authority. The V5 shared-environment installation recommendation was explicitly rejected by the operator.

## PowerShell 5.1 / Unicode

1. `.ps1` source must be ASCII-only. PowerShell 5.1 may decode UTF-8 without BOM through the active ANSI code page.
2. Spanish/editorial strings belong in UTF-8 JSON or Python fixtures, not PS literals.
3. Compare Unicode codepoints and NFC against independent fixtures; reject mojibake (`Ã`) and U+FFFD.
4. GUI/CLI replay derives CLI input from saved GUI UTF-8 evidence; change only provenance/request identity.

## Source authority / add-only installation

- Active checkout only; ZIPs are evidence/read-only. Never overlay snapshots onto checkout.
- Verify SHA-256 pins and frozen C11-C manifest. Never run Git or inspect HEAD/status/branch/.git/commit IDs.
- Preflight all source pins, payload hashes/byte counts and destinations before the first write. Different same-path bytes block the entire install; identical reuse is reported; no silent overwrite.
- D-owned source patch must be narrow, preimage/postimage hash-gated and have a byte-exact backup before atomic replacement. Do not patch protected C11-C source.
- The visual consumer remains an in-memory D-owned component at the existing E1 boundary. It must not activate renderer-native input, dispatch, media/audio production or release.

## Process / receipts

- Use `Start-Process -Wait -PassThru` or an equivalent process API; capture stdout/stderr separately with SHA-256 and propagate nonzero exit codes immediately.
- Receipts record run IDs, source pins, evidence input hashes, output hashes, process exit codes, governance booleans and `release_authority=NONE`.
- Read-only audit runners must not write into source directories except their unique evidence output root; never call Git, generators, Godot, D3 V5, FFmpeg, renderer or media.
- Keep no more than one new GUI/CLI entrypoint pair; both call the same shared helper.

## V12 package self-containment and hash-guarded rollback

A package must carry every newly introduced guide, register, docket or reference that its own installer requires as an ADD operation. The installer must validate the package member SHA and staged postimage; it must not require the new file to exist in the checkout before installation. Document/prompt references must resolve either to the current checkout or to a same-package ADD. The canonical continuity prompt directory is root `prompts/`.

### Hash-guarded rollback

Rollback is allowed only when the installed destination still matches the exact expected postimage. A replacement backup must hash to the exact preimage recorded before mutation before it is restored. If the current destination matches neither the expected postimage nor the expected preimage, refuse to overwrite/delete it and preserve the unknown/operator-modified state. Restore the verified backup atomically and verify the restored destination against the preimage. For ADD rollback, delete only when the current file matches the exact expected postimage. The transaction journal must be written before each mutation. If the journal is empty, report `rollback=NOT_NEEDED`; never imply that a rollback occurred.

V12 also requires static checks that the installer source retains these postimage/preimage/unknown-state guards, not only a textual policy assertion. It continues to require PowerShell 5.1 AST, ASCII-only runner source, validated payload operation rows, short `%TEMP%` staging with a maximum path length of 240 characters, direct Python 3.13 executable probing, separate stdout/stderr, immediate exit-code checks, non-null byte-exact backups, no automatic dependency installation, source SHA pins and frozen C11-C manifest checks.

## V13 complete E1 Drill test staging roots

The E1 Drill consumer suite calls the existing shared production service and D9.9/D9.10 resolver chain. A staged test tree must include the complete pinned source roots required by that chain, not merely the new consumer files. For this gate the stage must copy and path-budget-check `challenges/`, the complete `assets/` tree (including `assets/c6/garage_background.svg`), `docs/current/d/` (including the D1.5 platform layout contract), `docs/current/e/`, `docs/history/c11e/`, `definitions/`, `profiles/`, `release/`, `core/`, `tools/`, and `c11c-suite/c11c-producer/`. Verify required stage-root existence before Python execution. Do not widen repository writes: these are read-only staged test inputs; only the 18 manifest operations may enter the transaction.


## StrictMode variable initialization

Under `Set-StrictMode -Version 2.0`, every variable must be assigned before its first read. For staged-source inspection, load every file into its corresponding variable before checking any of those variables; do not put an unassigned variable in a compound `-or` expression. Validate required source strings are non-empty before inspection. Build-time validation must assert assignment-before-first-use for staged source variables checked statically.

## V22 historical addendum — `Tee-Object` parameter sets and one-shot continuation

Before authoring a PowerShell runner or recovery script, reread this current guide from the active checkout, record its exact path/version/SHA in the build verification, and add a regression/static assertion for each relevant rule.

1. **`Tee-Object` parameter-set exclusivity:** `-FilePath` and `-Variable` are alternative parameter sets in Windows PowerShell 5.1. Never specify both in one invocation. To stream and preserve output, use `Tee-Object -FilePath $logPath` and consume its output downstream (for example `ForEach-Object { Write-Host ([string]$_) }`). Read the completed log only after the child process and pipeline have exited.
2. **Do not assume `Tee-Object` binding errors are child failures.** A parameter-binding error must be diagnosed at the parent pipeline boundary. Require a child-issued run/output ID and independently check child output roots/diagnostics before deciding that a one-shot child started.
3. **One-shot lock recovery:** never delete a one-shot lock to retry. A new continuation may use an existing `ATTEMPT_RESERVED` lock only when exact run/package identity, the previous failure receipt, empty/no child console output, absence of a child output ID, and absence of matching output/diagnostic directories prove the child did not start. Record the authorization; retain the same lock. Once the child launch is authorized, mark it before invoking the child; any later failure blocks retry.
4. **Capture exit code immediately:** after a native child pipeline, assign `$LASTEXITCODE` on the very next statement. Do not execute another native program, `Get-Content`, hash utility or other native command before capture. Then read stdout/stderr after the child has exited.
5. **Never print a later PASS after a thrown failure.** Do not append manual commands after a script error. A one-shot script is executed with `powershell.exe -NoProfile -ExecutionPolicy Bypass -File <saved-script>`; no multi-stage interactive paste.
6. **No reinstallation after successful transaction.** If install receipt and journal prove PASS, resume from the exact remaining gate. `SKIP_IDENTICAL_POSTIMAGE` has no backup and cannot satisfy a new replacement-backup requirement.
7. **Keep evidence boundaries exact.** Match the original install run ID, package SHA, journal, backups, postimages and audit receipt. Do not substitute a later idempotent run. Preserve all failed output folders and diagnostic ZIPs.

### R6.3A actual parameter-binding incident

Recovery script `RECOVER_C11E_R6_3A_FIRST_INSTALL_AUDIT_AND_REQUALIFY.ps1` called `Tee-Object` with both `-FilePath` and `-Variable`, causing the Spanish PowerShell 5.1 parameter-set error immediately after `R6_3A_REQUALIFICATION_START=TRUE`. The install and independent audit had already passed; all 14 documentation files were added. The approved continuation `RESUME_C11E_R6_3A_REQUALIFICATION_AFTER_TEE_BINDING_FAILURE_V3.ps1` must validate the existing `ATTEMPT_RESERVED` lock, exact first-run audit and docs receipts, previous binding error, empty child console log/no `R6_3A_OUTPUT_ID`, and no matching D output or diagnostics. The approved V3 continuation launches the existing D-owned runner once using `Start-Process -Wait -PassThru` with separate stdout/stderr files. It does not reinstall, re-audit, or repeat the 32 consumer tests.


## V23 addendum — process launch, log capture and one-shot continuation

Before authoring a PowerShell runner or recovery script, reread this guide from the active checkout, record its exact path/version/SHA in build verification, and add a static assertion for each applicable rule.

1. Use `Start-Process -Wait -PassThru -RedirectStandardOutput <stdout> -RedirectStandardError <stderr>` for one-shot child PowerShell runners. Build the `-ArgumentList` string with a Windows command-line quoting helper and test paths with spaces and trailing backslashes. Do not combine `-NoNewWindow` with redirection unless that exact parameter set is separately verified in Windows PowerShell 5.1.
2. Immediately after `Start-Process` returns, assign `$exitCode = [int]$process.ExitCode`. Only after the process has exited may stdout/stderr be read, hashed, parsed or printed. Keep them as separate files.
3. `Tee-Object -FilePath` and `-Variable` are mutually exclusive parameter sets in Windows PowerShell 5.1. Never specify both. The R6.3A V3 continuation does not use `Tee-Object`.
4. Do not classify a parent-side parameter-binding error as a child failure. Require a child-issued output ID and independently check output roots and diagnostics before determining that a child started.
5. Never delete or overwrite an existing one-shot lock. Resume from `ATTEMPT_RESERVED` only when exact run/package identity, previous failure log, empty/absent child console, no child output ID and no matching output/diagnostic directories prove the child did not start. Write a separate authorization with `FileMode.CreateNew` before child launch; after that marker exists, any failure prohibits retry.
6. Complete every non-mutating preflight before documentation writes and before consuming the launch marker: PowerShell executable, Python version/imports, package identity, runner path/SHA, receipts, lock, logs, output roots and diagnostics.
7. Run saved scripts with `powershell.exe -NoProfile -ExecutionPolicy Bypass -File <script>`. Capture exit codes immediately. Never append interactive commands after `throw` or print a later PASS.
8. Do not reinstall after a successful transaction. `SKIP_IDENTICAL_POSTIMAGE` has no backup and cannot satisfy a replacement-backup audit.
9. Preserve exact install RUN_ID/package SHA/journal/backups/postimages/audit receipts. Never substitute a later idempotent run; preserve failed outputs and diagnostics.

### R6.3A parameter-binding incident

The first-install recovery was successful through independent audit and 14/14 documentation ADD_ONLY. Its parent script then passed both `-FilePath` and `-Variable` to `Tee-Object`; PowerShell 5.1 rejected the mutually exclusive parameter sets before the child runner emitted an output ID. The original `ATTEMPT_RESERVED` lock is retained. Resume V3 proves that no child output or diagnostics were created, verifies all accepted receipts, completes non-mutating checks before writes/authorization, and starts the exact installed runner once using `Start-Process` with separate logs. No install, audit, 32-test suite, native capture, music generation, Godot, GUI or CLI smoke is repeated.


## V26 addendum — Correct handling of optional manifest preimages and flat ZIP extraction

The 2026-11-15 E4C PRE_ROLL bridge installer V1 stopped during pre-transaction package validation because it dereferenced `operation.preimage_sha256` for `ADD` operations. The field is intentionally present only for `REPLACE`; under `Set-StrictMode -Version 2.0`, direct property access on an `ADD` object terminates execution. The corrected installer must inspect `$operation.PSObject.Properties['preimage_sha256']` before reading the value, require a valid 64-character SHA only for `REPLACE`, and reject a non-empty preimage on `ADD`. Do not weaken strict mode or add fake preimage values to ADD manifest rows.

### Manifest operation schema

- `REPLACE`: requires `path`, `operation`, `preimage_sha256`, `bytes`, `sha256`. The destination must exist and match the exact preimage before staging or writing.
- `ADD`: requires `path`, `operation`, `bytes`, `sha256`; `preimage_sha256` is omitted. Destination must be absent or byte-identical to the postimage.
- Validate exactly five `REPLACE` and fourteen `ADD` operations for the V2 bridge package, with unique safe relative paths and exact payload cardinality.
- Never cast a missing manifest property to a string under strict mode. Use `PSObject.Properties` presence checks and explicit null handling.

### ZIP layout and extraction contract

The V2 corrective ZIP is deliberately flat at archive root: installer, manifest, sidecars, README, build verification and `payload/`. The operator must create a new, version-specific extraction directory and use `Expand-Archive -DestinationPath $Kit`. The installer must then exist directly at `$Kit\INSTALL_C11E_E4C_TRACKING_PREROLL_BRIDGE_FIX_V2.ps1`. Do not rely on Explorer's inferred folder naming and do not create a second same-name nested folder. The README must print and verify the exact installer path before invoking it.

### Failed preflight classification

If failure occurs before the evidence root and transaction journal are created, report `FAILED_PRE_TRANSACTION_NO_CHECKOUT_WRITES`. A console error from the parent `powershell.exe -File` command is not an installer receipt. Capture the child PowerShell exit code immediately after that command; never reuse a stale `$LASTEXITCODE` after a path-not-found error.

The V2 installer is still required to perform all source pins, exact replacement preimages, package inventory, staged `py_compile`, focused test suites and PowerShell AST parsing before creating its transaction journal and applying the first checkout write. It must never invoke Git, pip, Godot, FFmpeg, renderer or production dispatch.


# V27 addendum — Atomic file replacement under Windows PowerShell 5.1

The 2026-11-15 PRE_ROLL bridge installer V2.1 failed while updating its transaction journal. The installer called `[System.IO.File]::Replace(source, destination, $null)`. On the target Windows PowerShell 5.1/.NET Framework runtime, that call raised `The path is not of a legal form` while resolving the null backup-path argument. The first journal creation had succeeded; the next journal update failed before the first checkout payload mutation. The failed installation must remain evidence only and must not be rerun.

For atomic replacement, never pass a null third argument to `System.IO.File.Replace`. Create a unique, fully qualified backup path in the destination directory, call `File.Replace(source, destination, backupPath)`, verify the destination exists, then remove the transient swap backup. The durable transaction backup remains separately copied to the evidence root and hash-verified before replacement. The source temporary file must be created beside the destination so the replace is same-volume. For a destination that does not yet exist, use `File.Move(source, destination)`.

Journal and receipt writes use the same helper: write UTF-8 without BOM to a unique sibling temporary file, then use the explicit-backup atomic replacement path when the journal already exists. A helper failure must clean its temporary source when safe and preserve the original destination. Catch-path journal/receipt writes must use this corrected helper as well.

Required pre-transaction regression tests on Windows PowerShell 5.1: (1) create a new UTF-8 file; (2) replace the same file repeatedly; (3) replace an existing destination using a non-null, unique backup path; (4) move to a missing destination; (5) use paths containing spaces; (6) verify exact contents, source consumption, and absence of leaked `.tmp` / `.swap.bak` files. Parse the installer, helper and test runner with the PowerShell 5.1 AST before execution.

The installer must run these tests before creating its transaction journal or changing the checkout. The operator must verify the external ZIP SHA-256 before extraction. The sidecar detects manifest mismatch inside the ZIP; it is not a substitute for the external ZIP hash.


# V28 addendum — Coordinator/wrapper identity and installed-guide alignment

The V3 PRE_ROLL bridge overlay installed PowerShell style guide V27, while its tracking batch coordinator still required V26 and its PowerShell wrapper still required V25/V26 and pinned a stale coordinator SHA. This mismatch blocked PREPARE_ONLY even though the V3 installer receipt was PASS. Do not repeat the old wrapper or run the old coordinator directly.

For an installed batch runner, the wrapper's hard-coded `BATCH_DRIVER_SHA` must equal the exact SHA-256 of `c11e_e4c_tracking_tier_batch.py` installed by the same transaction. A source test must compute the actual coordinator hash and compare it to the wrapper's declared hash. When the latest packaged style guide is V27, both wrapper and coordinator must require V27; neither may require uninstalled V24/V25/V26 files. The coordinator continues to verify its V23 source pin through its existing source-pin set, and the wrapper may verify V23 plus the newly installed current guide V27. Never make a missing legacy guide a runtime prerequisite.

After installation, run the wrapper once without `-Execute`, supplying a new BatchId. Require the wrapper and coordinator exits to be zero, `PASS_PREPARE_ONLY_NO_RENDER`, the exact four selector rows, `renderer_invoked=false`, `godot_invoked=false`, `ffmpeg_invoked=false`, `production_dispatch=false`, and `release_authority=NONE`. PREPARE_ONLY must not create `ATTEMPT_RESERVED.lock.json` or `EXECUTION_AUTHORIZED_ONCE.json`; it does not consume the BatchId. Only after independent review of that receipt may the operator authorize execution once. Preserve the prepare stdout/stderr and the exact BatchId for the execution handoff.

Do not run Git checks. Operator manages commits. Keep the frozen C11-C manifest SHA pinned and unchanged.


## V30 — Windows PowerShell 5.1 native stderr capture correction (2026-11-15)

### Incident: native unittest stderr was misclassified as a terminating PowerShell error

The first Pursuit batch overlay installer (V1) executed a Python `unittest` file using `& $python $stageTest1 2>&1` while `$ErrorActionPreference = 'Stop'`. Python's standard `unittest.TextTestRunner` writes its progress/result stream to stderr by default. Windows PowerShell 5.1 converts redirected native stderr records into `NativeCommandError`; with `ErrorActionPreference=Stop`, the installer terminated while collecting the test output. The visible `...test_expected_post_r63a_consumer_and_test_are_pinned ... ok` line is a passing test line, not proof that the full suite completed. The transaction had not started: `transactionStarted` was still false and all 18 ADD_ONLY operations remained uncommitted. No checkout payload mutation occurred.

### Mandatory native child process rule

1. Do not invoke Python `unittest` using `& $python <test.py> 2>&1` under a terminating `$ErrorActionPreference`. This is unsafe in Windows PowerShell 5.1 even when stderr is normal test output and the child would otherwise exit successfully.
2. For installer child processes that may write stderr on success (Python tests, environment probes, `py_compile`, and nested PowerShell tests), use `Start-Process -Wait -PassThru` with separate `-RedirectStandardOutput` and `-RedirectStandardError` paths.
3. Capture `[int]$process.ExitCode` immediately on the statement following `Start-Process`. Read both files only after `-Wait` has completed. Preserve both streams in the installation evidence directory.
4. Evaluate exit code and expected output independently. Non-empty stderr is not itself a failure; an exit code of zero plus the expected test summary is required. Conversely, a success-looking line does not override a nonzero child exit.
5. A failed preflight must still write `INSTALL_FAILURE.json` and `INSTALL_PROGRESS.json`. The failure receipt records the current gate, exact exception, `transaction_started`, committed operation count, package/manifest identities when available, and evidence/stage paths. If `transaction_started=false`, explicitly state that checkout payload mutation did not begin.
6. Keep the staged package and all stdout/stderr logs on failure. Remove the staging directory only after the full install and embedded PREPARE_ONLY both succeed. Never infer transaction state from an outer PowerShell exit alone; inspect the durable receipt/journal.
7. Continue to run PowerShell 5.1 AST checks, all package/source pins and the frozen C11-C manifest check before the first checkout write. ADD_ONLY operations remain non-overwriting and no rollback/deletion is implied by a failed partial transaction.

### Required regression coverage

The installer contract tests must statically assert the presence of separate Start-Process stdout/stderr capture for Python test invocations, immediate exit-code capture, reads after process completion, and absence of the unsafe `& $python $stageTest1 2>&1`/`& $python $stageTest2 2>&1` form. The two Python test suites must run to completion and their `Ran N tests` plus `OK` summaries must be read from the completed log files.

## Pursuit recovery V4 — authoritative installer correction (2026-11-15)

The V3 recovery package was not executed: Windows PowerShell 5.1 rejected its script at parse time because the audit-receipt hashtable declared `source_pins_post` twice (the summary key and detailed array). The parser error occurred before installer execution, so V3 made no checkout mutations. Do not run V3.

V4 is the only recovery candidate. It retains the 19/19 ADD_ONLY destinations committed by V2, audits the exact V2 run `C11E_E4C_PURSUIT_BATCH_OVERLAY_V2_20261115T130255Z_b5f15417`, corrects the duplicate key to `source_pin_results_post`, and adds an operator-side `Parser.ParseFile` gate before invoking the installer. Its transaction is bounded to two SHA-pinned replacements (pursuit runner and runner-contract test) plus 15 ADD_ONLY documentation/prompt destinations. It must pass 34/34 source pins, frozen C11-C manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` / 796318 bytes, Windows PowerShell 5.1 AST, Python 3.13 tests and atomic I/O 6/6 before mutation.

V4's default embedded pursuit action is PREPARE_ONLY. Do not pass `-Execute`. Independently audit the V4 receipt, journal, two backups, 17 postimages, 34 source pins and the resulting five-selector BatchId before authorizing a later execution. Preserve all failed evidence. C11-C/E1/dispatch boundaries remain unchanged.

## Overlay installer and batch runner additions — V32

1. Pin every modified Python coordinator and PowerShell runner by SHA-256. Keep operator commits unmanaged by scripts; do not run Git status, branch, HEAD or commit checks.
2. In PowerShell 5.1, parse the installer and every shipped `.ps1` with `System.Management.Automation.Language.Parser.ParseFile` before transaction. Also instruct the operator to parse the installer in a parent PowerShell process before invoking `-File`.
3. Invoke Python and nested PowerShell through `Start-Process -Wait -PassThru -RedirectStandardOutput -RedirectStandardError`; read both files only after process exit. Avoid native stderr redirection through PowerShell's error pipeline.
4. Run source-pin, frozen-manifest, fixture and PREPARE_ONLY checks before `TRANSACTION_STARTED`. Preserve actual replacement backups and an append-only operation journal. Use same-directory temp files with `Invoke-C11EAtomicReplace`.
5. On failure, roll back only destinations whose current content still matches this transaction's postimage. Preserve conflicting or changed files and report rollback as incomplete rather than deleting unknown data.
6. PREPARE_ONLY must not create execution locks, authorization markers, media, renderer/Godot/FFmpeg invocations or dispatch. `-Execute` must be explicit.

## Package-relative helper dependencies and interactive preflight (V33)

1. Treat ZIP entry paths as authoritative. When the archive stores `payload/support/X.ps1`, the extracted path is `<stageRoot>\payload\support\X.ps1`; never assume a stripped `support` directory. Test every staged path with `Test-Path -PathType Leaf` before reading or parsing it.
2. AST-parse the installer, runner, atomic helper and helper test from their exact extracted paths before any transaction.
3. If the installer invokes helper-defined functions, dot-source the helper into the installer scope after its AST and content hash pass. Then verify each required function with `Get-Command -CommandType Function`. Parsing a helper file does not load its functions.
4. Exercise the installer's actual JSON writer through a create/readback/delete probe before setting `transaction_started`. A separate helper unit test does not prove the installer wrapper is bound.
5. Keep a fallback evidence writer for failure JSON so that a missing atomic dependency does not suppress its own incident record. Do not report an evidence path as written unless `Test-Path` confirms it.
6. In interactive PowerShell, submit a complete `if { ... } else { ... }` construct in one parse unit. If pasting line-by-line, prefer `if (...) { throw ... }` followed by an independent `Write-Host PASS` line; do not submit `else` after PowerShell has already executed the preceding `if` block.
7. Do not print PASS unconditionally after a command that may have thrown. Place PASS only after the guarded operation has completed without error.


## V5.3 installer hardening — mandatory sequence (2026-11-15)

- Validate every ZIP member name and duplicates before `Expand-Archive`; reject rooted paths, drive/colon names, backslashes, traversal segments and directory entries. Then compare exact ZIP entry set with manifest+sidecar+payload inventory.
- Resolve support members as `<stageRoot>\payload\support\...`; dot-source the atomic helper and check both required functions with `Get-Command`. A function name or path string in source is not proof that the function is imported.
- Stage test fixture in both `project\tests\fixtures` and `project\definitions`; do not use copy-to-self. The test contract's `ROOT.parent` resolves to the extracted package root and must find `PACKAGE_MANIFEST.json` and the V5.3 installer there.
- Do not set `transaction_started=true` before all four REPLACE backups exist, match preimage SHA/bytes and are persisted in the journal. Revalidate all 20 destinations at the boundary, and recheck each immediately before the atomic operation.
- A backup-preparation failure is a pre-transaction failure (`transaction_started=false`), not a rollback. Preserve its evidence and stop. Persist the backup manifest in the failure record/receipt.
- On interactive Windows PowerShell, keep the full `if { throw }` block together; execute a standalone `Write-Host ...PASS` only after that block returns. Never type `else` as a separate prompt after the `if` already executed.
- The V5.3 staged Python suite contains 37 tests. Native Windows PowerShell 5.1 AST and atomic-I/O 7/7 are mandatory local preflight gates and must not be represented as Linux build results.

V5.3 refuerza además el límite transaccional: exige que existan previamente todos los directorios padre; comprueba el binding exacto de cada destino REPLACE con su payload; usa creación atómica exclusiva para ADD (no sobrescribe un destino concurrente); y limita el rollback a operaciones confirmadas o a la operación REPLACE en vuelo. Los temporales en vuelo se limpian en fallo. La suite Python se exige exactamente en 37/37 y la prueba atómica amplía a 7/7 con colisión ADD.
