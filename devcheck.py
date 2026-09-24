from pathlib import Path
import ast

ROOT=Path(__file__).parent
errors=[]

required_pages = [
    "dashboard","review","production","art_direction","families","seeds","products","artifacts","jobs","logs","validation","games","reproduction","settings","about"
]
for name in required_pages:
    p=ROOT/"c11c_studio"/"ui"/"pages"/(name+".py")
    if not p.exists(): errors.append(f"missing page: {p}")
required_services=[
    "tool_discovery","introspection","family_registry","seed_manager","command_builder","job_manager","environment_validator","artifact_registry","product_catalog","snapshot"
]
for name in required_services:
    p=ROOT/"c11c_studio"/"services"/(name+".py")
    if not p.exists(): errors.append(f"missing service: {p}")
required_scripts=[
    "validate_c11c_powershell.ps1","validate_c11c_delivery_configuration.ps1","run_c11c_art_direction_review.ps1","run_c11c_production.ps1","run_c11c_production_bulk.ps1","run_c11c_production_25.ps1","run_all_c11c_visual_loops.ps1"
]
cb=(ROOT/"c11c_studio/services/command_builder.py").read_text(encoding="utf-8")
for s in required_scripts:
    if s not in cb: errors.append(f"command builder missing canonical script reference: {s}")
for p in ROOT.rglob("*.py"):
    try: ast.parse(p.read_text(encoding="utf-8"), filename=str(p))
    except SyntaxError as e: errors.append(f"syntax: {p}: {e}")
# Important accidental patterns
for p in ROOT.rglob("*.py"):
    if p.name == "devcheck.py": continue
    txt=p.read_text(encoding="utf-8",errors="ignore")
    if "$family:" in txt: errors.append(f"PowerShell interpolation pattern leaked into Python: {p}")
    if "-Grammar" in txt and "supports" not in txt.lower() and "script_supports" not in txt: errors.append(f"Ungated Grammar flag reference: {p}")
if errors:
    print("C11-C STUDIO DEVCHECK FAIL")
    print("\n".join(errors)); raise SystemExit(1)
print("C11-C STUDIO DEVCHECK PASS")
print(f"Python files parsed: {sum(1 for _ in ROOT.rglob('*.py'))}")
print(f"Required pages: {len(required_pages)}")
print(f"Required services: {len(required_services)}")
