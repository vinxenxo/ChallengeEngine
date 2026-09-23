C11-C VISUAL DRILL SOCIAL PRESENTATION V1 — REVISED OVERLAY

Apply this ZIP at the repository root, preserving paths.

The first overlay had two packaging defects. This revised overlay fixes both:
1) it explicitly contains core/presentation/C11CVisualEditorialLayer.gd;
2) the reviewer resolves PowerShell Join-Path correctly and handles the legacy 12345_A envelope.

Verification:
  .\tools\prototypes\c11c_bulk\verify_c11c_visual_drill_overlay.ps1
  python .\tests\run_all.py

Review generation:
  .\tools\prototypes\c11c_bulk\run_c11c_visual_drill_review.ps1 -ResetReviewAssets

Audio is one deterministic 18-second GLOBAL master for every Visual Drill; the same master is reused/truncated for shorter exercise durations.
Matrix is OFF for Visual Drills.
Simulation, RNG, SimulationResult, WinningFrameDetector/Gate, C7, C9 and C11-B geometry are not changed by this overlay.
