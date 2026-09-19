# tests/C7A08AudioVisualCorpusExportTest.gd
extends SceneTree

const AudioExportBridge = preload(
	"res://core/audio/AudioExportBridge.gd"
)

var failures: Array[String] = []


func _assert(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)
		print("[FAIL] " + message)
	else:
		print("[PASS] " + message)


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
	print(
		"[C7A08-TEST] Iniciando exportación física "
		+ "del corpus multiperfil (C7-A4.5.3)..."
	)
	_run_tests()
	_conclude()


func _run_tests() -> void:
	var fixtures = [
		{
			"id": "CHALLENGE_001",
			"profile": "c7_profile_tone_only"
		},
		{
			"id": "CHALLENGE_002",
			"profile": "c7_profile_noise_only"
		},
		{
			"id": "CHALLENGE_003",
			"profile": "c7_profile_mixed_alt"
		},
		{
			"id": "CHALLENGE_004",
			"profile": "c7_profile_mixed_overlap"
		},
		{
			"id": "CHALLENGE_005",
			"profile": "c7_profile_multi_noise"
		}
	]

	var timeline := MockVideoTimeline.new()

	var expected_total_samples: int = (
		timeline.get_total_frames() * 735
	)

	for fixture in fixtures:
		_run_fixture(
			fixture["id"],
			fixture["profile"],
			timeline,
			expected_total_samples
	)


func _run_fixture(
	challenge_id: String,
	profile_id: String,
	timeline: VideoTimeline,
	expected_total_samples: int
) -> void:
	var json_path := (
		"res://tests/fixtures/c7/challenges/"
		+ challenge_id
		+ ".json"
	)

	var file := FileAccess.open(json_path, FileAccess.READ)

	if file == null:
		_assert(
			false,
			"[" + challenge_id + "] No se pudo abrir el JSON."
		)
		return

	var json_data = JSON.parse_string(file.get_as_text())
	file.close()

	if typeof(json_data) != TYPE_DICTIONARY:
		_assert(
			false,
			"[" + challenge_id + "] JSON inválido."
		)
		return

	var generation_cfg: Dictionary = (
		json_data.get("generation", {})
	)

	var seed: int = int(
		generation_cfg.get("seed", 0)
	)

	_assert(
		seed != 0,
		"[" + challenge_id + "] generation.seed válido."
	)

	var sim_result := MockSimulationResult.new(seed)

	var output_a := ProjectSettings.globalize_path(
		"user://c7a08_" + challenge_id + "_a.pcm"
	)

	var output_b := ProjectSettings.globalize_path(
		"user://c7a08_" + challenge_id + "_b.pcm"
	)

	# =========================================================
	# A — Render principal
	# =========================================================

	var result_a := AudioExportBridge.render_and_export_track(
		sim_result,
		timeline,
		profile_id,
		output_a
	)

	_assert(
		result_a.get("success", false) == true,
		"[" + challenge_id + "] Exportación A correcta."
	)

	if not result_a.get("success", false):
		return

	_assert(
		result_a.get("sample_rate", 0) == 44100,
		"[" + challenge_id + "] sample_rate=44100."
	)

	_assert(
		result_a.get("channels", 0) == 1,
		"[" + challenge_id + "] channels=1."
	)

	_assert(
		result_a.get("format", "") == "s16le",
		"[" + challenge_id + "] format=s16le."
	)

	_assert(
		result_a.get("total_samples", 0)
		== expected_total_samples,
		"[" + challenge_id
		+ "] total_samples coincide con timeline."
	)

	_assert(
		result_a.has("canonical_hash")
		and str(result_a["canonical_hash"]).length() == 64,
		"[" + challenge_id + "] SHA-256 válido."
	)

	_assert(
		FileAccess.file_exists(output_a),
		"[" + challenge_id + "] PCM físico existe."
	)

	if not FileAccess.file_exists(output_a):
		return

	var file_a := FileAccess.open(output_a, FileAccess.READ)

	if file_a == null:
		_assert(
			false,
			"[" + challenge_id + "] No se pudo abrir PCM A."
		)
		return

	var bytes_a := file_a.get_buffer(file_a.get_length())
	file_a.close()

	_assert(
		bytes_a.size() == expected_total_samples * 2,
		"[" + challenge_id
		+ "] tamaño PCM = total_samples * 2."
	)

	# =========================================================
	# B — Misma seed => bit-exact
	# =========================================================

	var sim_result_b := MockSimulationResult.new(seed)

	var result_b := AudioExportBridge.render_and_export_track(
		sim_result_b,
		timeline,
		profile_id,
		output_b
	)

	_assert(
		result_b.get("success", false) == true,
		"[" + challenge_id + "] Exportación B correcta."
	)

	if not result_b.get("success", false):
		return

	_assert(
		result_a["canonical_hash"]
		== result_b["canonical_hash"],
		"[" + challenge_id
		+ "] misma seed => mismo SHA-256."
	)

	var file_b := FileAccess.open(output_b, FileAccess.READ)

	if file_b == null:
		_assert(
			false,
			"[" + challenge_id + "] No se pudo abrir PCM B."
		)
		return

	var bytes_b := file_b.get_buffer(file_b.get_length())
	file_b.close()

	_assert(
		bytes_a == bytes_b,
		"[" + challenge_id
		+ "] misma seed => PCM byte-exact."
	)

	print(
		"[C7A08] ",
		challenge_id,
		" ",
		profile_id.lpad(28, " "),
		" PASS"
	)


func _conclude() -> void:
	if failures.is_empty():
		print("[C7A08-TEST] RESULTADO GLOBAL: PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)

		print(
			"[C7A08-TEST] RESULTADO GLOBAL: FAIL failures=%d"
			% failures.size()
		)

		quit(1)


func _initialize() -> void:
	pass