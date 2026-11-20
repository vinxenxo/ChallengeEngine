# C11-E installer incident register — V61

## 2026-11-20 — L2 Direct RGB24 Visual Probe V1

The new package is ADD_ONLY. The installer preflights all ZIP members, manifest bytes/SHA values, source C11-C pins, D4.8 V2, and every target collision before writing. It uses same-directory temporary files, SHA postimage verification, atomic moves, and rollback limited to transaction-owned additions. Existing identical files are skipped; conflicting destinations block before mutation.

The runtime uses a temporary isolated Godot project, not the active checkout. It records two exact Godot invocations (project import/class scan and one-frame capture) and no other media processes. No FFmpeg/FFprobe/audio/mux/dispatch is permitted. Target PowerShell 5.1 AST must pass before install and before runner invocation.
