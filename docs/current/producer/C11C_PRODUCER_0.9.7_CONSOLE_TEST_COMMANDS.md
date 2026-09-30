# C11-C Producer 0.9.7 — Current Console Commands

Run from the repository root.

## Fast Producer checks

```powershell
python .\c11c-suite\self_test.py
python .\c11c-suite\c11c-producer\self_test.py
python .\c11c-suite\c11c-producer\test_producer_gui_contract.py
```

## Current Challenge review

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\qa\c11\run_c11c_challenge_bulk_qa.ps1
```

## Historical C11-A.1 qualification

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\qa\c11\run_c11a1_challenge_bulk_qa.ps1
```

Use the historical A1 runner only for the explicit qualification/compatibility gate.

## Challenge production

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\prototypes\c11c_bulk\run_c11c_challenge_production.ps1 `
  -ChallengeId CHALLENGE_001 `
  -Seed 12345 `
  -DeliveryProfile MASTER_1080
```

## Visual Loop / Drill production

Use the canonical root Loop launcher or the Suite Drill producer wrapper. Delivery profiles remain declarative and do not change mechanic truth.

## Freeze boundary

Before creating the frozen archive, rerun the complete 2.19.12 acceptance after any change to active Suite/Producer routing.
