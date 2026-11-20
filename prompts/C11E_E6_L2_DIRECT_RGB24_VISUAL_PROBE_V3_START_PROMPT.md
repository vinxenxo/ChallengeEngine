# C11-E E6 L2 Direct RGB24 Visual Probe V3 — Start Prompt

The V2 installer failed only at receipt-sidecar temp writing. The final sidecar path (226 chars) was extended by `.tmp.` + 32-character GUID to 263 chars, exceeding classic .NET Framework MAX_PATH. The transaction catch ran; the operator then observed the V2 tests and runner missing.

Install V3 into the active checkout from a fresh staging directory. It uses short sibling temp names `r.<guid>.tmp` and `s.<guid>.tmp`, validates final/temp paths <=240 chars, creates the receipt directory before payload writes, writes/validates both temp files before atomic moves, and rolls back only exact transaction-owned postimages.

Require Windows PowerShell 5.1 AST, exact package member/hash checks, frozen C11-C/D4.8 pins, 20 source pins and 24/24 ADD_ONLY destinations. Run 72 tests once. Execute the V3 runner once.

Scope is unchanged: one direct `SubViewport` capture, `E6-L-01`, seed 100006, `radial_bloom`, frame 0, RGB24 720x1280, one QImage composition. No FFmpeg/FFprobe/audio/mux, historical MP4, production renderer, dispatch or Smoke18. Keep `E6_ACCEPTED=0` and release authority NONE.
