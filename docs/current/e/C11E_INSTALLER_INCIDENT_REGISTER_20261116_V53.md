# C11-E Installer Incident Register — V53 (2026-11-16)

## Incident: E5 Overlay V1 rejected by PowerShell 5.1 parser (2026-11-16)

The operator's V1 invocation exposed six duplicate keys in the installer's `Write-ProgressSnapshot` hashtable: `package_id`, `package_zip_path`, `package_zip_sha256`, `package_manifest_sha256`, `evidence_root` and `staging_root`. The initial interactive block also submitted `else` as a separate console command; that is not valid as a second interactive submission after a closed `if` block. The installer itself was then invoked and rejected by PowerShell's parser at line 358 before any script statement executed. Its child exit code was 1.

Disposition: `FAILED_AT_PARSE_TIME_PRE_EXECUTION`. The installer body did not run, no install evidence root or journal could be created by that script, no ADD_ONLY destination was written, and no E5 BatchId was reserved. Do not invoke or reuse the V1 extraction.

V2 correction: remove duplicate hashtable keys; change package identity and installer name to V2; add a saved launcher so no bootstrap `else` block is pasted interactively; verify archive SHA and member safety before extraction; AST-parse launcher, installer, atomic helper and helper test; invoke the installer as a separate child with `Start-Process -Wait -PassThru`, separate stdout/stderr files and immediate exit-code capture; preserve `LAUNCH_FAILURE.json` and the V2 extraction on any failure.

## E5 combined overlay hardening

The E5 combined package is authored against the current PowerShell runner style guide V36 (65,465 bytes; SHA-256 `4f3940d50b07ccd48e30f44dbc8653a9021791d20382dbccdb7ca0d93f98f337`). The installer is Windows PowerShell 5.1-only and self-parses the installer, atomic helper and helper-test scripts before any checkout transaction.

Pre-transaction sequence: external ZIP sidecar; embedded manifest sidecar; exact ZIP member inventory; path traversal/duplicate rejection; exact payload bytes/SHA; V36 and 31 source pins; historical references; frozen C11-C manifest; stage reconstruction using a short `%TEMP%` path; PS 5.1 AST; seven atomic-I/O tests; Python 3.13 compile; exactly 18 Python tests including an isolated full 24-row/12-pair integration batch; source recheck at transaction boundary.

The transaction is 16 ADD_ONLY destinations. It requires existing destination parents and absent destinations, rechecks each path immediately before creation, writes a durable append-only journal and uses same-directory short temporary names followed by non-overwriting `File.Move`. Rollback is permitted only for this uncommitted ADD_ONLY transaction and only when a destination still matches the exact package postimage.

After all adds, the installation receipt and journal become immutable. The optional explicit `-ExecuteBatch` launches the E5 coordinator in a separate process with dedicated stdout/stderr files and immediate exit-code capture. The runner result path is prevalidated before launch; its final receipt uses `CreateNew`. A batch failure after install commit never rolls back the installed payload. Any BatchId emitted after reservation is consumed and may not be reused.

## Lessons retained

- Keep PowerShell source ASCII-only and BOM-free; always run `Parser.ParseFile` under Windows PowerShell 5.1.
- Do not use `$Args` as a variable; it is an automatic PowerShell variable.
- Do not split `else` into a later interactive submission.
- Never use `Tee-Object -FilePath` and `-Variable` together.
- Do not pipe native stderr into a terminating PowerShell pipeline for unittest; capture stdout/stderr separately with `Start-Process -Wait -PassThru`.
- Assign the child exit code immediately after `Start-Process` returns; read logs only after process exit. Nonempty stderr alone is not failure.
- Never invoke Git; commits are operator-managed.
- Do not print PASS after a failed child or failed validation.
- Do not retry a reserved one-shot BatchId, reinstall after a committed transaction, or overwrite an existing destination.

## Status

The E5 package is prepared and locally verified at source/test level. Native Windows PowerShell 5.1 AST/runtime acceptance and active-checkout execution are intentionally delegated to the supplied installer command; they are not claimed as completed in this build environment.
