from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

from universal_producer import evaluate_universal_request


def _write_utf8(stream, text: str) -> None:
    """Write protocol text as UTF-8 regardless of the Windows console code page.

    The JSON CLI contract is UTF-8. Using ``print`` on Windows may encode accented
    editorial fields with the active OEM/ANSI code page while callers correctly
    decode captured stdout as UTF-8. Write bytes to the underlying pipe instead.
    """
    data = text.encode("utf-8")
    binary_stream = getattr(stream, "buffer", None)
    if binary_stream is not None:
        binary_stream.write(data)
        binary_stream.flush()
        return
    # Supports in-process callers/tests that substitute StringIO-like streams.
    stream.write(text)
    stream.flush()


def main() -> int:
    parser = argparse.ArgumentParser(description="C11-D D9.9 canonical universal Producer planner (plan-only).")
    parser.add_argument("--request", required=True, help="Universal D9.9 request JSON")
    parser.add_argument("--output", help="Optional result JSON output path")
    parser.add_argument("--print-json", action="store_true", help="Print complete canonical result JSON")
    args = parser.parse_args()
    request_path = Path(args.request).resolve()
    try:
        raw = json.loads(request_path.read_text(encoding="utf-8-sig"))
        result = evaluate_universal_request(raw, Path(__file__).resolve().parents[3])
        payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        if args.output:
            output_path = Path(args.output).resolve()
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(payload, encoding="utf-8")
        if args.print_json or not args.output:
            _write_utf8(sys.stdout, payload)
        else:
            summary = json.dumps(
                {
                    "status": result["status"],
                    "request_hash": result["request_hash"],
                    "plan_hash": result["plan_hash"],
                    "renderer": False,
                    "release_authority": "NONE",
                },
                ensure_ascii=False,
            ) + "\n"
            _write_utf8(sys.stdout, summary)
        return 0
    except Exception as exc:
        _write_utf8(sys.stderr, f"D9.9 UNIVERSAL PRODUCER ERROR: {exc}\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
