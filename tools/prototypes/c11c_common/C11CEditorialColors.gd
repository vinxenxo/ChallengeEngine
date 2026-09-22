class_name C11CEditorialColors
extends RefCounted

## C11-C editorial text/decor colors derived directly from each family's active palette.
## Presentation-only. No engine/core/simulation/C7 dependencies.

static func palette(family_id: String, palette: Dictionary) -> Dictionary:
    var primary: Color = Color("FFFFFF")
    var secondary: Color = Color("FFFFFF")
    var highlight: Color = Color("FFFFFF")

    match family_id:
        "geometric":
            primary = Color(str(palette["dominant"]))
            secondary = Color(str(palette["secondary"]))
            highlight = Color(str(palette["highlight"]))
        "fractal":
            primary = Color(str(palette["violet"]))
            secondary = Color(str(palette["cyan"]))
            highlight = Color(str(palette["highlight"]))
        "sacred_symmetry":
            primary = Color(str(palette["primary"]))
            secondary = Color(str(palette["accent"]))
            highlight = Color(str(palette["highlight"]))
        "living_particles":
            primary = Color(str(palette["mid"]))
            secondary = Color(str(palette["bright"]))
            highlight = Color(str(palette["highlight"]))
        "invisible_forces":
            primary = Color(str(palette["primary"]))
            secondary = Color(str(palette["secondary"]))
            highlight = Color(str(palette["highlight"]))
        _:
            primary = Color(str(palette.get("primary", "FFFFFF")))
            secondary = Color(str(palette.get("secondary", "FFFFFF")))
            highlight = Color(str(palette.get("highlight", "FFFFFF")))

    return {
        "header_math": secondary,
        "header_hook": primary,
        "footer_geek": secondary,
        "footer_data": highlight,
        "footer_palette": primary,
        "footer_signature": primary,
        "rule": secondary
    }
