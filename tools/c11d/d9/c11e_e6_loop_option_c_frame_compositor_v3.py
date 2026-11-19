"""C11-E E6 Loop Option C V3: dependency-free D-owned RGB24 frame compositor.

One immutable RGB24 source frame in memory becomes one 720x1280 RGB24 frame.
The approved center rectangle is 504x896 at (108,192), with black header/footer
and side gutters. Downsampling uses exact rational pixel-area averaging implemented
with the Python standard library only. There are no imaging imports, file I/O, process
spawn, selector binding, E1 dispatch, audio, video or media behavior.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
from typing import Any

SCHEMA = "C11E-E6-LOOP-OPTION-C-FRAME-COMPOSITOR-V3"
RESAMPLER = "EXACT_RATIONAL_AREA_BOX_V1"
CANVAS_WIDTH = 720
CANVAS_HEIGHT = 1280
CONTENT_X = 108
CONTENT_Y = 192
CONTENT_WIDTH = 504
CONTENT_HEIGHT = 896
HEADER_HEIGHT = 192
FOOTER_Y = 1088
FOOTER_HEIGHT = 192
BACKGROUND_RGB = (0, 0, 0)
SOURCE_ASPECT_NUMERATOR = 9
SOURCE_ASPECT_DENOMINATOR = 16


class OptionCCompositionError(ValueError):
    """Raised when a source frame cannot satisfy the approved Option C contract."""


@dataclass(frozen=True)
class Rect:
    x: int
    y: int
    width: int
    height: int


@dataclass(frozen=True)
class CompositionPlan:
    schema: str
    source_width: int
    source_height: int
    source_pixel_format: str
    canvas_width: int
    canvas_height: int
    content_rect: Rect
    header_rect: Rect
    footer_rect: Rect
    left_gutter_rect: Rect
    right_gutter_rect: Rect
    scale: Fraction
    resampler: str
    crop: bool
    non_uniform_scaling: bool
    frame_order: str
    editorial_text_drawn: bool
    audio_or_media_created: bool

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["scale"] = f"{self.scale.numerator}/{self.scale.denominator}"
        return result


def _is_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def build_composition_plan(source_width: int, source_height: int) -> CompositionPlan:
    """Build a deterministic plan. Aspect mismatch, crop, distortion and upscale fail closed."""
    if not _is_int(source_width) or not _is_int(source_height):
        raise OptionCCompositionError("SOURCE_DIMENSIONS_MUST_BE_INTEGERS")
    if source_width <= 0 or source_height <= 0:
        raise OptionCCompositionError("SOURCE_DIMENSIONS_MUST_BE_POSITIVE")
    if source_width * SOURCE_ASPECT_DENOMINATOR != source_height * SOURCE_ASPECT_NUMERATOR:
        raise OptionCCompositionError("SOURCE_ASPECT_RATIO_MUST_BE_9_16")
    if source_width < CONTENT_WIDTH or source_height < CONTENT_HEIGHT:
        raise OptionCCompositionError("SOURCE_UPSCALE_NOT_ALLOWED")
    scale = Fraction(CONTENT_WIDTH, source_width)
    if Fraction(source_height) * scale != CONTENT_HEIGHT:
        raise OptionCCompositionError("NON_UNIFORM_SCALE_WOULD_BE_REQUIRED")
    return CompositionPlan(
        schema=SCHEMA,
        source_width=source_width,
        source_height=source_height,
        source_pixel_format="RGB24",
        canvas_width=CANVAS_WIDTH,
        canvas_height=CANVAS_HEIGHT,
        content_rect=Rect(CONTENT_X, CONTENT_Y, CONTENT_WIDTH, CONTENT_HEIGHT),
        header_rect=Rect(0, 0, CANVAS_WIDTH, HEADER_HEIGHT),
        footer_rect=Rect(0, FOOTER_Y, CANVAS_WIDTH, FOOTER_HEIGHT),
        left_gutter_rect=Rect(0, CONTENT_Y, CONTENT_X, CONTENT_HEIGHT),
        right_gutter_rect=Rect(CONTENT_X + CONTENT_WIDTH, CONTENT_Y, CONTENT_X, CONTENT_HEIGHT),
        scale=scale,
        resampler=RESAMPLER,
        crop=False,
        non_uniform_scaling=False,
        frame_order="PRESERVE_SINGLE_FRAME_CALLER_ORDER",
        editorial_text_drawn=False,
        audio_or_media_created=False,
    )


def _axis_area_weights(source_length: int, destination_length: int) -> tuple[tuple[tuple[int, int], ...], ...]:
    """Return exact integer source-pixel overlap weights for every destination pixel.

    Coordinates use a common integer lattice. Each destination interval has length
    source_length and each source interval has length destination_length. The weights
    for every output pixel sum exactly to source_length; no floating-point math occurs.
    """
    if not _is_int(source_length) or not _is_int(destination_length):
        raise OptionCCompositionError("RESAMPLE_AXIS_LENGTHS_MUST_BE_INTEGERS")
    if source_length <= 0 or destination_length <= 0 or destination_length > source_length:
        raise OptionCCompositionError("RESAMPLE_AXIS_LENGTHS_INVALID")
    rows: list[tuple[tuple[int, int], ...]] = []
    for destination_index in range(destination_length):
        interval_start = destination_index * source_length
        interval_end = (destination_index + 1) * source_length
        first_source = interval_start // destination_length
        last_source = (interval_end - 1) // destination_length
        weights: list[tuple[int, int]] = []
        for source_index in range(first_source, last_source + 1):
            source_start = source_index * destination_length
            source_end = (source_index + 1) * destination_length
            overlap = min(interval_end, source_end) - max(interval_start, source_start)
            if overlap > 0:
                weights.append((source_index, overlap))
        if sum(weight for _, weight in weights) != source_length:
            raise OptionCCompositionError("RESAMPLE_AREA_WEIGHT_SUM_MISMATCH")
        rows.append(tuple(weights))
    return tuple(rows)


def compose_rgb24_frame(source_rgb24: bytes, source_width: int, source_height: int) -> bytes:
    """Compose one immutable RGB24 frame, returning exactly 720*1280*3 bytes.

    The content region is area-downsampled with integer rational overlap weights.
    The remaining canvas bytes stay black. This function has no external runtime
    dependencies and has no filesystem, process, renderer, audio or media side effects.
    """
    plan = build_composition_plan(source_width, source_height)
    if not isinstance(source_rgb24, bytes):
        raise OptionCCompositionError("SOURCE_FRAME_MUST_BE_IMMUTABLE_BYTES")
    expected_source_bytes = source_width * source_height * 3
    if len(source_rgb24) != expected_source_bytes:
        raise OptionCCompositionError("SOURCE_RGB24_BYTE_COUNT_MISMATCH")

    x_weights = _axis_area_weights(source_width, CONTENT_WIDTH)
    y_weights = _axis_area_weights(source_height, CONTENT_HEIGHT)
    denominator = source_width * source_height
    rounding = denominator // 2
    source = memoryview(source_rgb24)
    canvas = bytearray(CANVAS_WIDTH * CANVAS_HEIGHT * 3)

    for output_y, y_contributors in enumerate(y_weights):
        output_row_start = ((CONTENT_Y + output_y) * CANVAS_WIDTH + CONTENT_X) * 3
        for output_x, x_contributors in enumerate(x_weights):
            red = green = blue = 0
            for source_y, weight_y in y_contributors:
                source_row_start = source_y * source_width * 3
                for source_x, weight_x in x_contributors:
                    weight = weight_x * weight_y
                    source_offset = source_row_start + source_x * 3
                    red += source[source_offset] * weight
                    green += source[source_offset + 1] * weight
                    blue += source[source_offset + 2] * weight
            output_offset = output_row_start + output_x * 3
            canvas[output_offset] = (red + rounding) // denominator
            canvas[output_offset + 1] = (green + rounding) // denominator
            canvas[output_offset + 2] = (blue + rounding) // denominator

    result = bytes(canvas)
    expected_output_bytes = CANVAS_WIDTH * CANVAS_HEIGHT * 3
    if len(result) != expected_output_bytes:
        raise OptionCCompositionError("COMPOSED_RGB24_BYTE_COUNT_MISMATCH")
    return result
