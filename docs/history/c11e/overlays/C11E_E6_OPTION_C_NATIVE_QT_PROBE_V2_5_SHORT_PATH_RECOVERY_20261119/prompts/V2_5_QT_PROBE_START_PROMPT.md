# V2.5 start prompt — resolve extraction/staging path budgets before QImage gate

1. Verify the V2.5 ZIP against its SHA-256 sidecar.
2. Preflight every ZIP member's full extraction path and extract only to `%TEMP%\c11e25`; never use the long Downloads directory.
3. Run V2.5 installer in Windows PowerShell 5.1. Require AST PASS, frozen pins PASS, package rows PASS, stage and write-temp path budgets PASS, and all 18 destinations verified.
4. Run the V2.4 17-test focused suite once.
5. Run the V2.4 Qt/QImage probe exactly once with seven iterations. Preserve receipts/sidecars and complete output.
6. Only after A3/source pins, 37/37 QImage and P95 <=33.333ms pass, inspect all three synthetic previews and explicitly decide resampler quality.
7. Do not run Godot, FFmpeg, FFprobe, audio, mux, production renderer or dispatch. No E6 acceptance or release authority is implied.
