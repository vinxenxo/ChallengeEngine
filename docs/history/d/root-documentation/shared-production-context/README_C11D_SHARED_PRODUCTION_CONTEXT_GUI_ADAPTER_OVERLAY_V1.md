# C11-D Shared Production Context GUI Adapter Overlay V1

Additive D-owned integration seam for the future GUI. It accepts a canonical D9.9 request assembled from GUI selections and delegates to `prepare_shared_production_context`; it does not duplicate content-family selection, editorial resolution, profile validation or plan composition.

The active Producer GUI controller and helper are hash-pinned read-only by this overlay. The release manifest retains the original frozen C11-C hash for `main.py`; the active working tree has pre-existing D-layer differences. This overlay does not modify existing GUI files and does not silently wire the adapter into the current GUI.

Validation: run `python -B .\tools\c11d\d9\test_shared_production_context_gui_adapter.py`. Expected: 8/8 GUI lineage pins, parent facade pins 22/22, content types 3/3, API/CLI parity 3/3, negative checks 5/5, active GUI source pins 2/2, original manifest main.py hash retained 1/1, GUI helper manifest match 1/1, and source drift negative 1/1. No renderer dispatch, output persistence or media creation is enabled.
