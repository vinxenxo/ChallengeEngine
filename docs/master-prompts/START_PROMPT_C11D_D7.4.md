# START PROMPT — C11-D D7.4

Start from the completed D7.3 canonical catalog.

Run:

`powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\c11d\d7\run_d7_4_catalog_identity_provenance.ps1`

Run it twice. The runner must report PASS/CLOSED, 90 items, 90 core cases, one-to-one true, identity recomputation true, provenance true, negative tests true, current source hashes true, D4.8 BLOCKED, runtime NONE, production false.

If both runs are clean, close the checkpoint with:

`powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\c11d\d7\close_d7_4_handover.ps1`
