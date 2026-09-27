# C11-C Batch Review Runner

## Selective stages

`run_c11c_art_direction_batch_v4.ps1` accepts any combination of:

```powershell
-Loops
-Drills
-Longforms
```

or:

```powershell
-All
```

Examples:

```powershell
# 27 Visual Loops
.\tools\prototypes\c11c_bulk\run_c11c_art_direction_batch_v4.ps1 -Loops -Reset

# 20 Drills + 5 Longforms
.\tools\prototypes\c11c_bulk\run_c11c_art_direction_batch_v4.ps1 -Drills -Longforms -Resume

# Complete review corpus
.\tools\prototypes\c11c_bulk\run_c11c_art_direction_batch_v4.ps1 -All -Workers 7 -Reset
```

Default maximum workers: **7**.

`-Resume` uses persistent stage state plus artifact verification. It never treats an older revision as a completed current render.
