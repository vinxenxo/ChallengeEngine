# E4A.3 V1 execution stall — failure analysis V2

## Observed outcome

Windows overlay application succeeded and the 46/46 Python contract tests completed. The console stopped after `E4A_3_FOCUSED_TESTS=46/46_PASS`, during the Godot phase. No Godot exit marker, stdout/stderr hashes, receipt or report were produced in the supplied excerpt. Therefore E4A.3 V1 runtime is FAIL/INCOMPLETE, not PASS.

## Root cause

The V1 runner built the Godot command with `--headless`. The GDScript's real-body branch creates a `SubViewport`, awaits `process_frame`, then awaits `RenderingServer.frame_post_draw` before reading `viewport.get_texture().get_image()`.

Official Godot `RenderingServer` documentation: headless mode disables rendering and window management; most RenderingServer methods return dummy values. The docs define `frame_post_draw` as a signal emitted after RenderingServer has updated all Viewports. The runner therefore requested a real render-completion event in a mode that disables rendering. This is why the command can wait indefinitely at the first SubViewport capture. References:
- https://docs.godotengine.org/en/latest/classes/class_renderingserver.html
- https://docs.godotengine.org/en/latest/tutorials/rendering/viewports.html

## Corrective action in V2

- Remove `--headless` only for this test path. It is an offscreen SubViewport proof, but it still requires an active rendering backend. The normal Godot executable may briefly open a window; the test remains isolated.
- Stream stdout/stderr to files and print a five-second Python heartbeat.
- Print `EVIDENCE_DIR` before starting Godot and preserve all process logs.
- Enforce 90-second timeout, terminate/kill the child on timeout, and stop the run as FAIL.
- Add GDScript stage markers before/after every viewport and around both awaited frame signals.
- Add tests for non-headless invocation, finite timeout, process termination and log preservation.

No C11-C code, source media, gameplay generator, production renderer, audio, dispatch or manifest change is involved.

## Status

V2 preparation: 50/50 Python tests PASS, Python compilation PASS. Windows runtime must be re-executed once with V2 against the accepted E4A.2 RUN directory. Do not rerun V1 and do not accept the old `46/46` as a runtime result.
