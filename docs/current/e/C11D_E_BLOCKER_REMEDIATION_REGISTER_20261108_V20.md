# C11-D/E Blocker Remediation Register — V18

## Current active blocker — FFmpeg 9 in-memory pixel decode (2026-11-08)

**Status:** `BLOCKED_ON_CORRECTION_INSTALL_AND_WINDOWS_REEXECUTION`.

The path-budget correction V2 is installed; its Windows wrapper preflight passed 52/52 with zero skips/errors/failures. A/V run `Q5_022257_316922` reused accepted Fractal Bloom A and failed before any new source launcher, music generation, AAC mux or A/V completion. FFmpeg 9.0 stderr: `Unrecognized option 'vsync'. Error splitting the argument list: Option not found`.

**Cause:** the in-memory pixel decoder still used removed legacy `-vsync 0`.

**Remedy prepared:** replace only this flag with output-per-stream `-fps_mode passthrough`, preserve pipe-to-memory YUV420P frame hashing and 660-frame equality, improve stderr diagnostics, and add assertion in existing test_04 without changing 52 total tests. Package `C11E_R1V_FFMPEG9_PIXEL_DECODE_FIX_V1_20261108.zip` requires pinned path-budget V2 receipt, exact failed evidence and all 11 predecessor docs. Windows FFmpeg 9 confirmation remains pending.

**No-go boundary:** do not repeat Fractal A, R1P, Option C or a silent-only phase. The next action is correction install PASS, then one integrated wrapper run. General production gates remain unchanged and blocked.

## R1V capture-log false negative

- Prior C11-C launcher for Fractal Bloom A exited 0 and created a valid silent H.264 MP4; operator visual review confirms the Loop/layers are correct.
- V3 runner failed after one launcher because it expected ASCII `720x1280@30`; Godot 4.7.1 writes UTF-16LE with `720×1280 @ 30 FPS`. It also expected `yuv420p/tv` where C11-C produced `yuvj420p/pc`. This is a validator bug, not a launcher failure. Reuse the existing pinned capture; do not rerender A.

## R1V audio integration amendment

- Operator approved the bounded integrated A/V qualification (5 × A/B = 10 outputs, 9 new source captures + reused Fractal A). Use existing C11-C FAMILY_MUSIC_V4 helper and profile registry. Pass R1P music_seed; never gameplay seed.
- Loop music profiles remain C11-C family-specific; do not use D3 V5 (Challenge-only). Preserve H.264 with `-c:v copy`, mux only AAC 192k/44.1k/stereo, FFprobe the final container.
- Old R1V silent-only policy and approval are immutable. New amendment supersedes only the prohibition of audio/mux for this exact R1V A/V test. General D4.8 policy still DISABLED.

## Final review findings before integrated A/V package

- The original source capture confirms Godot writes a Unicode multiplication sign and spaces in the Movie Maker geometry line; the parser accepts UTF-16LE BOM and exact dimensions/FPS/frame count. Source pixel-format/range is pinned to observed `yuvj420p/pc` or the explicit alternative `yuv420p/tv`; mismatched pairs fail closed.
- Five native C11-C FAMILY_MUSIC_V4 WAVs and repeated outputs were tested locally for deterministic PCM16/44.1 kHz/stereo and profile RMS/peak limits. A reference AAC mux confirms H.264 elementary-stream identity with `-c:v copy` and a separate AAC stream. These are local engineering validations, not Windows A/V qualification receipts.
- Second installer review corrected two schema/path issues before packaging: the new amendment/approval files are validated from the ZIP payload before installation; the Option C installation receipt uses `status`, not `install_status`. The combined test report includes skip count and Windows wrapper requires zero skips.

## Apply and execution safeguards

- Installer V4 is PowerShell-only, with no Python invocation or repeated test suite. It verifies every payload hash, parent evidence, policies, source pins, PowerShell AST and collisions, then add-only copies.
- Wrapper runs one combined 52-test suite through direct Python 3.13 and redirected native streams. No standalone tests or manual launchers.
- Different-byte collisions abort; identical files verify/skip; no overwrite. Preflight checks Fractal A evidence and all output/temp roots. Runner stops fail-closed and preserves partial evidence; no cleanup or rerun of prior roots.

## Other historical blockers

- E4A.6 `GeneradorMaestro.gd` postimage remains a known baseline candidate-policy conflict. Do not restore it or soften the candidate rule; progress with the independent Option C D compositor.
- D compositor is not implemented. D9.10 PREPARE_ONLY.
- D9.14/D9.16 BLOCKED, D9.17 BLOCKED_NO_GO, D10 BLOCKED_FOR_PROMOTION, release authority NONE.
- E4C Drill, E5, Smoke18, Matrix101 and E8 remain downstream. CH_008/009 remain held until the 11s/12s timing contradiction is formally resolved.

No Git inspection/bookkeeping. Operator owns commits. C11-C 2.19.12 and all protected paths remain immutable.


## Resolved R1V lineage blocker — prior report field mapping (V2 installed)

**Observed:** V1.1 installation passed 21/21. The first wrapper had one test_20 schema error; the V2 lineage fix installed successfully (12/12). The subsequent Windows wrapper `R1V_AV_WRAPPER_V1_20261108_003543_5D7E5320` passed 52/52 with zero skips/errors/failures; receipt SHA `1d3be8687d2c7b937b388883c9e3f3a167c0ed71e02ea4869305c56ab4905e92d`.

**Root cause:** `verify_prior_fractal_a()` incorrectly requested `report.governance.d4_8_production_policy_state`. In the exact accepted prior report schema, the field is `report.approval.d4_8_production_policy_state = DISABLED_UNCHANGED`; general production lock is `report.governance.d4_8_general_production = BLOCKED`. Also require `d_renderer_dispatch = OFF` and `release_authority = NONE`. The report, process receipt and prior Fractal MP4 hashes match the hard pins; this is not missing/corrupt evidence and not a launcher or audio failure.

**Resolution:** V2 changed only the lineage assertion in `c11e_r1v_av_family_qualification_v1.py`; the prior Fractal A lineage now passes on the active Windows checkout. No capture, audio, mux, seed, policy or authorization changes were made by that correction.

**Do not:** rerun Fractal A, R1P or Option C; manually run tests or individual launchers; create a silent-only phase. The current active blocker is the Windows path-length compatibility failure documented below.


## Lineage-fix installer packaging correction

The first lineage-fix installer package V1 failed complete preflight because it treated successor document paths (V18/V43/V96 etc.) as existing same-path replacements. It made no filesystem changes. V2 adds those new versioned documents and pins the actual V1.1 predecessor paths/hashes; only the Python validator is same-path pinned replacement. Do not install Library V1.0 and do not manually create successor documents.


## Lineage-fix installer V1 packaging defect — superseded by V2

The first correction installer V1 stopped at complete preflight on `docs/current/e/C11D_E_BLOCKER_REMEDIATION_REGISTER_20261108_V20.md`, because it treated a new successor-version path as an existing same-path replacement. No files were copied/replaced. Actual installed predecessor is V16 (SHA `4b1ab75a5610d4996100340c44c57573c8594ee0cff8d25bb126acb2c0ca2380`). V2 uses ADD for all successor-version documents and pins the real predecessor paths separately. It uses same-path PINNED_REPLACE only for the Python validator, with exact installed V1.1 SHA.


## R1V Windows path-budget correction (2026-11-08)

The V2 lineage fix installed successfully (`PASS_PINNED_CODE_REPLACEMENT_AND_ADD_ONLY_DOCS`). The active Windows wrapper then passed all 52 integrated tests (0 errors, 0 failures, 0 skips). The audiovisual capture stage reused the accepted Fractal Bloom A source and stopped before starting any new C11-C launcher, audio generation or AAC mux.

The captured exception named the planned `*_r1v_source_ffprobe.json` output under the new run tree. That path measured 264 characters; the corresponding stderr sidecar path measured 275 characters, exceeding the conservative Win32 `MAX_PATH` budget. This is treated as a path-length compatibility defect, not a missing prior capture or media/encoder failure. The evidence ZIP confirms the prior Fractal A folder and its six required source artifacts are present.

Prepared correction V1: use compact 16-character run folder IDs (`Q5_HHMMSS_XXXXXX`) and preflight all 140 planned paths using Windows semantics. The real checkout root and selectors yield a maximum path of 257 characters; any planned path above 259 is rejected before output-root creation or external process launch. Test 04 retains the suite count at 52 and includes this regression.

No launcher was started in the failed A/V attempt; completed A/V outputs=0, music generations=0, AAC muxes=0. Do not repeat the 52-test acceptance except through the integrated wrapper, and do not rerun R1P, Option C or the prior Fractal A source capture. C11-C frozen manifest and all production locks remain unchanged.


## Windows path-budget installer V1 pin typo — superseded by package V2

The operator attempted the path-budget installer package V1. It stopped during `VERIFY_FROZEN_BASELINE_V2_RECEIPT_AND_FAILED_RUN_EVIDENCE`, before staging or applying any payload. The expected wrapper receipt SHA in V1's manifest was malformed (65 hexadecimal characters): `1d3be8687d2c7b937b388883c9e3f3a167c0ed71e02ea4869305c56ab4905e92d`. The receipt extracted from the supplied wrapper evidence ZIP is the valid 64-character SHA-256 `1d3be8687d2c7b937b388883c9e3f3a167c0ed71e02ea486930c56ab4905e92d`.

Corrective package V2 changes the manifest pin to the verified value, validates all non-null SHA-256 fields as exactly 64 hexadecimal characters before checking checkout files, and excludes incidental `__pycache__` bytecode from the ZIP. It retains the path-budget code/test payload and pins, predecessor checks, C11-C freeze hash and governance scope. V1 made no checkout changes; do not retry it.

## Latest Windows R1V execution — FFmpeg 9 decode compatibility (2026-11-08)

- Path-budget correction V2 installed PASS: 13/13 payloads; install receipt SHA `f57999151f94f378d08290b15bd30586a2180f855e280ef96b2ff4056b1decc5`.
- Active Windows integrated wrapper `R1V_AV_WRAPPER_V1_20261108_012250_5CC5EFEF` passed 52/52, zero skips/errors/failures; wrapper receipt SHA `f8149461d80029bacbf8aa3ddb59ad33ee75246e5225c176a3190063594380b0`.
- A/V preflight passed with the compact run ID and 257-character max path. It reused the accepted Fractal Bloom A MP4; FFprobe found 660 frames at 720x1280/30 and 22 seconds.
- Run `Q5_022257_316922` failed closed in the in-memory pixel decoder because the host is FFmpeg 9.0 and the code still supplied removed `-vsync 0`. Decoder stderr: `Unrecognized option 'vsync'. Error splitting the argument list: Option not found`.
- No new launcher, music generation, mux or A/V output was started/completed (0/0/0/0). The source MP4 remains pinned/unchanged. Full incident record: `C11E_R1V_FFMPEG9_PIXEL_DECODE_COMPATIBILITY_CORRECTION_20261108_V1.md`.
- Corrective code V1 replaces only `-vsync 0` with `-fps_mode passthrough`, retains rawvideo pipe-to-memory and exact frame hashing, and extends the existing test_04 without changing the combined 52-test count. Error diagnostics now include FFmpeg stderr and decoded/expected frame counts.
- Next step: install the FFmpeg9 pixel-decode fix V1 after exact receipt/evidence/predecessor preflight, then run the same integrated wrapper once. Do not repeat accepted 52-test work manually, R1P, Option C, or Fractal A. No separate silent-only stage.


## Latest operator execution checkpoint — 2026-11-08 (authoritative; supersedes prior next-step text)

- Active checkout: `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. V1.1 A/V overlay PASS 21/21; lineage correction V2 PASS 12/12; path-budget correction V2 PASS 13/13. Latest path-budget install receipt SHA-256: `f57999151f94f378d08290b15bd30586a2180f855e280ef96b2ff4056b1decc5`. Frozen C11-C manifest remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- Active Windows wrapper `R1V_AV_WRAPPER_V1_20261108_012250_5CC5EFEF` passed the combined gate: 52/52, zero skips, errors or failures. Receipt SHA-256: `f8149461d80029bacbf8aa3ddb59ad33ee75246e5225c176a3190063594380b0`.
- A/V run `Q5_022257_316922` passed preflight, reused the accepted Fractal Bloom A, then failed closed during in-memory pixel decoding. Report SHA-256 `67759765d0c4d55737b3480d1d54f56e9b878dde75f2e462225bbc57f5412a70`; process receipt SHA-256 `f904e08edac76d07f5324b88937c71b0104ea1db18201d12154e6ec7df4ec74b`.
- Exact FFmpeg 9.0 stderr: `Unrecognized option 'vsync'. Error splitting the argument list: Option not found`. No new C11-C launcher, WAV generation, AAC mux or completed A/V output occurred. The existing Fractal A source and its MP4 hash remain unchanged.
- Root cause: FFmpeg 9 removed legacy `-vsync`; the compatible per-output video sync option is `-fps_mode passthrough`. The correction preserves in-memory rawvideo pipe decoding, 660-frame identity accounting, and the no-frame-files policy. A local FFmpeg 7.1.5 reproduction returned all 660 frames / 912,384,000 bytes; Windows FFmpeg 9 confirmation remains pending.
- **Current next action:** install `C11E_R1V_FFMPEG9_PIXEL_DECODE_FIX_V1_20261108.zip` from a fresh Downloads folder, then run the existing integrated wrapper once. Do not reinstall V1.1, lineage V2 or path-budget V2; do not rerun R1P, Option C or Fractal A.
- No silent-only intermediate stage. Renderer OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`.

