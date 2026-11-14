# C11-E E4C V2.3 R3 — timeout unit correction and A/V continuation

## Background

V2.3 R2 is installed and independently audited PASS. The prior A/V attempt was not given 30 minutes: `.WaitForExit(1800)` means 1,800 milliseconds in .NET. R3 corrects this to 1,800 seconds (1,800,000 milliseconds) and publishes progress.

## Install

Download the ZIP and sidecar from this delivery. Extract to a new Downloads directory. Verify ZIP SHA using the sidecar. Run `INSTALL_C11E_E4C_V2_3_R3_REQUALIFIER_TIMEOUT_FIX.ps1` with ProjectRoot, PythonExe and PackageZip exactly as shown in the assistant handoff. The installer verifies 21 source pins, frozen C11-C manifest, package inventory, PS AST, Python compile, and the focused timeout contract tests. It does not rerun the 27 already accepted consumer tests.

## Independent audit

Run `VERIFY_C11E_E4C_V2_3_R3_INSTALL_V1.ps1` with ProjectRoot, PackageRoot, PackageZip and the RunId reported by the installer. Require PASS on both replacement postimages, all add-only postimages, backups 2/2, source pins 21/21, frozen C11-C and governance. Do not run A/V if audit fails.

## Requalification

Run the installed wrapper only after independent audit PASS. Continue to reuse the preserved CLI smoke evidence `artifacts/production/c11e/E4C-CLI-SMOKE-20261112T091253Z-5a2e96b8`. Do not rerun GUI/CLI smoke, native capture, Godot, or family music generation. Wrapper announces `REQUALIFIER_TIMEOUT_SECONDS=1800` and `REQUALIFIER_TIMEOUT_MILLISECONDS=1800000`; it uses bounded `WaitForExit` polls of at most 3,000 milliseconds while enforcing the full 1,800,000-millisecond stopwatch deadline, then streams stage and frame progress lines.

Expected final status: `V2_REQUALIFICATION=PASS_TECHNICAL_PENDING_OPERATOR_REVIEW`, seven `operator_review` frames, silent V2 intermediate and final A/B/C MP4s. A technical receipt does not equal operator visual/audio acceptance.

Expected frame oracle: GAME native body identity 630/630; PRE_ROLL+END_CTA native full-frame passthrough 180/180; timebase 90/630/90; video stream hash A/B/C identical; audio A/B identical and C distinct; FFprobe H.264 High yuv420p TV 720x1280 30 fps, AAC-LC 48 kHz stereo, 27 seconds and <=20 ms start drift; E1 pins unchanged 91/91. Human review is then required.

Release authority remains NONE, E1 PREPARE_ONLY, family adapter NOT_CONNECTED_E1, production dispatch FALSE.
