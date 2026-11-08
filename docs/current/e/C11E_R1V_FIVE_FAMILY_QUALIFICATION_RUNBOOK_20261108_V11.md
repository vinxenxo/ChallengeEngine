# R1V Five-Family Integrated A/V Qualification Runbook — V11

## Predecessor incident disposition

The prior V3 R1V runner launched Fractal Bloom A successfully, then failed at a false-negative log parser. Godot's UTF-16LE log uses `720×1280 @ 30 FPS`; the source MP4 is H.264 High `yuvj420p/pc`. The user's visual review of this source and all layers is PASS. New run reuses this source after verifying the report, receipt, source MP4 SHA, C11-C PASS marker, Godot log, authoring/manifest/FFprobe/social sidecars and raw stdout/stderr hashes. Never relaunch or overwrite Fractal A.

## One installation

Extract the A/V overlay into a fresh Downloads folder, not the checkout. Run `INSTALL_C11E_R1V_FAMILY_NATIVE_AUDIO_AV_QUALIFICATION_V1.ps1` with the active ProjectRoot. The installer is PowerShell-only; no Python, `py.exe`, `Start-Process` or test suite. It validates package manifest and every payload hash, C11-C frozen manifest, R1P/Option C receipts, prior Fractal A evidence, D4.8/R1V policies (new approval amendment read from the package payload), 64 source pins, output authority, allowlisted destinations, PowerShell AST and add-only state. A second review checks exact Option C receipt JSON property names before installation. Identical files verify/skip; different bytes abort. It never overwrites.

## One integrated wrapper

Run only `tools/c11d/d9/RUN_C11E_R1V_FIVE_FAMILY_AV_QUALIFICATION_V1.ps1`. The wrapper resolves direct Python 3.13 once and invokes one combined suite (32 prior R1V tests + 20 A/V tests = 52) with native stdout/stderr redirected to files and numeric process exit. It requires 52 tests, zero skips, zero errors and zero failures before capture. The prior-Fractal-A fixture is expected to execute on Windows; its Linux-only skip is not accepted by the wrapper. Do not run tests separately or invoke launchers manually.

## Ten A/V slots

Selectors are derived from R1P receipts, not hardcoded independent seeds:

| Family | Grammar | Gameplay seed | Music seed | Duration | Cycles | C11-C profile |
|---|---|---:|---:|---:|---:|---|
| Fractal Bloom | radial_bloom | 100006 | 500006 | 22s | 2 | ORGANIC_BLOOM |
| Geometric Waves | harmonic_membrane | 100001 | 500001 | 23s | 3 | CIRCUIT_PULSE |
| Invisible Forces | dipole_field | 100021 | 500021 | 22s | 2 | FLOWING_VECTOR |
| Living Particles | swarm | 100016 | 500016 | 20s | 1 | ORGANIC_BLOOM |
| Sacred Symmetry | astrolabe | 100011 | 500011 | 23s | 3 | ORBITAL_RITUAL |

Each selector has A/B with same gameplay seed and same music_seed. One source (Fractal A) is reused, nine C11-C source launchers are invoked. All ten slots receive family audio and AAC mux in the same per-slot runner.

## Audio and mux contract

Use the pinned `tools/prototypes/c11c_common/C11CSafeAmbient.py` and `generate_c11c_family_music.py`, profile registry `profiles/presentation/c11c_visual_music_profiles.json`, kind `loop`, R1P `music_seed`, cycle count, duration, internal family and grammar. Expected WAV: PCM s16le, 44.1 kHz stereo, exact duration/sample count; peak/RMS constrained by native registry. Native FFmpeg mux maps C video + WAV, `-c:v copy`, AAC 192k, 44100, 2 channels, `-shortest`, faststart. FFprobe must show exactly H.264 video + AAC stereo, duration/rate/frames/layout correct. Extract H.264 elementary streams and require source/final hashes identical. Compare A/B PTS, per-frame pixel hashes, global pixel hash, WAV SHA, AAC elementary SHA and seed domains.

No D3 V5 for Loop; no filters, scale, frame rate conversion, H.264 re-encode, D compositor, D9.10 dispatch, GIF or production release. C11-C source MP4 stays silent and immutable; final A/V file is a distinct artifact.

## Stop and preserve

On any missing pin, policy/approval change, output collision, non-empty temp pattern, launcher non-zero, missing C11-C PASS, sidecar mismatch, PTS/pixel mismatch, audio profile metric failure, mux/probe error, H.264 stream hash difference, A/B divergence or override.cfg unexpected change: stop fail-closed. Preserve partial run folder, process logs and report; never clean/reuse an output root. Installer and wrapper must be run once; no parallel manual steps.

Expected technical result: `PASS_R1V_AV_FIVE_FAMILY_QUALIFICATION_10_OF_10_PENDING_OPERATOR_VISUAL_AUDIO_REVIEW`. This does not replace human review. Fractal A visual is already reviewed; other visual slots and all audio listening remain pending. Only after those reviews will remaining 22 Loop variants be admitted.


## Recovery procedure after the first V1.1 Windows wrapper attempt

V1.1 installation is already accepted in the active checkout (`PASS_ADD_ONLY_INSTALL`, 21/21). Do not reinstall V1.1 and do not install the unrelated V1.0 Library ZIP. The wrapper executed 52 tests, with one error in the prior Fractal A lineage validation; it failed closed before the first launcher.

The exact cause was an incorrect JSON field path in `verify_prior_fractal_a()`. Historical report schema: `approval.d4_8_production_policy_state = DISABLED_UNCHANGED`; `governance.d4_8_general_production = BLOCKED`; `governance.d_renderer_dispatch = OFF`; `governance.release_authority = NONE`. The R1P/Option C/approval hashes and report/process receipt hashes remain valid.

1. Extract `C11E_R1V_AV_PRIOR_CAPTURE_LINEAGE_FIX_V2_20261108.zip` into a new, separate Downloads folder.
2. Run its `INSTALL_C11E_R1V_AV_PRIOR_CAPTURE_LINEAGE_FIX_V2.ps1` against the active ProjectRoot. It is a pinned replacement for one Python module plus synchronized versioned docs/prompts; all current target hashes are preflighted. It does not run Python or launchers.
3. After installer PASS, run the existing integrated wrapper exactly once: `tools/c11d/d9/RUN_C11E_R1V_FIVE_FAMILY_AV_QUALIFICATION_V1.ps1`. Do not run test modules separately.
4. Accept no skips/errors/failures. The active Windows 52/52 test gate is already accepted. The runner must also pass the new Windows path-budget guard (all planned paths <=259) before the integrated ten-output A/V pipeline begins.

This is a validator-only correction. It does not recreate or replace the previously reviewed Fractal Bloom A source, does not add a silent intermediate phase, and does not repeat R1P or Option C. Music remains per-slot FAMILY_MUSIC_V4 using the R1P music_seed followed immediately by AAC mux/FFprobe.


### Correction of lineage-fix installer packaging error

The first lineage-fix installer V1 stopped before changes because it incorrectly expected the new V17 document target to pre-exist. No files were copied. Do not run V1 again. The correct V1.1 checkout predecessors are blocker register V16, roadmap V42, current authority V95, doc index V56, backlog V70, gates matrix V93, Runbook V8, Master/Start V96 and First V20. V2 verifies those old paths/hashes and adds the successors as new versioned files. The Python validator module is its sole PINNED_REPLACE.

Extract the V2 package to a new Downloads directory and require `PASS_PINNED_CODE_REPLACEMENT_AND_ADD_ONLY_DOCS`. Only then run the existing wrapper once.


## R1V Windows path-budget correction (2026-11-08)

The V2 lineage fix installed successfully (`PASS_PINNED_CODE_REPLACEMENT_AND_ADD_ONLY_DOCS`). The active Windows wrapper then passed all 52 integrated tests (0 errors, 0 failures, 0 skips). The audiovisual capture stage reused the accepted Fractal Bloom A source and stopped before starting any new C11-C launcher, audio generation or AAC mux.

The captured exception named the planned `*_r1v_source_ffprobe.json` output under the new run tree. That path measured 264 characters; the corresponding stderr sidecar path measured 275 characters, exceeding the conservative Win32 `MAX_PATH` budget. This is treated as a path-length compatibility defect, not a missing prior capture or media/encoder failure. The evidence ZIP confirms the prior Fractal A folder and its six required source artifacts are present.

Path-budget implementation V1; corrected installer package V2: generate compact 16-character run folder IDs (`Q5_HHMMSS_XXXXXX`) while retaining full UTC timestamps and collision checks in receipts; preflight all 140 planned source/inventory/WAV/delivery paths using Windows path semantics; fail before creating output roots or launching any process if any path exceeds 259 characters. Exact five-selector plan maximum is 257 characters. Test 04 retains 52 tests and includes this regression.

No launcher was started in the failed A/V attempt; completed A/V outputs=0, music generations=0, AAC muxes=0. Do not repeat the 52-test acceptance except through the integrated wrapper, and do not rerun R1P, Option C or the prior Fractal A source capture. C11-C frozen manifest and all production locks remain unchanged.


## Corrected Windows path-budget installer package V2

The attempted package V1 stopped during its first evidence-pin preflight because its expected wrapper-receipt SHA literal contained 65 hex characters. The evidence ZIP's receipt SHA is verified as `1d3be8687d2c7b937b388883c9e3f3a167c0ed71e02ea486930c56ab4905e92d`. Package V1 made no changes. Use only package V2; its installer checks every non-null SHA-256 field for a 64-character hexadecimal form before any file hash comparisons. If V2 install passes (`INSTALL_STATUS=PASS_PINNED_REPLACEMENTS_AND_ADD_ONLY_DOCS`), invoke the integrated wrapper once. The wrapper will repeat the 52-test gate as part of its required integrated flow; do not run it manually beforehand.
