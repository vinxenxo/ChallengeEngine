# res://core/execution/ChallengeExecutionPipeline.gd
class_name ChallengeExecutionPipeline
extends RefCounted

const MechanicRegistry = preload("res://core/mechanics/MechanicRegistry.gd")
const VideoProfileRegistry = preload("res://core/authoring/VideoProfileRegistry.gd")
const RNGStreamRegistry = preload("res://core/deterministic/RNGStreamRegistry.gd")
const StructuralRNG = preload("res://core/deterministic/StructuralRNG.gd")
const MechanicRNGContext = preload("res://core/deterministic/MechanicRNGContext.gd")

static func execute(canonical_v2: Dictionary) -> Dictionary:
	# ---------------------------------------------------------
	# 1. Structural Validation (Authoring V2 Gate)
	# ---------------------------------------------------------
	if canonical_v2.is_empty() or not canonical_v2.has("mechanic") or not canonical_v2.has("simulation") or not canonical_v2.has("video"):
		return {
			"success": false,
			"error": "Invalid Canonical V2 structure: missing required root sections.",
			"simulation_result": null
		}
		
	var mechanic_id = str(canonical_v2.get("mechanic", ""))
	if mechanic_id.strip_edges().is_empty():
		return {
			"success": false,
			"error": "Challenge definition missing mechanic ID.",
			"simulation_result": null
		}
		
	# ---------------------------------------------------------
	# 2. Mechanic Instance Resolution
	# ---------------------------------------------------------
	var mechanic = MechanicRegistry.create_mechanic(mechanic_id)
	if mechanic == null:
		return {
			"success": false,
			"error": "Failed to create mechanic instance for: '%s'" % mechanic_id,
			"simulation_result": null
		}
		
	# ---------------------------------------------------------
	# 3. Extraction of Generation Parameters & RNG Isolation
	# ---------------------------------------------------------
	var simulation: Dictionary = canonical_v2.get("simulation", {})
	if not simulation is Dictionary:
		return {
			"success": false,
			"error": "Canonical V2 simulation section is not a Dictionary.",
			"simulation_result": null
		}

	# Canonical V2 source of truth. Legacy generation remains a compatibility
	# fallback for pre-F4.4 productive fixtures.
	var generation = canonical_v2.get("generation", {})
	var seed = int(simulation.get("seed", generation.get("seed", 0)))
	var rng_version = str(simulation.get("rng_version", generation.get("rng_version", "1.0")))
	
	if rng_version == "2.0":
		var registry = RNGStreamRegistry.new()
		var structural = StructuralRNG.new(registry)
		var streams: Array[int] = []
		var consumer := ""
		
		match mechanic_id:
			"pilot":
				streams = [10, 20]
				consumer = "PilotMechanic"
			"parking_v2":
				streams = [30, 40, 50, 60]
				consumer = "ParkingMechanic"
			"hit_v1":
				streams = [70, 80, 90]
				consumer = "HitMechanic"
			"catch_v1":
				streams = [100, 110, 120]
				consumer = "CatchMechanic"
			"find_v1":
				streams = [130, 140, 150, 160]
				consumer = "FindMechanic"
			_:
				streams = []
				
		if not streams.is_empty():
			var created = MechanicRNGContext.create(seed, rng_version, consumer, streams, structural, registry)
			if not created.is_valid:
				return {
					"success": false,
					"error": "Failed to create MechanicRNGContext for '%s' (Error: %s)" % [mechanic_id, created.error_code],
					"simulation_result": null
				}
			mechanic.set_rng_context(created.context)
			
	# ---------------------------------------------------------
	# 4. Temporal Setup & Game Frames Preparation
	# ---------------------------------------------------------
	mechanic.setup(canonical_v2)
	
	var video_binding = canonical_v2.get("video", "")
	var video_profile: Dictionary = {}
	if video_binding is Dictionary:
		video_profile = _normalize_inline_canonical_video(video_binding)
	else:
		var video_profile_id = str(video_binding)
		video_profile = VideoProfileRegistry.get_profile(video_profile_id)

	if video_profile.is_empty():
		return {
			"success": false,
			"error": "Execution pipeline failed to resolve video profile binding: %s" % str(video_binding),
			"simulation_result": null
		}
		
	var fps = int(video_profile.get("fps", 30))
	var phases = video_profile.get("phases", {})
	var game_duration = float(phases.get("game_duration", 6.0))
	var game_frames = int(round(game_duration * fps))
	
	if mechanic.has_method("prepare"):
		mechanic.prepare(game_frames)
		
	# ---------------------------------------------------------
	# 5. Execution (Sovereign Simulation)
	# ---------------------------------------------------------
	var sim_result = mechanic.simulate(game_frames, seed, canonical_v2)
	if sim_result == null:
		return {
			"success": false,
			"error": "Mechanic simulate() returned null result.",
			"simulation_result": null
		}
		
	return {
		"success": true,
		"error": "",
		"simulation_result": sim_result
	}


static func _normalize_inline_canonical_video(video: Dictionary) -> Dictionary:
	# F4.4 Phase 1: Canonical V2 stores temporal fields flat under video.
	# F3 consumes a VideoProfile-shaped view internally; this normalization is
	# local, non-persistent, and never mutates the canonical input.
	if not video.has("fps") or not video.has("game_duration"):
		return {}

	return {
		"profile_id": "__inline_canonical_v2__",
		"fps": int(round(float(video.get("fps", 30)))),
		"phases": {
			"hook_duration": float(video.get("hook_duration", 0.0)),
			"game_duration": float(video.get("game_duration")),
			"reveal_duration": float(video.get("reveal_duration", 0.0)),
			"cta_duration": float(video.get("cta_duration", 0.0))
		}
	}
