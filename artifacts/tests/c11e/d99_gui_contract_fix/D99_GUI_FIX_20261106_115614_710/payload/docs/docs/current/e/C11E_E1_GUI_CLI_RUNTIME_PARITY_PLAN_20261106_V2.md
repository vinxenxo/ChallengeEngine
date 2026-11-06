# C11-E E1 Producer GUI Runtime / GUI↔CLI Parity — Execution Plan V2

## Purpose

Close the remaining GUI runtime obligation for full Challenge E4A using the existing Producer application. No new GUI, module, Producer, adapter or binder is authorized or needed. The reviewed `main.py` callback `_run_d9_universal_plan` already prepares E1 from the GUI request, invokes D9 universal CLI and C11-E E1 CLI in separate processes, compares both, and writes receipts. This route is plan-only; it does not dispatch, render or create media.

## Reviewed source reference

Snapshot `ChallengeEngineV01_STATELESS_C11-E4A5B-REVIEWED_20261105.zip` (source evidence only; active checkout remains authority):
- `c11c-suite/c11c-producer/main.py`: 110,784 bytes, SHA `9685c4346cf56d3134fbf296585efbd779e5695635a249f0b85bd2c3682dac4e` (reference pin, not a Git pin).
- E1 service: SHA `348997e575d985fe153a4f433f089c5f205be5d4d8f3853baf07be917a134951`.
- E1 CLI: SHA `e7272231dca2eb730506308b092fce9b3644f7f8cfd9f2c2bbbbd1b695e82fc4`.
- D9 universal CLI: SHA `c648a3722299b4700a9b74d1cabc6cac1fa48ad6275497ae8073bc07f442bb54`.
- D9 resolver `9ad2adbf...`; GUI request adapter `0e95109f...`; editorial model `5c575be1...`.

If the live `main.py` or other source differs from the reviewed reference, do not block on Git or blindly apply a snapshot. Inspect the current live source and confirm that the callback and no-dispatch boundaries still match before using the UI. No source change is part of this test.

## Exact operator path

1. Start the existing Producer from the active checkout (`c11c-suite\c11c-producer\run.bat` or the normal project launcher).
2. Open tab `C11-D · EDITORIAL UNIVERSAL (D9.9)`.
3. Set Content Type = Challenge; Family/mechanic = `parking_v2`; Variant = `CHALLENGE_004`; Mode = `REVIEW · PLAN`.
4. Gameplay seed = `314159`; Music seed = `840001`; Delivery = `REVIEW_720`; Presentation profile = `social_default_v1`; Variation index = `0`; Audio enabled = ON. There is no Hook/countdown checkbox in this phase; E1 preserves its existing Challenge default internally.
5. Keep the existing editorial controls/allowlist. Keep the existing personalization control enabled so all established editorial inputs remain wired and visible. Leave title, subtitle, CTA, player name and challenge label blank; retain the current language value. Do not add per-field omission toggles. D9.8 still emits every canonical field key for the selected family; an empty optional value is represented as `UNKNOWN` per the existing D9.8 rule, not by dropping the field. This is a value normalization only; every canonical key remains present.
6. Click only `RESOLVER + PLAN EDITORIAL / PUENTE (SIN RENDER)`. Do not click D9.14 certification preflight or the E3 audio pilot button.
7. In outputs, inspect `C11-E E1` and `GUI ↔ CLI` parity views. Confirm PASS and fail-closed/renderer-off fields.

## Why this proves the right thing

In `_run_d9_universal_plan`, the GUI calls `prepare_c11e_production_intent(... request_origin="GUI")`, evaluates the D9 plan, then calls `universal_producer_cli.py` and `c11e_production_cli.py` with the same canonical request. It compares:

- E1 semantic intent/request/editorial/plan hashes;
- selection and effective editorial;
- presentation options and independent seed domains;
- preserved GUI and CLI origins;
- identical fail-closed execution boundary;
- D9 canonical request, plan, bridge planning record and D-only adapter envelope.

The callback writes its own evidence under `artifacts/tests/c11d_d9/producer_universal/D99-GUI-<ID>/`.

## Required uploaded evidence

Upload the complete generated run folder as a ZIP. It should include at least:
- `c11e_gui_cli_parity.json` — status PASS and all E1 checks true;
- `gui_cli_parity.json` — D9 bridge/adapter parity PASS;
- `c11e_production_intent.json` and `c11e_production_intent_receipt.json` — `PASS_E1_PREPARATION_ONLY`;
- `producer_universal_receipt.json` — `PASS_BRIDGE_PLANNING_ONLY`;
- `cross_suite_lifecycle_receipt.json` — lifecycle validation;
- `request.json`, `d9_request.json`, `canonical_request.json`, `editorial_resolution.json`, `universal_plan.json`, bridge and adapter JSON.

Confirm every boundary: `renderer=false`, `renderer_dispatch_invoked=false`, `renderer_input_emitted=false`, `production_execution=false`, `media_created=false`, `release_authority=NONE`, D4.8 BLOCKED. No media should be generated.

## Acceptance

PASS only if E1 GUI/CLI and D9 GUI/CLI parity both pass, lifecycle validates, seed domains remain distinct and the boundary remains fail-closed. This closes the GUI parity obligation for the tested Challenge fixture only. It does not authorize production or infer all possible GUI configurations; broader scenarios belong to E5/Smoke18.


## D99 request correction (V1 surgical source patch)

The GUI callback previously built an E1-owned `presentation_options` key and then copied/stripped it for D9.9. The operator reported a strict resolver error. The supplied D22A8281E993 artifact itself has PASS receipts and shows `request.json` with the key but `d9_request.json` without it; it is therefore evidence of a successful run, not the failing trace. To make the boundary unambiguous and remove the not-yet-approved UI option, the patch removes the checkbox and never serializes this key from `main.py`. E1 defaults `show_hook_countdown=true` for Challenge when the option is absent. The D9.9 schema/resolver and E1 service remain unchanged.

Do not modify canonical editorial field lists. D9.8 always returns the complete allowlisted `editorial` object: six fields for Challenge and four shared fields for Loop/Drill. Empty optional text normalizes to `UNKNOWN`; this is the existing canonical absence marker. The patch's focused tests assert these key sets and the D9.9/E1 boundary.


## Editorial controls: explicit scope boundary

Do not implement field-by-field optional controls now. Keep all established GUI editorial fields connected to `editorial_profile` / `production_override`; the request always includes these containers. When values are blank, D9.8 retains each canonical key and applies `UNKNOWN` as its currently approved empty-string normalization. Any future field-selection UX is out of scope for this patch.
