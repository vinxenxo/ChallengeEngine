# C11-D to C11-E Full-Family Roadmap — V15

**Date:** 2026-11-03. This roadmap supersedes V14's pre-E3-audio-test status only; it does not supersede governance locks.

## Product outcome

A GUI-first, single-service production workflow creating validated audiovisual MP4s for Challenge, Visual Loop and Visual Drill. Preserve C11-C visual mechanics/generators and family audio implementations. Add D presentation/layout, enabled family-scoped editorial and music orchestration, FFmpeg mux, FFprobe QA and immutable run receipts. CLI is only an automated compatibility adapter over the same E1 service.

## E gates

- **E0:** foundation, source authority and continuity — accepted; do not repeat.
- **E1:** one shared GUI/CLI production service — automated accepted; real Producer GUI runtime observation remains pending.
- **E2:** bounded CH001 title-to-pixels R4 control — formally closed; does not imply family-wide or music acceptance.
- **E3.2:** D3 V5 music contract bound to E1 intent — accepted/committed.
- **E3 audio implementation:** V1.3 applied; Windows V1.4 compile/tests 31/31 PASS, PySide6 6.11.2. Temporary FFmpeg mux and seed-isolation integration tests passed. No production output and no GUI launch. Next: E3-GUI-01 real GUI runtime and test-only CH001 audio attach pilot, followed by full mastering/mux/FFprobe/determinism/receipt acceptance.
- **E4A:** full Challenge presentation/layout/editorial plus Challenge D3 V5 audio.
- **E4B:** Visual Loop binder, grammar-specific editorial/layout and existing C11-C family audio through a verified audio-only E adapter.
- **E4C:** Visual Drill binder, phase and END_CTA precedence, family editorial/layout and existing C11-C family audio through a verified audio-only E adapter.
- **E5:** three-family determinism, gameplay/music seed isolation, adapter non-leakage, GUI-primary acceptance and CLI separate-process parity.
- **E6:** Smoke18, six audiovisual scenarios per family.
- **E7:** Matrix101: 54 Challenge + 27 Loop + 20 Drill. CH_008/009 remain held because declared duration is 11s while phase sum is 12s (3+7+0+2); provisional runnable set 99 until authority resolves the conflict.
- **E8:** independent acceptance, immutable freeze and explicit promotion authority.

## Hard constraints

C11-C 2.19.12 remains the sole production authority through E8. Frozen manifest remains 796,318 bytes / SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. Do not alter `core/audio`, protected C generators/mechanics, canonical definitions, D4.8/D9.10 locks or the manifest. No sixth suite module, second producer or `c11d-control`. `release_authority=NONE` until formal E8.

## Immediate handoff point

V1.3 patch application and V1.4 Windows automated tests are accepted. The next action is a real Windows Producer GUI launch and operator-driven test-only Challenge audio pilot against the immutable R4 video, without gameplay rerender. Continue from `C11E_E3_EXECUTION_BACKLOG_20261103_V2.md`.
