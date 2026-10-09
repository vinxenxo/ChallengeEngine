# C11-D D9.5.1 — Producer GUI Request Integration Overlay V1

## Apply

Extract this ZIP into the repository root with overwrite enabled for listed files only, e.g.:

```powershell
Expand-Archive `
  -LiteralPath "$env:USERPROFILE\Downloads\C11D_D9.5.1_PRODUCER_GUI_REQUEST_INTEGRATION_OVERLAY_V1.zip" `
  -DestinationPath "." `
  -Force
```

## Validation (Windows / PowerShell)

```powershell
python .\c11c-suite\c11c-producer\self_test.py
python .\c11c-suite\c11c-producer\test_producer_gui_contract.py
python .\c11c-suite\self_test.py
.\c11c-suite\run.bat
```

The local project must already have D4.2/D4.3/D4.4/D4.6/D4.7 `PASS/CLOSED` receipts for the new planning action. If they are absent, the GUI blocks and reports the missing predecessor rather than bypassing governance.

## Scope

- Updates the existing `c11c-producer` only (0.10.0), preserves all existing C11-C producer routes.
- Adds D4 Production Request, D4.3 editorial personalization fields, D4.6/D4.5 exact-plan parity and unique non-overwriting evidence.
- Updates the five-app Suite documentation, D9 roadmap, milestones, handover and prompts.
- Adds a 90 core + 12 personalization + 4 negative canonical integration test.
- Does NOT create a sixth suite; does NOT revive `c11c-studio`.
- Does NOT render media from the new tab; D4.8 remains BLOCKED, renderer/production/release authority NONE.
- Does NOT modify C11-C core, renderer runners, timing, RNG, geometry or existing product behavior.

## Acceptance boundary

Canonical helper tests and static contracts can pass without Qt, but **Windows GUI launch and interaction are still a required user-workstation gate**. The new request's editorial fields are not yet proven to change pixels in an MP4; D9.5.2 must address and test that bridge without bypassing D4.8 or violating frozen C11-C contracts.
