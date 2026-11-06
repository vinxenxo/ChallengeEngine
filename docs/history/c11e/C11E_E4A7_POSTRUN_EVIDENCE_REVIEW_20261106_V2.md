# C11-E E4A.7 Post-Run Independent Evidence Review — V2

**Review date:** 2026-11-06. **Run:** `20261106T070808Z-62F31F9C`.

## Files reviewed

Library upload `RUN_20261106T070808Z-62F31F9C.zip`: 67,118,130 bytes, SHA-256 `ad4024cc6caa3b9140a284390b852c76f3dcd5d50d88cf03813d6bb4e374d293`. ZIP CRC returned no bad member. 268 entries, 73,563,270 uncompressed bytes. `SHA256SUMS.txt` covers 267 entries (the sums file itself is excluded); all 267 verified, no missing/mismatch. Receipt SHA `102cf07a0b8920318c3ba211a3bd4374c3e080018486363d701f81e65613aaa0`; sidecar matches. Report SHA `efb0f1a9245d3fce15bf48041c8972e90f6874d308fa99340afb5c731f94403a`; report pin in receipt matches. Documentation stage has 13 files, all manifest paths/bytes/SHA match.

55 process exit-code files all record zero. 24 stderr logs are nonempty because FFmpeg loudnorm/ebur128/volumedetect write normal metrics to stderr; they do not indicate failed processes. Empty stderr for mux/FFprobe calls is retained.

## D3 V5 / seed-domain results

A and B use gameplay seed 314159 and music seed 840001; C uses gameplay 314159 and music seed 840002. All are TEST fixture values, not defaults. D3 V5 raw WAV A/B are byte-identical (SHA `6956653f...`), C differs (`1b2fdaf9...`). Parameter hash A/B equal; C parameter hash differs. Engine reports 15.0 s, stereo, 22,050 Hz, variation 0.

## D3.3

15 s delivery masters are PCM S16LE 48 kHz stereo. A/B SHA `50018594...`; C SHA `85909dc4...`. 30 s repeated QA windows: input A Integrated -17.2 LUFS, TP -9.6 dBTP, LRA .2 LU; output I -14.0 LUFS, TP -6.4 dBTP, LRA .1 LU. A/B values match; C output TP -6.1 dBTP. `TP=-1 dBTP` is a maximum ceiling and `LRA=7` an upper range bound, not a requirement to drive true peak/LRA to those exact values. No clipping; all six D3.3 QA booleans PASS for each case, including mono compatibility/audibility. Mono master check artifacts are distinct and preserved for A/B/C.

## Mux

A/B/C each have one H.264 High 720×1280/30 FPS/450 frames/15 s stream and one AAC-LC 48 kHz stereo audio stream, non-silent. Start and end A/V drift 0.000 s. Source H.264 elementary SHA `6164e47a...` equals A, B and C extracted H.264. Decoded AAC A/B PCM SHA equal (`3d6bfd12...`); C differs (`83aaad64...`). MP4 A/B are byte-identical (SHA `03f5f933...`); C SHA `41b9a361...`.

## Protection/governance

Receipt records frozen manifest SHA `e405d08e...`; active D consumer, protected shared C11-C layer, D3 engine/spec/profile/contract, E1 service, E3 audio pipeline, D9 model/resolver and approved policy pins. `c11c_generator_modified=false`, `core_audio_modified=false`, `d3_engine_modified=false`, `gameplay_rerendered=false`; production renderer/dispatch/media false and `release_authority=NONE`.

## Disposition

`PASS_ISOLATED_E4A7_D_COMPOSITED_CHALLENGE_AV_TEST_ONLY` is accepted for the technical subgate. The outer wrapper ZIP alone was incomplete; the separately uploaded inner worker ZIP is now independently audited. No rerender or E4A.7 repeat is needed.

**Human audio listening: PASS.** The operator explicitly confirmed A/B/C as OK/PASS on 2026-11-06. No repeat listening package or A/V run is needed. Visual review is already user PASS. E1 intents in this A/V worker are `request_origin=TEST`; GUI runtime is not evidenced here.

## Next task

Existing Producer GUI D9.9 button performs actual GUI -> shared E1 service and invokes D9 canonical CLI plus E1 CLI, comparing semantic intent and bridge parity. Run one TEST-like REVIEW Challenge fixture; it does not dispatch or create media. Upload the resulting `D99-GUI-<ID>` evidence folder. Full E4A remains open only until the D99 GUI source correction is applied and the subsequent GUI/E1/D9.9 runtime parity run passes.


## D99 GUI request artefact review — 2026-11-06

Uploaded `D99-GUI-D22A8281E993.zip` (15,049 bytes) contains 13 JSON payload files plus the directory entry. Its timestamps are 2026-11-06 11:21:14 local. Both `c11e_gui_cli_parity.json` and `gui_cli_parity.json` report PASS; the E1 receipt is `PASS_E1_PREPARATION_ONLY`; the D9.10 producer receipt is `PASS_BRIDGE_PLANNING_ONLY`. All renderer/dispatch/media flags are false.

The successful artifact's `request.json` contains `presentation_options: {show_hook_countdown:true}`; its `d9_request.json` does not; the canonical D9.9 request has no `presentation_options`. Thus the supplied artifact does not reproduce the user-reported `Unknown universal request field(s): presentation_options` exception. Do not mark this uploaded evidence as failed.

The minimal hardening removes the not-yet-needed checkbox and its request serialization from GUI `main.py`. It does not change `c11e_production_service.py`; that service already defaults Challenge `show_hook_countdown=true` when the option is absent. It does not change D9.9 schema/resolver. D9.8 outputs all approved editorial keys even when values are empty; empty optional values normalize to `UNKNOWN`. The GUI artifact has `personalization_enabled=false`, `editorial_profile={}`, and `production_override={}`; its canonical editorial object nevertheless includes all six Challenge keys.

Full E4A stays open until the surgical source patch is applied and a new GUI run records PASS. The D22A8281E993 evidence remains a prior successful D9.9/E1 plan-only run and should be retained unchanged.
