from pathlib import Path
from types import SimpleNamespace
from c11c_studio.services.command_builder import CommandBuilder

ROOT=Path(__file__).resolve().parent
BULK=ROOT/".contract_tools"/"c11c_bulk"
BULK.mkdir(parents=True, exist_ok=True)

class Catalog:
    def __init__(self, scripts): self.scripts={str(p):SimpleNamespace(parameters=set(params)) for p,params in scripts.items()}
    def script_supports(self, script, param): return param in self.scripts.get(str(script),SimpleNamespace(parameters=set())).parameters

class Paths:
    def __init__(self):
        self.bulk_tools=BULK
    def family_dir(self,f): return ROOT/"tools"/"prototypes"/f

class Ctx:
    project_root=ROOT
    paths=Paths()
    powershell_path="powershell.exe"

def main():
    scripts={}
    names=["validate_c11c_powershell.ps1","validate_c11c_delivery_configuration.ps1","validate_c11c_preflight.ps1","run_c11c_art_direction_review.ps1","run_c11c_production.ps1","run_c11c_production_bulk.ps1","run_all_c11c_visual_loops.ps1","clean_c11c_artifacts.ps1","reset_c11c_artifacts.ps1","export_all_review_assets.ps1","export_review_gifs.ps1","export_review_keyframes.ps1","retire_legacy_c11c_tool_versions.ps1"]
    for n in names:
        p=BULK/n; p.write_text("param()", encoding="utf-8"); scripts[p]={"NoSound","NoFooter","Force","ResetReviewAssets","Seed","Seeds","Family","Apply"}
    for f in CommandBuilder.CANONICAL_FAMILIES:
        p=Paths().family_dir(f)/"run_prototype.ps1"; p.parent.mkdir(parents=True, exist_ok=True); p.write_text("param()", encoding="utf-8"); scripts[p]={"Seed","NoSound","NoFooter"}
    b=CommandBuilder(Ctx(),Catalog(scripts))
    assert b.review([1,2,3,4,5],b.CANONICAL_FAMILIES).arguments[-6:]==["-Seeds","1","2","3","4","5"]
    assert b.production_single("c11c_geometric_waves_v1",271828).working_directory==str(ROOT)
    specs=b.production_25([1,2,3,4,5])
    assert len(specs)==5 and all("run_c11c_production_bulk.ps1" in s.arguments[4] for s in specs)
    assert b.prototype("c11c_geometric_waves_v1",271828).arguments[-2:]==["-Seed","271828"]
    print("C11-C Studio v0.4.0 command-contract PASS")

if __name__=="__main__": main()
