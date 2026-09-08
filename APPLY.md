# F0.1.5 / F0.1.6 recovery patch

This patch is intended to be overlaid on the restored good baseline.

Modified/added files:
- core/authoring/ChallengeAuthoringPolicy.gd (new)
- core/authoring/ChallengeAuthoringRequest.gd
- core/authoring/ChallengeAuthoringRequestValidator.gd
- core/authoring/AssetFamilyValidator.gd
- core/authoring/CanonicalV2Assembler.gd (new)
- core/authoring/ChallengeGenerator.gd
- profiles/assets/fam_001.json
- tests/C6F0_1_5CanonicalAssemblerTest.gd (new/replacement)
- tests/C6F0_1_6AuthoringPipelineTest.gd (new/replacement)

Important invariants:
- generate() legacy body is intentionally not replaced by the normative path.
- no DifficultyProfileRegistry.initialize_defaults() exists or is required.
- no CHALLENGE_001 fallback exists in production code.
- no simulation/RNG/timeline code is changed.
- normative generation is currently proven only for pilot, because only pilot has complete contractual video/assets metadata.

Required local verification (Godot 4.7.1 Mono):
1. godot --headless --path . --editor --quit
2. godot --headless --path . -s .\tests\C6F0_1_5CanonicalAssemblerTest.gd
3. godot --headless --path . -s .\tests\C6F0_1_6AuthoringPipelineTest.gd
4. python .\tests\run_all.py

Do not certify F0.1.6 until all applicable regression tests are green.
