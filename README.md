# C11-C 2.19.12 — Family Coverage Challenge Probe Minimal Repair

Minimal repair only.

Changed file:
`tools/qa/c11/run_c11c_family_coverage_smoke.ps1`

Exact fix:
The Challenge validation assigned the return value of `Assert-Media` through `| Out-Null`, which discarded the ffprobe object. The next line then accessed `$challengeProbe.streams` under `Set-StrictMode`, producing `PropertyNotFoundException`.

The repair removes only that `| Out-Null` from the assignment so the existing probe object remains available.

No engine, Challenge definition, production runner, audio/video contract, WorkerRoot, override.cfg, timing, FPS, or presentation code is changed.
