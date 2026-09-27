# MASTER HANDOVER — C11-C Test Hotfix 2.18.4

## Authority

This is an incremental test/contract repair over the user's active C11-C 2.18.x repository and C11-C Suite 0.1.x.

## Repairs

- Align `C11CVisualDurationPolicyContractTest.gd` and the active duration policy with the current 21/17-second Visual Drill gameplay matrix.
- Make `C11CVisualLoopLongformSourceArtifactContractTest.gd` executable by the Godot test runner (`extends SceneTree`).

## Rule

Every future Godot contract test added to `tests/` must be directly runnable through `tests/run_all.py`, `c11c-suite/c11c-test/run_all.bat`, and `c11c-suite/c11c-test/run_suite.bat`.

Every new operational PowerShell/Python QA function must also receive a launcher entry in the corresponding C11-C Suite GUI.

## Frozen boundaries

Do not change simulation truth, mechanics, RNG ownership, or frozen C7/C9 contracts.
