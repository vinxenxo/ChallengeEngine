# C11-D D8.1 Scope + Runner Cleanup

Scope review result:
- Workspace forensic inventory: 2,479 media / 24,680,857,985 bytes.
- `artifacts/production/audiovisual/**`: historical C11-C production, not D8 scope.
- `artifacts/qa/**`: historical C11-A/B/C and smoke/test evidence, not D8 scope.
- `artifacts/prototypes/**`: prototypes, not D8 scope.
- `artifacts/maintenance/**`: historical/quarantine, not D8 scope.
- `artifacts/tests/**`: phase evidence, not D8 scope. The 7 D3 audio files matched the name filter only because their path contains `c11d_d3`.
- `artifacts/releases/**`: frozen ZIP archive, not D8 media.

Canonical D8 media scope is explicit-registry-only and currently empty.
D8.0 remains closed; this overlay corrects future runner semantics and does not reopen D8.0.
D8.1 is `PASS_NO_MEDIA` when the canonical registry is empty.
