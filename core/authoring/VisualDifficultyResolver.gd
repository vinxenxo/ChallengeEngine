class_name VisualDifficultyResolver
extends RefCounted

## C10-A — Pure, deterministic difficulty resolver.
## No filesystem access, no RNG, no presentation knowledge.
## Policy shape:
## {
##   "allowed_parameters": [...],
##   "base_parameters": {...},
##   "tiers": {"1": {...}, ..., "5": {...}}
## }

static func validate_custom_parameters(policy: Dictionary, custom_parameters: Dictionary) -> Array[String]:
    var errors: Array[String] = []
    var allowed: Array = policy.get("allowed_parameters", [])

    for key in custom_parameters.keys():
        if not allowed.has(key):
            errors.append("Custom parameter '%s' is not allowed for this authoring contract." % str(key))

    return errors

static func resolve(
    difficulty_tier: int,
    policy: Dictionary,
    custom_parameters: Dictionary = {}
) -> Dictionary:
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
        effective[key] = base_parameters[key]

    var tiers: Dictionary = policy.get("tiers", {})
    var tier_key := str(difficulty_tier)
    if not tiers.has(tier_key):
        return {
            "success": false,
            "error": "Authoring policy is missing tier '%s'." % tier_key,
            "effective_parameters": {}
        }

    var tier_parameters: Dictionary = tiers[tier_key]
    for key in tier_parameters.keys():
        effective[key] = tier_parameters[key]

    for key in custom_parameters.keys():
        effective[key] = custom_parameters[key]

    return {
        "success": true,
        "error": "",
        "effective_parameters": effective,
        "difficulty_tier": difficulty_tier
    }
