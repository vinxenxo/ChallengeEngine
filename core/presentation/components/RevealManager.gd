extends Node
class_name RevealManager

var mechanics_canvas: CanvasItem 
var winning_label: TypographyLabel

func process_frame(absolute_frame: int, winning_frame: int, timeline: VideoTimeline, state: String):
	if mechanics_canvas == null:
		return
		
	# Énfasis visual y texto de éxito en el winning_frame absoluto exacto dentro de la fase GAME
	if absolute_frame == winning_frame and state == "GAME":
		mechanics_canvas.modulate = Color(1.2, 1.2, 0.8, 1.0)
		mechanics_canvas.scale = Vector2(1.05, 1.05)
		if winning_label != null:
			winning_label.visible = true
			winning_label.text = "🎯 ¡LO HAS CLAVADO!"
		
	var phase = str(timeline.get_phase_at_frame(absolute_frame)).to_upper()
	
	# Fase REVEAL: Transición visual de cierre
	if phase == "REVEAL":
		if winning_label != null and absolute_frame > winning_frame + 60:
			winning_label.visible = false
			
		var phase_start = 0
		if timeline.has_method("get_phase_start_frame"):
			phase_start = timeline.get_phase_start_frame("REVEAL")
			
		var duration = 0
		if "durations" in timeline and timeline.durations is Dictionary:
			duration = timeline.durations.get("REVEAL", 0)
			
		if duration > 0:
			var progress = float(absolute_frame - phase_start) / float(duration)
			mechanics_canvas.modulate = mechanics_canvas.modulate.lerp(Color(1.0, 1.0, 1.0, 0.3), progress * 0.1)
			mechanics_canvas.scale = mechanics_canvas.scale.lerp(Vector2(1.0, 1.0), progress * 0.2)