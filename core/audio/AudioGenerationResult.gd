# res://core/audio/AudioGenerationResult.gd
class_name AudioGenerationResult
extends RefCounted

var generator_type: String
var profile_id: String
var duration_frames: int
var deterministic_parameters: Dictionary

func _init(p_gen: String, p_prof: String, p_frames: int, p_params: Dictionary):
	generator_type = p_gen
	profile_id = p_prof
	duration_frames = p_frames
	deterministic_parameters = p_params.duplicate()
	deterministic_parameters.make_read_only()

func is_equal(other: AudioGenerationResult) -> bool:
	if generator_type != other.generator_type: return false
	if profile_id != other.profile_id: return false
	if duration_frames != other.duration_frames: return false
	
	if deterministic_parameters.size() != other.deterministic_parameters.size(): return false
	for key in deterministic_parameters:
		if not other.deterministic_parameters.has(key): return false
		if deterministic_parameters[key] != other.deterministic_parameters[key]: return false
		
	return true