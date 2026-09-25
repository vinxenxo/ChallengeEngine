extends SceneTree

## C11-C 2.11.1 — family-aware music binding contract.
## Music is delivery/presentation metadata: no gameplay frame/event/answer-sheet input is permitted.

const ProfileService = preload("res://core/presentation/C11CVisualMusicProfile.gd")
const PROFILE_PATH := "res://profiles/presentation/c11c_visual_music_profiles.json"
const DRILLS := ["tracking", "saccade", "pursuit", "peripheral_scan"]
const LOOPS := ["geometric", "fractal", "sacred_symmetry", "living_particles", "invisible_forces"]
const HISTORICAL_ALIASES := ["kaleidoscope", "particle_flow", "vector_field"]

var failures: Array[String] = []

func _initialize() -> void:
    _assert(FileAccess.file_exists(PROFILE_PATH), "Music profile JSON must exist.")
    var data = JSON.parse_string(FileAccess.get_file_as_string(PROFILE_PATH))
    _assert(data is Dictionary, "Music profile JSON must be a valid object.")
    if not data is Dictionary:
        _conclude()
        return
    _assert(str(data.get("mode", "")) == "FAMILY_MUSIC_V4", "Music mode must be FAMILY_MUSIC_V4.")
    _assert(bool(data.get("mobile_safe", false)), "Music contract must declare mobile-safe delivery.")
    _assert(not bool(data.get("event_coupled", true)), "Music must not be event-coupled to gameplay truth.")
    _assert(bool(data.get("seed_deterministic", false)), "Music must be deterministic with seed/family identity.")
    var design_rules: Dictionary = data.get("design_rules", {})
    _assert(int(design_rules.get("sample_rate", 0)) == 44100, "Music sample rate must remain 44100 Hz.")
    _assert(int(design_rules.get("channels", 0)) == 2, "Music must remain stereo.")
    _assert(float(design_rules.get("max_peak", 1.0)) <= 0.36, "Music peak must remain within the C11-C mobile-presence ceiling.")
    _assert(is_equal_approx(float(design_rules.get("max_peak", 0.0)), 0.36), "Music contract must document the active 0.36 peak ceiling.")
    _assert(str(design_rules.get("scale", "")) == "A minor pentatonic", "Music scale must be the A-minor pentatonic scale.")
    var pentatonic: Array = design_rules.get("pentatonic_hz", [])
    _assert(pentatonic.size() >= 9, "Pentatonic frequency bank must contain the documented A-minor range.")
    _assert(float(design_rules.get("target_rms_min", 0.0)) >= 0.08, "Music must have a meaningful audible RMS target.")
    _assert(float(design_rules.get("target_rms_max", 0.0)) <= 0.16, "Music RMS must remain bounded to avoid an intrusive mobile mix.")
    _assert(Array(design_rules.get("attack_seconds", [])).size() == 2, "Music contract must expose attack range.")
    _assert(Array(design_rules.get("release_seconds", [])).size() == 2, "Music contract must expose release range.")
    _assert(str(design_rules.get("noise_modulation", "")).find("low_frequency") >= 0, "Music must use slow deterministic noise modulation.")
    _assert(str(design_rules.get("generator_revision", "")).begins_with("4.1.1"), "Music generator revision must be 4.1.x for this checkpoint.")
    _assert(str(design_rules.get("stereo_motion", "")).find("plus_minus_0.16") >= 0, "Stereo motion must remain bounded to the documented mobile-safe range.")
    _assert(str(design_rules.get("seed_pitch_scale", "")).find("0.80_to_1.20") >= 0, "Seeded whole-pad pitch scaling must be documented as 0.80x–1.20x.")

    var profiles: Array = data.get("profiles", [])
    var ids: Dictionary = {}
    for entry in profiles:
        if entry is Dictionary:
            ids[str(entry.get("id", ""))] = true
    _assert(profiles.size() == 5, "Exactly five semantic music profiles must be defined.")
    for entry_variant in profiles:
        if entry_variant is Dictionary:
            var profile_entry: Dictionary = entry_variant
            _assert(profile_entry.has("decay_sec"), "Every music profile must declare an explicit ADSR decay stage.")
            _assert(float(profile_entry.get("pan_depth", 1.0)) <= 0.16, "Every music profile must keep stereo motion within ±0.16.")
    _assert(ids.size() == 5, "Music profile IDs must be unique.")

    for family in DRILLS:
        _assert(ProfileService.profile_for("visual_drill/" + family) != "", "%s must resolve to a music profile." % family)
    for family in LOOPS:
        _assert(ProfileService.profile_for("visual_loop/" + family) != "", "%s must resolve to a music profile." % family)
    for family in HISTORICAL_ALIASES:
        _assert(ProfileService.profile_for("visual_loop/" + family) != "", "Historical alias %s must remain resolvable." % family)

    var all_reachable: Dictionary = {}
    for route in [
        "visual_drill/tracking", "visual_drill/saccade", "visual_drill/pursuit", "visual_drill/peripheral_scan",
        "visual_loop/geometric", "visual_loop/fractal", "visual_loop/sacred_symmetry", "visual_loop/living_particles", "visual_loop/invisible_forces",
        "visual_loop/kaleidoscope"
    ]:
        all_reachable[ProfileService.profile_for(route)] = true
    _assert(all_reachable.size() == 5, "All five semantic music profiles must be reachable from current or preserved historical routes.")

    var reachable: Dictionary = {}
    for route in [
        "visual_drill/tracking", "visual_drill/saccade", "visual_drill/pursuit", "visual_drill/peripheral_scan",
        "visual_loop/geometric", "visual_loop/fractal", "visual_loop/sacred_symmetry", "visual_loop/living_particles", "visual_loop/invisible_forces"
    ]:
        reachable[ProfileService.profile_for(route)] = true
    _assert(reachable.size() == 4, "The four current Drill families must use four intentionally distinct semantic profiles.")
    _assert(ProfileService.profile_for("visual_drill/saccade") == ProfileService.profile_for("visual_loop/geometric"), "Saccade and Geometric Waves must share their intended musical pairing.")
    _assert(ProfileService.profile_for("visual_drill/pursuit") == ProfileService.profile_for("visual_loop/fractal"), "Pursuit and Fractal Bloom must share their intended musical pairing.")
    _assert(ProfileService.profile_for("visual_drill/peripheral_scan") == ProfileService.profile_for("visual_loop/sacred_symmetry"), "Peripheral Scan and Sacred Symmetry must share their intended musical pairing.")
    _assert(ProfileService.profile_for("visual_drill/tracking") == ProfileService.profile_for("visual_loop/invisible_forces"), "Tracking and Invisible Forces must share their intended musical pairing.")

    for source_path in [
        "res://tools/prototypes/c11c_common/generate_c11c_family_music.py",
        "res://tools/prototypes/c11c_common/C11CSafeAmbient.py",
        "res://tools/prototypes/c11c_bulk/run_c11c_visual_drill_review.ps1"
    ]:
        var source := FileAccess.get_file_as_string(source_path)
        _assert(source.find("FAMILY_MUSIC_V4") >= 0, "%s must use FAMILY_MUSIC_V4." % source_path)
        _assert(source.find("game_event") < 0 and source.find("answer_sheet") < 0, "%s must not couple music generation to gameplay truth." % source_path)


    var generator_source := FileAccess.get_file_as_string("res://tools/prototypes/c11c_common/generate_c11c_family_music.py")
    _assert(generator_source.find("PENTATONIC_HZ") >= 0, "Music generator must use the pentatonic frequency bank.")
    _assert(generator_source.find("note_envelope") >= 0, "Music generator must implement an ADSR envelope.")
    _assert(generator_source.find("value_noise_1d") >= 0 and generator_source.find("cyclic_value_noise_1d") >= 0, "Music generator must use slow deterministic loop-safe noise modulation.")
    _assert(generator_source.find("lowpass_pair") >= 0 and generator_source.find("low_pass_periodic_modulated") >= 0, "Music generator must apply low-pass filtering with loop-safe deterministic cutoff modulation.")
    _assert(generator_source.find("stereo_phase") >= 0, "Music generator must implement slow deterministic stereo motion.")
    _assert(generator_source.find("winning_frame") < 0 and generator_source.find("close_calls") < 0, "Music generator must not depend on frozen gameplay truth.")
    _assert(generator_source.find("grammar") >= 0, "Music generator must accept visual grammar as a deterministic semantic input.")
    _assert(FileAccess.get_file_as_string("res://tools/prototypes/c11c_common/C11CSafeAmbient.py").find("generate(out, seed, family, profile, cycles, dur, kind, grammar)") >= 0, "Safe ambient wrapper must forward grammar to the family music generator.")

    _conclude()

func _assert(condition: bool, message: String) -> void:
    if not condition:
        failures.append(message)

func _conclude() -> void:
    if failures.is_empty():
        print("[C11C_VISUAL_MUSIC_PROFILE_CONTRACT_SUITE] PASS")
        quit(0)
    else:
        for failure in failures:
            push_error(failure)
        print("[C11C_VISUAL_MUSIC_PROFILE_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
        quit(1)
