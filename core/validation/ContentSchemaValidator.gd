class_name ContentSchemaValidator
extends RefCounted

## C6-F0.3 — Unified Content Schema and Invariant Validator.
## Enforces document-level additionalProperties: false, strict schema parity, nested structural checks, numeric ranges, enums, and cross-field temporals.

static func validate_document(doc: Dictionary) -> Dictionary:
	var errors: Array[String] = []
	
	if not doc is Dictionary:
		return {"is_valid": false, "errors": ["Document is not a Dictionary."]}
		
	for top_key in doc.keys():
		if not top_key in ["envelope", "payload"]:
			errors.append("Document contains disallowed top-level property: '%s'." % str(top_key))
			
	if not doc.has("envelope") or not doc["envelope"] is Dictionary:
		errors.append("Missing mandatory top-level 'envelope' block.")
	if not doc.has("payload") or not doc["payload"] is Dictionary:
		errors.append("Missing mandatory top-level 'payload' block.")
		
	if not errors.is_empty():
		return {"is_valid": false, "errors": errors}
		
	var env_res = ContentEnvelope.create_from_dictionary(doc["envelope"])
	if not bool(env_res.get("success", false)):
		for err in env_res.get("errors", []):
			errors.append("Envelope validation failed: " + str(err))
		return {"is_valid": false, "errors": errors}
		
	var env: ContentEnvelope = env_res["envelope"]
	var payload: Dictionary = doc["payload"]
	
	# Kind Dispatch & Payload Structural Routing
	match env.kind:
		"visual_loop":
			var loop_res = _validate_visual_loop_payload(payload)
			if not loop_res.is_valid:
				for err in loop_res.errors:
					errors.append("Visual Loop payload validation failed: " + str(err))
					
		"visual_drill":
			var drill_res = _validate_visual_drill_payload(payload)
			if not drill_res.is_valid:
				for err in drill_res.errors:
					errors.append("Visual Drill payload validation failed: " + str(err))
					
		_:
			errors.append("Unrecognized envelope kind for payload dispatch: '%s'." % env.kind)

	# Cross-field Temporal Invariant Validation for Time-based Payloads
	if env.kind in ["visual_loop", "visual_drill"]:
		if payload.has("duration") and payload.has("fps") and payload.has("frame_count"):
			var duration_val = payload["duration"]
			var fps_val = payload["fps"]
			var frames_val = payload["frame_count"]
			
			if (duration_val is float or duration_val is int) and (fps_val is int) and (frames_val is int):
				var duration := float(duration_val)
				var fps := int(fps_val)
				var stated_frames := int(frames_val)
				var expected_frames := int(round(duration * float(fps)))
				
				if stated_frames != expected_frames:
					errors.append("Temporal invariant violation: frame_count (%d) does not match expected round(duration * fps) -> (%d)." % [stated_frames, expected_frames])
				
	if not errors.is_empty():
		return {"is_valid": false, "errors": errors}
		
	return {"is_valid": true, "errors": []}


static func _validate_visual_loop_payload(payload: Dictionary) -> Dictionary:
	var errors: Array[String] = []
	
	var allowed := ["duration", "fps", "frame_count", "loop", "visual_parameters"]
	for k in payload.keys():
		if not k in allowed:
			errors.append("Visual loop payload contains disallowed property: '%s'." % str(k))
			
	var required := ["duration", "fps", "frame_count", "loop", "visual_parameters"]
	for req in required:
		if not payload.has(req):
			errors.append("Visual loop payload missing required field '%s'." % req)
			
	if not errors.is_empty():
		return {"is_valid": false, "errors": errors}
		
	var dur = payload["duration"]
	if not dur is float and not dur is int:
		errors.append("Visual loop 'duration' must be a number.")
	elif float(dur) < 0.1:
		errors.append("Visual loop duration must be >= 0.1.")
		
	var f = payload["fps"]
	if not f is int or not f in [30, 60]:
		errors.append("Visual loop 'fps' must be integer 30 or 60.")
		
	var fc = payload["frame_count"]
	if not fc is int or int(fc) < 1:
		errors.append("Visual loop 'frame_count' must be integer >= 1.")
		
	var loop = payload["loop"]
	if not loop is Dictionary:
		errors.append("Visual loop 'loop' must be a Dictionary.")
	else:
		for l_k in loop.keys():
			if not l_k in ["seamless", "boundary_tolerance", "transition_window_frames"]:
				errors.append("Visual loop 'loop' contains disallowed property: '%s'." % str(l_k))
		if not loop.has("seamless") or not loop["seamless"] is bool:
			errors.append("Visual loop missing boolean 'seamless'.")
			
		if not loop.has("boundary_tolerance") or (not loop["boundary_tolerance"] is float and not loop["boundary_tolerance"] is int):
			errors.append("Visual loop missing numeric 'boundary_tolerance'.")
		else:
			var tol := float(loop["boundary_tolerance"])
			if tol < 0.0 or tol > 0.01:
				errors.append("Visual loop 'boundary_tolerance' must be between 0.0 and 0.01.")
				
		if loop.has("transition_window_frames"):
			if not loop["transition_window_frames"] is int:
				errors.append("Visual loop 'transition_window_frames' must be an integer.")
			elif int(loop["transition_window_frames"]) < 0:
				errors.append("Visual loop 'transition_window_frames' must be >= 0.")
			
	var vp = payload["visual_parameters"]
	if not vp is Dictionary:
		errors.append("Visual loop 'visual_parameters' must be a Dictionary.")
	else:
		for vp_k in vp.keys():
			if not vp_k in ["generator", "layers"]:
				errors.append("Visual loop 'visual_parameters' contains disallowed property: '%s'." % str(vp_k))
				
		if not vp.has("generator") or not vp["generator"] is String:
			errors.append("Visual loop missing string 'generator'.")
		elif not str(vp["generator"]) in ["fractal", "vector_field", "particle_flow", "kaleidoscope", "geometric"]:
			errors.append("Visual loop invalid generator enum value: '%s'." % str(vp["generator"]))
			
		if not vp.has("layers") or not vp["layers"] is Array or (vp["layers"] as Array).is_empty():
			errors.append("Visual loop missing non-empty layers array.")
		else:
			for i in range((vp["layers"] as Array).size()):
				var layer = vp["layers"][i]
				if not layer is Dictionary:
					errors.append("Visual loop layer at index %d must be a Dictionary." % i)
					continue
				for l_key in layer.keys():
					if not l_key in ["blend_mode", "speed", "complexity", "color_palette"]:
						errors.append("Visual loop layer contains disallowed property: '%s'." % str(l_key))
				if not layer.has("blend_mode") or not layer["blend_mode"] is String:
					errors.append("Visual loop layer at index %d missing string 'blend_mode'." % i)
				if not layer.has("speed") or (not layer["speed"] is float and not layer["speed"] is int):
					errors.append("Visual loop layer at index %d missing numeric 'speed'." % i)
				if not layer.has("complexity") or not layer["complexity"] is int:
					errors.append("Visual loop layer at index %d missing integer 'complexity'." % i)
				if layer.has("color_palette") and not layer["color_palette"] is String:
					errors.append("Visual loop layer field 'color_palette' must be a String.")
			
	return {"is_valid": errors.is_empty(), "errors": errors}


static func _validate_visual_drill_payload(payload: Dictionary) -> Dictionary:
	var errors: Array[String] = []
	
	var allowed := ["duration", "fps", "frame_count", "exercise_parameters", "stimulus", "targets", "distractors", "trajectory", "task"]
	for k in payload.keys():
		if not k in allowed:
			errors.append("Visual drill payload contains disallowed property: '%s'." % str(k))
			
	var required := ["duration", "fps", "frame_count", "exercise_parameters", "stimulus", "targets", "distractors", "trajectory", "task"]
	for req in required:
		if not payload.has(req):
			errors.append("Visual drill payload missing required field '%s'." % req)
			
	if not errors.is_empty():
		return {"is_valid": false, "errors": errors}
		
	var dur = payload["duration"]
	if not dur is float and not dur is int:
		errors.append("Visual drill 'duration' must be a number.")
	elif float(dur) < 0.1:
		errors.append("Visual drill duration must be >= 0.1.")
		
	var f = payload["fps"]
	if not f is int or not f in [30, 60]:
		errors.append("Visual drill 'fps' must be integer 30 or 60.")
		
	var fc = payload["frame_count"]
	if not fc is int or int(fc) < 1:
		errors.append("Visual drill 'frame_count' must be integer >= 1.")
		
	var ep = payload["exercise_parameters"]
	if not ep is Dictionary:
		errors.append("Visual drill 'exercise_parameters' must be a Dictionary.")
	else:
		for ep_k in ep.keys():
			if not ep_k in ["difficulty_tier", "speed_multiplier", "pacing_mode"]:
				errors.append("Visual drill 'exercise_parameters' contains disallowed property: '%s'." % str(ep_k))
		if not ep.has("difficulty_tier") or not ep["difficulty_tier"] is int or int(ep["difficulty_tier"]) < 1 or int(ep["difficulty_tier"]) > 5:
			errors.append("Visual drill difficulty_tier must be integer between 1 and 5.")
		if not ep.has("speed_multiplier") or (not ep["speed_multiplier"] is float and not ep["speed_multiplier"] is int):
			errors.append("Visual drill missing numeric 'speed_multiplier'.")
		if ep.has("pacing_mode"):
			if not ep["pacing_mode"] is String:
				errors.append("Visual drill 'pacing_mode' must be a String.")
			elif not str(ep["pacing_mode"]) in ["constant", "accelerating", "pulsed"]:
				errors.append("Visual drill invalid 'pacing_mode' enum value: '%s'." % str(ep["pacing_mode"]))
			
	var stimulus = payload["stimulus"]
	if not stimulus is Dictionary:
		errors.append("Visual drill 'stimulus' must be a Dictionary.")
	else:
		for s_k in stimulus.keys():
			if not s_k in ["shape", "size", "color"]:
				errors.append("Visual drill 'stimulus' contains disallowed property: '%s'." % str(s_k))
		if not stimulus.has("shape") or not stimulus["shape"] is String:
			errors.append("Visual drill stimulus missing string 'shape'.")
		elif not str(stimulus["shape"]) in ["dot", "ring", "target", "polygon"]:
			errors.append("Visual drill invalid stimulus shape enum value.")
		if not stimulus.has("size") or (not stimulus["size"] is float and not stimulus["size"] is int):
			errors.append("Visual drill stimulus missing numeric 'size'.")
		if not stimulus.has("color") or not stimulus["color"] is String:
			errors.append("Visual drill stimulus missing string 'color'.")
			
	var targets = payload["targets"]
	if not targets is Dictionary:
		errors.append("Visual drill 'targets' must be a Dictionary.")
	else:
		for t_k in targets.keys():
			if not t_k in ["count"]:
				errors.append("Visual drill 'targets' contains disallowed property: '%s'." % str(t_k))
		if not targets.has("count") or not targets["count"] is int or int(targets["count"]) < 1:
			errors.append("Visual drill targets missing integer 'count' >= 1.")
			
	var distractors = payload["distractors"]
	if not distractors is Dictionary:
		errors.append("Visual drill 'distractors' must be a Dictionary.")
	else:
		for d_k in distractors.keys():
			if not d_k in ["count"]:
				errors.append("Visual drill 'distractors' contains disallowed property: '%s'." % str(d_k))
		if not distractors.has("count") or not distractors["count"] is int or int(distractors["count"]) < 0:
			errors.append("Visual drill distractors missing integer 'count' >= 0.")
			
	var trajectory = payload["trajectory"]
	if not trajectory is Dictionary:
		errors.append("Visual drill 'trajectory' must be a Dictionary.")
	else:
		for tr_k in trajectory.keys():
			if not tr_k in ["pattern", "speed"]:
				errors.append("Visual drill 'trajectory' contains disallowed property: '%s'." % str(tr_k))
		if not trajectory.has("pattern") or not trajectory["pattern"] is String:
			errors.append("Visual drill trajectory missing string 'pattern'.")
		elif not str(trajectory["pattern"]) in ["linear", "lissajous", "random_walk", "orbital"]:
			errors.append("Visual drill invalid trajectory pattern enum value.")
		if not trajectory.has("speed") or (not trajectory["speed"] is float and not trajectory["speed"] is int):
			errors.append("Visual drill trajectory missing numeric 'speed'.")
			
	var task = payload["task"]
	if not task is Dictionary:
		errors.append("Visual drill 'task' must be a Dictionary.")
	else:
		for tk_k in task.keys():
			if not tk_k in ["type", "target_switch_interval"]:
				errors.append("Visual drill 'task' contains disallowed property: '%s'." % str(tk_k))
		if not task.has("type") or not task["type"] is String:
			errors.append("Visual drill task missing string 'type'.")
		elif not str(task["type"]) in ["pursuit", "saccade", "tracking", "peripheral_scan"]:
			errors.append("Visual drill invalid task type enum value.")
		if task.has("target_switch_interval") and not task["target_switch_interval"] is float and not task["target_switch_interval"] is int:
			errors.append("Visual drill task 'target_switch_interval' must be a number.")
			
	return {"is_valid": errors.is_empty(), "errors": errors}