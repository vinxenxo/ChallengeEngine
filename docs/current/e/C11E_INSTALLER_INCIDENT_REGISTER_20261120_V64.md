# C11-E Installer and Runner Incident Register — V64

| Incident | Cause | Disposition |
|---|---|---|
| L2 V2 installer | Long sidecar temp path exceeded classic MAX_PATH | V3 introduced short sibling temp names and pre-created receipt directory; preserved. |
| L2 V3 tests | Test module assumed installer was copied to repository root, but installer is a package root member | V4 uses `C11E_L2_INSTALLER_SOURCE` supplied from extracted ZIP root; no installer destination added. |
| L2 V3 runner | Stale `CAPTURE_GD_SHA`/bytes literal differed from final GDScript pin manifest | V4 derives final harness hash/bytes and aligns runner constant; focused regression tests assert equality. |

V3 installation receipt is preserved. Do not repeat V3. No edits to C11-C or D4.8.
