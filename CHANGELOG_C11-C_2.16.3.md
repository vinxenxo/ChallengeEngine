# C11-C 2.16.3 — Resume Reliability and Editorial Spacing

- Fixed extraordinary review resume with persistent per-item state and artifact recovery.
- Resume now recovers seeds from a partial state file when the final corpus manifest does not yet exist.
- Authoring snapshots are isolated to the review output root to prevent concurrent missing-authoring failures.
- Retained seven workers and typed Drill seed binding.
- Header target font increased to 29 logical px, Bold.
- Header/Footer separation increased to 20 logical px.
- Visible Header/Footer separator rules retained.


### Artifact-isolation hotfix
- Review-only `-OutputTag <grammar>` added to all five Visual Loop launchers.
- The review runner uses the grammar tag for every concurrent loop render.
- Exact grammar-qualified manifest matching prevents Resume ambiguity when Invisible Forces reuses seeds across seven grammars.
- Resume now constructs an explicit pending queue and reports the pending count.

- Visual Loop manifests/log markers now identify the active 2.16.3 refinement revision.
- Resume validates the physical artifact set on every skip rather than trusting a stale ledger entry alone.
