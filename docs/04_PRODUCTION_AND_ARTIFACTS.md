# Production and Artifacts

## Canonical artifact policy

New generated evidence belongs under `artifacts/`. The intended structure is:

```text
artifacts/
├── production/
├── qa/
├── regression/
├── tests/
├── scratch/
└── legacy/
```

## Evidence classes

- `artifacts/qa/`: repeatable validation outputs.
- `artifacts/regression/`: reference comparisons and freeze reports.
- `artifacts/tests/`: test logs, inventories and certificates.
- `artifacts/production/`: intentionally retained production-grade exports.
- `artifacts/legacy/`: historical roots migrated out of the repository hot path.

## Physical export doctrine

Movie Maker exports use the graphical Compatibility renderer. Headless execution is appropriate for validation and fixture preparation, not as a substitute for the established Movie Maker path.

The physical smoke verifies resolution, frame count, FPS, packaging and hashes. It does not replace the production manifest.

## Reproducibility

The C11 freeze uses fixed seeds and explicit manifests. Source/documentation sealing uses SHA-256 hashes over the declared freeze scope.
