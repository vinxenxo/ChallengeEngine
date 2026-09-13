import json
from pathlib import Path

src = Path("challenges")
dst = Path("challenges_c7")
dst.mkdir(exist_ok=True)

for path in src.glob("CHALLENGE_*.json"):
    data = json.loads(path.read_text(encoding="utf-8"))
    if "canonical_v2" not in data:
        data["canonical_v2"] = {}
    data["canonical_v2"]["audio"] = {
        "enabled": True,
        "profile_id": "c7_test_profile"
    }
    dest_path = dst / path.name
    dest_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
print("Corpus paralelo ./challenges_c7 generado correctamente con audio habilitado.")