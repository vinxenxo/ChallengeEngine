class_name DifficultyProfileValidator
extends RefCounted

static func validate(challenge_data: Dictionary, profile_data: Dictionary) -> Array:
	var errors = []
	
	# 1. Correspondencia de mecánica
	var c_mechanic = challenge_data.get("mechanic", "")
	var p_mechanic = profile_data.get("mechanic", "")
	if c_mechanic != p_mechanic:
		errors.append("Mechanic mismatch: challenge is '%s' but profile is '%s'" % [c_mechanic, p_mechanic])
		
	var overrides = challenge_data.get("difficulty", {}).get("overrides", {})
	var allowed = profile_data.get("allowed_parameters", [])
	var constraints = profile_data.get("constraints", {})
	
	# 2. Reglas de overrides y dominio
	for k in overrides:
		if not allowed.has(k):
			errors.append("Override key not allowed: " + k)
			continue
			
		if constraints.has(k):
			var rule = constraints[k]
			var val = overrides[k]
			
			# Type check estricto
			if rule.has("type"):
				var expected_type = rule["type"]
				if expected_type == "int" and typeof(val) != TYPE_INT:
					errors.append("Parameter '%s' must be int" % k)
				elif expected_type == "float" and typeof(val) != TYPE_FLOAT and typeof(val) != TYPE_INT:
					errors.append("Parameter '%s' must be float/number" % k)
					
			# Bounds check
			if rule.has("min") and val < rule["min"]:
				errors.append("Parameter '%s' (%s) is below min (%s)" % [k, str(val), str(rule["min"])])
			if rule.has("max") and val > rule["max"]:
				errors.append("Parameter '%s' (%s) is above max (%s)" % [k, str(val), str(rule["max"])])
				
	return errors