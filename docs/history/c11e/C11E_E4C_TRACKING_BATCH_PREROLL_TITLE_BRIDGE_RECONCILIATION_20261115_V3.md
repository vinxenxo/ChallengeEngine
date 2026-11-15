# C11E E4C tracking tier PRE_ROLL family-title bridge — V2 installer reconciliation

**Date:** 2026-11-15  
**Status:** V2 package prepared; Windows installation not yet performed.

## Incident A — consumed batch execution failure

Batch `E4C-TRACKING-T2-5-20261115T005529Z-a78c6c24` was authorized exactly once and stopped at `tracking/tier-2`, child exit code 2. Captured stderr: `C11-E PRODUCTION SERVICE ERROR: D composition plan editorial must be hidden during PRE_ROLL`. The failure bundle records `STOPPED_FAIL_CLOSED`, `completed_rows=[]`, `cli_summary_exists=false`, and no selector output roots. The identifier is permanently consumed.

## Root cause

The approved R6.3A consumer V2 supports family title visibility during PRE_ROLL, with subtitle and call-to-action visible only in GAME. The existing E4C Drill executor still contained a stale all-editorial-hidden PRE_ROLL assertion. The D executor helper and its tests are the correct repair boundary. No consumer, binder, E1 service, GUI/CLI, C11-C or renderer modification is authorized.

## Incident B — corrective installer V1 did not transact

The first PRE_ROLL bridge installer V1 was invoked from the nested extracted path. It failed during pre-transaction manifest validation with a PowerShell StrictMode property error: `preimage_sha256` does not exist on `ADD` manifest rows. The property is optional by design and exists only on the five REPLACE rows. There was no transaction journal or checkout write. The ZIP extraction layout also created avoidable path ambiguity; V2 uses a flat archive plus an explicit `Expand-Archive -DestinationPath` command. V1 must not be rerun.

## V2 corrections and scope

- Fix optional-property handling using `$op.PSObject.Properties['preimage_sha256']`; require the property only for REPLACE.
- Validate exactly 5 REPLACE and 14 ADD operations, unique safe paths, file byte lengths, and SHA-256 values.
- Preflight five exact active-checkout destination preimages and 30 source pins.
- Stage four Python modules/tests and copy the current pinned CLI and GUI as read-only test fixtures.
- Run Python 3.13 compilation, the executor focused suite and tracking-batch suite, and real PowerShell 5.1 AST parsing before the first checkout write.
- Preserve exact backups, append-only transaction journal, and install receipt; verify five postimages, fourteen new files, 30 postinstall pins and frozen C11-C SHA.
- Upgrade the batch coordinator and runner to require PowerShell guide V26; preserve V23–V25 historical guide checks.
- Document the failure, update authority/roadmap/gates/backlog/style guide/incident register and all three prompts.

## Execution boundary

V2 installer is preflight/install only: no Godot, FFmpeg, renderer, native capture, music generation, production media, production dispatch, Git checks or dependency installation. After V2 install, generate a new PREPARE_ONLY BatchId. Independently audit it. Never reuse the consumed BatchId above. Any subsequent actual execution is a separate operator authorization and must stop fail-closed.

## Fixed governance

C11-C 2.19.12 remains the sole production baseline; frozen manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. `release_authority=NONE`; `production_dispatch=false`; Git checks skipped; commits operator-managed.


## V3 installer transaction repair (2026-11-15)

V2.1 passed external ZIP, manifest, installer, Python 3.13.14 and PySide6 6.11.2 checks, then failed while replacing its existing transaction journal. The exception came from `System.IO.File.Replace` receiving `$null` as its backup path. The initial journal file had already been created; the failure occurred on the first journal update, before the first payload destination mutation. Preserve the failed V2.1 evidence and do not rerun that installer.

V3 replaces both null-backup `File.Replace` call sites: journal/receipt writes and transactional REPLACE operations now use the packaged atomic-file helper. The helper supplies a unique fully qualified sibling backup path, verifies the destination, and removes only the temporary swap backup; the durable preimage backup remains in the transaction evidence. The V3 installer runs a PowerShell 5.1 AST check and an isolated atomic-I/O regression test before any checkout mutation, then performs the existing 4 Python compile/test stages and 30 pre/post source pins. The consumed batch ID remains permanently reserved; V3 does not execute it and does not render.

V3 does not change the E1 service, GUI/CLI facade, C11-C protected sources or frozen C11-C manifest. `production_dispatch=false`, `release_authority=NONE`, Git checks skipped and commits remain operator-managed. After successful installation and an independent audit, the next operational step is a fresh PREPARE_ONLY batch with a new BatchId; execution remains a separate authorization gate.
