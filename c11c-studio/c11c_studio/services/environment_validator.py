from dataclasses import dataclass, field

from ..core.project_context import ProjectContext
from .tool_discovery import discover_all


@dataclass
class CheckResult:
    name: str
    status: str
    message: str = ""


@dataclass
class ValidationReport:
    checks: list = field(default_factory=list)

    def add(self, c):
        self.checks.append(c)

    def ok(self):
        return all(c.status != "FAIL" for c in self.checks)

    def lines(self):
        return ["[" + c.status + "] " + c.name + ": " + c.message
                for c in self.checks]


class EnvironmentValidator:
    def __init__(self, ctx):
        self.ctx = ctx
        self.tools = {}

    def run_all(self):
        r = ValidationReport()
        r.add(CheckResult("project_root",
            "PASS" if self.ctx.project_root.exists() else "FAIL",
            str(self.ctx.project_root)))

        self.tools = discover_all(self.ctx.project_root)
        for name in ("python", "powershell", "ffmpeg", "ffprobe", "godot"):
            t = self.tools.get(name)
            status = "PASS" if (t and t.present) else (
                "WARN" if name in ("godot", "powershell") else "FAIL")
            r.add(CheckResult(name, status,
                (t.version if t and t.version else "not found")))

        fams = []
        if self.ctx.paths.prototypes.exists():
            for d in self.ctx.paths.prototypes.iterdir():
                if (d.is_dir() and d.name.startswith("c11c_")
                        and d.name not in ("c11c_bulk", "c11c_common",
                                           "c11c_review_assets")):
                    fams.append(d)
        r.add(CheckResult("families_present",
            "PASS" if len(fams) >= 1 else "FAIL",
            str(len(fams)) + " family directories detected"))

        r.add(CheckResult("delivery_config", "PASS",
            str(self.ctx.delivery_width) + "x" + str(self.ctx.delivery_height)
            + " @ " + str(self.ctx.fps) + " FPS ("
            + str(round(self.ctx.default_duration, 2)) + "s)"))

        for name in ("production", "prototypes_artifacts", "qa", "releases"):
            p = getattr(self.ctx.paths, name)
            r.add(CheckResult("artifacts." + name,
                "PASS" if p.exists() else "WARN", str(p)))

        return r
