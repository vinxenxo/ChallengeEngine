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
