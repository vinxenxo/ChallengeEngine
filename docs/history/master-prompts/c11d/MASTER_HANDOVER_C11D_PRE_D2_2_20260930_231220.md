# C11-D MASTER HANDOVER

## Current phase

C11-D â€” Declarative Challenge recovery, visual/editorial parity, reusable asset families, production and provenance pipeline.

## Current checkpoint

D2.1 â€” Declarative Asset Family Registry / Evidence Binding
STATUS: ACTIVE

## Frozen reference baseline

C11-C 2.19.12 is FROZEN and IMMUTABLE.

Frozen ZIP:
ChallengeEngineV01_STATELESS_C11-C_2.19.12_FROZEN_20260930_175709.zip

Frozen ZIP SHA-256:
D85425CF18C5211C8497574F4FC66202D613EACC0EC14CD4E2FEF0B24F634A32

Frozen tree SHA-256:
2D39B7B923B42CDC6647A4D25493B75023CDD19CEE18214BBDE1FDD295B8F256

build_factory.py SHA-256:
3DB8FBC21CF0C78430018424F83A9EED5B42DF34A3908BA152F6771F0679D2A3

## Closed checkpoints

D0 â€” CLOSED / PASS
9/9 Challenge dossiers recovered and evidenced.

D1 â€” functional checkpoints complete.
D1.0 source audit: PASS
D1.1 visual/editorial mapping: PASS
D1.5 canonical Instagram Reels layout profile established
D1.6 contract regression: 5/5 PASS
D1.7 declarative Challenge mapping: 9/9 PASS

D2.0 â€” CLOSED / PASS
15 logical C6 assets audited.
9/9 Challenges audited.
9/9 D0 dossiers discovered.
2 explicit asset family groups.
5 Challenges remain UNKNOWN for asset family.
27 asset references.
0 unresolved asset references.
0 family promotions.
0 family merges.
0 protected C11-C source modifications.

## D2.0 evidence

Audit:
artifacts\tests\c11d_d2\d2_0_asset_family_audit.json

Contract:
docs\current\d\D2.0_ASSET_FAMILY_AUDIT_CONTRACT.md

Receipt:
artifacts\tests\c11d_d2\d2_0_validation_receipt.json

## D2.1 active scope

Build an additive declarative asset-family registry from the D2.0 audit evidence.

The registry is an evidence-binding layer, not runtime activation authority.

Rules:
1. Preserve explicit asset_family and asset_family_version evidence.
2. Preserve UNKNOWN where evidence is insufficient.
3. Do not infer family membership from filenames alone.
4. Do not collapse assets solely because SHA-256 values match.
5. Preserve current Challenge references and D0 provenance separately.
6. Historical evidence remains provenance/reference until explicitly promoted.
7. Do not modify simulation, mechanics, RNG, SimulationResult, winning_frame, close_calls, WinningFrameDetector, RenderedFrameStream, C7, C9, frozen C11-C presentation, or frozen C11-C production.

## Explicit D2.0 family groups

System.Object[]

## UNKNOWN bindings

System.Object[]

## D2.1 registry

definitions\c11d\asset_families\C11D_ASSET_FAMILY_REGISTRY_V1.json

## D2.1 contract

docs\current\d\D2.1_ASSET_FAMILY_REGISTRY_CONTRACT.md

## D2.1 receipt

artifacts\tests\c11d_d2\d2_1_validation_receipt.json

## Next-context rule

A new context must read MASTER_HANDOVER_C11D_CURRENT.md first, then START_PROMPT_C11D_CURRENT.md, then the D2.0 audit and D2.1 registry, contract and receipt.
Do not reopen D2.0 unless new contradictory evidence appears.

## Prompt maintenance rule

Update MASTER HANDOVER and START PROMPT at every major milestone and checkpoint handoff.
Snapshot the previous living prompts under docs\history\master-prompts\c11d before replacing them.