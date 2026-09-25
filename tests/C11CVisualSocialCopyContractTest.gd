extends SceneTree

## C11-C 2.11.1 — social copy format and hook-reuse contract.

const SOCIAL_WRITER := "res://tools/prototypes/c11c_common/write_social_metadata.py"
const HOOK_BANK := "res://profiles/presentation/c11c_visual_hooks.json"
const FAMILY_CATALOG := "res://profiles/presentation/c11c_visual_family_catalog.json"

var failures: Array[String] = []

func _initialize() -> void:
    var writer := FileAccess.get_file_as_string(SOCIAL_WRITER)
    _assert(not writer.is_empty(), "Social writer must exist.")
    _assert(writer.find("FIXED_HASHTAGS = [\"#GenerativeArt\", \"#GodotEngine\", \"#LoopArt\", \"#OddlySatisfying\"]") >= 0, "Fixed hashtag bank must be canonical and shared.")
    _assert(writer.find("**{display_name}**") >= 0, "Social copy must use the Markdown title format.")
    _assert(writer.find("- **Variante:**") >= 0, "Social copy must expose the variant field.")
    _assert(writer.find("- **Paleta:**") >= 0, "Social copy must expose the palette field.")
    _assert(writer.find("- **Seed:**") >= 0, "Social copy must expose the seed field.")
    _assert(writer.find("- **Detalles:**") >= 0, "Social copy must expose the details field.")
    _assert(writer.find("Diseñado en código con #GodotEngine") >= 0, "Social copy must contain the publication sentence.")
    _assert(writer.find("editorial.get('header_line_2'") >= 0, "Visual Loop social copy must reuse the rendered Header hook when available.")
    _assert(writer.find("loop_hook = line2 or '¿Puedes notar dónde termina el bucle?'") >= 0, "Visual Loop social copy must use an emoji-free deterministic fallback hook.")
    _assert(writer.find("encoding='utf-8'") >= 0, "Social writer must emit UTF-8 without BOM.")
    _assert(writer.find("música ambiental determinista") >= 0, "Public social copy must describe audio generically.")
    _assert(FileAccess.file_exists(HOOK_BANK), "Hook bank must exist.")
    _assert(FileAccess.file_exists(FAMILY_CATALOG), "Canonical family catalog must exist.")
    _conclude()

func _assert(condition: bool, message: String) -> void:
    if not condition:
        failures.append(message)

func _conclude() -> void:
    if failures.is_empty():
        print("[C11C_VISUAL_SOCIAL_COPY_CONTRACT_SUITE] PASS")
        quit(0)
    else:
        for failure in failures:
            push_error(failure)
        print("[C11C_VISUAL_SOCIAL_COPY_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
        quit(1)
