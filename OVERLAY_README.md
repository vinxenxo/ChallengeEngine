# C11-C 2.19.12 V18 - A1 StrictMode repair + legacy CLI wrapper

ROOT-RELATIVE INCREMENTAL OVERLAY

V18 is a surgical repair on V17. It fixes the observed Windows PowerShell 5.1 StrictMode failure by predeclaring `producer_exit_code` in the per-run record before assigning it at completion.

It also restores a non-authoritative `build_factory.py` compatibility wrapper. The historical factory implementation itself is not preserved in the archived C11-C baselines: both the current 2.19.14 baseline and the frozen 2.19.2 archive contain a zero-byte `build_factory.py`. The V18 file is therefore a reconstructed thin adapter, not a recovered historical factory implementation. It delegates to the canonical C11-C Challenge producer and preserves the legacy CLI shape (`--config`, `--output`, `--no-gif`).

Changed:
- build_factory.py
- tools/qa/c11/run_c11a1_challenge_bulk_qa.ps1
- tests/C11A1FactoryIsolationContractTest.gd

Included for convenience (unchanged from V17):
- FULL_ACCEPTANCE_C11C_2.19.12_A1_SINGLE.ps1
- C11C_2.19.12_A1_CLOSURE_RECEIPT_V18.md
- docs/current/c11c/C11-C_2.19_C11A1_CANONICAL_PRODUCER_CLOSURE_V18.md
- docs/current/c11c/C11C_2.19.12_A1_CLOSURE_CHANGELOG_V18.md

The canonical producer remains authoritative. C11-A.1 itself does not invoke `build_factory.py`; the file exists only as legacy CLI compatibility. No `core/` or engine/simulation files are included.

Apply at repository root with Expand-Archive -DestinationPath . -Force.
