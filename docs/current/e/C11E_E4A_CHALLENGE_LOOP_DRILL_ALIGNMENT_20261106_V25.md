# C11-E Challenge / Loop / Drill Alignment — V25

The product remains one E factory for Challenge, Visual Loop and Visual Drill. Shared orchestration does not flatten family-specific binders, mechanics, timelines or music.

- **Challenge:** D-owned live presentation/editorial consumer with title/subtitle in HOOK/HEADER and CTA in CTA/FOOTER. D3 Music V5 + D3.3 + FFmpeg AAC mux. E4A.6 visual and E4A.7 D-composited A/V are PASS_TEST_ONLY; full E4A still needs the D99 GUI request correction and E1 GUI/CLI runtime parity; user listening A/B/C is PASS. The V1 installer failed during `File.Replace` because it passed a null backup pathname; targeted tests and pins had already passed. V2 is the repaired runner, not a redesign of the source patch.
- **Visual Loop:** preserve existing C11-C Loop grammar/variant timeline, binder and family music. E4B remains held.
- **Visual Drill:** preserve existing C11-C Drill phase timeline, binder, END_CTA precedence and family music. E4C remains held until E4B.
- Canonical editorial fields remain complete in the D9.8 resolver output: Challenge `title`, `subtitle`, `call_to_action`, `language`, `player_name`, `challenge_label`; Loop/Drill `title`, `subtitle`, `call_to_action`, `language`. Empty optional strings normalize to `UNKNOWN` per D9.8; their keys remain present. Language is metadata-only. Challenge-only `player_name` and `challenge_label` remain blocked for visual consumption pending separate geometry authority.
- `request.seed` and `request.music_seed` are independent; no automatic generation and no cross-domain sharing.
- GUI and CLI converge on the existing E1 shared production service. D9.9 / D9.10 remain plan-only; D renderer input/dispatch is not enabled. `presentation_options` is E1-internal only and must not be serialized as a D9.9 universal request field; no Hook/countdown GUI control is part of this current stage. Keep every established editorial input wired; do not implement per-field optional controls yet.

C11-C 2.19.12 remains immutable production authority. No shared-layer, binder, mechanic, RNG or timeline changes are authorized by these test receipts.


## Current continuation boundary

The D99 postimage removes only the Hook/countdown checkbox and `presentation_options` construction from the D-owned Producer GUI. It leaves the shared editorial inputs and their containers intact, leaves E1's internal Challenge default unchanged, and leaves D9.9 schema/resolver unchanged. V2 must first report a source/test PASS and verify `main.py` SHA `4141072659f307468900c1cfb09774479abc6c10abae6ae638a11192cfcd04e6`. The operator then runs one plan-only Challenge GUI/CLI parity fixture. Until that evidence is reviewed PASS, E4B Loop remains held; no Loop code or media work is being started ahead of the ordered gate.
