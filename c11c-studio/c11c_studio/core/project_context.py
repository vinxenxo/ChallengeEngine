import re
from dataclasses import dataclass, field
from pathlib import Path
from .paths import Paths

_VERSION_RE = re.compile(r"C11-C[^0-9]{0,20}v?(\d+\.\d+\.\d+)", re.I)
_DELIVERY_RE = re.compile(r"(?:720x1280|720×1280|PHYSICAL.*?720x1280)", re.I)


def _highest_version(values):
    uniq = set(values)
    return max(uniq, key=lambda x: tuple(int(v) for v in x.split("."))) if uniq else None


def detect_backend_version(root: Path) -> tuple[str, str]:
    candidates = []
    for rel in ("docs", "tools/prototypes/c11c_bulk", "tools/prototypes/c11c_common"):
        p = root / rel
        if p.exists():
            candidates.extend(sorted(p.rglob("*.md"))[:80])
            candidates.extend(sorted(p.rglob("*.ps1"))[:80])
    versions = []
    for p in candidates:
        try:
            text = p.read_text(encoding="utf-8-sig", errors="ignore")
        except OSError:
            continue
        versions.extend(_VERSION_RE.findall(text))
    v = _highest_version(versions)
    if v:
        return f"C11-C v{v}", "DISCOVERED"
    return "C11-C v2.1.4", "BASELINE-FALLBACK"


@dataclass
class ProjectContext:
    project_root: Path
    paths: Paths
    backend_version: str
    backend_version_source: str
    c11b_state: str = "CLOSED / CERTIFIED / FROZEN"
    logical_width: int = 540
    logical_height: int = 960
    delivery_width: int = 720
    delivery_height: int = 1280
    fps: int = 30
    default_duration: float = 18.0
    default_frames: int = 540
    repository_state: dict = field(default_factory=dict)
    tool_paths: dict = field(default_factory=dict)
    godot_version: str | None = None

    @classmethod
    def discover(cls, root, cfg=None):
        root = Path(root).resolve()
        version, source = detect_backend_version(root)
        paths = Paths(root)
        ctx = cls(root, paths, version, source)
        overrides = (cfg.get("tool_paths", {}) if cfg else {}) or {}
        ctx.tool_paths = overrides
        ctx.repository_state = {
            "has_project_godot": (root / "project.godot").exists(),
            "has_tools": paths.tools.exists(),
            "has_artifacts": paths.artifacts.exists(),
            "has_prototypes": paths.prototypes.exists(),
            "has_production_25": (paths.bulk_tools / "run_c11c_production_25.ps1").exists(),
        }
        return ctx
