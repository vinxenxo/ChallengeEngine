# E4B Loop GUI/CLI Parity Review — V3

## GUI evidence accepted

`D99-GUI-439FD530F839.zip` SHA-256 `b933deefcf32764b9817641bd990c2879525e2931be5cbcf3cfa357574b6792f`. Correct values (NFC):

- Title: `Título editorial Loop — composición armónica en movimiento`
- Subtitle: `Explora el patrón geométrico, observa sus ciclos y descubre cómo evoluciona la forma`
- CTA: `Guarda este loop y comparte tu patrón favorito`
- Language: `es`

GUI editorial hash: `283e63025fa1a4e6f185a33d81f5a3c40a6defa4a047b9b7e089f5a159a2c214`. GUI internal D9/E1 parity and lifecycle five-stage PASS_PLAN_ONLY; no renderer/media/dispatch.

## CLI V1 finding

`e4b_loop_overlay_cli.zip` SHA-256 `5402a3297991958cdb21a547fd21ef8f00e2a43303e334e734df1f2fe4e2a747` is structurally intact and D9/E1 exit 0, but the serialized editorial contains mojibake because PS 5.1 decoded UTF-8-no-BOM `.ps1` literals via ANSI. V1 is not accepted for populated parity. No resolver defect is indicated.

## CLI/GUI V2 recovery

V2 reads the existing GUI `request.json` through Python UTF-8. It validates the four exact Unicode/NFC fields and supporting GUI canonical request, E1 receipt, D9 plan, bridge/adapter identity and lifecycle. It clones the raw request to CLI provenance, new request ID, and writes UTF-8 JSON. D9.9 and E1 CLI both consume this same JSON. It requires:

- each GUI and CLI field exact-equal;
- D9.8 editorial hash same as GUI;
- D9/E1 request and plan hashes equal within the CLI run;
- no mojibake and Unicode NFC round-trip;
- seed, family music and all governance constraints preserved.

The sandbox diagnostic against a read-only V70 source copy returned `PASS_GUI_CLI_EDITORIAL_PARITY_ONLY` and matched GUI editorial hash. This is not an active Windows run. Run V2 in the user's checkout; do not rerun GUI.
