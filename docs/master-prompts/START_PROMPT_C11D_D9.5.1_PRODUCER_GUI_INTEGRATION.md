# START PROMPT — C11-D D9.5.1 Producer GUI Integration

1. Expand the D9.5.1 overlay into the root of the active `ChallengeEngineV01_STATELESS` repo.
2. Run the exact commands:

```powershell
python .\c11c-suite\c11c-producer\self_test.py
python .\c11c-suite\c11c-producer\test_producer_gui_contract.py
python .\c11c-suite\self_test.py
.\c11c-suite\run.bat
```

3. Verify the existing main Suite launcher still has only five apps; open Producer 0.10.0, exercise the old C11-C producer, and exercise the new C11-D request tab. Check missing D4 receipts block planning and valid PASS/CLOSED receipts yield request/plan/parity evidence only.
4. Report real Windows Qt output and screenshots/logs only as observed; don't assert GUI launch acceptance from static tests.
5. Next milestone D9.5.2: determine a safe path to show the request's editorial text in actual media without modifying protected C11-C behavior or silently bypassing D4.8.
6. Then update and version/test the five existing apps (Catalog, Config, Maintenance, Test and Producer), cross-suite life-cycle, GUI/CLI parity, real GUI production, replay, changed music seed, bad-config/overwrite/cancel/protected-root negatives. See `docs/current/d/D9_SUITE_INTEGRATION_PLAN_V1.md`.

Do not create a new suite, do not revive c11c-studio, and do not start D10. D4.8 remains BLOCKED; D7 frozen; D8 accepted as PASS_NO_MEDIA control-plane; C11-C truth/geometry/production behavior immutable.
