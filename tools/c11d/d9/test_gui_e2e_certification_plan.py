from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PLAN = ROOT / "docs" / "current" / "d" / "D9_GUI_E2E_CERTIFICATION_PLAN_V1.md"
REQUIRED_CASES = tuple(f"D9-GUI-{i:03d}" for i in range(1, 12))


def run_checks() -> int:
    if not PLAN.is_file():
        raise AssertionError(f"D9 GUI E2E plan missing: {PLAN.relative_to(ROOT)}")
    text = PLAN.read_text(encoding="utf-8-sig")
    missing = [case_id for case_id in REQUIRED_CASES if f"`{case_id}`" not in text]
    if missing:
        raise AssertionError(f"GUI E2E certification plan cases missing: {missing}")
    for token in (
        "operator_execution=REQUIRED",
        "renderer_activation=false",
        "media_created=false",
        "D4.8=BLOCKED",
        "release_authority=NONE",
        "Future D renderer baseline required",
        "Explicitly disabled today",
    ):
        if token not in text:
            raise AssertionError(f"Certification plan missing governance token: {token}")
    # This is intentionally a static preflight, never a media/renderer command.
    return len(REQUIRED_CASES)


if __name__ == "__main__":
    count = run_checks()
    print(
        "C11-D D9 GUI E2E CERTIFICATION PREFLIGHT PASS | "
        f"cases={count}/{len(REQUIRED_CASES)} | operator_execution=REQUIRED | "
        "renderer_activation=false | media_created=false | D4.8=BLOCKED | release_authority=NONE"
    )
