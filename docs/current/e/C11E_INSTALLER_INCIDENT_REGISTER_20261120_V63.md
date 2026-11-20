# C11-E Installer and Harness Incident Register — V63

## E6-L2-V1-CAPTURE-001

V1 staged no `TypographyLabel.gd` transitive global class and measured the DPI-dependent root window (658x1170). It is preserved; no source C11-C change.

## E6-L2-V2-INSTALL-002

**Observed:** PS 5.1 AST, ZIP 29/29, 24 destinations, frozen pins, 20 source pins and preflight passed. Installer failed at `File.WriteAllText($sideTmp,...)` with `DirectoryNotFoundException`. Subsequent tests reported the V2 test directory absent; runner `.ps1` was absent.

**Root cause:** final sidecar path was 226 characters; V2 appended `.tmp.` and a 32-character GUID, producing a 263-character path over classic .NET Framework MAX_PATH. The error surfaced as DirectoryNotFoundException. Payload/receipt creation is inside a catch/rollback transaction; preserve all V2 evidence and do not rerun in place.

**V3 remediation:** precompute and budget final/temp paths; create and verify a unique receipt directory before payload writes; use short same-directory `r.<guid>.tmp` and `s.<guid>.tmp` files; stage/validate both before atomic moves; rollback only transaction-owned matching hashes and empty transaction-created directories.

No changes to historical receipts, C11-C, D4.8 or V1/V2 files.
