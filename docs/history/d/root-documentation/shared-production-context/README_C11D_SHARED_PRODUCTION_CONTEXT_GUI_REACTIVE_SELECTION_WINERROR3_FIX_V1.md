# C11-D Shared Production GUI Reactive Selection WinError 3 Fix V1

## Purpose

Fixes the source-drift negative test for the reactive GUI selection state. The prior test copied the entire repository into a temporary directory. On Windows, deep paths under the multi-gigabyte `artifacts/` tree could not be recreated, producing `WinError 3` before the deliberate source-drift check ran.

## Change

The test now stages only the direct source-lineage files and the contract/schemas required by `audit_reactive_selection_contract`. It alters the catalog source in that temporary mirror and expects the exact fail-closed reason `Pinned source drift`. The real repository, its `artifacts/` tree, and all production media remain untouched.

## Scope and governance

- One modified test file and one updated checkpoint; this is not a production code change.
- The reactive GUI implementation, dynamic catalog, canonical state, C11-C frozen inputs and manifest are unchanged.
- No renderer input, dispatch, persistence or media creation.
- The Windows operator must rerun the focused test and the regression sequence after applying.
- `renderer=OFF`, `media_created=false`, `D4.8=BLOCKED`, `release_authority=NONE`; D9.17 remains NO-GO and D10 remains blocked.
