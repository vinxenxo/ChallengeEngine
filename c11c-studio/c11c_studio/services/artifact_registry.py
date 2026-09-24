from dataclasses import dataclass
from pathlib import Path
PROTECTED={"production","qa","regression","releases","legacy","tests"}
@dataclass
class ArtifactRoot:
 key:str; path:Path; label:str; protection:str; exists:bool; file_count:int=0; size_bytes:int=0
class ArtifactRegistry:
 def __init__(self,ctx):self.ctx=ctx
 def roots(self):
  p=self.ctx.paths; specs=[("production",p.production,"Production","PROTECTED"),("review",p.review_assets,"Review assets","REGENERABLE"),("prototypes",p.prototype_artifacts,"Prototype staging","EXPERIMENTAL"),("qa",p.qa,"QA evidence","PROTECTED"),("regression",p.regression,"Regression evidence","PROTECTED"),("releases",p.releases,"Releases","PROTECTED"),("legacy",p.legacy,"Legacy","PROTECTED"),("tests",p.tests,"Tests","PROTECTED"),("scratch",p.scratch,"Scratch","DISPOSABLE")]; out=[]
  for key,path,label,prot in specs:
   n=s=0
   if path.exists():
    for f in path.rglob("*"):
     try:
      if f.is_file():n+=1;s+=f.stat().st_size
     except OSError:pass
   out.append(ArtifactRoot(key,path,label,prot,path.exists(),n,s))
  return out
 def is_protected(self,key):return key in PROTECTED
