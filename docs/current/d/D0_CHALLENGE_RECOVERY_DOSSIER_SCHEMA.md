# Entry state: C11-C 2.19.12 FROZEN

> D0 is active only after the frozen archive, SHA-256 and final acceptance report are verified.

# D0 — Challenge Recovery Dossier Schema

One dossier must be created for each historical Challenge `CHALLENGE_001` … `CHALLENGE_009` before D1 visual work starts.

```yaml
challenge_id:
mechanic:
mechanic_version:
historical_intent:
current_definition_path:
native_timing:
logical_geometry:
source_capture_contract:
delivery_profiles:
asset_references: []
asset_role_map: {}
seed_evidence: []
production_evidence: []
test_evidence: []
historical_docs: []
known_mismatches: []
open_questions: []
frozen_contracts_touched: []
d0_disposition:
```

## Rules

- A dossier records evidence; it does not invent missing history.
- Conflicts between a historical document and the frozen repository are logged as `known_mismatches`, with the current source identified as authoritative.
- `mechanic_version` and native timing must come from the current challenge definition/runtime contracts or explicit historical evidence.
- Asset provenance is descriptive until D2 defines a first-class registry.
- No dossier may require a change to C11-B simulation truth merely to make its historical presentation fit.
