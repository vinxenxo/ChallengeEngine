# C11E E4A.3 Godot compositor overlay V2 — application notes

## Why V2 exists

V1 launched Godot with `--headless`, which disables RenderingServer rendering while the test awaits `RenderingServer.frame_post_draw`. Apply V2 instead; do not rerun V1.

## Apply and execute

Save `C11E_E4A_D_GODOT_COMPOSITOR_PIXEL_OVERLAY_V2.zip` and its `.sha256` sidecar in Downloads. Stop any foreground V1 process with Ctrl+C first. Use the single integrated PowerShell 5.1 apply/test block from the continuation response. It verifies the ZIP and sidecar, the exact V1 source preimages, all payload postimages and the frozen C11-C manifest before mutation.

V2 replaces exactly three paths: the D materializer, E4A.3 runner and focused tests. It adds the V39 authority/matrix/backlog/increment/failure/README/roadmap/master-prompt/start-prompt files. It does not modify C11-C source or any production authority.

The runner reuses the accepted E4A.2 directory:
`artifacts/tests/c11e/e4a_real_body_pixel_review/RUN_20261104_002559_542bcf60`

The new Godot process uses the normal renderer-enabled invocation (no `--headless`), with a 90-second hard timeout and a heartbeat every 5 seconds. The runner prints the new `EVIDENCE_DIR` early. The GDScript logs each variant/sample begin and completion and marks the `frame_post_draw` wait.

Expected pre-execution tests: 50/50 Python PASS. Windows runtime remains open until a complete ZIP with Godot 4.7.1 exit 0, report, receipt, PNGs, comparisons, logs and SHA256SUMS is reviewed.

## Scope

The test consumes six real E4A.2 delivery frames and creates 18 test PNGs / 12 comparisons. No gameplay renderer, C11-C rerun, production D dispatch, MP4 generation, audio or layout approval.

C11-C frozen manifest SHA: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. Release authority remains NONE.
