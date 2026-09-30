# Architecture — C11-C 2.19.12

The tested architecture remains:

```text
Definitions
  ↓
deterministic simulation / authoring
  ↓
SimulationResult / authored envelope
  ↓
passive presentation
  ↓
RenderedFrameStream / Movie Maker
  ↓
production/export orchestration
```

C11-C final hardening changes only operator tooling, documentation and release packaging. It does not introduce a second runtime path.

`c11c-suite` is an operator shell over canonical repository tools, not a replacement backend.
