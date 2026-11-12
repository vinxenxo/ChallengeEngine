# E4C GUI single-selector A/V acceptance — D99-GUI-6514F1066E79 — 2026-11-12

## Evidence identity
- Production ZIP: `D99-GUI-6514F1066E79-production.zip`, 17,778,067 bytes, SHA-256 `5fb910dd7515ca1f80f2fa77a0829836613e933ca7106f00852ccd31d797f8e4`.
- Tests/plan ZIP: `D99-GUI-6514F1066E79-tests.zip`, 35,864 bytes, SHA-256 `5c94ad64666548db478a4265a71345efe28c2a346f215e7cdb477f51dc8dde91`.
- `E4C_DRILL_AV_QUALIFICATION_RECEIPT.json`: SHA-256 `d8aad7176ed99d8bc0c067cece58272c5ac44045d55d746c768ea72324d459db`.
- `E4C_DRILL_AV_QUALIFICATION_RUNNING.json`: SHA-256 `2f9b388b3541548d79c254161290ad73241109349aea1f57c1ac9c10e092ab2a`.
- Final A MP4: 1,487,139 bytes, SHA-256 `7604f69e7c28e044a4bdb7fccc76c74604495ec9bbe4b46fcbca23a62b7c49ba`.
- Final C MP4: 1,486,037 bytes, SHA-256 `d93753dabcfd85f3a3e721125081a649fbfa3a033a751e77a39df4c38357bf84`.
- Native silent C11-C capture: SHA-256 `d10950bca9358de4ffe8a9f4f24c8c35cdb37e25050775a9220a4d15ffb45338`.
- D-composed silent intermediate: SHA-256 `60fd3155e70691bb7f2e636d20539e5898554669503888ee34bb78402c9589ad`.

## Request and preparation
`request_id=D99-GUI-6514F1066E79`; `request_origin=GUI`; `visual_drills/tracking/tier-1`; gameplay seed `12345`; music seed A/B `840001`; changed C `840002`; `REVIEW_720`; presentation `social_default_v1`; variation 0; audio ON; personalization ON; title/subtitle/CTA all populated. E1 receipt `PASS_E1_PREPARATION_ONLY`, `valid=true`, 91 source pins; GUI/CLI semantic identity equality true. E1 remains plan-only.

## Execution and media results
- Qualification receipt: `PASS_E4C_DRILL_SINGLE_SELECTOR_A_V_QUALIFICATION`.
- Existing C11-C Drill launcher invoked silently with `-NoSound`; no C11-C source mutation.
- Native timeline: 3s pre-roll + 21s gameplay + 3s end CTA = 27s; 810 frames at 30fps; H.264 High 720×1280; one video stream and no audio.
- D composition: all 810 frames; PRE_ROLL 90, GAME 630, END_CTA 90. Three editorial fields visible in GAME; outer bands hidden in PRE_ROLL and END_CTA. Operator visual review PASS.
- `FAMILY_MUSIC_V4` profile `FLOWING_VECTOR`; 27s, 44.1 kHz, stereo, signed 16-bit PCM. A/B WAV SHA `e54b960c799102fb104a99ccd7b94c4a41b5b22d54665acda72106b36646f277` identical; C WAV SHA `5e81b6426f7915c7cad4c658fc24b90cd17c870a4497f45136a53e43b71efd40` different. D3 V5 was not invoked. Operator listening review PASS.
- Final A and C: H.264 High, yuv420p, TV range, 720×1280, 30fps, 810 frames; AAC-LC 48 kHz stereo; 27.000s; both stream start times 0.000s.
- Receipt H.264 stream identity A/C true; AAC stream difference A/C true. Independent extraction from submitted MP4s: raw H.264 SHA A/C `500fc010b0d39062997d73643643943d03552082d75a2b8db6c55a3bbe5ad150` identical (807,042 bytes); AAC ADTS SHA A `23162fb059ca5e215758d6bbd58b6baba0efc9bd13e94d5921fd96726e19cd67` and C `f98747cc8f408521a3d00e7f4d90a066f3adf366de46d6f89bfefb65e26e86cd` different.
- Source pins: 91/91 pre-execution = immediately-pre-render = post-execution. Frozen C11-C manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` unchanged.

## Non-blocking diagnostics
Godot stderr contains teardown warnings for one leaked CanvasItem RID and one ObjectDB instance at exit. Godot stdout confirms successful Movie Maker completion, 810 frames and expected 27s. Treat as non-blocking shutdown diagnostics for this run; retain monitoring, but do not fail the media acceptance solely on these warnings. FFmpeg `-v error` stderr and stream-hash log files are empty; successful receipts/FFprobe and independent stream extraction provide the actual proof.

## Governance and disposition
`renderer_invoked=true` only under the explicit isolated E4C qualification scope; `production_dispatch=false`; `production_release=false`; `release_authority=NONE`; `c11c_source_mutation=false`; E1 `PREPARE_ONLY`; `family_adapter_preparation_status=NOT_CONNECTED_E1`.

**Disposition:** ACCEPTED — GUI single-selector A/V pilot. Count as matrix row 1/20 (`tracking/tier-1`). Do not repeat this selector merely for matrix coverage. The CLI smoke is a separate entrypoint gate; the remaining matrix has 19 selectors. E4C remains open pending CLI A/V smoke and full 20-row matrix.
