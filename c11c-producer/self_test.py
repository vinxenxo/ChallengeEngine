from __future__ import annotations
import ast, hashlib, json, py_compile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
main=(ROOT/'main.py').read_text(encoding='utf-8')
py_compile.compile(str(ROOT/'main.py'), doraise=True)
ast.parse(main)
SCHEMA=json.loads((ROOT/'producer_schema.json').read_text(encoding='utf-8'))
assert len(SCHEMA['families'])==5
assert [x[0] for x in SCHEMA.get('video_types', [])]==['challenges','visual_loops','visual_drills']
assert set(SCHEMA['drills'])=={'tracking','saccade','pursuit','peripheral_scan'}
for fid,d in SCHEMA['drills'].items():
    assert d['difficulty_values']==[1,2,3,4,5]
    assert d['gameplay_seconds'] in (17.0,21.0)
    assert d['production_launcher']=='c11c-producer/run_visual_drill_production.ps1'
assert {p['key'] for p in SCHEMA['drills']['tracking']['parameters']}=={'speed_multiplier','pacing_mode'}
assert {p['key'] for p in SCHEMA['drills']['saccade']['parameters']}=={'speed_multiplier'}
assert {p['key'] for p in SCHEMA['drills']['pursuit']['parameters']}=={'speed_multiplier'}
assert SCHEMA['drills']['pursuit']['parameters'][0]['min']==0.75 and SCHEMA['drills']['pursuit']['parameters'][0]['max']==1.5
assert SCHEMA['drills']['peripheral_scan']['parameters']==[]
assert "run_visual_drill_production.ps1" in main
assert "tools/prototypes/c11c_bulk/run_c11c_production.ps1" in main
assert "self.subtype_label.setText('Dificultad')" in main
assert "self.subtype_label.setText('Subfamilia')" in main
def extract_style(text):
    a=text.index("STYLE='''")+len("STYLE='''")
    b=text.index("'''",a)
    return text[a:b]
assert hashlib.sha256(extract_style(main).encode()).hexdigest()=='a96307a08896da86eb1544f7eb7e61db05fede8004f10584a1586f2db831b804'
ps=(ROOT/'run_visual_drill_production.ps1').read_text(encoding='utf-8')
for token in ['C11CMovieCapture.ps1','C11CSafeAmbient.py','VisualContentPlayer.tscn','720','1280','FAMILY_MUSIC_V3']:
    assert token in ps
assert "Start-Process -FilePath 'godot'" not in ps
assert "& godot @Args > $stdoutPath 2> $stderrPath" in ps
bridge=(ROOT/'C11CVisualDrillProducerEnvelopeGenerator.gd').read_text(encoding='utf-8')
for token in ['VisualAuthoringGenerator.gd','VisualDrillSeedVariation.gd','tracking','saccade','pursuit','peripheral_scan']:
    assert token in bridge
doc=(ROOT.parent/'docs/c11-C_PRODUCER_CANONICAL_NAMING.md').read_text(encoding='utf-8')
for token in ['geometric','Geometric Waves','fractal','Fractal Bloom','kaleidoscope','Sacred Symmetry','particle_flow','Living Particles','vector_field','Invisible Forces']:
    assert token in doc
print('C11-C Producer 0.4.0 + Visual Drills overlay v0.1.3 self-test PASS')
print('LIGHT_THEME_AND_LAYOUT_BASE040_PRESERVED PASS')
