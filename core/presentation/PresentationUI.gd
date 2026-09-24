# res://core/presentation/PresentationUI.gd
class_name PresentationUI
extends RefCounted

var root_control: Node
var safe_area: SafeAreaLayout
var badge_label: TypographyLabel
var hook_label: HookComponent
var winning_label: TypographyLabel
var cta: CTAComponent
var countdown: CountdownComponent
var reveal_manager: RevealManager
var winning_highlight: WinningHighlightComponent
var current_profile: PresentationProfile
var theme_name: String

var gameplay_envelope: Control 
var mechanic_node: Node2D
var use_c11c_shared_social_editorial: bool = false
var c11c_shared_footer_region: Control = null
const C11CVisualTypographyClass = preload("res://core/presentation/C11CVisualTypography.gd")

func _init(root: Node = null, theme_name: String = "default_c6", profile: PresentationProfile = null, use_shared_social_editorial: bool = false):
	self.root_control = root
	self.theme_name = theme_name
	self.use_c11c_shared_social_editorial = use_shared_social_editorial

	var unified_frame: UnifiedSocialFrame = null
	if root_control != null and root_control is UnifiedSocialFrame:
		unified_frame = root_control as UnifiedSocialFrame

	if unified_frame != null:
		# UnifiedSocialFrame owns the structural geometry. Avoid creating an
		# unattached SafeAreaLayout for this path.
		safe_area = null
		_build_unified_frame_ui(unified_frame)
	else:
		# Preserve the legacy SafeAreaLayout path for non-unified callers.
		safe_area = SafeAreaLayout.new()
		_build_legacy_ui()

	if profile != null:
		apply_profile(profile)

func _build_legacy_ui() -> void:
	if root_control != null:
		root_control.add_child(safe_area)
	var vbox := VBoxContainer.new()
	vbox.set_anchors_preset(Control.PRESET_FULL_RECT)
	safe_area.add_child(vbox)
	_build_header_ui(vbox)
	_build_body_ui(vbox)
	_build_footer_ui(vbox)
	if reveal_manager != null and root_control != null:
		root_control.add_child(reveal_manager)

func _build_unified_frame_ui(frame: UnifiedSocialFrame) -> void:
	var header_root := frame.get_header_content_root()
	var body_root := frame.get_body_ui_root()
	var footer_root := frame.get_footer_content_root()

	if use_c11c_shared_social_editorial:
		c11c_shared_footer_region = footer_root.get_parent() as Control

	if not use_c11c_shared_social_editorial:
		var header_box := VBoxContainer.new()
		header_box.set_anchors_preset(Control.PRESET_FULL_RECT)
		header_root.add_child(header_box)
		_build_header_ui(header_box)

	# C11-C Visual Drill CTA lives in the HEADER. It reuses the same shared
	# CTAComponent used by Challenge; no second CTA implementation exists.
	if use_c11c_shared_social_editorial:
		cta = CTAComponent.new()
		cta.name = "VisualDrillEndCTA"
		cta.visible = false
		cta.set_anchors_preset(Control.PRESET_FULL_RECT)
		cta.offset_left = 24.0
		cta.offset_top = 12.0
		cta.offset_right = -24.0
		cta.offset_bottom = -12.0
		cta.z_index = 50
		header_root.add_child(cta)

	gameplay_envelope = Control.new()
	gameplay_envelope.set_anchors_preset(Control.PRESET_FULL_RECT)
	gameplay_envelope.mouse_filter = Control.MOUSE_FILTER_IGNORE
	body_root.add_child(gameplay_envelope)
	_build_body_children(true)

	var footer_box := Control.new()
	footer_box.set_anchors_preset(Control.PRESET_FULL_RECT)
	footer_box.mouse_filter = Control.MOUSE_FILTER_IGNORE
	footer_root.add_child(footer_box)
	_build_footer_children(footer_box)

func _build_header_ui(parent: Control) -> void:
	var top_hbox := HBoxContainer.new()
	top_hbox.alignment = BoxContainer.ALIGNMENT_END
	parent.add_child(top_hbox)

	badge_label = TypographyLabel.new()
	badge_label.role = TypographyLabel.Role.BADGE
	top_hbox.add_child(badge_label)

	hook_label = HookComponent.new()
	parent.add_child(hook_label)

func _build_body_ui(parent: Control) -> void:
	gameplay_envelope = Control.new()
	gameplay_envelope.size_flags_vertical = Control.SIZE_EXPAND_FILL
	gameplay_envelope.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	parent.add_child(gameplay_envelope)
	_build_body_children()

func _build_body_children(reveal_in_body: bool = false) -> void:
	countdown = CountdownComponent.new()
	gameplay_envelope.add_child(countdown)

	winning_label = TypographyLabel.new()
	winning_label.role = TypographyLabel.Role.HEADLINE
	winning_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	winning_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	winning_label.set_anchors_preset(Control.PRESET_CENTER)
	winning_label.grow_horizontal = Control.GROW_DIRECTION_BOTH
	winning_label.grow_vertical = Control.GROW_DIRECTION_END
	winning_label.visible = false
	gameplay_envelope.add_child(winning_label)

	reveal_manager = RevealManager.new()
	reveal_manager.winning_label = winning_label
	if reveal_in_body:
		gameplay_envelope.add_child(reveal_manager)

func _build_footer_ui(parent: Control) -> void:
	_build_footer_children(parent)

func _build_footer_children(parent: Control) -> void:
	# C11-C Visual Drill CTA is mounted in the HEADER on the shared social path.
	# Preserve the historical Challenge CTA in the legacy footer path.
	if not use_c11c_shared_social_editorial:
		cta = CTAComponent.new()
		cta.visible = false
		parent.add_child(cta)

	winning_highlight = WinningHighlightComponent.new(root_control as Control if root_control is Control else null)
	if winning_highlight != null:
		winning_highlight.hide()

func apply_profile(profile: PresentationProfile):
	self.current_profile = profile
	if safe_area != null:
		safe_area.apply_profile(profile)
		
	var font: Font = null
	if ResourceLoader.exists("res://core/presentation/PresentationTheme.gd"):
		var theme_script = load("res://core/presentation/PresentationTheme.gd")
		if theme_script and theme_script.has_method("get_theme_config"):
			var cfg = theme_script.get_theme_config(theme_name)
			font = cfg.get("font", null)
	
	if badge_label != null:
		badge_label.apply_profile(profile)
		if font != null: badge_label.apply_font(font)
		
	if hook_label != null and profile != null:
		hook_label.apply_profile(profile)
		if font != null: hook_label.apply_font(font)
		
	if winning_label != null:
		winning_label.apply_profile(profile)
		if font != null: winning_label.apply_font(font)
		
	if cta != null:
		cta.label_main.apply_profile(profile)
		cta.label_sub.apply_profile(profile)
		if use_c11c_shared_social_editorial:
			C11CVisualTypographyClass.apply_to_typography_label(cta.label_main)
			C11CVisualTypographyClass.apply_to_typography_label(cta.label_sub)
		elif font != null:
			cta.label_main.apply_font(font)
			cta.label_sub.apply_font(font)
			
	if countdown != null and profile != null:
		countdown.apply_profile(profile)
		if use_c11c_shared_social_editorial:
			var c11c_countdown_font: Font = C11CVisualTypographyClass.get_font()
			if c11c_countdown_font != null:
				countdown.apply_font(c11c_countdown_font)
		elif font != null:
			countdown.apply_font(font)

func setup_mechanic_canvas(mechanic_root: Node2D):
	self.mechanic_node = mechanic_root
	if reveal_manager != null:
		reveal_manager.mechanics_canvas = mechanic_root

## Única interfaz de la UI: Consumidor puro del RenderModel
func apply_render_model(render_model: Dictionary) -> void:
	if mechanic_node != null and gameplay_envelope != null:
		if gameplay_envelope.size.x > 0:
			var center_pos = gameplay_envelope.global_position + (gameplay_envelope.size / 2.0)
			mechanic_node.global_position = center_pos

	if badge_label != null:
		badge_label.visible = render_model.get("show_badge", false)
		var b_text = render_model.get("badge_text", "")
		if not b_text.is_empty():
			badge_label.text = b_text

	if hook_label != null:
		hook_label.apply_render_model(render_model)

	if countdown != null:
		countdown.apply_render_model(render_model)

	if c11c_shared_footer_region != null and use_c11c_shared_social_editorial:
		var presentation_phase: String = str(render_model.get("presentation_phase", "GAME"))
		c11c_shared_footer_region.visible = presentation_phase != "END_CTA"

	if reveal_manager != null:
		reveal_manager.process_render_model(render_model)

	if winning_highlight != null:
		winning_highlight.hide()
		if render_model.get("is_success_game", false):
			winning_highlight.show_for_rects(render_model.get("success_highlight_rects", []))

	if cta != null and current_profile != null:
		var cta_vis = render_model.get("cta_visible", false)
		cta.visible = cta_vis
		if cta_vis:
			var cta_colors_variant: Variant = render_model.get("cta_colors", {})
			var cta_colors: Dictionary = cta_colors_variant if cta_colors_variant is Dictionary else {}
			cta.configure(
				str(render_model.get("cta_main", "")),
				str(render_model.get("cta_sub", "")),
				current_profile,
				cta_colors
			)
			if bool(render_model.get("cta_animated", false)):
				cta.apply_presentation_motion(float(render_model.get("cta_progress", 1.0)))
			else:
				cta.reset_presentation_motion()
	else:
		if cta != null:
			cta.visible = false
			cta.reset_presentation_motion()
