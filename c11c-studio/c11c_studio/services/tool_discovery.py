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
