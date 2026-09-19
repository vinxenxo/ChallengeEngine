# Data and Contracts

## Canonical truth flow

`Definition -> deterministic simulation -> SimulationResult / FrameSnapshot -> passive presentation -> RenderedFrameStream -> production artifact`

## Canonical visual envelope

The visual loop/drill envelope remains the C6-F0.8 contract. C11 does not extend it with social-frame text fields. QA diagnostics are presentation-only and are injected by the playback/export tooling.

## Challenge contracts

Historical challenge definitions keep their native mechanic and RNG versions. Examples currently covered by C11-A.1:

- CHALLENGE_001: key / RNG 1.0
- CHALLENGE_002: parking legacy / RNG 1.0
- CHALLENGE_003: pilot / RNG 2.0
- CHALLENGE_004: parking_v2 / RNG 2.0
- CHALLENGE_005: hit_v1 / RNG 2.0
- CHALLENGE_006: catch_v1 / RNG 2.0
- CHALLENGE_007: find_v1 / RNG 2.0
- CHALLENGE_008: choose_v1 / RNG 2.0
- CHALLENGE_009: count_v1 / RNG 2.0

## Presentation contract

`UnifiedSocialFrame` owns structural regions. `PresentationFramer` and `CoordinateMapper` determine how existing logical geometry is placed inside the Body region.

No presentation change may alter the semantic contents of `SimulationResult`.
