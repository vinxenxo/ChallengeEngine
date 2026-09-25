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
    {"name":"AQUAMARINE_SUN", "background":"03110D", "accent":"46E0C1", "secondary":"FFD45A", "tertiary":"C7FFF0", "target":"FFFFFA", "target_soft":"E6FFF8", "text_primary":"FFE9A5", "text_secondary":"FFF9E8", "text_data":"E6FFF8", "rule":"4AA38F", "counter":"07180F"},
    {"name":"DEEP_AZURE_CORAL", "background":"031322", "accent":"3CE5FF", "secondary":"FF755F", "tertiary":"BDEFFF", "target":"F8FFFF", "target_soft":"CDEFFF", "text_primary":"FFC2B8", "text_secondary":"F0FCFF", "text_data":"CDEFFF", "rule":"3D93A8", "counter":"071B29"},
    {"name":"PLASMA_VIOLET_MINT", "background":"10071A", "accent":"B96BFF", "secondary":"61F1C5", "tertiary":"E5C8FF", "target":"FFFBFF", "target_soft":"F4E5FF", "text_primary":"9FFFF0", "text_secondary":"FAF6FF", "text_data":"F4E5FF", "rule":"7A5FA6", "counter":"170D24"},
    {"name":"POLAR_GOLD_INDIGO", "background":"080C1D", "accent":"FFDA62", "secondary":"667CFF", "tertiary":"FFF0AD", "target":"FFFFFA", "target_soft":"F4F0D0", "text_primary":"C5D0FF", "text_secondary":"FFFBEA", "text_data":"F4F0D0", "rule":"A28F51", "counter":"0E132B"},
    {"name":"ACID_CYAN_MAGENTA", "background":"070F12", "accent":"55F7D1", "secondary":"F05BFF", "tertiary":"B7FFF0", "target":"FFFFFF", "target_soft":"D9FFF6", "text_primary":"F8B7FF", "text_secondary":"F2FFFB", "text_data":"D9FFF6", "rule":"46A88F", "counter":"0D171A"},
    {"name":"COPPER_ICE_NAVY", "background":"0A0E18", "accent":"E88A57", "secondary":"79D9FF", "tertiary":"FFD5BF", "target":"FFFDFB", "target_soft":"E2F5FF", "text_primary":"CDEEFF", "text_secondary":"FFF6EF", "text_data":"E2F5FF", "rule":"8B6954", "counter":"101621"},
    {"name":"NOCTURNAL_LIME_ROSE", "background":"0A100A", "accent":"A8F04C", "secondary":"FF668F", "tertiary":"DFFFBE", "target":"FCFFF8", "target_soft":"EEFFD8", "text_primary":"FFC0D2", "text_secondary":"F7FFEF", "text_data":"EEFFD8", "rule":"729B4A", "counter":"101710"}
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
    {"name":"FROSTED_MINT", "background":"041312", "accent":"7CF7DE", "secondary":"A9B7FF", "tertiary":"D8FFF6", "target":"FFFFFF", "target_soft":"ECFFF9", "text_primary":"C8D1FF", "text_secondary":"F6FFFC", "text_data":"ECFFF9", "rule":"57B2A2", "counter":"081918"},
    {"name":"SIGNAL_RED_CYAN", "background":"150609", "accent":"FF4D58", "secondary":"36E8F2", "tertiary":"FFC7CC", "target":"FFFDFD", "target_soft":"FFE6E8", "text_primary":"9AFBFF", "text_secondary":"FFF4F4", "text_data":"FFE6E8", "rule":"AE505A", "counter":"1C0B0F"},
    {"name":"LASER_ORANGE_ULTRAMARINE", "background":"120A04", "accent":"FF8C32", "secondary":"536DFF", "tertiary":"FFE0BF", "target":"FFFDF8", "target_soft":"FFF0D8", "text_primary":"C5D0FF", "text_secondary":"FFF7EE", "text_data":"FFF0D8", "rule":"AD7047", "counter":"1B1007"},
    {"name":"PHOTON_BLUE_VIOLET", "background":"070A18", "accent":"43D6FF", "secondary":"B86BFF", "tertiary":"BEEFFF", "target":"FBFFFF", "target_soft":"E8DEFF", "text_primary":"E2C8FF", "text_secondary":"F2FCFF", "text_data":"E8DEFF", "rule":"5C86A8", "counter":"0E1024"},
    {"name":"LIME_MAGENTA_FLASH", "background":"0D1005", "accent":"B6F43D", "secondary":"FF4FB6", "tertiary":"E7FFB6", "target":"FFFFFF", "target_soft":"F0FFD3", "text_primary":"FFC7EB", "text_secondary":"FAFFEE", "text_data":"F0FFD3", "rule":"7B9B44", "counter":"161A08"},
    {"name":"WHITE_AMBER_CARBON", "background":"101113", "accent":"FFF5D6", "secondary":"FFB53D", "tertiary":"FFFFFF", "target":"FFFFFF", "target_soft":"F9F1DD", "text_primary":"FFD48A", "text_secondary":"FAFAFA", "text_data":"F9F1DD", "rule":"9A7D49", "counter":"18191C"},
    {"name":"ROYAL_CYAN_CRIMSON", "background":"0A0A18", "accent":"64DFFF", "secondary":"FF5368", "tertiary":"C9F5FF", "target":"FFFFFF", "target_soft":"E7F9FF", "text_primary":"FFC4CC", "text_secondary":"F1FCFF", "text_data":"E7F9FF", "rule":"517E9E", "counter":"111124"}
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
    {"name":"ARCTIC_INDIGO", "background":"070D19", "accent":"8ED1FF", "secondary":"7D7BFF", "tertiary":"D9EEFF", "target":"F9FCFF", "target_soft":"EAF5FF", "text_primary":"CECAFF", "text_secondary":"F2F8FF", "text_data":"EAF5FF", "rule":"5E8CAC", "counter":"0C1422"},
    {"name":"DEEP_VIOLET_GOLD", "background":"0B0715", "accent":"AF80FF", "secondary":"F4C75F", "tertiary":"E4D2FF", "target":"FFFEFF", "target_soft":"F1E7FF", "text_primary":"FFE3A0", "text_secondary":"FAF6FF", "text_data":"F1E7FF", "rule":"80629C", "counter":"130D20"},
    {"name":"OCEAN_ROSE", "background":"061118", "accent":"4EDBFF", "secondary":"FF7698", "tertiary":"C3F1FF", "target":"FAFFFF", "target_soft":"E2F7FF", "text_primary":"FFC8D5", "text_secondary":"F2FDFF", "text_data":"E2F7FF", "rule":"4A8EA4", "counter":"0C1820"},
    {"name":"MOSS_MAGENTA", "background":"091008", "accent":"78E36B", "secondary":"F06BFF", "tertiary":"D4FFD0", "target":"FBFFFA", "target_soft":"E7FBE4", "text_primary":"F6BCFF", "text_secondary":"F5FFF2", "text_data":"E7FBE4", "rule":"4C9B52", "counter":"101810"},
    {"name":"EMBER_AZURE", "background":"160806", "accent":"FF7148", "secondary":"57B9FF", "tertiary":"FFD0BF", "target":"FFF9F6", "target_soft":"FFE9E0", "text_primary":"BEE5FF", "text_secondary":"FFF1EA", "text_data":"FFE9E0", "rule":"AF5F4C", "counter":"1D0C09"},
    {"name":"ICE_VERMILION", "background":"071217", "accent":"70E7FF", "secondary":"FF6257", "tertiary":"C8F6FF", "target":"FFFFFF", "target_soft":"E5FAFF", "text_primary":"FFD0CC", "text_secondary":"F4FDFF", "text_data":"E5FAFF", "rule":"4B96A7", "counter":"0D1B22"},
    {"name":"AURORA_INDIGO", "background":"060A14", "accent":"65FFC7", "secondary":"8A76FF", "tertiary":"C8FFE9", "target":"FBFFFE", "target_soft":"E4FFF4", "text_primary":"C8C1FF", "text_secondary":"F1FFF9", "text_data":"E4FFF4", "rule":"4F9E84", "counter":"0D1320"}
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
    {"name":"STEEL_ROSE", "background":"0D1017", "accent":"D6E5FF", "secondary":"FF7AA8", "tertiary":"F0F5FF", "target":"FFFFFF", "target_soft":"F6F9FF", "text_primary":"FFD0E0", "text_secondary":"FBFDFF", "text_data":"F6F9FF", "rule":"8794AE", "counter":"141720"},
    {"name":"SOLAR_CYAN", "background":"061217", "accent":"4EF1FF", "secondary":"FFD45C", "tertiary":"C5FAFF", "target":"FFFFFF", "target_soft":"E3FDFF", "text_primary":"FFE9A3", "text_secondary":"F0FDFF", "text_data":"E3FDFF", "rule":"4E9AA5", "counter":"0D1A22"},
    {"name":"ECLIPSE_ROSE", "background":"120711", "accent":"E66FFF", "secondary":"FF6F87", "tertiary":"E5C8FF", "target":"FFFCFF", "target_soft":"F1E6FF", "text_primary":"FFC6D1", "text_secondary":"FBF5FF", "text_data":"F1E6FF", "rule":"915A8F", "counter":"1B0D1A"},
    {"name":"RADIANT_GOLD_VIOLET", "background":"0E0A13", "accent":"FFD861", "secondary":"B07BFF", "tertiary":"FFF0AF", "target":"FFFFFC", "target_soft":"FFF4D2", "text_primary":"D8C1FF", "text_secondary":"FFF8E5", "text_data":"FFF4D2", "rule":"A18A51", "counter":"17121F"},
    {"name":"AQUA_ORANGE_STORM", "background":"07100F", "accent":"4AE8D4", "secondary":"FF9147", "tertiary":"C9FFF5", "target":"FFFFFB", "target_soft":"E7FFF7", "text_primary":"FFD1AF", "text_secondary":"F2FFF9", "text_data":"E7FFF7", "rule":"4A9D8F", "counter":"0D1816"},
    {"name":"LUNAR_GREEN_BLUE", "background":"07100C", "accent":"93F07A", "secondary":"63A9FF", "tertiary":"DFFFF2", "target":"FCFFFC", "target_soft":"ECFFF4", "text_primary":"C9DFFF", "text_secondary":"F2FFF5", "text_data":"ECFFF4", "rule":"5A9460", "counter":"101A12"},
    {"name":"HOT_COPPER_TEAL", "background":"130805", "accent":"FF7B4D", "secondary":"45D9C1", "tertiary":"FFD1C2", "target":"FFF9F6", "target_soft":"FFEAE3", "text_primary":"AFFFEF", "text_secondary":"FFF4EF", "text_data":"FFEAE3", "rule":"A95C4E", "counter":"1A0E09"}
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
