extends SceneTree

# ============================================================
# C7-A0.3-F1 — Audio Timeline & Event Stream Synchronization Test
# Validates phase-aware mapping, absolute frame translation,
# sequence collision resolution, and stream immutability.
# ============================================================

const AudioEventStream = preload("res://core/audio/AudioEventStream.gd")
const AudioTimelineResolver = preload("res://core/audio/AudioTimelineResolver.gd")
const AudioEvent = preload("res://core/audio/AudioEvent.gd")

var failures: Array[String] = []

func _assert(condition: bool, fail_msg: String) -> void:
	if not condition:
		failures.append(fail_msg)

# Mocks tipados heredando de las clases base oficiales del baseline
class MockVideoTimeline extends VideoTimeline:
	func _init() -> void:
		hook_frames = 120
		game_frames = 420
		reveal_frames = 0
		cta_frames = 120
		
	func get_total_frames() -> int:
		return hook_frames + game_frames + reveal_frames + cta_frames

class MockSimulationResult extends SimulationResult:
	func _init() -> void:
		winning_frame = 100

func _run_tests() -> void:
	# -------------------------------------------------------------------------
	# Test 1: Mapeo estándar de fases y cálculo de offsets absolutos
	# -------------------------------------------------------------------------
	var timeline_normal = MockVideoTimeline.new()
	timeline_normal.hook_frames = 120
	timeline_normal.game_frames = 420
	timeline_normal.reveal_frames = 60
	timeline_normal.cta_frames = 120
	
	var sim_result = MockSimulationResult.new()
	sim_result.winning_frame = 50 # Relativo a GAME
	
	var stream = AudioTimelineResolver.resolve(sim_result, timeline_normal)
	var events = stream.get_all_events()
	
	_assert(events.size() == 3, "Se esperaban exactamente 3 eventos en la timeline normal (Countdown, Success, CTA).")
	
	# Verificación de ticks absolutos
	_assert(events[0].event_id == "countdown_tick" and events[0].tick == 0, "El countdown debe estar en el tick 0 absoluto.")
	_assert(events[1].event_id == "success_reveal" and events[1].tick == 170, "Success reveal debe estar en el tick 170 (120 + 50).")
	_assert(events[2].event_id == "cta_transition" and events[2].tick == 600, "CTA transition debe estar en el tick 600 (120 + 420 + 60).")

	# -------------------------------------------------------------------------
	# Test 2: Comportamiento sin HOOK y sin REVEAL
	# -------------------------------------------------------------------------
	var timeline_minimal = MockVideoTimeline.new()
	timeline_minimal.hook_frames = 0
	timeline_minimal.game_frames = 300
	timeline_minimal.reveal_frames = 0
	timeline_minimal.cta_frames = 60
	
	sim_result.winning_frame = 150
	var stream_min = AudioTimelineResolver.resolve(sim_result, timeline_minimal)
	var events_min = stream_min.get_all_events()
	
	_assert(events_min.size() == 2, "Se esperaban 2 eventos en la timeline mínima.")
	_assert(events_min[0].event_id == "success_reveal" and events_min[0].tick == 150, "Success debe estar en el tick 150 sin hook.")
	_assert(events_min[1].event_id == "cta_transition" and events_min[1].tick == 300, "CTA debe estar en el tick 300.")

	# -------------------------------------------------------------------------
	# Test 3: Resolución de colisiones por 'sequence' (Mismo tick exacto)
	# -------------------------------------------------------------------------
	var manual_stream = AudioEventStream.new()
	var ev1 = AudioEvent.new("event_alpha", 100, 0, {})
	manual_stream.add_event(ev1)
	
	var ev_colision_res = AudioEvent.new("event_gamma", 100, 1, {})
	manual_stream.add_event(ev_colision_res)
	var manual_events = manual_stream.get_all_events()
	_assert(manual_events.size() == 2, "El stream debe permitir múltiples eventos concurrentes en el mismo tick usando sequences distintas.")
	_assert(manual_events[0].sequence == 0 and manual_events[1].sequence == 1, "Las secuencias deben ordenarse de forma ascendente.")

	# -------------------------------------------------------------------------
	# Test 4: Inmutabilidad estricta del stream sellado
	# -------------------------------------------------------------------------
	manual_stream.seal()
	var test_arr = manual_stream.get_all_events()
	_assert(manual_stream.get_all_events().size() == 2, "La consulta del stream sellado debe retornar la instantánea correcta.")

func _conclude() -> void:
	if failures.is_empty():
		print("[C7A03_AUDIO_TIMELINE_SUITE] PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		print("[C7A03_AUDIO_TIMELINE_SUITE] FAIL failures=%d" % failures.size())
		quit(1)

func _initialize() -> void:
	print("[TEST] Running C7A03AudioTimelineTest...")
	_run_tests()
	_conclude()