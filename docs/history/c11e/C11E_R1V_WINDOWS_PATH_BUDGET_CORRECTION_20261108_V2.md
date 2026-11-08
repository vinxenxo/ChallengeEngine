# C11-E R1V Windows path-budget correction — V1



## R1V Windows path-budget correction (2026-11-08)

The V2 lineage fix installed successfully (`PASS_PINNED_CODE_REPLACEMENT_AND_ADD_ONLY_DOCS`). The active Windows wrapper then passed all 52 integrated tests (0 errors, 0 failures, 0 skips). The audiovisual capture stage reused the accepted Fractal Bloom A source and stopped before starting any new C11-C launcher, audio generation or AAC mux.

The captured exception named the planned `*_r1v_source_ffprobe.json` output under the new run tree. That path measured 264 characters; the corresponding stderr sidecar path measured 275 characters, exceeding the conservative Win32 `MAX_PATH` budget. This is treated as a path-length compatibility defect, not a missing prior capture or media/encoder failure. The evidence ZIP confirms the prior Fractal A folder and its six required source artifacts are present.

Correction: generate compact run folder IDs (`Q5_HHMMSS_XXXXXX`) while retaining full UTC timestamps and collision checks in receipts; preflight every planned source, inventory, WAV and delivery artifact path using Windows path semantics; fail before creating output roots or launching any process if any path exceeds 259 characters. The existing 52-test count is retained; test 04 now includes the Windows path-budget regression.

No launcher was started in the failed A/V attempt; completed A/V outputs=0, music generations=0, AAC muxes=0. Do not repeat the 52-test acceptance except through the integrated wrapper, and do not rerun R1P, Option C or the prior Fractal A source capture. C11-C frozen manifest and all production locks remain unchanged.


## Installer package V1 pin defect and V2 correction

V1 package preflight aborted before writes. It pinned the wrapper receipt with a 65-character malformed SHA string. Direct extraction of the receipt from the uploaded `R1V_AV_WRAPPER_V1_20261108_003543_5D7E5320.zip` confirms SHA-256 `1d3be8687d2c7b937b388883c9e3f3a167c0ed71e02ea486930c56ab4905e92d`. V2 corrects that literal and adds manifest-wide SHA-256 format validation (64 hexadecimal characters). No changes to the underlying path-budget module/test behavior or A/V pipeline.
