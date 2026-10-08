# C11-D D8.1 Overlay V2

Cumulative repair over the D8.1 V1 overlay.

Fixes the false-positive `D8_0_INVENTORY_DRIFT` caused by comparing D8.0 global workspace-media counts with D8.1 artifact/release-only media counts.

Inventory drift scope: entire workspace media (same universe as D8.0).
Probe scope: media under `artifacts/` and `release/` only.

No media is written or transformed. D8.1 evidence remains the sole write scope.
