# E4B Loop GUI/CLI Parity Review — V4

## Accepted populated parity

`D99-GUI-439FD530F839.zip` and active-checkout V2 runner evidence `20261106T204002Z-CF365847.zip` are accepted `PASS_TEST_ONLY`. The exact NFC values are retained across GUI and CLI; editorial hash is `283e63025fa1a4e6f185a33d81f5a3c40a6defa4a047b9b7e089f5a159a2c214`. The earlier V1 CLI mojibake remains invalid for populated parity and must not be rerun.

## Full-family GUI/CLI matrix path

- A new diagnostic button is added to the existing D9.9 Producer tab. It executes the matrix through the same canonical D9.9/D9.10/E1 helper used by the CLI, using current GUI values as `matrix_request_template.json`.
- The CLI runner consumes the exact GUI-exported template and its 81-row matrix report, runs the same 27 grammar × 3 seed cases, and requires equality of selection, four editorial values/hash, seed scenario and family music profile for each row.
- Request/plan/intent identity hashes may vary by generated request ID/origin; they are not compared as if they were editorial identity.
- Windows GUI and CLI matrix evidence remain pending until both runs complete and are independently audited.

## Encoding boundary

PowerShell 5.1 runner source remains ASCII-only. Spanish editorial values live in GUI widgets and UTF-8 JSON; Python performs Unicode/NFC comparison. No expected strings are duplicated in PowerShell source.
