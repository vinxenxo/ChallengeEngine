# C11-E Execution Backlog — V45

**Date:** 2026-11-06. E4A.6 visual and E4A.7 D-composited A/V technical subgates are now PASS_TEST_ONLY. Full Challenge E4A remains open only for the two human/GUI obligations below.

## Completed — E4A.6 visual/reserved bands

Recovery V1.2 receipt SHA `3279011fa16479d4901c5b271463707a437ce7458d306c1667ab222cb1603980`. User visual review PASS. Silent D-composited MP4 SHA `841b03531301c7e70c0e09ce3e9f536241d2072a87792e099ed7a955bef8c52f`; 720×1280/30 FPS/450 frames/15 s/H.264 High/yuv420p/TV/zero audio. Pixel audit: inactive bands 12/12 PASS (RGB max tolerance 3); active HOOK/CTA 4/4 PASS. No rerender; do not repeat V2 tests, Godot, Movie Maker or recovery.

## Completed — E4A.7 D-composited Challenge A/V

- Execution ZIP `RUN_20261106T070808Z-62F31F9C.zip`; SHA `ad4024cc6caa3b9140a284390b852c76f3dcd5d50d88cf03813d6bb4e374d293`; 268 entries, ZIP CRC PASS.
- Receipt SHA `102cf07a0b8920318c3ba211a3bd4374c3e080018486363d701f81e65613aaa0`; report SHA `efb0f1a9245d3fce15bf48041c8972e90f6874d308fa99340afb5c731f94403a` matches receipt. `SHA256SUMS.txt` validates 267/267 files; 55/55 process exit codes are zero.
- D3 V5 raw A/B identical, C differs; D3.3 master A/B identical, C differs; 48 kHz stereo/15 s delivery masters; QA −14.0 LUFS, true peak −6.4 dBTP A/B and −6.1 C, LRA 0.1 LU (below 7 LU max), mono compatibility/no clipping PASS.
- A/B/C decoded AAC: A=B, C differs. All 3 final MP4s have H.264 High 720×1280/30 FPS/450 frames/15 s + AAC-LC stereo 48 kHz; 0.000 s A/V start/end drift. H.264 elementary SHA `6164e47adc8fd09cef3eea3780b77fbced007acba17a6939de7437bcf485ed5e` is identical to source across A/B/C. MP4 A/B byte-identical (SHA `03f5f9...`); C SHA `41b9a3...`.
- User visual disposition PASS; operator listening A/B/C = PASS (user-confirmed). E4A.7 intents are `request_origin=TEST`; they do not by themselves prove GUI runtime parity.
- Do not rerun E4A.7 or visual capture.

## Completed — operator A/B/C listening review

User explicitly confirmed `A, B y C: OK / PASS` on 2026-11-06. Do not repeat listening package or audio tests unless a new defect is reported.

## Immediate P0 — surgical D99 GUI request contract correction

The user reported `Unknown universal request field(s): presentation_options`. D9.9's strict schema does not list this field. The D22A8281E993 evidence folder that was uploaded has PASS receipts (E1 and D9 bridge/CLI parity); it records `presentation_options` in `request.json` but not in `d9_request.json`, so it does not capture the reported failure. Remove the premature GUI checkbox and all construction of this option from `c11c-suite/c11c-producer/main.py`. Do not change `universal_producer.py`, the D9.9 schema or the E1 service. E1's existing default keeps Challenge hook/countdown true when omitted. Keep the six Challenge editorial keys and four Loop/Drill shared keys in canonical output; empty D9.8 values normalize to `UNKNOWN` and must not remove their keys.

Run the one hash-gated D-owned patch `APPLY_C11E_D99_GUI_EDITORIAL_CONTRACT_FIX_V1.ps1`. It verifies the active source preimage, C11-C manifest and E1/D9 supporting pins, runs the 19 E1 service tests, 3 focused GUI/editorial contract tests and D9.9 producer matrix (9 Challenge + 32 Loop selectors + 20 Drill variants; three process parity representatives; 20 negatives), then modifies only the D9 Producer `main.py` and adds one focused test plus versioned documents. No renderer, dispatch or media.

## Immediate P1 — existing Producer GUI runtime / E1 GUI↔CLI parity

Use the existing `c11c-suite/c11c-producer/main.py`, tab `C11-D · EDITORIAL UNIVERSAL (D9.9)`. This callback already invokes the D9 canonical CLI and the C11-E E1 CLI, then compares canonical request, editorial, plan, bridge, adapter and E1 semantic identity. No new GUI, runner, producer, module or binder is needed.

Set Challenge / `parking_v2` / `CHALLENGE_004`; REVIEW; gameplay seed 314159; music seed 840001; `REVIEW_720`; `social_default_v1`; variation 0; audio enabled; no hook/countdown checkbox or serialized `presentation_options`; personalization enabled; leave title/subtitle/CTA/player_name/challenge_label blank and retain the current language value; no editorial overrides. Click only `RESOLVER + PLAN EDITORIAL / PUENTE (SIN RENDER)`. Do not click D9.14 or the E3 audio pilot button. The flow is preparation only and must create no media or renderer dispatch.

Evidence appears in `artifacts/tests/c11d_d9/producer_universal/D99-GUI-<ID>/`. Collect the complete per-run folder as a ZIP. Expected PASS artifacts: `c11e_gui_cli_parity.json` (all E1 checks true), `gui_cli_parity.json` (D9 bridge parity PASS), `c11e_production_intent_receipt.json` (`PASS_E1_PREPARATION_ONLY`), `producer_universal_receipt.json` (`PASS_BRIDGE_PLANNING_ONLY`), `cross_suite_lifecycle_receipt.json`, request/intent/plan and hashes. Require renderer/dispatch/media false and `release_authority=NONE`.

## Full E4A closure rule

Full E4A closes only after E4A.6 and E4A.7 technical receipts, user A/B/C listening + sync review (already PASS), and existing Producer GUI/E1/D9.9 parity evidence all PASS. A failed GUI/parity test is investigated only at the failed subgate; never rerun the completed A/V worker unless its input/source pin changed or a concrete defect is identified.

## After full E4A

E4B Loop (family binder/grammar/timeline/music preserved) → E4C Drill (phase/END_CTA/binder/music preserved) → E5 (cross-family determinism, seed isolation, profile non-leakage, GUI/CLI) → E6 Smoke18 → E7 Matrix101 → E8 full historical C-to-E mapping, independent acceptance, freeze and separate promotion. CH_008/009 remain held (11 s declared vs 12 s phase sum; 99 provisional runnable).

C11-C 2.19.12 remains production authority. No changes to protected source, C11-C mechanics/RNG/binders/timelines/core audio, manifest or production locks. No Git invocation by runners.


## Editorial payload non-regression

The D99 patch must not narrow the editorial payload. Keep the established text inputs and always include the `editorial_profile` and `production_override` objects. D9.8 emits all six Challenge keys and all four Loop/Drill shared keys. Blank optional text normalizes to `UNKNOWN`; no key is deleted. The existing global personalization checkbox remains; do not invent per-field selection controls.
