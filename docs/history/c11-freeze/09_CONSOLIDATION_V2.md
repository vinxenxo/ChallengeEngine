# C11 Freeze Consolidation v2 — Regression Hardening

This layer exists to restore pre-C11 compatibility after the B.1 UI integration while keeping C11 presentation contracts intact.

The VisualContentPlayer remains usable both as a scene and as a directly instantiated script because existing C6 playback tests use both forms.

Physical export tests are external physical checks. They are no longer assumed to find historical `output/*.avi` artifacts during the logical corpus run. The physical suite generates the fixture first and then validates the canonical artifact location.

Authoring productive tests use their authoritative adapter metadata. They do not assert historical placeholder values or intentionally-unavailable metadata when the current adapters provide productive metadata.

C11 stress tests are deterministic: the seed corpus is generated from a fixed corpus seed and then reused verbatim. The stress runner does not generate random seeds during a test.

QA video configurations are disposable copies. They may carry descriptive Hook/CTA text and `qa_mode` presentation metadata, but canonical challenge definitions are not changed.
