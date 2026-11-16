# E5 Cross-Family Canary — Source and Receipt Map V2 (2026-11-16)

## Static contract pins

The E5 JSON contract pins 31 source/evidence files. They include the shared E1 service, CLI, current Producer GUI wiring, GUI request mapping, request schemas, D9 shared adapters, E4B Loop stage contract, E4C Drill execution, family-specific music source/contracts, delivery/presentation profiles, the three canonical family identities, the accepted Challenge/Loop/Drill historical evidence and the frozen C11-C manifest.

PowerShell guide identity is independently pinned: `docs/current/e/C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261116_V36.md`, 65,465 bytes, SHA-256 `4f3940d50b07ccd48e30f44dbc8653a9021791d20382dbccdb7ca0d93f98f337`.

The runner unions the family-specific source identities returned by all 24 in-memory service preparations and verifies that dynamic source set before and after the bulk. The dynamic count is not hardcoded as a universal invariant; path and digest equality are.

## Receipt chain

`INSTALL_RECEIPT.json` records the committed 16-file ADD_ONLY transaction and the SHA of the immutable `INSTALL_JOURNAL.jsonl`. `BUILD_VERIFICATION.json` records the V36 path/hash, PowerShell AST, atomic 7/7, Python compile and 18/18 staged test results.

The batch folder contains one `ATTEMPT_RESERVED.lock.json`, one `PREPARE_ONLY_AUTHORIZED_ONCE.json`, `BATCH_PROGRESS.json`, `SOURCE_PINS_PRE.json`, `SOURCE_PINS_POST.json`, `PREFLIGHT_RECEIPT.json`, 12 request folders with GUI intent, CLI request/result/logs and `ROW_RECEIPT.json`, then `BATCH_RESULT.json`, `RUNNER_LAUNCH_RECEIPT.json` and `RUNNER_RESULT.json`.

`COMBINED_EXECUTION_RECEIPT.json` binds the install receipt/journal/build verification, runner result, batch result and launch receipt SHA-256 values. The install receipt and journal are never rewritten after the combined receipt is created.

## What PASS means

It proves the bounded E5 PREPARE_ONLY cross-family request/service entry canary: 24 rows, 12 service-origin pairs, A/B replay, independent seed probes C/D, family profile/binder/timebase boundary checks, stable source pins and intact governance.

It does not prove actual Qt user interaction, renderer activation, audio/video generation, FFmpeg mux/FFprobe, or complete E5 A/V acceptance. Media count remains zero; family adapter remains `NOT_CONNECTED_E1`; `release_authority=NONE`.


## Combined installer V2 correction

The V1 installer's `Write-ProgressSnapshot` ordered hashtable repeated six keys and was rejected by PowerShell 5.1 before script execution. The V1 attempt therefore did not install payload or reserve an E5 BatchId. V2 changes the package identity/installer name, removes duplicate keys, includes a saved launch wrapper, and records launcher/installer logs and separate failure receipts. The launch wrapper verifies the external ZIP sidecar and ZIP member paths before extracting to a new V2-only path, then AST-parses all shipped PowerShell scripts before it starts the installer.
