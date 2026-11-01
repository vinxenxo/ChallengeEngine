# C11-E execution hygiene and assistant error log â€” V15

**Date:** 2026-11-01

## Incident: V9 E2 Python test 09 stale textual assertion

Physical attempt `C11E-E2-CH001-AB-20261101-V9-R1` completed the integrated Godot JSON contract test successfully (30/30) and then stopped in `test_09_godot_scene_inherits_main_and_adds_no_c_source_edits`. The test searched for `TITLE_IS_NOT_HOOK_CTA_OR_GAMEPLAY` in the scene script. V9 had moved the semantic validation into `C11EE2SidecarValidator.gd`; the old assertion incorrectly required implementation detail to remain duplicated in the scene source.

The evidence ZIP records tests 01-08 passing, test 09 failing, runner exit 1, zero render invocations, and no media. Failure evidence SHA-256: `4d7bef8e98825c3f748257eb8bd81f444e45ddf4d0b52ab21cbfc03d8e3c8c1d`.

## Repair

Update test 09 to assert all of the following:
- E2 scene inherits `GeneradorMaestro.gd`, is mounted by `Main.tscn`, and calls `super._ready()`.
- Scene delegates full sidecar validation to `C11EE2SidecarValidatorScript.validate(sidecar)`.
- Shared validator enforces `visual.semantic_separation == TITLE_IS_NOT_HOOK_CTA_OR_GAMEPLAY`.
- The header title label reads only `_c11e_sidecar["editorial"]["title"]`.
- No ChallengePresentationBinder, SimulationResult or FrameSnapshot dependency is introduced by this E2 extension.

The repair script verifies exact preimage hashes and V9 source pins, backs up the test, executes the full Python suite, and writes documentation/receipt only after 9/9 PASS. It must rollback the Python test if verification fails.

## Lessons / hard execution rules

- A nonzero exit code terminates the whole PowerShell block. Never continue manually with receipt/hash/media checks after a `throw`.
- Never print a PASS marker outside the successful branch that has actually validated the result. Never rely on `$?`, `$LASTEXITCODE`, `$Record`, or `$ReceiptPath` left by a previous command or session.
- Keep each run self-contained and use a fresh request ID. Do not reuse stale artifacts.
- Do not regenerate installer packages to repair a test assertion; prefer one exact-hash-guarded source repair and integrated regression check.
- Test contracts must validate observable architecture and shared enforcement, not insist that a marker string remain in one file after a deliberate refactor.
- Preserve separate installation, automated test, physical renderer, human review and release-authority decisions.

## Authority

E2 remains no-audio, no release authority and no baseline promotion. E3 remains blocked until physical A/B and human review pass. C11-C production sources and frozen release pins remain immutable.