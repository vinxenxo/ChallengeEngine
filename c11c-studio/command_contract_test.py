from pathlib import Path
from types import SimpleNamespace
from c11c_studio.services.command_builder import CommandBuilder

ROOT=Path(__file__).resolve().parent
BULK=ROOT/".contract_tools"/"c11c_bulk"

class Catalog:
    def __init__(self, scripts):
        self.scripts={str(p):SimpleNamespace(parameters=set(params)) for p,params in scripts.items()}
    def script_supports(self, script, param):
        return param in self.scripts.get(str(script),SimpleNamespace(parameters=set())).parameters

class Paths:
    def __init__(self): self.bulk_tools=BULK
    def family_dir(self,f): return ROOT/"tools"/"prototypes"/f

class Ctx:
    project_root=ROOT
    paths=Paths()
    powershell_path="powershell.exe"

def main():
    scripts={}
    names=[
        "validate_c11c_powershell.ps1","validate_c11c_delivery_configuration.ps1",
        "validate_c11c_preflight.ps1","run_c11c_art_direction_review.ps1",
        "run_c11c_production.ps1","run_c11c_production_bulk.ps1",
        "run_all_c11c_visual_loops.ps1","clean_c11c_artifacts.ps1",
        "reset_c11c_artifacts.ps1","export_all_review_assets.ps1",
        "export_review_gifs.ps1","export_review_keyframes.ps1",
        "retire_legacy_c11c_tool_versions.ps1"
    ]
    supported={"NoSound","NoFooter","Force","ResetReviewAssets","Seed","Seeds","Family","Apply"}
    for n in names:
        p=BULK/n; p.write_text("param()", encoding="utf-8"); scripts[p]=supported
    for f in CommandBuilder.CANONICAL_FAMILIES:
        p=Paths().family_dir(f)/"run_prototype.ps1"; p.parent.mkdir(parents=True,exist_ok=True); p.write_text("param()",encoding="utf-8"); scripts[p]={"Seed","NoSound","NoFooter"}
    b=CommandBuilder(Ctx(),Catalog(scripts))
    five=[1,2,3,4,5]

    review=b.review(five,b.CANONICAL_FAMILIES,reset=True)
    assert review.arguments[:4]==["-NoProfile","-ExecutionPolicy","Bypass","-Command"], review.arguments
    assert "-Seeds @( 1, 2, 3, 4, 5 )" in review.arguments[4], review.arguments
    assert "-ResetReviewAssets" in review.arguments[4], review.arguments
    assert review.working_directory==str(ROOT)

    specs=b.production_25(five)
    assert len(specs)==5
    for spec in specs:
        assert spec.arguments[:4]==["-NoProfile","-ExecutionPolicy","Bypass","-Command"], spec.arguments
        assert "-Seeds @( 1, 2, 3, 4, 5 )" in spec.arguments[4], spec.arguments
        assert spec.working_directory==str(ROOT)

    for factory in (b.export_review_assets,b.export_review_gifs,b.export_review_keyframes):
        spec=factory(five)
        assert spec.arguments[:4]==["-NoProfile","-ExecutionPolicy","Bypass","-Command"], spec.arguments
        assert "-Seeds @( 1, 2, 3, 4, 5 )" in spec.arguments[4], spec.arguments
        assert spec.working_directory==str(ROOT)

    single=b.production_single("c11c_geometric_waves_v1",271828,audio=False,footer=False,force=True)
    assert "-Family" in single.arguments and "-Seed" in single.arguments
    assert all(flag in single.arguments for flag in ("-NoSound","-NoFooter","-Force"))
    assert b.all_families(271828).arguments[-2:]==["-Seed","271828"]
    assert b.prototype("c11c_geometric_waves_v1",271828).arguments[-2:]==["-Seed","271828"]
    assert b.cleanup(True).arguments[-1]=="-Apply"
    assert b.reset(True).arguments[-1]=="-Apply"
    assert b.retire_legacy_tools(True).arguments[-1]=="-Apply"
    for spec in (b.validate_powershell(),b.validate_delivery(),b.validate_preflight()):
        assert spec.working_directory==str(ROOT)

    print("C11-C Studio v0.5.1 command-contract PASS")

if __name__=="__main__": main()
