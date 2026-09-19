# Artifact Policy

## Canonical root

All newly generated evidence must live under `artifacts/`.

```text
artifacts/
├── production/
├── qa/
├── regression/
├── tests/
├── releases/
├── legacy/
└── scratch/
```

## Version-control rule

Durable evidence such as JSON manifests, textual logs, frame digests and certificates can be committed when they represent a deliberate baseline. Large generated media is ignored by default because the production pipeline can regenerate it.

## Historical evidence

Historical artifacts may retain path strings from the repository layout that existed when they were created. That does not make those strings active dependencies.

## Scratch

`artifacts/scratch/` is disposable and ignored. Do not store the only copy of a required fixture or contract there.
