# C11-C Review Tooling Fix 1.0.2

- Removes PowerShell `$variable:` interpolation ambiguity from FFmpeg filter strings by using the `-f` format operator.
- Changes keyframe time parameter to `double[]` so fractional timestamps (1.25, 2.5, etc.) are preserved exactly.
- No visual, shader, engine, simulation, or production artifact changes.
