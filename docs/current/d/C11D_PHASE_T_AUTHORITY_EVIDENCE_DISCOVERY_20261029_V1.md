# C11-D Phase T — Repository Authority Evidence Discovery V1

**Gate mode:** `READ_ONLY_AUTHORITY_EVIDENCE_DISCOVERY`  
**Prerequisite:** Phase S closeout `PASS_HASH_AND_GOVERNANCE_CHECK`.  
**Purpose:** search the checkout working tree for possible explicit authority/approval records outside the already pinned Phase P/Q/R/S set, and produce a hashed candidate inventory for human review.

## Scope and limits

The scanner traverses eligible working-tree text files, hashes each file it inspects, calculates a deterministic aggregate scan-index hash, records matches with line numbers/snippets, and inventories document/archive formats that it cannot content-search. It skips known generated/cache/vendor directories and excludes its own Phase T harness/results to avoid self-matches. It does **not** inspect Git history, external files, file contents inside archives, or the contents of binary PDF/Office documents. Those exclusions are reported; therefore the scan cannot prove global absence of authority evidence.

Candidate matches are leads only. A filename or keyword match is not proof of valid authority. Human review must verify issuer/role, authority scope, exact decision text, covered policy IDs, effective date/version, signatures or immutable record identity, source pins, and any required conditions. A record that says “not approved”, “blocked”, “missing”, or “not adopted” is not an approval.

## Search behavior

- Searchable text extensions include Markdown, plain text, JSON, YAML, TOML, CSV, PowerShell, Python, GDScript, Godot scene/resource, XML, INI/CFG, RST and logs.
- A single text file larger than 4 MiB is listed as skipped, not silently treated as searched.
- The scan excludes `.git`, `.godot`, `node_modules`, `.venv`, `venv`, `__pycache__`, `bin`, `obj`, `dist`, `build`, `.pytest_cache`, `.mypy_cache`, `cache`, `tmp` and `temp` directory segments, plus Phase T's own files/results.
- PDF/Office documents and archive files are inventoried by path, size and hash when possible, but their contents are not searched by this PowerShell-only gate.
- Any scan error makes the scan incomplete. Candidate findings and unsearched documents require review; no automatic policy adjudication is performed.

## Required governance invariants

`renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `automatic_seed_generation=false`; `master_seed=NOT_ADOPTED`; `approved_bindings=0`; `approved_custom_data_bindings=0`; `approved_renderer_projection_bindings=0`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`.

The 11s-versus-12s timing conflicts for CHALLENGE_008/009 remain unchanged. Phase T does not change `AGENTS.md`, `CONTINUE.md`, the frozen C11-C manifest, policy matrices, or approval counts.

## Operator sequence

1. Apply this packet add-only and verify source pins.
2. Run `scan_d_renderer_phase_t_authority_evidence_discovery_20261029.ps1 -Root <checkout>` to create a report under a short temporary path.
3. Run the Phase T Python suite against the emitted JSON report; require `40/40`, exit 0, and preserve stdout/stderr hashes.
4. Run the same scanner with `-RecordResults`, passing both report paths and both test log paths. This copies the evidence into stable add-only records only after all preconditions pass.
5. Run the postcheck. Review any candidates and any unsearched documents before deciding the next gate.

The scanner does not decide whether any item is valid authority. A result with zero candidates still means “no candidate matched this search configuration”, not “no authority exists”.
