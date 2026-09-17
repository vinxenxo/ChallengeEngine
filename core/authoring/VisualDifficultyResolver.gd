class_name VisualDifficultyResolver
extends RefCounted

## C10-A.1 — Pure, deterministic difficulty resolver.
## No filesystem access, no RNG, no presentation knowledge.

static func validate_policy(policy: Dictionary) -> Array[String]:
    var errors: Array[String] = []
    if not policy.has("allowed_parameters") or not (policy["allowed_parameters"] is Array):
        errors.append("Authoring policy requires allowed_parameters Array.")
    if not policy.has("base_parameters") or not (policy["base_parameters"] is Dictionary):
        errors.append("Authoring policy requires base_parameters Dictionary.")
    if not policy.has("tiers") or not (policy["tiers"] is Dictionary):
        errors.append("Authoring policy requires tiers Dictionary.")
        return errors

    for tier in ["1", "2", "3", "4", "5"]:
        if not policy["tiers"].has(tier) or not (policy["tiers"][tier] is Dictionary):
            errors.append("Authoring policy is missing tier '%s'." % tier)

    return errors

static func validate_custom_parameters(policy: Dictionary, custom_parameters: Dictionary) -> Array[String]:
    var errors: Array[String] = []
    var allowed: Array = policy.get("allowed_parameters", [])
    var constraints: Dictionary = policy.get("constraints", {})

    for key in custom_parameters.keys():
        var key_str := str(key)
        if not allowed.has(key_str):
            errors.append("Custom parameter '%s' is not allowed for this authoring contract." % key_str)
            continue
        if constraints.has(key_str):
            var constraint: Dictionary = constraints[key_str]
            var value = custom_parameters[key]
            var type_name := str(constraint.get("type", ""))
            if type_name == "float" and typeof(value) != TYPE_FLOAT and typeof(value) != TYPE_INT:
                errors.append("Parameter '%s' must be numeric." % key_str)
                continue
            if type_name == "int" and typeof(value) != TYPE_INT:
                errors.append("Parameter '%s' must be int." % key_str)
                continue
            if type_name == "bool" and typeof(value) != TYPE_BOOL:
                errors.append("Parameter '%s' must be bool." % key_str)
                continue
            if type_name == "string" and typeof(value) != TYPE_STRING:
                errors.append("Parameter '%s' must be string." % key_str)
                continue
            if constraint.has("min") and (value is int or value is float) and float(value) < float(constraint["min"]):
                errors.append("Parameter '%s' is below minimum." % key_str)
            if constraint.has("max") and (value is int or value is float) and float(value) > float(constraint["max"]):
                errors.append("Parameter '%s' is above maximum." % key_str)
            if constraint.has("enum") and not constraint["enum"].has(value):
                errors.append("Parameter '%s' has an unsupported value '%s'." % [key_str, str(value)])

    return errors

static func resolve(
    difficulty_tier: int,
    policy: Dictionary,
    custom_parameters: Dictionary = {}
) -> Dictionary:
    var policy_errors := validate_policy(policy)
    if not policy_errors.is_empty():
        return {
            "success": false,
            "error": "Invalid authoring policy: %s" % str(policy_errors),
            "effective_parameters": {}
        }

    if difficulty_tier < 1 or difficulty_tier > 5:
        return {
            "success": false,
            "error": "difficulty_tier must be in range 1..5.",
            "effective_parameters": {}
        }

    var override_errors := validate_custom_parameters(policy, custom_parameters)
    if not override_errors.is_empty():
        return {
            "success": false,
            "error": "Invalid custom parameters: %s" % str(override_errors),
            "effective_parameters": {}
        }

    var effective: Dictionary = {}
    var base_parameters: Dictionary = policy.get("base_parameters", {})
    for key in base_parameters.keys():
        effective[str(key)] = base_parameters[key]

    var tiers: Dictionary = policy.get("tiers", {})
    var tier_parameters: Dictionary = tiers[str(difficulty_tier)]
    for key in tier_parameters.keys():
        effective[str(key)] = tier_parameters[key]

    for key in custom_parameters.keys():
        effective[str(key)] = custom_parameters[key]

    return {
        "success": true,
        "error": "",
        "effective_parameters": effective,
        "difficulty_tier": difficulty_tier
    }
