from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from c11e_e3_audio_pipeline import C11EE3AudioPilotError, run_e3_audio_pilot


def main() -> int:
    parser = argparse.ArgumentParser(description="C11-E E3 Challenge audiovisual pilot (test-only, GUI-launched in operator workflow)")
    parser.add_argument("--root", required=True, help="Active ChallengeEngine repository root")
    parser.add_argument("--intent", required=True, help="Sealed E1 intent JSON produced by the Producer GUI")
    parser.add_argument("--source-video", required=True, help="Pinned E2 R4 A video-only MP4 fixture")
    parser.add_argument("--source-receipt", required=True, help="Pinned E2 R4 render receipt JSON")
    parser.add_argument("--source-receipt-sha256", required=True, help="Pinned E2 R4 receipt SHA sidecar")
    parser.add_argument("--output-root", required=True, help="Fresh evidence directory outside the repository")
    parser.add_argument("--operator-gui", action="store_true", help="Mark the worker as launched by the Producer GUI")
    args = parser.parse_args()
    try:
        receipt = run_e3_audio_pilot(
            project_root=Path(args.root),
            e1_intent_path=Path(args.intent),
            source_video_path=Path(args.source_video),
            source_receipt_path=Path(args.source_receipt),
            source_receipt_sha_path=Path(args.source_receipt_sha256),
            output_root=Path(args.output_root),
            operator_gui_invoked=bool(args.operator_gui),
        )
        print("C11E_E3_AUDIO_PILOT=PASS")
        print("RECEIPT=" + str(Path(args.output_root) / "C11E_E3_AUDIO_PILOT_RECEIPT.json"))
        print("RECEIPT_SHA256=" + str(receipt.get("receipt_sha256", "WRITTEN_SIDECAR")))
        print("RELEASE_AUTHORITY=NONE")
        return 0
    except Exception as exc:
        print(f"C11E_E3_AUDIO_PILOT=FAIL: {type(exc).__name__}: {exc}", file=sys.stderr)
        print("RELEASE_AUTHORITY=NONE", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
