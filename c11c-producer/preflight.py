from pathlib import Path
ROOT=Path(__file__).resolve().parent
probe=(ROOT/'seed_probe.gd').read_text(encoding='utf-8')
assert 'return _fail(' not in probe
assert '_fail("Missing request JSON path")' in probe
assert 'func _init() -> void:' in probe
assert 'VariationProfileClass.build(family, seed)' in probe
print('C11-C Producer seed_probe preflight PASS')
