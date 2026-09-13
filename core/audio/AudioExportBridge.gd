# core/audio/AudioExportBridge.gd
class_name AudioExportBridge
extends RefCounted

const SAMPLE_RATE = 44100
const SAMPLES_PER_FRAME = 735 # Relación exacta: 44100 / 60

# Renderiza toda la pista de audio de un challenge y la exporta a un archivo binario crudo .pcm
static func render_and_export_track(
	simulation_result: SimulationResult, 
	video_timeline: VideoTimeline, 
	audio_profile_id: String,
	output_path: String
) -> Dictionary:
	
	if simulation_result.metadata == null or not simulation_result.metadata.has("seed_used"):
		push_error("C7_AUDIO_EXPORT_MISSING_SEED_METADATA")
		return {"success": false, "error": "MISSING_SEED_METADATA"}
	
	var raw_seed = simulation_result.metadata["seed_used"]
	if typeof(raw_seed) != TYPE_INT and typeof(raw_seed) != TYPE_FLOAT:
		push_error("C7_AUDIO_EXPORT_INVALID_SEED_TYPE")
		return {"success": false, "error": "INVALID_SEED_TYPE"}
	var seed_used = int(raw_seed)
	
	var event_stream = AudioTimelineResolver.resolve(simulation_result, video_timeline)
	var events = event_stream.get_all_events()
	
	var total_frames = video_timeline.get_total_frames()
	var total_samples = total_frames * SAMPLES_PER_FRAME
	
	var master_buffer = AudioBuffer.new(SAMPLE_RATE, 1)
	master_buffer.data.resize(total_samples)
	for i in range(total_samples):
		master_buffer.data[i] = 0.0
		
	var registry_context = AudioRNGContext.new(seed_used, RNGStreamRegistry.new())
	var tone_generator = ToneBurstGenerator.new()
	
	for event in events:
		var profile = AudioProfileAdapter.from_authoring_profile(audio_profile_id, event.event_id)
		if profile == null:
			push_error("C7_AUDIO_EXPORT_PROFILE_RESOLUTION_FAILED for event: " + event.event_id)
			return {"success": false, "error": "PROFILE_RESOLUTION_FAILED"}
		
		# Instrumentación diagnóstica exigida
		print("[C7_DEBUG] event_id=", event.event_id, " generator_type=", profile.generator_type, " parameters=", profile.parameters)
		
		var gen_result = tone_generator.generate(profile, event, registry_context)
		if gen_result == null:
			push_error("C7_AUDIO_EXPORT_GENERATION_FAILED")
			return {"success": false, "error": "GENERATION_FAILED"}
		
		var event_buffer = ToneBurstPCMInterpreter.render(gen_result)
		if event_buffer == null or event_buffer.data.is_empty():
			push_error("C7_AUDIO_EXPORT_RENDER_FAILED")
			return {"success": false, "error": "RENDER_FAILED"}
		
		var start_sample = event.tick * SAMPLES_PER_FRAME
		for s in range(event_buffer.data.size()):
			var target_idx = start_sample + s
			if target_idx < total_samples:
				master_buffer.data[target_idx] += event_buffer.data[s]
				
	for i in range(total_samples):
		master_buffer.data[i] = clampf(master_buffer.data[i], -1.0, 1.0)
		
	var file = FileAccess.open(output_path, FileAccess.WRITE)
	if file == null:
		push_error("C7_AUDIO_EXPORT_FILE_OPEN_FAILED: " + output_path)
		return {
			"success": false,
			"error": "No se pudo abrir el archivo de salida PCM en: " + output_path
		}
		
	var pcm_bytes = master_buffer.get_pcm16_bytes()
	file.store_buffer(pcm_bytes)
	file.close()
	
	return {
		"success": true,
		"audio_path": output_path,
		"sample_rate": SAMPLE_RATE,
		"channels": 1,
		"format": "s16le",
		"total_samples": total_samples,
		"canonical_hash": master_buffer.get_canonical_hash()
	}