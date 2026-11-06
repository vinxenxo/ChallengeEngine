# C11-E E4A.6 Live Pixel Capture / Reserved Bands — Postmortem V10

**Date:** 2026-11-05. V8 corrects the V2 wrapper diagnosis and records the recovered Movie Maker evidence without changing earlier receipts.

## Visual requirement

With a D editorial envelope enabled, full-width HEADER and FOOTER reserved bands remain opaque pure black for every frame, including when optional editorial is absent or inactive. Title/subtitle may appear only in HOOK/HEADER; CTA only in CTA/FOOTER. Inactive region labels/separators hide; black background remains. BODY and no-envelope legacy C rendering remain unchanged. The current body/video background colour is accepted for this gate; user selection of that colour is a separate future feature.

## V2 Windows evidence

Windows PowerShell 5.1.26100.9818 AST PASS; Python 22/22 PASS; Godot 4.7.1 editor import PASS; live-root PASS for 900 frames, one mount and 900 black-band frames. Movie Maker stdout includes:

- `C11E_E4A6_LIVE_CONSUMER_CONFIGURED` with enabled=true, success=true, matching envelope SHA and source_frames=900;
- `TELEMETRY_JSON` with 900 total frames split 180 HOOK + 420 GAME + 180 REVEAL + 120 CTA;
- `AUDIO_EXPORT_JSON` with `audio_enabled=false`;
- Movie Maker mode, successful `Done recording movie at path`, and a 900-frame 540x960/60 FPS/15 s AVI.

AVI SHA-256 from the uploaded V2 evidence archive: `2f6d0c73cb09571584db68e37760c933706473a07e559fc93113f26eabb89f45`. FFprobe finds an unexpected PCM S16LE 48 kHz stereo stream despite the Godot export flag. It is not accepted as music and must be removed from the visual review derivative using `-map 0:v:0 -an`.

## V2 false-negative — exact root cause

`Test-CaptureLog([string]$stdout,...)` uses `Test-Path` and `[IO.File]::ReadAllText($stdout)`, so its first parameter is a **file path**. The capture branch called `Test-CaptureLog $movie.Stdout $envelopeSha`, where `$movie.Stdout` is the in-memory process output. `Test-Path` therefore returned false; the validator never parsed the valid Movie Maker markers/telemetry. The error is in the runner's argument contract, not in the D consumer or Movie Maker capture. The V2 command's overall status remains `BLOCKED` and must not be rewritten as if it emitted a PASS receipt.

The recovery-only runner uses explicit `Test-CaptureLogText` and `Test-CaptureLogFile` helpers, validates the existing stdout, and resumes at FFprobe/FFmpeg. It does not rerun rendering or source tests.

## Independent postprocess corroboration

The uploaded AVI was independently decoded and normalized in the analysis environment. It yielded H.264 High 720x1280, 30 FPS, 450 frames, 15.000 s, yuv420p, limited/tv range and zero audio streams. Eight boundary stills were extracted. Twelve inactive-band checks returned 0 non-black samples in 31,680 interior samples each; four active HOOK/CTA checks exceeded 100 non-black samples. This corroboration used FFmpeg 7.1.5; the Windows recovery receipt must use the installed FFmpeg 9.0 and becomes the project-side postprocess evidence.

## Source boundary and next

Recovery writes only test/review outputs and new versioned docs. D consumer SHA `eba81fff4c24ca75033c8f963665df1961136046c41fee0e88681fe55a631203`; focused test SHA `9845eda094037f8748493171755b32d3479ddf6548612e9a6ecebba187cbc512`. Frozen shared C11-C layer and root `GeneradorMaestro.gd` remain read-only. No production renderer, dispatch or media.

After recovery receipt: full Challenge E4A A/V with corrected silent MP4 unchanged, actual D3 V5/D3.3, A/B/C music-seed isolation, identical H.264, AAC mux/FFprobe, A/V sync/listening and E1 GUI/CLI parity. Then E4B, E4C, E5, Smoke18, Matrix101 and E8 in order.


## Recovery V1 false BLOCKED — Git HEAD pin

Windows PowerShell 5.1 AST passed, but recovery V1 stopped at `EVIDENCE_AND_SOURCE_PREFLIGHT` because it required the V2 run's prior `HEAD` (`0b24934f423763513540e31ba9104052617c4e4f`). The operator had made the expected iteration commit; live `HEAD` was `d5589fde1e5132c653c1ac5604a34a524c02a47a`. The runner also required a `.git` directory and attempted a final HEAD-stability check. No media/evidence processing, source write or documentation write occurred.

This was an unnecessary gate and directly contradicted the operator's standing workflow: the operator commits every iteration. Recovery V1.1 removes all Git commands, `.git` assumptions, HEAD/status checks and Git receipt fields. It retains frozen-manifest byte/SHA checks plus exact source and evidence hashes. Never reintroduce Git state as an iteration precondition.


## Recovery V1.1 documentation preflight failures — exact cause

Recovery V1.1 removed Git checks successfully. The operator's first run placed the runner in Downloads without the companion `RECOVERY_DOC_MANIFEST_V1_1.json`, so it stopped at `DOCUMENTATION_PREFLIGHT` with “Recovery documentation manifest is missing.” The operator then copied the manifests to Downloads, but not the relative payload tree `docs/current/e/...`, `docs/history/...` and `prompts/...`; the next run therefore stopped at the first missing payload (`C11E_CURRENT_AUTHORITY_20261105_V66.md`). Neither attempt reached FFmpeg/FFprobe, source writes, output media or documentation installation.

The underlying design error was requiring manually co-located package files while the operator was told to run a script directly from Downloads. A manifest is an index, not the documents it hashes. Copying a manifest alone can never satisfy its payload contract. Recovery V1.2 removes this external dependency: the compressed documentation ZIP and manifest are embedded in the `.ps1`; the runner verifies the embedded archive SHA, extracts to its unique recovery run directory, verifies every document SHA, then uses that staged root for the normal add-only installation. The only required Downloads file is the runner itself. No separate manifest movement or nested extraction is required.
