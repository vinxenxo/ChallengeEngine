# C11-E PowerShell Runner Style Guide — V11

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

## Process / receipts

- Use `Start-Process -Wait -PassThru`; capture stdout/stderr and hashes; propagate nonzero exit codes.
- Receipts record run IDs, source pins, evidence input hashes, output hashes, process exit codes, governance booleans and `release_authority=NONE`.
- Read-only audit runners must not write into source directories except their unique evidence output root; never call Git, generators, Godot, D3 V5, FFmpeg, renderer or media.
- Keep no more than one new GUI/CLI entrypoint pair; both call the same shared helper.
