# C11-D Shared Production GUI Dynamic Catalog — Checkpoint V1

## Purpose

Add a read-only, dynamically generated option catalog for future GUI cascading controls. It reads the existing D9.8 `build_catalog()` projection from the live C11-C Producer schema and reconciles its content-type support with the canonical D9.9 request contract and the future-GUI state schema. It does not embed a second list of families, subfamilies, grammars or variants.

## Interface

- `audit_dynamic_gui_catalog(project_root=None)` — source/contract/schema audit.
- `build_dynamic_gui_catalog(project_root=None)` — deterministic complete option snapshot.
- `get_family_options(content_type, mode='REVIEW', project_root=None)` — filtered family choices.
- `get_selector_options(content_type, family_id, mode='REVIEW', project_root=None)` — subtype/variant choices.
- `resolve_gui_catalog_selection(content_type, family_id, selector_id, mode='REVIEW', project_root=None)` — validates the chosen path through the canonical D9.8 selector resolver and returns a selection-only record.
- CLI: `--audit-only`, `--catalog`, `--families-for`, `--selectors-for`, `--resolve-selection`.

## Selection and governance

- Challenges: REVIEW and PRODUCTION modes while canonical state remains ACTIVE and request-plan compatible.
- Visual Loops and Visual Drills: available for REVIEW selection while their canonical catalog records remain ACTIVE_MODEL_ONLY / `request_plan_compatible=false`; PRODUCTION mode is rejected. Their flags are preserved and not promoted to active-compatible.
- Longform: represented in the catalog as disabled and never selectable.
- `auto` loop selector is represented as a selection mode, not as a concrete grammar.
- Unknown content types, families and selectors are rejected by the catalog and canonical D9.8 resolver.
- Catalog reads are in-memory/STDOUT only. No request or report is persisted; no rendering, media creation, native input, dispatch or release authority.

## Verification

Contract pins the frozen C11-C manifest first and eight canonical sources. Contract and response JSON schemas use Draft 2020-12. The tests compare API and CLI snapshots, exercise all selector domains and disabled modes, and verify source drift rejection in a temporary mirror.

## Boundary

This defines the data source for future dependent controls; it does not modify the existing GUI, wire GUI widget events, create a canonical production request, resolve presentation geometry, approve policy, or activate the renderer. `renderer=OFF`, `media_created=false`, `D4.8=BLOCKED`, `release_authority=NONE`, D9.17 NO-GO, D10 BLOCKED.
