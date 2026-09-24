class_name C11CDrillPaletteBank
extends RefCounted

## C11-C 2.7.0 — Visual Drill presentation palettes.
## Presentation-only. Palette selection is driven by the existing cosmetic variant.

const TRACKING_PALETTES := [
    {"name":"CYAN_MAGENTA", "background":"030813", "accent":"16E6FF", "secondary":"FF3EBA", "target":"FFFFFF", "target_soft":"E8FDFF", "text_primary":"62F1FF", "text_secondary":"FFC0E7", "text_data":"E8FDFF", "rule":"2CB6D0", "counter":"06111A"},
    {"name":"BLUE_LILAC", "background":"050817", "accent":"4D7CFE", "secondary":"B98CFF", "target":"F7FBFF", "target_soft":"E8EEFF", "text_primary":"91AEFF", "text_secondary":"D5BEFF", "text_data":"F2F5FF", "rule":"6D86D9", "counter":"0A0C1D"},
    {"name":"TURQUOISE_ORCHID", "background":"031010", "accent":"28E0D1", "secondary":"E06BFF", "target":"FFFFFF", "target_soft":"E8FFFB", "text_primary":"67F1E7", "text_secondary":"E9B4FF", "text_data":"EEFFFD", "rule":"35BDB5", "counter":"071313"},
    {"name":"SPECTRAL_BLUE", "background":"04101A", "accent":"66D9FF", "secondary":"477BFF", "target":"F8FFFF", "target_soft":"E8F8FF", "text_primary":"9BE8FF", "text_secondary":"9AAFFF", "text_data":"EFFBFF", "rule":"59A9DA", "counter":"07131C"},
    {"name":"WARM_COLD", "background":"120B06", "accent":"FFB04A", "secondary":"37D7FF", "target":"FFFDF6", "target_soft":"FFF1D8", "text_primary":"FFD18B", "text_secondary":"7DE8FF", "text_data":"FFF4DE", "rule":"D99B4B", "counter":"1D1205"},
    {"name":"INDIGO_ROSE", "background":"0B0815", "accent":"8A6CFF", "secondary":"FF4F9A", "target":"FBF8FF", "target_soft":"F0EAFF", "text_primary":"BCAFFF", "text_secondary":"FF98C2", "text_data":"F6F0FF", "rule":"9279D9", "counter":"130B18"},
    {"name":"AQUA_ULTRAVIOLET", "background":"060611", "accent":"40F0EE", "secondary":"B86CFF", "target":"F8FFFF", "target_soft":"E7FFFF", "text_primary":"78F9F6", "text_secondary":"D3A8FF", "text_data":"F0FFFF", "rule":"4AC9C8", "counter":"0A0D16"},
    {"name":"SILVER_ICE", "background":"071019", "accent":"DDEAFF", "secondary":"79B9FF", "target":"FFFFFF", "target_soft":"EDF6FF", "text_primary":"EAF2FF", "text_secondary":"A9D2FF", "text_data":"FFFFFF", "rule":"9DBBE0", "counter":"0B111A"},
    {"name":"CORAL_VIOLET", "background":"120710", "accent":"FF6E7A", "secondary":"8A6CFF", "target":"FFF9FB", "target_soft":"FFE8EC", "text_primary":"FFACB4", "text_secondary":"BCAFFF", "text_data":"FFF2F4", "rule":"D17C86", "counter":"1A090F"},
    {"name":"MINT_FUCHSIA", "background":"04110D", "accent":"75F5D4", "secondary":"FF4FC7", "target":"FFFFFF", "target_soft":"E8FFF7", "text_primary":"A7FFE9", "text_secondary":"FF9CDE", "text_data":"F3FFF9", "rule":"63CFAF", "counter":"07150F"},
    {"name":"ACID_LIME_BLUE", "background":"091006", "accent":"B6FF4A", "secondary":"438CFF", "target":"FAFFF2", "target_soft":"EDFFD3", "text_primary":"D1FF7D", "text_secondary":"8FB5FF", "text_data":"F7FFE8", "rule":"9BCB4B", "counter":"0E1605"},
    {"name":"EMBER_AQUA", "background":"120806", "accent":"FF5A3D", "secondary":"22FFC8", "target":"FFF9F3", "target_soft":"FFEAE0", "text_primary":"FFAC98", "text_secondary":"72FFD9", "text_data":"FFF1E9", "rule":"D4745B", "counter":"1B0C07"}
]

const SACCADE_PALETTES := [
    {"name":"CYAN_MAGENTA", "background":"030813", "accent":"16E6FF", "secondary":"FF3EBA", "target":"FFFFFF", "target_soft":"E8FDFF", "counter":"06111A"},
    {"name":"BLUE_LILAC", "background":"050817", "accent":"4D7CFE", "secondary":"B98CFF", "target":"F7FBFF", "target_soft":"E8EEFF", "counter":"0A0C1D"},
    {"name":"TURQUOISE_ORCHID", "background":"031010", "accent":"28E0D1", "secondary":"E06BFF", "target":"FFFFFF", "target_soft":"E8FFFB", "counter":"071313"},
    {"name":"SPECTRAL_BLUE", "background":"04101A", "accent":"66D9FF", "secondary":"477BFF", "target":"F8FFFF", "target_soft":"E8F8FF", "counter":"07131C"},
    {"name":"WARM_COLD", "background":"120B06", "accent":"FFB04A", "secondary":"37D7FF", "target":"FFFDF6", "target_soft":"FFF1D8", "counter":"1D1205"},
    {"name":"INDIGO_ROSE", "background":"0B0815", "accent":"8A6CFF", "secondary":"FF4F9A", "target":"FBF8FF", "target_soft":"F0EAFF", "counter":"130B18"},
    {"name":"AQUA_ULTRAVIOLET", "background":"060611", "accent":"40F0EE", "secondary":"B86CFF", "target":"F8FFFF", "target_soft":"E7FFFF", "counter":"0A0D16"},
    {"name":"SILVER_ICE", "background":"071019", "accent":"DDEAFF", "secondary":"79B9FF", "target":"FFFFFF", "target_soft":"EDF6FF", "counter":"0B111A"},
    {"name":"CORAL_VIOLET", "background":"120710", "accent":"FF6E7A", "secondary":"8A6CFF", "target":"FFF9FB", "target_soft":"FFE8EC", "counter":"1A090F"},
    {"name":"MINT_FUCHSIA", "background":"04110D", "accent":"75F5D4", "secondary":"FF4FC7", "target":"FFFFFF", "target_soft":"E8FFF7", "counter":"07150F"},
    {"name":"ACID_LIME_BLUE", "background":"091006", "accent":"B6FF4A", "secondary":"438CFF", "target":"FAFFF2", "target_soft":"EDFFD3", "counter":"0E1605"},
    {"name":"EMBER_AQUA", "background":"120806", "accent":"FF5A3D", "secondary":"22FFC8", "target":"FFF9F3", "target_soft":"FFEAE0", "counter":"1B0C07"}
]

static func tracking(variant: float) -> Dictionary:
    return _from_variant(TRACKING_PALETTES, variant)

static func saccade(variant: float) -> Dictionary:
    return _from_variant(SACCADE_PALETTES, variant)

static func _from_variant(entries: Array, variant: float) -> Dictionary:
    var normalized: float = clampf(variant, 0.0, 0.999999)
    var index: int = mini(entries.size() - 1, int(floor(normalized * float(entries.size()))))
    return entries[index].duplicate(true)
