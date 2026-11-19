# V2.4 start prompt

1. Verify the V2.4 package ZIP against its sidecar SHA-256 and extract into a fresh empty directory.
2. Run the add-only installer in Windows PowerShell 5.1; inspect its receipt, package SHA, C11-C manifest pin and unchanged D4.8 V2 pin.
3. Run the 17 V2.4 focused regression tests using Python 3.13.14, preserving their full output.
4. Run the V2.4 runner exactly once with `--iterations 7`. Confirm the A3 V4 field mapping PASS, source pins, QImage 37-test result and native-stage timing result.
5. Preserve the V2.4 receipt and sidecar and send the complete transcript. Do not run Godot, FFmpeg, FFprobe, audio, mux or any production renderer/dispatch path.
6. Treat any PASS as synthetic QImage-stage evidence only; do not claim E6 acceptance or release authority.
