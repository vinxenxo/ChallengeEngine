class_name AudioEvent
extends RefCounted

var event_id: String
var tick: int
var sequence: int
var dynamic_payload: Dictionary

func _init(p_event_id: String, p_tick: int, p_sequence: int, p_payload: Dictionary = {}):
	event_id = p_event_id
	tick = p_tick
	sequence = p_sequence
	
	for key in p_payload:
		assert(typeof(key) == TYPE_STRING, "Claves de payload deben ser String")
		assert(_is_scalar(p_payload[key]), "Valores de payload deben ser escalares (int, float, string, bool, null)")
	
	dynamic_payload = p_payload.duplicate()
	dynamic_payload.make_read_only()

func _is_scalar(value) -> bool:
	return typeof(value) in [TYPE_INT, TYPE_FLOAT, TYPE_STRING, TYPE_BOOL, TYPE_NIL]

func is_before(other: AudioEvent) -> bool:
	if tick != other.tick:
		return tick < other.tick
	return sequence < other.sequence