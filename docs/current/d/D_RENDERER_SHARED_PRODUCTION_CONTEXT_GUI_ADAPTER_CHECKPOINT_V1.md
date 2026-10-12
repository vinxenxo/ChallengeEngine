# D9 Shared Production Context GUI Adapter V1 — Checkpoint

## Status

`CONTRACT_AND_TESTS_PREPARED; WINDOWS_CHECKOUT_GATE_REQUIRED`

## Purpose

Provide the future GUI with a D-owned adapter calling the same `prepare_shared_production_context` API used by CLI. The adapter accepts the canonical D9.9 raw request after UI controls have been mapped into the canonical request vocabulary. No GUI-specific catalog, editorial or presentation resolver is permitted.

## Frozen GUI boundary

`c11c-suite/c11c-producer/main.py` and `c11c-suite/c11c-producer/c11d_gui_request.py` are hash-pinned as active inputs for this overlay and remain unmodified by it. The manifest retains the original frozen C11-C hash for `main.py`; the active tree contains pre-existing D-layer differences. `adapter_connected_to_current_gui=false`: this is a stable D-owned seam for the future GUI, not a claim that the current GUI has been patched.

## Contract

- GUI-origin requests require `provenance.request_origin == GUI`.
- Output is exactly the shared backend facade record, so a GUI caller and CLI using the same canonical request receive exact equality.
- Unknown content/family/variant/profile selectors reject through the canonical facade.
- Adapter does not mutate input, persist records, spawn subprocesses or dispatch renderer operations.

## Required local evidence

- GUI source lineage: 8/8
- parent shared facade lineage: 22/22
- Challenges / Visual Loops / Visual Drills: 3/3
- GUI API / CLI exact record parity: 3/3
- negative checks: 5/5
- active GUI source snapshots pinned by this overlay: 2/2
- original frozen C11-C `main.py` manifest hash retained: 1/1
- `c11d_gui_request.py` active bytes match manifest: 1/1
- source drift negative: 1/1

All runtime and release locks remain: renderer OFF; media false; D4.8 BLOCKED; release authority NONE; D9.17 NO-GO; D10 BLOCKED.
