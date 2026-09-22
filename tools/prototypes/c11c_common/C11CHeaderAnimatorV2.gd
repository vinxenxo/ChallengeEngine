extends RefCounted

## C11-C editorial header animator R4.
## Deterministic Matrix / airport-board presentation shared by all five Visual Loop families.
## Presentation-only: no simulation, engine RNG or timing ownership.

const CHARS: String = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/[]{}<>|+-_=.:*"
const INTRO_END: float = 0.12
const MIDPOINT_IN_START: float = 0.44
const MIDPOINT_PEAK: float = 0.49
const MIDPOINT_HOLD_END: float = 0.51
const MIDPOINT_OUT_END: float = 0.56
const BOLD_EMBOLDEN: float = 0.70

var primary_text: String
var secondary_text: String
var seed_value: int

func _init(primary: String, secondary: String, seed: int) -> void:
    primary_text = primary
    secondary_text = secondary
    seed_value = seed

static func apply_bold(label: Label, embolden: float = BOLD_EMBOLDEN) -> Label:
    var base_font: Font = label.get_theme_default_font()
    var bold_font := FontVariation.new()
    bold_font.base_font = base_font
    bold_font.variation_embolden = embolden
    label.add_theme_font_override("font", bold_font)
    return label

static func wrap_two_lines(text: String, font: Font, font_size: int, max_width: float) -> String:
    var clean: String = text.strip_edges().replace("\r", "").replace("\n", " ")
    var words: PackedStringArray = clean.split(" ", false)
    if words.size() <= 1:
        return clean

    var measure_font := FontVariation.new()
    measure_font.base_font = font
    measure_font.variation_embolden = BOLD_EMBOLDEN

    # Exactly one word-boundary split. Choose the split whose two rendered lines
    # are both safe and as balanced as possible, with overflow heavily penalized.
    var best_break: int = 1
    var best_score: float = 1.0e30
    for i in range(1, words.size()):
        var left: String = " ".join(words.slice(0, i))
        var right: String = " ".join(words.slice(i))
        var left_width: float = measure_font.get_string_size(left, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size).x
        var right_width: float = measure_font.get_string_size(right, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size).x
        var max_line: float = maxf(left_width, right_width)
        var overflow: float = maxf(0.0, max_line - max_width)
        var balance: float = absf(left_width - right_width)
        var score: float = overflow * 100000.0 + balance
        if score < best_score:
            best_score = score
            best_break = i

    return " ".join(words.slice(0, best_break)) + "\n" + " ".join(words.slice(best_break))

func display_at(frame_index: int, total_frames: int) -> Dictionary:
    var total: int = maxi(1, total_frames)
    var frame: int = posmod(frame_index, total)
    var u: float = float(frame) / float(total)

    # Intro Matrix: both header blocks materialize through the same scramble style.
    if u < INTRO_END:
        var intro_t: float = inverse_lerp(0.0, INTRO_END, u)
        return {
            "line1_text": _reveal_text(primary_text, intro_t, frame, 11),
            "line2_text": _reveal_text(secondary_text, intro_t, frame, 29),
            "transition": true,
            "phase": intro_t,
            "mode": "intro"
        }

    if u < MIDPOINT_IN_START:
        return {
            "line1_text": primary_text,
            "line2_text": secondary_text,
            "transition": false,
            "phase": 0.0,
            "mode": "steady"
        }

    # Midpoint Matrix exchange: first header block receives the former second block,
    # while the second block receives the former first block. The visual exchange
    # reaches the swapped state at the midpoint, then resolves back to the canonical order.
    if u < MIDPOINT_PEAK:
        var in_t: float = inverse_lerp(MIDPOINT_IN_START, MIDPOINT_PEAK, u)
        return {
            "line1_text": _scramble_blend(primary_text, secondary_text, in_t, frame, 11),
            "line2_text": _scramble_blend(secondary_text, primary_text, in_t, frame, 29),
            "transition": true,
            "phase": in_t,
            "mode": "midpoint_exchange"
        }

    if u < MIDPOINT_HOLD_END:
        return {
            "line1_text": secondary_text,
            "line2_text": primary_text,
            "transition": false,
            "phase": 1.0,
            "mode": "midpoint_hold"
        }

    if u < MIDPOINT_OUT_END:
        var out_t: float = inverse_lerp(MIDPOINT_HOLD_END, MIDPOINT_OUT_END, u)
        return {
            "line1_text": _scramble_blend(secondary_text, primary_text, out_t, frame, 11),
            "line2_text": _scramble_blend(primary_text, secondary_text, out_t, frame, 29),
            "transition": true,
            "phase": out_t,
            "mode": "midpoint_return"
        }

    return {
        "line1_text": primary_text,
        "line2_text": secondary_text,
        "transition": false,
        "phase": 1.0,
        "mode": "steady"
    }

func _reveal_text(target_text: String, amount: float, frame_index: int, lane: int) -> String:
    var lines: PackedStringArray = target_text.split("\n", true)
    var out: Array[String] = []
    for line_index in range(lines.size()):
        out.append(_reveal_line(lines[line_index], amount, frame_index, lane + line_index * 53))
    return "\n".join(out)

func _reveal_line(target: String, amount: float, frame_index: int, salt: int) -> String:
    if target.is_empty():
        return target
    var out: String = ""
    var reveal: float = clampf(amount, 0.0, 1.0)
    var width: int = target.length()
    for i in range(width):
        var threshold: float = float(i + 1) / float(width + 2)
        if reveal >= threshold + 0.08:
            out += target.substr(i, 1)
        elif reveal <= threshold - 0.08:
            out += _scramble_char(i + salt, frame_index)
        else:
            out += _scramble_char(i + salt, frame_index + salt * 7)
    return out

func _scramble_blend(from_text: String, to_text: String, amount: float, frame_index: int, lane: int) -> String:
    var from_lines: PackedStringArray = from_text.split("\n", true)
    var to_lines: PackedStringArray = to_text.split("\n", true)
    var line_count: int = maxi(from_lines.size(), to_lines.size())
    var out_lines: Array[String] = []
    for line_index in range(line_count):
        var a: String = from_lines[line_index] if line_index < from_lines.size() else ""
        var b: String = to_lines[line_index] if line_index < to_lines.size() else ""
        out_lines.append(_scramble_line(a, b, amount, frame_index, lane + line_index * 53))
    return "\n".join(out_lines)

func _scramble_line(from_text: String, to_text: String, amount: float, frame_index: int, lane: int) -> String:
    var width: int = maxi(from_text.length(), to_text.length())
    if width == 0:
        return ""
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
            out += _scramble_char(i + lane, frame_index)
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
