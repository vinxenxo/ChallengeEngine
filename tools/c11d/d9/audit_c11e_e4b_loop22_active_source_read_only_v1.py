#!/usr/bin/env python3
"""Read-only active-checkout source reconciliation for the remaining 22 C11-E Visual Loop grammars.

Reads the live producer schema, five C11-C prototypes and launchers, variation profile,
FAMILY_MUSIC_V4 generator/registry, duration policy, and installed Loop22 plan. It never
invokes Godot, C11-C launchers, audio generation, FFmpeg/FFprobe, tests, Git, or media.
It writes only a JSON report and SHA256 sidecar under artifacts/tests/c11e.
"""
from __future__ import annotations
import argparse, hashlib, json, os, re, sys, zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

EXPECTED_ROOT = Path(r"C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS")
FROZEN_SHA = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
FROZEN_BYTES = 796318
R1P_ARCHIVE_SHA = "d49f54ffdee6026426c2bb87fcb72b5c8a68f09cb64fb91f71e25dc10fd26b52"
PLAN_REL = Path("docs/current/e/C11E_E4B_REMAINING_22_LOOP_GRAMMAR_QUALIFICATION_PLAN_20261109_V2.md")

FAMILIES = {
    "c11c_geometric_waves_v1": {"label":"Geometric Waves", "internal":"geometric", "function":"geometric", "prototype":"GeometricWavesPrototype.gd", "launcher":"tools/prototypes/c11c_geometric_waves_v1/run_prototype.ps1", "profile":"CIRCUIT_PULSE", "binding":"visual_loop/geometric", "paired_drill":"visual_drill/saccade"},
    "c11c_fractal_bloom_v1": {"label":"Fractal Bloom", "internal":"fractal", "function":"fractal", "prototype":"FractalBloomPrototype.gd", "launcher":"tools/prototypes/c11c_fractal_bloom_v1/run_prototype.ps1", "profile":"ORGANIC_BLOOM", "binding":"visual_loop/fractal", "paired_drill":"visual_drill/pursuit"},
    "c11c_sacred_symmetry_v1": {"label":"Sacred Symmetry", "internal":"sacred_symmetry", "function":"sacred", "prototype":"SacredSymmetryPrototype.gd", "launcher":"tools/prototypes/c11c_sacred_symmetry_v1/run_prototype.ps1", "profile":"ORBITAL_RITUAL", "binding":"visual_loop/sacred_symmetry", "paired_drill":"visual_drill/peripheral_scan"},
    "c11c_living_particles_v1": {"label":"Living Particles", "internal":"living_particles", "function":"living", "prototype":"LivingParticlesPrototype.gd", "launcher":"tools/prototypes/c11c_living_particles_v1/run_prototype.ps1", "profile":"ORGANIC_BLOOM", "binding":"visual_loop/living_particles", "paired_drill":"visual_drill/pursuit"},
    "c11c_invisible_forces_v1": {"label":"Invisible Forces", "internal":"invisible_forces", "function":"invisible", "prototype":"InvisibleForcesPrototype.gd", "launcher":"tools/prototypes/c11c_invisible_forces_v1/run_prototype.ps1", "profile":"FLOWING_VECTOR", "binding":"visual_loop/invisible_forces", "paired_drill":"visual_drill/tracking"},
}
PILOT = {
    "c11c_geometric_waves_v1": ["harmonic_membrane"],
    "c11c_fractal_bloom_v1": ["radial_bloom"],
    "c11c_sacred_symmetry_v1": ["astrolabe"],
    "c11c_living_particles_v1": ["swarm"],
    "c11c_invisible_forces_v1": ["dipole_field"],
}
# Candidate rows inherited from the accepted R1P complement plan. The active checkout and
# R1P source receipts are authoritative and must match exactly; no value is silently rewritten.
ROWS = [
("c11c_geometric_waves_v1","interference_plane","CIRCUIT_PULSE",100002,500002,3,23,690),
("c11c_geometric_waves_v1","parametric_ribbon","CIRCUIT_PULSE",100003,500003,3,23,690),
("c11c_geometric_waves_v1","lattice_wave","CIRCUIT_PULSE",100004,500004,1,20,600),
("c11c_geometric_waves_v1","orbital_wave","CIRCUIT_PULSE",100005,500005,3,23,690),
("c11c_fractal_bloom_v1","dendritic_tunnel","ORGANIC_BLOOM",100007,500007,1,20,600),
("c11c_fractal_bloom_v1","spiral_fractal","ORGANIC_BLOOM",100008,500008,1,20,600),
("c11c_fractal_bloom_v1","fractal_filigree","ORGANIC_BLOOM",100009,500009,1,20,600),
("c11c_fractal_bloom_v1","nested_worlds","ORGANIC_BLOOM",100010,500010,2,22,660),
("c11c_sacred_symmetry_v1","gear_train","ORBITAL_RITUAL",100012,500012,2,22,660),
("c11c_sacred_symmetry_v1","polygon_orrery","ORBITAL_RITUAL",100013,500013,2,22,660),
("c11c_sacred_symmetry_v1","origami_mandala","ORBITAL_RITUAL",100014,500014,3,23,690),
("c11c_sacred_symmetry_v1","celestial_chart","ORBITAL_RITUAL",100015,500015,3,23,690),
("c11c_living_particles_v1","vortex","ORGANIC_BLOOM",100017,500017,3,23,690),
("c11c_living_particles_v1","collision_cloud","ORGANIC_BLOOM",100018,500018,3,23,690),
("c11c_living_particles_v1","organic_pulse","ORGANIC_BLOOM",100019,500019,2,22,660),
("c11c_living_particles_v1","magnetic_filament_cloud","ORGANIC_BLOOM",100020,500020,1,20,600),
("c11c_invisible_forces_v1","vortex_field","FLOWING_VECTOR",100022,500022,3,23,690),
("c11c_invisible_forces_v1","saddle_field","FLOWING_VECTOR",100023,500023,3,23,690),
("c11c_invisible_forces_v1","quadrupole_field","FLOWING_VECTOR",100024,500024,1,20,600),
("c11c_invisible_forces_v1","gravitational_lens","FLOWING_VECTOR",100025,500025,1,20,600),
("c11c_invisible_forces_v1","topographic_basin","FLOWING_VECTOR",100026,500026,2,22,660),
("c11c_invisible_forces_v1","scalar_potential","FLOWING_VECTOR",100027,500027,3,23,690),
]

class AuditError(RuntimeError): pass

def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def read_text(root: Path, rel: str) -> tuple[str,dict[str,Any]]:
    p=root/rel
    if not p.is_file(): raise AuditError(f"SOURCE_MISSING: {rel}")
    data=p.read_bytes()
    try: s=data.decode('utf-8-sig')
    except UnicodeDecodeError as e: raise AuditError(f"SOURCE_ENCODING_UNSUPPORTED: {rel}: {e}")
    return s, {"path":rel,"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()}

def extract_gd_array(text: str, const_name: str) -> list[str]:
    m=re.search(rf"const\s+{re.escape(const_name)}\s*:\s*Array\[String\]\s*=\s*\[(.*?)\]",text,re.S)
    if not m: raise AuditError(f"GDSCRIPT_ARRAY_NOT_FOUND: {const_name}")
    return re.findall(r'"([^"\n]+)"',m.group(1))

def extract_variation_modes(text: str, fn: str) -> list[str]:
    m=re.search(rf"static\s+func\s+_{re.escape(fn)}\s*\([^\n]*\).*?(?=\nstatic\s+func\s+_|\Z)",text,re.S)
    if not m: raise AuditError(f"VARIATION_FUNCTION_NOT_FOUND: _{fn}")
    gm=re.search(r"var\s+grammar_modes\s*:\s*Array\[String\]\s*=\s*\[(.*?)\]",m.group(0),re.S)
    if not gm: raise AuditError(f"VARIATION_GRAMMAR_MODES_NOT_FOUND: _{fn}")
    return re.findall(r'"([^"\n]+)"',gm.group(1))

def json_candidates(path: Path):
    try: obj=json.loads(path.read_text(encoding='utf-8-sig'))
    except Exception: return
    def walk(node):
        if isinstance(node,dict):
            yield node
            for v in node.values(): yield from walk(v)
        elif isinstance(node,list):
            for v in node: yield from walk(v)
    yield from walk(obj)

def locate_r1p_archive(root: Path) -> dict[str,Any]:
    base=root/'artifacts'/'tests'/'c11e'
    matches=[]; searched=0
    if base.is_dir():
        for p in base.rglob('*.zip'):
            searched+=1
            try:
                if sha256_file(p)==R1P_ARCHIVE_SHA:
                    with zipfile.ZipFile(p,'r') as z:
                        bad=z.testzip()
                        json_names=[n for n in z.namelist() if n.lower().endswith('.json')]
                    matches.append({'path':str(p.relative_to(root)),'sha256':R1P_ARCHIVE_SHA,'zip_crc':'PASS' if bad is None else f'FAIL:{bad}','json_entries':len(json_names),'receipt_like_entries':[n for n in json_names if 'receipt' in n.lower() or 'payload' in n.lower()][:40]})
            except (OSError,zipfile.BadZipFile):
                continue
    
    if len(matches)>1: status='DUPLICATE_HASH_MATCHES'
    elif len(matches)==0: status='NOT_LOCATED_IN_ACTIVE_CHECKOUT_ARTIFACTS'
    elif matches[0]['zip_crc']!='PASS': status='FOUND_EXACT_HASH_BUT_ZIP_CRC_FAILED'
    else: status='FOUND_EXACT_HASH_AND_CRC_PASS'
    return {'expected_sha256':R1P_ARCHIVE_SHA,'zip_files_searched':searched,'matches':matches,'status':status}

def parse_plan_table(text: str) -> dict[str,tuple[str,int,int,int,int]]:
    out={}
    for line in text.splitlines():
        if not line.startswith('|'): continue
        cells=[x.strip() for x in line.strip().strip('|').split('|')]
        if len(cells)<9: continue
        grammar=cells[2].strip('`')
        if grammar in {r[1] for r in ROWS}:
            # family id / profile / gameplay / music / cycles / duration / frames
            out[grammar]=(cells[1].strip('`'),cells[3].strip('`'),int(cells[4]),int(cells[5]),int(cells[6]),int(cells[7].split()[0]),int(cells[8]))
    return out

def audit(root: Path, enforce_windows_root: bool=True) -> dict[str,Any]:
    root=root.resolve()
    if enforce_windows_root and os.name=='nt' and root != EXPECTED_ROOT:
        raise AuditError(f"ACTIVE_CHECKOUT_MISMATCH: expected {EXPECTED_ROOT}, got {root}")
    project_marker=root/'project.godot'
    if not project_marker.is_file(): raise AuditError('PROJECT_MARKER_MISSING')
    frozen=root/'release/C11C_FREEZE_PACKAGE_MANIFEST.json'
    if not frozen.is_file() or frozen.stat().st_size!=FROZEN_BYTES or sha256_file(frozen)!=FROZEN_SHA:
        raise AuditError('FROZEN_C11C_MANIFEST_PIN_MISMATCH')

    source_rows=[{'path':'release/C11C_FREEZE_PACKAGE_MANIFEST.json','bytes':FROZEN_BYTES,'sha256':FROZEN_SHA}]
    def load(rel):
        t,p=read_text(root,rel); source_rows.append(p); return t
    schema_text=load('c11c-suite/c11c-producer/producer_schema.json')
    try: schema=json.loads(schema_text)
    except json.JSONDecodeError as e: raise AuditError(f'PRODUCER_SCHEMA_JSON_INVALID: {e}')
    variation=load('tools/prototypes/c11c_common/C11CVariationProfile.gd')
    duration=load('tools/prototypes/c11c_common/C11CVisualLoopDuration.gd')
    music=load('tools/prototypes/c11c_common/generate_c11c_family_music.py')
    profile_text=load('profiles/presentation/c11c_visual_music_profiles.json')
    try: profile_registry=json.loads(profile_text)
    except json.JSONDecodeError as e: raise AuditError(f'MUSIC_PROFILE_REGISTRY_INVALID: {e}')

    expected_remaining={}
    for f,g,profile,seed,mseed,cycles,seconds,frames in ROWS:
        expected_remaining.setdefault(f,[]).append(g)
    pilot_and_remaining={f:set(PILOT[f])|set(expected_remaining.get(f,[])) for f in FAMILIES}
    mapping=[]
    for fid,info in FAMILIES.items():
        family_schema=schema.get('families',{}).get(fid)
        if not isinstance(family_schema,dict): raise AuditError(f'PRODUCER_SCHEMA_FAMILY_MISSING: {fid}')
        if family_schema.get('name')!=info['label']: raise AuditError(f'PRODUCER_SCHEMA_FAMILY_LABEL_MISMATCH: {fid}')
        schema_ids=[]
        for item in family_schema.get('grammars',[]):
            if isinstance(item,(list,tuple)) and len(item)>=1 and item[0]!='auto': schema_ids.append(str(item[0]))
        schema_set=set(schema_ids)
        if schema_set != pilot_and_remaining[fid]: raise AuditError(f'PRODUCER_SCHEMA_GRAMMAR_SET_MISMATCH: {fid}: expected={sorted(pilot_and_remaining[fid])} actual={sorted(schema_set)}')
        proto_rel=f"tools/prototypes/{fid}/{info['prototype']}"
        proto=load(proto_rel)
        proto_ids=extract_gd_array(proto,'GRAMMAR_IDS')
        if set(proto_ids)!=schema_set or len(proto_ids)!=len(schema_ids): raise AuditError(f'PROTOTYPE_GRAMMAR_SET_MISMATCH: {fid}')
        mode_ids=extract_variation_modes(variation,info['function'])
        if set(mode_ids)!=schema_set or len(mode_ids)!=len(schema_ids): raise AuditError(f'VARIATION_PROFILE_GRAMMAR_SET_MISMATCH: {fid}')
        launcher_rel=info['launcher']
        _,launcher_pin=read_text(root,launcher_rel); source_rows.append(launcher_pin)
        mapping.append({'family_id':fid,'family':info['label'],'schema_grammar_count':len(schema_ids),'prototype_grammar_count':len(proto_ids),'variation_grammar_count':len(mode_ids),'pilot_selectors':sorted(PILOT[fid]),'remaining_selectors':sorted(expected_remaining.get(fid,[])),'prototype_path':proto_rel,'launcher_path':launcher_rel,'native_music_profile':info['profile']})

    # Exactly 27 unique grammars, exact 5-pilot / 22-remaining complement.
    schema_total=sum(len(schema['families'][fid]['grammars'])-sum(1 for g in schema['families'][fid]['grammars'] if isinstance(g,list) and g and g[0]=='auto') for fid in FAMILIES)
    remaining_ids=[r[1] for r in ROWS]
    if len(remaining_ids)!=22 or len(set(remaining_ids))!=22: raise AuditError('REMAINING_SELECTOR_CARDINALITY_OR_DUPLICATE_ERROR')
    if schema_total!=27: raise AuditError(f'EXPECTED_27_SELECTOR_SCHEMA_TOTAL_GOT_{schema_total}')

    # FAMILY_MUSIC_V4 data/profile alignment.
    registry=profile_registry
    if registry.get('mode')!='FAMILY_MUSIC_V4': raise AuditError('MUSIC_REGISTRY_MODE_MISMATCH')
    registry_profiles={p.get('id'):p for p in registry.get('profiles',[]) if isinstance(p,dict)}
    bindings=registry.get('bindings',{})
    generator_ids=set(re.findall(r'"([A-Z_]+)"\s*:',music))
    for fid,info in FAMILIES.items():
        prof=registry_profiles.get(info['profile'])
        if not prof: raise AuditError(f"MUSIC_PROFILE_MISSING: {info['profile']}")
        binding=bindings.get(info['binding'])
        if not isinstance(binding,dict) or binding.get('profile')!=info['profile']:
            raise AuditError(f"MUSIC_BINDING_MISMATCH: {info['binding']}")
        if binding.get('paired_with')!=info['paired_drill']:
            raise AuditError(f"MUSIC_BINDING_PAIRED_DRILL_MISMATCH: {info['binding']}")
        if 'visual_grammar' not in binding.get('music_semantic_inputs',[]):
            raise AuditError(f"MUSIC_BINDING_OMITS_VISUAL_GRAMMAR: {info['binding']}")
        if info['profile'] not in music: raise AuditError(f"MUSIC_GENERATOR_PROFILE_MISSING: {info['profile']}")
    if not re.search(r'SAMPLE_RATE\s*=\s*44100',music) or not re.search(r'CHANNELS\s*=\s*2',music): raise AuditError('MUSIC_AUDIO_FORMAT_CONTRACT_MISMATCH')
    if not re.search(r'def\s+generate\([^\n]*seed[^\n]*family[^\n]*profile_id[^\n]*grammar',music): raise AuditError('FAMILY_MUSIC_GENERATOR_SIGNATURE_MISMATCH')

    # Duration policy: cycles 1/2/3 -> 20/22/23 s, 30 fps -> 600/660/690 frames.
    if not re.search(r'const\s+FPS\s*:\s*int\s*=\s*30',duration): raise AuditError('LOOP_FPS_POLICY_MISMATCH')
    for cy,sec in [(1,20),(2,22)]:
        if not re.search(rf'{cy}\s*:\s*return\s+{sec}\.0',duration): raise AuditError(f'LOOP_DURATION_POLICY_MISMATCH: cycles={cy}')
    if not re.search(r'_\s*:\s*return\s+23\.0',duration): raise AuditError('LOOP_DURATION_POLICY_MISMATCH: cycles=3_fallback')
    for f,g,p,seed,mseed,cy,sec,frames in ROWS:
        if mseed==seed or frames!=sec*30 or (cy,sec) not in [(1,20),(2,22),(3,23)]: raise AuditError(f'SEED_OR_DURATION_CONTRACT_ERROR: {g}')
        if p!=FAMILIES[f]['profile']: raise AuditError(f'PLAN_PROFILE_MISMATCH: {g}')

    # Confirm that the installed plan table contains the candidate matrix as written.
    plan_text=load(str(PLAN_REL).replace('\\','/'))
    plan_rows=parse_plan_table(plan_text)
    if len(plan_rows)!=22: raise AuditError(f'LOOP22_PLAN_TABLE_ROWS_MISMATCH: {len(plan_rows)}')
    for f,g,p,seed,mseed,cy,sec,frames in ROWS:
        got=plan_rows.get(g)
        wanted=(f,p,seed,mseed,cy,sec,frames)
        if got!=wanted: raise AuditError(f'LOOP22_PLAN_ROW_MISMATCH: {g}: expected={wanted} actual={got}')

    # Hash all sources again before writing evidence; any mid-audit drift fails closed.
    post=[]
    for src in source_rows:
        p=root/src['path']
        digest=sha256_file(p)
        if digest!=src['sha256']: raise AuditError(f'SOURCE_CHANGED_DURING_AUDIT: {src["path"]}')
        post.append({'path':src['path'],'sha256':digest,'stable':True})
    if len({x['path'] for x in source_rows})!=len(source_rows): raise AuditError('DUPLICATE_SOURCE_PATH_IN_AUDIT')

    r1p=locate_r1p_archive(root)
    if r1p['status']=='FOUND_EXACT_HASH_AND_CRC_PASS': state='PASS_STATIC_SOURCE_MAPPING_R1P_ARCHIVE_HASH_AND_CRC_PRESENT'
    elif r1p['status']=='NOT_LOCATED_IN_ACTIVE_CHECKOUT_ARTIFACTS': state='PASS_STATIC_SOURCE_MAPPING_R1P_ARCHIVE_LOCATION_PENDING'
    else: state='FAIL_CLOSED_R1P_ARCHIVE_EVIDENCE_AMBIGUOUS_OR_INVALID'
    return {
        'schema':'C11E-E4B-LOOP22-ACTIVE-SOURCE-READ-ONLY-AUDIT-V1',
        'status':state,
        'run_mode':'READ_ONLY_SOURCE_RECONCILIATION',
        'active_checkout':str(root),
        'frozen_c11c_manifest':{'path':'release/C11C_FREEZE_PACKAGE_MANIFEST.json','sha256':FROZEN_SHA,'bytes':FROZEN_BYTES,'pass':True},
        'selector_counts':{'producer_schema_total':schema_total,'pilot_selectors':5,'remaining_selectors':len(ROWS),'remaining_family_distribution':{FAMILIES[f]['label']:len(v) for f,v in expected_remaining.items()},'planned_ab_output_slots':len(ROWS)*2},
        'family_mapping':mapping,
        'remaining_selector_rows':[{'family_id':f,'grammar_id':g,'music_profile':p,'gameplay_seed':seed,'music_seed':mseed,'loop_cycles':cy,'duration_seconds':sec,'fps':30,'frame_count':frames} for f,g,p,seed,mseed,cy,sec,frames in ROWS],
        'music_contract':{'mode':'FAMILY_MUSIC_V4','sample_rate':44100,'channels':2,'profile_bindings':'PASS_5_FAMILY_BINDINGS','gameplay_music_seed_domains_separate':all(seed!=mseed for _,_,_,seed,mseed,_,_,_ in ROWS)},
        'duration_contract':{'cycles_to_seconds':{'1':20,'2':22,'3':23},'fps':30,'frames':{'20s':600,'22s':660,'23s':690}},
        'r1p_archive_discovery':r1p,
        'policy_refresh':{'A1':'NOT_AUDITED_BY_THIS_SCRIPT','A3':'NOT_AUDITED_BY_THIS_SCRIPT','B1':'NOT_AUDITED_BY_THIS_SCRIPT','D1':'NOT_AUDITED_BY_THIS_SCRIPT','E4B_LOOP':'NOT_AUDITED_BY_THIS_SCRIPT','separate_decisions_required':True},
        'source_pins_before_after':{'count':len(source_rows),'stable':True,'rows':post},
        'processes_invoked':{'git':False,'tests':False,'godot':False,'c11c_launchers':False,'music_generation':False,'ffmpeg':False,'ffprobe':False,'renderer':False,'dispatch':False,'media_created':False,'media_modified':False},
        'execution_authority':{'loop22_media_authorization':'NOT_GRANTED','renderer':'OFF','release_authority':'NONE'},
        'next_gate':'Resolve the R1P archive projection and refresh current policy fingerprints/decision docket. Only then prepare the separate 22-selector / 44-output execution amendment.'
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--project-root',type=Path,required=True)
    args=ap.parse_args()
    try:
        report=audit(args.project_root)
        base=args.project_root/'artifacts/tests/c11e/e4b_loop22_source_reconciliation'
        base.mkdir(parents=True,exist_ok=True)
        stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
        out=base/f'LOOP22_READ_ONLY_AUDIT_{stamp}.json'
        out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        digest=sha256_file(out)
        side=out.with_suffix(out.suffix+'.sha256')
        side.write_text(f'{digest}  {out.name}\n',encoding='ascii')
        print('========== C11-E E4B LOOP22 ACTIVE SOURCE RECONCILIATION V1 ==========')
        print('STATUS='+report['status'])
        print('SCHEMA_GRAMMARS=27/27')
        print('REMAINING_SELECTORS=22/22')
        print('FAMILY_DISTRIBUTION=4/4/4/4/6')
        print('PLANNED_AB_OUTPUT_SLOTS=44')
        print('FAMILY_MUSIC_BINDINGS=5/5; DURATION_POLICY=PASS')
        print('R1P_ARCHIVE='+report['r1p_archive_discovery']['status'])
        print('SOURCE_PINS_STABLE='+str(report['source_pins_before_after']['count'])+'/'+str(report['source_pins_before_after']['count']))
        print('GIT=False; TESTS=False; GODOT=False; LAUNCHERS=False; MUSIC=False; FFMPEG=False; FFPROBE=False; MEDIA=False')
        print('LOOP22_MEDIA_AUTHORIZATION=NOT_GRANTED; RENDERER=OFF; RELEASE_AUTHORITY=NONE')
        print('REPORT='+str(out))
        print('REPORT_SHA256='+digest)
        return 0
    except Exception as e:
        print('STATUS=FAIL_CLOSED_READ_ONLY_AUDIT')
        print('ERROR='+str(e))
        return 2

if __name__=='__main__':
    raise SystemExit(main())
