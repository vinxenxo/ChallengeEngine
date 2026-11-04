# C11-E Gates and Acceptance Matrix — V45

| Gate | State | Evidence / next action |
|---|---|---|
| E0/E1 baseline | ACCEPTED / RETAINED | Existing shared service, GUI route and CLI compatibility retained. |
| E1 Challenge visibility option E4A.1 | IMPLEMENTED / FOCUSED_TESTS_PASS | Request-scoped `show_hook_countdown`; default ON; sealed in E1; D9.9 receives sanitized request; Loop/Drill unchanged; legacy E1 intents remain valid. Manual GUI observation still pending. |
| E2/E3.2 | ACCEPTED_BOUNDED | Retain; do not repeat absent relevant source drift. |
| E3 D3 V5 / D3.3 / mux-QC | ACCEPTED_BOUNDED_TEST_ONLY | Three MP4 + three WAV A/B/C; audio seed isolation, unchanged H.264, FFprobe and 0s A/V drift. Does not include D compositor. |
| E4A.2 | ACCEPTED_BOUNDED | Real Challenge004 BODY reference. |
| E4A.3 V2 | ACCEPTED_BOUNDED | Six real frames, 18 PNGs, 12 comparisons; operator accepted countdown/hook + editorial coexistence. |
| E4A.4 | PASS_TEST_ONLY_USER_REVIEW | A/V mux evidence accepted; no D visual compositor in its MP4s. |
| E4A.5 source seam | CONTEXT_RECONCILED / LIVE_PINS_CHECKED_BY_APPLY | Do not repeat failed V1–V5 packager chain. Live sources are checked by the one-step E4A.1 apply runner. |
| E4A Challenge D visual consumer | IN_PROGRESS | Next: D-owned adapter reuses C render model and shared C11-C editorial layer; isolated pixel tests, no production dispatch. |
| E4B Loop | NOT_STARTED | Preserve Loop binder/timeline/music. |
| E4C Drill | NOT_STARTED | Preserve Drill binder/END_CTA/music. |
| E5 | NOT_STARTED | Cross-family determinism, seed isolation, non-leakage, GUI/CLI parity. |
| E6 Smoke18 | NOT_STARTED | Six audiovisual cases per family. |
| E7 Matrix101 | NOT_STARTED | 54 + 27 + 20; CH_008/009 held, 99 provisional runnable. |
| E8 | NOT_STARTED | Historical row-by-row regression, independent acceptance, freeze and explicit promotion. |

E1 option PASS does not mean option-to-pixels consumption. Renderer dispatch, production media and release remain OFF; C11-C 2.19.12 remains production authority; `release_authority=NONE`.
