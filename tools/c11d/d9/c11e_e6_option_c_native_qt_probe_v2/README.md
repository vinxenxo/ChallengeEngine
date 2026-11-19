# C11-E E6 Option C Native Qt/QImage Probe V2

V2 fixes the A3 preflight classifier/validator defect from V1. It preserves the existing QImage compositor V1 implementation and its 37 target Qt tests. It validates the historic/current review-manifest file hashes and structurally reconstructs the exact postimage with one approved JSON pointer update; it does not compare whole-file SHA values to pointer hashes.

Install add-only using `INSTALL_C11E_E6_OPTION_C_NATIVE_QT_PROBE_V2.ps1`. Run `RUN_C11E_E6_OPTION_C_NATIVE_QT_PROBE_V2.py` with Python 3.13.14 and PySide6 6.11.2. Package output path: `artifacts/tests/c11e/e6_option_c_native_qt_probe_v2/<RUN_ID>/`.

This is a synthetic L1 probe only. It creates no video/audio, calls no media tool, does not integrate into E1 or a family stage, and does not accept Smoke18/E6. Geometry is approved; resampler quality remains pending human review.
