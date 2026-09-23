#!/usr/bin/env python3
# C11-C Studio bootstrap v4 - all patches (v4+v5+v6) included.
# Usage:
#   python bootstrap_studio_v4.py
#   python bootstrap_studio_v4.py --target DIR
#   python bootstrap_studio_v4.py --install
#   python bootstrap_studio_v4.py --install --run --project "D:\Repo"

import argparse
import os
import subprocess
import sys
from pathlib import Path


BLOB = r'''
###<FILE>requirements.txt
PySide6>=6.6.0

###<FILE>run.bat
@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv" (
    echo [C11-C Studio] Creating venv...
    python -m venv .venv
)
call .venv\Scripts\activate.bat
python -c "import PySide6" 2>NUL
if errorlevel 1 (
    echo [C11-C Studio] Installing deps...
    pip install -r requirements.txt
)
python main.py %*
endlocal

###<FILE>README.md
# C11-C Studio (v0.1.0)

Desktop orchestrator for the C11-C Visual Loops toolchain
(ChallengeEngineV01_STATELESS). Frontend only - never reimplements render
math, RNG, or frozen C11-B contracts.

## Quick start (Windows)

    run.bat

First launch creates .venv, installs PySide6, starts the app.

## Manual launch

    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    python main.py --project "D:\Path\To\ChallengeEngineV01_STATELESS"

## CLI

    python main.py --project <path>
    python main.py --validate
    python main.py --review-5x5
    python main.py --production-25

## What works

- Project discovery + environment validation (Godot/Python/FFmpeg/FFprobe/PowerShell)
- Dashboard with live status cards and recent jobs
- Family registry (5 canonical + dynamic discovery)
- Review Lab: select individual families, per-family details, live log
- Production: single + 5x5, random seed generator, grammar selector (gated)
- Families page: REVIEW preselects and jumps; OPEN FOLDER opens explorer
- Artifacts browser with protected/regenerable classification
- Log Center (live + raw + parsed)
- Validation Center
- Settings (persisted to %APPDATA%\C11CStudio\config.json)
- JobManager: async subprocess, stdout/stderr capture, cancel

## Contract compliance

- Delivery: 720x1280 / 30 FPS / 18 s baseline shown as defaults, not laws.
- Logical canvas 540x960 always displayed separately.
- One canonical MP4 per product enforced at validation level.
- Production never deleted by review cleanup.
- No hard-coded absolute paths.
- PowerShell arrays (-Seeds, -Families) passed as separate args (never
  comma-joined) because -File mode does not evaluate the comma operator.

## Canonical tool paths expected in the repo

    tools\prototypes\c11c_bulk\validate_c11c_powershell.ps1
    tools\prototypes\c11c_bulk\validate_c11c_delivery_configuration.ps1
    tools\prototypes\c11c_bulk\run_c11c_art_direction_review.ps1
    tools\prototypes\c11c_bulk\run_c11c_production.ps1
    tools\prototypes\c11c_bulk\run_c11c_production_bulk.ps1
    tools\prototypes\c11c_<family>\run_prototype.ps1

If a tool is missing, the job returns non-zero and the Log Center shows
the real cause - the raw log is never hidden.

###<FILE>main.py
import argparse
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox

from c11c_studio.core.config import AppConfig
from c11c_studio.core.project_context import ProjectContext
from c11c_studio.ui.theme import apply_dark_theme
from c11c_studio.ui.main_window import MainWindow


APP_NAME = "C11-C Studio"
APP_VERSION = "0.1.0"


def parse_args():
    p = argparse.ArgumentParser(prog="c11c-studio")
    p.add_argument("--project", type=str, default=None)
    p.add_argument("--validate", action="store_true")
    p.add_argument("--review-5x5", action="store_true")
    p.add_argument("--production-25", action="store_true")
    return p.parse_args()


def resolve_project_root(cfg, cli_path):
    if cli_path:
        return Path(cli_path).expanduser().resolve()
    saved = cfg.get("project_root")
    if saved and Path(saved).exists():
        return Path(saved)
    return None


def looks_like_project(path):
    if not path or not path.exists():
        return False
    signals = ["project.godot", "tools", "artifacts"]
    return sum((path / s).exists() for s in signals) >= 2


def main():
    args = parse_args()
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    apply_dark_theme(app)

    cfg = AppConfig.load()
    root = resolve_project_root(cfg, args.project)

    if root is None or not looks_like_project(root):
        chosen = QFileDialog.getExistingDirectory(
            None, "Select ChallengeEngineV01_STATELESS project root",
            str(Path.home()))
        if not chosen:
            QMessageBox.warning(None, APP_NAME,
                "No project selected. Cannot start without a project root.")
            return 2
        root = Path(chosen).resolve()
        if not looks_like_project(root):
            resp = QMessageBox.question(
                None, APP_NAME,
                "The selected folder does not look like a ChallengeEngine "
                "project:\n" + str(root) + "\n\nContinue anyway?")
            if resp != QMessageBox.Yes:
                return 2
        cfg.set("project_root", str(root))
        cfg.save()

    ctx = ProjectContext.discover(root)

    if args.validate:
        from c11c_studio.services.environment_validator import EnvironmentValidator
        report = EnvironmentValidator(ctx).run_all()
        for line in report.lines():
            print(line)
        return 0 if report.ok() else 1

    win = MainWindow(ctx, app_version=APP_VERSION)
    win.show()

    if args.review_5x5:
        win.trigger_review_5x5()
    elif args.production_25:
        win.trigger_production_25()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())

###<FILE>c11c_studio/__init__.py
__version__ = "0.1.0"

###<FILE>c11c_studio/core/__init__.py

###<FILE>c11c_studio/core/paths.py
from pathlib import Path


class Paths:
    def __init__(self, root):
        self.root = Path(root).resolve()

    @property
    def tools(self): return self.root / "tools"

    @property
    def prototypes(self): return self.tools / "prototypes"

    @property
    def bulk_tools(self): return self.prototypes / "c11c_bulk"

    @property
    def common_tools(self): return self.prototypes / "c11c_common"

    @property
    def artifacts(self): return self.root / "artifacts"

    @property
    def production(self):
        return self.artifacts / "production" / "audiovisual"

    @property
    def prototypes_artifacts(self):
        return self.artifacts / "prototypes"

    @property
    def review_assets(self):
        return self.prototypes_artifacts / "c11c_review_assets"

    @property
    def legacy(self): return self.artifacts / "legacy"

    @property
    def qa(self): return self.artifacts / "qa"

    @property
    def regression(self): return self.artifacts / "regression"

    @property
    def releases(self): return self.artifacts / "releases"

    @property
    def tests(self): return self.artifacts / "tests"

    @property
    def scratch(self): return self.artifacts / "scratch"

    def family_prototype_dir(self, folder):
        return self.prototypes / folder

###<FILE>c11c_studio/core/config.py
import json
import os
from pathlib import Path


def _config_dir():
    base = os.environ.get("APPDATA") or str(Path.home())
    d = Path(base) / "C11CStudio"
    d.mkdir(parents=True, exist_ok=True)
    return d


class AppConfig:
    def __init__(self, data=None):
        self._data = data or {}
        self._path = _config_dir() / "config.json"

    @classmethod
    def load(cls):
        p = _config_dir() / "config.json"
        if p.exists():
            try:
                return cls(json.loads(p.read_text(encoding="utf-8")))
            except Exception:
                return cls({})
        return cls({})

    def save(self):
        self._path.write_text(
            json.dumps(self._data, indent=2, ensure_ascii=False),
            encoding="utf-8")

    def get(self, key, default=None):
        return self._data.get(key, default)

    def set(self, key, value):
        self._data[key] = value

###<FILE>c11c_studio/core/project_context.py
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

###<FILE>c11c_studio/domain/__init__.py

###<FILE>c11c_studio/domain/parameter.py
from dataclasses import dataclass, field


@dataclass
class Parameter:
    id: str
    name: str
    type: str
    state: str = "READ_ONLY"
    description: str = ""
    default: object = None
    value: object = None
    min: object = None
    max: object = None
    step: object = None
    unit: object = None
    options: list = field(default_factory=list)
    source: str = ""
    family: object = None
    grammar: object = None

    @property
    def editable(self):
        return self.state == "USER_CONFIGURABLE"

###<FILE>c11c_studio/domain/family.py
from dataclasses import dataclass, field

from .parameter import Parameter


@dataclass
class Family:
    id: str
    technical: str
    artistic: str
    folder: str
    short_description: str = ""
    visual_metaphor: str = ""
    grammars: list = field(default_factory=list)
    palette_bank: list = field(default_factory=list)
    parameters: list = field(default_factory=list)
    default_duration: float = 18.0
    audio_profile: str = "C11CSafeAmbient"

    @property
    def launcher_name(self):
        return "run_prototype.ps1"

    def has_grammars(self):
        return len(self.grammars) > 0

###<FILE>c11c_studio/domain/seed.py
import random
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class SeedRecord:
    seed: int
    source: str = "MANUAL"
    created_at: str = field(
        default_factory=lambda: datetime.now().isoformat(timespec="seconds"))
    batch_id: object = None
    used_in_families: list = field(default_factory=list)


def generate_unique_seeds(count, min_v=1, max_v=2147483647):
    if count <= 0:
        return []
    if count > (max_v - min_v + 1):
        raise ValueError("Too many unique seeds requested.")
    seen = set()
    out = []
    while len(out) < count:
        s = random.randint(min_v, max_v)
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out

###<FILE>c11c_studio/domain/job.py
from dataclasses import dataclass, field
from enum import Enum


class JobState(str, Enum):
    QUEUED = "QUEUED"
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    RENDERING = "RENDERING"
    AUDIO = "AUDIO"
    MUXING = "MUXING"
    VALIDATING = "VALIDATING"
    EXPORTING = "EXPORTING"
    PUBLISHED = "PUBLISHED"
    PASS = "PASS"
    FAILED = "FAILED"
    CANCEL_REQUESTED = "CANCEL_REQUESTED"
    CANCELLED = "CANCELLED"
    SKIPPED = "SKIPPED"
    BLOCKED = "BLOCKED"


@dataclass
class Job:
    id: str
    batch_id: object
    job_type: str
    family: object = None
    seed: object = None
    state: JobState = JobState.QUEUED
    started_at: object = None
    finished_at: object = None
    command: list = field(default_factory=list)
    cwd: object = None
    exit_code: object = None
    log_path: object = None
    stdout: str = ""
    stderr: str = ""
    outputs: list = field(default_factory=list)
    errors: list = field(default_factory=list)
    display_command: str = ""

###<FILE>c11c_studio/domain/product.py
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Product:
    product_id: str
    family: str
    seed: int
    root: Path
    mp4: object = None
    wav: object = None
    social_txt: object = None
    manifest_json: object = None
    authoring_json: object = None
    ffprobe_json: object = None
    godot_log: object = None
    status: str = "CANDIDATE"
    metadata: dict = field(default_factory=dict)

###<FILE>c11c_studio/services/__init__.py

###<FILE>c11c_studio/services/tool_discovery.py
import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ToolInfo:
    name: str
    path: object
    version: object
    present: bool

    def __str__(self):
        tag = "OK " + (self.version or "") if self.present else "MISSING"
        return self.name + ": " + tag


def _which(cands):
    for c in cands:
        p = shutil.which(c)
        if p:
            return p
    return None


def _run_version(cmd, timeout=6.0):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        txt = (r.stdout or r.stderr or "").strip().splitlines()
        return txt[0] if txt else None
    except Exception:
        return None


def discover_all(project_root=None):
    tools = {}
    tools["python"] = ToolInfo(
        "python", os.sys.executable,
        "%d.%d.%d" % (os.sys.version_info.major,
                      os.sys.version_info.minor,
                      os.sys.version_info.micro),
        True)

    ps = _which(["powershell.exe", "pwsh.exe", "powershell", "pwsh"])
    tools["powershell"] = ToolInfo(
        "powershell", ps,
        _run_version([ps, "-NoProfile", "-Command",
                      "$PSVersionTable.PSVersion.ToString()"]) if ps else None,
        bool(ps))

    ffmpeg = _which(["ffmpeg.exe", "ffmpeg"])
    ffprobe = _which(["ffprobe.exe", "ffprobe"])
    if project_root:
        for cand in project_root.rglob("ffmpeg.exe"):
            ffmpeg = ffmpeg or str(cand); break
        for cand in project_root.rglob("ffprobe.exe"):
            ffprobe = ffprobe or str(cand); break
    tools["ffmpeg"] = ToolInfo("ffmpeg", ffmpeg,
        _run_version([ffmpeg, "-version"]) if ffmpeg else None,
        bool(ffmpeg))
    tools["ffprobe"] = ToolInfo("ffprobe", ffprobe,
        _run_version([ffprobe, "-version"]) if ffprobe else None,
        bool(ffprobe))

    godot = _which(["godot.exe", "Godot.exe", "godot"])
    if not godot and project_root:
        for cand in project_root.rglob("Godot*.exe"):
            godot = str(cand); break
    tools["godot"] = ToolInfo("godot", godot,
        _run_version([godot, "--version"]) if godot else None,
        bool(godot))

    return tools

###<FILE>c11c_studio/services/environment_validator.py
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

###<FILE>c11c_studio/services/family_registry.py
from ..core.project_context import ProjectContext
from ..domain.family import Family
from ..domain.parameter import Parameter


_CANONICAL = [
    {
        "id": "c11c_geometric_waves_v1",
        "technical": "geometric",
        "artistic": "Geometric Waves",
        "folder": "c11c_geometric_waves_v1",
        "short_description": "Harmonic loom. Liquid architecture.",
        "visual_metaphor": "Wave interference; tension/release; deterministic geometry",
        "grammars": [],
        "palette_bank": ["cyan", "magenta", "white"],
        "parameters": [
            ("frequency", "float", "SEED_DERIVED"),
            ("phase", "float", "SEED_DERIVED"),
            ("amplitude", "float", "SEED_DERIVED"),
            ("morph", "float", "SEED_DERIVED"),
            ("polygon_order", "integer", "SEED_DERIVED"),
            ("layer_count", "integer", "SEED_DERIVED"),
            ("palette_anchor", "color", "SEED_DERIVED"),
        ],
    },
    {
        "id": "c11c_fractal_bloom_v1",
        "technical": "fractal",
        "artistic": "Fractal Bloom",
        "folder": "c11c_fractal_bloom_v1",
        "short_description": "Mycelium, neural synapses, infinite universe.",
        "visual_metaphor": "z(n+1) = z(n)^2 + c; radial nucleus; controlled zoom",
        "grammars": ["RADIAL BLOOM", "DENDRITIC TUNNEL", "SPIRAL FRACTAL",
                     "FRACTAL FILIGREE", "NESTED WORLDS"],
        "palette_bank": ["indigo", "violet", "cyan"],
        "parameters": [
            ("julia_constant", "float", "SEED_DERIVED"),
            ("detail", "float", "SEED_DERIVED"),
            ("branching", "float", "SEED_DERIVED"),
            ("zoom", "float", "SEED_DERIVED"),
            ("domain_warp", "float", "SEED_DERIVED"),
            ("depth_layers", "integer", "SEED_DERIVED"),
            ("color_diversity", "float", "SEED_DERIVED"),
        ],
    },
    {
        "id": "c11c_sacred_symmetry_v1",
        "technical": "kaleidoscope",
        "artistic": "Sacred Symmetry",
        "folder": "c11c_sacred_symmetry_v1",
        "short_description": "Generative astrolabe. Celestial mechanism.",
        "visual_metaphor": "Radial symmetry; clockwork motion; precision",
        "grammars": [],
        "palette_bank": ["gold", "amber", "copper"],
        "parameters": [
            ("symmetry_order", "integer", "SEED_DERIVED"),
            ("ring_count", "integer", "SEED_DERIVED"),
            ("gear_count", "integer", "SEED_DERIVED"),
            ("gear_ratio", "string", "SEED_DERIVED"),
            ("rotation_phase", "float", "SEED_DERIVED"),
        ],
    },
    {
        "id": "c11c_living_particles_v1",
        "technical": "particle_flow",
        "artistic": "Living Particles",
        "folder": "c11c_living_particles_v1",
        "short_description": "Magnetic dust, ink in fluid, attractors, eddies.",
        "visual_metaphor": "Emergent flow; collisions; trail persistence",
        "grammars": [],
        "palette_bank": ["emerald", "sea-green", "turquoise"],
        "parameters": [
            ("particle_count", "integer", "SEED_DERIVED"),
            ("density", "float", "SEED_DERIVED"),
            ("flow", "float", "SEED_DERIVED"),
            ("attractors", "integer", "SEED_DERIVED"),
            ("collisions", "boolean", "SEED_DERIVED"),
            ("trail_persistence", "float", "SEED_DERIVED"),
        ],
    },
    {
        "id": "c11c_invisible_forces_v1",
        "technical": "vector_field",
        "artistic": "Invisible Forces",
        "folder": "c11c_invisible_forces_v1",
        "short_description": "Solar wind, gravitational topography, field traces.",
        "visual_metaphor": "No ves la fuerza, solo su rastro",
        "grammars": ["TOPOGRAPHIC_BASIN"],
        "palette_bank": ["crimson", "orange", "yellow"],
        "parameters": [
            ("field_config", "string", "SEED_DERIVED"),
            ("trace_count", "integer", "SEED_DERIVED"),
            ("pulse_speed", "float", "SEED_DERIVED"),
            ("field_phase", "float", "SEED_DERIVED"),
            ("trace_curvature", "float", "SEED_DERIVED"),
        ],
    },
]


def _to_parameter(t):
    pid, ptype, pstate = t
    return Parameter(id=pid, name=pid.replace("_", " ").title(),
                     type=ptype, state=pstate, source="canonical")


class FamilyRegistry:
    def __init__(self, ctx):
        self.ctx = ctx
        self._families = []

    def load(self):
        canonical_by_folder = {c["folder"]: c for c in _CANONICAL}
        discovered = []

        protos = self.ctx.paths.prototypes
        if protos.exists():
            for d in sorted(protos.iterdir()):
                if not d.is_dir() or not d.name.startswith("c11c_"):
                    continue
                if d.name in ("c11c_bulk", "c11c_common", "c11c_review_assets"):
                    continue
                meta = canonical_by_folder.get(d.name)
                if meta:
                    discovered.append(self._from_meta(meta))
                else:
                    stem = d.name.replace("c11c_", "").replace("_v1", "")
                    discovered.append(Family(
                        id=d.name, technical=stem,
                        artistic=stem.replace("_", " ").title(),
                        folder=d.name,
                        short_description="Discovered family."))

        if not discovered:
            discovered = [self._from_meta(m) for m in _CANONICAL]

        self._families = discovered
        return discovered

    def _from_meta(self, meta):
        return Family(
            id=meta["id"],
            technical=meta["technical"],
            artistic=meta["artistic"],
            folder=meta["folder"],
            short_description=meta.get("short_description", ""),
            visual_metaphor=meta.get("visual_metaphor", ""),
            grammars=list(meta.get("grammars", [])),
            palette_bank=list(meta.get("palette_bank", [])),
            parameters=[_to_parameter(t) for t in meta.get("parameters", [])],
        )

    @property
    def families(self):
        return self._families

###<FILE>c11c_studio/services/seed_manager.py
import json
import uuid
from datetime import datetime
from pathlib import Path

from ..domain.seed import SeedRecord, generate_unique_seeds


class SeedManager:
    def __init__(self, workspace):
        self.workspace = Path(workspace)
        self.workspace.mkdir(parents=True, exist_ok=True)
        self._current_batch_id = None
        self._records = []

    def new_batch_id(self):
        self._current_batch_id = (
            datetime.now().strftime("batch_%Y%m%d_%H%M%S_")
            + uuid.uuid4().hex[:6])
        return self._current_batch_id

    def random_batch(self, count, source="RANDOM"):
        bid = self.new_batch_id()
        seeds = generate_unique_seeds(count)
        recs = [SeedRecord(seed=s, source=source, batch_id=bid) for s in seeds]
        self._records.extend(recs)
        return recs

    def manual_batch(self, seeds):
        bid = self.new_batch_id()
        recs = [SeedRecord(seed=s, source="MANUAL", batch_id=bid) for s in seeds]
        self._records.extend(recs)
        return recs

    @property
    def records(self):
        return list(self._records)

    def save_batch(self, recs):
        bid = recs[0].batch_id or self.new_batch_id()
        path = self.workspace / (bid + ".json")
        path.write_text(json.dumps([r.__dict__ for r in recs], indent=2),
                        encoding="utf-8")
        return path

###<FILE>c11c_studio/services/command_builder.py
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class CommandSpec:
    executable: str
    arguments: list = field(default_factory=list)
    working_directory: object = None
    environment: dict = field(default_factory=dict)
    display_command: str = ""

    def __post_init__(self):
        if not self.display_command:
            parts = []
            for a in [self.executable, *self.arguments]:
                if " " in a:
                    parts.append('"' + a + '"')
                else:
                    parts.append(a)
            self.display_command = " ".join(parts)


def _ps(powershell, script, args=()):
    argv = ["-NoProfile", "-ExecutionPolicy", "Bypass",
            "-File", str(script), *args]
    return CommandSpec(executable=powershell, arguments=argv,
                       working_directory=str(script.parent))


def _array_flag(flag, values):
    # Pass each value as its own argument so PowerShell's parameter binder
    # collects them into [int[]] / [string[]]. -File mode does NOT evaluate
    # the comma operator, so "1,2,3" cannot be cast to int[].
    out = [flag]
    out.extend(str(v) for v in values)
    return out


class CommandBuilder:
    def __init__(self, ctx):
        self.ctx = ctx
        self.ps = ctx.powershell_path or "powershell.exe"

    def validate_powershell(self):
        s = self.ctx.paths.bulk_tools / "validate_c11c_powershell.ps1"
        return _ps(self.ps, s)

    def validate_delivery(self):
        s = self.ctx.paths.bulk_tools / "validate_c11c_delivery_configuration.ps1"
        return _ps(self.ps, s)

    def review_5x5(self, seeds, families, audio=True):
        s = self.ctx.paths.bulk_tools / "run_c11c_art_direction_review.ps1"
        argv = []
        argv += _array_flag("-Seeds", seeds)
        argv += _array_flag("-Families", families)
        if not audio:
            argv.append("-NoSound")
        return _ps(self.ps, s, argv)

    def production_single(self, family, seed, audio=True,
                          grammar=None, allow_grammar=False):
        s = self.ctx.paths.bulk_tools / "run_c11c_production.ps1"
        argv = ["-Family", family, "-Seed", str(seed)]
        if allow_grammar and grammar:
            argv += ["-Grammar", grammar]
        if not audio:
            argv.append("-NoSound")
        return _ps(self.ps, s, argv)

    def production_5x5(self, seeds, families, audio=True,
                       grammar=None, allow_grammar=False):
        s = self.ctx.paths.bulk_tools / "run_c11c_production_bulk.ps1"
        argv = []
        argv += _array_flag("-Seeds", seeds)
        argv += _array_flag("-Families", families)
        if allow_grammar and grammar:
            argv += ["-Grammar", grammar]
        if not audio:
            argv.append("-NoSound")
        return _ps(self.ps, s, argv)

    def reproduce_family(self, family_folder, seed,
                         grammar=None, allow_grammar=False):
        s = self.ctx.paths.prototypes / family_folder / "run_prototype.ps1"
        argv = ["-Seed", str(seed)]
        if allow_grammar and grammar:
            argv += ["-Grammar", grammar]
        return _ps(self.ps, s, argv)

###<FILE>c11c_studio/services/job_manager.py
import uuid
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import QObject, QProcess, Signal, QProcessEnvironment

from ..domain.job import Job, JobState


class JobManager(QObject):
    job_started = Signal(str)
    job_output = Signal(str, str)
    job_state_changed = Signal(str, str)
    job_finished = Signal(str, int)

    def __init__(self, log_dir, parent=None):
        super().__init__(parent)
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.jobs = {}
        self._current = None

    def start_job(self, job_type, spec, family=None, seed=None, batch_id=None):
        if self._current is not None:
            raise RuntimeError("A job is already running (spec 23).")

        jid = uuid.uuid4().hex[:10]
        log_path = self.log_dir / (jid + "_" + job_type + ".log")
        job = Job(id=jid, batch_id=batch_id, job_type=job_type,
                  family=family, seed=seed,
                  command=[spec.executable, *spec.arguments],
                  cwd=spec.working_directory,
                  display_command=spec.display_command,
                  log_path=log_path, state=JobState.STARTING,
                  started_at=datetime.now().isoformat(timespec="seconds"))
        self.jobs[jid] = job

        proc = QProcess(self)
        if spec.working_directory:
            proc.setWorkingDirectory(spec.working_directory)
        env = QProcessEnvironment.systemEnvironment()
        for k, v in spec.environment.items():
            env.insert(k, v)
        proc.setProcessEnvironment(env)
        proc.setProgram(spec.executable)
        proc.setArguments(spec.arguments)

        proc.readyReadStandardOutput.connect(lambda: self._on_stdout(jid))
        proc.readyReadStandardError.connect(lambda: self._on_stderr(jid))
        proc.finished.connect(lambda code, st: self._on_finished(jid, code))
        proc.errorOccurred.connect(lambda err: self._on_error(jid, err))

        self._current = (jid, proc)
        job.state = JobState.RUNNING
        self.job_started.emit(jid)
        self.job_state_changed.emit(jid, job.state.value)
        proc.start()
        return job

    def cancel_current(self):
        if not self._current:
            return
        jid, proc = self._current
        job = self.jobs[jid]
        job.state = JobState.CANCEL_REQUESTED
        self.job_state_changed.emit(jid, job.state.value)
        proc.kill()

    def _append(self, job, text):
        job.stdout += text
        if job.log_path:
            try:
                with job.log_path.open("a", encoding="utf-8") as fh:
                    fh.write(text)
            except Exception:
                pass
        self.job_output.emit(job.id, text)

    def _on_stdout(self, jid):
        cur = self._current
        if not cur or cur[0] != jid:
            return
        chunk = bytes(cur[1].readAllStandardOutput()).decode(
            "utf-8", errors="replace")
        self._append(self.jobs[jid], chunk)

    def _on_stderr(self, jid):
        cur = self._current
        if not cur or cur[0] != jid:
            return
        chunk = bytes(cur[1].readAllStandardError()).decode(
            "utf-8", errors="replace")
        job = self.jobs[jid]
        job.stderr += chunk
        self._append(job, chunk)

    def _on_finished(self, jid, code):
        job = self.jobs[jid]
        job.exit_code = code
        job.finished_at = datetime.now().isoformat(timespec="seconds")
        job.state = JobState.PASS if code == 0 else JobState.FAILED
        self.job_state_changed.emit(jid, job.state.value)
        self.job_finished.emit(jid, code)
        self._current = None

    def _on_error(self, jid, err):
        job = self.jobs[jid]
        job.errors.append(str(err))
        job.state = JobState.FAILED
        self.job_state_changed.emit(jid, job.state.value)
        self._current = None

###<FILE>c11c_studio/services/artifact_registry.py
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ArtifactRoot:
    key: str
    path: Path
    label: str
    protection: str
    exists: bool
    size_bytes: int = 0
    file_count: int = 0


PROTECTED_KEYS = {"production", "qa", "regression", "releases", "legacy", "tests"}


class ArtifactRegistry:
    def __init__(self, ctx):
        self.ctx = ctx

    def roots(self):
        p = self.ctx.paths
        specs = [
            ("production", p.production, "Production (audiovisual)", "protected"),
            ("review", p.review_assets, "Review assets", "regenerable"),
            ("prototypes", p.prototypes_artifacts, "Prototypes", "experimental"),
            ("qa", p.qa, "QA evidence", "protected"),
            ("regression", p.regression, "Regression evidence", "protected"),
            ("releases", p.releases, "Releases", "protected"),
            ("legacy", p.legacy, "Legacy", "protected"),
            ("tests", p.tests, "Tests", "protected"),
            ("scratch", p.scratch, "Scratch", "disposable"),
        ]
        out = []
        for key, path, label, protection in specs:
            exists = path.exists()
            size = 0
            files = 0
            if exists:
                for f in path.rglob("*"):
                    try:
                        if f.is_file():
                            files += 1
                            size += f.stat().st_size
                    except Exception:
                        pass
            out.append(ArtifactRoot(key, path, label, protection,
                                    exists, size, files))
        return out

    def is_protected(self, key):
        return key in PROTECTED_KEYS

###<FILE>c11c_studio/ui/__init__.py

###<FILE>c11c_studio/ui/theme.py
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication


QSS = """
QWidget { background-color: #0e1116; color: #e6edf3;
    font-family: 'Segoe UI'; font-size: 10pt; }
QMainWindow { background-color: #0e1116; }
QFrame#TopBar { background-color: #141922;
    border-bottom: 1px solid #232a36; }
QLabel#TopBarTitle { font-size: 14pt; font-weight: 600; color: #e6edf3; }
QLabel#TopBarMeta { color: #8b96a8; font-family: 'Consolas'; }
QFrame#NavRail { background-color: #11151d;
    border-right: 1px solid #232a36; }
QPushButton#NavButton {
    text-align: left; padding: 10px 14px; border: none;
    border-radius: 6px; color: #b7c1d3; background: transparent;
    font-size: 10pt;
}
QPushButton#NavButton:hover { background: #1a2130; color: #ffffff; }
QPushButton#NavButton:checked {
    background: #1e2a3d; color: #7ad7ff; font-weight: 600; }
QLabel#PageTitle { font-size: 18pt; font-weight: 600; color: #e6edf3; }
QLabel#PageSubtitle { color: #8b96a8; }
QFrame#Card { background: #141922;
    border: 1px solid #232a36; border-radius: 8px; }
QLabel#CardTitle { color: #8b96a8; font-size: 9pt; letter-spacing: 1px; }
QLabel#CardValue { font-size: 16pt; font-weight: 600; color: #e6edf3; }
QLabel#CardState { font-family: 'Consolas'; color: #6ee7a7; }
QPushButton.Primary {
    background: #1f6feb; color: #ffffff; border: none;
    padding: 9px 16px; border-radius: 6px; font-weight: 600;
}
QPushButton.Primary:hover { background: #2b7fff; }
QPushButton.Ghost {
    background: transparent; color: #b7c1d3;
    border: 1px solid #2b3444; padding: 8px 14px; border-radius: 6px;
}
QPushButton.Ghost:hover { border-color: #3d4a60; color: #ffffff; }
QPlainTextEdit#LogView {
    background: #0a0d12; color: #c9d3e2;
    font-family: 'Consolas'; font-size: 9pt;
    border: 1px solid #232a36; border-radius: 6px;
}
QTableWidget {
    background: #0f141c; alternate-background-color: #121924;
    gridline-color: #1e2632; border: 1px solid #232a36;
    border-radius: 6px;
}
QHeaderView::section {
    background: #141922; color: #8b96a8; padding: 6px;
    border: none; border-bottom: 1px solid #232a36; font-weight: 600;
}
QLineEdit, QSpinBox, QComboBox, QPlainTextEdit {
    background: #0f141c; border: 1px solid #232a36;
    border-radius: 5px; padding: 5px 8px; color: #e6edf3;
}
QLineEdit:focus, QSpinBox:focus, QComboBox:focus { border-color: #1f6feb; }
QStatusBar { background: #0e1116; color: #8b96a8; }
"""


def apply_dark_theme(app):
    app.setStyle("Fusion")
    app.setStyleSheet(QSS)
    app.setFont(QFont("Segoe UI", 10))

###<FILE>c11c_studio/ui/widgets/__init__.py

###<FILE>c11c_studio/ui/widgets/status_card.py
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel


class StatusCard(QFrame):
    def __init__(self, title, value="-", state="", parent=None):
        super().__init__(parent)
        self.setObjectName("Card")
        self.setFrameShape(QFrame.NoFrame)

        v = QVBoxLayout(self)
        v.setContentsMargins(14, 12, 14, 12)
        v.setSpacing(4)

        self.title = QLabel(title.upper())
        self.title.setObjectName("CardTitle")
        self.value = QLabel(value)
        self.value.setObjectName("CardValue")
        self.state = QLabel(state)
        self.state.setObjectName("CardState")

        v.addWidget(self.title)
        v.addWidget(self.value)
        v.addWidget(self.state)

    def set(self, value, state=""):
        self.value.setText(value)
        self.state.setText(state)

###<FILE>c11c_studio/ui/widgets/log_view.py
from PySide6.QtWidgets import QPlainTextEdit
from PySide6.QtGui import QTextCursor


class LogView(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("LogView")
        self.setReadOnly(True)
        self.setMaximumBlockCount(20000)

    def append_text(self, text):
        self.moveCursor(QTextCursor.End)
        self.insertPlainText(text)
        self.moveCursor(QTextCursor.End)

    def clear_log(self):
        self.clear()

###<FILE>c11c_studio/ui/widgets/nav_button.py
from PySide6.QtWidgets import QPushButton


class NavButton(QPushButton):
    def __init__(self, label, parent=None):
        super().__init__(label, parent)
        self.setObjectName("NavButton")
        self.setCheckable(True)

###<FILE>c11c_studio/ui/pages/__init__.py

###<FILE>c11c_studio/ui/pages/dashboard.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QHeaderView)
from PySide6.QtCore import Qt

from ..widgets.status_card import StatusCard


class DashboardPage(QWidget):
    def __init__(self, ctx, tools, parent=None):
        super().__init__(parent)
        self.ctx = ctx
        self.tools = tools

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(18)

        title = QLabel("Dashboard")
        title.setObjectName("PageTitle")
        sub = QLabel("C11-C Visual Loops - operational overview")
        sub.setObjectName("PageSubtitle")
        root.addWidget(title)
        root.addWidget(sub)

        cards = QHBoxLayout()
        cards.setSpacing(14)
        g = self.tools.get("godot")
        self.card_backend = StatusCard("Backend", self.ctx.backend_version, "READY")
        self.card_godot = StatusCard(
            "Godot",
            (g.version or "missing") if g else "missing",
            "READY" if g and g.present else "MISSING")
        self.card_delivery = StatusCard(
            "Delivery",
            "%dx%d / %d FPS / %ds" % (self.ctx.delivery_width,
                self.ctx.delivery_height, self.ctx.fps,
                int(self.ctx.default_duration)),
            "CANONICAL")
        self.card_families = StatusCard("Families", "5", "")
        self.card_prod = StatusCard("Production", "-", "")
        self.card_review = StatusCard("Review corpus", "-", "")

        for c in (self.card_backend, self.card_godot, self.card_delivery,
                  self.card_families, self.card_prod, self.card_review):
            cards.addWidget(c)
        root.addLayout(cards)

        actions = QHBoxLayout()
        self.btn_validate = QPushButton("VALIDATE ENVIRONMENT")
        self.btn_review = QPushButton("NEW 5x5 REVIEW")
        self.btn_produce = QPushButton("PRODUCE 5x5 FINAL")
        self.btn_single = QPushButton("PRODUCE SINGLE")
        self.btn_open_prod = QPushButton("OPEN PRODUCTION")
        self.btn_open_review = QPushButton("OPEN REVIEW")
        for b in (self.btn_validate, self.btn_review, self.btn_produce,
                  self.btn_single, self.btn_open_prod, self.btn_open_review):
            actions.addWidget(b)
        actions.addStretch(1)
        root.addLayout(actions)

        recent = QLabel("Recent activity")
        recent.setStyleSheet("color:#8b96a8; font-weight:600; margin-top:8px;")
        root.addWidget(recent)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(
            ["Date/Time", "Type", "Family", "Seed", "State", "Duration"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        root.addWidget(self.table, 1)

    def set_counts(self, production, review, families):
        self.card_prod.set(str(production))
        self.card_review.set(str(review))
        self.card_families.set(str(families))

    def add_job_row(self, when, jtype, family, seed, state, duration):
        r = self.table.rowCount()
        self.table.insertRow(r)
        for c, txt in enumerate([when, jtype, family, seed, state, duration]):
            it = QTableWidgetItem(txt)
            it.setFlags(it.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(r, c, it)

###<FILE>c11c_studio/ui/pages/review.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QSpinBox, QComboBox, QGroupBox,
                               QFormLayout, QCheckBox, QSplitter, QTextBrowser)
from PySide6.QtCore import Signal, Qt


class ReviewPage(QWidget):
    request_run = Signal(dict)

    def __init__(self, families, parent=None):
        super().__init__(parent)
        self.families = families
        self.family_by_folder = {f.folder: f for f in families}

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(12)

        t = QLabel("Review Lab")
        t.setObjectName("PageTitle")
        s = QLabel("Experimental corpus - regenerable. Never affects Production. "
                   "Select one or more families to review.")
        s.setObjectName("PageSubtitle")
        root.addWidget(t)
        root.addWidget(s)

        splitter = QSplitter(Qt.Horizontal)
        splitter.setChildrenCollapsible(False)

        left = QWidget()
        lv = QVBoxLayout(left)
        lv.setContentsMargins(0, 0, 8, 0)
        lv.setSpacing(6)
        lv.addWidget(self._section_label("FAMILIES"))

        self.family_checks = {}
        for f in families:
            cb = QCheckBox(f.artistic + "  (" + f.technical + ")")
            cb.setChecked(True)
            cb.toggled.connect(self._update_run_state)
            cb.clicked.connect(
                lambda _=False, fol=f.folder: self._show_details(fol))
            self.family_checks[f.folder] = cb
            lv.addWidget(cb)

        row = QHBoxLayout()
        btn_all = QPushButton("SELECT ALL")
        btn_all.setProperty("class", "Ghost")
        btn_none = QPushButton("SELECT NONE")
        btn_none.setProperty("class", "Ghost")
        btn_all.clicked.connect(lambda: self._set_all(True))
        btn_none.clicked.connect(lambda: self._set_all(False))
        row.addWidget(btn_all)
        row.addWidget(btn_none)
        row.addStretch(1)
        lv.addLayout(row)
        lv.addStretch(1)

        right = QWidget()
        rv = QVBoxLayout(right)
        rv.setContentsMargins(8, 0, 0, 0)
        rv.setSpacing(6)
        rv.addWidget(self._section_label("FAMILY DETAILS"))

        self.details = QTextBrowser()
        self.details.setOpenExternalLinks(False)
        self.details.setStyleSheet(
            "QTextBrowser { background:#0a0d12; color:#c9d3e2; "
            "border:1px solid #232a36; border-radius:6px; padding:10px; "
            "font-family:Consolas; font-size:9pt; }")
        self.details.setText(
            "Click a family to inspect its grammars, palettes, "
            "parameters and audio profile.")
        rv.addWidget(self.details, 1)

        splitter.addWidget(left)
        splitter.addWidget(right)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        splitter.setSizes([320, 720])
        root.addWidget(splitter, 1)

        gb = QGroupBox("Review batch")
        form = QFormLayout(gb)
        self.sp_seeds = QSpinBox()
        self.sp_seeds.setRange(1, 25)
        self.sp_seeds.setValue(5)
        self.sp_seeds.valueChanged.connect(self._update_run_state)
        self.cb_seedmode = QComboBox()
        self.cb_seedmode.addItems(["RANDOM", "MANUAL"])
        self.cb_audio = QCheckBox("Audio ON")
        self.cb_audio.setChecked(True)
        form.addRow("Unique seeds per family", self.sp_seeds)
        form.addRow("Seed mode", self.cb_seedmode)
        form.addRow("", self.cb_audio)
        root.addWidget(gb)

        row2 = QHBoxLayout()
        self.btn_run = QPushButton("RUN REVIEW")
        self.btn_run.setProperty("class", "Primary")
        self.btn_cancel = QPushButton("CANCEL")
        self.btn_cancel.setProperty("class", "Ghost")
        self.btn_cancel.setEnabled(False)
        self.summary = QLabel("")
        self.summary.setStyleSheet("color:#8b96a8; font-family:Consolas;")
        row2.addWidget(self.btn_run)
        row2.addWidget(self.btn_cancel)
        row2.addWidget(self.summary, 1)
        root.addLayout(row2)

        self.info = QLabel("Awaiting run.")
        self.info.setStyleSheet("color:#8b96a8; font-family:Consolas;")
        root.addWidget(self.info)

        self.btn_run.clicked.connect(self._emit_run)
        self.btn_cancel.clicked.connect(
            lambda: self.request_run.emit({"cancel": True}))

        self._update_run_state()
        if families:
            self._show_details(families[0].folder)

    def _section_label(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet(
            "color:#8b96a8; font-weight:600; letter-spacing:1px; padding:2px 0;")
        return lbl

    def _set_all(self, value):
        for cb in self.family_checks.values():
            cb.setChecked(value)

    def preselect_families(self, folders):
        folders = set(folders)
        for fol, cb in self.family_checks.items():
            cb.blockSignals(True)
            cb.setChecked(fol in folders)
            cb.blockSignals(False)
        self._update_run_state()
        if folders:
            first = next(iter(folders))
            self._show_details(first)

    def _selected_folders(self):
        return [fol for fol, cb in self.family_checks.items() if cb.isChecked()]

    def _update_run_state(self):
        n = len(self._selected_folders())
        seeds = self.sp_seeds.value()
        total = n * seeds
        self.summary.setText(
            str(n) + " famil(ies) x " + str(seeds) + " seeds = "
            + str(total) + " renders")
        self.btn_run.setEnabled(n > 0)

    def _show_details(self, folder):
        f = self.family_by_folder.get(folder)
        if not f:
            return
        html = []
        html.append("<div style='font-size:13pt; color:#e6edf3;'><b>"
                    + f.artistic + "</b></div>")
        html.append("<div style='color:#7ad7ff;'>" + f.technical
                    + "  |  " + f.id + "</div>")
        html.append("<br>")
        if f.short_description:
            html.append("<div>" + f.short_description + "</div>")
        if f.visual_metaphor:
            html.append("<div style='color:#8b96a8;'><i>"
                        + f.visual_metaphor + "</i></div>")
        html.append("<br>")
        html.append("<div style='color:#8b96a8;'><b>GRAMMARS ("
                    + str(len(f.grammars)) + ")</b></div>")
        if f.grammars:
            for g in f.grammars:
                html.append("<div>  - " + g + "</div>")
        else:
            html.append("<div>  (none declared)</div>")
        html.append("<br>")
        html.append("<div style='color:#8b96a8;'><b>PALETTE BANK</b></div>")
        html.append("<div>  " + (", ".join(f.palette_bank)
                                 if f.palette_bank else "-") + "</div>")
        html.append("<br>")
        html.append("<div style='color:#8b96a8;'><b>PARAMETERS ("
                    + str(len(f.parameters)) + ")</b></div>")
        if f.parameters:
            html.append("<pre style='font-family:Consolas; font-size:9pt;'>")
            for p in f.parameters:
                html.append(p.id.ljust(24) + "  " + p.type.ljust(8)
                            + "  [" + p.state + "]")
            html.append("</pre>")
        else:
            html.append("<div>  (none declared)</div>")
        html.append("<br>")
        html.append("<div style='color:#8b96a8;'><b>AUDIO PROFILE</b></div>")
        html.append("<div>  " + f.audio_profile + "</div>")
        html.append("<div style='color:#8b96a8;'><b>DEFAULT DURATION</b></div>")
        html.append("<div>  " + str(f.default_duration) + " s</div>")
        self.details.setHtml("".join(html))

    def _emit_run(self):
        folders = self._selected_folders()
        if not folders:
            return
        self.request_run.emit({
            "seed_count": self.sp_seeds.value(),
            "seed_mode": self.cb_seedmode.currentText(),
            "audio": self.cb_audio.isChecked(),
            "families": folders,
        })

    def set_running(self, running):
        enabled = (not running) and len(self._selected_folders()) > 0
        self.btn_run.setEnabled(enabled)
        self.btn_cancel.setEnabled(running)
        self.info.setText("RUNNING..." if running else "Idle.")

###<FILE>c11c_studio/ui/pages/production.py
import random

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QSpinBox, QComboBox, QGroupBox,
                               QFormLayout, QCheckBox, QMessageBox)
from PySide6.QtCore import Signal


def _unique_random_seeds(n):
    seen = set()
    out = []
    while len(out) < n:
        s = random.randint(1, 2147483647)
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out


class ProductionPage(QWidget):
    request_single = Signal(dict)
    request_5x5 = Signal(dict)

    def __init__(self, families, parent=None):
        super().__init__(parent)
        self.families = families
        self.family_by_folder = {f.folder: f for f in families}
        self._pending_5x5_seeds = None

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(14)

        t = QLabel("Production")
        t.setObjectName("PageTitle")
        s = QLabel("Protected zone - one canonical MP4 per product. "
                   "Existing products are not overwritten.")
        s.setObjectName("PageSubtitle")
        root.addWidget(t)
        root.addWidget(s)

        gb1 = QGroupBox("Single Product")
        f1 = QFormLayout(gb1)

        self.cb_family = QComboBox()
        for f in families:
            self.cb_family.addItem(
                f.artistic + "  (" + f.technical + ")", f.folder)
        self.cb_family.currentIndexChanged.connect(self._refresh_grammars)

        self.cb_grammar = QComboBox()
        self.cb_grammar.setEnabled(False)
        self.cb_grammar.currentIndexChanged.connect(self._update_run_state)

        self.chk_send_grammar = QCheckBox(
            "Send -Grammar to backend (only if the .ps1 supports it)")
        self.chk_send_grammar.setChecked(False)
        self.chk_send_grammar.toggled.connect(self._on_send_grammar_toggled)

        self.lbl_grammar_hint = QLabel("")
        self.lbl_grammar_hint.setStyleSheet(
            "color:#8b96a8; font-family:Consolas; font-size:8pt;")
        self.lbl_grammar_hint.setWordWrap(True)

        grammar_row = QVBoxLayout()
        grammar_row.setSpacing(2)
        grammar_row.addWidget(self.cb_grammar)
        grammar_row.addWidget(self.chk_send_grammar)
        grammar_row.addWidget(self.lbl_grammar_hint)

        seed_row = QHBoxLayout()
        self.sp_seed = QSpinBox()
        self.sp_seed.setRange(1, 2147483647)
        self.sp_seed.setValue(271828)
        self.btn_random_seed = QPushButton("RANDOM")
        self.btn_random_seed.setProperty("class", "Ghost")
        self.btn_random_seed.setFixedWidth(90)
        self.btn_random_seed.clicked.connect(self._randomize_single_seed)
        seed_row.addWidget(self.sp_seed, 1)
        seed_row.addWidget(self.btn_random_seed)

        self.cb_audio_s = QCheckBox("Audio ON")
        self.cb_audio_s.setChecked(True)
        self.cb_footer_s = QCheckBox("Footer ON")
        self.cb_footer_s.setChecked(True)

        f1.addRow("Family", self.cb_family)
        f1.addRow("Grammar / Subfamily", grammar_row)
        f1.addRow("Seed", seed_row)
        f1.addRow("", self.cb_audio_s)
        f1.addRow("", self.cb_footer_s)
        root.addWidget(gb1)

        b1 = QHBoxLayout()
        self.btn_single = QPushButton("PRODUCE FINAL")
        self.btn_single.setProperty("class", "Primary")
        b1.addWidget(self.btn_single)
        b1.addStretch(1)
        root.addLayout(b1)

        gb2 = QGroupBox("Production 5x5 (25 final products)")
        f2 = QFormLayout(gb2)
        self.sp_seeds5 = QSpinBox()
        self.sp_seeds5.setRange(1, 25)
        self.sp_seeds5.setValue(5)
        self.sp_seeds5.valueChanged.connect(self._reset_5x5_preview)

        self.cb_seedmode5 = QComboBox()
        self.cb_seedmode5.addItems(["RANDOM", "MANUAL"])
        self.cb_audio5 = QCheckBox("Audio ON")
        self.cb_audio5.setChecked(True)
        self.cb_footer5 = QCheckBox("Footer ON")
        self.cb_footer5.setChecked(True)

        self.lbl_preview = QLabel("(seeds will be generated at run time)")
        self.lbl_preview.setStyleSheet(
            "color:#8b96a8; font-family:Consolas; font-size:9pt;")
        self.lbl_preview.setWordWrap(True)

        self.btn_gen_seeds = QPushButton("GENERATE SEEDS NOW")
        self.btn_gen_seeds.setProperty("class", "Ghost")
        self.btn_gen_seeds.clicked.connect(self._pregen_5x5_seeds)

        preview_row = QHBoxLayout()
        preview_row.addWidget(self.lbl_preview, 1)
        preview_row.addWidget(self.btn_gen_seeds)

        f2.addRow("Unique seeds", self.sp_seeds5)
        f2.addRow("Seed mode", self.cb_seedmode5)
        f2.addRow("", self.cb_audio5)
        f2.addRow("", self.cb_footer5)
        f2.addRow("Preview", preview_row)
        root.addWidget(gb2)

        b2 = QHBoxLayout()
        self.btn_5x5 = QPushButton("PRODUCE 25 FINAL PRODUCTS")
        self.btn_5x5.setProperty("class", "Primary")
        b2.addWidget(self.btn_5x5)
        b2.addStretch(1)
        root.addLayout(b2)

        self.info = QLabel("Idle.")
        self.info.setStyleSheet("color:#8b96a8; font-family:Consolas;")
        root.addWidget(self.info)
        root.addStretch(1)

        self.btn_single.clicked.connect(self._emit_single)
        self.btn_5x5.clicked.connect(self._emit_5x5)

        self._refresh_grammars()

    def _on_send_grammar_toggled(self, checked):
        has_grammars = self.cb_grammar.count() > 1
        self.cb_grammar.setEnabled(checked and has_grammars)
        self._update_run_state()

    def _refresh_grammars(self):
        folder = self.cb_family.currentData()
        f = self.family_by_folder.get(folder)
        self.cb_grammar.blockSignals(True)
        self.cb_grammar.clear()
        self.cb_grammar.addItem("AUTO / RANDOM (seed-derived)", None)
        if f and f.grammars:
            for g in f.grammars:
                self.cb_grammar.addItem(g, g)
        self.cb_grammar.blockSignals(False)

        if f and f.grammars:
            self.lbl_grammar_hint.setText(
                str(len(f.grammars)) + " declared grammars for "
                + f.artistic + ". Backend v2.1.4 does NOT accept "
                "-Grammar (seed-derived). Enable the checkbox above only "
                "if your .ps1 supports it.")
        else:
            self.lbl_grammar_hint.setText(
                "No grammars declared for this family. The backend derives "
                "the grammar from the seed.")

        self.cb_grammar.setEnabled(
            self.chk_send_grammar.isChecked() and self.cb_grammar.count() > 1)
        self._update_run_state()

    def _update_run_state(self):
        pass

    def _randomize_single_seed(self):
        self.sp_seed.setValue(random.randint(1, 2147483647))

    def _reset_5x5_preview(self):
        self._pending_5x5_seeds = None
        self.lbl_preview.setText("(seeds will be generated at run time)")

    def _pregen_5x5_seeds(self):
        n = self.sp_seeds5.value()
        seeds = _unique_random_seeds(n)
        self._pending_5x5_seeds = seeds
        self.lbl_preview.setText(", ".join(str(s) for s in seeds))

    def _grammar_payload(self):
        if not self.chk_send_grammar.isChecked():
            return (None, False)
        g = self.cb_grammar.currentData()
        return (g, bool(g))

    def _emit_single(self):
        g, allow = self._grammar_payload()
        self.request_single.emit({
            "family": self.cb_family.currentData(),
            "grammar": g,
            "allow_grammar": allow,
            "seed": self.sp_seed.value(),
            "audio": self.cb_audio_s.isChecked(),
            "footer": self.cb_footer_s.isChecked(),
        })

    def _emit_5x5(self):
        resp = QMessageBox.question(
            self, "Confirm production 5x5",
            "Produce up to 25 canonical final products.\n\n"
            "Existing products will NOT be overwritten (safe default).\n\n"
            "Proceed?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if resp != QMessageBox.Yes:
            return

        if self._pending_5x5_seeds:
            seeds_payload = list(self._pending_5x5_seeds)
        else:
            seeds_payload = None

        g, allow = self._grammar_payload()

        self.request_5x5.emit({
            "seed_count": self.sp_seeds5.value(),
            "seed_mode": self.cb_seedmode5.currentText(),
            "families": [f.folder for f in self.families],
            "audio": self.cb_audio5.isChecked(),
            "footer": self.cb_footer5.isChecked(),
            "pre_generated_seeds": seeds_payload,
            "grammar": g,
            "allow_grammar": allow,
        })

    def set_running(self, running):
        self.btn_single.setEnabled(not running)
        self.btn_5x5.setEnabled(not running)
        self.btn_random_seed.setEnabled(not running)
        self.btn_gen_seeds.setEnabled(not running)
        self.info.setText("RUNNING..." if running else "Idle.")

###<FILE>c11c_studio/ui/pages/families.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QFrame, QPushButton, QScrollArea, QGridLayout)
from PySide6.QtCore import Signal


class FamilyCard(QFrame):
    review_requested = Signal(str)
    open_folder_requested = Signal(str)

    def __init__(self, family, parent=None):
        super().__init__(parent)
        self.family = family
        self.setObjectName("Card")

        v = QVBoxLayout(self)
        v.setContentsMargins(14, 12, 14, 12)
        v.setSpacing(6)

        name = QLabel(family.artistic.upper())
        name.setStyleSheet("font-size:13pt; font-weight:600;")
        tech = QLabel(family.technical)
        tech.setStyleSheet("color:#7ad7ff; font-family:Consolas;")
        v.addWidget(name)
        v.addWidget(tech)

        desc = QLabel(family.short_description or family.visual_metaphor or "")
        desc.setWordWrap(True)
        desc.setStyleSheet("color:#b7c1d3;")
        v.addWidget(desc)

        g = ", ".join(family.grammars) if family.grammars else "-"
        p = ", ".join(family.palette_bank) if family.palette_bank else "-"
        meta = QLabel("GRAMMAR: " + g + "\nPALETTE: " + p
                      + "\nPARAMS : " + str(len(family.parameters)))
        meta.setStyleSheet("color:#8b96a8; font-family:Consolas;")
        v.addWidget(meta)

        row = QHBoxLayout()
        btn_r = QPushButton("REVIEW")
        btn_r.setProperty("class", "Primary")
        btn_o = QPushButton("OPEN FOLDER")
        btn_o.setProperty("class", "Ghost")
        row.addWidget(btn_r)
        row.addWidget(btn_o)
        row.addStretch(1)
        v.addLayout(row)

        btn_r.clicked.connect(
            lambda: self.review_requested.emit(self.family.folder))
        btn_o.clicked.connect(
            lambda: self.open_folder_requested.emit(self.family.folder))


class FamiliesPage(QWidget):
    request_review = Signal(str)
    request_open_folder = Signal(str)

    def __init__(self, families, parent=None):
        super().__init__(parent)
        self.families = families

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        t = QLabel("Families")
        t.setObjectName("PageTitle")
        s = QLabel("Discovered from tools/prototypes - dynamic, metadata-driven. "
                   "Click REVIEW to inspect a family, or OPEN FOLDER to browse it.")
        s.setObjectName("PageSubtitle")
        root.addWidget(t)
        root.addWidget(s)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        holder = QWidget()
        grid = QGridLayout(holder)
        grid.setSpacing(14)
        for i, fam in enumerate(families):
            card = FamilyCard(fam)
            card.review_requested.connect(self.request_review)
            card.open_folder_requested.connect(self.request_open_folder)
            grid.addWidget(card, i // 2, i % 2)
        scroll.setWidget(holder)
        root.addWidget(scroll, 1)

###<FILE>c11c_studio/ui/pages/seeds.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QSpinBox, QComboBox, QTableWidget,
                               QTableWidgetItem, QHeaderView)
from PySide6.QtCore import Qt


class SeedsPage(QWidget):
    def __init__(self, seed_manager, parent=None):
        super().__init__(parent)
        self.sm = seed_manager

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(14)

        t = QLabel("Seeds"); t.setObjectName("PageTitle")
        s = QLabel("Seed is a reproduction identifier - same 5 seeds "
                   "cross all 5 families for 5x5.")
        s.setObjectName("PageSubtitle")
        root.addWidget(t); root.addWidget(s)

        row = QHBoxLayout()
        self.sp_count = QSpinBox(); self.sp_count.setRange(1, 100)
        self.sp_count.setValue(5)
        self.cb_mode = QComboBox(); self.cb_mode.addItems(["RANDOM", "MANUAL"])
        self.btn_generate = QPushButton("GENERATE")
        self.btn_save = QPushButton("SAVE BATCH")
        row.addWidget(QLabel("Count:")); row.addWidget(self.sp_count)
        row.addWidget(QLabel("Mode:")); row.addWidget(self.cb_mode)
        row.addWidget(self.btn_generate); row.addWidget(self.btn_save)
        row.addStretch(1)
        root.addLayout(row)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Seed", "Source", "Batch", "Created"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        root.addWidget(self.table, 1)

        self.btn_generate.clicked.connect(self._generate)
        self.btn_save.clicked.connect(self._save)

    def _generate(self):
        n = self.sp_count.value()
        if self.cb_mode.currentText() == "RANDOM":
            self.sm.random_batch(n)
        else:
            self.sm.manual_batch(list(range(1000, 1000 + n)))
        self._refresh()

    def _save(self):
        if self.sm.records:
            p = self.sm.save_batch(self.sm.records[-5:])
            self.window().statusBar().showMessage("Saved " + p.name, 4000)

    def _refresh(self):
        self.table.setRowCount(0)
        for r in self.sm.records:
            i = self.table.rowCount(); self.table.insertRow(i)
            vals = [str(r.seed), r.source, r.batch_id or "-", r.created_at]
            for c, txt in enumerate(vals):
                it = QTableWidgetItem(txt)
                it.setFlags(it.flags() ^ Qt.ItemIsEditable)
                self.table.setItem(i, c, it)

###<FILE>c11c_studio/ui/pages/artifacts.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTableWidget,
                               QTableWidgetItem, QHeaderView, QPushButton,
                               QHBoxLayout, QMessageBox)
from PySide6.QtCore import Qt


def _human(n):
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return "%.1f %s" % (n, unit)
        n /= 1024
    return "%.1f PB" % n


class ArtifactsPage(QWidget):
    def __init__(self, registry, parent=None):
        super().__init__(parent)
        self.registry = registry

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(14)

        t = QLabel("Artifacts"); t.setObjectName("PageTitle")
        s = QLabel("Classification & dry-run cleanup. Production, QA, "
                   "Regression, Releases, Legacy, Tests are protected.")
        s.setObjectName("PageSubtitle")
        root.addWidget(t); root.addWidget(s)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(
            ["Root", "Protection", "Files", "Size", "Path"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        root.addWidget(self.table, 1)

        row = QHBoxLayout()
        self.btn_refresh = QPushButton("REFRESH")
        self.btn_dry = QPushButton("PREVIEW CLEANUP (scratch only)")
        row.addWidget(self.btn_refresh); row.addWidget(self.btn_dry)
        row.addStretch(1)
        root.addLayout(row)

        self.btn_refresh.clicked.connect(self.refresh)
        self.btn_dry.clicked.connect(self._dry_run)
        self.refresh()

    def refresh(self):
        self.table.setRowCount(0)
        for root in self.registry.roots():
            r = self.table.rowCount(); self.table.insertRow(r)
            lock = "[LOCK] " if self.registry.is_protected(root.key) else ""
            vals = [root.label, lock + root.protection, str(root.file_count),
                    _human(root.size_bytes), str(root.path)]
            for c, txt in enumerate(vals):
                it = QTableWidgetItem(txt)
                it.setFlags(it.flags() ^ Qt.ItemIsEditable)
                self.table.setItem(r, c, it)

    def _dry_run(self):
        scratch = None
        for r in self.registry.roots():
            if r.key == "scratch":
                scratch = r
                break
        if not scratch or not scratch.exists:
            QMessageBox.information(self, "Dry-run",
                                    "Scratch root does not exist.")
            return
        QMessageBox.information(
            self, "Dry-run: SCRATCH only",
            "Target: " + str(scratch.path) + "\n"
            "Files: " + str(scratch.file_count) + "\n"
            "Size: " + _human(scratch.size_bytes) + "\n\n"
            "No deletion will occur automatically. Production and evidence "
            "roots are never touched.")

###<FILE>c11c_studio/ui/pages/logs.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QComboBox, QLineEdit)
from ..widgets.log_view import LogView


class LogsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(10)

        t = QLabel("Logs"); t.setObjectName("PageTitle")
        s = QLabel("Raw stdout/stderr is preserved verbatim. No line is dropped.")
        s.setObjectName("PageSubtitle")
        root.addWidget(t); root.addWidget(s)

        row = QHBoxLayout()
        self.cb_filter = QComboBox(); self.cb_filter.addItems(
            ["ALL", "INFO", "WARN", "ERROR"])
        self.le_search = QLineEdit()
        self.le_search.setPlaceholderText("Search...")
        self.btn_clear = QPushButton("CLEAR")
        self.btn_open = QPushButton("OPEN RAW LOG")
        row.addWidget(QLabel("Filter:")); row.addWidget(self.cb_filter)
        row.addWidget(self.le_search)
        row.addWidget(self.btn_clear); row.addWidget(self.btn_open)
        row.addStretch(1)
        root.addLayout(row)

        self.view = LogView()
        root.addWidget(self.view, 1)

        self.btn_clear.clicked.connect(self.view.clear_log)

###<FILE>c11c_studio/ui/pages/validation.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                               QTableWidget, QTableWidgetItem, QHeaderView,
                               QHBoxLayout)
from PySide6.QtGui import QColor


class ValidationPage(QWidget):
    def __init__(self, ctx, parent=None):
        super().__init__(parent)
        self.ctx = ctx

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(12)

        t = QLabel("Validation Center"); t.setObjectName("PageTitle")
        s = QLabel("Preflight checks. PASS / WARN / FAIL.")
        s.setObjectName("PageSubtitle")
        root.addWidget(t); root.addWidget(s)

        row = QHBoxLayout()
        self.btn_run = QPushButton("RUN ALL")
        row.addWidget(self.btn_run); row.addStretch(1)
        root.addLayout(row)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Check", "Status", "Message"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        root.addWidget(self.table, 1)

        self.btn_run.clicked.connect(self.run)

    def run(self):
        from ...services.environment_validator import EnvironmentValidator
        report = EnvironmentValidator(self.ctx).run_all()
        self.table.setRowCount(0)
        for c in report.checks:
            r = self.table.rowCount(); self.table.insertRow(r)
            for col, txt in enumerate([c.name, c.status, c.message]):
                it = QTableWidgetItem(txt)
                if col == 1:
                    if c.status == "PASS":
                        it.setForeground(QColor("#6ee7a7"))
                    elif c.status == "WARN":
                        it.setForeground(QColor("#f5c451"))
                    else:
                        it.setForeground(QColor("#ff8080"))
                self.table.setItem(r, col, it)

###<FILE>c11c_studio/ui/pages/settings.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QGroupBox,
                               QLabel, QLineEdit, QPushButton, QHBoxLayout,
                               QFileDialog)
from PySide6.QtCore import Signal


class SettingsPage(QWidget):
    project_changed = Signal(str)

    def __init__(self, ctx, cfg, parent=None):
        super().__init__(parent)
        self.ctx = ctx
        self.cfg = cfg

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(14)

        t = QLabel("Settings"); t.setObjectName("PageTitle")
        root.addWidget(t)

        gb = QGroupBox("General")
        f = QFormLayout(gb)
        self.le_project = QLineEdit(str(self.ctx.project_root))
        self.le_project.setReadOnly(True)
        btn_pick = QPushButton("..."); btn_pick.setFixedWidth(32)
        row = QHBoxLayout()
        row.addWidget(self.le_project); row.addWidget(btn_pick)
        f.addRow("Project root", row)

        gb_del = QGroupBox("Delivery (read-only in v0.1)")
        fd = QFormLayout(gb_del)
        fd.addRow(QLabel("%dx%d @ %d FPS - %.2fs (%d frames)" % (
            self.ctx.delivery_width, self.ctx.delivery_height, self.ctx.fps,
            self.ctx.default_duration, self.ctx.default_frames)))
        fd.addRow(QLabel("Logical: %dx%d (Header 0-144 / Body 144-816 / "
                         "Footer 816-960)" % (
            self.ctx.logical_width, self.ctx.logical_height)))

        gb_ver = QGroupBox("Versions")
        fv = QFormLayout(gb_ver)
        fv.addRow("Backend", QLabel(self.ctx.backend_version))
        fv.addRow("C11-B", QLabel(self.ctx.c11b_state))

        root.addWidget(gb); root.addWidget(gb_del); root.addWidget(gb_ver)
        root.addStretch(1)
        btn_pick.clicked.connect(self._pick)

    def _pick(self):
        p = QFileDialog.getExistingDirectory(
            self, "Select project root", str(self.ctx.project_root))
        if p:
            self.le_project.setText(p)
            self.cfg.set("project_root", p)
            self.cfg.save()
            self.project_changed.emit(p)

###<FILE>c11c_studio/ui/pages/about.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class AboutPage(QWidget):
    def __init__(self, ctx, app_version, parent=None):
        super().__init__(parent)
        v = QVBoxLayout(self)
        v.setContentsMargins(24, 20, 24, 20)
        v.setSpacing(8)

        v.addWidget(QLabel("<h2>C11-C Studio</h2>"))
        v.addWidget(QLabel("GUI version: " + app_version))
        v.addWidget(QLabel("Backend reference: " + ctx.backend_version))
        v.addWidget(QLabel("C11-B: " + ctx.c11b_state))
        v.addWidget(QLabel("Architecture: GUI -> canonical toolchain -> "
                           "Godot/Python/FFmpeg/FFprobe -> artifacts"))
        v.addWidget(QLabel("Rule: the GUI can control the system; "
                           "the GUI must not become the system."))
        v.addStretch(1)

###<FILE>c11c_studio/ui/main_window.py
from datetime import datetime

from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                               QLabel, QFrame, QStackedWidget, QStatusBar,
                               QMessageBox)
from PySide6.QtCore import QTimer, QUrl
from PySide6.QtGui import QDesktopServices

from ..core.config import AppConfig
from ..services.tool_discovery import discover_all
from ..services.family_registry import FamilyRegistry
from ..services.seed_manager import SeedManager
from ..services.command_builder import CommandBuilder
from ..services.job_manager import JobManager
from ..services.artifact_registry import ArtifactRegistry

from .widgets.nav_button import NavButton
from .pages.dashboard import DashboardPage
from .pages.review import ReviewPage
from .pages.production import ProductionPage
from .pages.families import FamiliesPage
from .pages.seeds import SeedsPage
from .pages.artifacts import ArtifactsPage
from .pages.logs import LogsPage
from .pages.validation import ValidationPage
from .pages.settings import SettingsPage
from .pages.about import AboutPage


class MainWindow(QMainWindow):
    def __init__(self, ctx, app_version="0.1.0"):
        super().__init__()
        self.ctx = ctx
        self.app_version = app_version
        self.cfg = AppConfig.load()

        self.family_registry = FamilyRegistry(ctx)
        self.families = self.family_registry.load()

        self.tools = discover_all(ctx.project_root)
        if self.tools.get("powershell") and self.tools["powershell"].present:
            ctx.powershell_path = self.tools["powershell"].path
        if self.tools.get("ffmpeg") and self.tools["ffmpeg"].present:
            ctx.ffmpeg_path = self.tools["ffmpeg"].path
        if self.tools.get("ffprobe") and self.tools["ffprobe"].present:
            ctx.ffprobe_path = self.tools["ffprobe"].path
        if self.tools.get("godot") and self.tools["godot"].present:
            ctx.godot_version = self.tools["godot"].version
        ctx.python_path = self.tools["python"].path

        self.seed_manager = SeedManager(ctx.paths.scratch / "seeds")
        self.command_builder = CommandBuilder(ctx)
        self.artifact_registry = ArtifactRegistry(ctx)
        self.job_manager = JobManager(log_dir=ctx.paths.scratch / "logs")

        self.job_manager.job_output.connect(self._on_job_output)
        self.job_manager.job_finished.connect(self._on_job_finished)
        self.job_manager.job_state_changed.connect(self._on_job_state)

        self.setWindowTitle("C11-C Studio - " + ctx.project_root.name)
        self.setMinimumSize(1024, 640)
        self.resize(1360, 860)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        root.addWidget(self._build_topbar())

        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)
        body.addWidget(self._build_nav())
        self.stack = QStackedWidget()
        body.addWidget(self.stack, 1)
        body_w = QWidget()
        body_w.setLayout(body)
        root.addWidget(body_w, 1)

        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("Ready.")

        self._build_pages()
        self._wire()
        self._refresh_dashboard_counts()

        self._timer = QTimer(self)
        self._timer.setInterval(15000)
        self._timer.timeout.connect(self._refresh_env_badge)
        self._timer.start()

    def _build_topbar(self):
        bar = QFrame()
        bar.setObjectName("TopBar")
        bar.setFixedHeight(56)
        h = QHBoxLayout(bar)
        h.setContentsMargins(16, 8, 16, 8)

        title = QLabel("C11-C Studio")
        title.setObjectName("TopBarTitle")
        h.addWidget(title)

        self.env_meta = QLabel(self._env_summary())
        self.env_meta.setObjectName("TopBarMeta")
        h.addWidget(self.env_meta)
        h.addStretch(1)

        project = QLabel("Project: " + str(self.ctx.project_root))
        project.setObjectName("TopBarMeta")
        h.addWidget(project)
        return bar

    def _env_summary(self):
        g = self.tools.get("godot")
        f1 = self.tools.get("ffmpeg")
        f2 = self.tools.get("ffprobe")
        gtag = ("OK " + (g.version or "")) if g and g.present else "MISSING"
        ftag = "OK" if f1 and f1.present else "MISSING"
        ptag = "OK" if f2 and f2.present else "MISSING"
        return ("Backend: " + self.ctx.backend_version + "   |   "
                "Godot: " + gtag + "   |   "
                "FFmpeg: " + ftag + "   |   "
                "FFprobe: " + ptag)

    def _refresh_env_badge(self):
        self.env_meta.setText(self._env_summary())

    def _build_nav(self):
        rail = QFrame()
        rail.setObjectName("NavRail")
        rail.setFixedWidth(210)
        v = QVBoxLayout(rail)
        v.setContentsMargins(10, 14, 10, 14)
        v.setSpacing(4)

        self.nav_buttons = []
        items = [
            ("Dashboard", 0), ("Review", 1), ("Production", 2),
            ("Families", 3), ("Seeds", 4), ("Artifacts", 5),
            ("Logs", 6), ("Validation", 7), ("Settings", 8),
            ("About / Diagnostics", 9),
        ]
        for label, idx in items:
            b = NavButton(label)
            b.clicked.connect(lambda _=False, i=idx: self._goto(i))
            v.addWidget(b)
            self.nav_buttons.append(b)
        v.addStretch(1)
        self.nav_buttons[0].setChecked(True)
        return rail

    def _build_pages(self):
        self.dashboard = DashboardPage(self.ctx, self.tools)
        self.review = ReviewPage(self.families)
        self.production = ProductionPage(self.families)
        self.families_page = FamiliesPage(self.families)
        self.seeds_page = SeedsPage(self.seed_manager)
        self.artifacts_page = ArtifactsPage(self.artifact_registry)
        self.logs_page = LogsPage()
        self.validation_page = ValidationPage(self.ctx)
        self.settings_page = SettingsPage(self.ctx, self.cfg)
        self.about_page = AboutPage(self.ctx, self.app_version)

        for w in (self.dashboard, self.review, self.production,
                  self.families_page, self.seeds_page, self.artifacts_page,
                  self.logs_page, self.validation_page, self.settings_page,
                  self.about_page):
            self.stack.addWidget(w)

    def _wire(self):
        self.dashboard.btn_validate.clicked.connect(self._goto_validate)
        self.dashboard.btn_review.clicked.connect(lambda: self._goto(1))
        self.dashboard.btn_produce.clicked.connect(lambda: self._goto(2))
        self.dashboard.btn_single.clicked.connect(lambda: self._goto(2))

        self.review.request_run.connect(self._on_review_run)
        self.production.request_single.connect(self._on_single_run)
        self.production.request_5x5.connect(self._on_5x5_run)

        self.families_page.request_review.connect(self._on_family_review)
        self.families_page.request_open_folder.connect(
            self._on_family_open_folder)

    def _goto(self, idx):
        self.stack.setCurrentIndex(idx)
        for i, b in enumerate(self.nav_buttons):
            b.setChecked(i == idx)

    def _goto_validate(self):
        self._goto(7)
        self.validation_page.run()

    def _on_family_review(self, folder):
        self.review.preselect_families([folder])
        self._goto(1)

    def _on_family_open_folder(self, folder):
        p = self.ctx.paths.prototypes / folder
        if not p.exists():
            alt = self.ctx.paths.review_assets / folder
            if alt.exists():
                p = alt
            else:
                QMessageBox.warning(
                    self, "Folder not found",
                    "Neither prototype nor review folder exists for:\n"
                    + folder + "\n\nLooked in:\n"
                    + str(self.ctx.paths.prototypes / folder) + "\n"
                    + str(alt))
                return
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(p)))

    def trigger_review_5x5(self):
        self._goto(1)
        self._on_review_run({
            "seed_count": 5,
            "audio": True,
            "families": [f.folder for f in self.families],
        })

    def trigger_production_25(self):
        self._goto(2)
        self._on_5x5_run({
            "seed_count": 5,
            "families": [f.folder for f in self.families],
            "audio": True,
            "footer": True,
            "pre_generated_seeds": None,
            "grammar": None,
            "allow_grammar": False,
        })

    def _on_review_run(self, cfg):
        if cfg.get("cancel"):
            self.job_manager.cancel_current()
            return
        folders = cfg.get("families", [])
        if not folders:
            QMessageBox.warning(self, "No families",
                                "Select at least one family to review.")
            return
        recs = self.seed_manager.random_batch(cfg.get("seed_count", 5))
        seeds = [r.seed for r in recs]
        spec = self.command_builder.review_5x5(
            seeds, folders, audio=cfg.get("audio", True))
        self._start("review_5x5", spec, cfg, seeds)
        self.review.set_running(True)

    def _on_single_run(self, cfg):
        spec = self.command_builder.production_single(
            cfg["family"], cfg["seed"],
            audio=cfg.get("audio", True),
            grammar=cfg.get("grammar"),
            allow_grammar=cfg.get("allow_grammar", False))
        self._start("production_single", spec, cfg, [cfg["seed"]])
        self.production.set_running(True)

    def _on_5x5_run(self, cfg):
        pre = cfg.get("pre_generated_seeds")
        if pre:
            seeds = list(pre)
            self.seed_manager.manual_batch(seeds)
        else:
            recs = self.seed_manager.random_batch(cfg.get("seed_count", 5))
            seeds = [r.seed for r in recs]
        spec = self.command_builder.production_5x5(
            seeds, cfg.get("families", []),
            audio=cfg.get("audio", True),
            grammar=cfg.get("grammar"),
            allow_grammar=cfg.get("allow_grammar", False))
        self._start("production_5x5", spec, cfg, seeds)
        self.production.set_running(True)

    def _start(self, jtype, spec, cfg, seeds):
        self.logs_page.view.append_text(
            "\n=== " + jtype + " @ "
            + datetime.now().isoformat(timespec="seconds") + " ===\n"
            "$ " + spec.display_command + "\n")
        try:
            job = self.job_manager.start_job(jtype, spec)
        except RuntimeError as e:
            QMessageBox.warning(self, "Job busy", str(e))
            return
        self.statusBar().showMessage(
            "Running " + jtype + " (" + job.id + ")...")
        self.dashboard.add_job_row(
            datetime.now().strftime("%H:%M:%S"), jtype, "-",
            ",".join(map(str, seeds))[:40], "RUNNING", "-")
        self._goto(6)

    def _on_job_output(self, job_id, chunk):
        self.logs_page.view.append_text(chunk)

    def _on_job_state(self, job_id, state):
        self.statusBar().showMessage("Job " + job_id + ": " + state)

    def _on_job_finished(self, job_id, code):
        job = self.job_manager.jobs[job_id]
        self.statusBar().showMessage(
            "Job " + job_id + " finished (exit " + str(code) + ") - "
            + job.state.value, 8000)
        self.dashboard.add_job_row(
            datetime.now().strftime("%H:%M:%S"), job.job_type,
            job.family or "-", str(job.seed or "-"),
            job.state.value, "-")
        self.review.set_running(False)
        self.production.set_running(False)
        self._refresh_dashboard_counts()

        if code != 0:
            self.logs_page.view.append_text(
                "\n[FAIL] Job returned non-zero exit. See raw log at: "
                + str(job.log_path) + "\n")

    def _refresh_dashboard_counts(self):
        prod_dir = self.ctx.paths.production
        review_dir = self.ctx.paths.review_assets
        n_prod = sum(1 for _ in prod_dir.rglob("*.mp4")) if prod_dir.exists() else 0
        n_rev = sum(1 for _ in review_dir.rglob("*.mp4")) if review_dir.exists() else 0
        self.dashboard.set_counts(n_prod, n_rev, len(self.families))

###<END>
'''


def parse_blob(blob):
    files = {}
    cur = None
    buf = []

    def flush():
        if cur is not None:
            content = "\n".join(buf).rstrip("\n")
            if content:
                content += "\n"
            files[cur] = content

    for line in blob.split("\n"):
        if line.startswith("###<FILE>"):
            flush()
            cur = line[len("###<FILE>"):].strip()
            buf = []
        elif line.strip() == "###<END>":
            flush()
            cur = None
            break
        else:
            if cur is not None:
                buf.append(line)
    flush()
    return files


def write_project(target):
    files = parse_blob(BLOB)
    written = []
    for rel, content in files.items():
        p = target / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8", newline="\n")
        written.append(p)
    return written


def create_venv_and_install(target):
    venv_dir = target / ".venv"
    print("[boot] creating venv at " + str(venv_dir))
    r = subprocess.run([sys.executable, "-m", "venv", str(venv_dir)])
    if r.returncode != 0:
        print("[boot] ERROR: venv creation failed", file=sys.stderr)
        return r.returncode

    if os.name == "nt":
        py = venv_dir / "Scripts" / "python.exe"
    else:
        py = venv_dir / "bin" / "python"

    print("[boot] upgrading pip...")
    subprocess.run([str(py), "-m", "pip", "install", "--upgrade", "pip"],
                   check=False)

    print("[boot] installing requirements...")
    r = subprocess.run([str(py), "-m", "pip", "install", "-r",
                        str(target / "requirements.txt")])
    return r.returncode


def launch_app(target, project_root):
    if os.name == "nt":
        py = target / ".venv" / "Scripts" / "python.exe"
    else:
        py = target / ".venv" / "bin" / "python"
    if not py.exists():
        py = Path(sys.executable)

    cmd = [str(py), str(target / "main.py")]
    if project_root:
        cmd += ["--project", project_root]
    print("[boot] launching: " + " ".join(cmd))
    return subprocess.call(cmd)


def main():
    ap = argparse.ArgumentParser(prog="bootstrap_studio_v4")
    ap.add_argument("--target", default="c11c-studio")
    ap.add_argument("--install", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--project", default=None)
    args = ap.parse_args()

    target = Path(args.target).expanduser().resolve()
    target.mkdir(parents=True, exist_ok=True)

    print("[boot] target: " + str(target))
    written = write_project(target)
    print("[boot] wrote " + str(len(written)) + " files")

    rc = 0
    if args.install:
        rc = create_venv_and_install(target)
        if rc != 0:
            print("[boot] install failed", file=sys.stderr)
            return rc

    if args.run:
        return launch_app(target, args.project)

    print()
    print("=" * 60)
    print(" C11-C Studio bootstrapped.")
    print("=" * 60)
    print(" Project: " + str(target))
    print()
    print(" Next steps:")
    print("   cd " + str(target))
    if not args.install:
        print("   python -m venv .venv")
        print("   .venv\\Scripts\\activate.bat")
        print("   pip install -r requirements.txt")
    print("   python main.py --project \"D:\\Path\\To\\ChallengeEngineV01_STATELESS\"")
    print()
    print(" Or simply double-click run.bat (Windows).")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())