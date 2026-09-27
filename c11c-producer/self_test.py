from __future__ import annotations
import ast,hashlib,json,os,py_compile
from pathlib import Path
ROOT=Path(__file__).resolve().parent; PROJECT=Path(os.environ.get("C11C_PROJECT_ROOT",ROOT.parent)).resolve()
main=(ROOT/"main.py").read_text(encoding="utf-8"); ast.parse(main); py_compile.compile(str(ROOT/"main.py"),doraise=True)
s=json.loads((ROOT/"producer_schema.json").read_text(encoding="utf-8"))
assert s["backend_truth"]=="ChallengeEngine-C11-C2.16.9 FROZEN.zip"
assert s["backend_profile_sha256"]=="f7df994d8842183275bc331decd75762a153f3100248c7cc8b590e34c1347e2d"
assert len(s["families"])==5 and "scalar_potential" in [x[0] for x in s["families"]["c11c_invisible_forces_v1"]["grammars"]]
assert set(x["id"] for x in s["challenges"])=={f"CHALLENGE_{i:03d}" for i in range(1,10)}
assert set(s["drills"])=={"tracking","saccade","pursuit","peripheral_scan"}
assert s["review_workers"]==7
assert (ROOT/"run_visual_drill_production.ps1").exists()
assert (PROJECT/"tools/prototypes/c11c_bulk/run_c11c_art_direction_batch_v4.ps1").exists()
assert (PROJECT/"tools/prototypes/c11c_bulk/run_c11c_challenge_production.ps1").exists()
assert "seed_probe.gd" in main and "run_c11c_art_direction_batch_v4.ps1" in main and "run_c11c_challenge_production.ps1" in main
assert "self.manual.setEnabled(active and manual)" in main
assert "_new_unique_seeds" in main
profile=PROJECT/"tools/prototypes/c11c_common/C11CVariationProfile.gd"
if profile.exists(): assert hashlib.sha256(profile.read_bytes()).hexdigest()==s["backend_profile_sha256"]
print("C11-C Producer 0.7.0 self-test PASS")
