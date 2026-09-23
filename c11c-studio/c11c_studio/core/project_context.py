from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .paths import Paths


@dataclass
class ProjectContext:
    project_root: Path
    paths: Paths
    backend_version: str = "C11-C v2.1.4"
    c11b_state: str = "CLOSED / CERTIFIED / FROZEN"
    godot_version: Any = None
    ffmpeg_path: Any = None
    ffprobe_path: Any = None
    python_path: Any = None
    powershell_path: Any = None
    delivery_width: int = 720
    delivery_height: int = 1280
    fps: int = 30
    default_duration: float = 18.0
    default_frames: int = 540
    logical_width: int = 540
    logical_height: int = 960
    repository_state: dict = field(default_factory=dict)

    @classmethod
    def discover(cls, root):
        root = Path(root).resolve()
        ctx = cls(project_root=root, paths=Paths(root))
        ctx.repository_state = {
            "has_project_godot": (root / "project.godot").exists(),
            "has_tools": (root / "tools").exists(),
            "has_artifacts": (root / "artifacts").exists(),
            "has_prototypes": ctx.paths.prototypes.exists(),
        }
        return ctx
