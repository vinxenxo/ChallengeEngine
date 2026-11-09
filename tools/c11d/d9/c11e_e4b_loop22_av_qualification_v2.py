#!/usr/bin/env python3
"""C11-E E4B Loop22 integrated 44-slot audiovisual qualification runner V2 (shared-directory fix).

Bounded TEST_ONLY scope. It invokes only the existing pinned C11-C family launchers
in silent mode, generates the existing C11-C FAMILY_MUSIC_V4 native WAV assets from
R1P music_seed, creates a separate 48 kHz PCM delivery copy, and muxes AAC-LC 192k
with H.264 stream copy. It never invokes D renderer/dispatch, D3 V5, or production.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, os, re, shutil, subprocess, sys, tempfile, time, uuid, wave, zipfile
from datetime import datetime, timezone
from pathlib import Path, PureWindowsPath
from typing import Any
sys.dont_write_bytecode=True

HERE=Path(__file__).resolve().parent
MATRIX_REL="definitions/c11d/production/C11E_E4B_LOOP22_SELECTOR_MATRIX_V1.json"
POLICY_REL="definitions/c11d/production/C11E_E4B_LOOP22_AV_SCOPE_AMENDMENT_V1.json"
APPROVAL_REL="definitions/c11d/production/C11E_E4B_LOOP22_AV_OPERATOR_APPROVAL_RECORD_20261109_V1.json"
SUPPORT_REL="tools/c11d/d9/c11e_e4b_loop22_av_support_v1.py"
SUPPORT_SHA256="4f79a33f063dc22e350fc707f82b572ed1007bb14d36b0c6d49b6fd511a0e6e1"
BASE_REL="tools/c11d/d9/c11e_r1v_five_family_qualification_v3.py"
R1P_REL="artifacts/tests/c11e/e4b_r1p/E4B_R1P_20261107_032743_5F75045C_RECOVERED.zip"
MATRIX_SHA256="eb0ce2fab5ee97c298e232685ec3452779fc1e1f4a8dcd1c9c994bff1a45a1a1"
POLICY_SHA256="c0869c23001ed4e04a4fd81e3b1c9a974493c7b1a48cae5351eb55384c988628"
APPROVAL_RAW_SHA256="00584ca6f4fc3ca7a0269f56a270d7d022b9d360bd91bc983d75c7b0934b5c98"
APPROVAL_CANONICAL_SHA256="4d3d4a1d5044469e819721fd7a818881246ab6f219b1e8cc7924f2ceb895e970"
R1P_SHA256="d49f54ffdee6026426c2bb87fcb72b5c8a68f09cb64fb91f71e25dc10fd26b52"
FROZEN_SHA256="e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
POLICY_PINS={'definitions/c11d/production/D_RENDERER_UNIFIED_PRESENTATION_REGION_POLICY_PROPOSAL_V1.json': {'bytes': 9440, 'sha256': '101092bb32127bb8854a501a9215c0b6cf69581594383903716907d49719c01a'}, 'definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json': {'bytes': 8376, 'sha256': '609a4d183aac07c2cbe1abaf41444160fdd137217faffbead3aef618320d57dc'}, 'definitions/c11d/production/C11E_E4B_LOOP_EDITORIAL_COMPOSITION_PROPOSAL_V1.json': {'bytes': 5528, 'sha256': '9e206704665ea85226ecc10854be9f679c32fe9ed7efb690a829f6e8456d43da'}, 'definitions/c11d/production/D_RENDERER_UNIFIED_DELIVERY_TIMEBASE_POLICY_PROPOSAL_V1.json': {'bytes': 9507, 'sha256': '41a62b0766db47cd99772f28642ef67766314f20f0f7891789d6b7497bbfee85'}, 'definitions/c11d/production/D_RENDERER_UNIFIED_AUDIO_MUSIC_DELIVERY_POLICY_PROPOSAL_V1.json': {'bytes': 7457, 'sha256': '3dd4874e1b6506de6d9ddbe6ad1b567a284b94cc00ef1bac0d35d1731af05e23'}}
AUDIO_PINS={
 "tools/prototypes/c11c_common/C11CSafeAmbient.py":{"bytes":1739,"sha256":"c376fd44a3115f0d800213d95e28143363748e16c7b5800369fcadbf237fb02c"},
 "tools/prototypes/c11c_common/generate_c11c_family_music.py":{"bytes":16382,"sha256":"41bb8f9842ac941ea86c838f272b11bd0642973b26e92defa006721a3d8cb84d"},
 "profiles/presentation/c11c_visual_music_profiles.json":{"bytes":7038,"sha256":"b78706c5a9adbf1581d925f522b76cc3419983177de213734cc79996af5cbf58"}}
FAMILY_ROUTE={"geometric":"CIRCUIT_PULSE","fractal":"ORGANIC_BLOOM","sacred_symmetry":"ORBITAL_RITUAL","living_particles":"ORGANIC_BLOOM","invisible_forces":"FLOWING_VECTOR"}
EXPECTED_RECEIPTS=[2,3,4,5,7,8,9,10,12,13,14,15,17,18,19,20,22,23,24,25,26,27]

class Loop22Error(RuntimeError): pass
def require(ok: bool,msg: str)->None:
 if not ok: raise Loop22Error(msg)
def sha(path: Path)->str:
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()
def sha_bytes(b: bytes)->str: return hashlib.sha256(b).hexdigest()
def canonical(v: Any)->Any:
 if isinstance(v,dict): return {str(k):canonical(v[k]) for k in sorted(v,key=lambda x:str(x))}
 if isinstance(v,(list,tuple)): return [canonical(x) for x in v]
 return v
def canonical_sha(v: Any)->str:
 return sha_bytes(json.dumps(canonical(v),ensure_ascii=False,separators=(',',':'),allow_nan=False).encode('utf-8'))
def read_json(p: Path)->Any:
 require(p.is_file(),f"Required JSON missing: {p}")
 try: return json.loads(p.read_text(encoding='utf-8-sig'))
 except Exception as e: raise Loop22Error(f"Invalid JSON {p}: {e}") from e
def dump_json(p: Path,v: Any)->str:
 p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(v,ensure_ascii=False,indent=2,sort_keys=True,allow_nan=False)+'\n',encoding='utf-8',newline='\n')
 return sha(p)
def load_support(project_root: Path):
 p=project_root/SUPPORT_REL
 require(p.is_file() and sha(p)==SUPPORT_SHA256,f"Loop22 support module missing or SHA-pinned content differs: {p}")
 spec=importlib.util.spec_from_file_location('c11e_e4b_loop22_support',p)
 require(spec is not None and spec.loader is not None,'Cannot load Loop22 support module')
 m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
def load_base(project_root: Path):
 p=project_root/BASE_REL
 require(p.is_file() and p.stat().st_size==89479 and sha(p)=='9d1baba14ca8cf96e3f2f466cedc104ec4b9cf1b94ef4b11690abe7a6de9e019','Pinned C11-E shared R1V validation core differs')
 spec=importlib.util.spec_from_file_location('c11e_loop22_shared_core_v3',p)
 require(spec is not None and spec.loader is not None,'Cannot load pinned C11-E shared core')
 m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
def verify_policy_inputs(project_root: Path):
 observed={}
 for rel,pin in POLICY_PINS.items():
  p=project_root/Path(*rel.split('/'))
  require(p.is_file() and p.stat().st_size==pin['bytes'] and sha(p)==pin['sha256'],f"Approved source policy pin mismatch: {rel}")
  observed[rel]=pin['sha256']
 matrix_p=project_root/MATRIX_REL; policy_p=project_root/POLICY_REL; approval_p=project_root/APPROVAL_REL
 require(sha(matrix_p)==MATRIX_SHA256,f"Loop22 selector matrix SHA mismatch: {matrix_p}")
 require(sha(policy_p)==POLICY_SHA256,f"Loop22 scope amendment SHA mismatch: {policy_p}")
 require(sha(approval_p)==APPROVAL_RAW_SHA256,f"Loop22 operator approval raw SHA mismatch: {approval_p}")
 matrix=read_json(matrix_p); policy=read_json(policy_p); approval=read_json(approval_p)
 ah=dict(approval); stored=ah.pop('approval_record_canonical_sha256',None)
 require(stored==canonical_sha(ah)==APPROVAL_CANONICAL_SHA256,'Loop22 operator approval canonical SHA mismatch')
 require(policy.get('status')=='APPROVED_BOUNDED_TEST_SCOPE_ONLY_NOT_RENDERER_INPUT'
  and policy.get('authority',{}).get('operator_approval_canonical_sha256')==stored
  and policy.get('authority',{}).get('selector_matrix_sha256')==MATRIX_SHA256,'Loop22 scope amendment does not bind approved matrix/record')
 require(approval.get('decision')=='APPROVE_BOUNDED_LOOP22_22_SELECTOR_44_OUTPUT_AV_QUALIFICATION_TEST_ONLY'
  and approval.get('scope')==policy.get('scope'),'Loop22 operator decision/scope mismatch')
 require(matrix.get('status')=='APPROVED_BOUNDED_TEST_SCOPE_MATRIX_NOT_D4_EXECUTABLE_INPUT'
  and matrix.get('scope',{}).get('selector_count')==22 and matrix.get('scope',{}).get('av_outputs')==44,'Loop22 matrix scope invalid')
 require(policy.get('approved_upstream_policy_hashes')==POLICY_PINS and approval.get('approved_upstream_policy_hashes')==POLICY_PINS,'Loop22 approved upstream policy map drift')
 gov=policy.get('governance',{})
 for k,v in {'renderer':'OFF','D4.8':'BLOCKED','D9.10':'PREPARE_ONLY','D9.14':'BLOCKED','D9.16':'BLOCKED','D9.17':'BLOCKED_NO_GO','D10':'BLOCKED_FOR_PROMOTION','release_authority':'NONE'}.items():
  require(gov.get(k)==v,f"Loop22 governance lock drift: {k}")
 require(policy.get('execution',{}).get('preflight_before_first_launcher') is True and policy.get('execution',{}).get('all_44_launchers_are_new') is True,'Loop22 execution guard missing')
 return matrix,policy,approval
def load_matrix_selectors(project_root: Path, matrix: dict, archive_path: Path):
 require(archive_path.is_file() and sha(archive_path)==R1P_SHA256,'R1P recovered archive missing or hash mismatch')
 selectors=matrix.get('selectors',[])
 require(len(selectors)==22,'Loop22 matrix must contain exactly 22 selectors')
 require(sorted(int(x['receipt_index']) for x in selectors)==EXPECTED_RECEIPTS,'Loop22 selector set is not exact 22 complement')
 pilot_indices={int(x['receipt_index']) for x in load_base(project_root).SELECTOR_EXPECTATIONS}
 require(pilot_indices=={1,6,11,16,21},'R1V pilot selector identities differ from protected allowlist')
 require(not pilot_indices.intersection(EXPECTED_RECEIPTS),'Loop22 matrix overlaps accepted R1V pilot')
 with zipfile.ZipFile(archive_path,'r') as z:
  require(z.testzip() is None,'R1P archive CRC failure during Loop22 selector binding')
  by_family={k:0 for k in FAMILY_ROUTE}
  result=[]
  for row in selectors:
   idx=int(row['receipt_index']); raw=z.read(row['receipt_file']); receipt=json.loads(raw.decode('utf-8-sig'))
   hi=dict(receipt); stored=hi.pop('receipt_sha256',None)
   observed=canonical_sha(hi)
   side=z.read(row['receipt_file']+'.sha256').decode('ascii').strip().split()[0]
   require(stored==observed==side==row['r1p_receipt_sha256'],f"R1P receipt/sidecar canonical mismatch at {idx}")
   require(sha_bytes(raw)==row.get('r1p_receipt_raw_sha256',sha_bytes(raw)),'R1P receipt raw SHA drift')
   sel=receipt.get('selection',{}); seeds=receipt.get('seed_domains',{}); timing=receipt.get('timing',{})
   ident=receipt.get('request_identity',{})
   require(sel.get('family_id')==row['family_id'] and sel.get('grammar_id')==row['grammar_id'] and int(sel.get('grammar_index',-1))==int(row['grammar_index']),f"R1P selector identity mismatch at receipt {idx}")
   require(int(seeds.get('gameplay_seed',-1))==int(row['gameplay_seed']) and int(seeds.get('music_seed',-1))==int(row['music_seed']) and seeds.get('music_seed_consumed_by_visual_parameters') is False,f"R1P seed domain mismatch at receipt {idx}")
   require(int(row['gameplay_seed'])!=int(row['music_seed']),'Gameplay and music seeds must be distinct')
   require(float(timing.get('duration_seconds',0))==float(row['duration_seconds']) and int(timing.get('fps',0))==30 and int(timing.get('frame_count',0))==int(row['frame_count_consistency_only']) and int(timing.get('loop_cycles',0))==int(row['loop_cycles']),f"R1P timing/cycle mismatch at receipt {idx}")
   require(int(row['frame_count_consistency_only'])==int(row['duration_seconds'])*30,'Loop22 frame count is not duration*30')
   require(receipt.get('family_music_profile_id')==row['music_profile_id']==FAMILY_ROUTE[row['internal_family_id']],f"Music profile mapping mismatch at receipt {idx}")
   require(ident==row['r1p_request_identity'],f"R1P request identity hashes mismatch at receipt {idx}")
   require(row.get('request_compatibility')=='PLAN_ONLY_NOT_D4_EXECUTABLE_COMPATIBILITY' and row.get('r1p_status')=='PASS_PARAMETER_PAYLOAD_MATERIALIZED_IN_MEMORY_NOT_RENDERER_INPUT','R1P compatibility/status drift')
   require(receipt.get('payload_sha256')==row['r1p_payload_sha256']==receipt.get('repeat_payload_sha256'),'R1P payload hash/repeat mismatch')
   gov=receipt.get('governance',{})
   for k,v in {'renderer':'OFF','D4.8':'BLOCKED','D9.10':'PREPARE_ONLY','D9.17':'BLOCKED_NO_GO','D10':'BLOCKED_FOR_PROMOTION','release_authority':'NONE'}.items(): require(gov.get(k)==v,f"R1P governance lock changed at {idx}:{k}")
   by_family[row['internal_family_id']]+=1
   result.append({**row,'receipt_raw_sha256':sha_bytes(raw),'receipt_canonical_sha256':observed,
      'receipt_payload_sha256':receipt['payload_sha256'],'r1p_music_seed_domain':seeds})
 require(by_family=={'geometric':4,'fractal':4,'sacred_symmetry':4,'living_particles':4,'invisible_forces':6},f"Loop22 family distribution mismatch: {by_family}")
 require(len(result)==22,'Incomplete Loop22 R1P bindings')
 return result

def verify_audio_source_pins(project_root: Path):
 rows=[]
 for rel,pin in AUDIO_PINS.items():
  p=project_root/Path(*rel.split('/'))
  require(p.is_file() and p.stat().st_size==pin['bytes'] and sha(p)==pin['sha256'],f"C11-C audio dependency pin mismatch: {rel}")
  rows.append({'path':rel,'bytes':pin['bytes'],'sha256':pin['sha256']})
 return rows

def verify_all_pins(base, support, project_root: Path, r1p_archive: Path):
 r1p=base.verify_r1p_archive(project_root,r1p_archive)
 option_c=base.verify_option_c_evidence(project_root)
 audio=verify_audio_source_pins(project_root)
 matrix,policy,approval=verify_policy_inputs(project_root)
 require(r1p['total_source_pins_verified']==61,'Base R1P/C11-C/Option-C source pin count mismatch')
 return {'base_source_pins':r1p['total_source_pins_verified'],'family_audio_source_pins':len(audio),
  'approved_policy_pins':len(POLICY_PINS),'total_source_pin_checks':61+len(audio)+len(POLICY_PINS),
  'r1p_zip_sha256':r1p['recovered_zip_sha256'],'r1p_receipts':r1p['receipt_count'],
  'option_c':option_c,'audio_pins':audio,'policy_pins':POLICY_PINS}

def build_run_id(now=None, token=None):
 moment=now or datetime.now(); suffix=(token or uuid.uuid4().hex[:6]).upper()
 require(re.fullmatch(r'[0-9A-F]{6}',suffix) is not None,'Invalid Loop22 run token')
 return f"L22_{moment.strftime('%H%M%S')}_{suffix}"

def windows_path_budget(project_root: str|Path, run_id: str, selectors: list[dict]):
 root=PureWindowsPath(str(project_root)); parent=root/'artifacts'/'tests'/'c11e'/'e4b_loop22_av'/run_id
 candidates=[]
 for s in selectors:
  for repeat in ('A','B'):
   tag=f"{run_id}_R{int(s['receipt_index']):02d}_{repeat}"
   stem=f"{s['output_prefix']}_seed_{s['gameplay_seed']}_{tag}"
   sr=parent/'source'/s['internal_family_id']/repeat
   nr=parent/'native_audio'/s['internal_family_id']/repeat
   pr=parent/'delivery_pcm'/s['internal_family_id']/repeat
   dr=parent/'delivery_av'/s['internal_family_id']/repeat
   names=[f'{stem}.mp4',f'{stem}_authoring.json',f'{stem}_manifest.json',f'{stem}_godot.log',f'{stem}_social.txt',f'{stem}_ffprobe.json',f'{stem}_loop22_source_ffprobe.json',f'{stem}_loop22_source_ffprobe.json.stderr.log',f'{stem}_loop22_frames.stdout.json',f'{stem}_loop22_frames.stderr.log',f'{stem}_loop22_pixel_decode.stderr.log',f'{stem}_loop22_pixel_hashes.json',f'{stem}_loop22_frame_inventory.json']
   candidates.extend(str(sr/n) for n in names)
   candidates += [str(nr/f'{tag}_native_44100.wav'),str(pr/f'{tag}_delivery_48000.wav'),str(dr/f'{tag}_AV_720.mp4'),str(dr/f'{tag}_final_ffprobe.json'),str(dr/f'{tag}_final_ffprobe.json.stderr.log'),str(dr/f'{tag}_source_h264.sha256'),str(dr/f'{tag}_final_h264.sha256'),str(dr/f'{tag}_aac.sha256')]
   temp_root=PureWindowsPath(r'C:\Users\vinxe\AppData\Local\Temp')
   candidates += [str(temp_root/f'C11C_{stem}_silent.mp4'),str(temp_root/f'{stem}_999999.avi')]
 longest=max(candidates,key=len)
 return {'max_path_chars':len(longest),'max_allowed_chars':259,'longest_path':longest,'candidate_path_count':len(candidates),'windows_max_path_guard':'PASS' if len(longest)<=259 else 'FAIL'}

def build_resample_command(ffmpeg, native_wav, delivery_wav, duration):
 return [ffmpeg,'-y','-hide_banner','-loglevel','error','-i',str(native_wav),'-map','0:a:0','-af','aresample=48000:async=0','-ar','48000','-ac','2','-c:a','pcm_s16le','-t',f'{float(duration):.1f}',str(delivery_wav)]
def validate_delivery_pcm(wav_path: Path,duration: float):
 require(wav_path.is_file() and wav_path.stat().st_size>44,f"Delivery PCM WAV missing/empty: {wav_path}")
 with wave.open(str(wav_path),'rb') as wf:
  ch,width,rate,frames=wf.getnchannels(),wf.getsampwidth(),wf.getframerate(),wf.getnframes()
  raw=wf.readframes(frames)
 expected=int(duration*48000)
 require((ch,width,rate,frames)==(2,2,48000,expected),f"Delivery PCM contract/sample count mismatch: {(ch,width,rate,frames)} != (2,2,48000,{expected})")
 require(len(raw)==expected*4,'Delivery PCM byte count mismatch')
 return {'sample_rate_hz':rate,'channels':ch,'sample_width_bytes':width,'sample_frames':frames,
  'expected_sample_frames':expected,'duration_seconds':frames/rate,'pcm_sha256':sha_bytes(raw),
  'wav_sha256':sha(wav_path),'wav_bytes':wav_path.stat().st_size}

def build_mux_command(ffmpeg,source_mp4,delivery_wav,output_mp4):
 return [ffmpeg,'-y','-hide_banner','-loglevel','error','-i',str(source_mp4),'-i',str(delivery_wav),
  '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-profile:a','aac_low','-b:a','192k',
  '-ar','48000','-ac','2','-shortest','-movflags','+faststart',str(output_mp4)]

def validate_final_probe(probe,selector,source_stream):
 streams=probe.get('streams',[]); require(len(streams)==2,'Final MP4 must contain exactly two streams')
 vv=[x for x in streams if x.get('codec_type')=='video']; aa=[x for x in streams if x.get('codec_type')=='audio']
 require(len(vv)==1 and len(aa)==1,'Final MP4 must contain one video and one audio stream')
 v,a=vv[0],aa[0]
 require(v.get('codec_name')=='h264' and int(v.get('width',0))==720 and int(v.get('height',0))==1280 and v.get('r_frame_rate')=='30/1' and int(v.get('nb_frames',-1))==int(selector['frame_count_consistency_only']),'Final H264 geometry/fps/frame count mismatch')
 require(v.get('pix_fmt')==source_stream.get('pix_fmt') and v.get('color_range')==source_stream.get('color_range'),'Final mux changed H264 pixel/range metadata')
 require(a.get('codec_name')=='aac' and a.get('profile') in ('LC','AAC LC') and a.get('sample_rate')=='48000' and int(a.get('channels',0))==2 and a.get('channel_layout')=='stereo','Final AAC-LC 48k stereo delivery contract mismatch')
 require(int(a.get('bit_rate') or 0)>=175000 and int(a.get('bit_rate') or 0)<=210000,'Final AAC bitrate is outside the 192 kb/s delivery neighborhood')
 return {'video_stream':v,'audio_stream':a,'container_duration_seconds':float(probe.get('format',{}).get('duration',0) or 0),
  'preencode_pcm_duration_contract':'EXACT_48000_SAMPLE_FRAMES_VALIDATED','postencode_duration_tolerance':'NOT_DEFINED_BY_D1; RECORDED_NOT_GATED'}

def run_process(command,cwd,timeout=3600):
 return subprocess.run(command,cwd=str(cwd),stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=timeout,check=False)

def unique_output_directories(jobs):
 # Return ordered unique output roots, failing closed on cross-role/family aliases.
 ordered={}; owners={}
 for job in jobs:
  family=str(job['selector']['internal_family_id']); repeat=str(job['repeat'])
  for role in ('source_root','native_root','pcm_root','delivery_root'):
   path=Path(job[role])
   key=os.path.normcase(os.path.normpath(os.path.abspath(os.fspath(path)))).casefold()
   owner=(role,family,repeat)
   if key in owners:
    require(owners[key]==owner,f'Loop22 output directory identity collision: {path} belongs to {owner}, already claimed by {owners[key]}')
   else:
    owners[key]=owner; ordered[key]=path
 return list(ordered.values())

def run_loop22(project_root: Path,r1p_archive: Path|None=None):
 require(sys.platform=='win32','Loop22 physical qualification is Windows-only')
 require(sys.version_info[:2]==(3,13),f'Python 3.13 required; found {sys.version.split()[0]}')
 project_root=project_root.resolve(strict=True)
 require(str(project_root).lower()==r'C:\users\vinxe\projects\challengeenginev01_stateless'.lower(),'Unexpected active checkout; refusing to run outside the authorized ProjectRoot')
 r1p_archive=r1p_archive or project_root/R1P_REL
 support=load_support(project_root); base=load_base(project_root)
 matrix,policy,approval=verify_policy_inputs(project_root)
 selectors=load_matrix_selectors(project_root,matrix,r1p_archive)
 option_c=base.verify_option_c_evidence(project_root)
 tools=base._tool_preflight(project_root)
 pre_pins=verify_all_pins(base,support,project_root,r1p_archive)
 run_id=build_run_id()
 evidence_parent=project_root/'artifacts/tests/c11e/e4b_loop22_av'
 evidence_root=evidence_parent/run_id
 require(not evidence_root.exists(),'Loop22 evidence root collision; no overwrite')
 path_budget=windows_path_budget(project_root,run_id,selectors)
 require(path_budget['max_path_chars']<=259,f"Loop22 MAX_PATH budget exceeded: {path_budget['longest_path']} ({path_budget['max_path_chars']})")
 jobs=[]
 for s in selectors:
  for repeat in ('A','B'):
   tag=f"{run_id}_R{int(s['receipt_index']):02d}_{repeat}"
   sr=evidence_root/'source'/s['internal_family_id']/repeat
   nr=evidence_root/'native_audio'/s['internal_family_id']/repeat
   pr=evidence_root/'delivery_pcm'/s['internal_family_id']/repeat
   dr=evidence_root/'delivery_av'/s['internal_family_id']/repeat
   stem=f"{s['output_prefix']}_seed_{s['gameplay_seed']}_{tag}"
   temp_mp4=Path(tempfile.gettempdir())/f"C11C_{stem}_silent.mp4"
   temp_avi=f"{stem}_*.avi"
   require(len(str(temp_mp4))<=259 and len(str(Path(tempfile.gettempdir())/f'{stem}_999999.avi'))<=259,f"C11-C temp path exceeds Windows MAX_PATH budget for {tag}")
   require(not temp_mp4.exists() and not list(Path(tempfile.gettempdir()).glob(temp_avi)),f"C11-C temp output preimage exists for {tag}")
   jobs.append({'selector':s,'repeat':repeat,'tag':tag,'source_root':sr,'native_root':nr,'pcm_root':pr,'delivery_root':dr,
                'stem':stem,'temp_mp4':temp_mp4,'temp_avi_glob':temp_avi})
 output_dirs=unique_output_directories(jobs)
 require(len(output_dirs)==40,f'Loop22 unique output directory cardinality mismatch: expected 40, found {len(output_dirs)}')
 for path in [evidence_root]+output_dirs:
  require(not path.exists(),f'Loop22 output destination already exists; refusing overwrite: {path}')
 require(not any(evidence_root.parent.glob(evidence_root.name+'*')),'Loop22 run-id prefix collision')
 override_path=project_root/'override.cfg'; override_existed=override_path.exists(); override_bytes=override_path.read_bytes() if override_existed else None
 temp_backups=base.temp_file_state('C11C_override_backup_*.cfg')
 lock_token=hash_bytes(str(project_root).lower().encode())[:16]
 lock=Path(tempfile.gettempdir())/f'C11E_LOOP22_{lock_token}.lock'
 try: lock_fd=os.open(str(lock),os.O_CREAT|os.O_EXCL|os.O_WRONLY)
 except FileExistsError as e: raise Loop22Error(f'Another Loop22 run holds project lock: {lock}') from e
 start=datetime.now(timezone.utc).isoformat()
 process_records=[]; source_rows=[]; av_rows=[]; failure=None; override_report={'path':str(override_path),'existed_before':override_existed,'sha256_before':sha_bytes(override_bytes) if override_bytes is not None else None,'temp_backups_preimage':temp_backups}
 try:
  evidence_root.mkdir(parents=True,exist_ok=False); (evidence_root/'processes').mkdir()
  # Each family/repeat/role path is shared by multiple selectors. Create each unique
  # physical directory exactly once; retain exist_ok=False fail-closed.
  for p in output_dirs:
   p.mkdir(parents=True,exist_ok=False)
  if override_existed: (evidence_root/'override_cfg_preimage.bin').write_bytes(override_bytes)
  run_manifest={'schema':'C11E-E4B-LOOP22-AV-RUN-MANIFEST-V2','run_id':run_id,'started_utc':start,
   'project_root':str(project_root),'r1p_zip_sha256':R1P_SHA256,'selector_matrix_sha256':MATRIX_SHA256,
   'scope_policy_sha256':POLICY_SHA256,'operator_approval_raw_sha256':APPROVAL_RAW_SHA256,
   'scope':{'selectors':22,'repeats':2,'av_outputs':44,'new_c11c_silent_launcher_invocations':44,
    'native_family_music_wav':44,'delivery_pcm_48k_wav':44,'aac_mux':44,'reused_prior_capture_slots':0,
    'video_stream_copy':True,'d_compositor':False,'d3_v5':False,'d9_10_dispatch':False,'renderer':False},
   'path_budget':path_budget,'output_directory_plan':{'logical_references':len(jobs)*4,'unique_directories':len(output_dirs),'expected_unique_directories':40,'sharing_key':'role+internal_family_id+repeat'},'preflight_source_pins':pre_pins,'runtime_tools':tools,
   'jobs':[{'receipt_index':j['selector']['receipt_index'],'family_id':j['selector']['family_id'],'grammar_id':j['selector']['grammar_id'],
      'repeat':j['repeat'],'gameplay_seed':j['selector']['gameplay_seed'],'music_seed':j['selector']['music_seed'],'tag':j['tag']} for j in jobs],
   'governance':matrix['governance']}
  run_manifest_sha=dump_json(evidence_root/'loop22_run_manifest.json',run_manifest)
  dump_json(evidence_root/'preflight_report.json',{'status':'PASS_LOOP22_PRELAUNCH_PREFLIGHT','run_id':run_id,
   'validated_selectors':22,'planned_slots':44,'planned_new_launchers':44,'all_output_leaves_absent':True,
   'all_temp_paths_absent':True,'unique_output_directories':len(output_dirs),'logical_output_directory_references':len(jobs)*4,'windows_path_budget':path_budget,'source_pins':pre_pins,
   'policy_inputs':{'matrix':MATRIX_SHA256,'scope':POLICY_SHA256,'approval_raw':APPROVAL_RAW_SHA256},'tools':tools})
 except Exception:
  os.close(lock_fd)
  try: lock.unlink()
  except FileNotFoundError: pass
  raise

 audio_helper=project_root/'tools/prototypes/c11c_common/C11CSafeAmbient.py'
 music_registry=read_json(project_root/'profiles/presentation/c11c_visual_music_profiles.json')
 audio_rules=music_registry.get('design_rules',{})
 try:
  for slot,j in enumerate(jobs,1):
   s=j['selector']; rep=j['repeat']; sr=j['source_root']; nr=j['native_root']; pr=j['pcm_root']; dr=j['delivery_root']
   launcher=base.safe_project_file(project_root,s['launcher_path'])
   command=base.build_launcher_command(tools['powershell']['path'],launcher,s,sr,j['tag'])
   t0=datetime.now(timezone.utc).isoformat(); capture=run_process(command,project_root,timeout=3600)
   key=f'{slot:02d}_{s["internal_family_id"]}_{rep}'
   out=evidence_root/'processes'/f'{key}_C11C.stdout.log'; err=evidence_root/'processes'/f'{key}_C11C.stderr.log'
   out.write_bytes(capture.stdout); err.write_bytes(capture.stderr)
   record={'slot':slot,'receipt_index':s['receipt_index'],'family_id':s['family_id'],'grammar_id':s['grammar_id'],'repeat':rep,
    'launcher_invoked':True,'command':command,'started_utc':t0,'completed_utc':datetime.now(timezone.utc).isoformat(),
    'exit_code':capture.returncode,'stdout_path':str(out),'stdout_sha256':sha(out),'stderr_path':str(err),'stderr_sha256':sha(err)}
   process_records.append(record)
   require(capture.returncode==0,f'C11-C launcher failed slot {slot}: exit {capture.returncode}; stderr={capture.stderr[:500]!r}')
   require(b'[C11-C-2.16.3] PASS' in capture.stdout,f'C11-C PASS marker missing in slot {slot}')
   restored=base.restore_known_c11c_override_state(override_path,override_existed,override_bytes)
   require(restored in ('PASS_ORIGINAL_PREIMAGE_PRESENT','PASS_ORIGINALLY_ABSENT'),f'override.cfg restoration failure after slot {slot}: {restored}')
   require(not j['temp_mp4'].exists() and not list(Path(tempfile.gettempdir()).glob(j['temp_avi_glob'])),f'C11-C temp AVI/MP4 remains after slot {slot}')
   pin_guard=verify_all_pins(base,support,project_root,r1p_archive)
   selector={**s,'frame_count_consistency_only':int(s['frame_count_consistency_only'])}
   source_job={'source_output_tag':j['tag']}
   inventory=support.inspect_source_video(base,project_root,sr,selector,rep,tools,source_job)
   # Save index without per-frame list duplication in aggregate report.
   dump_json(evidence_root/'source_index'/f'{key}.json',{k:v for k,v in inventory.items() if k!='pixel_frame_hashes'})
   music_cmd=support.build_music_command(sys.executable,audio_helper,nr/f'{j["tag"]}_native_44100.wav',selector)
   music_proc=run_process(music_cmd,project_root,timeout=3600)
   mo=evidence_root/'processes'/f'{key}_MUSIC.stdout.log'; me=evidence_root/'processes'/f'{key}_MUSIC.stderr.log'; mo.write_bytes(music_proc.stdout); me.write_bytes(music_proc.stderr)
   require(music_proc.returncode==0 and b'FAMILY_MUSIC_V4 generated' in music_proc.stdout,f'FAMILY_MUSIC_V4 generation failed for slot {slot}: {music_proc.stderr[:400]!r}')
   native_wav=nr/f'{j["tag"]}_native_44100.wav'
   native_metrics=support.decode_audio_metrics(native_wav,float(s['duration_seconds']),audio_rules)
   native_metrics.update({'music_seed':int(s['music_seed']),'music_profile_id':s['music_profile_id'],'loop_cycles':int(s['loop_cycles']),
     'grammar_id':s['grammar_id'],'native_sample_rate_contract':'44100_HZ_PRESERVED'})
   delivery_wav=pr/f'{j["tag"]}_delivery_48000.wav'
   resample_cmd=build_resample_command(tools['ffmpeg']['path'],native_wav,delivery_wav,s['duration_seconds'])
   res_proc=run_process(resample_cmd,project_root,timeout=1800)
   ro=evidence_root/'processes'/f'{key}_RESAMPLE.stdout.log'; re_=evidence_root/'processes'/f'{key}_RESAMPLE.stderr.log'; ro.write_bytes(res_proc.stdout); re_.write_bytes(res_proc.stderr)
   require(res_proc.returncode==0,f'48k PCM delivery resample failed slot {slot}: {res_proc.stderr[:500]!r}')
   pcm_metrics=validate_delivery_pcm(delivery_wav,float(s['duration_seconds']))
   mux_path=dr/f'{j["tag"]}_AV_720.mp4'
   mux_cmd=build_mux_command(tools['ffmpeg']['path'],Path(inventory['source_video_path']),delivery_wav,mux_path)
   mux_proc=run_process(mux_cmd,project_root,timeout=3600)
   xo=evidence_root/'processes'/f'{key}_MUX.stdout.log'; xe=evidence_root/'processes'/f'{key}_MUX.stderr.log'; xo.write_bytes(mux_proc.stdout); xe.write_bytes(mux_proc.stderr)
   require(mux_proc.returncode==0 and mux_path.is_file() and mux_path.stat().st_size>0,f'AAC-LC mux failed slot {slot}: {mux_proc.stderr[:500]!r}')
   final_probe=support.ffprobe_json(tools['ffprobe']['path'],mux_path,project_root,dr/f'{j["tag"]}_final_ffprobe.json')
   av_qa=validate_final_probe(final_probe,selector,inventory['source_video_stream'])
   src_h264=support.hash_encoded_stream(tools['ffmpeg']['path'],Path(inventory['source_video_path']),'0:v:0','h264',project_root)
   out_h264=support.hash_encoded_stream(tools['ffmpeg']['path'],mux_path,'0:v:0','h264',project_root)
   require(src_h264==out_h264,'Final mux changed/re-encoded C11-C H.264 bitstream')
   aac=support.hash_encoded_stream(tools['ffmpeg']['path'],mux_path,'0:a:0','adts',project_root)
   dump_text(dr/f'{j["tag"]}_source_h264.sha256',src_h264+'\n'); dump_text(dr/f'{j["tag"]}_final_h264.sha256',out_h264+'\n'); dump_text(dr/f'{j["tag"]}_aac.sha256',aac+'\n')
   audio={ 'native_wav':native_metrics,'delivery_pcm_48000':pcm_metrics,'aac_stream_sha256':aac,
     'generator_exit_code':music_proc.returncode,'generator_stdout_sha256':sha(mo),'generator_stderr_sha256':sha(me),
     'resample_exit_code':res_proc.returncode,'resample_stdout_sha256':sha(ro),'resample_stderr_sha256':sha(re_),
     'mux_exit_code':mux_proc.returncode,'mux_stdout_sha256':sha(xo),'mux_stderr_sha256':sha(xe),
     'source_h264_elementary_sha256':src_h264,'final_h264_elementary_sha256':out_h264,'video_bitstream_preserved':True,
     'commands':{'music':music_cmd,'resample':resample_cmd,'mux':mux_cmd}}
   av_rows.append({'slot':slot,'receipt_index':s['receipt_index'],'family_id':s['family_id'],'grammar_id':s['grammar_id'],'repeat':rep,
     'gameplay_seed':int(s['gameplay_seed']),'music_seed':int(s['music_seed']),'music_profile_id':s['music_profile_id'],
     'source_inventory':inventory,'audio':audio,'final_av_path':str(mux_path),'final_av_sha256':sha(mux_path),
     'final_av_bytes':mux_path.stat().st_size,'final_av_probe':av_qa})
   dump_json(evidence_root/'progress.json',{'run_id':run_id,'status':'RUNNING_FAIL_CLOSED_ON_NEXT_ERROR',
     'completed_slots':slot,'completed_silent_captures':len(source_rows)+1,'completed_av_outputs':len(av_rows),
     'last_completed_slot':key,'timestamp_utc':datetime.now(timezone.utc).isoformat()})
   source_rows.append(inventory)
   # Revalidate authority + source pins after each completed slot.
   verify_all_pins(base,support,project_root,r1p_archive)
 except Exception as exc:
  failure=f'{type(exc).__name__}: {exc}'
 finally:
  try:
   override_result=base.restore_known_c11c_override_state(override_path,override_existed,override_bytes)
   override_report['final_guard_result']=override_result
   if override_result not in ('PASS_ORIGINAL_PREIMAGE_PRESENT','PASS_ORIGINALLY_ABSENT') and failure is None: failure=f'override.cfg final restore failed: {override_result}'
  except Exception as exc:
   override_report['final_guard_result']=f'FAIL_PRESERVED_UNKNOWN_STATE:{exc}'
   if failure is None: failure=str(exc)
  override_report['temp_backups_post']=base.temp_file_state('C11C_override_backup_*.cfg')
  os.close(lock_fd)
  try: lock.unlink()
  except FileNotFoundError: pass
 comparisons=None
 if failure is None:
  try:
   grouped={}
   for row in av_rows: grouped.setdefault((row['family_id'],row['grammar_id']),{})[row['repeat']]=row
   require(len(grouped)==22,'A/B comparison matrix does not contain 22 unique selector pairs')
   checks=[]
   for key,pair in sorted(grouped.items()):
    require(set(pair)=={'A','B'},f'Missing A/B pair for {key}')
    a,b=pair['A'],pair['B']; ai=a['source_inventory']; bi=b['source_inventory']
    tests={'frame_count_equal':ai['frame_count']==bi['frame_count'],'pts_equal':ai['pts']==bi['pts'],
      'pixel_frame_hashes_equal':ai['pixel_frame_hashes']==bi['pixel_frame_hashes'],
      'global_pixel_stream_equal':ai['global_pixel_stream_sha256']==bi['global_pixel_stream_sha256'],
      'native_wav_equal':a['audio']['native_wav']['wav_sha256']==b['audio']['native_wav']['wav_sha256'],
      'delivery_pcm_equal':a['audio']['delivery_pcm_48000']['wav_sha256']==b['audio']['delivery_pcm_48000']['wav_sha256'],
      'aac_stream_equal':a['audio']['aac_stream_sha256']==b['audio']['aac_stream_sha256'],
      'gameplay_seed_same':a['gameplay_seed']==b['gameplay_seed'],'music_seed_same':a['music_seed']==b['music_seed'],
      'gameplay_music_seed_distinct':a['gameplay_seed']!=a['music_seed'] and b['gameplay_seed']!=b['music_seed']}
    require(all(tests.values()),f'A/B deterministic identity failure for {key}: {tests}')
    checks.append({'family_id':key[0],'grammar_id':key[1],'checks':tests,
      'source_mp4_sha256_A':ai['source_video_sha256'],'source_mp4_sha256_B':bi['source_video_sha256'],
      'native_wav_sha256':a['audio']['native_wav']['wav_sha256'],'delivery_pcm_sha256':a['audio']['delivery_pcm_48000']['wav_sha256'],
      'aac_sha256':a['audio']['aac_stream_sha256']})
   comparisons={'selector_pairs':checks,'pairs_passed':len(checks)}
  except Exception as exc: failure=f'{type(exc).__name__}: {exc}'
 final_pins=None
 try:
  final_pins=verify_all_pins(base,support,project_root,r1p_archive)
  require(override_report.get('temp_backups_post')==temp_backups,'C11C override temp backup inventory changed')
  require(all(not j['temp_mp4'].exists() and not list(Path(tempfile.gettempdir()).glob(j['temp_avi_glob'])) for j in jobs),'C11-C temporary AV files remain')
 except Exception as exc:
  if failure is None: failure=f'{type(exc).__name__}: {exc}'
 status='PASS_E4B_LOOP22_AV_QUALIFICATION_44_OF_44_PENDING_OPERATOR_VISUAL_AUDIO_REVIEW' if failure is None and len(av_rows)==44 and len(process_records)==44 and comparisons and comparisons['pairs_passed']==22 else 'FAIL_E4B_LOOP22_AV_QUALIFICATION_STOPPED_FAIL_CLOSED'
 report={'schema':'C11E-E4B-LOOP22-AV-REPORT-V1','run_id':run_id,'status':status,'failure':failure,
  'completed_silent_captures':len(source_rows),'completed_launcher_invocations':len(process_records),
  'completed_native_wav':sum(1 for x in av_rows if x['audio'].get('native_wav')),
  'completed_delivery_pcm_48k':sum(1 for x in av_rows if x['audio'].get('delivery_pcm_48000')),
  'completed_aac_mux':len(av_rows),'completed_av_outputs':len(av_rows),
  'r1p':{'run_id':'E4B_R1P_20261107_032743_5F75045C','recovered_zip_sha256':R1P_SHA256,'receipt_count':27,
   'qualified_selector_count':22,'excluded_r1v_pilot_receipt_indices':[1,6,11,16,21]},
  'selector_matrix_sha256':MATRIX_SHA256,'scope_policy_sha256':POLICY_SHA256,'operator_approval_raw_sha256':APPROVAL_RAW_SHA256,
  'run_manifest_sha256':run_manifest_sha,'processes':process_records,
  'source_inventories':[{k:v for k,v in x.items() if k!='pixel_frame_hashes'} for x in source_rows],
  'audiovisual_outputs':[{k:v for k,v in x.items() if k!='source_inventory'}|{'source_inventory_sha256':x['source_inventory']['inventory_sha256']} for x in av_rows],
  'repeat_determinism':comparisons,'source_pins_after_run':final_pins,'override_cfg_integrity':override_report,
  'human_review':{'visual':'PENDING_OPERATOR_REVIEW_44_SLOTS','audio':'PENDING_OPERATOR_LISTENING_REVIEW_44_SLOTS'},
  'delivery_contract':{'native_wav_pcm_s16le_44100_stereo_preserved':True,'delivery_pcm_pcm_s16le_48000_stereo_exact_samples':True,
    'aac_lc_192k_48000_stereo':True,'h264_stream_copy':True,'video_reencode_after_source_capture':False,
    'audio_gain_mix_normalize_fade_or_crossfade':False,'postencode_duration_tolerance':'NOT_DEFINED_BY_D1; RECORDED_NOT_GATED'},
  'governance':matrix['governance']}
 report_path=evidence_root/'loop22_av_report.json'; report_sha=dump_json(report_path,report)
 (evidence_root/'loop22_av_report.sha256').write_text(f'{report_sha}  loop22_av_report.json\n',encoding='ascii')
 receipt={'schema':'C11E-E4B-LOOP22-AV-PROCESS-RECEIPT-V1','run_id':run_id,'python_version':sys.version.split()[0],
  'python_executable':sys.executable,'runtime_executables':tools,'planned_selectors':22,'planned_slots':44,
  'completed_launcher_invocations':len(process_records),'completed_av_outputs':len(av_rows),'report_sha256':report_sha,
  'status':status,'exit_code':0 if status.startswith('PASS_') else 1,'failure':failure}
 receipt_path=evidence_root/'loop22_av_process_receipt.json'; receipt_sha=dump_json(receipt_path,receipt)
 (evidence_root/'loop22_av_process_receipt.sha256').write_text(f'{receipt_sha}  loop22_av_process_receipt.json\n',encoding='ascii')
 evidence_zip=evidence_parent/f'{run_id}_EVIDENCE.zip'
 require(not evidence_zip.exists(),'Loop22 evidence ZIP collision')
 with zipfile.ZipFile(evidence_zip,'x',compression=zipfile.ZIP_STORED,allowZip64=True) as z:
  for p in sorted(evidence_root.rglob('*')):
   if p.is_file(): z.write(p,arcname=p.relative_to(evidence_root).as_posix())
 with zipfile.ZipFile(evidence_zip,'r') as z: require(z.testzip() is None,'Loop22 evidence ZIP CRC failure')
 return {'status':status,'run_id':run_id,'silent_captures':len(source_rows),'launcher_invocations':len(process_records),
  'av_outputs':len(av_rows),'ab_pairs_passed':comparisons.get('pairs_passed') if comparisons else 0,
  'report_path':str(report_path),'report_sha256':report_sha,'process_receipt_path':str(receipt_path),
  'process_receipt_sha256':receipt_sha,'evidence_zip':str(evidence_zip),'evidence_zip_sha256':sha(evidence_zip),'failure':failure}

def hash_bytes(b: bytes)->str: return hashlib.sha256(b).hexdigest()
def dump_text(p: Path,text: str)->None: p.write_text(text,encoding='ascii',newline='\n')
def main():
 ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('--project-root',type=Path,required=True); ap.add_argument('--r1p-recovered-zip',type=Path,default=None)
 a=ap.parse_args()
 try:
  result=run_loop22(a.project_root,a.r1p_recovered_zip); print(json.dumps(result,ensure_ascii=False,sort_keys=True)); return 0 if result['status'].startswith('PASS_') else 1
 except Exception as e:
  print(json.dumps({'status':'FAIL_LOOP22_PREFLIGHT_OR_EXECUTION','error':f'{type(e).__name__}: {e}'},ensure_ascii=False),file=sys.stderr); return 2
if __name__=='__main__': raise SystemExit(main())
