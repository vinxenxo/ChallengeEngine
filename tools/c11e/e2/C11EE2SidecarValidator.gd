extends RefCounted

const EXPECTED_MANIFEST_SHA256 := "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
const EXPECTED_CHALLENGE_SHA256 := "ec8925fa5b4ab996a791c8cf7f5b139470774720f57880c5b01b2d0aa5b57bea"
const MAX_SEED := 2147483646

static func is_positive_integral_seed(value: Variant) -> bool:
	var value_type := typeof(value)
	if value_type != TYPE_INT and value_type != TYPE_FLOAT:
		return false
	var numeric_value := float(value)
	if is_nan(numeric_value) or is_inf(numeric_value):
		return false
	if numeric_value < 1.0 or numeric_value > float(MAX_SEED):
		return false
	return numeric_value == floor(numeric_value)

static func _is_exact_integer(value: Variant, expected: int) -> bool:
	var value_type := typeof(value)
	if value_type != TYPE_INT and value_type != TYPE_FLOAT:
		return false
	var numeric_value := float(value)
	if is_nan(numeric_value) or is_inf(numeric_value):
		return false
	return numeric_value == float(expected)

static func _dictionary(value: Variant) -> Dictionary:
	if typeof(value) == TYPE_DICTIONARY:
		var dictionary_value: Dictionary = value
		return dictionary_value
	return {}

static func validate(sidecar_value: Variant) -> bool:
	if typeof(sidecar_value) != TYPE_DICTIONARY:
		return false
	var sidecar: Dictionary = sidecar_value
	if sidecar.get("schema") != "C11E-CHALLENGE-EDITORIAL-SIDECAR-V1":
		return false
	if sidecar.get("schema_version") != "1.0":
		return false
	if sidecar.get("content_type") != "challenges" or sidecar.get("challenge_id") != "CHALLENGE_001":
		return false

	var editorial: Dictionary = _dictionary(sidecar.get("editorial"))
	var title_value: Variant = editorial.get("title")
	if typeof(title_value) != TYPE_STRING:
		return false
	var title: String = str(title_value).strip_edges()
	if title.is_empty() or title == "UNKNOWN" or title.length() > 160:
		return false
	for index in range(title.length()):
		if title.unicode_at(index) < 32:
			return false

	var visual: Dictionary = _dictionary(sidecar.get("visual_target"))
	if visual.get("slot_id") != "header.editorial_title" or visual.get("region") != "HEADER":
		return false
	if visual.get("semantic_separation") != "TITLE_IS_NOT_HOOK_CTA_OR_GAMEPLAY":
		return false
	if visual.get("visibility") != "ALL_CHALLENGE_FRAMES":
		return false
	var bounds: Dictionary = _dictionary(visual.get("bounds_logical_540x960"))
	if not _is_exact_integer(bounds.get("x"), 24):
		return false
	if not _is_exact_integer(bounds.get("y"), 24):
		return false
	if not _is_exact_integer(bounds.get("width"), 496):
		return false
	if not _is_exact_integer(bounds.get("height"), 104):
		return false

	var boundary: Dictionary = _dictionary(sidecar.get("execution_boundary"))
	if boundary.get("renderer_input_is_e2_test_only") != true:
		return false
	if boundary.get("release_authority") != "NONE" or boundary.get("baseline_promotion") != false:
		return false
	if boundary.get("audio_enabled") != false:
		return false

	var source: Dictionary = _dictionary(sidecar.get("source_identity"))
	if source.get("c11c_manifest_sha256") != EXPECTED_MANIFEST_SHA256:
		return false
	if source.get("challenge_source_sha256") != EXPECTED_CHALLENGE_SHA256:
		return false

	var seeds: Dictionary = _dictionary(sidecar.get("seed_domains"))
	if seeds.get("independent_domains") != true:
		return false
	var gameplay: Dictionary = _dictionary(seeds.get("gameplay"))
	var music: Dictionary = _dictionary(seeds.get("music"))
	if gameplay.get("field") != "request.seed":
		return false
	if music.get("field") != "request.music_seed":
		return false
	if not is_positive_integral_seed(gameplay.get("value")):
		return false
	if not is_positive_integral_seed(music.get("value")):
		return false
	return true
