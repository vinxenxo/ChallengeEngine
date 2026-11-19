# C11-E E6 Option C Native Qt Probe V2.3 — import-path recovery

Date: 2026-11-19  
Package: `C11E_E6_OPTION_C_NATIVE_QT_PROBE_V2_3_IMPORT_PATH_FIX.zip`  
Mode: `ADD_ONLY`; new code and documentation paths only.

## Incident and confirmed boundary

V2.2 installation completed with `INSTALL_STATUS=PASS_ADD_ONLY`, `INSTALL_FILES=9/9 VERIFIED`, and an independently SHA-pinned installation receipt. The V2.2 runner then terminated at:

`ModuleNotFoundError: No module named 'support.a3_lineage_adjudicator_v3'`

The exception occurred on the generic package import after the runner's explicit file-existence and SHA-256 comparison. Because that comparison returns before the import when the file is absent or has a different hash, the observed traceback places the failure at Python package-name resolution, not at the A3 policy validation or QImage runtime. The exact preloaded package-resolution state on the user's Python process was not captured, so this overlay does not claim a more specific cause (such as a confirmed namespace collision).

## V2.3 correction

V2.3 does not use `from support.a3_lineage_adjudicator_v3 import ...`. It loads the adjudicator from its absolute, versioned file path using `importlib.util.spec_from_file_location`, after checking the exact SHA-256 `2094769bba1993f26ca40f36a1070e871d06e0c9b01443d4a3a846136a07e5b7`. The callable entry point is verified before continuing. This avoids relying on the generic top-level package name `support`.

The V2.2 A3 adjudicator content is reused byte-for-byte; only the runner's module-loading mechanism and regression-test imports are changed. The A3 rules remain strict: two independently pinned hash domains, equality of expected/actual claims, exact bridge/source checks, and exact reconstruction with only `/source_lineage/6/sha256` changed.

## Diagnostic coverage

The new runner reports whether the V2.2 adjudicator file is present with the expected SHA, but V2.3 does not depend on it. Four new loader tests include a deliberately preloaded unrelated top-level `support` module, hash mismatch rejection and missing-file rejection. Nine A3 domain-separation regression tests are retained with direct file loading.

## Scope and governance

- Uses the already installed V2 QImage implementation, fixtures and 37-test target suite from `tools/c11d/d9/c11e_e6_option_c_native_qt_probe_v2`.
- Adds a separate runner/evidence root under `...native_qt_probe_v2_3`; does not modify V2, V2.1 or V2.2.
- No renderer, Godot, FFmpeg, FFprobe, audio generation, mux, production dispatch, BatchId consumption or E6 acceptance.
- Frozen C11-C manifest remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` (796,318 bytes); D4.8 V2 remains `0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07` (12,996 bytes).
- `GIT_CHECKS=SKIPPED`; commits operator-managed; source pins enforced.

A successful result remains only `PASS_QIMAGE_STAGE_BENCHMARKED_NOT_END_TO_END`, not E6 acceptance or release authority.
