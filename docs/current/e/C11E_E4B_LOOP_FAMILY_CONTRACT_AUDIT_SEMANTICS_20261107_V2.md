# E4B Loop Family Contract Audit Semantics — V2

## Authoritative meaning

The audit is executed with `--project-root` pointing to the active checkout. It inspects manifest/authoring metadata and tests file existence at paths relative to that checkout. It does not open, decode, probe, compare or visually inspect MP4 content.

V2 therefore reports `audit_target=ACTIVE_CHECKOUT_PROJECT_ROOT`, `mp4_present_in_project_root_count`, and per-selector `mp4_present_in_project_root`. The aggregate must equal the sum of the 27 explicit booleans and remain within 0..27. Both zero and 27 are valid observations. `visual_review_performed=false` is mandatory.

## Interpretation

- `mp4_present_in_project_root=true`: a file exists at the path named by the historical production manifest.
- `visual_review_performed=false`: no visual acceptance is claimed, regardless of file count.
- This audit does not establish MP4 decode health, ffprobe metadata, frame count, frame order, aspect ratio, pixel geometry, overlays, text shaping, audio or human approval.

## V1 correction

V1 named the active-checkout observation as a snapshot count and its test/runner required zero. That assumption failed on the operator checkout (27). V2 keeps V1 files immutable and uses a wrapper with accurate field names, dynamic validation and tests for absent, present and mixed cases.
