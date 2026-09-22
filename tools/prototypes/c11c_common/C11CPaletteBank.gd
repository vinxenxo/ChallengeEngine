class_name C11CPaletteBank
extends RefCounted

## C11-C presentation palette bank v2.0.1.
## Palette selection is presentation-only and deterministic.

const PALETTES := {
    "geometric": [
        {"name":"CYAN_MAGENTA", "dominant":"16E6FF", "secondary":"FF3EBA", "highlight":"FFFFFF"},
        {"name":"ELECTRIC_BLUE_LILAC", "dominant":"4D7CFE", "secondary":"B98CFF", "highlight":"F5F8FF"},
        {"name":"TURQUOISE_ORCHID", "dominant":"28E0D1", "secondary":"E06BFF", "highlight":"FFFFFF"},
        {"name":"SPECTRAL_BLUE", "dominant":"A4DFFF", "secondary":"477BFF", "highlight":"F5FFFF"},
        {"name":"WARM_COLD_HARMONIC", "dominant":"FFB04A", "secondary":"37D7FF", "highlight":"FFF7E8"},
        {"name":"INDIGO_ROSE", "dominant":"5666D9", "secondary":"FF4F9A", "highlight":"F5F0FF"},
        {"name":"AQUA_ULTRAVIOLET", "dominant":"40F0EE", "secondary":"B86CFF", "highlight":"F8FFFF"},
        {"name":"SILVER_ICE", "dominant":"DDEAFF", "secondary":"79B9FF", "highlight":"FFFFFF"},
        {"name":"CORAL_VIOLET", "dominant":"FF6E7A", "secondary":"8A6CFF", "highlight":"FFF8FB"},
        {"name":"MINT_FUCHSIA", "dominant":"75F5D4", "secondary":"FF4FC7", "highlight":"FFFFFF"},
        {"name":"ACID_LIME_BLUE", "dominant":"B6FF4A", "secondary":"438CFF", "highlight":"F7FFE9"},
        {"name":"SKY_ROSE", "dominant":"66D9FF", "secondary":"FF82C8", "highlight":"FFFFFF"},

        {"name":"LAVA_BLUE", "dominant":"5A0A3D", "secondary":"FF6B35", "highlight":"FFE7D6"},
        {"name":"ULTRA_PINK_CYAN", "dominant":"FF2FB3", "secondary":"28F0FF", "highlight":"FFFFFF"},
        {"name":"VIOLET_LIME", "dominant":"8A5CFF", "secondary":"C8FF2E", "highlight":"F7FFDD"},
        {"name":"OBSIDIAN_TEAL", "dominant":"0DE2B4", "secondary":"7B3DFF", "highlight":"F2FFFF"},
        {"name":"EMBER_AQUA", "dominant":"FF3B1F", "secondary":"22FFC8", "highlight":"FFF4EA"},
        {"name":"VIOLET_GOLD", "dominant":"9B4DFF", "secondary":"FFC928", "highlight":"FFFBEA"},
        {"name":"FUCHSIA_TEAL", "dominant":"FF2CA3", "secondary":"16E6C5", "highlight":"FFF8FC"},
        {"name":"ARCTIC_ORANGE", "dominant":"8CEBFF", "secondary":"FF7C43", "highlight":"FFFFFF"},
    ],
    "fractal": [
        {"name":"INDIGO_VIOLET_CYAN", "indigo":"121A4C", "violet":"6F35E8", "cyan":"22D3EE", "highlight":"F8FBFF"},
        {"name":"MIDNIGHT_ELECTRIC_VIOLET", "indigo":"080D24", "violet":"8A35FF", "cyan":"5B6CFF", "highlight":"FFFFFF"},
        {"name":"TEAL_INDIGO", "indigo":"062A2F", "violet":"244DAA", "cyan":"27E2C5", "highlight":"EFFFFF"},
        {"name":"ULTRAVIOLET_MAGENTA_CYAN", "indigo":"21002F", "violet":"B21CFF", "cyan":"FF4BCB", "highlight":"FFF2FF"},
        {"name":"MONOCHROME_INDIGO", "indigo":"11163E", "violet":"3F52B5", "cyan":"9CB3FF", "highlight":"F4F7FF"},
        {"name":"BLUE_CYAN_ICE", "indigo":"061B35", "violet":"2A72C7", "cyan":"72F4FF", "highlight":"FFFFFF"},
        {"name":"VIOLET_ROSE_CYAN", "indigo":"280A3D", "violet":"A73DF2", "cyan":"FF7AD8", "highlight":"FFF7FF"},
        {"name":"DEEP_TEAL_VIOLET", "indigo":"062B30", "violet":"4F46C6", "cyan":"63E6FF", "highlight":"F4FFFF"},
        {"name":"ULTRAVIOLET_MINT", "indigo":"17002A", "violet":"7A20E8", "cyan":"64FFC9", "highlight":"F4FFF9"},
        {"name":"ACID_LIME_VIOLET", "indigo":"17222A", "violet":"863BDB", "cyan":"B6FF4E", "highlight":"FAFFE9"},
        {"name":"ROSE_ULTRAVIOLET", "indigo":"300A24", "violet":"D336B8", "cyan":"7C63FF", "highlight":"FFF5FD"},
        {"name":"ROYAL_BLUE_FUCHSIA", "indigo":"09153F", "violet":"315CDE", "cyan":"FF58E5", "highlight":"FFFFFF"},

        {"name":"CORAL_ULTRAVIOLET", "indigo":"3A0A20", "violet":"FF4F91", "cyan":"8A5CFF", "highlight":"FFF3F8"},
        {"name":"MINT_MAGENTA", "indigo":"031E22", "violet":"6BFFCF", "cyan":"FF3DB8", "highlight":"F0FFF9"},
        {"name":"CYAN_LIME_NEBULA", "indigo":"061F2C", "violet":"29D9FF", "cyan":"B6FF3A", "highlight":"F5FFE9"},
        {"name":"ROYAL_VIOLET_ROSE", "indigo":"11113A", "violet":"7C3AED", "cyan":"F43F8B", "highlight":"FFF5FA"},
        {"name":"CRIMSON_CYAN_NEBULA", "indigo":"1B0614", "violet":"E03A5A", "cyan":"31E9FF", "highlight":"FFF4F8"},
        {"name":"GOLD_VIOLET_NEBULA", "indigo":"201708", "violet":"8E5BFF", "cyan":"FFD34E", "highlight":"FFFBEA"},
        {"name":"LIME_VIOLET_VOID", "indigo":"0B1520", "violet":"7C3AED", "cyan":"D2FF39", "highlight":"F8FFE9"},
        {"name":"ICE_ROSE_NEBULA", "indigo":"0A1828", "violet":"7ED6FF", "cyan":"FF4F9A", "highlight":"FFFFFF"},
    ],
    "sacred_symmetry": [
        {"name":"LIQUID_GOLD", "primary":"C98A17", "secondary":"FFD447", "highlight":"FFF3B0", "white_gold":"FFFFFF", "accent":"FF9E2C"},
        {"name":"GOLD_COPPER", "primary":"B96A24", "secondary":"F2A23A", "highlight":"FFE19A", "white_gold":"FFF8ED", "accent":"D77C2F"},
        {"name":"AMBER_LASER", "primary":"C66E00", "secondary":"FFB000", "highlight":"FFE36B", "white_gold":"FFFFF7", "accent":"FF5D00"},
        {"name":"BRONZE_PALE_GOLD", "primary":"8C5A34", "secondary":"D6A85A", "highlight":"F1D08A", "white_gold":"FFF4DE", "accent":"B77B46"},
        {"name":"WARM_OBSIDIAN", "primary":"6F3E1E", "secondary":"B56A2B", "highlight":"E2AF5F", "white_gold":"FFF1DA", "accent":"8B4B22"},
        {"name":"CHAMPAGNE_BRASS", "primary":"A88A49", "secondary":"E7C56E", "highlight":"FFEFC1", "white_gold":"FFFFFF", "accent":"C7A44A"},
        {"name":"COPPER_FIRE", "primary":"9C3F25", "secondary":"EF7336", "highlight":"FFC07A", "white_gold":"FFF6EC", "accent":"FF9C3D"},
        {"name":"PLATINUM_WARM_GOLD", "primary":"9D8C70", "secondary":"E4CC98", "highlight":"FFF1C9", "white_gold":"FFFFFF", "accent":"C9A86A"},
        {"name":"ROSE_GOLD", "primary":"9E5550", "secondary":"E7A08A", "highlight":"FFD1C1", "white_gold":"FFF8F6", "accent":"C96A55"},
        {"name":"ANTIQUE_BRASS", "primary":"6F6A3D", "secondary":"B5A650", "highlight":"E2D68A", "white_gold":"FFFBEA", "accent":"8D8438"},
        {"name":"WARM_PLATINUM", "primary":"8B8178", "secondary":"C9B9A7", "highlight":"EFE0CF", "white_gold":"FFFFFF", "accent":"A78E76"},
        {"name":"IVORY_GOLD", "primary":"A7945E", "secondary":"F0D58D", "highlight":"FFF6D8", "white_gold":"FFFFFF", "accent":"D2AE61"},

        {"name":"ROSE_BRONZE", "primary":"7A3943", "secondary":"D97768", "highlight":"F1B1A5", "white_gold":"FFF7F4", "accent":"E8A445"},
        {"name":"CHAMPAGNE_IVORY", "primary":"85734D", "secondary":"D7B96A", "highlight":"FFF1C7", "white_gold":"FFFFFA", "accent":"B99A59"},
        {"name":"COPPER_PLATINUM", "primary":"724136", "secondary":"C89A87", "highlight":"F1D3C4", "white_gold":"FFF9F5", "accent":"D1B5A0"},
        {"name":"WARM_SILVER", "primary":"6B625A", "secondary":"BCAEA0", "highlight":"E8D9CC", "white_gold":"FFFDF9", "accent":"D4B58B"},
        {"name":"BLACK_GOLD_CRIMSON", "primary":"7D1515", "secondary":"D7A11E", "highlight":"FFE7A0", "white_gold":"FFFFFF", "accent":"FF4A3D"},
        {"name":"MIDNIGHT_BRASS", "primary":"5A5140", "secondary":"C7A24E", "highlight":"FFE09A", "white_gold":"FFF7E1", "accent":"F06C3B"},
        {"name":"ROYAL_COPPER", "primary":"6B2045", "secondary":"D27839", "highlight":"F1B77A", "white_gold":"FFF4E9", "accent":"C5B2FF"},
        {"name":"EMBER_CHAMPAGNE", "primary":"8F301D", "secondary":"F3B46A", "highlight":"FFE8B8", "white_gold":"FFFFFF", "accent":"FF5C39"},
    ],
    "living_particles": [
        {"name":"EMERALD_SEA_GREEN", "deep":"0C5A43", "mid":"22B87B", "bright":"67F0C0", "highlight":"E8FFF7"},
        {"name":"TURQUOISE_AQUA", "deep":"0B4E55", "mid":"1DC7C0", "bright":"63F4EA", "highlight":"E9FFFF"},
        {"name":"JADE_LIME", "deep":"214F25", "mid":"61BB32", "bright":"B7F26A", "highlight":"F3FFE7"},
        {"name":"CYAN_MINT", "deep":"0A4D63", "mid":"24C7D7", "bright":"8BFFE5", "highlight":"EFFFFF"},
        {"name":"PETROL_AQUA", "deep":"063944", "mid":"117F91", "bright":"54E6E3", "highlight":"E6FFFF"},
        {"name":"SEAFOAM_EMERALD", "deep":"0F4C3A", "mid":"38C99A", "bright":"90F7C7", "highlight":"F1FFF9"},
        {"name":"DEEP_TEAL_SPECTRAL", "deep":"062D35", "mid":"177E89", "bright":"5DE7F5", "highlight":"EEFFFF"},
        {"name":"ALGAE_GREEN_AQUA", "deep":"21462C", "mid":"57B96D", "bright":"6DE9D0", "highlight":"EFFFF9"},
        {"name":"COBALT_ALGAE", "deep":"082A48", "mid":"1C88A9", "bright":"83E07B", "highlight":"F5FFF0"},
        {"name":"LIME_TURQUOISE", "deep":"234D2A", "mid":"8DCB38", "bright":"31E4CE", "highlight":"F1FFF8"},
        {"name":"ICE_CYAN_MINT", "deep":"073A4B", "mid":"56D8F0", "bright":"A8FFD9", "highlight":"FFFFFF"},
        {"name":"JADE_CHARTREUSE", "deep":"174526", "mid":"32BB67", "bright":"D0F24A", "highlight":"FAFFE3"},

        {"name":"MINT_CHARTREUSE", "deep":"0C4D3A", "mid":"2CE0A0", "bright":"D1FF4E", "highlight":"F4FFE0"},
        {"name":"CYAN_GOLDEN", "deep":"07384A", "mid":"25D8E8", "bright":"D8F45D", "highlight":"F8FFE8"},
        {"name":"FOREST_AQUA", "deep":"0D341F", "mid":"2CA76A", "bright":"56E6D1", "highlight":"EAFFF8"},
        {"name":"ICE_JADE", "deep":"062B36", "mid":"72E7FF", "bright":"B8FFD5", "highlight":"F2FFF9"},
        {"name":"DEEP_VIOLET_ALGAE", "deep":"17102B", "mid":"6949D8", "bright":"58F0B8", "highlight":"F0FFFA"},
        {"name":"EMBER_SEAFOAM", "deep":"2B1610", "mid":"B55A31", "bright":"63E8C3", "highlight":"FFF1E8"},
        {"name":"MAGENTA_PLANKTON", "deep":"2B0A25", "mid":"C94AB6", "bright":"5CF0E3", "highlight":"FFF1FC"},
        {"name":"LIME_CYAN_ABYSS", "deep":"0B2530", "mid":"9CD834", "bright":"28E8F1", "highlight":"F3FFE8"},
    ],
    "invisible_forces": [
        {"name":"CRIMSON_CADMIUM_GOLD", "deep":"4B0714", "primary":"C72536", "secondary":"FF5A1F", "highlight":"FFD34E"},
        {"name":"CRIMSON_ORANGE", "deep":"430B12", "primary":"C62E24", "secondary":"FF6B26", "highlight":"FFD166"},
        {"name":"DEEP_RED_AMBER", "deep":"3A0A0A", "primary":"A71D31", "secondary":"E85D2A", "highlight":"FFC857"},
        {"name":"HOT_ORANGE_YELLOW", "deep":"4A1007", "primary":"D53A0A", "secondary":"FF7A00", "highlight":"FFD84A"},
        {"name":"WARM_MONOCHROME", "deep":"24100D", "primary":"8B3A2D", "secondary":"C76435", "highlight":"FFD27A"},
        {"name":"SCARLET_COPPER", "deep":"3C0B12", "primary":"D13A2F", "secondary":"FF8354", "highlight":"FFE08A"},
        {"name":"VERMILION_PEACH_GOLD", "deep":"42120A", "primary":"E0481C", "secondary":"FF9C52", "highlight":"FFE6A6"},
        {"name":"BURGUNDY_AMBER", "deep":"25070E", "primary":"9E303A", "secondary":"D86A45", "highlight":"F4C36A"},
        {"name":"MAGENTA_RED_GOLD", "deep":"33091E", "primary":"C62C62", "secondary":"F04A35", "highlight":"FFD060"},
        {"name":"PLASMA_ORANGE", "deep":"3C1208", "primary":"D8470F", "secondary":"FF8A22", "highlight":"FFE27A"},
        {"name":"EMBER_GOLD", "deep":"351109", "primary":"B63A16", "secondary":"E78A24", "highlight":"FFD85C"},
        {"name":"RUST_YELLOW", "deep":"32140A", "primary":"9B4927", "secondary":"D77D2E", "highlight":"F5D66A"},

        {"name":"SCARLET_GOLD", "deep":"3A0610", "primary":"E12B3B", "secondary":"FF7F11", "highlight":"FFE36A"},
        {"name":"EMBER_CHAMPAGNE", "deep":"30120A", "primary":"C94B2D", "secondary":"FF9B54", "highlight":"FFE5B5"},
        {"name":"RUBY_COPPER", "deep":"31070B", "primary":"B61E4A", "secondary":"E66A32", "highlight":"FFD08A"},
        {"name":"FIREBRICK_GOLD", "deep":"3A0C06", "primary":"B52B20", "secondary":"F06B1F", "highlight":"FFD24A"},
        {"name":"CRIMSON_LIME_GOLD", "deep":"2A0A0E", "primary":"D82E44", "secondary":"B8D438", "highlight":"FFE58A"},
        {"name":"PURPLE_FIRE_GOLD", "deep":"210915", "primary":"B33B8D", "secondary":"FF5F25", "highlight":"FFD95C"},
        {"name":"BURNISHED_CYAN", "deep":"1D0B08", "primary":"B74D2D", "secondary":"2AD8CF", "highlight":"FFE0A3"},
        {"name":"HOT_MAGENTA_ORANGE", "deep":"28060D", "primary":"D82167", "secondary":"FF6A17", "highlight":"FFD34A"},
    ]
}

static func palette(family_id: String, palette_index: int, seed_value: int = 0) -> Dictionary:
    var family: String = _canonical_family(family_id)
    var entries: Array = PALETTES.get(family, PALETTES["geometric"])
    var idx: int = posmod(palette_index, entries.size())
    var result: Dictionary = entries[idx].duplicate(true)
    if seed_value != 0:
        _apply_seed_variant(result, family, seed_value, idx)
    return result

static func _apply_seed_variant(palette: Dictionary, family: String, seed_value: int, palette_index: int) -> void:
    # Controlled intra-palette variation: deterministic but now broad enough to
    # prevent a five-render review batch from collapsing into the same colorway.
    # The variant is a cosmetic hash of seed + selected palette, never simulation RNG.
    var variant: int = _mixed(seed_value, 601 + palette_index * 97) % 16
    var shifts: Array[float] = [-0.092, 0.0, 0.076, -0.054, 0.108, -0.080, 0.034, -0.026, 0.064, -0.116, 0.018, 0.098, -0.046, 0.052, -0.068, 0.086]
    var base_shift: float = shifts[variant]
    var family_scale: float = 1.0
    match family:
        "geometric": family_scale = 1.00
        "fractal": family_scale = 0.94
        "sacred_symmetry": family_scale = 0.16
        "living_particles": family_scale = 1.05
        "invisible_forces": family_scale = 0.26
        _: family_scale = 1.0

    var hue_shift: float = base_shift * family_scale
    var sat_scale: float = 1.0 + [-0.06, 0.04, 0.08, -0.02, 0.12, 0.06, -0.08, 0.10, 0.02, 0.14, -0.04, 0.09, -0.10, 0.05, 0.11, -0.03][variant]
    var value_scale: float = 1.0 + [-0.04, 0.02, 0.04, -0.03, 0.06, 0.01, -0.05, 0.03, 0.05, -0.02, 0.07, 0.02, -0.06, 0.04, 0.01, -0.01][variant]

    var roles: Array[String] = []
    match family:
        "geometric": roles = ["dominant", "secondary", "highlight"]
        "fractal": roles = ["indigo", "violet", "cyan", "highlight"]
        "sacred_symmetry": roles = ["primary", "secondary", "highlight", "white_gold", "accent"]
        "living_particles": roles = ["deep", "mid", "bright", "highlight"]
        "invisible_forces": roles = ["deep", "primary", "secondary", "highlight"]
        _: roles = []

    for i in range(roles.size()):
        var role: String = roles[i]
        if not palette.has(role):
            continue
        var role_hue_shift: float = hue_shift
        if role == "secondary":
            role_hue_shift *= -0.42
        elif role == "accent":
            role_hue_shift *= 0.72
        elif role == "highlight" or role == "white_gold":
            role_hue_shift *= 0.22
        var role_value: float = value_scale + float(i - roles.size() / 2) * 0.009
        palette[role] = _variant_color_hex(str(palette[role]), role_hue_shift, sat_scale, role_value)

    palette["palette_variant"] = variant
    palette["palette_variant_seed"] = seed_value
    palette["name"] = "%s V%02d" % [str(palette["name"]), variant]

static func _variant_color_hex(hex_value: String, hue_shift: float, sat_scale: float, value_scale: float) -> String:
    var color := Color(hex_value)
    var h: float = color.h
    var s: float = color.s
    var v: float = color.v
    var shifted := Color.from_hsv(fposmod(h + hue_shift, 1.0), clampf(s * sat_scale, 0.0, 1.0), clampf(v * value_scale, 0.0, 1.0), color.a)
    return shifted.to_html(false)

static func _mixed(seed_value: int, salt: int) -> int:
    var x: int = (int(seed_value) ^ int(salt * 374761393)) & 0x7fffffff
    x = int((x ^ (x >> 13)) * 1274126177) & 0x7fffffff
    x = int((x ^ (x >> 16)) * 2246822519) & 0x7fffffff
    x = int((x ^ (x >> 13)) * 3266489917) & 0x7fffffff
    return int(x ^ (x >> 16)) & 0x7fffffff

static func _canonical_family(family_id: String) -> String:
    match family_id:
        "geometric", "geometric_waves", "c11c_geometric_waves_v1": return "geometric"
        "fractal", "fractal_bloom", "c11c_fractal_bloom_v1": return "fractal"
        "sacred_symmetry", "kaleidoscope", "c11c_sacred_symmetry_v1": return "sacred_symmetry"
        "living_particles", "particle_flow", "c11c_living_particles_v1": return "living_particles"
        "invisible_forces", "vector_field", "c11c_invisible_forces_v1": return "invisible_forces"
        _: return "geometric"
