from __future__ import annotations
import hashlib, json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parent
import os
PROJECT=Path(os.environ.get('C11C_PROJECT_ROOT', ROOT.parent)).resolve()
schema=json.loads((ROOT/'producer_schema.json').read_text(encoding='utf-8'))
profile=PROJECT/schema['backend_profile_source']
assert profile.exists(), profile
assert hashlib.sha256(profile.read_bytes()).hexdigest()==schema['backend_profile_sha256']
assert len(schema['families'])==5
assert all(f['grammars'][0][0]=='auto' for f in schema['families'].values())
probe=(ROOT/'seed_probe.gd').read_text(encoding='utf-8')
assert 'return _fail(' not in probe
assert 'return null' not in probe.split('func _init',1)[1].split('func _score',1)[0]
assert 'C11CVariationProfile.gd' in probe or 'C11CVariationProfile' in probe
main=(ROOT/'main.py').read_text(encoding='utf-8')
assert 'run_c11c_production.ps1' in main
assert '-Seeds' not in main
assert 'VISUAL LOOPS' in main
print('C11-C Producer 0.3.0 self-test PASS')
