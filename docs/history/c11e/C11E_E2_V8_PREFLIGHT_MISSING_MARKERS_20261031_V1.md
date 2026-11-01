# E2 V8 standalone native preflight — missing markers (V1)

Observed operator output: `Godot ha terminado sin emitir los dos marcadores obligatorios. No iniciar E2.` No complete Godot stdout/stderr, process detail or result JSON was included with the report. The correct gate status is FAILED/UNVERIFIED; do not infer PASS from the absence of another error.

Code-reviewed V8 harness defect: the standalone `SceneTree` test preloaded `C11EChallenge001E2.gd` and instantiated it to reach the validator. That script inherits the complete `GeneradorMaestro.gd` runtime. This makes a simple JSON numeric unit test depend on the whole production scene script and its dependencies. The test also used stdout markers as its only proof channel.

V9 extracts a lightweight shared `C11EE2SidecarValidator.gd`, preloads only that helper in the test, and writes a structured JSON result whose schema/status/types/30-case denominator are checked by the runner. This is a design remediation, not a runtime PASS. Real Godot 4.7.1 Mono execution is still required.
