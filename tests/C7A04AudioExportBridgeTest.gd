extends SceneTree

# ============================================================
# C7-A0.4-F1 — Audio Export Bridge & PCM Master File Test
# Validates physical specs, byte-exact equality/divergence,
# hash determinism, and isolated process fail-closed rejection.
# ============================================================

const AudioExportBridge = preload("res://core/audio/AudioExportBridge.gd")

var failures: Array[String] = []

func _assert(condition: bool, fail_msg: String) -> void:
	if not condition:
		failures.append(fail_msg)

class MockVideoTimeline extends VideoTimeline:
	func _init() -> void:
		hook_frames = 60
		game_frames = 120
		reveal_frames = 0
		cta_frames = 60
		
	func get_total_frames() -> int:
		return hook_frames + game_frames + reveal_frames + cta_frames

class MockSimulationResult extends SimulationResult:
	func _init(seed_val: int) -> void:
		winning_frame = 30
		metadata = {"seed_used": seed_val}

func _run_tests() -> void:
	var profile_id = "c7_test_profile"
	var timeline = MockVideoTimeline.new()
	var path_a = "user://test_master_a.pcm"
	var path_b = "user://test_master_b.pcm"
	var path_c = "user://test_master_c.pcm"
	
	# -------------------------------------------------------------------------
	# 1. Ejecuciones A y B (Misma Seed 77777 -> Bit-exact determinism y specs físicas)
	# -------------------------------------------------------------------------
	var sim_a = MockSimulationResult.new(77777)
	var res_a = AudioExportBridge.render_and_export_track(sim_a, timeline, profile_id, ProjectSettings.globalize_path(path_a))
	if not res_a.get("success", false):
		failures.append("Exportación A falló: " + str(res_a.get("error", "unknown")))
		return
	
	var sim_b = MockSimulationResult.new(77777)
	var res_b = AudioExportBridge.render_and_export_track(sim_b, timeline, profile_id, ProjectSettings.globalize_path(path_b))
	if not res_b.get("success", false):
		failures.append("Exportación B falló: " + str(res_b.get("error", "unknown")))
		return
	
	_assert(res_a["sample_rate"] == 44100, "sample_rate debe ser 44100.")
	_assert(res_a["channels"] == 1, "channels debe ser 1 (mono).")
	_assert(res_a["format"] == "s16le", "format debe ser s16le.")
	
	var expected_total_samples = timeline.get_total_frames() * 735
	_assert(res_a["total_samples"] == expected_total_samples, "total_samples debe coincidir con timeline * 735.")
	_assert(FileAccess.file_exists(path_a) or FileAccess.file_exists(ProjectSettings.globalize_path(path_a)), "El fichero .pcm debe existir físicamente en disco.")
	
	_assert(res_a["canonical_hash"] == res_b["canonical_hash"], "Fallo Determinismo Hash: Dos renders con idéntica seed deben producir el mismo SHA-256.")
	
	var file_a = FileAccess.open(path_a, FileAccess.READ)
	var file_b = FileAccess.open(path_b, FileAccess.READ)
	if file_a != null and file_b != null:
		var bytes_a = file_a.get_buffer(file_a.get_length())
		var bytes_b = file_b.get_buffer(file_b.get_length())
		file_a.close()
		file_b.close()
		_assert(bytes_a == bytes_b, "Fallo Bit-Exact Bytes: Los ficheros PCM de A y B deben ser físicamente idénticos (bytes_A == bytes_B).")
		_assert(bytes_a.size() == expected_total_samples * 2, "El tamaño en bytes debe ser exactamente total_samples * 2.")
	else:
		_assert(false, "No se pudieron abrir los ficheros PCM A y B para comparar bytes.")

	# -------------------------------------------------------------------------
	# 2. Ejecución C (Seed distinta 88888 -> Divergencia comprobada A != C)
	# -------------------------------------------------------------------------
	var sim_c = MockSimulationResult.new(88888)
	var res_c = AudioExportBridge.render_and_export_track(sim_c, timeline, profile_id, ProjectSettings.globalize_path(path_c))
	if not res_c.get("success", false):
		failures.append("Exportación C falló: " + str(res_c.get("error", "unknown")))
		return
	
	_assert(res_a["canonical_hash"] != res_c["canonical_hash"], "Fallo Divergencia: Semillas distintas deben producir hashes SHA-256 diferentes.")
	
	var file_c = FileAccess.open(path_c, FileAccess.READ)
	if file_c != null:
		var bytes_c = file_c.get_buffer(file_c.get_length())
		file_c.close()
		file_a = FileAccess.open(path_a, FileAccess.READ)
		var bytes_a = file_a.get_buffer(file_a.get_length())
		file_a.close()
		_assert(bytes_a != bytes_c, "Fallo Divergencia Bytes: Semillas distintas deben producir bytes PCM diferentes (A != C).")
	else:
		_assert(false, "No se pudo abrir el fichero PCM C.")

	# -------------------------------------------------------------------------
	# 3. Pruebas Negativas en Subproceso Aislado (Fail-Closed Operacional)
	# -------------------------------------------------------------------------
	var godot_exe = OS.get_executable_path()
	var project_path = ProjectSettings.globalize_path("res://")
	var output = []
	
	var exit_code_asset = OS.execute(
		godot_exe,
		[
			"--headless",
			"--path",
			project_path,
			"--script",
			"tests/helpers/FailTestUnknownAsset.gd"
		],
		output,
		true,
		false
	)
	_assert(exit_code_asset == 0, "Fail-Closed Fallido: Resolver un asset desconocido debe retornar éxito en el helper (exit 0 al confirmar rechazo vacío). Recibido: " + str(exit_code_asset))
	
	var exit_code_event = OS.execute(
		godot_exe,
		[
			"--headless",
			"--path",
			project_path,
			"--script",
			"tests/helpers/FailTestUnknownEvent.gd"
		],
		output,
		true,
		false
	)
	_assert(exit_code_event == 0, "Fail-Closed Fallido: Resolver un event_id inexistente debe retornar éxito en el helper (exit 0 al confirmar adapter nulo). Recibido: " + str(exit_code_event))

func _conclude() -> void:
	if failures.is_empty():
		print("[C7A04_AUDIO_EXPORT_BRIDGE_SUITE] PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		print("[C7A04_AUDIO_EXPORT_BRIDGE_SUITE] FAIL failures=%d" % failures.size())
		quit(1)

func _initialize() -> void:
	print("[TEST] Running C7A04AudioExportBridgeTest...")
	_run_tests()
	_conclude()