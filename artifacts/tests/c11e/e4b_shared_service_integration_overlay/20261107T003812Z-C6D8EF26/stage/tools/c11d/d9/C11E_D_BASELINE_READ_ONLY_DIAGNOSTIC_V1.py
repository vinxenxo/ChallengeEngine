from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def main() -> int:
    root = Path(__file__).resolve().parents[3]
    result: dict[str, Any] = {
        "schema": "C11E-D-BASELINE-READ-ONLY-DIAGNOSTIC-V1",
        "scope": "READ_ONLY_CURRENT_TREE_CANDIDATE_PREFLIGHT",
        "project_root": str(root),
        "repository_files_written": False,
        "renderer_invoked": False,
        "media_created": False,
        "release_authority": "NONE",
    }
    try:
        import importlib.util

        candidate_path = root / "tools" / "c11d" / "baseline_candidate" / "d_baseline_candidate.py"
        spec = importlib.util.spec_from_file_location("c11e_d_baseline_candidate_read_only", candidate_path)
        if spec is None or spec.loader is None:
            raise RuntimeError("Cannot load D baseline candidate evaluator")
        candidate_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(candidate_module)
        record = candidate_module.build_candidate_preflight(root)
        governance = record.get("governance", {})
        result.update(
            {
                "status": "PREFLIGHT_REPORT_AVAILABLE",
                "candidate_preflight_sha256": record.get("seal_sha256"),
                "blocker_count": len(record.get("blockers", [])),
                "blockers": record.get("blockers", []),
                "d4_8": governance.get("d4_8"),
                "d9_14": governance.get("d9_14_real_media_status"),
                "d9_15_checkpoint_valid": governance.get("d9_15_operator_acceptance_checkpoint_valid"),
                "d9_16": governance.get("d9_16_full_acceptance_status"),
                "d9_17": governance.get("d9_17_closure_status"),
                "d10": governance.get("d10_baseline_status"),
            }
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        result.update(
            {
                "status": "BLOCKED_READ_ONLY_PREFLIGHT",
                "error_type": type(exc).__name__,
                "error": str(exc),
            }
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
