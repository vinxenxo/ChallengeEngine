"""Safe file-path module loader for pinned Python modules using dataclasses."""
from __future__ import annotations
import importlib.util
import sys
from pathlib import Path
from types import ModuleType


def load_module_registered(path: Path, module_name: str) -> ModuleType:
    """Load a file module with sys.modules registration before code execution.

    dataclasses._is_type resolves postponed annotations through
    sys.modules[cls.__module__].  module_from_spec() alone does not register
    the module; exec_module() alone can therefore raise
    AttributeError: 'NoneType' object has no attribute '__dict__'.
    """
    if not isinstance(module_name, str) or not module_name or any(ch.isspace() for ch in module_name):
        raise ValueError("MODULE_NAME_INVALID")
    source = Path(path)
    if not source.is_file():
        raise FileNotFoundError(f"MODULE_SOURCE_MISSING:{source}")
    if module_name in sys.modules:
        raise RuntimeError(f"MODULE_NAME_ALREADY_REGISTERED:{module_name}")
    spec = importlib.util.spec_from_file_location(module_name, source)
    if spec is None or spec.loader is None:
        raise ImportError(f"MODULE_SPEC_UNAVAILABLE:{source}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        if sys.modules.get(module_name) is module:
            sys.modules.pop(module_name, None)
        raise
    if sys.modules.get(module_name) is not module:
        raise RuntimeError("MODULE_REGISTRATION_REPLACED_DURING_IMPORT")
    return module
