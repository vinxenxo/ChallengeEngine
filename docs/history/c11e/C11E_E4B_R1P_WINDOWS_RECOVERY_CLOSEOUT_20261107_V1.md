# C11-E E4B R1P — Windows Recovery Closeout V1

**Date:** 2026-11-07  
**Disposition:** `CLOSED_PASS_27_OF_27`

The operator installed the archive-recovery add-only overlay (12/12) and ran the recovery-only verifier for `E4B_R1P_20261107_032743_5F75045C` in the active Windows checkout. Console status: `PASS_R1P_ARCHIVE_RECOVERED_AND_PAYLOADS_REVALIDATED_27_OF_27`; process exit 0; 30/30 live source pins; live Python/Godot executable pins PASS. No Godot rerun, recipe regeneration or source mutation occurred.

## Operator console pins

- Package manifest: `9caf06569abaeb63538dd48fe9314b6036098fc3bb7d71d44dac3dd707f0950f`
- Install receipt: `deb24b8f7583dd0b22b04797fc61bbbe9a4466a07195c93cd12f2ec701436142`
- Recovery verifier: `6f22082b9ee457fe5bf93ef1c2e5822316888141078574d310d8049a0739c027`
- Recovery stdout: `b004a48b98e34b9eb4cf1ca14e3d9ea8b9f223c998b4c0eabd6ab7faac7f77ce`
- Recovery stderr: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Recovery process receipt: `b4299cca349b646cc05fffaf83765f5108ad55b70d177d27ce0745031a4c07a0`
- Recovered ZIP: `d49f54ffdee6026426c2bb87fcb72b5c8a68f09cb64fb91f71e25dc10fd26b52`
- Recovery report: `6bd16983a01919c7c41f785b281988139ae2a569a23daa81db6a20694f21c640`

## Independent library archive pair review

The two uploaded ZIPs were inspected read-only. The original archive SHA is `a3bb4ddd6f4933026b0221c7e0eb1b62ffe40d477d72ce0190bbe9587b67b800`; the recovered archive SHA is `d49f54ffdee6026426c2bb87fcb72b5c8a68f09cb64fb91f71e25dc10fd26b52`.

After replacing `\\` with `/` in original ZIP member names, both archives contain the same 72 normalized paths and every member byte stream is identical. All 27 canonical receipt hashes and SHA sidecars pass; all 27 deterministic repeat payload hashes match; family counts are 5/5/7/5/5; source-manifest pins match V84 30/30; and captured R1P subprocess log hashes match the embedded receipt. The separate operator Windows recovery output records 30/30 source pins against the active checkout.

R1P timing descriptors across 27 selectors are 8×20 s/600 frames, 7×22 s/660 frames and 12×23 s/690 frames at 30 FPS. These remain predicted timing descriptors, not actual frame inventories.

## Scope boundary

R1P is closed for parameter payloads only. No launcher, prototype instance, renderer, frame buffer, actual frame inventory, pixel payload, D3/audio, FFmpeg, mux or media was invoked. R1V is a new stage and remains separately gated.
