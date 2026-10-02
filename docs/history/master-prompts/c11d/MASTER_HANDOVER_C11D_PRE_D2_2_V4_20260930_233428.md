# C11-D MASTER HANDOVER

## Current phase

C11-D â€” Declarative Challenge recovery, visual/editorial parity, reusable asset families, production and provenance pipeline.

## Current checkpoint`r`n`r`nD2.2 â€” Asset Role / Evidence Matrix`r`nSTATUS: ACTIVE`r`n`r`n## D2.0 evidence

Audit:
artifacts\tests\c11d_d2\d2_0_asset_family_audit.json

Contract:
docs\current\d\D2.0_ASSET_FAMILY_AUDIT_CONTRACT.md

Receipt:
artifacts\tests\c11d_d2\d2_0_validation_receipt.json

## D2.1 completed scope

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

## D2.2 active scope

Build and validate an evidence-backed asset role matrix.
Preserve UNKNOWN where role evidence is insufficient.
No filename-only inference, no SHA-256 merge, no historical promotion, no runtime activation.

Matrix: artifacts\tests\c11d_d2\d2_2_asset_role_evidence_matrix.json
Contract: docs\current\d\D2.2_ASSET_ROLE_EVIDENCE_MATRIX_CONTRACT.md
Receipt: artifacts\tests\c11d_d2\d2_2_validation_receipt.json