# C11-E E6 Loop Option C — Implementation and Qualification Review V4

**Date:** 2026-11-19  
**Disposition:** `V4_DEPENDENCY_FREE_BUILD_PREPARED / ACTIVE_CHECKOUT_INSTALLATION_PENDING`

## Incident closure

Compositor V3 ZIP SHA-256: `7785fbec6a7052f81d7872adf8671f60652e820242fe855ab3fbd13616541db0`. The operator's Windows PowerShell 5.1 run passed AST, ZIP 15/15, extracted members 15/15, protected pins 15/15, payload pins 11/11, and destination enumeration (11). Python `3.13.14` was present. It then failed because `from PIL import Image` raised `ModuleNotFoundError: No module named 'PIL'`. Exact terminal state: `PILLOW_LANCZOS_PREFLIGHT_FAILED`, `TRANSACTION_STARTED=FALSE`, `PROJECT_PAYLOAD_MUTATION=FALSE`. No project file was written. Do not rerun V3.

This exposes a package defect, not an operator environment defect: the V2/V3 primitive required Pillow although the installer did not install or package it. V4 removes that external dependency rather than asking the operator to modify Python.

## V4 implementation

The D-owned module `tools/c11d/d9/c11e_e6_loop_option_c_frame_compositor_v3.py` consumes one immutable RGB24 byte buffer and returns one 720×1280 RGB24 byte buffer. It uses pure-Python integer overlap weights for exact rational pixel-area averaging. For the approved 720×1280 source the fixed output is 504×896 at `(108,192)` with factor 7/10. The canvas remains black outside the content rectangle.

No Pillow, NumPy, image framework or runtime dependency is required. The module has no filesystem/process effects, no selector/family binding, no E1 dispatch and no renderer/audio/video behavior. It does not rasterize text.

## Filter semantics and visual gate

`EXACT_RATIONAL_AREA_BOX_V1` computes pixel-area overlaps on an integer lattice. Each output pixel's horizontal weights sum to source width and vertical weights sum to source height; the 2D denominator is their product. There is no floating-point resampling and no filter overshoot/ringing. It is not claimed to be perceptually superior to LANCZOS. The output may appear softer; compare synthetic edge/checkerboard/gradient fixtures before any real family media is considered. A local Linux build-environment benchmark on Python 3.13.5 measured 0.818 seconds per 720×1280 frame over three iterations. This is informational only, not a Windows target benchmark, and it does not qualify the module for 30 fps or full Smoke18 throughput.

The approved geometry remains unchanged: 720×1280, black 192 px header/footer, 504×896 content at `(108,192)`, 108 px side gutters. Operator approval applies to geometry, not to the area filter's visual quality.

## Tests

V4 adds 37 offline tests covering exact geometry, source validation, rational axis weights, exact area-overlap bounds, deterministic repeat output, constant-field preservation, checkerboard no-overshoot, RGB24 output size, black reserved regions, immutable input, and absence of external imaging imports. Test runs are isolated and do not create media.

Build environment validation is Python `3.13.5`. The target installer requires exactly Python 3.13.14; that target version and native Windows PowerShell 5.1 AST must be confirmed by the user's installer run.

## Installer V4

The installer performs: PS5.1 AST; ZIP exact-member and extracted-byte verification; manifest/sidecar verification; 9 payload SHA/byte pins; 15 protected source pins; Python 3.13.14 check; staging compilation 2/2; 37 tests with zero skips; aggregate collision report; final pin/destination recheck; then ADD_ONLY transaction. It does not run pip, install dependencies, inspect Git, execute renderer/media tools or mutate C11-C/D4.8.

All V4 documentation is stored under the package-specific path `docs/history/c11e/overlays/C11E_E6_OPTION_C_COMPOSITOR_V4_20261119_2040Z/`. Canonical current authority, doc index and pre-existing prompts are not replaced. The overlay's handover and prompts are supplementary and direct the next window to read the active canonical checkout docs first.

## Roadmap

After the V4 install/test receipt, proceed in this order: (1) create and inspect synthetic visual fixtures; (2) benchmark full-frame throughput on target Windows Python 3.13.14 and set a measured admission limit; if per-frame throughput is not acceptable, move hot-path resampling to an already-authorized native D/Godot boundary rather than wiring this Python loop into 30 fps; (3) specify typography, fonts and hashes, shaping, fallback, wrapping, overflow, clipping and opacity; (4) connect only at the existing D-owned Option C boundary and qualify 27 Loop selector bindings; (5) complete the Challenge E6 editorial successor without changing E4A V1; (6) requalify the 13 reuse candidates and freeze 18 Smoke18 rows (6/6/6, with Challenge A/B/C nested); (7) prepare a separate scoped D4.8 successor and exact E6 TEST_ONLY manifest; (8) only then render visuals and family-native audio/A/V under exact pinned authority.

## Protected invariants

C11-C manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` is immutable. D4.8 V2 SHA-256 `0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07` remains unchanged and globally BLOCKED. E1 PREPARE_ONLY; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; renderer OFF; dispatch/media OFF; release NONE; E6 accepted 0; no Matrix101 freeze. No Git checks. No Godot/FFmpeg/FFprobe/audio/mux/media/BatchId in V4.
