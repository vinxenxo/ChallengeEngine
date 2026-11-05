# C11-E Challenge / Loop / Drill Alignment — V16

- Challenge uses the D-owned presentation/editorial layer and D3 V5 music route with independent `music_seed`. Native phase owners remain HOOK/GAME/REVEAL/CTA. Editorial mapping remains title/subtitle -> HEADER/HOOK; call_to_action -> FOOTER/CTA; language metadata-only; player_name/challenge_label blocked by unresolved geometry.
- Visual Loop retains its C11-C grammar/variant timeline, binder and existing family-aware music. It is not routed through the Challenge 8-bit profile.
- Visual Drill retains its C11-C phase/END_CTA precedence, binder and existing family-aware music.
- E4A.6 live consumer and Movie Maker capture are test-only PASS. Existing 900-frame AVI is immutable input; no capture rerun.
- Postprocess V3 now passes source FFprobe, PCM safety check, silent MP4 encode and MP4 FFprobe, but fails at still extraction because the user's FFmpeg rejects legacy `-vsync`. Its second run then refused to overwrite the already-created MP4. V4 validates and reuses that MP4 when valid, uses `-fps_mode vfr` for the eight stills, and can resume from an interrupted output without recapture.
- The active `GeneradorMaestro.gd` D-only postimage differs from the SHA pinned in the frozen C11-C manifest. No additional writes until D/E source isolation is resolved.
- E4B and E4C remain held until full E4A D-composited A/V is accepted.
