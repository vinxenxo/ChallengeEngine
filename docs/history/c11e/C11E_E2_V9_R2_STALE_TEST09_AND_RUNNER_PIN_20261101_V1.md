# C11-E E2 V9 R2 â€” stale test 09 and subsequent runner pin correction

**Date:** 2026-11-01  
**Request:** `C11E-E2-CH001-AB-20261101-V9-R2`  
**Failure ZIP:** `C11E_E2_CH001_AB_FAILURE_EVIDENCE_20261101_092839_74a33a1e.zip`  
**ZIP SHA-256:** `3d6bf533e0cbcc7c717e9e69a0e77af98aae81d13a31e9034fe685c95d4d81ad`  
**Observed HEAD:** `b299521dcd738c0ab45f4db37e0d3ab70a00c06b`

## Failure

The runner passed its integrated Godot 4.7.1 Mono JSON numeric contract (30/30). Python tests 01â€“08 passed; test 09 failed on the assertion that `TITLE_IS_NOT_HOOK_CTA_OR_GAMEPLAY` must appear literally inside `C11EChallenge001E2.gd`. In V9 that semantic rule is enforced by the shared `C11EE2SidecarValidator.gd`, and the production scene delegates to that validator. The old assertion was stale. Runner diagnostic records zero renderer invocations, no media and release authority NONE.

## Subsequent fix and newly detected dependency

V19 corrected test 09. The operator-reported suite result was 9/9 PASS, corrected test SHA `ab4ed3fd421ef0cac86d4ef25167f0161a186ef5bd90373414abed7bea17d2a9`, receipt SHA `6cbe3fe05d1b6f7cc7fe3971171d398a3b2197477668fce5b7b7a93b74dfd855`.

Inspection then found the V9 runner still pinned the old test SHA `36b6f296d17f72b51b96946953b1abc72e907f5823567fd8a9993ae5f4169342`. The V20 pin fix updates exactly that literal. New runner SHA: `c5d6bc26c70151238f60466fa401e1fd14ef9b0a25b34aa45d98ebce2ba5c763`.

R1 and R2 are both consumed. The next physical request is R3. Do not reuse either failed request identifier.