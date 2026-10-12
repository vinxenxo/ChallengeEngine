from __future__ import annotations
import argparse, json, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
if str(HERE) not in sys.path: sys.path.insert(0,str(HERE))
from shared_production_context_service import audit, prepare_shared_production_context

def _write_ascii(text: str) -> None:
    data=text.encode('ascii',errors='backslashreplace')
    binary=getattr(sys.stdout,'buffer',None)
    if binary is not None:
        binary.write(data); binary.flush()
    else:
        sys.stdout.write(data.decode('ascii')); sys.stdout.flush()

def main() -> int:
    parser=argparse.ArgumentParser(description='C11-D GUI/CLI shared canonical context service; prepare-only')
    parser.add_argument('--project-root',type=Path,default=None)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--request',type=Path,help='Read-only D9.9 request JSON')
    group.add_argument('--audit-only',action='store_true',help='Validate service source pins and governance')
    args=parser.parse_args()
    try:
        if args.audit_only:
            c=audit(args.project_root)
            _write_ascii('C11-D SHARED BACKEND CLI AUDIT PASS | '+f"source_pins={c['source_pins']}/{c['source_pins']} | supported_content_types={c['supported_content_types']}/3 | composition_stages={c['composition_stages']}/6 | cli_gui_backend={c['cli_gui_backend']} | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE\n")
            return 0
        raw=json.loads(args.request.read_text(encoding='utf-8-sig'))
        record=prepare_shared_production_context(raw,args.project_root)
        _write_ascii(json.dumps(record,ensure_ascii=True,indent=2,sort_keys=True)+'\n')
        return 0
    except Exception as exc:
        _write_ascii(f'C11-D SHARED BACKEND CLI FAIL | {exc} | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE\n')
        return 2
if __name__=='__main__':
    raise SystemExit(main())
