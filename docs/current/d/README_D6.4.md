# C11-D D6.4 — Request / Plan / Provenance Integration

D6.4 is the current active checkpoint in the D branch.

## Inputs owned by predecessors

- D4.2: canonical request and request SHA-256.
- D4.4: canonical Production Plan and plan SHA-256.
- D4.8: blocked production governance decision.
- D6.1: canonical seed registry and governance policy.
- D6.2: explicit seed resolver and deterministic derivation capability.
- D6.3: isolation/collision validation.
- D5.2: provenance/lineage model consumed read-only.

## D6.4 ownership

D6.4 is an integration adapter. It owns only its integration/provenance evidence. It does not replace the request normalizer, seed resolver, production orchestrator or provenance registry.

## Canonical chain

`request -> request SHA -> D6.2 seed resolution -> seed authority -> registry/policy -> D4.4 plan -> plan SHA`

The canonical mappings remain:

- `request.seed -> gameplay.seed -> GAMEPLAY`
- `request.music_seed -> music.seed -> MUSIC`

Equal numeric values are valid across independent authorities. Personalization and `variation_index` are not seed authorities. Derivation remains inactive and `master_seed` remains `NOT_ADOPTED`.

## Execution

Run:

```powershell
Set-Location "C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\c11d\d6\run_d6_4_seed_request_plan_integrator.ps1
```

The runner performs two internal integration runs, compares all four D6.4 evidence hashes, verifies protected inputs and applies the filesystem mutation guard.

Expected close:

`D6.4 = PASS / CLOSED`

`NEXT = D6.5 - Full D6 Acceptance`
