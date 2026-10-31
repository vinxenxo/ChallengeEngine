# C11-E E2 V6 — V2 installer remediation and retry authority

## V1 installer failure

The first V6 remediation package failed during its first replacement before any of the nine payloads were applied. Windows PowerShell 5.1 called `[IO.File]::Replace($Temp, $Destination, $null)`; .NET rejected the null backup path. The receipt is pinned by the V2 installer: `C:\Users\vinxe\Documents\C11E_E2_V6_FIX_20261031_105922\C11E_E2_V6_FIX_RECEIPT.json`, SHA-256 `408fd6fa62f7e549475779621073a05e570d65b268168e4c87ce8b4f764d559e`, status `FAILED_PARTIAL_OR_NONE`, files 0/9. The live E2 runner remains the V5 preimage SHA-256 `9340907afd4e787495be5a9d711024a8a7ab2787aa507842ea7c7ada0c198b72`.

## V2 installer design

1. Repeat checkout identity, parent, C11-C manifest, E0 receipt, V1 failure receipt, runner/README exact preimages, four E2 source pins, payload size/hash, path containment and add-only preflights before writing.
2. Find exactly one orphan temp beside the runner matching `run_c11e_e2_ch001_ab.ps1.c11e-v6-*.tmp`; require its SHA-256 to equal the intended V6 runner postimage. Copy and hash-verify it into a fresh Documents receipt directory before deleting that exact temp. Unknown/multiple temp files cause a stop.
3. For each replacement, use `[IO.File]::Replace($Temp, $Destination, $BackupPath)` with a unique non-null backup path in the same volume. Retain and hash-check the backup against the pinned preimage. For additions, use same-directory `File.Move` after all preflights.
4. Record each successful operation immediately, preserve backups and any partial state in the receipt, then verify all nine postimages. Nonzero exit stops all later work.

The V6 runner code postimage remains SHA-256 `33186f24d6a531bbcbd249d647d5a2cbc5bb6cd9f116d0e8731bc29557cab6f5`. V2 does not modify the pair builder, its 9-test suite, Godot scene/script or protected C sources.

## Physical retry after install only

Only after installer exit code 0, receipt `APPLIED`, nine verified postimages, and live runner hash matching the V6 postimage may the runner be invoked. Use fresh RequestId `C11E-E2-CH001-AB-20261031-V6`. Preserve V5's failed evidence and V1 installer receipt. E2 remains unaccepted until two actual MP4s pass FFprobe and A/B pixel/body isolation, provenance checks and human visual review. No audio is part of E2.
