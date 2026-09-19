# tests/C7A07MultiProfileCorpusTest.gd
extends SceneTree

const AudioGeneratorRegistry = preload("res://core/audio/AudioGeneratorRegistry.gd")
const AudioProfileAdapter = preload("res://core/audio/AudioProfileAdapter.gd")
const AudioEvent = preload("res://core/audio/AudioEvent.gd")
const AudioRNGContext = preload("res://core/audio/AudioRNGContext.gd")
const RNGStreamRegistry = preload("res://core/deterministic/RNGStreamRegistry.gd")
const ToneBurstPCMInterpreter = preload("res://core/audio/renderers/ToneBurstPCMInterpreter.gd")
const NoiseBurstPCMInterpreter = preload("res://core/audio/renderers/NoiseBurstPCMInterpreter.gd")

var failures: Array[String] = []

func _init() -> void:
	print("[C7A07-TEST] Iniciando verificación estricta de corpus multiperfil (C7-A4.5)...")
	_run_tests()
	_conclude()

func _assert(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)
		print("[FAIL] " + message)
	else:
		print("[PASS] " + message)

func _run_tests() -> void:
	var registry = AudioGeneratorRegistry.new()
	var expected_fixtures = [
		{
			"id": "CHALLENGE_001",
			"profile": "c7_profile_tone_only",
			"events": ["countdown_tick", "success_reveal"]
		},
		{
			"id": "CHALLENGE_002",
			"profile": "c7_profile_noise_only",
			"events": ["countdown_tick", "success_reveal"]
		},
		{
			"id": "CHALLENGE_003",
			"profile": "c7_profile_mixed_alt",
			"events": ["countdown_tick", "success_reveal", "cta_transition"]
		},
		{
			"id": "CHALLENGE_004",
			"profile": "c7_profile_mixed_overlap",
			"events": ["countdown_tick", "success_reveal", "near_miss"]
		},
		{
			"id": "CHALLENGE_005",
			"profile": "c7_profile_multi_noise",
			"events": ["countdown_tick", "success_reveal", "cta_transition"]
		}
	]

	for fixture in expected_fixtures:
		var ch_id = fixture["id"]
		var profile_id = fixture["profile"]
		var expected_events: Array = fixture["events"]
		
		var json_path = "res://tests/fixtures/c7/challenges/" + ch_id + ".json"
		var file = FileAccess.open(json_path, FileAccess.READ)
		if file == null:
			_assert(false, "[" + ch_id + "] No se pudo abrir el archivo JSON en " + json_path)
			continue
			
		var json_text = file.get_as_text()
		file.close()
		
		var json = JSON.new()
		var error = json.parse(json_text)
		if error != OK:
			_assert(false, "[" + ch_id + "] Error de parseo JSON: " + json.get_error_message())
			continue
			
		var data = json.get_data()
		var audio_cfg = data.get("canonical_v2", {}).get("audio", {})
		
		var cfg_enabled = audio_cfg.get("enabled", false) == true
		var cfg_profile = audio_cfg.get("profile_id") == profile_id
		
		_assert(cfg_enabled, "[" + ch_id + "] Audio debe estar habilitado.")
		_assert(cfg_profile, "[" + ch_id + "] profile_id coincide con la matriz canónica.")
		
		var fixture_ok = cfg_enabled and cfg_profile
		
		for ev_id in expected_events:
			var profile = AudioProfileAdapter.from_authoring_profile(profile_id, ev_id)
			if profile == null:
				fixture_ok = false
				_assert(false, "[" + ch_id + ":" + ev_id + "] AudioProfileAdapter falló al resolver el perfil.")
				continue
				
			_assert(profile.profile_id == profile_id, "[" + ch_id + ":" + ev_id + "] El profile_id resuelto coincide.")
			_assert(not profile.generator_type.is_empty(), "[" + ch_id + ":" + ev_id + "] generator_type no vacío.")
			
			print(
				"[C7A07-DEBUG] ",
				ch_id,
				":",
				ev_id,
				" generator_type=",
				profile.generator_type,
				" parameters=",
				profile.parameters
			)


			var event_stub = AudioEvent.new(ev_id, 0, 0, {})

			var generation_cfg: Dictionary = data.get("generation", {})
			var canonical_seed: int = int(generation_cfg.get("seed", 0))

			_assert(
				canonical_seed != 0,
				"[" + ch_id + "] generation.seed debe existir y ser distinto de cero."
			)

			var rng_ctx := AudioRNGContext.new(
				canonical_seed,
				RNGStreamRegistry.new()
			)
			
            
			var gen_result = registry.generate(profile.generator_type, profile, event_stub, rng_ctx)
			if gen_result == null:
				fixture_ok = false
				_assert(false, "[" + ch_id + ":" + ev_id + "] El registry falló al generar.")
				continue
				
			var buffer = null
			if gen_result.generator_type == "tone_burst":
				buffer = ToneBurstPCMInterpreter.render(gen_result)
			elif gen_result.generator_type == "noise_burst":
				buffer = NoiseBurstPCMInterpreter.render(gen_result)
				
			if buffer == null or buffer.data.is_empty() or buffer.get_canonical_hash().length() != 64:
				fixture_ok = false
				_assert(false, "[" + ch_id + ":" + ev_id + "] Falló la renderización PCM o el hash canónico.")
			else:
				_assert(true, "[" + ch_id + ":" + ev_id + "] PCM renderizado y hash SHA-256 válidos.")

		if fixture_ok:
			print("[C7A07] " + ch_id + " " + profile_id.lpad(24, " ") + "      PASS")
		else:
			print("[C7A07] " + ch_id + " " + profile_id.lpad(24, " ") + "      FAIL")

func _conclude() -> void:
	if failures.is_empty():
		print("[C7A07-TEST] RESULTADO GLOBAL: PASS")
		quit(0)
	else:
		push_error("[C7A07-TEST] RESULTADO GLOBAL: FAIL failures=%d" % failures.size())
		quit(1)