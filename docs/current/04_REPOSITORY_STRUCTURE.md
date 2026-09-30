# Repository Structure — C11-C 2.19.12

```text
ChallengeEngineV01_STATELESS/
├── core/                  # deterministic engine/runtime boundaries
├── challenges/            # declarative Challenge definitions
├── definitions/           # authoring/runtime definitions
├── profiles/              # delivery/presentation/audio profiles
├── assets/                # source assets
├── schemas/               # data contracts
├── tests/                 # canonical regression suites
├── c11c-suite/            # active GUI/CLI operator shell
├── tools/                 # canonical operational/QA/maintenance tools
├── artifacts/             # generated evidence/output; excluded from frozen source package
└── docs/                  # current + historical documentation
```

The misspelled `c11c-suite/c11c-maintenace` compatibility tree is historical residue and must be quarantined before freeze.
