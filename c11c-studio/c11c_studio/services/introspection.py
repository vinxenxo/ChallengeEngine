import json
import re
from dataclasses import dataclass, field
from pathlib import Path

_PARAM_RE=re.compile(r"(?m)^\s*\[([A-Za-z0-9_\[\]]+)\]\s*\$([A-Za-z_][A-Za-z0-9_]*)")
_PARAM_NAME_RE=re.compile(r"(?m)^\s*(?:\[[^\]]+\]\s*)?\$([A-Za-z_][A-Za-z0-9_]*)")
_UNIFORM_RE=re.compile(r"(?m)^\s*uniform\s+([A-Za-z0-9_]+)\s+([A-Za-z_][A-Za-z0-9_]*)")

@dataclass
class ScriptCapability:
    path: Path
    parameters: dict[str,str]=field(default_factory=dict)

@dataclass
class BackendCatalog:
    scripts: dict[str,ScriptCapability]=field(default_factory=dict)
    shader_uniforms: dict[str,dict[str,str]]=field(default_factory=dict)
    json_files: list[str]=field(default_factory=list)
    json_keys: dict[str,list[str]]=field(default_factory=dict)
    grammar_names: dict[str,set[str]]=field(default_factory=dict)
    palette_names: dict[str,set[str]]=field(default_factory=dict)

class BackendIntrospector:
    def __init__(self,ctx): self.ctx=ctx; self.catalog=BackendCatalog()
    def scan(self):
        self._scan_scripts(); self._scan_shaders(); self._scan_json(); return self.catalog
    def _scan_scripts(self):
        paths=[]
        if self.ctx.paths.bulk_tools.exists(): paths += list(self.ctx.paths.bulk_tools.glob("*.ps1"))
        if self.ctx.paths.prototypes.exists():
            for d in self.ctx.paths.prototypes.glob("c11c_*_v1"):
                p=d/"run_prototype.ps1"
                if p.exists(): paths.append(p)
        for p in paths:
            try: txt=p.read_text(encoding="utf-8-sig",errors="ignore")
            except OSError: continue
            params={}
            m=re.search(r"(?is)^\s*param\s*\((.*?)\)\s*",txt)
            if m:
                block=m.group(1)
                typed={n:t for t,n in _PARAM_RE.findall(block)}
                for nm in _PARAM_NAME_RE.findall(block):
                    params[nm]=typed.get(nm,"unknown")
            self.catalog.scripts[str(p)]=ScriptCapability(p,params)
    def _scan_shaders(self):
        if not self.ctx.paths.prototypes.exists(): return
        for d in self.ctx.paths.prototypes.glob("c11c_*_v1"):
            for p in d.glob("*.gdshader"):
                try: txt=p.read_text(encoding="utf-8",errors="ignore")
                except OSError: continue
                self.catalog.shader_uniforms[str(p)]={n:t for t,n in _UNIFORM_RE.findall(txt)}
    def _scan_json(self):
        roots=[self.ctx.paths.common_tools,self.ctx.paths.review_assets,self.ctx.paths.production,self.ctx.project_root/"definitions",self.ctx.project_root/"profiles"]
        seen=set()
        for root in roots:
            if not root.exists(): continue
            for p in root.rglob("*.json"):
                sp=str(p)
                if sp in seen: continue
                seen.add(sp)
                try: data=json.loads(p.read_text(encoding="utf-8-sig"))
                except (OSError,ValueError): continue
                self.catalog.json_files.append(sp)
                self.catalog.json_keys[sp]=self._flatten(data)
                self._harvest(p.name,data)
    def _flatten(self,obj,prefix=""):
        out=[]
        if isinstance(obj,dict):
            for k,v in obj.items():
                key=f"{prefix}.{k}" if prefix else str(k); out.append(key); out.extend(self._flatten(v,key))
        elif isinstance(obj,list) and obj and isinstance(obj[0],dict):
            out.extend(self._flatten(obj[0],prefix+"[]"))
        return out
    def _harvest(self,name,obj):
        if isinstance(obj,dict):
            fam=str(obj.get("family",obj.get("family_id",""))).strip()
            vals=obj.get("grammars") or obj.get("grammar")
            if fam and vals:
                if isinstance(vals,str): vals=[vals]
                self.catalog.grammar_names.setdefault(fam,set()).update(map(str,vals))
            pals=obj.get("palettes") or obj.get("palette_bank")
            if fam and pals:
                if isinstance(pals,str): pals=[pals]
                self.catalog.palette_names.setdefault(fam,set()).update(map(str,pals))
            for v in obj.values(): self._harvest(name,v)
        elif isinstance(obj,list):
            for v in obj: self._harvest(name,v)
    def script_supports(self,script,param):
        cap=self.catalog.scripts.get(str(script)); return bool(cap and param in cap.parameters)
