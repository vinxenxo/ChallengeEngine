# R1V Godot Log False-Negative / Family A/V Amendment — History V1

## Prior attempt

R1V wrapper V3 completed its 32-test active-checkout suite (32/32) and invoked one C11-C launcher: Fractal Bloom A / radial_bloom / gameplay seed 100006 / 22s. Launcher returned exit 0; stderr was empty; Godot wrote a 720×1280@30 Movie Maker recording and 660 frames; C11-C reported PASS; MP4 SHA was `7971ced1d9cdbb7dd76a0d8d76e766faa9a051fc27419c9e737c41264796f659`.

The runner failed closed because its regex accepted only ASCII `x` and no spaces, while Godot emitted the Unicode multiplication sign `×` and spaces in UTF-16LE. The original stream also reported `yuvj420p` full range `pc`; the verifier did not admit this observed source pair. No source inventory was written by that failed run and no other launcher ran. Operator visually reviewed Fractal A and confirms the visual Loop and all layers are correct.

## Repair

The new inventory decoder handles UTF-16 BOM/strict UTF-8 detection, `×`/`x`/`X`, optional spaces, and exact completed-frame lines. Source format is restricted to two precise pairs: `yuvj420p/pc` (observed C11-C output) or `yuv420p/tv` (explicit alternative). Other combinations fail closed. Inventory was locally tested against the retained Fractal MP4: 660 frames and increasing uniform PTS at 30 fps; FFmpeg decoded pixel hashes to memory and created no frame images.

## Music decision and scope change

The operator requested music be coupled into the test production and approved the bounded amendment. Historical roadmaps require family-native Loop/Drill music to remain intact, while D3 V5 is Challenge-only. The new A/V flow uses C11-C FAMILY_MUSIC_V4, the pinned helper/profile registry and R1P music_seed. The launcher still captures a silent immutable C MP4, and the music helper + AAC mux run immediately within the same R1V slot. Video is copied without re-encode; final AV is separate. The old silent-only V2 policy and original approval are immutable; the supplement authorizes only five selectors × two repeats / ten A/V outputs.

No general renderer activation or release authority is granted. The integrated test/install/wrapper are one add-only application and one 52-test preflight. Do not repeat old failed runner attempts or perform separate audio tests.
