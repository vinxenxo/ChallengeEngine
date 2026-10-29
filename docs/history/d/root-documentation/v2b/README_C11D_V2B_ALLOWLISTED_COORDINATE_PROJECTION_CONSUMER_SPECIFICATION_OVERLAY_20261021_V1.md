# C11-D V2-B Allowlisted Coordinate Projection Consumer Specification Overlay V1

Mode: `ADD_ONLY`. Status: `SPECIFICATION_ONLY_NOT_IMPLEMENTED`. Payload contains the closed JSON consumer contract, JSON Schema, read-only stdlib regression suite, checkpoint, current continuity checkpoint, and two V19 prompts.

The specification is deliberately renderer-neutral. It admits exactly four candidates and leaves CHALLENGE_008 / CHALLENGE_009 blocked. It reads one explicitly allowlisted custom_data field per source frame; it does not copy or serialize `FrameSnapshot.custom_data`. It preserves the existing frame sequence and emits only logical target marker descriptors.

No production consumer code is included. No bindings, renderer projection, payload materialization, media creation or render test are approved. Pixel rounding and raster crop semantics remain blocked. C11-C stays immutable.

## Windows validation

Apply and test separately from the root `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. The regression suite uses Python standard library only and accepts the exact coordinate-policy decision receipt path as its second argument.
