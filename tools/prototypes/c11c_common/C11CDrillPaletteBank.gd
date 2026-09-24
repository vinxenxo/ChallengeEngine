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


const PURSUIT_PALETTES := [
    {"name":"VOID_CYAN","background":"020710","accent":"59E7FF","secondary":"8D7CFF","tertiary":"B7F5FF","target":"FFFFFF","target_soft":"E8FBFF","text_primary":"9BEFFF","text_secondary":"B7ADFF","text_data":"EEFCFF","rule":"378FA8","counter":"06131B"},
    {"name":"ASTRAL_VIOLET","background":"07040F","accent":"B485FF","secondary":"5CE1FF","tertiary":"F0CAFF","target":"FFF9FF","target_soft":"F1E7FF","text_primary":"D1B8FF","text_secondary":"A0EFFF","text_data":"FAF3FF","rule":"795BA6","counter":"120A1C"},
    {"name":"SOLAR_AMBER","background":"100803","accent":"FFB84A","secondary":"5EE5FF","tertiary":"FFE2A4","target":"FFFCF2","target_soft":"FFF0C8","text_primary":"FFD08C","text_secondary":"89EDFF","text_data":"FFF6E2","rule":"C79042","counter":"1A1005"},
    {"name":"DEEP_EMERALD","background":"020D0A","accent":"55F0B0","secondary":"6FD7FF","tertiary":"B8FFE0","target":"F5FFF9","target_soft":"E0FFF1","text_primary":"96FFD2","text_secondary":"9AE7FF","text_data":"F2FFF8","rule":"3C9F79","counter":"06160F"},
    {"name":"ION_BLUE","background":"020A16","accent":"5A9DFF","secondary":"4BF0FF","tertiary":"B8D7FF","target":"F8FCFF","target_soft":"E4F0FF","text_primary":"A0C7FF","text_secondary":"8DEEFF","text_data":"F2F8FF","rule":"3A73B5","counter":"07101D"},
    {"name":"PLASMA_ROSE","background":"10030C","accent":"FF68BD","secondary":"9A78FF","tertiary":"FFC2E6","target":"FFF8FC","target_soft":"FFE5F2","text_primary":"FF9ED4","text_secondary":"C8B7FF","text_data":"FFF0F8","rule":"BA558F","counter":"190A15"},
    {"name":"GLACIAL_MINT","background":"03110F","accent":"6FFFE3","secondary":"7C9BFF","tertiary":"C5FFF3","target":"F9FFFE","target_soft":"E5FFF9","text_primary":"A9FFED","text_secondary":"ACBCFF","text_data":"F3FFFC","rule":"48BFA7","counter":"071814"},
    {"name":"OBSIDIAN_LIME","background":"080D03","accent":"B9FF58","secondary":"48B5FF","tertiary":"E5FFB8","target":"FBFFF4","target_soft":"ECFFD4","text_primary":"D1FF8A","text_secondary":"96C9FF","text_data":"F6FFE8","rule":"8AAA43","counter":"101604"}
]

const PERIPHERAL_PALETTES := [
    {"name":"ECLIPSE_TEAL","background":"020B0C","accent":"62FFE1","secondary":"43A8FF","tertiary":"B7FFF1","target":"FAFFFE","target_soft":"E5FFF8","text_primary":"A4FFEF","text_secondary":"9ACFFF","text_data":"F2FFFC","rule":"398F87","counter":"061614"},
    {"name":"CORONA_GOLD","background":"100902","accent":"FFD05A","secondary":"FF7A4A","tertiary":"FFE9A8","target":"FFFDF4","target_soft":"FFF3C9","text_primary":"FFE08D","text_secondary":"FFB58D","text_data":"FFF7E2","rule":"C69D45","counter":"1B1104"},
    {"name":"SOLAR_VIOLET","background":"08030D","accent":"C18BFF","secondary":"FF5CC8","tertiary":"E7C9FF","target":"FFF9FF","target_soft":"F1E7FF","text_primary":"D8B7FF","text_secondary":"FF9BDA","text_data":"FBF2FF","rule":"8D5EB2","counter":"160A19"},
    {"name":"MAGNETIC_BLUE","background":"020915","accent":"66B4FF","secondary":"63FFE8","tertiary":"C4E3FF","target":"F9FDFF","target_soft":"E6F4FF","text_primary":"A9D7FF","text_secondary":"A2FFF0","text_data":"F2F9FF","rule":"4486BA","counter":"07121D"},
    {"name":"EMBER_ORBIT","background":"120603","accent":"FF754D","secondary":"FFCF4A","tertiary":"FFD0C0","target":"FFF8F4","target_soft":"FFE8DF","text_primary":"FFAA8F","text_secondary":"FFE08E","text_data":"FFF1EA","rule":"C36B54","counter":"1D0B06"},
    {"name":"AURORA_GREEN","background":"031008","accent":"70F09C","secondary":"83B8FF","tertiary":"C6FFD8","target":"F9FFF9","target_soft":"E5FFEB","text_primary":"A9FFBF","text_secondary":"B3D1FF","text_data":"F2FFF4","rule":"4BA66B","counter":"07150E"},
    {"name":"ULTRAVIOLET_NEON","background":"07040E","accent":"9E73FF","secondary":"5EEAFF","tertiary":"D6C6FF","target":"FCFAFF","target_soft":"EFE9FF","text_primary":"C5AEFF","text_secondary":"A1F3FF","text_data":"F8F4FF","rule":"7456AE","counter":"110A19"},
    {"name":"ICE_CORONA","background":"061019","accent":"A8E6FF","secondary":"8CF5CE","tertiary":"D8F7FF","target":"FFFFFF","target_soft":"ECFAFF","text_primary":"D0F1FF","text_secondary":"B2FFE2","text_data":"F7FCFF","rule":"6E9AB0","counter":"0B151C"}
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

static func pursuit(variant: float) -> Dictionary:
    return _from_variant(PURSUIT_PALETTES, variant)

static func peripheral_scan(variant: float) -> Dictionary:
    return _from_variant(PERIPHERAL_PALETTES, variant)

static func _from_variant(entries: Array, variant: float) -> Dictionary:
    var normalized: float = clampf(variant, 0.0, 0.999999)
    var index: int = mini(entries.size() - 1, int(floor(normalized * float(entries.size()))))
    return entries[index].duplicate(true)
