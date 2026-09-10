# C6-E / E3 DELTA — APPLY NOTES

This is an additive E3 delta, not a replacement repository.

Apply on top of the already-certified local C6-E/E2 working tree.

Files:
- `core/validation/PresentationProfileValidator.gd` — new hard presentation gate.
- `tests/C6E3PresentationValidationTest.gd` — new E3 contract suite.
- `core/validation/ChallengeDefinitionValidator.gd` — integrate the E3 gate into Layer 0.
- `tests/run_all.py` — register the new suite.

Do NOT replace E2 presentation files from this delta package.
Do NOT replace `GeneradorMaestro.gd`, `PresentationUI.gd`, `PresentationProfile.gd`, mechanics, RNG, timeline or simulation files from another baseline.

Local certification sequence:
1. `godot --headless --path . --editor --quit`
2. `godot --headless -s tests/C6E3PresentationValidationTest.gd`
3. `python .\tests\run_all.py`
4. `python build_factory.py --batch ./challenges --output ./output --workers 1`

E3 is not certified until the above runs are green in the real Godot 4.7.1 environment.
