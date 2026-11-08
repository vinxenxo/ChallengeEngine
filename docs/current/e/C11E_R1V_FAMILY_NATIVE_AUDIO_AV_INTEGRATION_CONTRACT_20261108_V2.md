# R1V Family-Native Audio / A/V Integration Contract — V2

## Purpose

Combine visual-source qualification and family-native music into one per-slot R1V audiovisual production run. This is for Visual Loop only and is bounded to five representative R1P selectors × A/B (10 outputs).

## Family audio authority

Use existing C11-C `FAMILY_MUSIC_V4`, not D3 V5. The pinned helper `C11CSafeAmbient.py` resolves family-specific profiles using the current registry. Expected bindings: fractal → ORGANIC_BLOOM; geometric → CIRCUIT_PULSE; invisible_forces → FLOWING_VECTOR; living_particles → ORGANIC_BLOOM; sacred_symmetry → ORBITAL_RITUAL. Use `request.music_seed` from each R1P receipt and keep it separate from the gameplay `request.seed`; pass `loop_cycles`, duration, internal family, kind `loop`, and grammar. The native family music route for Loop is retained; D3 V5 remains Challenge-only.

## Single run / per-slot sequence

1. Reuse the already generated Fractal Bloom A source only after validating its original evidence; launch the remaining nine C11-C source captures using original pinned launchers with `-NoSound` (the launcher’s built-in family audio branch is bypassed so it cannot consume gameplay seed).
2. Validate source C MP4 remains silent, H.264 720×1280/30, expected duration/frame count, source sidecars and C11-C PASS. Parse Godot UTF-16 log robustly, admitting exact `×` and spaces. Preserve observed `yuvj420p/pc` or the explicitly allowed `yuv420p/tv` pair.
3. Inventory every frame PTS, strict monotonicity and 1/30-second spacing. Decode `yuv420p` frame bytes through a pipe to memory and calculate per-frame/global SHA; no PNG/raw frame spool.
4. In the same slot, invoke the existing `C11CSafeAmbient.py` with R1P music_seed and family timing; validate PCM s16le / 44.1 kHz / stereo, exact sample count, duration, peak and RMS against pinned C11-C registry.
5. Mux to a separate output using pinned native FFmpeg AAC delivery, `-c:v copy`, AAC 192k, 44.1 kHz stereo, `-shortest`, faststart. Do not filter, scale, transcode or re-encode video.
6. FFprobe final MP4: exactly one H.264 video stream + one AAC stereo audio stream, correct geometry/fps/frames/durations/start offsets. Extract source and final H.264 elementary streams; their SHA-256 must match. Record AAC elementary-stream hash.
7. Compare A/B decoded frame hashes/PTS/global hash, WAV hash, AAC hash and seed domains.

## Exact bound scope

Five selector identities; two repeats each; 10 final A/V files; one already-made Fractal A source reused; nine new C11-C launcher invocations. No new launch outside those nine, no extra selectors, no production dispatch, no D composition, no D3 V5, no audio outside these slots. General D4.8 policy remains DISABLED, runtime authority NONE, D9.10 PREPARE_ONLY, release NONE.

## Evidence and acceptance

Retain source C MP4, C11-C sidecars, Godot stdout/stderr and logs, per-frame PTS/pixel SHA manifests, WAV/metrics, music/mux/FFprobe logs, final A/V MP4, source/final H.264 hashes, AAC hash, per-slot receipts, source pins, A/B comparison, wrapper/process receipts and evidence ZIP. Technical PASS requires all 10 slots and five A/B pairs. Human visual review applies to all new slots; human audio listening applies to all ten. Only after both may the remaining 22 Loop grammars be separately admitted.


## Operational qualification guard

The approval amendment and scope policy are both pinned by raw SHA and canonical approval digest. The installer checks the two new JSON files from its package payload before copying, verifies all existing parent receipts against their exact schema fields, and only then performs add-only installation. The wrapper performs one direct Python 3.13 probe and one 52-test combined suite; zero skips/errors/failures are required on Windows. This A/V policy supersedes only the R1V silent-only audio/mux prohibition for the ten approved Loop test slots; general D4.8 remains disabled.
