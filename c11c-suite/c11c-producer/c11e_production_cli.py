"""C11-E CLI facade; delegates all request semantics to the shared E service."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from c11e_production_service import (
    C11EProductionServiceError,
    prepare_c11e_production_intent,
    validate_c11e_production_intent,
)


def _write_utf8(stream, value: str) -> None:
    data = value.encode("utf-8")
    binary = getattr(stream, "buffer", None)
    if binary is not None:
        binary.write(data)
        binary.flush()
    else:
        stream.write(value)
        stream.flush()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="C11-E shared production-intent CLI (E1 preparation only).")
    parser.add_argument("--request", required=True, help="D9.9 canonical universal request JSON")
    parser.add_argument("--origin", choices=("CLI", "API", "TEST", "UNKNOWN"), default="CLI")
    parser.add_argument("--output", help="Optional output JSON path")
    parser.add_argument("--print-json", action="store_true")
    parser.add_argument(
        "--execute-drill-av", action="store_true",
        help="Run the shared D-owned isolated E4C A/V qualification adapter after E1 validation (CLI origin only).",
    )
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parents[2]
    try:
        raw = json.loads(Path(args.request).read_text(encoding="utf-8-sig"))
        if args.execute_drill_av:
            if args.origin != "CLI":
                raise C11EProductionServiceError("--execute-drill-av requires --origin CLI; E1 planning remains available for all existing origins")
            d9_dir = root / "tools" / "c11d" / "d9"
            if str(d9_dir) not in sys.path:
                sys.path.insert(0, str(d9_dir))
            from c11e_e4c_drill_execution import execute_drill_av_request
            execution = execute_drill_av_request(raw, root, request_origin="CLI")
            rendered_execution = json.dumps(execution, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
            if args.output:
                output_path = Path(args.output).resolve()
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(rendered_execution, encoding="utf-8")
            if args.print_json or not args.output:
                _write_utf8(sys.stdout, rendered_execution)
            else:
                _write_utf8(sys.stdout, json.dumps({
                    "status": execution.get("status"),
                    "request_id": execution.get("request_id"),
                    "selector": execution.get("selector"),
                    "final_A_sha256": execution.get("final_A_sha256"),
                    "video_bitstream_identical_A_C": execution.get("video_bitstream_identical_A_C"),
                    "audio_bitstream_changed_A_C": execution.get("audio_bitstream_changed_A_C"),
                    "release_authority": "NONE",
                }, ensure_ascii=False) + "\n")
            return 0 if execution.get("status") == "PASS_E4C_DRILL_SINGLE_SELECTOR_A_V_QUALIFICATION" else 2
        prepared = prepare_c11e_production_intent(raw, root, request_origin=args.origin)
        validation = validate_c11e_production_intent(prepared["intent"], root)
        payload = {
            "schema": "C11-E-PRODUCTION-CLI-RESULT-V1",
            "status": "PASS_E1_PREPARATION_ONLY",
            "intent": prepared["intent"],
            "validation": validation,
            "execution_boundary": prepared["intent"]["execution_boundary"],
        }
        rendered = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        if args.output:
            output_path = Path(args.output).resolve()
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")
        if args.print_json or not args.output:
            _write_utf8(sys.stdout, rendered)
        else:
            summary = {
                "status": payload["status"],
                "request_id": prepared["intent"]["request"]["request_id"],
                "intent_sha256": prepared["intent"]["intent_sha256"],
                "request_hash": prepared["intent"]["identity"]["request_hash"],
                "editorial_hash": prepared["intent"]["identity"]["editorial_hash"],
                "plan_hash": prepared["intent"]["identity"]["plan_hash"],
                "renderer": False,
                "media_created": False,
                "release_authority": "NONE",
            }
            _write_utf8(sys.stdout, json.dumps(summary, ensure_ascii=False) + "\n")
        return 0
    except Exception as exc:
        _write_utf8(sys.stderr, f"C11-E PRODUCTION SERVICE ERROR: {exc}\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
