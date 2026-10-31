# C11-E — execution hygiene and assistant error log (V9)

## Mandatory controls

1. Deliver one exact ZIP/checksum and one complete Windows PowerShell 5.1 block. Verify file existence; never assume Downloads contents.
2. Before writes, verify branch, exact HEAD/parent, C11-C manifest, E0/E1/E2 receipts, live source pins, payload hashes, destination preimages/add-only state and containment.
3. Resolve native executables to one absolute existing path. `Get-Command -All` can return multiple Python app aliases; never cast a collection to one filename.
4. Record process executable, arguments, working directory, existence, full startup exception and native exit code. Capture `$LASTEXITCODE` immediately.
5. A nonzero installer/runner exit stops the sequence. Text printed manually after a thrown failure is not evidence and must never be labeled PASS/COMPLETED.
6. Failure diagnostics precede compression; verify ZIP existence, nonzero size, readable entries and SHA-256 before reporting.
7. Each physical retry uses a fresh RequestId. Preserve failed stages, partial output, AVIs/MP4s and receipts. Never overwrite them.
8. Separate static package integrity, PowerShell runtime, source tests, pair preparation, Godot, source AVI, delivery MP4, mux, FFprobe, A/B comparison and human review.
9. Protect C mechanics, RNG, frame-stream semantics, C11-C manifest and D governance. Never serialize arbitrary `FrameSnapshot.custom_data`.
10. Never accept a gate from a partial artifact or process exit alone.

## Recorded incidents

- Earlier errors retained: separated PowerShell `if/else`; assumed Downloads files; invalid `$Relative:` interpolation; verification after failed install; protected-root audit error; stale HEAD pin; path-separator guard; Python WindowsApps collision; false V4 ZIP announcement; manual false PASS after exit 1; E0 V1 archive-copy omission; E2 V5 summary/receipt `request_id` mismatch.
- **E2 V5 (2026-10-31):** 9/9 tests and pair preparation passed; runner queried missing `$Prepared.request_id` and stopped before Godot. Failure evidence SHA-256 `e33086794ef150e3f6d851d95d7752162c97e43fda0422057ddd24ec3f43d3c7`.
- **E2 V6 installer V1 (2026-10-31):** failed at first replacement because `[IO.File]::Replace` received a null backup path. Receipt SHA-256 `408fd6fa62f7e549475779621073a05e570d65b268168e4c87ce8b4f764d559e`, files applied 0/9. Runner remained V5 at SHA-256 `9340907afd4e787495be5a9d711024a8a7ab2787aa507842ea7c7ada0c198b72`. A manual “INSTALLED AND VERIFIED” message printed after the thrown failure is a false PASS; ignore it.
- **Correction V2:** non-null unique backup path; pin failed V1 receipt; archive only the verified orphan runner temp; retain/hash-check preimage backups; verify every postimage. Static package checks do not assert PowerShell runtime success.

## Publication standard

Inspect installer/runner, payload hashes, CRC, exact preimages, add-only paths, path containment and fail-fast branches. State whether runtime was actually run. Package static integrity is not runtime acceptance or render proof.
