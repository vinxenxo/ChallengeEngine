from __future__ import annotations
import importlib
import os
import sys
from pathlib import Path

QIMAGE_MODULE_REL = Path("tools/c11d/d9/c11e_e6_option_c_qimage_frame_compositor_v1.py")


def _norm_path(value: str | os.PathLike[str]) -> str:
    return os.path.normcase(os.path.normpath(str(Path(value).resolve())))


def ensure_payload_tools_root(payload_package: Path) -> Path:
    """Put the existing V2 payload root on sys.path for `import tools...`.

    The target test module lives at <package>/payload/tests/... and imports the
    compositor as `tools.c11d...`. Therefore <package>/payload (not merely
    <package>) must be a sys.path entry. The expected module must exist before
    sys.path is mutated. A preloaded unrelated regular `tools` package is
    rejected rather than silently resolving a different module.
    """
    package = Path(payload_package).resolve()
    payload_root = package / "payload"
    module_path = (payload_root / QIMAGE_MODULE_REL).resolve()
    if not module_path.is_file():
        raise FileNotFoundError("QIMAGE_PAYLOAD_MODULE_MISSING:" + str(module_path))

    expected_tools_dir = _norm_path(payload_root / "tools")
    existing_tools = sys.modules.get("tools")
    if existing_tools is not None:
        existing_paths = list(getattr(existing_tools, "__path__", []))
        if existing_paths and not any(_norm_path(p) == expected_tools_dir for p in existing_paths):
            raise ImportError("QIMAGE_TOOLS_NAMESPACE_PRELOADED_OUTSIDE_PAYLOAD")
        if not existing_paths:
            raise ImportError("QIMAGE_TOOLS_NAMESPACE_PRELOADED_AS_NON_PACKAGE")

    root_norm = _norm_path(payload_root)
    kept = []
    for entry in sys.path:
        candidate = entry if entry else os.getcwd()
        try:
            if _norm_path(candidate) == root_norm:
                continue
        except (OSError, RuntimeError):
            pass
        kept.append(entry)
    sys.path[:] = [str(payload_root), *kept]
    importlib.invalidate_caches()
    return module_path


def validate_qimage_module_origin(module, expected_path: Path) -> Path:
    """Assert the imported module came from the exact pinned payload location."""
    actual_value = getattr(module, "__file__", None)
    if not actual_value:
        raise ImportError("QIMAGE_MODULE_ORIGIN_MISSING")
    actual = Path(actual_value).resolve()
    expected = Path(expected_path).resolve()
    if actual != expected:
        raise ImportError(f"QIMAGE_MODULE_ORIGIN_MISMATCH:{actual}:{expected}")
    return actual
