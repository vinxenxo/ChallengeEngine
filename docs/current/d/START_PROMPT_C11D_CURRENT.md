# C11-D START PROMPT — D9.5.1 / Producer GUI Request Integration

Continue from the user's latest local tree represented by `ChallengeEngineV01_STATELESS_C11-D_9_4_LATEST_20261008_224201.zip` and the current workspace with D9.4 PASS.

## State

D0–D8 PASS/CLOSED; D7 FROZEN; D9.1–D9.4 PASS as real-media checkpoint. Overall D9 is ACTIVE because the five existing suite GUIs still need integration and real Windows GUI E2E acceptance. D10 is BLOCKED.

## First patch

Apply `C11D_D9.5.1_PRODUCER_GUI_REQUEST_INTEGRATION_OVERLAY_V1.zip` to the existing repo root. It updates `c11c-producer` to 0.10.0 by adding a D4 request/personalization/planning tab in the existing GUI, shared with D4.6/D4.5 canonical adapters. It does not create a sixth suite and does not revive c11c-studio.

Run:

```powershell
python .\c11c-suite\c11c-producer\self_test.py
python .\c11c-suite\c11c-producer\test_producer_gui_contract.py
python .\c11c-suite\self_test.py
.\c11c-suite\run.bat
```

After launch, manually exercise the `C11-D · REQUEST + PERSONALIZACIÓN` tab. The local repo must contain PASS/CLOSED receipts for D4.2, D4.3, D4.4, D4.6 and D4.7; otherwise the UI planning action should block and report the missing receipt rather than guessing.

## Next target

Once the Qt GUI has been exercised, D9.5.2 studies the safe way to bring the editorial values into real Challenge media. Preserve the frozen C11-C boundary and D4.8 BLOCKED status; do not claim a personalization is visible in the MP4 until a real physical render and visual evidence prove it.

## D9 later suite updates

D9.6 Catalog 0.2.0, D9.7 Config 0.2.0, D9.8 Maintenance 0.2.0, D9.9 Test 0.2.0, D9.10 common shell 0.1.5 (only if needed), followed by cross-suite lifecycle, real GUI E2E, negatives and D9 final acceptance. See `docs/current/d/D9_SUITE_INTEGRATION_PLAN_V1.md`.

## Non-negotiable boundaries

No sixth suite; c11c-studio is retired. C11-C simulation/mechanics/RNG, timing truth, C7/C9, logical 540×960 geometry and proven production behavior are immutable. `master_seed` remains NOT_ADOPTED; seed domains stay isolated; D4.8 remains BLOCKED; release authority NONE. D10 may not begin before D9 is formally closed.


## Latest handover — D9.6 Catalog overlay

Current work is D9 Suite Integration/Evolution. D9.4 is a PASS checkpoint only, not overall D9 closure; D10 is BLOCKED. Producer 0.10.0 D9.5.1 plan/personalization GUI passed user Windows interaction (plan generation works; not media rendering). D9.6 Catalog 0.2.0 overlay adds `C11-D PRODUCTS / PROVENANCE` inside the existing Catalog GUI. Apply `C11D_D9.6_CATALOG_INTEGRATION_OVERLAY_V1.zip` then run catalog self-test, GUI contract and consolidated Suite self-test. Windows Qt bring-up and reading local D9.4 manifest/media still need acceptance. Never create a sixth suite or revive c11c-studio.


## Latest handover — D9.6 Catalog overlay

Current work is D9 Suite Integration/Evolution. D9.4 is a PASS checkpoint only, not overall D9 closure; D10 is BLOCKED. Producer 0.10.0 D9.5.1 plan/personalization GUI passed user Windows interaction (plan generation works; not media rendering). D9.6 Catalog 0.2.0 overlay adds `C11-D PRODUCTS / PROVENANCE` inside the existing Catalog GUI. Apply `C11D_D9.6_CATALOG_INTEGRATION_OVERLAY_V1.zip` then run catalog self-test, GUI contract and consolidated Suite self-test. Windows Qt bring-up and reading local D9.4 manifest/media still need acceptance. Never create a sixth suite or revive c11c-studio.
