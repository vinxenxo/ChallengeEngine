# core/audio/AudioEventStream.gd
class_name AudioEventStream
extends RefCounted

var _events: Array[AudioEvent] = []
var _is_sealed: bool = false

# Añade un evento validando unicidad de tupla (tick, sequence), límites no negativos y orden temporal
func add_event(event: AudioEvent) -> void:
	assert(not _is_sealed, "El stream de eventos está sellado y no admite modificaciones.")
	assert(event.tick >= 0, "CRÍTICO: El tick de un AudioEvent no puede ser negativo (%d)." % event.tick)
	assert(event.sequence >= 0, "CRÍTICO: La sequence de un AudioEvent no puede ser negativa (%d)." % event.sequence)
	
	# Comprobación de unicidad estricta y orden total de la tupla (tick, sequence)
	for existing in _events:
		assert(
			not (existing.tick == event.tick and existing.sequence == event.sequence),
			"CRÍTICO: Colisión de tupla (tick, sequence) en AudioEventStream: tick=%d, seq=%d" % [event.tick, event.sequence]
		)
	
	_events.append(event)
	# Ordenación estricta por tick ascendente, y secundariamente por sequence ascendente
	_events.sort_custom(func(a, b):
		if a.tick != b.tick:
			return a.tick < b.tick
		return a.sequence < b.sequence
	)

func seal() -> void:
	_is_sealed = true

func get_events_for_tick(tick: int) -> Array[AudioEvent]:
	var matching: Array[AudioEvent] = []
	for event in _events:
		if event.tick == tick:
			matching.append(event)
		elif event.tick > tick:
			break # Como el array está ordenado cronológicamente, cortamos la búsqueda
	return matching

# Devuelve una copia de sólo lectura para garantizar la inmutabilidad absoluta del stream sellado
func get_all_events() -> Array[AudioEvent]:
	var snapshot: Array[AudioEvent] = _events.duplicate(true)
	snapshot.make_read_only()
	return snapshot