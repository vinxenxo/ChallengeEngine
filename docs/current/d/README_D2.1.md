# C11-D D2.1 — Declarative Asset Family Registry Overlay V2

Corrected additive overlay for `ChallengeEngineV01_STATELESS`.

## Important installation rule

The ZIP is intentionally packed with project-root-relative paths.

**Extract directly into the project root. Do not extract the ZIP into an additional folder.**

Expected after extraction:

```text
tools\c11d\d2\run_d2_1_handoff_registry.ps1
```

## Execute

From:

```text
C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS
```

run:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\tools\c11d\d2\run_d2_1_handoff_registry.ps1
```

## V2 correction

V1 failed in Windows PowerShell 5.1 when the registry builder attempted to use `Select-Object -ExpandProperty challenge_id` against `[ordered]` dictionaries stored in `ChallengeBindings`.

V2 uses direct dictionary-key access for those registry records and does not rely on `Select-Object -ExpandProperty` for them.

## Preconditions

D2.0 must already be closed with:

```text
artifacts\tests\c11d_d2\d2_0_validation_receipt.json
```

containing:

```text
result = PASS
```

## Generated outputs

```text
docs\current\d\MASTER_HANDOVER_C11D_CURRENT.md
docs\current\d\START_PROMPT_C11D_CURRENT.md
docs\history\master-prompts\c11d\MASTER_HANDOVER_C11D_PRE_D2_1_*.md
docs\history\master-prompts\c11d\START_PROMPT_C11D_PRE_D2_1_*.md
definitions\c11d\asset_families\C11D_ASSET_FAMILY_REGISTRY_V1.json
docs\current\d\D2.1_ASSET_FAMILY_REGISTRY_CONTRACT.md
artifacts\tests\c11d_d2\d2_1_validation_receipt.json
```

## D2.1 boundary

`runtime_authority = NONE`.

D2.1 is declarative evidence binding only. It does not activate runtime routing, merge assets, rename assets, or modify frozen C11-C behavior.

## Frozen C11-C reference

ZIP SHA-256: `D85425CF18C5211C8497574F4FC66202D613EACC0EC14CD4E2FEF0B24F634A32`

Tree SHA-256: `2D39B7B923B42CDC6647A4D25493B75023CDD19CEE18214BBDE1FDD295B8F256`

`build_factory.py` SHA-256: `3DB8FBC21CF0C78430018424F83A9EED5B42DF34A3908BA152F6771F0679D2A3`
