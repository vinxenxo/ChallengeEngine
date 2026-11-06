# C11-E D99 GUI / D9.9 presentation-options contract incident — V1

**Date:** 2026-11-06.

## Operator report

The existing Producer button `RESOLVER + PLAN EDITORIAL / PUENTE (SIN RENDER)` displayed `Unknown universal request field(s): presentation_options`. The user clarified that no Hook/countdown toggle is required in the present GUI stage and that all approved editorial fields must remain wired; future optional selection should be handled by a future GUI, not by removing fields from the canonical payload.

## Uploaded evidence reconciliation

`D99-GUI-D22A8281E993.zip` contains `c11e_gui_cli_parity.json=status PASS`, `gui_cli_parity.json=status PASS`, `c11e_production_intent_receipt.json=status PASS_E1_PREPARATION_ONLY` and `producer_universal_receipt.json=result PASS_BRIDGE_PLANNING_ONLY`. In that artifact `request.json` includes `presentation_options`, but `d9_request.json` removes it and `canonical_request.json` has no such key. This archive therefore records a successful run; it does not reproduce the reported exception. Its success must not be relabeled as a failure.

## Root contract and minimal correction

- D9.9 `C11D_UNIVERSAL_PRODUCER_REQUEST_D9_9_V1.json` has a strict top-level allowlist and does not include `presentation_options`. Do not extend or loosen it for an E1 UI convenience field.
- E1 `prepare_c11e_production_intent` already copies the input, removes E1-only `presentation_options` before invoking D9.9, and supplies Challenge's existing default `show_hook_countdown=true` when omitted. Keep this service unchanged.
- The Producer GUI should not create a Hook/countdown checkbox or serialize the E1 option in its raw universal request. The V1 patch changes only the existing D-owned `c11c-suite/c11c-producer/main.py`: remove that checkbox, its enablement block, and the raw-request key; serialize the same canonical D9.9 request directly for D9 CLI. No new UI, module, binder or producer.
- Do not change `tools/c11d/d9/universal_producer.py`, D9.9 request schema, E1 service, protected C11-C or D3 V5.

## Editorial field invariant

D9.8 model is authoritative. Challenge canonical editorial output always has six keys: `title`, `subtitle`, `call_to_action`, `language`, `player_name`, `challenge_label`. Visual Loop and Visual Drill each keep four: `title`, `subtitle`, `call_to_action`, `language`. Empty optional strings normalize to `UNKNOWN` under `inheritance_policy.empty_optional_string=NORMALIZE_TO_UNKNOWN`; the keys remain present. Do not introduce a field-selection/optional-key layer now. Do not interpret UNKNOWN as permission to omit fields from the canonical result.

## Verification performed on reviewed source snapshot

Source reference `ChallengeEngineV01_STATELESS_C11-E4A5B-REVIEWED_20261105.zip` has `main.py` 110,784 bytes / SHA-256 `9685c4346cf56d3134fbf296585efbd779e5695635a249f0b85bd2c3682dac4e`. Prepared postimage SHA-256 `4141072659f307468900c1cfb09774479abc6c10abae6ae638a11192cfcd04e6`, 110,183 bytes. Supporting pins: E1 service `348997e575d985fe153a4f433f089c5f205be5d4d8f3853baf07be917a134951`; D9 resolver `9ad2adbf54946f2225ae2ed36b88abfc5717387f2ff03bbed684aa8bd32d87d1`; D9 request schema `342a61338c80a2f1616e8e9f38986bd90f410257c0e321f99840380fb0fd804b`; D9 editorial model JSON `50655c82521a353f1db6920f4d099cad92452ae369251f9fbde45cbaee4e8c53`. These are content pins only; no Git checks.

Focused local verification on the reviewed snapshot: E1 production-service tests 19/19 PASS; D9.9 producer matrix Challenge 9/9, Loop selectors 32, Drill variants 20, CLI parity 3/3, negative cases 20/20 PASS; new GUI/editorial contract tests 3/3 PASS. These tests ran against the reviewed source snapshot in the build workspace; the active Windows checkout still needs the hash-gated patch execution and one runtime GUI retry.

## Patch boundaries

Allowed writes: D-owned `c11c-suite/c11c-producer/main.py` and new `tools/c11d/d9/test_e1_gui_editorial_contract.py`, plus versioned C11-E docs/prompts. No Git, renderer, dispatch, media, C11-C generator/mechanics/shared layer, D9 resolver/schema, E1 service or D3 engine modifications. Stop before writes if the active `main.py` preimage or supporting pins differ.

## Documentation overlay collision

The operator also ran `INSTALL_C11E_E4A7_POSTRUN_DOCS_V2.ps1`. Its add-only preflight stopped at `docs/current/e/C11E_CURRENT_AUTHORITY_20261106_V69.md` because that path already existed with different bytes. This is a correct safety stop: the installer wrote no documents. Do not rerun or weaken V2. The D99 correction runner carries a distinct versioned document set (Authority V70, Index V30 and subsequent versions) and preflights all 14 destinations before any source change.

## Closure condition

After applying the patch, restart the existing Producer and click only the plan-only RESOLVER button once. Confirm `request.json` and `d9_request.json` contain no `presentation_options`; canonical editorial output retains the family-appropriate keys; E1/D9.9 parity receipts PASS; renderer/dispatch/media false; `release_authority=NONE`. Full E4A closes only after this PASS.
