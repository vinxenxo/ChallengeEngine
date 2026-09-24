from dataclasses import dataclass,field
from .tool_discovery import discover_all
@dataclass
class CheckResult:name:str;status:str;message:str=""
@dataclass
class ValidationReport:
 checks:list=field(default_factory=list)
 def add(self,c):self.checks.append(c)
 def ok(self):return all(c.status!="FAIL" for c in self.checks)
 def lines(self):return [f"[{c.status}] {c.name}: {c.message}" for c in self.checks]
class EnvironmentValidator:
 def __init__(self,ctx):self.ctx=ctx
 def run_all(self):
  r=ValidationReport(); p=self.ctx.project_root
  r.add(CheckResult("project_root","PASS" if p.exists() else "FAIL",str(p)))
  tools=discover_all(p,self.ctx.tool_paths)
  for k in ("python","powershell","ffmpeg","ffprobe","godot"):
   t=tools[k]; req=k in ("python","powershell","ffmpeg","ffprobe"); st="PASS" if t.present else ("FAIL" if req else "WARN"); r.add(CheckResult(k,st,t.version or "not found"))
  bulk=self.ctx.paths.bulk_tools
  for f in ("validate_c11c_powershell.ps1","validate_c11c_delivery_configuration.ps1","validate_c11c_preflight.ps1","run_c11c_art_direction_review.ps1","run_all_c11c_visual_loops.ps1","run_c11c_production.ps1","run_c11c_production_bulk.ps1","export_review_gifs.ps1","export_review_keyframes.ps1","export_all_review_assets.ps1","clean_c11c_artifacts.ps1","reset_c11c_artifacts.ps1","retire_legacy_c11c_tool_versions.ps1"):
   r.add(CheckResult("tool."+f,"PASS" if (bulk/f).exists() else "WARN",str(bulk/f)))
  r.add(CheckResult("delivery","PASS",f"{self.ctx.delivery_width}x{self.ctx.delivery_height} @ {self.ctx.fps} FPS / {self.ctx.default_duration:.2f}s / {self.ctx.default_frames} frames"))
  fam=[d for d in self.ctx.paths.prototypes.glob("c11c_*_v1") if d.is_dir()] if self.ctx.paths.prototypes.exists() else []
  r.add(CheckResult("families","PASS" if len(fam)>=5 else "WARN",f"{len(fam)} family directories discovered"))
  for key in ("production","review_assets","qa","regression","releases","legacy","tests"):
   path=getattr(self.ctx.paths,key); r.add(CheckResult("artifact."+key,"PASS" if path.exists() else "WARN",str(path)))
  return r
