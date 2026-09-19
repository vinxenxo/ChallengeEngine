C11-B.1 — Social UI Integration v1

Apply over the certified C11-B.0.2 v4 state.

Validation:
1. .\tools\verify_c11b1_installation.ps1
2. godot --headless --path . -s .\tests\C11B1SocialUIIntegrationContractTest.gd
3. python.exe .\tests\run_all.py

Expected new marker:
[C11B1_SOCIAL_UI_INTEGRATION_CONTRACT_SUITE] PASS
