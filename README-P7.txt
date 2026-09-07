# C6-F4.4-P7 COUNT

Minimal migration:
- CountMechanic consumes simulation.parameters.count first.
- Legacy difficulty.count/content remains fallback only.
- simulation.seed is authoritative in V2; generation.seed remains legacy fallback.
- ChallengeRuntimeBridge adds count_v1 to the native-V2 allow-list.
- Dedicated test uses the real Oracle API: ChallengeLegacyRuntimeOracle.run().
- Test compares logical discrete custom_data and global metrics.

Do not modify RNG stream definitions, mechanics math, SimulationResult,
WinningFrameDetector, VideoTimeline, or build_factory.py.
