# res://core/audio/AudioProfile.gd
class_name AudioProfile
extends RefCounted

var profile_id: String
var generator_type: String
var parameters: Dictionary

func _init(p_profile_id: String, p_generator_type: String, p_parameters: Dictionary):
	profile_id = p_profile_id
	generator_type = p_generator_type
	
	for key in p_parameters:
		assert(typeof(key) == TYPE_STRING, "Claves de parámetros deben ser String")
		assert(_is_scalar(p_parameters[key]), "Parámetros deben ser escalares JSON-safe")
		
	parameters = p_parameters.duplicate()
	parameters.make_read_only()

func _is_scalar(value) -> bool:
	return typeof(value) in [TYPE_INT, TYPE_FLOAT, TYPE_STRING, TYPE_BOOL, TYPE_NIL]