# C11-C Artifact Cleanup Policy v1.1

## Protected evidence

The cleanup tool never removes content under `artifacts/legacy`, `artifacts/qa`, `artifacts/regression`, `artifacts/releases`, `artifacts/production`, or `artifacts/tests`.

`artifacts/prototypes/c11c_review_assets` is also protected because its keyframes are active visual-review evidence.

## Disposable prototype output

Rendered prototype media under `artifacts/prototypes` is reproducible and disposable: MP4, GIF, AVI, WAV, PNG/JPEG/WebP/BMP, MOV, MKV and WebM. Prototype metadata/sidecars such as JSON, TXT, MD and SHA256 files are retained.

## Scratch

`artifacts/scratch` is disposable and is removed recursively when `-Apply` is supplied.

## Safety

The command is dry-run by default. Actual deletion requires `-Apply`.
