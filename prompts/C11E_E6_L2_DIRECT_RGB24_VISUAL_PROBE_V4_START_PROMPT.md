# C11-E E6 L2 Direct RGB24 Visual Probe V4 — Start Prompt

V3 installer completed 24/24, but its tests and runner exposed two independent V3 defects: the tests assumed the package-root installer was installed at repository root, and the runner's capture SHA literal was stale versus the final GDScript/manifest hash. The V3 runner stopped before Godot.

Install V4 from a fresh temporary extraction. The test command must set `C11E_L2_INSTALLER_SOURCE` to the extracted V4 installer path. V4 runner capture SHA and byte constants must match the V4 execution manifest and actual GDScript. Run the 78 focused tests once, then V4 runner once.

Scope remains one `E6-L-01` frame, `radial_bloom`, gameplay seed 100006, frame 0, direct opaque RGBA8 to RGB24, one QImage composition. No historical MP4, color transform, BT.709 assumption, FFmpeg/FFprobe/audio/mux or production renderer/dispatch.

Preserve V1–V3 evidence. C11-C/D4.8 immutable; E6 accepted 0; release authority NONE.
