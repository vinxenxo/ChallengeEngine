extends SceneTree

## C11-C 2.9.0 — Expanded semantic palette bank contract.

const PaletteBank = preload("res://tools/prototypes/c11c_common/C11CDrillPaletteBank.gd")

var failures: Array[String] = []

func _initialize() -> void:
    for family in ["tracking", "saccade", "pursuit", "peripheral_scan"]:
        _assert(PaletteBank.count_for(family) >= 18, "%s palette bank must contain at least 18 semantic palettes." % family)
        var names: Dictionary = {}
        for i in range(PaletteBank.count_for(family)):
            var variant: float = (float(i) + 0.25) / float(PaletteBank.count_for(family))
            var palette: Dictionary = _palette_for(family, variant)
            var name := str(palette.get("name", ""))
            names[name] = true
            _assert(palette.get("text_primary", "") != "", "%s palettes must include text_primary." % family)
            _assert(palette.get("text_secondary", "") != "", "%s palettes must include text_secondary." % family)
            _assert(palette.get("target", "") != "", "%s palettes must include target." % family)
        _assert(names.size() >= 18, "%s palette names must be unique." % family)
    if failures.is_empty():
        print("[C11C_DRILL_PALETTE_BANK_CONTRACT_SUITE] PASS")
        quit(0)
    else:
        for failure in failures:
            push_error(failure)
        print("[C11C_DRILL_PALETTE_BANK_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
        quit(1)

func _palette_for(family: String, variant: float) -> Dictionary:
    match family:
        "tracking": return PaletteBank.tracking(variant)
        "saccade": return PaletteBank.saccade(variant)
        "pursuit": return PaletteBank.pursuit(variant)
        "peripheral_scan": return PaletteBank.peripheral_scan(variant)
    return {}

func _assert(condition: bool, message: String) -> void:
    if not condition:
        failures.append(message)
