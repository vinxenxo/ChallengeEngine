# C11-E Current Authority — V29

**Date:** 2026-11-03  
**Authority:** active Windows checkout only. V29 records the successful read-only E4A discovery, the partial V3 source audit, and the V4 diagnostic finding that the legacy GUI contract test pins an obsolete application version. This revision authorizes only a test-successor validation; it does not authorize renderer activation or production promotion.

## 1. Product mission and workflow

One C11-E service for Challenge, Visual Loop and Visual Drill. Preserve C11-C generators/mechanics and existing family audio implementations. Add authorized D presentation/layout, scoped editorial values, family-correct audio, FFmpeg mux, FFprobe/audio QA and immutable run receipts.

Implement reusable service/worker through CLI first where practical, then wire the same implementation into the current low-fidelity Producer GUI as dispatcher. Both CLI and GUI execution/testing remain required during engineering. The later all-generation-through-new-GUI workflow applies only after D/E replaces C; CLI remains available for CI/compatibility.

## 2. Accepted evidence retained

- E0, E1, bounded E2 R4, E3.2, E3 GUI/audio pilot, E3 V1.3/V1.4, E3 V1.5 50/50 negative controls and supplemental recovery remain accepted within their exact scopes.
- E3 V1.5 recovery receipt SHA-256: `8e01946da3de35c05430335259a88e14f5bae1b660c6896de5d8f13c37c3fafe`; no rerun is authorized or needed.
- E3 pipeline postimage SHA-256: `46b087683a3dcb460601c925373b84e390999d44d73141328285e6c8a633ba5d`.
- E3 negative-control test postimage SHA-256: `f88e2a52ad32851de9c47526aaf1159e7814f96b2e33f8a857e0c1df6ef3512b`.

## 3. E3 closure

`E3=PASS_FORMALLY_CLOSED_TEST_ONLY`. The 50-test suite passed with zero skips. Original wrapper BLOCKED remains immutable as an evidence-packaging defect; recovery receipt verifies existing evidence without rerunning tests or media.

## 4. E4A discovery and source audit evidence

- E4A Challenge source discovery V2: `PASS_READ_ONLY`; inventory scanned 751 files, 803 matches, 111 presentation candidates, zero scan errors. No source mutation, GUI, renderer, CLI production job or media creation.
- Existing Challenge consumer path is present: `ChallengeRuntimeBridge.gd` calls `ChallengePresentationBinder.gd`; presentation path includes `C11CVisualEditorialLayer.gd` and `VisualContentPlayer.gd`. Reuse existing consumer; no parallel binder.
- Source audit V3: all 10 source hash pins passed and six of seven focused tests passed. The seventh, historical `c11c-suite/c11c-producer/test_producer_gui_contract.py`, stopped at its first assertion requiring literal `APP_VERSION = "0.11.1"` in `main.py`.
- V4 read-only diagnostic: current `main.py` SHA-256 `f0adc54de884d6d812396707cd6ced49038df0f52e4a9bc516a9ca5e6a0ddcd3`; current application version is `0.12.0-E3`. Historical GUI test SHA-256 `ce073a39db0af583ea215c66a6c5303230539e8de857505076963a46dddf4139` still expects `0.11.1`. Both target files were clean at branch `main`, HEAD `dd1a40f4df797c80ebcbfc90f0d40c55b4e186bd`. C11-C manifest SHA remained `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- D9.10 `source_revision=C11D-D9.10-PRODUCER-0.11.1` is provenance metadata and is not the Producer application's `APP_VERSION`; do not conflate them.
- V3 global audit remains `BLOCKED` until a successor contract test validates the current application version and every functional assertion. Six prior PASS results are retained and must not be rerun absent a relevant pin change.

## 5. Immediate bounded authorization

Run `START_C11E_E4A_GUI_CONTRACT_SUCCESSOR_TEST_V1.ps1`. It must revalidate the 12 source pins and Git identity, then create an ephemeral versioned successor test under the external audit output directory. The successor changes only three literals/locations in a copy: update the APP_VERSION expectation to `0.12.0-E3`, bind ROOT to the same checkout Producer directory, and update the success label. The historical test remains unchanged. Every other assertion must remain byte-for-byte identical. Run only this successor test under Python 3.13 and preserve stdout, stderr, exit code, generated test hash and transformation receipt.

`E4A static audit` stays pending until that execution passes. If a non-version functional assertion fails, retain the failure and diagnose it; do not weaken or delete it.

## 6. E4A implementation target and next gates

After static audit closure, review exact field/slot contract and prepare the minimal CLI-first integration in the existing Challenge consumer. Confirm D authority for title/subtitle/CTA and Challenge-specific `player_name`/`challenge_label`; language is metadata-only. Reserved hook/prep/final/header/footer fields and visibility switches remain disabled; title never maps to hook/CTA. Then expose the same worker/service through the current Producer GUI.

Physical Challenge A/B/C render and audiovisual review follow only after source contract and focused static checks pass. E4B Visual Loop, E4C Visual Drill, E5 determinism/seed isolation/CLI-GUI parity, E6 Smoke18, E7 Matrix101, and E8 independent acceptance/freeze/promotion remain subsequent gates. Historical C11-C production/review/test coverage must be mapped row-by-row before E8. CH_008/009 remain held pending authoritative correction of 11s declared versus 12s phase sum.

## 7. Governance

C11-C 2.19.12 remains the sole production baseline. Frozen manifest: 796,318 bytes; SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

`renderer=OFF`  
`release_authority=NONE`  
`baseline_promotion=false`  
`freeze_eligible=false`
