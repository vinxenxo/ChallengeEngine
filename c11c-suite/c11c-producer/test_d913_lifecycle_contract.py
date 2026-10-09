from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
main=(ROOT/"c11c-suite/c11c-producer/main.py").read_text(encoding="utf-8")
manifest=json.loads((ROOT/"c11c-suite/c11c-producer/BUILD_MANIFEST.json").read_text(encoding="utf-8"))
contract=json.loads((ROOT/"definitions/c11d/d9/D9_13_CROSS_SUITE_LIFECYCLE_V1.json").read_text(encoding="utf-8"))
backend=ROOT/"tools/c11d/d9/cross_suite_lifecycle.py"
assert backend.is_file()
assert "CROSS-SUITE LIFECYCLE (D9.13 · PLAN ONLY)" in main
assert "D9_LIFECYCLE.build_lifecycle_receipt(raw_request, PROJECT, run_root)" in main
assert "cross_suite_lifecycle_receipt.json" in main
assert manifest["version"]=="0.11.1" and manifest["d9_13_cross_suite_lifecycle"] is True
assert manifest["d9_13_media_created"] is False and manifest["d9_13_release_authority"]=="NONE"
assert [x["surface"] for x in contract["pipeline"]]==["c11c-config","c11c-producer","c11c-test","c11c-catalog","c11c-maintenance"]
assert contract["governance"]["renderer_activation"] is False and contract["governance"]["release_authority"]=="NONE"
print("C11C_PRODUCER_D9_13_LIFECYCLE_CONTRACT PASS | five surfaces | plan-only receipt | renderer=false | media=false | release_authority=NONE")
