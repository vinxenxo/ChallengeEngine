class_name C11CVariationProfile
extends RefCounted

## C11-C.6 — Presentation-only deterministic variation manifold.
## Same family + same seed => same profile. No production engine state is touched.

const VERSION: String = "1.6.0"

static func build(family_id: String, seed_value: int) -> Dictionary:
    var family: String = _canonical_family(family_id)
    match family:
        "geometric":
            return _geometric(seed_value)
        "fractal":
            return _fractal(seed_value)
        "sacred_symmetry":
            return _sacred(seed_value)
        "living_particles":
            return _living(seed_value)
        "invisible_forces":
            return _invisible(seed_value)
        _:
            return _geometric(seed_value)

static func _geometric(seed_value: int) -> Dictionary:
    var grammar_modes: Array[String] = [
        "harmonic_membrane",
        "interference_plane",
        "parametric_ribbon",
        "lattice_wave",
        "orbital_wave"
    ]
    var palette_modes: Array[String] = [
        "cyan_magenta",
        "electric_blue_lilac",
        "turquoise_orchid",
        "spectral_blue",
        "warm_cold_harmonic"
    ]
    var grammar_index: int = _index(seed_value, 11, grammar_modes.size())
    var palette_index: int = _index(seed_value, 13, palette_modes.size())
    return {
        "family": "geometric",
        "grammar_mode": grammar_index,
        "grammar_name": grammar_modes[grammar_index],
        "palette_mode": palette_index,
        "palette_name": palette_modes[palette_index],
        "polygon_sides": [5, 6, 7, 8][_index(seed_value, 17, 4)],
        "wave_frequency": lerpf(12.0, 28.0, _unit(seed_value, 19)),
        "morph": lerpf(0.18, 0.92, _unit(seed_value, 23)),
        "line_width": lerpf(0.0048, 0.0094, _unit(seed_value, 29)),
        "glow": lerpf(0.34, 0.72, _unit(seed_value, 31)),
        "wave_ratio": lerpf(0.62, 1.02, _unit(seed_value, 37)),
        "shape_rotation": lerpf(-0.42, 0.42, _unit(seed_value, 41)),
        "layer_spread": lerpf(0.014, 0.076, _unit(seed_value, 43)),
        "radial_wave_amplitude": lerpf(0.012, 0.062, _unit(seed_value, 47)),
        "liss_x_frequency": float([5, 6, 7, 8, 9, 10, 11][_index(seed_value, 53, 7)]),
        "liss_y_frequency": float([3, 4, 5, 6, 7, 8][_index(seed_value, 59, 6)]),
        "interference_scale": lerpf(0.74, 1.42, _unit(seed_value, 61)),
        "hero_scale": lerpf(0.80, 1.03, _unit(seed_value, 67)),
        "perspective_strength": lerpf(0.35, 1.02, _unit(seed_value, 71)),
        "depth_strength": lerpf(0.42, 0.94, _unit(seed_value, 73)),
        "secondary_phase": lerpf(-1.10, 1.10, _unit(seed_value, 79)),
        "color_phase": lerpf(-3.14, 3.14, _unit(seed_value, 83)),
        "stroke_scale": lerpf(0.78, 1.28, _unit(seed_value, 89))
    }

static func _fractal(seed_value: int) -> Dictionary:
    return {
        "family": "fractal",
        "zoom_strength": lerpf(0.48, 0.94, _unit(seed_value, 71)),
        "warp_strength": lerpf(0.018, 0.062, _unit(seed_value, 73)),
        "bloom_strength": lerpf(0.58, 0.92, _unit(seed_value, 79)),
        "layer_softness": lerpf(0.55, 1.10, _unit(seed_value, 83)),
        "julia_x_bias": lerpf(-0.055, 0.055, _unit(seed_value, 89)),
        "julia_y_bias": lerpf(-0.060, 0.060, _unit(seed_value, 97)),
        "zoom_cycles": float([1, 2, 3][_index(seed_value, 101, 3)]),
        "warp_frequency": lerpf(2.3, 4.8, _unit(seed_value, 103)),
        "layer_spread": lerpf(0.05, 0.18, _unit(seed_value, 107)),
        "breath_strength": lerpf(0.055, 0.115, _unit(seed_value, 109))
    }

static func _sacred(seed_value: int) -> Dictionary:
    var orders: Array[int] = [4, 6, 8, 12]
    var grammar_modes: Array[String] = ["astrolabe", "gear_train", "polygon_orrery", "origami_mandala", "celestial_chart"]
    var palette_modes: Array[String] = ["liquid_gold", "gold_copper", "amber_laser", "bronze_pale_gold", "warm_obsidian"]
    var grammar_index: int = _index(seed_value, 127, grammar_modes.size())
    var palette_index: int = _index(seed_value, 129, palette_modes.size())
    return {
        "family": "sacred_symmetry",
        "grammar_mode": grammar_index,
        "grammar_name": grammar_modes[grammar_index],
        "palette_mode": palette_index,
        "palette_name": palette_modes[palette_index],
        "symmetry_order": orders[_index(seed_value, 131, orders.size())],
        "ring_bias": lerpf(0.30, 0.82, _unit(seed_value, 133)),
        "glow": lerpf(0.40, 0.78, _unit(seed_value, 137)),
        "gear_inner": float([2, 3, 5][_index(seed_value, 139, 3)]),
        "gear_outer": float([1, -2, 3][_index(seed_value, 149, 3)]),
        "ring_scale": lerpf(0.90, 1.08, _unit(seed_value, 151)),
        "core_scale": lerpf(0.82, 1.16, _unit(seed_value, 157)),
        "tick_density": lerpf(0.82, 1.34, _unit(seed_value, 163)),
        "mechanical_rate": float([1.0, 1.5, 2.0][_index(seed_value, 167, 3)]),
        "macro_scale": lerpf(0.86, 1.04, _unit(seed_value, 169)),
        "node_density": lerpf(0.72, 1.28, _unit(seed_value, 173)),
        "fold_depth": lerpf(0.78, 1.22, _unit(seed_value, 179))
    }

static func _living(seed_value: int) -> Dictionary:
    var grammar_modes: Array[String] = ["swarm", "vortex", "collision_cloud", "organic_pulse", "magnetic_filament_cloud"]
    var palette_modes: Array[String] = ["emerald_sea_green", "turquoise_aqua", "jade_teal", "cyan_green_spectral", "green_blue_mono"]
    var grammar_index: int = _index(seed_value, 181, grammar_modes.size())
    var palette_index: int = _index(seed_value, 183, palette_modes.size())
    return {
        "family": "living_particles",
        "grammar_mode": grammar_index,
        "grammar_name": grammar_modes[grammar_index],
        "palette_mode": palette_index,
        "palette_name": palette_modes[palette_index],
        "particle_count": lerpf(104.0, 170.0, _unit(seed_value, 187)),
        "glow": lerpf(0.56, 0.88, _unit(seed_value, 191)),
        "attractor_a_x": lerpf(-0.22, -0.04, _unit(seed_value, 197)),
        "attractor_a_y": lerpf(-0.16, 0.09, _unit(seed_value, 199)),
        "attractor_b_x": lerpf(0.04, 0.22, _unit(seed_value, 211)),
        "attractor_b_y": lerpf(-0.05, 0.17, _unit(seed_value, 223)),
        "swirl_bias": lerpf(0.62, 1.48, _unit(seed_value, 227)),
        "particle_spread": lerpf(0.78, 1.18, _unit(seed_value, 229)),
        "turbulence": lerpf(0.012, 0.046, _unit(seed_value, 233)),
        "attractor_strength": lerpf(0.72, 1.44, _unit(seed_value, 239)),
        "particle_size_scale": lerpf(0.74, 1.30, _unit(seed_value, 241)),
        "phase_rate": lerpf(0.68, 1.24, _unit(seed_value, 251)),
        "collision_strength": lerpf(0.72, 1.40, _unit(seed_value, 257)),
        "core_scale": lerpf(0.78, 1.18, _unit(seed_value, 259)),
        "density_bias": lerpf(0.86, 1.16, _unit(seed_value, 261))
    }

static func _invisible(seed_value: int) -> Dictionary:
    return {
        "family": "invisible_forces",
        "trace_count": lerpf(50.0, 88.0, _unit(seed_value, 263)),
        "curvature": lerpf(0.58, 1.22, _unit(seed_value, 269)),
        "glow": lerpf(0.62, 0.94, _unit(seed_value, 271)),
        "field_rotation": lerpf(-0.20, 0.20, _unit(seed_value, 277)),
        "storm_offset_x": lerpf(-0.055, 0.055, _unit(seed_value, 281)),
        "storm_offset_y": lerpf(-0.040, 0.040, _unit(seed_value, 283)),
        "pulse_speed": lerpf(0.72, 1.32, _unit(seed_value, 293)),
        "field_twist": lerpf(0.78, 1.28, _unit(seed_value, 307)),
        "pulse_width": lerpf(0.72, 1.38, _unit(seed_value, 311)),
        "storm_scale": lerpf(0.86, 1.18, _unit(seed_value, 313))
    }

static func _canonical_family(family_id: String) -> String:
    match family_id:
        "c11c_geometric_waves_v1", "geometric", "geometric_waves":
            return "geometric"
        "c11c_fractal_bloom_v1", "fractal", "fractal_bloom":
            return "fractal"
        "c11c_sacred_symmetry_v1", "kaleidoscope", "sacred_symmetry":
            return "sacred_symmetry"
        "c11c_living_particles_v1", "particle_flow", "living_particles":
            return "living_particles"
        "c11c_invisible_forces_v1", "vector_field", "invisible_forces":
            return "invisible_forces"
        _:
            return "geometric"

static func _mixed(seed_value: int, salt: int) -> int:
    var x: int = (int(seed_value) ^ int(salt * 374761393)) & 0x7fffffff
    x = int((x ^ (x >> 13)) * 1274126177) & 0x7fffffff
    x = int((x ^ (x >> 16)) * 2246822519) & 0x7fffffff
    x = int((x ^ (x >> 13)) * 3266489917) & 0x7fffffff
    return int(x ^ (x >> 16)) & 0x7fffffff

static func _index(seed_value: int, salt: int, size: int) -> int:
    return _mixed(seed_value, salt) % maxi(size, 1)

static func _unit(seed_value: int, salt: int) -> float:
    return float(_mixed(seed_value, salt) % 1000000) / 999999.0
