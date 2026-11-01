# C11-E Execution Hygiene and Assistant Error Log — V18

**Date:** 2026-11-02

## 1. Current operating rules

1. Active Windows checkout is the execution authority. Verify branch, HEAD ancestry, exact file hashes and immutable C11-C manifest before applying an overlay or physical test.
2. Do not regenerate accepted snapshots, repeat passed gates, or create documentation-only iterations without a material evidence change.
3. Installers are add-only. Refuse to overwrite a different existing destination. A repair may normalize whitespace only in explicitly listed documentation files; it must not change source or evidence artifacts.
4. Use PowerShell 5.1-safe syntax. Avoid `&&` and `Read-Host`. For native process output requiring both streams, use `System.Diagnostics.ProcessStartInfo` with asynchronous or safely drained stdout/stderr; do not rely on PowerShell native `2>` when `$ErrorActionPreference='Stop'` can convert diagnostic stderr into a terminating error.
5. A process exit code and an explicit acceptance marker are both required. A stale JSON file, stale result object, or text marker without current request/pins is not a PASS.
6. Every physical attempt has a new RequestId. Failed attempt IDs are never reused. R4 is immutable evidence.
7. Keep evidence ZIP SHA, receipt SHA and receipt sidecar aligned. Validate ZIP CRC and the exact published SHA before relying on its content.
8. Keep test-only output separate from production release authority. Renderer/media flags in a scoped evidence receipt do not imply promotion or permission for a broader family.
9. Preserve user's local commit workflow. Stage only allowlisted paths; inspect `git diff --cached --check`, staged names and diff summary before commit.

## 2. V21 whitespace issue and correction

The V21 commit preparation stopped at `git diff --cached --check` because several Markdown metadata lines contained trailing spaces. This was a documentation-formatting error, not a runner failure and not an R4 failure. R4 then executed successfully with the V21-pinned runner.

V22 apply helper removes only terminal spaces/tabs from the eight explicitly enumerated V21 Markdown files, preserving their content and line endings as far as possible. It stages those files together with the V21 runner change and the new V22 documentary overlay. It does not rewrite the runner, receipt, ZIP, C11-C manifest, or any generator/mechanic source.

## 3. R3/R4 media-range incident closure

R3 exposed full-range `pc` MJPEG input being propagated through scale, yielding H.264 `yuvj420p` / full-range output. V21 V3 patched the delivery transcode to declare `in_range=pc:out_range=tv`, `format=yuv420p` and encoder `-color_range tv`, and made FFprobe assert `color_range=tv`.

R4 confirms both outputs now report H.264 High, `yuv420p`, `color_range=tv`, 720×1280, 30 fps, 270 frames, 9 seconds and no audio. The R3 issue is closed for the E2 delivery path; do not remove the explicit color-range controls.

## 4. R4 review boundaries

The evidence ZIP's `source_visual_content_*` stderr files contain FFmpeg informational diagnostics and signalstats output; both corresponding exit-code files are `0`. Their presence is not a runner failure. The final FFprobe logs are valid JSON and show one video stream with no audio stream, which is expected for E2.

The assistant performed a sampled visual review only. The operator must view both complete MP4s and record their decision before E3 starts. Do not update the R4 receipt's pending field.

## 5. No-go conditions

- Any unexpected staged path or modified protected source file.
- Any manifest, runner, test or evidence hash mismatch.
- Receipt/request mismatch, reused RequestId, absent final MP4, failed FFprobe, wrong pixel format/range, unexpected audio in E2, or incomplete A/B comparisons.
- Treating `renderer_invoked=true` in this constrained R4 receipt as release authority.
- Beginning E3 before operator approval and E3 source/contract preflight.
