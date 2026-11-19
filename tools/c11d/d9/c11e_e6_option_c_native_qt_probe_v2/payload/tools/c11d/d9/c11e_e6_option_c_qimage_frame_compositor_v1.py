"""C11-E E6 Option C native Qt/QImage single-frame compositor probe.

D-owned in-memory RGB24 primitive. It uses Qt's C++ QImage scaling and QPainter
operations through the already-existing PySide6 runtime; no Python pixel loops,
filesystem I/O, subprocesses, video decode/encode, dispatch, audio or media.

This V1 is a qualification probe. It is not yet connected to the shared E1 service
or to the Loop family-stage contract, and it is not an E6 compositor acceptance.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Any

from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QColor, QImage, QPainter

SCHEMA = "C11E-E6-OPTION-C-QIMAGE-FRAME-COMPOSITOR-V1"
BACKEND = "PYSIDE6_QIMAGE_CPP_SMOOTH_TRANSFORMATION_V1"
PYSIDE6_PIN = "6.11.2"
CANVAS_WIDTH = 720
CANVAS_HEIGHT = 1280
CONTENT_X = 108
CONTENT_Y = 192
CONTENT_WIDTH = 504
CONTENT_HEIGHT = 896
HEADER_HEIGHT = 192
FOOTER_Y = 1088
FOOTER_HEIGHT = 192
RIGHT_GUTTER_X = 612
SOURCE_ASPECT_NUMERATOR = 9
SOURCE_ASPECT_DENOMINATOR = 16

class OptionCNativeCompositionError(ValueError):
    """Raised when an input frame violates the approved Option C contract."""

@dataclass(frozen=True)
class CompositionPlan:
    schema: str
    backend: str
    source_width: int
    source_height: int
    source_pixel_format: str
    canvas_width: int
    canvas_height: int
    content_rect: tuple[int, int, int, int]
    header_rect: tuple[int, int, int, int]
    footer_rect: tuple[int, int, int, int]
    left_gutter_rect: tuple[int, int, int, int]
    right_gutter_rect: tuple[int, int, int, int]
    aspect_ratio: str
    crop: bool
    non_uniform_scaling: bool
    upscale: bool
    editorial_text_drawn: bool
    audio_or_media_created: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

def _is_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)

def build_composition_plan(source_width: int, source_height: int) -> CompositionPlan:
    if not _is_int(source_width) or not _is_int(source_height):
        raise OptionCNativeCompositionError("SOURCE_DIMENSIONS_MUST_BE_INTEGERS")
    if source_width <= 0 or source_height <= 0:
        raise OptionCNativeCompositionError("SOURCE_DIMENSIONS_MUST_BE_POSITIVE")
    if source_width * SOURCE_ASPECT_DENOMINATOR != source_height * SOURCE_ASPECT_NUMERATOR:
        raise OptionCNativeCompositionError("SOURCE_ASPECT_RATIO_MUST_BE_9_16")
    if source_width < CONTENT_WIDTH or source_height < CONTENT_HEIGHT:
        raise OptionCNativeCompositionError("SOURCE_UPSCALE_NOT_ALLOWED")
    return CompositionPlan(
        schema=SCHEMA,
        backend=BACKEND,
        source_width=source_width,
        source_height=source_height,
        source_pixel_format="RGB24",
        canvas_width=CANVAS_WIDTH,
        canvas_height=CANVAS_HEIGHT,
        content_rect=(CONTENT_X, CONTENT_Y, CONTENT_WIDTH, CONTENT_HEIGHT),
        header_rect=(0, 0, CANVAS_WIDTH, HEADER_HEIGHT),
        footer_rect=(0, FOOTER_Y, CANVAS_WIDTH, FOOTER_HEIGHT),
        left_gutter_rect=(0, CONTENT_Y, CONTENT_X, CONTENT_HEIGHT),
        right_gutter_rect=(RIGHT_GUTTER_X, CONTENT_Y, CONTENT_X, CONTENT_HEIGHT),
        aspect_ratio="9:16",
        crop=False,
        non_uniform_scaling=False,
        upscale=False,
        editorial_text_drawn=False,
        audio_or_media_created=False,
    )

def compose_rgb24_image(source_rgb24: bytes, source_width: int, source_height: int) -> QImage:
    """Return a new RGB888 QImage of 720x1280 with the approved black safe bands.

    QImage's constructor initially wraps immutable Python bytes; .copy() detaches
    the Qt image before scaling. QImage.scaled() and QPainter.drawImage() execute
    in Qt's native C++ implementation. The Python function performs no pixel loop.
    """
    build_composition_plan(source_width, source_height)
    if not isinstance(source_rgb24, bytes):
        raise OptionCNativeCompositionError("SOURCE_FRAME_MUST_BE_IMMUTABLE_BYTES")
    expected = source_width * source_height * 3
    if len(source_rgb24) != expected:
        raise OptionCNativeCompositionError("SOURCE_RGB24_BYTE_COUNT_MISMATCH")

    source_view = QImage(
        source_rgb24,
        source_width,
        source_height,
        source_width * 3,
        QImage.Format.Format_RGB888,
    )
    if source_view.isNull():
        raise OptionCNativeCompositionError("QIMAGE_SOURCE_CONSTRUCTION_FAILED")
    source = source_view.copy()
    if source.isNull() or source.format() != QImage.Format.Format_RGB888:
        raise OptionCNativeCompositionError("QIMAGE_SOURCE_DETACH_FAILED")

    scaled = source.scaled(
        CONTENT_WIDTH,
        CONTENT_HEIGHT,
        Qt.AspectRatioMode.IgnoreAspectRatio,
        Qt.TransformationMode.SmoothTransformation,
    )
    if scaled.isNull() or scaled.size().width() != CONTENT_WIDTH or scaled.size().height() != CONTENT_HEIGHT:
        raise OptionCNativeCompositionError("QIMAGE_SCALE_FAILED")

    canvas = QImage(CANVAS_WIDTH, CANVAS_HEIGHT, QImage.Format.Format_RGB888)
    if canvas.isNull():
        raise OptionCNativeCompositionError("QIMAGE_CANVAS_ALLOCATION_FAILED")
    canvas.fill(QColor(0, 0, 0))
    painter = QPainter(canvas)
    if not painter.isActive():
        raise OptionCNativeCompositionError("QPAINTER_BEGIN_FAILED")
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Source)
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
    painter.drawImage(QRect(CONTENT_X, CONTENT_Y, CONTENT_WIDTH, CONTENT_HEIGHT), scaled)
    if not painter.end():
        raise OptionCNativeCompositionError("QPAINTER_END_FAILED")
    if canvas.format() != QImage.Format.Format_RGB888:
        raise OptionCNativeCompositionError("QIMAGE_OUTPUT_FORMAT_MISMATCH")
    if canvas.bytesPerLine() != CANVAS_WIDTH * 3:
        raise OptionCNativeCompositionError("QIMAGE_OUTPUT_STRIDE_MISMATCH")
    if canvas.sizeInBytes() != CANVAS_WIDTH * CANVAS_HEIGHT * 3:
        raise OptionCNativeCompositionError("QIMAGE_OUTPUT_SIZE_MISMATCH")
    return canvas

def compose_rgb24_frame(source_rgb24: bytes, source_width: int, source_height: int) -> bytes:
    image = compose_rgb24_image(source_rgb24, source_width, source_height)
    result = bytes(image.constBits())
    expected = CANVAS_WIDTH * CANVAS_HEIGHT * 3
    if len(result) != expected:
        raise OptionCNativeCompositionError("QIMAGE_OUTPUT_BUFFER_LENGTH_MISMATCH")
    return result
