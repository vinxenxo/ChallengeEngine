extends "res://GeneradorMaestro.gd"

## C11-E E2 Challenge-only editorial presentation extension.
## It inherits and executes the frozen C runtime, then mounts one E-owned title
## label in UnifiedSocialFrame.HeaderRegion. It never edits C simulation/config
## truth and never maps title to hook, CTA, telemetry or result data.

const TypographyLabelScript = preload("res://core/presentation/components/TypographyLabel.gd")
const C11CVisualTypographyScript = preload("res://core/presentation/C11CVisualTypography.gd")
const C11EE2SidecarValidatorScript = preload("res://tools/c11e/e2/C11EE2SidecarValidator.gd")
const ExpectedManifestSha256 := "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
const ExpectedChallengeSha256 := "ec8925fa5b4ab996a791c8cf7f5b139470774720f57880c5b01b2d0aa5b57bea"

var _c11e_sidecar: Dictionary = {}
var _c11e_title_label: TypographyLabel

func _ready() -> void:
	var sidecar_path := _get_c11e_user_arg("--c11e-editorial-sidecar=")
	var expected_sidecar_sha := _get_c11e_user_arg("--c11e-editorial-sha256=")
	var expected_config_sha := _get_c11e_user_arg("--c11e-config-sha256=")
	if sidecar_path.is_empty() or expected_sidecar_sha.length() != 64 or expected_config_sha.length() != 64:
		push_error("[C11E_E2] Required sidecar/config identity arguments are missing.")
		get_tree().quit(31)
		return
	if not FileAccess.file_exists(sidecar_path):
		push_error("[C11E_E2] Editorial sidecar is missing: " + sidecar_path)
		get_tree().quit(32)
		return
	if FileAccess.get_sha256(sidecar_path) != expected_sidecar_sha:
		push_error("[C11E_E2] Editorial sidecar SHA-256 mismatch.")
		get_tree().quit(33)
		return
	if FileAccess.get_sha256("res://release/C11C_FREEZE_PACKAGE_MANIFEST.json") != ExpectedManifestSha256:
		push_error("[C11E_E2] Frozen C11-C manifest identity mismatch.")
		get_tree().quit(34)
		return
	if FileAccess.get_sha256("res://challenges/CHALLENGE_001.json") != ExpectedChallengeSha256:
		push_error("[C11E_E2] Frozen CHALLENGE_001 source identity mismatch.")
		get_tree().quit(35)
		return
	if not FileAccess.file_exists(_get_c11e_config_path()):
		push_error("[C11E_E2] Effective challenge config file is missing.")
		get_tree().quit(36)
		return
	if FileAccess.get_sha256(_get_c11e_config_path()) != expected_config_sha:
		push_error("[C11E_E2] Effective challenge config SHA-256 mismatch.")
		get_tree().quit(37)
		return

	var sidecar_file := FileAccess.open(sidecar_path, FileAccess.READ)
	if sidecar_file == null:
		push_error("[C11E_E2] Cannot open editorial sidecar.")
		get_tree().quit(38)
		return
	var parsed: Variant = JSON.parse_string(sidecar_file.get_as_text())
	sidecar_file.close()
	if not (parsed is Dictionary):
		push_error("[C11E_E2] Editorial sidecar must be a JSON object.")
		get_tree().quit(39)
		return
	_c11e_sidecar = parsed
	if not _validate_c11e_sidecar(_c11e_sidecar):
		push_error("[C11E_E2] Editorial sidecar contract validation failed.")
		get_tree().quit(40)
		return

	# Call the C runtime unchanged. The inherited _process continues to own every
	# frame, timeline transition, simulation snapshot and C presentation update.
	super._ready()
	if presentation_ui == null or presentation_profile == null:
		push_error("[C11E_E2] C Challenge runtime did not initialize its presentation context.")
		get_tree().quit(41)
		return
	if str(config_cache.get("challenge_id", "")) != "CHALLENGE_001":
		push_error("[C11E_E2] Active C config is not CHALLENGE_001.")
		get_tree().quit(42)
		return
	var generation: Dictionary = config_cache.get("generation", {})
	var expected_seed := int(_c11e_sidecar.get("seed_domains", {}).get("gameplay", {}).get("value", -1))
	if int(generation.get("seed", -2)) != expected_seed:
		push_error("[C11E_E2] C gameplay seed does not match the E2 sidecar.")
		get_tree().quit(43)
		return
	_mount_c11e_title()

func _get_c11e_user_arg(prefix: String) -> String:
	for arg: String in OS.get_cmdline_user_args():
		if arg.begins_with(prefix):
			return arg.substr(prefix.length())
	return ""

func _get_c11e_config_path() -> String:
	return _get_c11e_user_arg("--config=")

static func is_positive_integral_seed(value: Variant) -> bool:
	return C11EE2SidecarValidatorScript.is_positive_integral_seed(value)

func _validate_c11e_sidecar(sidecar: Dictionary) -> bool:
	return C11EE2SidecarValidatorScript.validate(sidecar)

func _mount_c11e_title() -> void:
	var frame := presentation_ui_root as UnifiedSocialFrame
	if frame == null:
		push_error("[C11E_E2] UnifiedSocialFrame is unavailable.")
		get_tree().quit(44)
		return
	var header_root := frame.get_header_content_root()
	if header_root == null:
		push_error("[C11E_E2] HeaderContent mount point is unavailable.")
		get_tree().quit(45)
		return
	_c11e_title_label = TypographyLabelScript.new() as TypographyLabel
	_c11e_title_label.name = "C11EEditorialTitle"
	_c11e_title_label.role = TypographyLabel.Role.HEADLINE
	_c11e_title_label.set_anchors_preset(Control.PRESET_FULL_RECT)
	_c11e_title_label.offset_left = 24.0
	_c11e_title_label.offset_top = 24.0
	_c11e_title_label.offset_right = -20.0
	_c11e_title_label.offset_bottom = -16.0
	_c11e_title_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_c11e_title_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_c11e_title_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_c11e_title_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_c11e_title_label.z_index = 100
	_c11e_title_label.visible = true
	_c11e_title_label.text = str(_c11e_sidecar["editorial"]["title"])
	_c11e_title_label.apply_profile(presentation_profile)
	C11CVisualTypographyScript.apply_header_to_typography_label(_c11e_title_label)
	_c11e_title_label.add_theme_color_override("font_color", Color.WHITE)
	_c11e_title_label.add_theme_color_override("font_outline_color", Color(0.0, 0.0, 0.0, 0.92))
	_c11e_title_label.add_theme_constant_override("outline_size", 4)
	header_root.add_child(_c11e_title_label)
	_c11e_title_label.move_to_front()
	print("[C11E_E2] TITLE_SLOT=header.editorial_title TITLE_SHA256=" + _sha256_text(_c11e_title_label.text))
	print("[C11E_E2] GAMEPLAY_SEED=" + str(int(_c11e_sidecar["seed_domains"]["gameplay"]["value"])))

func _sha256_text(value: String) -> String:
	var context := HashingContext.new()
	context.start(HashingContext.HASH_SHA256)
	context.update(value.to_utf8_buffer())
	return context.finish().hex_encode()
