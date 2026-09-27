# Repository Structure — Current

```text
ChallengeEngineV01_STATELESS/
├── challenges/                  # canonical challenge definitions
├── assets/                      # current project assets
├── definitions/                 # visual/drill definitions
├── profiles/                    # difficulty/presentation/music/delivery profiles
├── core/                        # runtime, authoring and presentation
├── tests/                       # complete logical regression corpus
├── c11c-suite/                  # operator GUI suite
│   ├── c11c-test/
│   ├── c11c-catalog/
│   ├── c11c-maintenance/
│   ├── c11c-config/
│   └── c11c-producer/           # relocated current Producer
├── c11c-producer/               # compatibility launchers only
├── tools/
│   ├── c11freeze/
│   ├── maintenance/
│   └── prototypes/c11c_bulk/
├── artifacts/                   # generated evidence/products
└── docs/
    ├── current/
    ├── master-prompts/
    ├── operations/
    ├── contracts/
    ├── checkpoints/
    └── history/
```

`docs/current/` is the source for present-state narrative. Historical documents are never overwritten to make them appear current.

The Suite is an operator layer and does not replace canonical backend launchers.
