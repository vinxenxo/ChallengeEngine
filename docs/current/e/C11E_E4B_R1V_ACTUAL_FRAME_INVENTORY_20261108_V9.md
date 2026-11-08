# E4B R1V Actual Frame Inventory — V9

R1V has one real source capture: Fractal Bloom / `radial_bloom`, gameplay seed 100006, 22 seconds, 720x1280 at 30 FPS, 660 frames. C11-C launcher exit 0; source MP4 H.264 High `yuvj420p/pc`, SHA `7971ced1d9cdbb7dd76a0d8d76e766faa9a051fc27419c9e737c41264796f659`. The initial V3 inventory parser falsely rejected Godot's UTF-16LE `720×1280 @ 30 FPS` log text and `yuvj420p/pc` pixel range. The operator visually confirms this source and layers. The failed V3 run's report records zero inventories; do not call it an inventory PASS.

An isolated validation of the retained source has since measured 660 increasing PTS values at 1/30 second intervals and calculated SHA-256 for every decoded yuv420p frame via an FFmpeg pipe to memory (no PNG/frame spool). This is engineering validation of the revised inventory logic, not a Windows R1V run receipt.

The integrated A/V runner V1 handles all 10 slots in one pass: reuses Fractal A without relaunch; performs nine new C11-C silent visual source captures; inventories PTS/frames/pixel hashes; generates native C11-C FAMILY_MUSIC_V4 from the R1P music_seed; muxes AAC 192k/44.1k stereo with H.264 bitstream copy; probes final A/V and compares A/B visual, PCM and AAC hashes. The source MP4 and its C11-C sidecars remain immutable/silent; the A/V MP4 is a separate output. No D compositor, D3 V5, filters, re-encode or dispatch.

Five selectors are representative only, not full 27-selector acceptance. After technical 10/10 and operator visual/listening review, the remaining 22 variants require a separate bounded expansion and the same family music contracts. Frames are hashed in memory; raw decoded frames are not written to disk.


## Integrated family-native A/V acceptance

The upcoming package creates per-slot source inventory and family music/AAC delivery in the same R1V run. The silent C MP4 is retained unchanged; the final A/V MP4 is separate and uses H.264 stream copy. The A/B comparison covers exact PTS, every decoded frame SHA, global decoded-pixel SHA, WAV SHA and AAC elementary-stream SHA. No frame PNGs or decoded raw frames are written to disk. The Windows wrapper requires the prior Fractal-A reuse test to execute (zero skipped tests).
