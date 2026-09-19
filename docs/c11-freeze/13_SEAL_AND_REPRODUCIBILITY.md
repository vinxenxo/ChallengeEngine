# C11 Freeze — Seal and Reproducibility

## Principle

Execution and sealing are separate operations.

The freeze gate may rerun the full corpus. The final seal must also support a **seal-only path** over already validated evidence so that a transient native-process failure cannot turn previously green evidence red merely because the seal was attempted later.

## Full validation

```powershell
.\tools\c11freeze\run_all.ps1 -SeedRepeat 2 -StressRetries 3
python.exe .\tools\c11freeze\generate_qa_video_matrix.py --include-canonical --limit 0
.\tools\c11freeze\run_qa_video_matrix.ps1
```

## Seal existing evidence

After the gates have independently passed:

```powershell
.\tools\c11freeze\finalize_c11_freeze.ps1 -SkipExecution
```

The seal operation validates the evidence itself before producing the SHA-256 manifest and certificate. It does not accept mere file presence.

## Native crash resilience

`run_seed_stress.py` retries process/runtime failures up to three additional times by default. A telemetry mismatch is still a genuine determinism failure and is never hidden by retrying successful executions.

The known Windows/Godot access-violation representation `0xC0000005` is recorded in the stress evidence when encountered. Retries are a robustness mechanism, not a pass override.

## QA video/audio boundary

The 54-video C11 matrix is intentionally audio-off. `build_factory` may therefore retain `C7_A2_MIXED_BATCH_REQUIRED` in its internal manifest. The C11 video gate accepts that exact out-of-scope condition only when the matrix summary is independently `54/54` with zero video failures and `audio_enabled=0`, `audio_disabled=54`.
