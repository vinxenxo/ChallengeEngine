# tests/C7A504AudioVisualFFprobeValidationTest.gd
extends SceneTree

var failures: Array[String] = []

func _init() -> void:
	print("[C7-A5.4] Iniciando validación física con ffprobe e integridad A/V del corpus...")
	_run_validation()
	_conclude()

func _assert(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)
		print("[FAIL] " + message)
	else:
		print("[PASS] " + message)

func _run_validation() -> void:
	var manifest_path = "res://artifacts/production/audiovisual/audio_corpus_manifest.json"
	_assert(FileAccess.file_exists(manifest_path), "El manifiesto C7-A5.1 debe existir.")
	if not FileAccess.file_exists(manifest_path):
		return

	var file = FileAccess.open(manifest_path, FileAccess.READ)
	var manifest = JSON.parse_string(file.get_as_text())
	file.close()

	var artifacts: Dictionary = manifest.get("artifacts", {})

	for ch_id in artifacts.keys():
		var mp4_rel = "res://artifacts/production/audiovisual/" + ch_id + ".mp4"
		var mp4_abs = ProjectSettings.globalize_path(mp4_rel)

		_assert(FileAccess.file_exists(mp4_rel), "[" + ch_id + "] Contenedor MP4 presente en disco.")

		var ffprobe_args = [
			"-v", "error",
			"-select_streams", "a:0",
			"-show_entries", "stream=codec_name,sample_rate,channels",
			"-of", "default=noprint_wrappers=1",
			mp4_abs
		]

		var output = []
		var exit_code = OS.execute("ffprobe", ffprobe_args, output, true)

		_assert(exit_code == 0, "[" + ch_id + "] ffprobe ejecutado correctamente para audio.")
		
		var stdout = ""
		if output.size() > 0:
			stdout = output[0]

		_assert(stdout.contains("codec_name=aac"), "[" + ch_id + "] Codec de audio verificado (aac).")
		_assert(stdout.contains("sample_rate=44100"), "[" + ch_id + "] Sample rate verificado (44100Hz).")
		_assert(stdout.contains("channels=1"), "[" + ch_id + "] Canales verificados (mono/1).")

		print("[C7-A5.4] Validación FFprobe OK: ", ch_id)

func _conclude() -> void:
	if failures.is_empty():
		print("[C7-A5.4-TEST] RESULTADO GLOBAL: PASS")
		quit(0)
	else:
		for f in failures:
			push_error(f)
		print("[C7-A5.4-TEST] RESULTADO GLOBAL: FAIL failures=%d" % failures.size())
		quit(1)