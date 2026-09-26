class_name C11CColorBoost
extends RefCounted

## C11-C 2.16.0 — mobile-vivid editorial palette transform.
## Presentation-only: increases chroma/value without changing palette identity.

static func vivid(c: Color, saturation_gain: float = 1.60, value_gain: float = 1.08) -> Color:
    if c.a <= 0.0:
        return c
    var s: float = clampf(c.s * saturation_gain, 0.0, 1.0)
    var v: float = clampf(c.v * value_gain, 0.0, 1.0)
    return Color.from_hsv(c.h, s, v, c.a)
