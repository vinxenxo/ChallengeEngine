extends RefCounted

## Deterministic airport-board / Matrix-like transition for Header line 2.
## C11-C v2.1.4: intentionally consumed via preload() so prototypes do not depend on global class registration order.

const CHARS: String = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/[]{}<>|+-_=.:*"
const PRIMARY_END: float = 0.39
const SCRAMBLE_IN_END: float = 0.50
const SECONDARY_END: float = 0.84
const SCRAMBLE_OUT_END: float = 0.95

var primary_text: String
var secondary_text: String
var seed_value: int

func _init(primary: String, secondary: String, seed: int) -> void:
    primary_text = primary
    secondary_text = secondary
    seed_value = seed

func display_at(frame_index: int, total_frames: int) -> Dictionary:
    var total: int = maxi(1, total_frames)
    var frame: int = posmod(frame_index, total)
    var u: float = float(frame) / float(total)
    if u < PRIMARY_END:
        return {"text": primary_text, "transition": false, "phase": u / PRIMARY_END}
    if u < SCRAMBLE_IN_END:
        var t_in: float = inverse_lerp(PRIMARY_END, SCRAMBLE_IN_END, u)
        return {"text": _scramble_blend(primary_text, secondary_text, t_in, frame), "transition": true, "phase": t_in}
    if u < SECONDARY_END:
        return {"text": secondary_text, "transition": false, "phase": inverse_lerp(SCRAMBLE_IN_END, SECONDARY_END, u)}
    if u < SCRAMBLE_OUT_END:
        var t_out: float = inverse_lerp(SECONDARY_END, SCRAMBLE_OUT_END, u)
        return {"text": _scramble_blend(secondary_text, primary_text, t_out, frame), "transition": true, "phase": t_out}
    return {"text": primary_text, "transition": false, "phase": inverse_lerp(SCRAMBLE_OUT_END, 1.0, u)}

func _scramble_blend(from_text: String, to_text: String, amount: float, frame_index: int) -> String:
    var width: int = maxi(from_text.length(), to_text.length())
    var out: String = ""
    var reveal: float = clampf(amount, 0.0, 1.0)
    for i in range(width):
        var a: String = from_text.substr(i, 1) if i < from_text.length() else " "
        var b: String = to_text.substr(i, 1) if i < to_text.length() else " "
        var threshold: float = float(i + 1) / float(width + 1)
        if a == " " and b == " ":
            out += " "
        elif reveal >= threshold + 0.10:
            out += b
        elif reveal <= threshold - 0.10:
            out += a
        else:
            out += _scramble_char(i, frame_index)
    return out.rstrip(" ")

func _scramble_char(index: int, frame_index: int) -> String:
    var h: int = _mixed(seed_value, index * 97 + frame_index * 13 + 31)
    return CHARS.substr(h % CHARS.length(), 1)

func _mixed(seed: int, salt: int) -> int:
    var x: int = (int(seed) ^ int(salt * 374761393)) & 0x7fffffff
    x = int((x ^ (x >> 13)) * 1274126177) & 0x7fffffff
    x = int((x ^ (x >> 16)) * 2246822519) & 0x7fffffff
    x = int((x ^ (x >> 13)) * 3266489917) & 0x7fffffff
    return int(x ^ (x >> 16)) & 0x7fffffff
