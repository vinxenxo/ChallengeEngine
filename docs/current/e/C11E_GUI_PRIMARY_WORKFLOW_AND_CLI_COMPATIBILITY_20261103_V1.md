# C11-E GUI-Primary Workflow and CLI Compatibility Contract V1

**Date:** 2026-11-03
**Applies from:** post-E3.2 implementation onward.

## 1. Operator decision

The Producer GUI is the sole primary operator workflow for C11-E development and production operation. The user will configure and launch product jobs through the GUI. Do not continue building a separate manual CLI experience.

CLI remains supported as a thin transport/compatibility interface over the same C11-E production service. It is required for automated tests, separate-process parity, reproducibility and controlled automation; it must not own business logic or offer a divergent production path.

## 2. Canonical topology

```text
Producer GUI ───────────┐
                        ├── C11-E Production Service ── Canonical request/resolver
Thin CLI adapter ───────┘                                  │
                                                           ├── Challenge adapter
                                                           ├── Visual Loop adapter
                                                           └── Visual Drill adapter
                                                                  │
                                                   C family generator/consumer
                                                                  │
                                                     D editorial presentation
                                                                  │
                                                       family music strategy
                                                                  │
                                                           FFmpeg mux
                                                                  │
                                                 FFprobe + semantic QA + receipt
```

GUI and CLI must compare the same canonical request identity, editorial hash, seed domains, selected family adapter, execution options and result receipt semantics. GUI origin/CLI origin may be provenance fields, but must not change semantic identity.

## 3. GUI workflow requirements

The existing Producer application remains the entry point and remains within the existing five-module suite. Do not create a new application or sixth surface.

The C11-E GUI must expose, where supported by the active schema:

1. Family/content selector and exact Challenge ID, Loop family/grammar, or Drill type/tier.
2. Mode/delivery/presentation profile from the accepted registries, not free-text invented values.
3. Gameplay seed and music seed as separate mandatory/explicit domains. No automatic generation, aliasing or fallback between them.
4. Audio enable/disable. Disabled must mean no music renderer/mux invocation and an explicit disabled state in the receipt.
5. Editorial values with the D9.8 field allowlist and inheritance order; only show fields supported by that family and binder.
6. Destination/output identity, preflight results, active job state, stdout/stderr logs, failure diagnostics, media preview and final FFprobe/QA receipt.

Use existing Producer GUI conventions and the shared service. Do not design around a new CLI command surface.

## 4. Job and failure behavior

The GUI must fail closed when a mandatory source pin, profile, seed, selected variant, output path or gate is invalid. It must not display READY/COMPLETE before the service/runner and validators return structured evidence. A failed subprocess stops the corresponding gate; retain logs and partial outputs in its isolated run folder. Retry uses a fresh RequestId/output root; never overwrite evidence.

For the E3 audio pilot, the GUI action will operate on a previously verified E2 R4 video artifact. It must verify the input media hash and provenance before music generation. This action does not invoke Godot or rerender gameplay.

## 5. CLI compatibility contract

- CLI invokes the same canonical E service used by GUI.
- No separate resolver, editorial mapping, seed policy, music defaults, dispatch table or receipt implementation.
- Automated tests launch CLI as a separate process and compare request/plan/editorial/result hashes with the GUI-facing service path.
- CLI flags cannot silently override unavailable or disabled editorial fields.
- CLI remains documented for CI/test/compatibility only. User-facing operational runbooks should use the GUI.

## 6. GUI acceptance sequence

- Static GUI contract tests: field visibility, enabled/disabled state, labels, callbacks, service call boundary and no duplicated business logic.
- Windows runtime smoke: application launches, family selectors populate, request prepares, invalid values are rejected, job status updates, logs are viewable and output/receipt is inspectable.
- E3 GUI run: choose verified E2 video; set explicit `music_seed`; request audio pilot; observe music, mastering, mux and probe stages; inspect final MP4 in review UI.
- CLI separate-process tests: same canonical request/result semantics; no production CLI workflow required from the operator.

A passing static contract does not count as a launched or manually observed GUI. E1's historical manual GUI observation remains a separate pending item until the live app is exercised and recorded.
