class_name ChallengeRuntimeContext
extends RefCounted

## C6-F4.1 — Runtime Context
## Data-only transport object for the resolved C6 runtime state.
## This class owns no migration, execution, timeline, validation, RNG,
## asset-loading or rendering behaviour.

var canonical_v2: Dictionary = {}
var simulation_result: SimulationResult = null
var timeline: VideoTimeline = null
var presentation_binding: PresentationBindingResult = null
