# C11-D V2-B Candidate Semantic Review Request Overlay V1

Mode: ADD_ONLY. This increment adds a source-bound review request for the six typed custom-data candidates in the accepted V2-B evidence audit, a strict review-request schema, a separate schema for semantic decision records, a focused test, a checkpoint, and V12 continuity prompts.

It does not alter source/runtime behavior, challenge JSON, the accepted runtime report, C11-C, or any existing proposal. It does not authorize bindings, projection, payload materialization, media, renderer execution, dispatch, or release. Every field decision begins `PENDING_EXPLICIT_SEMANTIC_REVIEW` and every approval flag stays false.

Runtime audit SHA pinned: `8c4503c128355fa21e670be0aaea25b093a73c325253a2afcec2a066a92e5f00`. Runtime report SHA: `f7a1522695cbd6d3f3681d3f266b625e3062d5141c32cddbb4532bcb466e0446`. Source semantic review SHA: `374472b2d7ab0a70d94ed1f650302869b829252dcf06a7afe29c7c2e18e345dc`. Frozen C11-C manifest SHA: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

Apply using the manifest's source pins and add-only preconditions. Then run the focused static test against the exact audit JSON already accepted in the operator's `%TEMP%`. Do not rerun Godot.
