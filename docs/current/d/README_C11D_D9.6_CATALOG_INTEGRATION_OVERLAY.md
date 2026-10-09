# C11-D D9.6 — Catalog Integration Overlay V1

**Existing app updated:** `c11c-suite/c11c-catalog` 0.2.0. No new suite or application.

## Apply

```powershell
Expand-Archive `
  -LiteralPath "$env:USERPROFILE\Downloads\C11D_D9.6_CATALOG_INTEGRATION_OVERLAY_V1.zip" `
  -DestinationPath "." `
  -Force
```

## Verify

```powershell
python .\c11c-suite\c11c-catalog\self_test.py
python .\c11c-suite\c11c-catalog\test_catalog_gui_contract.py
python .\c11c-suite\self_test.py
```

Then open the existing `c11c-suite\run.bat` and launch **CATALOG**. Confirm the original Artifact Browser remains and the new **C11-D PRODUCTS / PROVENANCE** tab appears. On a workspace with D7.3/D7.4 and D9.4/D9.5.1 evidence it should list only receipt-governed records.

## Limits

D7.3 rows are canonical plan intents, not rendered products. D9.5.1 rows are plan-only. D9.4 media is pilot validation evidence only, not D8 release eligible. Copying a plan replay command only copies it; Catalog never executes production. Renderer/production execution=false, release_authority=NONE.
