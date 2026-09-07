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

func _init(root: Node = null, theme_name: String = "default_c6", profile: PresentationProfile = null):
	self.root_control = root
	self.theme_name = theme_name
	
	safe_area = SafeAreaLayout.new()
	if root_control != null:
		root_control.add_child(safe_area)
	
	var vbox = VBoxContainer.new()
	vbox.set_anchors_preset(Control.PRESET_FULL_RECT)
	safe_area.add_child(vbox)
	
	var top_hbox = HBoxContainer.new()
	top_hbox.alignment = BoxContainer.ALIGNMENT_END
	vbox.add_child(top_hbox)
	
	badge_label = TypographyLabel.new()
	badge_label.role = TypographyLabel.Role.BADGE
	top_hbox.add_child(badge_label)
	
	hook_label = HookComponent.new()
	vbox.add_child(hook_label)
	
	gameplay_envelope = Control.new()
	gameplay_envelope.size_flags_vertical = Control.SIZE_EXPAND_FILL
	gameplay_envelope.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	vbox.add_child(gameplay_envelope)
	
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
	
	cta = CTAComponent.new()
	cta.visible = false
	vbox.add_child(cta)
	
	reveal_manager = RevealManager.new()
	reveal_manager.winning_label = winning_label
	if root_control != null:
		root_control.add_child(reveal_manager)

	winning_highlight = WinningHighlightComponent.new(root_control as Control)
	if winning_highlight != null:
		winning_highlight.hide()

	if profile != null:
		apply_profile(profile)

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
		if font != null:
			cta.label_main.apply_font(font)
			cta.label_sub.apply_font(font)
			
	if countdown != null and profile != null:
		countdown.apply_profile(profile)
		if font != null: countdown.apply_font(font)

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
			cta.configure(
				render_model.get("cta_main", ""),
				render_model.get("cta_sub", ""),
				current_profile
			)
	else:
		if cta != null:
			cta.visible = false