# C11-A FIX v3

Fixes the final PowerShell manifest-construction error without rerunning the 54 exports.

## Recovery
Run:

```powershell
.\tools\finalize_c11a_visual_bulk_qa.ps1
```

This validates the existing `qa/c11a_visual_qa/runs/*` corpus, rebuilds the manifest, and performs the A/B gates.

## Fresh complete run
Use:

```powershell
.\tools\run_c11a_visual_bulk_qa.ps1
```

C11-A output is isolated under `qa/c11a_visual_qa/`.

The package does not modify C6-F0.8 or C10 runtime code.
