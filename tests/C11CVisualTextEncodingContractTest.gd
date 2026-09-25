extends SceneTree

## C11-C 2.11.1 — editorial text encoding contract.
## No emoji is allowed in production copy; UTF-8 must preserve Spanish punctuation/accented text.

const HOOK_BANK := "res://profiles/presentation/c11c_visual_hooks.json"
const SOCIAL_WRITER := "res://tools/prototypes/c11c_common/write_social_metadata.py"

var failures: Array[String] = []

func _has_forbidden_emoji(text: String) -> bool:
    for i in text.length():
        var code := text.unicode_at(i)
        if (code >= 0x1F000 and code <= 0x1FAFF) or code == 0xFE0F or code == 0x200D:
            return true
    return false

func _initialize() -> void:
    _assert(FileAccess.file_exists(HOOK_BANK), "Visual hook bank must exist.")
    var raw := FileAccess.get_file_as_string(HOOK_BANK)
    _assert(not _has_forbidden_emoji(raw), "Hook bank must contain no emoji code points.")
    _assert(raw.find("¿") >= 0 and raw.find("ó") >= 0 and raw.find("ñ") >= 0, "Spanish Unicode characters must remain supported in editorial copy.")
    var writer := FileAccess.get_file_as_string(SOCIAL_WRITER)
    _assert(writer.find("encoding='utf-8'") >= 0, "Social writer must emit UTF-8 without BOM.")
    _assert(writer.find("FIXED_HASHTAGS = [\"#GenerativeArt\", \"#GodotEngine\", \"#LoopArt\", \"#OddlySatisfying\"]") >= 0, "Fixed hashtag bank must remain canonical.")
    _conclude()

func _assert(condition: bool, message: String) -> void:
    if not condition:
        failures.append(message)

func _conclude() -> void:
    if failures.is_empty():
        print("[C11C_VISUAL_TEXT_ENCODING_CONTRACT_SUITE] PASS")
        quit(0)
    else:
        for failure in failures:
            push_error(failure)
        print("[C11C_VISUAL_TEXT_ENCODING_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
        quit(1)
