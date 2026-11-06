# C11-E PowerShell Runner Style Guide — V10

## PowerShell 5.1 and Unicode

1. `.ps1` source must be ASCII-only. PowerShell 5.1 can decode UTF-8 without BOM through ANSI code page.
2. Editorial/Spanish test strings belong in UTF-8 JSON or Python fixtures, never duplicated as PowerShell literals.
3. Compare Unicode codepoints and NFC against an independent fixture; reject mojibake (`Ã`) and U+FFFD.
4. For GUI/CLI parity, derive the CLI template from the saved GUI UTF-8 evidence. Change only origin/request identity; compare semantic fields/editorial hashes, not identity-specific request hashes.

## Source authority and overlays

Active checkout only. ZIPs are evidence/read-only. Verify SHA-256 pins and frozen C11-C manifest. No Git/HEAD/status/branch/.git/commit comparisons. Add-only installers preflight all payload hashes, byte counts, source preimages and destinations before the first write. Differing same-path files must stop the complete install. Never overwrite versioned docs/tests.

A D-owned Producer GUI patch must be narrow, preimage/postimage hash-gated and backed up byte-for-byte before atomic replacement. C11-C generators, family scenes, binders, Matrix, RNG and music sources remain untouched.

## Process and governance

Use `Start-Process -Wait -PassThru`; capture stdout/stderr and hashes; propagate non-zero exit codes. Receipts record source pins, run ID, input/output identities, exit codes and governance flags. Keep preparation runners free of renderer/media. Set `renderer=false`, dispatch/production/media false and `release_authority=NONE` explicitly.
