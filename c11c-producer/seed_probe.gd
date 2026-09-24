extends SceneTree

const VariationProfile = preload("res://tools/prototypes/c11c_common/C11CVariationProfile.gd")

func _init() -> void:
    var args: PackedStringArray = OS.get_cmdline_user_args()
    if args.is_empty():
        _write_failure("Missing request JSON path")
        quit(2)
        return
    var request_path: String = args[0]
    if not FileAccess.file_exists(request_path):
        _write_failure("Request JSON not found: " + request_path)
        quit(2)
        return
    var file: FileAccess = FileAccess.open(request_path, FileAccess.READ)
    if file == null:
        _write_failure("Unable to open request JSON")
        quit(2)
        return
    var raw: String = file.get_as_text()
    file.close()
    var parsed: Variant = JSON.parse_string(raw)
    if not (parsed is Dictionary):
        _write_failure("Request JSON must contain an object")
        quit(2)
        return
    var request: Dictionary = parsed
    var family: String = str(request.get("family", "geometric"))
    var candidates_variant: Variant = request.get("candidates", [])
    if not (candidates_variant is Array):
        _write_failure("candidates must be an array")
        quit(2)
        return
    var candidates: Array = candidates_variant
    var targets_variant: Variant = request.get("targets", {})
    if not (targets_variant is Dictionary):
        _write_failure("targets must be an object")
        quit(2)
        return
    var targets: Dictionary = targets_variant
    var requested: int = int(request.get("count", 1))
    var tolerance_multiplier: float = float(request.get("tolerance_multiplier", 1.5))
    var best: Array = []
    for candidate in candidates:
        var seed: int = int(candidate)
        var profile: Dictionary = VariationProfile.build(family, seed)
        var score_data: Variant = _score(profile, targets, tolerance_multiplier)
        if score_data == null:
            continue
        var entry: Dictionary = {"seed": seed, "score": float(score_data), "profile": profile}
        _insert_best(best, entry, requested)
    if best.size() < requested:
        _write_failure("No hay suficientes seeds compatibles con los objetivos solicitados. Seeds encontradas: " + str(best.size()))
        quit(1)
        return
    var results: Array = []
    for entry_variant in best:
        var entry: Dictionary = entry_variant
        results.append({"seed": int(entry["seed"]), "score": float(entry["score"]), "profile": entry["profile"]})
    _write_success(results)
    quit(0)

func _score(profile: Dictionary, targets: Dictionary, tolerance_multiplier: float) -> Variant:
    var score: float = 0.0
    for key_variant in targets.keys():
        var key: String = str(key_variant)
        if not profile.has(key):
            return null
        var wanted: Variant = targets[key]
        var actual: Variant = profile[key]
        if wanted is String:
            if str(actual) != str(wanted):
                return null
        elif wanted is int:
            var diff_int: float = abs(float(actual) - float(wanted))
            if diff_int > 0.000001:
                return null
        elif wanted is float:
            var tol: float = max(0.0005, abs(float(wanted)) * 0.002 * tolerance_multiplier)
            var diff: float = abs(float(actual) - float(wanted))
            score += diff / tol
        else:
            if str(actual) != str(wanted):
                return null
    return score

func _insert_best(best: Array, entry: Dictionary, requested: int) -> void:
    var inserted: bool = false
    var entry_score: float = float(entry["score"])
    for i in range(best.size()):
        var current: Dictionary = best[i]
        if entry_score < float(current["score"]):
            best.insert(i, entry)
            inserted = true
            break
    if not inserted:
        best.append(entry)
    if best.size() > requested:
        best.resize(requested)

func _response_path() -> String:
    var args: PackedStringArray = OS.get_cmdline_user_args()
    if args.is_empty():
        return ""
    return args[0].get_base_dir().path_join("response.json")

func _write_success(results: Array) -> void:
    var path: String = _response_path()
    if path.is_empty():
        return
    _write(path, {"ok": true, "results": results})

func _write_failure(message: String) -> void:
    var path: String = _response_path()
    if path.is_empty():
        return
    _write(path, {"ok": false, "error": message})

func _write(path: String, data: Dictionary) -> void:
    var f: FileAccess = FileAccess.open(path, FileAccess.WRITE)
    if f == null:
        return
    f.store_string(JSON.stringify(data))
    f.close()
