# C11-E E4A — D99 Challenge GUI/CLI Parity Acceptance V1

**Date:** 2026-11-07  
**Evidence source:** `ChallengeEngineV01_STATELESS-C11-E-SNAPSHOT-NIGHTLY-V80.zip`  
**Snapshot SHA-256:** `98a370a6017f00a6d01b690bd5450284758a14a13b00084c97b4d13bea01bdde`

## Disposition

`E4A_D99_GUI_RUNTIME_PARITY=PASS_TEST_ONLY`.

The requested post-correction GUI evidence already exists in V80. The operator does **not** need to locate or rerun the Producer GUI fixture.

Evidence folder:

`artifacts/tests/c11d_d9/producer_universal/D99-GUI-37559C528640/`

The run was recorded on 2026-11-06 at 12:36:48–12:36:50 local time. The hash-gated GUI correction V2 receipt completed at `2026-11-06T12:34:49.6220607+01:00`, approximately two minutes earlier. This ordering, the installed patch receipt, the content of the generated request and the current V80 source are mutually consistent with a post-correction run. The D99 parity files do not themselves contain a `main.py` source hash, so source-to-run binding is chronological/evidence-correlated rather than a direct per-run executable pin.

## Exact fixture recovered

- `request_id`: `D99-GUI-37559C528640`
- Content: Challenge / `parking_v2` / `CHALLENGE_004`
- Mode: `REVIEW`
- Gameplay seed: `314159`
- Music seed: `840001`
- Delivery: `REVIEW_720`
- Presentation profile: `social_default_v1`
- Variation index: `0`
- Audio enabled: `true` (the approved parity fixture requires this; this does not mean an audio engine or media render ran)
- Personalization enabled: `true`

`request.json` and `d9_request.json` are byte-identical; both SHA-256 values are `ee8cf2e0c98febea8e47fbecbb8ee0feaf2bc9ff7e5016d0537c3963f4952aa9`. Neither contains `presentation_options`.

## Acceptance receipts

| Artifact | SHA-256 | Result |
|---|---|---|
| `c11e_gui_cli_parity.json` | `ba9553be408a75838ce3d77715f6790a1f3ddefd49e817a71f000d6fb624c8d6` | `PASS`; all 11 parity/fail-closed checks true |
| `gui_cli_parity.json` | `4a9d728e2b0f5773e1be6a1469fc45477ae1a442aa1ffe8fd01f8c2cc86746f5` | `PASS`; canonical request, plan, bridge and adapter agree |
| `c11e_production_intent_receipt.json` | `385bb84a629d927e21ba6d1dcd1f85a66262aa53a2f8b466fd13dd4b26f89296` | `PASS_E1_PREPARATION_ONLY` |
| `producer_universal_receipt.json` | `ffb65160b5c60b8d91bdd12bfbb1ffb4a184a3604f5d4ed4758fab0874f110ff` | `PASS_BRIDGE_PLANNING_ONLY`; D4.8 BLOCKED |
| `cross_suite_lifecycle_receipt.json` | `4bbd99900b76b6d583c82676972fa79387eb49c44f766bd63fbcc8f0ea4a52ad` | `PASS_PLAN_ONLY`; all five lifecycle stages pass |
| `canonical_request.json` | `5cbc1cb4b22c2ff491773649875d0088c540944ae27f66374c458bb06cda3a49` | Six canonical Challenge editorial keys retained |
| `c11e_production_intent.json` | `21719dce5650344db6504ca9e639887a44bd2096941b0184366044023997ffaa` | E1 prepared intent |

The E1 intent contains the internal default `request.presentation_options.show_hook_countdown=true`. That is expected: it is an E1-internal default. It is not serialized into the raw D9.9 `request.json` or `d9_request.json`, and the GUI no longer exposes the premature Hook/countdown control.

The canonical editorial result contains all six Challenge fields (`title`, `subtitle`, `call_to_action`, `language`, `player_name`, `challenge_label`); blank text values normalize to `UNKNOWN`. This run does not implement field-by-field key omission.

## Source correction evidence

V2 source-fix receipt:

`artifacts/tests/c11e/d99_gui_contract_fix/D99_GUI_FIX_20261106_123445_597/C11E_D99_GUI_CONTRACT_FIX_RECEIPT.json`

Receipt SHA-256: `833846ea248fe762219b91912ccdcf39c7c959caa06acf3ebc0af2398e036245`.

- Result: `PASS_SOURCE_PATCH_AND_TARGETED_TESTS`.
- PowerShell: 5.1.26100.9818.
- `main.py` exact patch preimage SHA: `9685c4346cf56d3134fbf296585efbd779e5695635a249f0b85bd2c3682dac4e`.
- V2 patch postimage SHA: `4141072659f307468900c1cfb09774479abc6c10abae6ae638a11192cfcd04e6`.
- Verified backup SHA equals the preimage.
- E1 service pins unchanged; E1 tests 19/19; D9.9 matrices and negative cases passed; focused GUI/editorial tests 3/3.

The later V80 `main.py` includes the subsequent shared-service integration and has SHA-256 `ad88ac99a4582a6a470b8885425144ab7265188c3771ed4c48d8857c43343c55`. Inspection confirms the GUI request constructor still does not emit `presentation_options`; the removed Hook/countdown GUI control is absent. This later source hash is not the D99 patch receipt's postimage because E4B subsequently extended the same Producer module.

## Governance and scope

The D99 run proves one actual Challenge GUI fixture and its E1/D9.10 GUI↔CLI parity. It does not prove every possible GUI state or authorize execution.

All receipts remain fail-closed:

- `renderer=false`
- `renderer_input_emitted=false`
- `renderer_dispatch_invoked=false`
- `production_execution=false`
- `media_created=false`
- `release_authority=NONE`
- D4.8 remains `BLOCKED`

**E4A disposition:** the previously documented final GUI parity obligation is now satisfied. Combined with the separately accepted E4A.6 live-root test and E4A.7 D-composited A/V test plus user visual/audio review, E4A is `PASS_TEST_ONLY`. It is not production activation, D4.8 clearance, D10 promotion or release approval.
