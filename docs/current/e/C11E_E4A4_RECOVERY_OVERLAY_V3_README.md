# C11-E E4A.4 Recovery V3 — README

Use the single file `RECOVER_C11E_E4A4_SUCCESS_FROM_LOGS_V3.ps1`. Save it directly anywhere, including Downloads, and invoke that exact path with PowerShell 5.1. The script contains its own pinned add-only documentation payload; no companion ZIP is required, and it does not assume the script sits directly in Downloads.

The worker's JSON `run_id` omits the `RUN_` prefix used by the run folder and ZIP. V3 verifies `folder = RUN_ + run_id`, confirms report identity and all archive hashes/media. This recovers existing outputs only; it never re-runs D3, mastering, FFmpeg, FFprobe, Godot, gameplay or renderer.

Default evidence root: `Documents\C11E_E4A4_APPLY_RUN_20261104_023647`. Default repository: `Projects\ChallengeEngineV01_STATELESS`. The script preserves C11-C authority and release locks.
