import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ToolInfo:
    key: str
    path: str | None
    version: str | None
    present: bool
    source: str


def _which(names):
    for n in names:
        p=shutil.which(n)
        if p:
            return p
    return None


def _version(cmd):
    if not cmd:
        return None
    try:
        r=subprocess.run(cmd,capture_output=True,text=True,timeout=8,check=False)
        lines=(r.stdout or r.stderr or "").strip().splitlines()
        return lines[0] if lines else None
    except (OSError, subprocess.SubprocessError):
        return None


def discover_all(root,overrides=None):
    root=Path(root).resolve(); overrides=overrides or {}
    def choose(key,names,candidates=()):
        ov=overrides.get(key)
        if ov and Path(ov).exists(): return str(Path(ov).resolve()),"CONFIG"
        p=_which(names)
        if p: return p,"PATH"
        for rel in candidates:
            q=root/rel
            if q.exists(): return str(q.resolve()),"PROJECT"
        return None,"MISSING"
    tools={}
    py=str(os.sys.executable)
    tools["python"]=ToolInfo("python",py,platform_python(),True,"CURRENT")
    ps,src=choose("powershell",["powershell.exe","pwsh.exe","powershell","pwsh"])
    tools["powershell"]=ToolInfo("powershell",ps,_version([ps,"-NoProfile","-Command","$PSVersionTable.PSVersion.ToString()"] if ps else []),bool(ps),src)
    ff,src=choose("ffmpeg",["ffmpeg.exe","ffmpeg"],["tools/bin/ffmpeg.exe"])
    fp,src2=choose("ffprobe",["ffprobe.exe","ffprobe"],["tools/bin/ffprobe.exe"])
    gd,src3=choose("godot",["godot.exe","Godot.exe","godot"],["tools/bin/godot.exe","tools/bin/Godot.exe"])
    tools["ffmpeg"]=ToolInfo("ffmpeg",ff,_version([ff,"-version"] if ff else []),bool(ff),src)
    tools["ffprobe"]=ToolInfo("ffprobe",fp,_version([fp,"-version"] if fp else []),bool(fp),src2)
    tools["godot"]=ToolInfo("godot",gd,_version([gd,"--version"] if gd else []),bool(gd),src3)
    return tools


def platform_python():
    import sys
    return ".".join(map(str,sys.version_info[:3]))
