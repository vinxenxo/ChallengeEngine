# C11-E Current Authority — V71

**Date:** 2026-11-06. Supersedes V70 for the current execution point. Records the operator-confirmed E4A.7 listening PASS and the V1 D99 runner failure, with the corrected V2 runner as the immediate recovery. It does not close full E4A or change production authority.

## Checkout authority and frozen baseline

The only code authority is `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. Evidence ZIPs are not checkout overlays. The operator commits each iteration. No per-iteration runner may execute Git, inspect HEAD/status/branch, require `.git`, compare commit IDs or manage refs. Use exact source SHA-256 pins and the frozen C11-C manifest.

C11-C 2.19.12 remains the only production baseline. `release/C11C_FREEZE_PACKAGE_MANIFEST.json`: 796,318 bytes; SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

## E4A.6 — D-composited visual / reserved bands

**Disposition: `PASS_TEST_ONLY_USER_VISUAL_REVIEW`.** Recovery V1.2 receipt SHA-256 `3279011fa16479d4901c5b271463707a437ce7458d306c1667ab222cb1603980`. The operator confirmed visual inspection PASS on 2026-11-06.

- Exact silent visual input: `artifacts/tests/c11e/e4a6_reserved_bands_black/RECOVERY_V1_2/CHALLENGE_004_D_BLACK_BANDS_720x1280_30FPS_SILENT.mp4`.
- SHA-256 `841b03531301c7e70c0e09ce3e9f536241d2072a87792e099ed7a955bef8c52f`; 671,647 bytes; H.264 High, 720×1280, 30 FPS, 450 frames, 15 s, yuv420p/TV, zero audio streams.
- 8 delivery-boundary stills; inactive black 12/12 PASS (RGB max tolerance 3); active HOOK/CTA 4/4 PASS. 22/22 focused Python tests, Godot editor import, 900-frame live-root and Movie Maker evidence were reused, not rerun.
- No renderer/gameplay rerender occurred during recovery. The incidental PCM in the AVI was discarded.

This is approval of the specific test output, not a blanket layout policy or production authorization. HEADER/FOOTER reserved-black invariant remains; user-selectable BODY background is a separate future editorial capability and not a blocker.

## E4A.7 — D-composited Challenge A/V

**Disposition: `PASS_ISOLATED_E4A7_D_COMPOSITED_CHALLENGE_AV_TEST_ONLY`.**

Execution evidence:
- Run ID: `20261106T070808Z-62F31F9C`.
- Evidence ZIP: `RUN_20261106T070808Z-62F31F9C.zip`; SHA-256 `ad4024cc6caa3b9140a284390b852c76f3dcd5d50d88cf03813d6bb4e374d293`; 67,118,130 bytes; 268 ZIP entries; CRC check PASS.
- Receipt SHA-256 `102cf07a0b8920318c3ba211a3bd4374c3e080018486363d701f81e65613aaa0`.
- Report SHA-256 `efb0f1a9245d3fce15bf48041c8972e90f6874d308fa99340afb5c731f94403a`; receipt's report pin matches.
- `SHA256SUMS.txt`: 267/267 entries verified, no missing or mismatched files. 55/55 process exit-code artifacts equal zero; non-empty stderr files contain normal FFmpeg filter/volume diagnostics, not failed exits.
- Documentation archive/install receipt: 13/13 files have matching paths, byte counts and SHA-256.

### Audio determinism and seed isolation

- D3 V5 engine `c11d_music_engine_v5` version 5.0, profile `challenge_8bit_v1` v1.0, 15 s output, 22,050 Hz stereo raw WAV.
- Gameplay seed 314159 for all cases. Music seed 840001 for A/B; 840002 for C. These are test fixtures, not product defaults. Variation 0.
- Raw A/B WAV SHA-256 `6956653f91a5bff2359426d6bcc7cd24eff599d840dbb6e431ff26b00960a96c` (byte-identical); C `1b2fdaf9ac5b377aa89cba7317d36aa4ea0a9a655be31569142f1d65e5f0a6ed` (different).
- D3.3 mastered 15 s WAVs are PCM S16LE, 48 kHz, stereo. A/B SHA-256 `50018594902f11bc9f8800b6ce773d3bbd77ed4d64bc5401cbdf8e8d626ddb03`; C `85909dc4898f8a0207cc7f829cec736a8cffa67c751981559f2bc8069a91234e`.
- D3.3 30 s repeated QA windows measure −14.0 LUFS; LRA 0.1 LU; true peak −6.4 dBTP A/B and −6.1 dBTP C. `TP=-1 dBTP` is the ceiling, not a target to hit; outputs remain below it. No hard clipping. All mono-compatibility/audibility checks PASS.
- Decoded AAC PCM A/B SHA-256 `3d6bfd12b80aae6684b69fbdf67bbd51488256d2c7f828a935f541cf42762f01`; C `83aaad64daad6c2c23e64ee3e5909eb748b2b4a462eae11b10f7a14ec4a50d7f`.

### Mux and source-video identity

- The input is exactly the user-reviewed E4A.6 MP4 above. It was not re-rendered or re-encoded.
- Source H.264 elementary stream SHA-256 `6164e47adc8fd09cef3eea3780b77fbced007acba17a6939de7437bcf485ed5e`; all A/B/C extracted mux video streams match it byte-for-byte.
- Each output contains one H.264 High 720×1280/30 FPS/450 frame/15 s video stream and one AAC-LC 48 kHz stereo stream. Audio is non-silent. FFprobe start/end drift is 0.000 s for all three.
- MP4 A and B are byte-identical: SHA-256 `03f5f93322d30d138e63c43eb590848bf7e28f91ab9e1b2123666ce3881c138b`; 1,045,687 bytes.
- MP4 C differs only because the changed music seed changes audio: SHA-256 `41b9a361a052ef1abef4aef154e55a96891cf9e6c843a9c00f4e2532bb71b8df`; 1,044,513 bytes.
- FFmpeg/FFprobe 9.0.

### Test fixture caveats

E1 leaves `tempo_bpm` and `duration_seconds` unresolved. The test used 104 BPM explicitly as the historical D9.2 pilot fixture (`HISTORICAL_D9_2_PILOT_FIXTURE_NOT_PRODUCT_DEFAULT`) and obtained 15 s from FFprobe (450/30). This does not define a product default and does not authorize changes to E1.

The A/B/C intents in E4A.7 use `request_origin=TEST` and each is `PASS_E1_PREPARATION_ONLY`; they do not prove a physical GUI session. All test dispatch/renderer/production-media flags are false; no D3 engine, C11-C generator or core audio source was modified. Frozen C11-C manifest SHA remains unchanged.

## Remaining work to close full E4A

1. Listening review of A/B/C was explicitly confirmed PASS by the user; do not repeat it.
2. Apply the hash-gated D99 GUI contract patch with `APPLY_C11E_D99_GUI_EDITORIAL_CONTRACT_FIX_V2.ps1`. V2 repairs the V1 installer mechanics only; the approved `main.py` postimage and regression test remain byte-identical. It performs the source-pin checks, focused tests, atomic replacement with a valid same-volume backup path, and add-only installation of the 14 versioned documents.
3. Run the existing Producer GUI plan callback once with the exact `REVIEW_720` / personalization-enabled fixture in the E1 GUI/CLI parity plan V3. It compares E1 GUI intent to E1 CLI and D9 GUI plan to D9 CLI, writes parity/lifecycle receipts, and does not dispatch or create media.
4. Close full Challenge E4A only after the V2 source patch and new GUI/CLI parity run PASS.

Do not rerun E4A.6 or E4A.7 unless evidence/source pins drift or a specific defect is found. Do not rerender gameplay. After full E4A only: E4B Loop, E4C Drill, E5, E6 Smoke18, E7 Matrix101, E8.

## D99 GUI request contract incident and surgical disposition

The user reported `Unknown universal request field(s): presentation_options` on RESOLVER. The supplied `D99-GUI-D22A8281E993.zip` (14 entries; run timestamp 2026-11-06 11:21:14 local) does not reproduce that exception: its `c11e_gui_cli_parity.json` is PASS, `gui_cli_parity.json` is PASS, `producer_universal_receipt.json` is `PASS_BRIDGE_PLANNING_ONLY`, and `c11e_production_intent_receipt.json` is `PASS_E1_PREPARATION_ONLY`. In that successful run `request.json` contains the E1-only `presentation_options`, while `d9_request.json` excludes it and `canonical_request.json` has no such field. Treat it as successful evidence, not the failing stack trace.

Nevertheless, the active GUI must not expose or serialize a visibility option at this stage. A surgical D-owned GUI patch is prepared against the reviewed `main.py` preimage SHA `9685c4346cf56d3134fbf296585efbd779e5695635a249f0b85bd2c3682dac4e`: remove the Hook/countdown checkbox and all GUI request serialization of `presentation_options`; leave the E1 service unchanged. E1 continues its existing Challenge default internally (`show_hook_countdown=true`) when the GUI option is absent. D9.9 remains strict and receives only its canonical request. No D9.9 schema, E1 service, renderer, binder, C11-C file or D3 engine change is required.

The D9.8 editorial model already carries every allowed field in the canonical editorial object. Challenge always has `title`, `subtitle`, `call_to_action`, `language`, `player_name`, `challenge_label`; Loop and Drill have the four shared fields. An empty input normalizes to `UNKNOWN` under the existing D9.8 policy (`empty_optional_string=NORMALIZE_TO_UNKNOWN`); it does not remove the key. Do not invent a future per-field selection system now.

The supplied V70 snapshot records the exact `main.py` preimage SHA `9685c4346cf56d3134fbf296585efbd779e5695635a249f0b85bd2c3682dac4e`; all seven supporting pins and the frozen C11-C manifest also match. The operator's V1 runner reached the source-apply stage after PASS preflight: PowerShell 5.1 AST PASS, Python 3.13, E1 19/19, D9.9 matrix PASS and focused D99 tests 3/3. It then failed at `[IO.File]::Replace($TempMain,$MainPath,$null)` because the null backup path is rejected by the active PowerShell/.NET overload. Its catch receipt also contains bare `false` tokens instead of `$false`, causing a secondary `false` command-not-found and preventing a clean failure receipt. There is no V1 success receipt or evidence that the `main.py` replacement completed; the supplied V70 snapshot itself still carries the preimage SHA. V2 supplies a valid unique same-volume backup path to `File.Replace`, verifies that backup against the preimage SHA, and uses PowerShell `$false` literals in receipt data. V2 keeps the original 16-file embedded payload contents except for versioned documentation: the `main.py` postimage remains 110,183 bytes / SHA `4141072659f307468900c1cfb09774479abc6c10abae6ae638a11192cfcd04e6`, and the focused test remains SHA `872bfd49a99b289b1980feb06d38e44dc55766818fe344fcf3678bcc7d3f325d`. The V2 runner repeats all mandatory source-pin and test preflights, refuses any source state other than the exact preimage or exact postimage, and keeps all document destinations add-only. Apply it once; then keep full E4A open until a new post-patch GUI run has PASS receipts and no resolver exception.

## D99 runner V1 failure and V2 recovery

The V1 run ID was `D99_GUI_FIX_20261106_115614_710`. Its captured process records establish that Python 3.13 preflight exited 0, E1 service tests were 19/19 PASS, the D9.9 matrix passed (Challenge 9/9, 32 Loop selectors, Drill 20/20, CLI parity 3/3, negatives 20/20), and the new focused GUI/editorial tests were 3/3 PASS. The runner stopped during `SOURCE_BACKUP_AND_APPLY`; the reported `System.ArgumentException` originated from the null third argument passed to `System.IO.File.Replace`. The subsequent catch failure came from unprefixed `false` tokens in receipt hashtables. Therefore the V1 attempt is BLOCKED, not a source-patch PASS.

V2 changes only the runner: it passes a new, run-scoped backup pathname on the same volume to `File.Replace`, verifies that atomic replacement backup equals the exact `main.py` preimage, and corrects all boolean values to `$false`. It reuses the already-reviewed source postimage and focused regression test unchanged. It embeds the current versioned docs directly, with fresh, non-colliding names; no standalone documentation installer is needed. It does not invoke Git, render, dispatch, or create media.

V2 must print `C11E_D99_GUI_EDITORIAL_CONTRACT_FIX=PASS_SOURCE_AND_TESTS`, verify the exact `main.py` postimage and produce `C11E_D99_GUI_CONTRACT_FIX_RECEIPT.json` before the GUI retry. If the source is already the exact postimage, the runner treats it as already applied; any other source hash stops before writes.

## Governance locks

C11-C 2.19.12 remains the only production baseline. `renderer=OFF`; production dispatch/media OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`. No core/C11-C source, mechanics, RNG, binders, timelines, simulation truth, shared presentation or manifest modifications. No sixth module, second Producer or parallel binder.


## Editorial payload invariant

The GUI patch removes only the premature Hook/countdown checkbox and the E1-only `presentation_options` key. It does not remove or make optional the editorial inputs. The raw universal request always contains the `editorial_profile` and `production_override` containers; D9.8 canonical editorial output always contains all six Challenge fields or all four Loop/Drill fields. Empty optional strings normalize to `UNKNOWN` under the existing D9.8 policy; their keys are never omitted. The existing global personalization enable control remains unchanged.
