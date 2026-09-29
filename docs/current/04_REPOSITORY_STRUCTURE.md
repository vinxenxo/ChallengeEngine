# Repository Structure — C11-C 2.19.5 Candidate

The root remains intentionally small and the current tree is the source of truth.

```text
ChallengeEngineV01_STATELESS/
├── .continue/rules/CONTINUE.md
├── AGENTS.md
├── README.md
├── core/
├── challenges/
├── definitions/
├── profiles/
├── assets/
├── schemas/
├── tests/
├── c11c-suite/                 # ACTIVE Suite
├── c11c-studio/                # RETIRED; do not modify
├── tools/
├── artifacts/
└── docs/
```

## Root rule

Release notes and one-off patch documents belong in historical documentation. Generated evidence remains under `artifacts/`. Persistent root `override.cfg` is not source truth and must not survive as an accidental capture side effect.

## Suite rule

The canonical active Suite implementation and launchers are under `c11c-suite/`. No operational Suite `.py/.ps1/.bat/.cmd` file may depend on `c11c-studio/`.

## Worker review rule

Parallel Art Direction workers use temporary project roots outside the repository. The worker roots exclude `artifacts/`, `.godot/`, `.git/`, caches and retired `c11c-studio/`. This prevents project-global Movie Maker state from becoming a concurrency bottleneck.

## Documentation topology

- `docs/current/` — current operational truth;
- `docs/current/c11c/` — C11-C state and acceptance;
- `docs/current/suite/` — Suite rules;
- `docs/current/producer/` — Producer rules;
- `docs/current/d/` — D roadmap/records, dormant until the new C11-C freeze;
- `docs/master-prompts/` — active cross-context handover/start prompts;
- `docs/history/` — immutable release archaeology and superseded evidence.
