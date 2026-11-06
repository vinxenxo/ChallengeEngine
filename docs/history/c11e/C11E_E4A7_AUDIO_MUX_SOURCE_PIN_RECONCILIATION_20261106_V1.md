# C11-E E4A.7 Audio/Mux Source-Pin Reconciliation — V1

**Date:** 2026-11-06. Read alongside the E4A.7 plan before executing the D-composited Challenge audio test.

## The prior E4A.4 input is not the current video input

E4A.4 bounded D3 V5/D3.3/AAC mux test passed on the old normalized C11-C video SHA `edbd446d67142d20e138e55563f16cbae8d9a4c39469fd2bebcb3c9d5723fb9e`. Its receipt correctly stated that the full-frame D compositor was not embedded. That input is not acceptable for E4A.7. Reuse E4A.4's tested audio mastering/mux/FFprobe method and predicates only.

The new visual source is Recovery V1.2 D-composited silent MP4 SHA `841b03531301c7e70c0e09ce3e9f536241d2072a87792e099ed7a955bef8c52f`, 671,647 bytes, 720×1280/30fps/450 frames/15s, H.264 High, yuv420p, TV range, no audio.

## E1 service pin correction

E4A.4's old E1 service SHA was `f0655d8d93df3b766b157d80a76a5bfc7b514d740815646f54c88ca788f602c0`. The latest reviewed E4A5B snapshot contains the newer E1 service SHA `348997e575d985fe153a4f433f089c5f205be5d4d8f3853baf07be917a134951` (schema 1.1; service 0.2.0-E3.2; Challenge `presentation_options.show_hook_countdown`). The E4A.7 worker pins the latter. If the live checkout does not match, stop before generation and review the actual current source; do not fall back to the older pin silently.

The unchanged supporting pins are listed in Authority V68 and E4A.7 plan V1: D9 resolver/editorial/GUI request, E3 pipeline, D3 engine/spec/profile/contract, approved Challenge policy, frozen manifest and protected visual sources.

## D3 request parameter boundary

The E1 contract intentionally leaves `tempo_bpm` and `duration_seconds` unresolved. For this isolated test, 104 BPM is a historical D9.2 pilot fixture only; duration comes from the exact MP4 FFprobe (15 seconds). The worker records these as test-time resolutions, not product defaults. Do not patch E1 or infer defaults.

Historical fixture controls: gameplay seed 314159 fixed for A/B/C; music seeds 840001/840001/840002; variation 0; profile `challenge_8bit_v1` v1.0. E1 intent validation must pass for all three before calling D3 V5.

## Acceptance mechanics

Use the exact D-composited MP4 with `-c:v copy`; compare extracted source H.264 elementary stream SHA with each output. A/B raw/mastered/decoded audio must repeat; C must change only the music-seed domain and yield different audio. Require D3.3 loudness/peak/no-clip/mono tests, AAC-LC 192k/48k/stereo, non-silence, exact 15 seconds and <=0.15 s A/V start/end drift. No gameplay rerender.
