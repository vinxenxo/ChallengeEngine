# D0 — Start Checklist

## Entry state

**C11-C 2.19.6 CONSOLIDATED REPAIR CANDIDATE — NOT FROZEN** is the exact input baseline.

## Step 0 — prove the starting repository

```powershell
python .	ests
un_all.py
python .\c11c-suite\c11c-producer\self_test.py
python .\c11c-suite\c11c-producer	est_producer_gui_contract.py
.\c11c-suite\c11c-test
un_all.bat
```

The recorded handoff evidence is all-green final regression, C11-A.1 54/54 PASS, factory isolation PASS and Windows single Tracking Producer FINAL PRODUCT PASS.

## Step 1 — recover the nine Challenges

Create one dossier each for `CHALLENGE_001` … `CHALLENGE_009` using `D0_CHALLENGE_RECOVERY_DOSSIER_SCHEMA.md`.

## Step 2 — reconcile evidence

Identify mismatches between current source and older Challenge evidence. Record them; do not rewrite historical evidence merely to eliminate the mismatch.

## Step 3 — D0 gate

Do not implement a new mechanic, new music engine, new asset registry or broad visual rewrite during D0. D0 is inventory/recovery.

## Step 4 — D1 handoff

D1 opens only when the nine dossiers and the machine-readable repository inventory are complete and no open D requirement silently requires changing a frozen C contract.
