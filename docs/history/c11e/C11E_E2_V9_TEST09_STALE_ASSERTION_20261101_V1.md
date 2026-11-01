# C11-E E2 V9 R1 â€” stale test 09 assertion

**Date:** 2026-11-01  
**Request:** `C11E-E2-CH001-AB-20261101-V9-R1`  
**Failure ZIP SHA-256:** `4d7bef8e98825c3f748257eb8bd81f444e45ddf4d0b52ab21cbfc03d8e3c8c1d`

## Observed

Godot JSON numeric contract passed in the runner: parsed gameplay and music values were `float`, full sidecar validation passed, and all 30 numeric cases passed. Python contract tests 01-08 passed. Test 09 failed because it asserted that the literal semantic marker `TITLE_IS_NOT_HOOK_CTA_OR_GAMEPLAY` appeared in `C11EChallenge001E2.gd`.

V9 intentionally centralizes semantic sidecar enforcement in `C11EE2SidecarValidator.gd`. The production scene delegates through `C11EE2SidecarValidatorScript.validate(sidecar)`. The marker remains enforced inside the shared validator, but no longer needs to be repeated in the scene file. Therefore the old assertion was stale and over-coupled to source layout.

## Impact

The runner stopped before pair preparation and before either renderer invocation. `renderer_invoked=false`, invocation count 0, `media_created=false`, release authority `NONE`. No video is accepted or produced by this attempt.

## Corrective action

The repaired test 09 reads both the production scene and shared validator. It checks inheritance, main scene mounting, `super._ready()`, delegation to the helper, enforcement of the semantic separation contract in the helper, and the editorial title source. The full nine-test suite is rerun before the next physical E2 attempt.

## Next action

Run a new physical attempt with request ID `C11E-E2-CH001-AB-20261101-V9-R2`. Do not reuse R1. E2 remains no-audio and does not authorize E3, release or promotion.