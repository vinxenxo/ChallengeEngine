# tests/C7A501OfficialAudioArtifactManifestTest.gd
extends SceneTree

const AudioExportBridge = preload("res://core/audio/AudioExportBridge.gd")

var failures: Array[String] = []

class MockVideoTimeline extends VideoTimeline:
	func _init() -> void:
		super._init({
			"fps": 60,
			"hook_duration": 1.0,
			"game_duration": 2.0,
			"reveal_duration": 0.0,
			"cta_duration": 1.0
		})

	func get_total_frames() -> int:
		return hook_frames + game_frames + reveal_frames + cta_frames

class MockSimulationResult extends SimulationResult:
	func _init(seed_val: int) -> void:
		winning_frame = 30
		metadata = {
			"seed_used": seed_val
		}

func _init() -> void:
	print("[C7-A5.1] Generando corpus oficial de artefactos de audio y manifiesto de producción...")
	_run_generation()
	_conclude()

func _assert(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)
		print("[FAIL] " + message)
	else:
		print("[PASS] " + message)

func _run_generation() -> void:
	var fixtures = [
		{"id": "CHALLENGE_001", "profile": "c7_profile_tone_only"},
		{"id": "CHALLENGE_002", "profile": "c7_profile_noise_only"},
		{"id": "CHALLENGE_003", "profile": "c7_profile_mixed_alt"},
		{"id": "CHALLENGE_004", "profile": "c7_profile_mixed_overlap"},
		{"id": "CHALLENGE_005", "profile": "c7_profile_multi_noise"}
	]

	var export_dir := "res://artifacts/production/audiovisual/"
	DirAccess.make_dir_recursive_absolute(
		ProjectSettings.globalize_path(export_dir)
	)

	var timeline := MockVideoTimeline.new()
	var expected_total_samples: int = timeline.get_total_frames() * 735
	var manifest_entries = {}

	for fixture in fixtures:
		var ch_id = fixture["id"]
		var profile_id = fixture["profile"]
		
		var json_path = "res://tests/fixtures/c7/challenges/" + ch_id + ".json"
		var file = FileAccess.open(json_path, FileAccess.READ)
		if file == null:
			_assert(false, "[" + ch_id + "] No se pudo abrir el JSON del challenge.")
			continue
			
		var json_data = JSON.parse_string(file.get_as_text())
		file.close()
		
		if typeof(json_data) != TYPE_DICTIONARY:
			_assert(false, "[" + ch_id + "] Estructura JSON inválida.")
			continue

		var generation_cfg: Dictionary = json_data.get("generation", {})
		var seed: int = int(generation_cfg.get("seed", 0))
		_assert(seed != 0, "[" + ch_id + "] Seed canónica válida.")

		var sim_result := MockSimulationResult.new(seed)
		var pcm_relative_path = "res://artifacts/production/audiovisual/" + ch_id + ".pcm"
		var pcm_global_path = ProjectSettings.globalize_path(pcm_relative_path)

		var export_res = AudioExportBridge.render_and_export_track(
			sim_result,
			timeline,
			profile_id,
			pcm_global_path
		)

		_assert(export_res.get("success", false) == true, "[" + ch_id + "] Exportación PCM completada.")
		if not export_res.get("success", false):
			continue

		_assert(export_res.get("total_samples", 0) == expected_total_samples, "[" + ch_id + "] Muestras totales correctas.")
		
		var sha256_hash = str(export_res.get("canonical_hash", ""))
		_assert(sha256_hash.length() == 64, "[" + ch_id + "] Hash SHA-256 de artefacto generado.")

		manifest_entries[ch_id] = {
			"challenge_id": ch_id,
			"profile_id": profile_id,
			"seed": seed,
			"artifact_path": pcm_relative_path,
			"sample_rate": export_res.get("sample_rate"),
			"channels": export_res.get("channels"),
			"format": export_res.get("format"),
			"total_samples": export_res.get("total_samples"),
			"canonical_hash": sha256_hash
		}
		print("[C7-A5.1] Artefacto oficial registrado: ", ch_id, " -> ", sha256_hash.substr(0, 16) + "...")

	# Serializar el manifiesto global de producción
	var manifest_data = {
		"version": "C7-A5.1",
		"timestamp_utc": Time.get_datetime_string_from_system(true),
		"artifacts": manifest_entries
	}

	var manifest_file = FileAccess.open("res://artifacts/production/audiovisual/audio_corpus_manifest.json", FileAccess.WRITE)
	if manifest_file != null:
		manifest_file.store_string(JSON.stringify(manifest_data, "\t"))
		manifest_file.close()
		_assert(true, "Manifiesto global 'audio_corpus_manifest.json' escrito exitosamente.")
	else:
		_assert(false, "No se pudo escribir el manifiesto global de audio.")

func _conclude() -> void:
	if failures.is_empty():
		print("[C7-A5.1-TEST] RESULTADO GLOBAL: PASS")
		quit(0)
	else:
		for f in failures:
			push_error(f)
		print("[C7-A5.1-TEST] RESULTADO GLOBAL: FAIL failures=%d" % failures.size())
		quit(1)