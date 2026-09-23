# C11-C Production 25 Batch Hotfix v2.1.6

Fixes production candidate validation so a family's accumulated prototype media cannot interfere with the current seed.

The production runner validates the exact canonical seed MP4 (`<ProductId>.mp4`) and the exact seed sidecars only; it no longer counts all MP4s in the family prototype directory.

Use:

```powershell
.\tools\prototypes\c11c_bulk\run_c11c_production_25.ps1
```

This tool does not clean prototype artifacts and does not delete existing production products unless `-Force` is explicitly supplied.

## v2.1.6 fix

The canonical production runner no longer counts every `.mp4` in a family staging directory. It validates the exact current seed candidate (`<ProductId>.mp4`) and its exact seed sidecars, so previous prototype renders cannot invalidate a new production run.
