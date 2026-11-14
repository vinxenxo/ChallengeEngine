# E4C Drill V2 existing-media requalification procedure — V1 (2026-11-12)

## Input evidence

Use only the preserved CLI smoke root `artifacts/production/c11e/E4C-CLI-SMOKE-20261112T091253Z-5a2e96b8`. The requalifier verifies receipt SHA `57fe829b2ae83fc16a962710b8a1ef8e4635ebf8fd4326714ed24c69c4a0f903`, intent SHA `9dfe5c1c4568ed7fbc4bb4260d47da4e518b1a163811fb88f2a9f1bff55c304e`, native MP4 SHA `d10950bca9358de4ffe8a9f4f24c8c35cdb37e25050775a9220a4d15ffb45338`, WAV A/B SHA `e54b960c799102fb104a99ccd7b94c4a41b5b22d54665acda72106b36646f277`, WAV C SHA `5e81b6426f7915c7cad4c658fc24b90cd17c870a4497f45136a53e43b71efd40`. The native MP4 is located recursively by its recorded basename under `native_source/tracking` and must resolve exactly once.

## Execution

Run `tools/c11d/d9/RUN_C11E_E4C_DRILL_AV_EXISTING_MEDIA_V2_REQUALIFICATION.ps1` with active project root and existing Python 3.13. It creates a fresh `E4C-CLI-COMPOSITION-V2-*` output ID. It imports the installed shared D executor and V2 D consumer, validates the preserved intent and current pins, then composes all frames using existing FFmpeg/FFprobe. It does not call the CLI facade or D executor's native C11-C capture/music generation steps.

## Required acceptance

- 810 total frames; PRE_ROLL/GAME/END_CTA = 90/630/90 at 30fps.
- 630/630 GAME body crops RGB888 byte-identical at `(0,192,720,896)`.
- 180/180 PRE_ROLL+END_CTA frames complete-frame byte-identical.
- Original native MP4 and WAV hashes unchanged; 91 E1 pins pre/post identical.
- V2 silent video is H.264 High yuv420p TV 720×1280, 810 frames, 27s.
- Final A/B/C H.264 elementary streams identical; WAV/AAC A/B identical; C distinct; AAC-LC 48kHz stereo; stream start delta <=20ms.
- Seven review PNGs: frame 0, 89, 90, 405, 719, 720, 809.

The V2 receipt remains `PASS_V2_TECHNICAL_REQUALIFICATION_PENDING_OPERATOR_VISUAL_AUDIO_ACCEPTANCE`. The operator must visually review the full A/B/C outputs and seven PNGs, and listen to the relevant A/C audio. The selector is not matrix row 1/20 until this review is explicitly accepted. No new native capture, Godot invocation, music generation, C11-C source mutation, production dispatch or release authority.


## V2.1 File.Replace path-length incident and V2.2 disposition — 2026-11-12

The operator's V2.1 installer passed package inventory, 21/21 source pins, frozen C11-C manifest, PowerShell AST, Python/PySide6 runtime, `py_compile=3/3`, tests `20/20`, forward/rollback File.Replace round-trip preflight and immediate recheck. The first transactional `File.Replace` failed because the path-derived backup filename made the full backup path 269 characters. The operator's journal/diagnostic confirmed the original consumer preimage remained exact and no ADD_ONLY destinations were created; the failure was a Win32 path-length issue, not a consumer/test failure.

V2.2 changes only the backup filename to the operation index plus RunId (`000.<RunId>.preimage.bak`); full `relative_path` remains recorded in the transaction journal. For the exact checkout path `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS` and V2.2 RunId shape, the forward backup path is 213 characters and the rollback-displaced backup path is 256, both within the 259-character Win32 path limit excluding NUL. The maximum generated destination temp path across all 25 operations is 195 characters. V2.2 retains exact hashes, journal-before-write, File.Replace, postimage checks and SHA-guarded rollback. Windows installation remains pending; no transaction PASS is claimed.
