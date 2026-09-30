# D0 — Challenge Recovery Dossier Schema

One dossier is required for each `CHALLENGE_001` … `CHALLENGE_009` before D1 visual work.

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

Evidence is recorded, not invented. Conflicts are preserved as `known_mismatches` with the frozen source identified as authoritative.
