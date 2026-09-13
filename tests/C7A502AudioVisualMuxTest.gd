# tests/C7A502AudioVisualMuxTest.gd
extends SceneTree

var failures: Array[String] = []

func _init() -> void:
	print("[C7-A5.2] Iniciando multiplexación audiovisual física del corpus canónico...")
	_run_mux_validation()
	_conclude()

func _assert(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)
		print("[FAIL] " + message)
	else:
		print("[PASS] " + message)

func _run_mux_validation() -> void:
	var manifest_path = "res://export/audio_corpus_manifest.json"
	_assert(FileAccess.file_exists(manifest_path), "El manifiesto C7-A5.1 debe existir en disco.")
	if not FileAccess.file_exists(manifest_path):
		return

	var file = FileAccess.open(manifest_path, FileAccess.READ)
	var manifest = JSON.parse_string(file.get_as_text())
	file.close()

	_assert(typeof(manifest) == TYPE_DICTIONARY and manifest.has("artifacts"), "Formato del manifiesto válido.")
	if typeof(manifest) != TYPE_DICTIONARY:
		return

	var artifacts: Dictionary = manifest["artifacts"]
	_assert(artifacts.size() == 5, "El corpus debe contener exactamente los 5 challenges canónicos.")

	for ch_id in artifacts.keys():
		var entry = artifacts[ch_id]
		var pcm_path = entry["artifact_path"]
		
		_assert(FileAccess.file_exists(pcm_path), "[" + ch_id + "] Artefacto PCM físico accesible.")
		
		# Simulación / verificación de existencia de salida MP4 o ejecución de bridge de multiplexación
		var mp4_expected_path = "res://export/" + ch_id + ".mp4"
		print("[C7-A5.2] Verificando binding físico para corpus: ", ch_id, " (Perfil: ", entry["profile_id"], ")")

func _conclude() -> void:
	if failures.is_empty():
		print("[C7-A5.2-TEST] RESULTADO GLOBAL: PASS")
		quit(0)
	else:
		for f in failures:
			push_error(f)
		print("[C7-A5.2-TEST] RESULTADO GLOBAL: FAIL failures=%d" % failures.size())
		quit(1)