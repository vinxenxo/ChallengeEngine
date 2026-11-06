# E4B Loop CLI Encoding Incident — V2

## Incident

The V1 PowerShell runner contained Spanish literals in a UTF-8-no-BOM `.ps1`. Windows PowerShell 5.1 decoded them through the ANSI code page, yielding `TÃ­tulo`, `composiciÃ³n`, `patrÃ³n`. Because the expected-value fixture came from the same script bytes, its comparisons passed even though the data was wrong.

## Evidence

- V1 CLI archive `e4b_loop_overlay_cli.zip`, SHA-256 `5402a3297991958cdb21a547fd21ef8f00e2a43303e334e734df1f2fe4e2a747`: ZIP CRC and internal hashes pass, but request, D9 and E1 values are mojibake.
- GUI archive `D99-GUI-439FD530F839.zip`, SHA-256 `b933deefcf32764b9817641bd990c2879525e2931be5cbcf3cfa357574b6792f`: actual strings are correct NFC Spanish.
- The V1 run remains valid as structural D9/E1 preparation only, not populated string parity.

## Root cause and corrective control

The V2 `.ps1` is ASCII-only. A Python 3.13 helper reads the GUI-exported request as UTF-8, compares each field against an independent Unicode codepoint fixture and NFC, rejects mojibake markers, then clones the exact GUI request while changing only `request_id` and provenance/origin. It serializes UTF-8 JSON; D9.9 CLI and E1 CLI consume the same raw request. The verifier checks exact fields, GUI/CLI editorial hash, D9/E1 identities and execution locks.

Local sandbox probe against read-only V70 sources passed and reproduced GUI editorial hash `283e630...`; this is diagnostic only. Active Windows execution of V2 is still pending.

## Prevention

- ASCII-only PowerShell source for operational runners.
- Never store non-ASCII editorial fixtures in PS 5.1 source without BOM.
- Use independently encoded fixtures; don't self-compare a value decoded from the same source.
- Read/write request JSON with explicit UTF-8.
- Preserve raw inputs, receipts and stdout/stderr hashes.
