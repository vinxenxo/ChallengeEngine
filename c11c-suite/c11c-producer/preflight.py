from pathlib import Path
ROOT=Path(__file__).resolve().parent
probe=(ROOT/'seed_probe.gd').read_text(encoding='utf-8')
assert 'func _init() -> void:' in probe
assert 'VariationProfileClass.build(family, seed)' in probe
assert 'OS.get_cmdline_user_args()' in probe
assert 'JSON.parse_string' in probe
print('C11-C Producer seed_probe preflight PASS')
