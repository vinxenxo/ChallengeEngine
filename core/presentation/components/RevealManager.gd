extends Node
class_name RevealManager

var mechanics_canvas: CanvasItem 
var winning_label: TypographyLabel

## E2-Hardening: Purificado de strings mágicos y acoplamientos temporales
func process_render_model(render_model: Dictionary) -> void:
	if mechanics_canvas == null:
		return
		
	if render_model.get("success_visible", false):
		mechanics_canvas.modulate = Color(1.2, 1.2, 0.8, 1.0)
		mechanics_canvas.scale = Vector2(1.05, 1.05)
		if winning_label != null:
			winning_label.visible = true
			winning_label.text = render_model.get("success_text", "")
		
	if render_model.get("reveal_visible", false):
		if winning_label != null and render_model.get("hide_success_text", false):
			winning_label.visible = false
			
		var progress: float = render_model.get("reveal_progress", 0.0)
		mechanics_canvas.modulate = mechanics_canvas.modulate.lerp(Color(1.0, 1.0, 1.0, 0.3), progress * 0.1)
		mechanics_canvas.scale = mechanics_canvas.scale.lerp(Vector2(1.0, 1.0), progress * 0.2)