# C11-D Phase V — Authority Candidate Source Review V1

## Purpose

Validate current source bytes for all 107 Phase U candidates, extract bounded current-source context around saved match lines for the 50 high-priority candidates, and record the current existence/hash/size of seven Phase T documents whose content was not inspected. This is read-only evidence preparation, not adjudication.

## Required outcomes

- Verify source SHA-256 and byte length for all 107 candidate paths against the Phase U triage queue.
- For exact-hash high-priority text files within the 512 KiB excerpt limit, extract no more than three windows per candidate, each with three lines of context on either side and a maximum excerpt length of 1,800 characters.
- Preserve each candidate's `NOT_REVIEWED` / `UNDETERMINED` state.
- Keep all seven unsearched documents `NOT_INSPECTED` / `UNDETERMINED`; hash/size checks are not content inspection.
- Produce a JSON and Markdown evidence packet whose hashes and source relationships can be verified.

## Interpretive limits

The 50/55/2 priority grouping is a keyword heuristic only. A hash match proves current bytes match the previously recorded source, not that the document is authoritative, current, approved, or applicable. Excerpts are navigation aids; the full document must be reviewed before any authority finding.

## Guardrails

`renderer=OFF`, zero approved bindings, `release_authority=NONE`. No runtime, Godot, payload, media or renderer action. CHALLENGE_008 and CHALLENGE_009 remain blocked at 11 seconds declared versus 12 seconds summed phases. C11-C remains the authoritative production baseline until the D baseline is formally accepted, frozen and promoted.

## Run

Use `tools/c11d/d9/review_d_renderer_phase_v_authority_candidate_sources_20261029.py`, then run the companion 40-test suite and verifier against the generated report. Retain source pin mismatches as blockers; never update hashes automatically. After the report is recorded, review full candidate sources and all seven uncovered documents manually.
