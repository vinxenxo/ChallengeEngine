# res://tests/C9CBatchAuthoringGenerator.gd
extends SceneTree

const ChallengeAuthoringRequest = preload("res://core/authoring/ChallengeAuthoringRequest.gd")
const ChallengeGenerator = preload("res://core/authoring/ChallengeGenerator.gd")
const ChallengeMigrationAdapter = preload("res://core/authoring/ChallengeMigrationAdapter.gd")
const ChallengeRuntimeBridge = preload("res://core/execution/ChallengeRuntimeBridge.gd")
const Schema = preload("res://core/validation/C6FChallengeSchemaValidator.gd")
const SimulationMetricsResolver = preload("res://core/simulation/SimulationMetricsResolver.gd")

func _initialize() -> void:
	print("[TEST] Running C9CBatchAuthoringGenerator...")

	var input_path := _get_arg("--input-batch=")
	var output_dir := _get_arg("--output-dir=")
	if input_path.is_empty() or output_dir.is_empty():
		printerr("FAIL: Faltan argumentos --input-batch= o --output-dir=")
		quit(1)
		return

	if input_path.begins_with("/") or input_path.find(":") >= 0:
		printerr("FAIL: --input-batch debe ser una ruta relativa al proyecto.")
		quit(1)
		return
	if output_dir.begins_with("/") or output_dir.find(":") >= 0 or output_dir.begins_with(".."):
		printerr("FAIL: --output-dir debe ser una ruta relativa al proyecto.")
		quit(1)
		return

	var input_file := FileAccess.open(input_path, FileAccess.READ)
	if input_file == null:
		printerr("FAIL: No se pudo abrir input batch: %s" % input_path)
		quit(1)
		return

	var json := JSON.new()
	var parse_error := json.parse(input_file.get_as_text())
	input_file.close()
	if parse_error != OK or typeof(json.data) != TYPE_ARRAY:
		printerr("FAIL: authoring_batch.json debe contener un Array JSON válido.")
		quit(1)
		return

	var requests: Array = json.data
	if requests.is_empty():
		printerr("FAIL: El lote de authoring está vacío.")
		quit(1)
		return

	if DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(output_dir)) != OK:
		printerr("FAIL: No se pudo crear output-dir: %s" % output_dir)
		quit(1)
		return

	var generated_ids: Dictionary = {}
	var generated_count := 0

	for index in range(requests.size()):
		var req_data = requests[index]
		if typeof(req_data) != TYPE_DICTIONARY:
			printerr("FAIL: Entrada #%d no es Dictionary." % (index + 1))
			quit(1)
			return

		var request_result := ChallengeAuthoringRequest.create_from_dictionary(req_data)
		if not bool(request_result.get("success", false)):
			printerr("FAIL: Request creation failed en entrada #%d: %s" % [index + 1, str(request_result.get("errors", []))])
			quit(1)
			return

		var request: ChallengeAuthoringRequest = request_result.get("request")
		var normative := ChallengeGenerator.generate_normative(request)
		if not bool(normative.get("success", false)):
			printerr("FAIL: Normative generation failed en entrada #%d: %s" % [index + 1, str(normative.get("error", ""))])
			quit(1)
			return

		var canonical: Dictionary = normative.get("challenge", {})
		var schema_result := Schema.validate_v2(canonical)
		if not bool(schema_result.get("is_valid", false)):
			printerr("FAIL: Canonical V2 inválido en entrada #%d: %s" % [index + 1, str(schema_result.get("errors", []))])
			quit(1)
			return

		if canonical.get("mechanic") != str(req_data.get("mechanic", "")):
			printerr("FAIL: mechanic mismatch en entrada #%d." % (index + 1))
			quit(1)
			return
		if int(canonical.get("simulation", {}).get("seed", -1)) != int(req_data.get("seed", -2)):
			printerr("FAIL: seed mismatch en entrada #%d." % (index + 1))
			quit(1)
			return

		var runtime_projection := ChallengeMigrationAdapter.canonical_v2_to_runtime_v1(canonical)
		if typeof(runtime_projection) != TYPE_DICTIONARY or runtime_projection.is_empty():
			printerr("FAIL: canonical_v2_to_runtime_v1 falló en entrada #%d." % (index + 1))
			quit(1)
			return

		var runtime_result := ChallengeRuntimeBridge.run_effective_pipeline(runtime_projection)
		if not bool(runtime_result.get("success", false)):
			printerr("FAIL: runtime equivalence failed en entrada #%d: %s" % [index + 1, str(runtime_result.get("error", ""))])
			quit(1)
			return

		var challenge_id := str(runtime_projection.get("challenge_id", "")).strip_edges()
		if challenge_id.is_empty():
			printerr("FAIL: challenge_id vacío en entrada #%d." % (index + 1))
			quit(1)
			return
		if generated_ids.has(challenge_id):
			printerr("FAIL: challenge_id duplicado '%s'." % challenge_id)
			quit(1)
			return

		var simulation_result = runtime_result.get("simulation_result")
		if simulation_result != null:
			SimulationMetricsResolver.resolve_metrics(simulation_result)

		var output_filename := "CHALLENGE_%s.json" % challenge_id
		var output_path := output_dir.path_join(output_filename)
		var output_file := FileAccess.open(output_path, FileAccess.WRITE)
		if output_file == null:
			printerr("FAIL: No se pudo escribir %s" % output_path)
			quit(1)
			return
		output_file.store_string(JSON.stringify(runtime_projection, "  "))
		output_file.close()

		generated_ids[challenge_id] = true
		generated_count += 1
		print("  -> Generado %s" % challenge_id)

	if generated_count != requests.size():
		printerr("FAIL: generated_count=%d requests=%d." % [generated_count, requests.size()])
		quit(1)
		return

	print("[C9-C] BATCH AUTHORING GENERATION: PASS (%d generados)" % generated_count)
	print("[C9-C] GENERATED_COUNT=%d" % generated_count)
	quit(0)

func _get_arg(prefix: String) -> String:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with(prefix):
			return arg.trim_prefix(prefix).strip_edges()
	return ""
