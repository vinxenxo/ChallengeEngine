# C11-E E3 recovery / E4A discovery — launcher and installer failure analysis V2

Date: 2026-11-03

## Observed V3 failure
The V3 launcher verified ZIP SHA-256 and extracted the archive successfully. The child installer then failed before any documentation writes because it attempted to open `C11E_E3_RECOVERY_E4A_DISCOVERY_OVERLAY_V2_MANIFEST.json`, which was not in the archive. The archive contained the V3 manifest. The installer also still asserted the V2 overlay ID, so merely renaming the manifest would not have been a valid correction.

## Root cause
V3 updated the manifest and launcher but reused the V2 installer without adapting its manifest filename and overlay-ID contract. This is a packaging/integration defect. E4A source audit was not reached. The previously recovered E3 50/50 test evidence remains valid; no tests or recovery are to be rerun.

## V4 correction
V4 supplies a V3-specific installer which reads the V3 manifest, validates `overlay_id=C11E_E3_RECOVERY_E4A_DISCOVERY_V3`, retains the add-only documentation semantics and protected-file hash preflight, and emits a V3 apply receipt schema. The V4 launcher invokes this installer, then validates the existing E3 recovery receipt and runs the read-only E4A source audit.

## Safety boundary
No production source replacement/addition, renderer invocation, media generation, git operation, C11-C baseline modification, or release authority is authorized by this overlay. The Windows run is still required to establish PASS.
