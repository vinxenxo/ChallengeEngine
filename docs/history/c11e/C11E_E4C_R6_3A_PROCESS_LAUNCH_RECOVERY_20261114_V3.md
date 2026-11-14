# C11-E E4C R6.3A — First-install audit recovery record

**Date:** 2026-11-14  
**Scope:** Only the two R6.3A attempts in the operator-supplied latest evidence ZIP.

## First attempt: child installation succeeded; outer driver failed

- Run ID: `C11E_E4C_V2_3_R6_3A_20261114T163406Z_fc8436fa`.
- Package SHA-256: `47d5a30c315365eb7a31e37fc4bc1c2ff6ca0a297d1e57eccf89c3f5a024b96e`.
- Installer receipt: `PASS_REPLACE_AND_ADD_ONLY_INSTALL`.
- 3 REPLACE +15 ADD; 18/18 postimages; 3/3 backups; 25/25 source pins; PowerShell AST 3/3; py_compile 3/3; consumer tests 32/32.
- Journal statuses: all three replacements `REPLACED_POSTIMAGE_VERIFIED`.
- Backups independently extracted from evidence ZIP and hashed: 18,143 bytes / SHA `81a45c8a...`; 36,497 bytes / SHA `9a20a6a8...`; 62,255 bytes / SHA `21762919...`. Each equals its journal/manifest preimage SHA.
- The outer driver failed at `ReadAllText(INSTALL.stdout.log)` because the file was still locked by the child process. The child installation had already persisted its PASS receipt, journal and backups. This is not an installer failure.

## Second attempt: idempotent skip, not a replacement transaction

- Run ID: `C11E_E4C_V2_3_R6_3A_20261114T163827Z_47eab402`.
- Package SHA-256: `e335b0ff2806e638166922ef67803c8e47534660ad13e781d3b74ab9ca7ef1a7`.
- All three replacements were `SKIP_IDENTICAL_POSTIMAGE` and each `backup_path` was null.
- The installer receipt nevertheless claimed `backups=3/3 PASS`. This is an accounting defect.
- The independent auditor's `REPLACEMENT_BACKUP_FAIL` for this second run is correct: that run did not make backups. It must not be used as the audit target.

## Recovery action

Use the original R6.3A package with SHA `47d5...` and audit the first transaction run ID. The recovery script extracts that exact package, runs the independent auditor against the first transaction, verifies its audit receipt, and then runs the already-installed D-only R6.3A role-style requalification exactly once. No installer rerun, source patch, smoke, native capture, Godot or music generation is permitted.

## Governance and acceptance

C11-C frozen manifest remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; E1 remains `PREPARE_ONLY`; family adapter `NOT_CONNECTED_E1`; production dispatch false; release authority NONE. E4C human selector remains 0/20 until seven-frame visual review and A/B/C listening acceptance.

## R6.3A continuation incident — 2026-11-14, Tee-Object parameter-set binding

The first R6.3A install transaction `C11E_E4C_V2_3_R6_3A_20261114T163406Z_fc8436fa` is authoritative and independently audited PASS. The recovery invocation `20261114T192552Z_7650ad32` also completed documentation ADD_ONLY 14/14 and created `R6_3A_REQUALIFICATION_ATTEMPT_LOCK.json` with `ATTEMPT_RESERVED`; it then failed before the child requalifier printed an output ID.

Root cause is the recovery script pipeline `... 2>&1 | Tee-Object -FilePath $runnerLog -Variable runnerLines`. Windows PowerShell 5.1 `Tee-Object` exposes `-FilePath` and `-Variable` through different parameter sets. Supplying both produces “Parameter set cannot be resolved using the specified named parameters.” This is a PowerShell parameter-binding failure, not a Python/FFmpeg/rendering failure. The child runner did not get a valid pipeline invocation. The lock must not be deleted or bypassed; a dedicated continuation script must prove the previous child did not start (empty/missing console log, no `R6_3A_OUTPUT_ID`, no matching output folder, no matching diagnostic output) and verify exact audit/doc receipts before resuming once.

The V3 continuation replaces the failed parent pipeline with `Start-Process -Wait -PassThru -RedirectStandardOutput` and `-RedirectStandardError`. It assigns the child process `ExitCode` immediately, then hashes/reads the separate logs after process exit. `Tee-Object -FilePath` and `-Variable` remain mutually exclusive and are not used by V3. No installation, audit, 32 tests, native capture, music generation, GUI/CLI smoke or Godot is repeated.

The user-reported `r6_3a_audit_recovery.zip` was not surfaced by the current Library index during this continuation. The diagnosis is independently established by the pasted console output and the exact recovery script source included in the previous kit. The continuation script performs live checkout checks before any child launch.

Current status: install PASS; independent audit PASS; docs ADD_ONLY 14/14 PASS; requalification is NOT_STARTED; E4C operator acceptance remains 0/20. A single continuation is allowed only after the fail-before-child preconditions pass. After child launch, any failure is terminal for this output attempt and must be diagnosed from its preserved output/diagnostics rather than rerun.

## Authoritative continuation — R6.3A requalification resume (2026-11-14)

This section supersedes earlier R6.3A immediate execution instructions.

### Accepted gates (do not repeat)
- Original R6.3A install: `C11E_E4C_V2_3_R6_3A_20261114T163406Z_fc8436fa`; 3 REPLACE +15 ADD_ONLY, postimages 18/18, backups 3/3, pins 25/25, Python compile 3/3, consumer tests 32/32, File.Replace forward/rollback, immediate recheck PASS.
- Independent audit of that exact first transaction: `PASS_INDEPENDENT_POST_INSTALL_AUDIT`; journal 18/18, postimages 18/18, backups 3/3, pins 25/25, frozen C11-C manifest and immutable decision record PASS.
- Documentation recovery: 14/14 ADD_ONLY PASS; all nine current project docs, history record, PowerShell style guide V21 and Master/Start/First prompts were added.
- Second installer run `...163827Z_47eab402` is an idempotent replay that skipped all three replacements; its backup receipt claim is not audit authority. Do not rerun or use it.

### Current failure
Recovery root: `artifacts/tests/c11e/r6_3a_audit_recovery/20261114T192552Z_7650ad32`. A one-shot lock was created as `ATTEMPT_RESERVED`. The attempt then failed with the Windows PowerShell 5.1 parameter-set error because the recovery script supplied both `-FilePath` and `-Variable` to `Tee-Object`. This is not a FFmpeg failure. No successful child output ID was reported. The corrected continuation must prove no child output/diagnostic exists before reusing the reserved lock.

### Next action
The V1 continuation is superseded and must not be run. Run only `RESUME_C11E_R6_3A_REQUALIFICATION_AFTER_TEE_BINDING_FAILURE_V3.ps1` from the V3 continuation kit. It verifies the exact first install/audit receipts, prior 14/14 document transaction, existing ATTEMPT_RESERVED lock, previous parameter-binding failure, no child output ID/root/diagnostics, Python/PySide6, package identity and the exact installed runner SHA. It does not reinstall, re-audit or repeat the 32 tests. It starts the runner once with `Start-Process -Wait -PassThru` and separate stdout/stderr files; it captures the exit code before reading logs. A failure after the V3 CreateNew claim prohibits retry.

### Required result
Technical PASS means 810/810 composition frames, 90/630/90 phases, preserved GAME body and family role styling, identical A/B/C video elementary streams, identical A/B AAC and distinct C, FFprobe contract, zero drift, seven review frames, technical receipt and operator bundle. This does not count as human acceptance. `tracking/tier-1` remains 0/20 until the operator reviews seven frames and all three A/B/C MP4/audio outputs.

### Governance / roadmap
C11-C 2.19.12 frozen manifest remains SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; E1 `PREPARE_ONLY`; `family_adapter=NOT_CONNECTED_E1`; dispatch false; `release_authority=NONE`; Git checks skipped; commits operator-managed. No protected C11-C edits, new capture, music generation, Godot, GUI/CLI smoke or dependency changes. After E4C 20/20 proceed to E5 → E6 Smoke18 → E7 Matrix101 (CH_008/009 held; 99 provisional) → E8. E9/E10 have not yet been accepted as scoped phase definitions; define them from the governance/acceptance roadmap after E8 rather than inventing gates in this recovery.


## Final root cause and approved continuation V3 — 2026-11-14

The operator's first-install recovery run completed the original R6.3A independent audit and the 14/14 ADD_ONLY documentation transaction. It then failed before the D-owned runner started because the recovery script used `Tee-Object -FilePath` and `-Variable` in one call; PowerShell 5.1 treats these as exclusive parameter sets. No `R6_3A_OUTPUT_ID` was issued and no D composition/mux began. The exact `ATTEMPT_RESERVED` one-shot lock remains intact.

The unissued continuation V1 was rejected because of an incorrect `$audit`/`$auditPath` binding and a wrong runner path. The V3 continuation draft was also unissued; its preflight ordering and log-capture strategy were superseded before operator execution.

V3 verifies the exact first install receipt/journal and independent-audit receipt without rerunning those gates. It verifies the prior documentation receipts and hashes, existing one-shot lock, parent-side binding failure, absent/empty child console and no child output/diagnostics. It resolves the exact installed D runner SHA from the original package manifest. It completes PowerShell/Python/PySide6/package/runner checks before documentation writes or launch authorization. It performs the next 14 document additions idempotently and creates a separate `FileMode.CreateNew` continuation marker only after every prelaunch check succeeds. It uses `Start-Process -Wait -PassThru` and separate stdout/stderr files; process exit is captured immediately and logs are read only after process exit. It does not reinstall, re-audit, repeat the 32 tests, recapture native media or regenerate family music.

Any failure after the V3 claim is terminal; the claim and original lock must be preserved. No automatic retry is permitted.

Current status: original R6.3A installation PASS; first-run independent audit PASS; first 14 documentation additions PASS; requalification child not started at the last logged failure; no output ID; human visual/audio acceptance remains pending; E4C remains 0/20.

Governance remains unchanged: C11-C 2.19.12 sole production authority; frozen manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; E1 PREPARE_ONLY; family adapter NOT_CONNECTED_E1; dispatch false; release authority NONE; no Git checks; commits operator-managed.
