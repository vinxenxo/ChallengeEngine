class_name C11CDrillPaletteBank
extends RefCounted

## C11-C 2.9.0 — Visual Drill presentation palettes.
## Presentation-only. Palette selection is driven by the existing cosmetic variant.


const TRACKING_PALETTES := [
    {"name":"DEEP_OCEAN_COPPER", "background":"03101A", "accent":"40D9FF", "secondary":"FF8E61", "tertiary":"C9F4FF", "target":"F9FCFF", "target_soft":"CBEFFF", "text_primary":"FFD1BC", "text_secondary":"EFFBFF", "text_data":"CBEFFF", "rule":"4AA0B9", "counter":"07131A"},
    {"name":"MOSS_CORAL", "background":"07120C", "accent":"77E09B", "secondary":"FF786E", "tertiary":"D2FFE1", "target":"FAFFF8", "target_soft":"E7FFEF", "text_primary":"FFC3BC", "text_secondary":"F3FFF4", "text_data":"E7FFEF", "rule":"4D9B69", "counter":"0A190F"},
    {"name":"ROYAL_AMETHYST", "background":"0A0716", "accent":"6E7BFF", "secondary":"E99BFF", "tertiary":"D4D7FF", "target":"FBFAFF", "target_soft":"EEEFFF", "text_primary":"F6CFFF", "text_secondary":"F7F4FF", "text_data":"EEEFFF", "rule":"686D9E", "counter":"110C1F"},
    {"name":"SUNSET_INK", "background":"160A0A", "accent":"FFB347", "secondary":"FF5D8F", "tertiary":"FFE2B8", "target":"FFF9F4", "target_soft":"FFF0DA", "text_primary":"FFC5D6", "text_secondary":"FFF5EA", "text_data":"FFF0DA", "rule":"B96E4F", "counter":"1E0F0F"},
    {"name":"FROSTED_MINT", "background":"041312", "accent":"7CF7DE", "secondary":"A9B7FF", "tertiary":"D8FFF6", "target":"FFFFFF", "target_soft":"ECFFF9", "text_primary":"C8D1FF", "text_secondary":"F6FFFC", "text_data":"ECFFF9", "rule":"57B2A2", "counter":"081918"},
    {"name":"ELECTRIC_SAPPHIRE", "background":"040B1B", "accent":"3FA7FF", "secondary":"5AF0FF", "tertiary":"C8E1FF", "target":"F8FCFF", "target_soft":"E3F2FF", "text_primary":"B0F8FF", "text_secondary":"F1F9FF", "text_data":"E3F2FF", "rule":"3E82C7", "counter":"071322"},
    {"name":"POMEGRANATE_GOLD", "background":"160704", "accent":"FF496E", "secondary":"FFC64D", "tertiary":"FFD0D9", "target":"FFF9F6", "target_soft":"FFE9E0", "text_primary":"FFE19A", "text_secondary":"FFF4EE", "text_data":"FFE9E0", "rule":"B95A58", "counter":"1F0C0B"},
    {"name":"FOREST_VIOLET", "background":"081006", "accent":"6EDB77", "secondary":"A77BFF", "tertiary":"D6F8C8", "target":"FBFFF9", "target_soft":"E7F8DE", "text_primary":"D0B8FF", "text_secondary":"F5F8F0", "text_data":"E7F8DE", "rule":"4A9858", "counter":"0D180A"},
    {"name":"ARCTIC_INDIGO", "background":"070D19", "accent":"8ED1FF", "secondary":"7D7BFF", "tertiary":"D9EEFF", "target":"F9FCFF", "target_soft":"EAF5FF", "text_primary":"CECAFF", "text_secondary":"F2F8FF", "text_data":"EAF5FF", "rule":"5E8CAC", "counter":"0C1422"},
    {"name":"TANGERINE_AQUA", "background":"140B03", "accent":"FF9E42", "secondary":"37E2D0", "tertiary":"FFD8A8", "target":"FFFDF7", "target_soft":"FFEFD0", "text_primary":"B6FFF8", "text_secondary":"FFF5E4", "text_data":"FFEFD0", "rule":"B97B3D", "counter":"1C1006"},
    {"name":"HOT_PINK_CYAN", "background":"13050E", "accent":"FF4BBF", "secondary":"44F0F2", "tertiary":"FFC9EA", "target":"FFF9FD", "target_soft":"FFE9F7", "text_primary":"A7FFFF", "text_secondary":"FFF3FB", "text_data":"FFE9F7", "rule":"B24D91", "counter":"1B0A16"},
    {"name":"LIME_ULTRAMARINE", "background":"091003", "accent":"B7F04A", "secondary":"527BFF", "tertiary":"E8FFB6", "target":"FDFFF6", "target_soft":"EFFFD5", "text_primary":"BBC8FF", "text_secondary":"F8FDEB", "text_data":"EFFFD5", "rule":"8AA34A", "counter":"111804"},
    {"name":"STEEL_ROSE", "background":"0D1017", "accent":"D6E5FF", "secondary":"FF7AA8", "tertiary":"F0F5FF", "target":"FFFFFF", "target_soft":"F6F9FF", "text_primary":"FFD0E0", "text_secondary":"FBFDFF", "text_data":"F6F9FF", "rule":"8794AE", "counter":"141720"},
    {"name":"EMBER_TEAL", "background":"120905", "accent":"FF6B4F", "secondary":"31E8B0", "tertiary":"FFCFC2", "target":"FFF9F6", "target_soft":"FFE9E3", "text_primary":"B5FFE9", "text_secondary":"FFF3EE", "text_data":"FFE9E3", "rule":"B75C4D", "counter":"1A0D08"},
    {"name":"VIOLET_LIME", "background":"0C0712", "accent":"AF73FF", "secondary":"C8F04F", "tertiary":"E8D3FF", "target":"FFFDFF", "target_soft":"F2E8FF", "text_primary":"E7FFA0", "text_secondary":"FAF6FF", "text_data":"F2E8FF", "rule":"7A5CAD", "counter":"130C1A"},
    {"name":"MIDNIGHT_GOLD", "background":"0D0D08", "accent":"FFE06A", "secondary":"69A7FF", "tertiary":"FFF0A8", "target":"FFFFF7", "target_soft":"FFF6D0", "text_primary":"C7DCFF", "text_secondary":"FFF9E8", "text_data":"FFF6D0", "rule":"A4934C", "counter":"16150A"},
    {"name":"CRIMSON_ICE", "background":"14050A", "accent":"FF5578", "secondary":"73D9FF", "tertiary":"FFD0DC", "target":"FFF9FB", "target_soft":"F2EFFF", "text_primary":"BFEFFF", "text_secondary":"FFF3F6", "text_data":"F2EFFF", "rule":"B55A70", "counter":"1C0A10"},
    {"name":"AQUAMARINE_SUN", "background":"03110D", "accent":"46E0C1", "secondary":"FFD45A", "tertiary":"C7FFF0", "target":"FFFFFA", "target_soft":"E6FFF8", "text_primary":"FFE9A5", "text_secondary":"FFF9E8", "text_data":"E6FFF8", "rule":"4AA38F", "counter":"07180F"}
]

const SACCADE_PALETTES := [
    {"name":"ELECTRIC_SAPPHIRE", "background":"040B1B", "accent":"3FA7FF", "secondary":"5AF0FF", "tertiary":"C8E1FF", "target":"F8FCFF", "target_soft":"E3F2FF", "text_primary":"B0F8FF", "text_secondary":"F1F9FF", "text_data":"E3F2FF", "rule":"3E82C7", "counter":"071322"},
    {"name":"POMEGRANATE_GOLD", "background":"160704", "accent":"FF496E", "secondary":"FFC64D", "tertiary":"FFD0D9", "target":"FFF9F6", "target_soft":"FFE9E0", "text_primary":"FFE19A", "text_secondary":"FFF4EE", "text_data":"FFE9E0", "rule":"B95A58", "counter":"1F0C0B"},
    {"name":"FOREST_VIOLET", "background":"081006", "accent":"6EDB77", "secondary":"A77BFF", "tertiary":"D6F8C8", "target":"FBFFF9", "target_soft":"E7F8DE", "text_primary":"D0B8FF", "text_secondary":"F5F8F0", "text_data":"E7F8DE", "rule":"4A9858", "counter":"0D180A"},
    {"name":"ARCTIC_INDIGO", "background":"070D19", "accent":"8ED1FF", "secondary":"7D7BFF", "tertiary":"D9EEFF", "target":"F9FCFF", "target_soft":"EAF5FF", "text_primary":"CECAFF", "text_secondary":"F2F8FF", "text_data":"EAF5FF", "rule":"5E8CAC", "counter":"0C1422"},
    {"name":"TANGERINE_AQUA", "background":"140B03", "accent":"FF9E42", "secondary":"37E2D0", "tertiary":"FFD8A8", "target":"FFFDF7", "target_soft":"FFEFD0", "text_primary":"B6FFF8", "text_secondary":"FFF5E4", "text_data":"FFEFD0", "rule":"B97B3D", "counter":"1C1006"},
    {"name":"HOT_PINK_CYAN", "background":"13050E", "accent":"FF4BBF", "secondary":"44F0F2", "tertiary":"FFC9EA", "target":"FFF9FD", "target_soft":"FFE9F7", "text_primary":"A7FFFF", "text_secondary":"FFF3FB", "text_data":"FFE9F7", "rule":"B24D91", "counter":"1B0A16"},
    {"name":"LIME_ULTRAMARINE", "background":"091003", "accent":"B7F04A", "secondary":"527BFF", "tertiary":"E8FFB6", "target":"FDFFF6", "target_soft":"EFFFD5", "text_primary":"BBC8FF", "text_secondary":"F8FDEB", "text_data":"EFFFD5", "rule":"8AA34A", "counter":"111804"},
    {"name":"STEEL_ROSE", "background":"0D1017", "accent":"D6E5FF", "secondary":"FF7AA8", "tertiary":"F0F5FF", "target":"FFFFFF", "target_soft":"F6F9FF", "text_primary":"FFD0E0", "text_secondary":"FBFDFF", "text_data":"F6F9FF", "rule":"8794AE", "counter":"141720"},
    {"name":"EMBER_TEAL", "background":"120905", "accent":"FF6B4F", "secondary":"31E8B0", "tertiary":"FFCFC2", "target":"FFF9F6", "target_soft":"FFE9E3", "text_primary":"B5FFE9", "text_secondary":"FFF3EE", "text_data":"FFE9E3", "rule":"B75C4D", "counter":"1A0D08"},
    {"name":"VIOLET_LIME", "background":"0C0712", "accent":"AF73FF", "secondary":"C8F04F", "tertiary":"E8D3FF", "target":"FFFDFF", "target_soft":"F2E8FF", "text_primary":"E7FFA0", "text_secondary":"FAF6FF", "text_data":"F2E8FF", "rule":"7A5CAD", "counter":"130C1A"},
    {"name":"MIDNIGHT_GOLD", "background":"0D0D08", "accent":"FFE06A", "secondary":"69A7FF", "tertiary":"FFF0A8", "target":"FFFFF7", "target_soft":"FFF6D0", "text_primary":"C7DCFF", "text_secondary":"FFF9E8", "text_data":"FFF6D0", "rule":"A4934C", "counter":"16150A"},
    {"name":"CRIMSON_ICE", "background":"14050A", "accent":"FF5578", "secondary":"73D9FF", "tertiary":"FFD0DC", "target":"FFF9FB", "target_soft":"F2EFFF", "text_primary":"BFEFFF", "text_secondary":"FFF3F6", "text_data":"F2EFFF", "rule":"B55A70", "counter":"1C0A10"},
    {"name":"AQUAMARINE_SUN", "background":"03110D", "accent":"46E0C1", "secondary":"FFD45A", "tertiary":"C7FFF0", "target":"FFFFFA", "target_soft":"E6FFF8", "text_primary":"FFE9A5", "text_secondary":"FFF9E8", "text_data":"E6FFF8", "rule":"4AA38F", "counter":"07180F"},
    {"name":"DEEP_OCEAN_COPPER", "background":"03101A", "accent":"40D9FF", "secondary":"FF8E61", "tertiary":"C9F4FF", "target":"F9FCFF", "target_soft":"CBEFFF", "text_primary":"FFD1BC", "text_secondary":"EFFBFF", "text_data":"CBEFFF", "rule":"4AA0B9", "counter":"07131A"},
    {"name":"MOSS_CORAL", "background":"07120C", "accent":"77E09B", "secondary":"FF786E", "tertiary":"D2FFE1", "target":"FAFFF8", "target_soft":"E7FFEF", "text_primary":"FFC3BC", "text_secondary":"F3FFF4", "text_data":"E7FFEF", "rule":"4D9B69", "counter":"0A190F"},
    {"name":"ROYAL_AMETHYST", "background":"0A0716", "accent":"6E7BFF", "secondary":"E99BFF", "tertiary":"D4D7FF", "target":"FBFAFF", "target_soft":"EEEFFF", "text_primary":"F6CFFF", "text_secondary":"F7F4FF", "text_data":"EEEFFF", "rule":"686D9E", "counter":"110C1F"},
    {"name":"SUNSET_INK", "background":"160A0A", "accent":"FFB347", "secondary":"FF5D8F", "tertiary":"FFE2B8", "target":"FFF9F4", "target_soft":"FFF0DA", "text_primary":"FFC5D6", "text_secondary":"FFF5EA", "text_data":"FFF0DA", "rule":"B96E4F", "counter":"1E0F0F"},
    {"name":"FROSTED_MINT", "background":"041312", "accent":"7CF7DE", "secondary":"A9B7FF", "tertiary":"D8FFF6", "target":"FFFFFF", "target_soft":"ECFFF9", "text_primary":"C8D1FF", "text_secondary":"F6FFFC", "text_data":"ECFFF9", "rule":"57B2A2", "counter":"081918"}
]

const PURSUIT_PALETTES := [
    {"name":"TANGERINE_AQUA", "background":"140B03", "accent":"FF9E42", "secondary":"37E2D0", "tertiary":"FFD8A8", "target":"FFFDF7", "target_soft":"FFEFD0", "text_primary":"B6FFF8", "text_secondary":"FFF5E4", "text_data":"FFEFD0", "rule":"B97B3D", "counter":"1C1006"},
    {"name":"HOT_PINK_CYAN", "background":"13050E", "accent":"FF4BBF", "secondary":"44F0F2", "tertiary":"FFC9EA", "target":"FFF9FD", "target_soft":"FFE9F7", "text_primary":"A7FFFF", "text_secondary":"FFF3FB", "text_data":"FFE9F7", "rule":"B24D91", "counter":"1B0A16"},
    {"name":"LIME_ULTRAMARINE", "background":"091003", "accent":"B7F04A", "secondary":"527BFF", "tertiary":"E8FFB6", "target":"FDFFF6", "target_soft":"EFFFD5", "text_primary":"BBC8FF", "text_secondary":"F8FDEB", "text_data":"EFFFD5", "rule":"8AA34A", "counter":"111804"},
    {"name":"STEEL_ROSE", "background":"0D1017", "accent":"D6E5FF", "secondary":"FF7AA8", "tertiary":"F0F5FF", "target":"FFFFFF", "target_soft":"F6F9FF", "text_primary":"FFD0E0", "text_secondary":"FBFDFF", "text_data":"F6F9FF", "rule":"8794AE", "counter":"141720"},
    {"name":"EMBER_TEAL", "background":"120905", "accent":"FF6B4F", "secondary":"31E8B0", "tertiary":"FFCFC2", "target":"FFF9F6", "target_soft":"FFE9E3", "text_primary":"B5FFE9", "text_secondary":"FFF3EE", "text_data":"FFE9E3", "rule":"B75C4D", "counter":"1A0D08"},
    {"name":"VIOLET_LIME", "background":"0C0712", "accent":"AF73FF", "secondary":"C8F04F", "tertiary":"E8D3FF", "target":"FFFDFF", "target_soft":"F2E8FF", "text_primary":"E7FFA0", "text_secondary":"FAF6FF", "text_data":"F2E8FF", "rule":"7A5CAD", "counter":"130C1A"},
    {"name":"MIDNIGHT_GOLD", "background":"0D0D08", "accent":"FFE06A", "secondary":"69A7FF", "tertiary":"FFF0A8", "target":"FFFFF7", "target_soft":"FFF6D0", "text_primary":"C7DCFF", "text_secondary":"FFF9E8", "text_data":"FFF6D0", "rule":"A4934C", "counter":"16150A"},
    {"name":"CRIMSON_ICE", "background":"14050A", "accent":"FF5578", "secondary":"73D9FF", "tertiary":"FFD0DC", "target":"FFF9FB", "target_soft":"F2EFFF", "text_primary":"BFEFFF", "text_secondary":"FFF3F6", "text_data":"F2EFFF", "rule":"B55A70", "counter":"1C0A10"},
    {"name":"AQUAMARINE_SUN", "background":"03110D", "accent":"46E0C1", "secondary":"FFD45A", "tertiary":"C7FFF0", "target":"FFFFFA", "target_soft":"E6FFF8", "text_primary":"FFE9A5", "text_secondary":"FFF9E8", "text_data":"E6FFF8", "rule":"4AA38F", "counter":"07180F"},
    {"name":"DEEP_OCEAN_COPPER", "background":"03101A", "accent":"40D9FF", "secondary":"FF8E61", "tertiary":"C9F4FF", "target":"F9FCFF", "target_soft":"CBEFFF", "text_primary":"FFD1BC", "text_secondary":"EFFBFF", "text_data":"CBEFFF", "rule":"4AA0B9", "counter":"07131A"},
    {"name":"MOSS_CORAL", "background":"07120C", "accent":"77E09B", "secondary":"FF786E", "tertiary":"D2FFE1", "target":"FAFFF8", "target_soft":"E7FFEF", "text_primary":"FFC3BC", "text_secondary":"F3FFF4", "text_data":"E7FFEF", "rule":"4D9B69", "counter":"0A190F"},
    {"name":"ROYAL_AMETHYST", "background":"0A0716", "accent":"6E7BFF", "secondary":"E99BFF", "tertiary":"D4D7FF", "target":"FBFAFF", "target_soft":"EEEFFF", "text_primary":"F6CFFF", "text_secondary":"F7F4FF", "text_data":"EEEFFF", "rule":"686D9E", "counter":"110C1F"},
    {"name":"SUNSET_INK", "background":"160A0A", "accent":"FFB347", "secondary":"FF5D8F", "tertiary":"FFE2B8", "target":"FFF9F4", "target_soft":"FFF0DA", "text_primary":"FFC5D6", "text_secondary":"FFF5EA", "text_data":"FFF0DA", "rule":"B96E4F", "counter":"1E0F0F"},
    {"name":"FROSTED_MINT", "background":"041312", "accent":"7CF7DE", "secondary":"A9B7FF", "tertiary":"D8FFF6", "target":"FFFFFF", "target_soft":"ECFFF9", "text_primary":"C8D1FF", "text_secondary":"F6FFFC", "text_data":"ECFFF9", "rule":"57B2A2", "counter":"081918"},
    {"name":"ELECTRIC_SAPPHIRE", "background":"040B1B", "accent":"3FA7FF", "secondary":"5AF0FF", "tertiary":"C8E1FF", "target":"F8FCFF", "target_soft":"E3F2FF", "text_primary":"B0F8FF", "text_secondary":"F1F9FF", "text_data":"E3F2FF", "rule":"3E82C7", "counter":"071322"},
    {"name":"POMEGRANATE_GOLD", "background":"160704", "accent":"FF496E", "secondary":"FFC64D", "tertiary":"FFD0D9", "target":"FFF9F6", "target_soft":"FFE9E0", "text_primary":"FFE19A", "text_secondary":"FFF4EE", "text_data":"FFE9E0", "rule":"B95A58", "counter":"1F0C0B"},
    {"name":"FOREST_VIOLET", "background":"081006", "accent":"6EDB77", "secondary":"A77BFF", "tertiary":"D6F8C8", "target":"FBFFF9", "target_soft":"E7F8DE", "text_primary":"D0B8FF", "text_secondary":"F5F8F0", "text_data":"E7F8DE", "rule":"4A9858", "counter":"0D180A"},
    {"name":"ARCTIC_INDIGO", "background":"070D19", "accent":"8ED1FF", "secondary":"7D7BFF", "tertiary":"D9EEFF", "target":"F9FCFF", "target_soft":"EAF5FF", "text_primary":"CECAFF", "text_secondary":"F2F8FF", "text_data":"EAF5FF", "rule":"5E8CAC", "counter":"0C1422"}
]

const PERIPHERAL_PALETTES := [
    {"name":"EMBER_TEAL", "background":"120905", "accent":"FF6B4F", "secondary":"31E8B0", "tertiary":"FFCFC2", "target":"FFF9F6", "target_soft":"FFE9E3", "text_primary":"B5FFE9", "text_secondary":"FFF3EE", "text_data":"FFE9E3", "rule":"B75C4D", "counter":"1A0D08"},
    {"name":"VIOLET_LIME", "background":"0C0712", "accent":"AF73FF", "secondary":"C8F04F", "tertiary":"E8D3FF", "target":"FFFDFF", "target_soft":"F2E8FF", "text_primary":"E7FFA0", "text_secondary":"FAF6FF", "text_data":"F2E8FF", "rule":"7A5CAD", "counter":"130C1A"},
    {"name":"MIDNIGHT_GOLD", "background":"0D0D08", "accent":"FFE06A", "secondary":"69A7FF", "tertiary":"FFF0A8", "target":"FFFFF7", "target_soft":"FFF6D0", "text_primary":"C7DCFF", "text_secondary":"FFF9E8", "text_data":"FFF6D0", "rule":"A4934C", "counter":"16150A"},
    {"name":"CRIMSON_ICE", "background":"14050A", "accent":"FF5578", "secondary":"73D9FF", "tertiary":"FFD0DC", "target":"FFF9FB", "target_soft":"F2EFFF", "text_primary":"BFEFFF", "text_secondary":"FFF3F6", "text_data":"F2EFFF", "rule":"B55A70", "counter":"1C0A10"},
    {"name":"AQUAMARINE_SUN", "background":"03110D", "accent":"46E0C1", "secondary":"FFD45A", "tertiary":"C7FFF0", "target":"FFFFFA", "target_soft":"E6FFF8", "text_primary":"FFE9A5", "text_secondary":"FFF9E8", "text_data":"E6FFF8", "rule":"4AA38F", "counter":"07180F"},
    {"name":"DEEP_OCEAN_COPPER", "background":"03101A", "accent":"40D9FF", "secondary":"FF8E61", "tertiary":"C9F4FF", "target":"F9FCFF", "target_soft":"CBEFFF", "text_primary":"FFD1BC", "text_secondary":"EFFBFF", "text_data":"CBEFFF", "rule":"4AA0B9", "counter":"07131A"},
    {"name":"MOSS_CORAL", "background":"07120C", "accent":"77E09B", "secondary":"FF786E", "tertiary":"D2FFE1", "target":"FAFFF8", "target_soft":"E7FFEF", "text_primary":"FFC3BC", "text_secondary":"F3FFF4", "text_data":"E7FFEF", "rule":"4D9B69", "counter":"0A190F"},
    {"name":"ROYAL_AMETHYST", "background":"0A0716", "accent":"6E7BFF", "secondary":"E99BFF", "tertiary":"D4D7FF", "target":"FBFAFF", "target_soft":"EEEFFF", "text_primary":"F6CFFF", "text_secondary":"F7F4FF", "text_data":"EEEFFF", "rule":"686D9E", "counter":"110C1F"},
    {"name":"SUNSET_INK", "background":"160A0A", "accent":"FFB347", "secondary":"FF5D8F", "tertiary":"FFE2B8", "target":"FFF9F4", "target_soft":"FFF0DA", "text_primary":"FFC5D6", "text_secondary":"FFF5EA", "text_data":"FFF0DA", "rule":"B96E4F", "counter":"1E0F0F"},
    {"name":"FROSTED_MINT", "background":"041312", "accent":"7CF7DE", "secondary":"A9B7FF", "tertiary":"D8FFF6", "target":"FFFFFF", "target_soft":"ECFFF9", "text_primary":"C8D1FF", "text_secondary":"F6FFFC", "text_data":"ECFFF9", "rule":"57B2A2", "counter":"081918"},
    {"name":"ELECTRIC_SAPPHIRE", "background":"040B1B", "accent":"3FA7FF", "secondary":"5AF0FF", "tertiary":"C8E1FF", "target":"F8FCFF", "target_soft":"E3F2FF", "text_primary":"B0F8FF", "text_secondary":"F1F9FF", "text_data":"E3F2FF", "rule":"3E82C7", "counter":"071322"},
    {"name":"POMEGRANATE_GOLD", "background":"160704", "accent":"FF496E", "secondary":"FFC64D", "tertiary":"FFD0D9", "target":"FFF9F6", "target_soft":"FFE9E0", "text_primary":"FFE19A", "text_secondary":"FFF4EE", "text_data":"FFE9E0", "rule":"B95A58", "counter":"1F0C0B"},
    {"name":"FOREST_VIOLET", "background":"081006", "accent":"6EDB77", "secondary":"A77BFF", "tertiary":"D6F8C8", "target":"FBFFF9", "target_soft":"E7F8DE", "text_primary":"D0B8FF", "text_secondary":"F5F8F0", "text_data":"E7F8DE", "rule":"4A9858", "counter":"0D180A"},
    {"name":"ARCTIC_INDIGO", "background":"070D19", "accent":"8ED1FF", "secondary":"7D7BFF", "tertiary":"D9EEFF", "target":"F9FCFF", "target_soft":"EAF5FF", "text_primary":"CECAFF", "text_secondary":"F2F8FF", "text_data":"EAF5FF", "rule":"5E8CAC", "counter":"0C1422"},
    {"name":"TANGERINE_AQUA", "background":"140B03", "accent":"FF9E42", "secondary":"37E2D0", "tertiary":"FFD8A8", "target":"FFFDF7", "target_soft":"FFEFD0", "text_primary":"B6FFF8", "text_secondary":"FFF5E4", "text_data":"FFEFD0", "rule":"B97B3D", "counter":"1C1006"},
    {"name":"HOT_PINK_CYAN", "background":"13050E", "accent":"FF4BBF", "secondary":"44F0F2", "tertiary":"FFC9EA", "target":"FFF9FD", "target_soft":"FFE9F7", "text_primary":"A7FFFF", "text_secondary":"FFF3FB", "text_data":"FFE9F7", "rule":"B24D91", "counter":"1B0A16"},
    {"name":"LIME_ULTRAMARINE", "background":"091003", "accent":"B7F04A", "secondary":"527BFF", "tertiary":"E8FFB6", "target":"FDFFF6", "target_soft":"EFFFD5", "text_primary":"BBC8FF", "text_secondary":"F8FDEB", "text_data":"EFFFD5", "rule":"8AA34A", "counter":"111804"},
    {"name":"STEEL_ROSE", "background":"0D1017", "accent":"D6E5FF", "secondary":"FF7AA8", "tertiary":"F0F5FF", "target":"FFFFFF", "target_soft":"F6F9FF", "text_primary":"FFD0E0", "text_secondary":"FBFDFF", "text_data":"F6F9FF", "rule":"8794AE", "counter":"141720"}
]

static func tracking(variant: float) -> Dictionary:
    return _from_variant(TRACKING_PALETTES, variant)

static func saccade(variant: float) -> Dictionary:
    return _from_variant(SACCADE_PALETTES, variant)

static func pursuit(variant: float) -> Dictionary:
    return _from_variant(PURSUIT_PALETTES, variant)

static func peripheral_scan(variant: float) -> Dictionary:
    return _from_variant(PERIPHERAL_PALETTES, variant)

static func count_for(family: String) -> int:
    match family:
        "tracking": return TRACKING_PALETTES.size()
        "saccade": return SACCADE_PALETTES.size()
        "pursuit": return PURSUIT_PALETTES.size()
        "peripheral_scan": return PERIPHERAL_PALETTES.size()
        _: return 0

static func _from_variant(entries: Array, variant: float) -> Dictionary:
    var normalized: float = clampf(variant, 0.0, 0.999999)
    var index: int = mini(entries.size() - 1, int(floor(normalized * float(entries.size()))))
    return entries[index].duplicate(true)
