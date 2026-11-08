# C11-D/E Blocker Remediation Register — V18

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

The first correction installer V1 stopped at complete preflight on `docs/current/e/C11D_E_BLOCKER_REMEDIATION_REGISTER_20261108_V19.md`, because it treated a new successor-version path as an existing same-path replacement. No files were copied/replaced. Actual installed predecessor is V16 (SHA `4b1ab75a5610d4996100340c44c57573c8594ee0cff8d25bb126acb2c0ca2380`). V2 uses ADD for all successor-version documents and pins the real predecessor paths separately. It uses same-path PINNED_REPLACE only for the Python validator, with exact installed V1.1 SHA.


## R1V Windows path-budget correction (2026-11-08)

The V2 lineage fix installed successfully (`PASS_PINNED_CODE_REPLACEMENT_AND_ADD_ONLY_DOCS`). The active Windows wrapper then passed all 52 integrated tests (0 errors, 0 failures, 0 skips). The audiovisual capture stage reused the accepted Fractal Bloom A source and stopped before starting any new C11-C launcher, audio generation or AAC mux.

The captured exception named the planned `*_r1v_source_ffprobe.json` output under the new run tree. That path measured 264 characters; the corresponding stderr sidecar path measured 275 characters, exceeding the conservative Win32 `MAX_PATH` budget. This is treated as a path-length compatibility defect, not a missing prior capture or media/encoder failure. The evidence ZIP confirms the prior Fractal A folder and its six required source artifacts are present.

Prepared correction V1: use compact 16-character run folder IDs (`Q5_HHMMSS_XXXXXX`) and preflight all 140 planned paths using Windows semantics. The real checkout root and selectors yield a maximum path of 257 characters; any planned path above 259 is rejected before output-root creation or external process launch. Test 04 retains the suite count at 52 and includes this regression.

No launcher was started in the failed A/V attempt; completed A/V outputs=0, music generations=0, AAC muxes=0. Do not repeat the 52-test acceptance except through the integrated wrapper, and do not rerun R1P, Option C or the prior Fractal A source capture. C11-C frozen manifest and all production locks remain unchanged.


## Windows path-budget installer V1 pin typo — superseded by package V2

The operator attempted the path-budget installer package V1. It stopped during `VERIFY_FROZEN_BASELINE_V2_RECEIPT_AND_FAILED_RUN_EVIDENCE`, before staging or applying any payload. The expected wrapper receipt SHA in V1's manifest was malformed (65 hexadecimal characters): `1d3be8687d2c7b937b388883c9e3f3a167c0ed71e02ea4869305c56ab4905e92d`. The receipt extracted from the supplied wrapper evidence ZIP is the valid 64-character SHA-256 `1d3be8687d2c7b937b388883c9e3f3a167c0ed71e02ea486930c56ab4905e92d`.

Corrective package V2 changes the manifest pin to the verified value, validates all non-null SHA-256 fields as exactly 64 hexadecimal characters before checking checkout files, and excludes incidental `__pycache__` bytecode from the ZIP. It retains the path-budget code/test payload and pins, predecessor checks, C11-C freeze hash and governance scope. V1 made no checkout changes; do not retry it.
