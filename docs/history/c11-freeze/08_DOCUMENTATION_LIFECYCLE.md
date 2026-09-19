# Long-Term Documentation Lifecycle

## Canonical layer

The repository should eventually expose a small durable set of documents:

```text
docs/
├── 00_PROJECT_OVERVIEW.md
├── 01_ARCHITECTURE.md
├── 02_DATA_AND_CONTRACTS.md
├── 03_PRESENTATION.md
├── 04_PRODUCTION_AND_ARTIFACTS.md
├── 05_TESTING_AND_REGRESSION.md
├── 06_ROADMAP.md
└── checkpoints/
    └── C11_FREEZE.md
```

Checkpoint implementation notes can live below `docs/history/`.

## Migration rule

Do not delete old documentation during the first pass. Build a canonical index that points to the authoritative current document and classify each old file as:

- canonical;
- historical evidence;
- superseded;
- migration note;
- obsolete/deprecated.

Only after the classification is reviewed should historical documents be moved under `docs/history/`.

## Long-term content requirement

The overview must answer, without requiring conversation history:

- what the engine does;
- what is mathematically deterministic;
- how challenges differ from visual families;
- how presentation consumes simulation truth;
- how seeds are governed;
- how videos are produced;
- how artifacts are stored;
- which tests prove which contracts;
- what is frozen now;
- what is intentionally out of scope.
