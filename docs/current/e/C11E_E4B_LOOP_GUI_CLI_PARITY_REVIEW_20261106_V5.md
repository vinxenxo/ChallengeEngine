# E4B Loop GUI/CLI Parity Review — V5

## Populated single-request parity — accepted

`D99-GUI-439FD530F839.zip` plus `20261106T204002Z-CF365847.zip` are accepted `PASS_TEST_ONLY`. Editorial hash `283e63025fa1a4e6f185a33d81f5a3c40a6defa4a047b9b7e089f5a159a2c214`; NFC Spanish strings are exact. Earlier V1 CLI mojibake remains invalid; V2 is authoritative. Do not rerun.

## Full-family matrix parity — accepted plan-only

Combined evidence `e4b_loop_family_matrix_all.zip`, SHA-256 `6d5637b5907c971e09331b810ef48279666a702552bb30588604a410a1eadc80`, contains Windows GUI and CLI matrix reports/templates/sidecars, overlay/runner receipts and logs. GUI run `E4B_LOOP_GUI_20261106T211920Z_F9377504`; CLI run `20261106T212054Z-DE8364C4`.

- 81/81 GUI vs CLI selector/scenario rows pass.
- Independent audit directly compared nine canonical identities across all 81 cases: canonical request, editorial, plan, bridge, adapter envelope, E1 request, E1 plan, E1 intent and frozen family music profile ID — all 81/81 per field.
- Four sidecars and report self-hashes pass. Outer evidence ZIP and nested CLI ZIP CRC pass.
- Request-origin/request IDs may legitimately differ; provenance-bound envelope equality is not substituted for semantic equality.

## Encoding controls

PowerShell 5.1 source remains ASCII-only. Spanish text comes from UTF-8 evidence/template and is NFC-checked by Python. No expected Spanish strings are re-encoded inside PowerShell source. Mojibake markers and U+FFFD must fail closed.

## Scope

GUI/CLI parity proves the plan-only request path, not rendering or D4 executable materialization. D9.9 plan state is `PLANNED`; E1 fields remain `NOT_CONSUMED_E1`; family adapter remains `NOT_CONNECTED_E1`. No generator, renderer, Godot, D3 V5, FFmpeg or media.
