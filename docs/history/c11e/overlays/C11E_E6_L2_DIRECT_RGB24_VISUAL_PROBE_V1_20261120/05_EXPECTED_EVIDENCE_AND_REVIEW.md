# Expected evidence and operator review

A successful runner must create a unique run folder with: capture metadata, source RGB24 bytes, source PNG preview, Godot import/capture logs, authoring snapshot, composed RGB24 bytes, composed PNG, JSON receipt and SHA-256 sidecar.

A PASS means only that one pinned scene frame was captured as opaque RGBA8, converted by byte-exact channel extraction to the required RGB24 buffer, and passed through the existing QImage compositor. It is not visual approval, six-selector Loop acceptance, Smoke18, or E6 acceptance.

`visual_resampler_review` remains `PENDING_OPERATOR_VISUAL_REVIEW`. The operator must inspect `composited_frame.png` and explicitly accept or reject the `SmoothTransformation` result. Geometry approval does not imply filtering-quality approval.
