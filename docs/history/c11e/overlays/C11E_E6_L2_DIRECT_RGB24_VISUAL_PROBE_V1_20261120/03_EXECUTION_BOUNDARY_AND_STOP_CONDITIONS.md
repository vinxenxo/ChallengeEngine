# Execution boundary and stop conditions

The V1 successor policy is narrowly armed only for one TEST_ONLY visual probe. It is not a general successor to D4.8 V2. D4.8 V2 remains byte-identical and BLOCKED.

The runtime stops before capture if any source SHA, C11-C frozen-manifest SHA, D4.8 SHA/byte count, QImage module SHA, predecessor receipt/sidecar, Python version, PySide6 version, or Godot executable SHA/byte count differs.

The runtime stops during capture if the selector, seed, grammar, frame index, viewport size, image format, alpha opacity, RGB byte count, or stride differs. The temporary Godot project exists under the OS temp folder only and is removed in `finally`. The active checkout is read-only except for a new unique evidence directory under `artifacts/tests/c11e/e6_l2_direct_rgb24_visual_probe_v1/`.

No FFmpeg, FFprobe, audio, mux, historical MP4, dispatch, BatchId or production media call is present in the allowed process list. Any requirement for a colour-space conversion blocks this V1 rather than permitting a guessed profile.
