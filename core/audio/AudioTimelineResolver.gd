# core/audio/AudioTimelineResolver.gd
class_name AudioTimelineResolver
extends RefCounted

# Transforma el resultado de la simulación y la estructura temporal en un stream auditado y ordenado
static func resolve(simulation_result: SimulationResult, video_timeline: VideoTimeline) -> AudioEventStream:
	var stream = AudioEventStream.new()
	
	# 1. Evento de inicio en el Hook (Tick 0 absoluto, sequence 0)
	if video_timeline.hook_frames > 0:
		stream.add_event(AudioEvent.new("countdown_tick", 0, 0, {"intensity": 0.5}))
	
	# 2. Inyección del evento en el winning_frame GAME-relative ajustado al offset absoluto de la timeline
	var winning_frame = simulation_result.winning_frame
	if winning_frame >= 0:
		var absolute_win_tick = video_timeline.hook_frames + winning_frame
		
		# Verificamos si ya existe algún evento en ese mismo tick exacto para escalar la sequence si fuera necesario
		var existing_at_tick = stream.get_events_for_tick(absolute_win_tick)
		var seq = 0
		if existing_at_tick.size() > 0:
			seq = existing_at_tick.size() # Asigna sequence incremental determinista para evitar colisión
			
		stream.add_event(AudioEvent.new("success_reveal", absolute_win_tick, seq, {"pitch_ratio": 1.2}))
		
	# 3. Evento de transición para la fase de CTA derivado contractualmente de la suma de fases reales
	if video_timeline.cta_frames > 0:
		var cta_start_tick = video_timeline.hook_frames + video_timeline.game_frames + video_timeline.reveal_frames
		
		var existing_at_cta = stream.get_events_for_tick(cta_start_tick)
		var seq_cta = 0
		if existing_at_cta.size() > 0:
			seq_cta = existing_at_cta.size()
			
		stream.add_event(AudioEvent.new("cta_transition", cta_start_tick, seq_cta, {}))
		
	stream.seal()
	return stream