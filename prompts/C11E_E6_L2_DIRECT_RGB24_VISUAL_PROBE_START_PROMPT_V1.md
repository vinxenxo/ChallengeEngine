# E6 L2 direct RGB24 visual probe — start prompt V1

Perform only the exact one-frame TEST_ONLY manifest installed by `C11E_E6_L2_DIRECT_RGB24_VISUAL_PROBE_V1`.

- Case: E6-L-01 / fractal_bloom / radial_bloom / gameplay seed 100006 / frame 0.
- Source: fresh capture from pinned C11-C Godot scene, not historical MP4.
- Pixel bridge: opaque RGBA8 → byte-exact RGB24 extraction; 720×1280, stride 2160, 2,764,800 bytes.
- Consumer: existing pinned QImage compositor once, `SmoothTransformation`, approved 720×1280 canvas/body geometry.
- Runtime: two Godot invocations (isolated import then one capture) and in-process PySide6 6.11.2 only.
- No BT.709, colour transform, MP4 decode, FFmpeg, FFprobe, audio, mux, dispatch or production renderer.

Preserve all receipts; inspect the final PNG and await explicit operator visual review. No six-selector expansion or E6 acceptance.
