from __future__ import annotations
import hashlib, json, py_compile, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent
py_compile.compile(str(ROOT/'main.py'), doraise=True)
SCHEMA = json.loads((ROOT/'producer_schema.json').read_text(encoding='utf-8'))
assert SCHEMA['backend_profile_sha256']
assert SCHEMA['backend_profile_source'].endswith('C11CVariationProfile.gd')
assert len(SCHEMA['families']) == 5
assert [x[0] for x in SCHEMA.get('video_types', [])] == ['challenges','visual_loops','visual_drills']
expected = {'c11c_geometric_waves_v1':20,'c11c_fractal_bloom_v1':18,'c11c_sacred_symmetry_v1':16,'c11c_living_particles_v1':19,'c11c_invisible_forces_v1':17}
for key, n in expected.items():
    assert len(SCHEMA['families'][key]['params']) == n, (key, len(SCHEMA['families'][key]['params']), n)
probe = (ROOT/'seed_probe.gd').read_text(encoding='utf-8')
assert 'var t: float' in probe and 'var p: float' in probe and 'var n:' not in probe
assert 'return _fail(' not in probe
print('C11-C Producer 0.4.0 self-test PASS')
