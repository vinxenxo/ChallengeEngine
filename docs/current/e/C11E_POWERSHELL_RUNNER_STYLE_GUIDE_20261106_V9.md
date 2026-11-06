# C11-E PowerShell Runner Style Guide — V9

## PowerShell 5.1 and Unicode

Windows PowerShell 5.1 may decode UTF-8 source without BOM using the active ANSI code page. Non-ASCII literals can become mojibake while same-source comparisons still pass.

1. Keep `.ps1` source ASCII-only. If non-ASCII source is unavoidable, use UTF-8 BOM and validate on PS 5.1.
2. Do not embed Spanish/editorial fixtures in PowerShell. Read GUI JSON through Python `encoding='utf-8-sig'`; serialize explicit UTF-8.
3. Compare codepoints/NFC to an independent fixture; reject mojibake markers and U+FFFD.
4. Derive CLI request from accepted GUI UTF-8 JSON, change only request ID/provenance, and compare exact values plus editorial hash. Request hashes may differ by identity/origin.
5. Derive test counts from captured logs; verify exit code and stdout/stderr SHA-256.

## Source authority and overlays

Active checkout only. ZIPs are evidence/read-only. Verify SHA-256 pins and frozen C11-C manifest. No Git/HEAD/status/branch/.git/commit comparisons. Add-only installers must preflight all payload hashes and destinations before the first write; identical files may be reused, differing same-path files must stop the complete install. Never overwrite versioned files.

## Process and governance

Use `Start-Process -Wait -PassThru`; capture stdout/stderr and hashes; propagate non-zero exit codes. Keep preparation runners free of renderer/media. Receipts record source pins, run ID, inputs/outputs, exit codes and governance flags. `renderer=false`, dispatch/production/media false and `release_authority=NONE` remain explicit.
