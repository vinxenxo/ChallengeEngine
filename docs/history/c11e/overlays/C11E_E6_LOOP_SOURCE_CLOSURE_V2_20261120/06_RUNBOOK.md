# Loop source closure V2 runbook

1. Verify ZIP SHA-256 against the `.sha256` sidecar; extract only to a new temporary folder, never over the active checkout.
2. Execute `INSTALL_C11E_E6_LOOP_SOURCE_CLOSURE_V2.ps1`. Require PS 5.1 AST PASS, frozen C11-C and D4.8 pins, 23/23 package members, 22/22 ADD_ONLY destinations, and repository postimage verification.
3. Run the V2 focused suite at `tests\\c11e\\e6_loop_source_closure_v2` once: 37 tests.
4. Run `tools\\c11d\\d9\\RUN_C11E_E6_LOOP_SOURCE_CLOSURE_V2.ps1` once with Python 3.13.14.
5. Preserve receipt and sidecar. Expected only if all other inputs are unchanged: 116 PASS, 2 PENDING, 0 BLOCKED, source media rehash complete, six selectors. A different count must be investigated, not forced to the expected result.
6. The two PENDING states are colorimetry and operator visual review. `qimage_real_rgb24_buffers_present=false` and `L2_ready=false` remain in the receipt.

No Godot, FFmpeg, FFprobe, audio generation, mux, renderer, dispatch or media creation is invoked.
