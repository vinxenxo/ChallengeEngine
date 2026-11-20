# E6 L2 Direct RGB24 — V3 failure analysis

## Operator-confirmed V3 results

V3 installer completed successfully: PS 5.1 AST PASS, 29/29 ZIP members, 24/24 ADD_ONLY postimages, frozen C11-C and D4.8 pins unchanged, 20/20 source dependency pins, receipt layout checks PASS. Install receipt SHA-256: `477db5d7bf0d0a64f22b241e853f3c7b5150c735cdc31272c8624a61fbc0cfda`.

The focused test suite then failed during import because it tried to read `INSTALL_C11E_E6_L2_DIRECT_RGB24_VISUAL_PROBE_V3.ps1` from the repository root. The installer is intentionally a root member of the extracted ZIP and is not among the 24 repository destinations. This was an invalid test fixture assumption, not a missing installed destination.

The V3 runner then stopped before invoking Godot. It expected `CaptureLoopFrame.gd` SHA-256 `348bf590c175f40f313b099b38f876f2ef9083f29783c095dcfd6c44ccdf1d6d`; the active V3 postimage was `a73c9f16a7ed4c8b302538ce704b2d047d4b0e2dcc0c59681a5e080bb8bceb1a` (6,640 bytes). The source pin manifest and execution manifest already contained the latter correct value. The runner literal had not been refreshed after the GDScript postimage was finalized.

## Consequence

No Godot process was invoked by the V3 runner. Do not classify this as a capture failure. Preserve V3 installation receipt, command output and package unchanged.
