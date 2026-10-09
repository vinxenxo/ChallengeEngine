from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import maintenance as maint


def copy_file(root: Path, rel: str) -> None:
    source = ROOT / rel
    if not source.is_file():
        raise FileNotFoundError(f"Maintenance fixture dependency missing: {rel} (expected at {source})")
    target = root / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def make_fixture(root: Path) -> None:
    required = [
        "definitions/c11d/d9/D9_11_MAINTENANCE_POLICY_V1.json",
        "definitions/c11d/d9/D9_SUITE_VERSION_MATRIX_V1.json",
        "docs/current/d/C11-D_ROADMAP_V1.0_STATELESS.md",
        "docs/current/d/C11-D_MILESTONES_APPROVED.md",
        "docs/current/suite/C11C_SUITE_CURRENT_RULES.md",
        "docs/current/suite/C11C_SUITE_TOOLING_MATRIX.md",
        "docs/current/d/D9_UNIVERSAL_EDITORIAL_MODEL_V1.md",
        "docs/current/d/D9.8_UNIVERSAL_EDITORIAL_MODEL_CHECKPOINT.md",
        "docs/current/d/D9.9_PRODUCER_UNIVERSAL_COVERAGE_CHECKPOINT.md",
        "docs/current/d/D9.10_EDITORIAL_TO_RENDER_BRIDGE_PLANNING_CHECKPOINT.md",
        "docs/current/d/D9.11_MAINTENANCE_0.2.0_CHECKPOINT.md",
        "docs/current/d/D9.12_TEST_0.2.0_CHECKPOINT.md",
        "docs/current/d/D9.13_CROSS_SUITE_LIFECYCLE_CHECKPOINT.md",
        "c11c-suite/main.py",
        "release/C11C_FREEZE_PACKAGE_MANIFEST.json",
    ]
    for rel in required:
        copy_file(root, rel)

    # The retired sixth surface is intentionally absent from the live repository.
    # Exercise quarantine/restore against a synthetic legacy tree inside the
    # temporary fixture instead of requiring c11d-control to exist operationally.
    legacy_root = root / maint.QUARANTINE_SOURCE
    legacy_root.mkdir(parents=True, exist_ok=True)
    (legacy_root / "README.md").write_text(
        "# Simulated retired c11d-control\n\nFixture-only legacy content; not an operational suite.\n",
        encoding="utf-8",
    )
    (legacy_root / "main.py").write_text(
        "# Fixture-only placeholder for retired legacy surface.\n",
        encoding="utf-8",
    )
    (legacy_root / "run.bat").write_text(
        "@echo off\r\necho fixture-only legacy surface\r\n",
        encoding="ascii",
    )
    (legacy_root / "self_test.py").write_text(
        "# Fixture-only placeholder; never executed.\n",
        encoding="utf-8",
    )


def expect(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    policy = maint._validate_policy(ROOT)
    expect(policy["version"] == "0.2.0", "canonical maintenance policy version mismatch")
    live_plan = maint.build_plan(ROOT)
    expect(live_plan["status"] == "PASS", json.dumps(live_plan.get("errors", []), ensure_ascii=False))
    expect(live_plan["registered_surface_count"] == 5, "shared Suite must retain five canonical surfaces")
    expect(live_plan["legacy_surface"]["registered"] is False, "legacy c11d-control must stay unregistered")
    expect(live_plan["governance"]["d4_8"] == "BLOCKED" and live_plan["governance"]["release_authority"] == "NONE", "governance must remain blocked")
    expect(live_plan["side_effects"] == {"files_moved": False, "files_deleted": False, "manifest_rewritten": False, "archive_created": False}, "plan must be strictly read-only")
    expect(not maint.is_allowed_quarantine_source("core/simulation.gd", policy), "core must never be quarantine target")
    expect(not maint.is_allowed_quarantine_source("assets/readme.md", policy), "assets must never be quarantine target")
    expect(not maint.is_allowed_quarantine_source("c11c-suite/c11c-producer/main.py", policy), "canonical Producer must never be quarantine target")
    expect(not maint.is_allowed_quarantine_source("c11c-suite/c11c-maintenance/main.py", policy), "canonical Maintenance must never be quarantine target")
    expect(not maint.is_allowed_quarantine_source("../c11c-suite/c11d-control", policy), "path traversal must not be quarantine target")
    expect(maint.is_allowed_quarantine_source("c11c-suite/c11d-control", policy), "only approved legacy path should be eligible")
    try:
        maint.relative_path(ROOT, "../outside.txt")
    except ValueError:
        pass
    else:
        raise AssertionError("path traversal unexpectedly accepted")
    try:
        maint.relative_path(ROOT, "C:/outside.txt")
    except ValueError:
        pass
    else:
        raise AssertionError("drive-qualified path unexpectedly accepted")

    with tempfile.TemporaryDirectory(prefix="d9_11_maintenance_test_") as temp:
        root = Path(temp)
        make_fixture(root)
        original_manifest = (root / maint.FREEZE_MANIFEST_REL).read_bytes()
        original_tree = maint.inventory_tree(root / maint.QUARANTINE_SOURCE)
        plan = maint.build_plan(root)
        expect(plan["status"] == "PASS", "fixture plan failed: " + json.dumps(plan.get("errors", [])))
        preview = maint.quarantine_legacy_control(root, apply=False)
        expect(preview["status"] == "WOULD_QUARANTINE", "quarantine should default to dry-run")
        expect((root / maint.QUARANTINE_SOURCE).is_dir(), "dry-run must leave legacy source in place")
        expect(not (root / maint.LEDGER_REL).exists(), "dry-run must not create a ledger")
        unauthorized = maint.quarantine_legacy_control(root, apply=True, confirmation="")
        expect(unauthorized["status"] == "BLOCKED", "quarantine must require explicit confirmation")
        conflict_root = root / "docs/history/root_conflicts"
        conflict_root.mkdir(parents=True, exist_ok=True)
        reserved = conflict_root / "c11d-control_quarantine_TESTSTAMP"
        reserved.mkdir()
        with patch.object(maint, "stamp_utc", return_value="TESTSTAMP"):
            unique_destination = maint._choose_destination(root, "docs/history/root_conflicts/c11d-control_quarantine_")
        expect(unique_destination.name == "c11d-control_quarantine_TESTSTAMP_01" and reserved.is_dir(), "quarantine destination conflict must choose a unique name without overwrite")
        with patch.object(maint, "write_ledger_atomic", side_effect=OSError("simulated ledger disk failure")):
            rollback = maint.quarantine_legacy_control(root, apply=True, confirmation=maint.CONFIRM_QUARANTINE)
        expect(rollback["status"] == "ROLLED_BACK" and (root / maint.QUARANTINE_SOURCE).is_dir(), "quarantine ledger failure must rollback the filesystem move")
        expect(not (root / maint.LEDGER_REL).exists(), "failed quarantine ledger transaction must not leave a false ledger")
        applied = maint.quarantine_legacy_control(root, apply=True, confirmation=maint.CONFIRM_QUARANTINE)
        expect(applied["status"] == "QUARANTINED", "explicit quarantine failed: " + json.dumps(applied, ensure_ascii=False))
        dest = root / applied["destination_path"]
        expect(not (root / maint.QUARANTINE_SOURCE).exists() and dest.is_dir(), "quarantine did not move intact directory")
        expect(maint.inventory_tree(dest)["tree_sha256"] == original_tree["tree_sha256"], "tree identity changed during quarantine")
        expect((root / maint.FREEZE_MANIFEST_REL).read_bytes() == original_manifest, "historical C11-C manifest was rewritten")
        restored_preview = maint.restore_legacy_control(root, apply=False)
        expect(restored_preview["status"] == "WOULD_RESTORE", "restore should default to dry-run")
        archived_main = dest / "main.py"
        original_main = archived_main.read_bytes()
        archived_main.write_bytes(original_main + b"\n# simulated mutation\n")
        tamper = maint.restore_legacy_control(root, apply=True, confirmation=maint.CONFIRM_RESTORE)
        expect(tamper["status"] == "BLOCKED" and any("quarantined legacy surface tree hash differs from ledger" in error for error in tamper.get("errors", [])), "preflight must block restore if quarantine tree hash changed")
        archived_main.write_bytes(original_main)
        (root / maint.FREEZE_MANIFEST_REL).write_bytes(original_manifest + b"\n")
        manifest_conflict = maint.restore_legacy_control(root, apply=True, confirmation=maint.CONFIRM_RESTORE)
        expect(manifest_conflict["status"] == "BLOCKED_MANIFEST_CHANGED", "restore must block if historical manifest changed")
        (root / maint.FREEZE_MANIFEST_REL).write_bytes(original_manifest)
        (root / maint.QUARANTINE_SOURCE).mkdir(parents=True)
        conflict = maint.restore_legacy_control(root, apply=True, confirmation=maint.CONFIRM_RESTORE)
        expect(conflict["status"] == "BLOCKED_SOURCE_CONFLICT", "restore must not overwrite or merge an existing source")
        (root / maint.QUARANTINE_SOURCE).rmdir()
        restored = maint.restore_legacy_control(root, apply=True, confirmation=maint.CONFIRM_RESTORE)
        expect(restored["status"] == "RESTORED", "verified quarantine restore failed")
        expect(maint.inventory_tree(root / maint.QUARANTINE_SOURCE)["tree_sha256"] == original_tree["tree_sha256"], "restored tree hash differs")
        expect((root / maint.FREEZE_MANIFEST_REL).read_bytes() == original_manifest, "restore rewrote historical manifest")
        ledger = maint.load_ledger(root)
        expect([event["event_type"] for event in ledger["events"] if event.get("resource") == maint.QUARANTINE_SOURCE] == ["QUARANTINED", "RESTORED"], "quarantine lifecycle ledger is not append-only")

        transient_a = root / "artifacts/scratch/selftest-é.txt"
        transient_b = root / "artifacts/tests/logs/verbose/selftest.log"
        transient_a.parent.mkdir(parents=True, exist_ok=True)
        transient_b.parent.mkdir(parents=True, exist_ok=True)
        transient_a.write_text("reversible cleanup café", encoding="utf-8")
        transient_b.write_text("verbose test output", encoding="utf-8")
        preview_cleanup = maint.cleanup_allowlisted(root, apply=False)
        expect(preview_cleanup["status"] == "WOULD_ARCHIVE_ALLOWLISTED_TRANSIENTS" and preview_cleanup["file_count"] == 2, "cleanup preview inventory mismatch")
        expect(transient_a.exists() and transient_b.exists(), "cleanup preview changed files")
        unauthorized_cleanup = maint.cleanup_allowlisted(root, apply=True, confirmation="wrong")
        expect(unauthorized_cleanup["status"] == "BLOCKED", "cleanup must require explicit confirmation")
        with patch.object(maint, "write_ledger_atomic", side_effect=OSError("simulated cleanup ledger disk failure")):
            cleanup_rollback = maint.cleanup_allowlisted(root, apply=True, confirmation=maint.CONFIRM_CLEANUP)
        expect(cleanup_rollback["status"] == "ROLLED_BACK" and transient_a.exists() and transient_b.exists(), "cleanup ledger failure must rollback archived files")
        archived = maint.cleanup_allowlisted(root, apply=True, confirmation=maint.CONFIRM_CLEANUP)
        expect(archived["status"] == "ARCHIVED_ALLOWLISTED_TRANSIENTS" and archived["file_count"] == 2, "safe transient archive failed")
        expect(not transient_a.exists() and not transient_b.exists(), "active transient paths should be cleaned after archive")
        archive_root = root / archived["archive_path"]
        expect((archive_root / "artifacts/scratch/selftest-é.txt").read_text(encoding="utf-8") == "reversible cleanup café", "cleanup archive did not preserve exact bytes")
        restore_cleanup_preview = maint.restore_cleanup_archive(root, apply=False)
        expect(restore_cleanup_preview["status"] == "WOULD_RESTORE_CLEANUP_ARCHIVE", "cleanup restore preview failed")
        transient_a.parent.mkdir(parents=True, exist_ok=True)
        transient_a.write_text("operator conflict", encoding="utf-8")
        cleanup_conflict = maint.restore_cleanup_archive(root, apply=True, confirmation=maint.CONFIRM_RESTORE_CLEANUP)
        expect(cleanup_conflict["status"] == "BLOCKED_SOURCE_CONFLICT", "cleanup restore must not overwrite conflicts")
        transient_a.unlink()
        clean_restored = maint.restore_cleanup_archive(root, apply=True, confirmation=maint.CONFIRM_RESTORE_CLEANUP)
        expect(clean_restored["status"] == "RESTORED_CLEANUP_ARCHIVE", "cleanup archive restore failed")
        expect(transient_a.read_text(encoding="utf-8") == "reversible cleanup café" and transient_b.read_text(encoding="utf-8") == "verbose test output", "cleanup restore did not preserve exact bytes")
        expect((root / maint.FREEZE_MANIFEST_REL).read_bytes() == original_manifest, "cleanup lifecycle rewrote historical freeze manifest")
        preflight = maint.freeze_preflight(root)
        expect(preflight["status"] == "PASS" and preflight["freeze_ready"] is False, "freeze preflight must pass as a report but never authorize freeze")
        expect(preflight["side_effects"]["archive_created"] is False and preflight["side_effects"]["manifest_rewritten"] is False, "freeze preflight must be read-only")
        audit = maint.docs_audit(root)
        expect(audit["status"] == "PASS" and audit["files_written"] is False, "documentation audit must remain dry-run-only")

    print("C11-D D9.11 MAINTENANCE PASS | policy=0.2.0 | dry-run=PASS | allowlist=2 | quarantine/restore=PASS | cleanup archive/restore=PASS | protected/path negatives=7/7 | conflict/rollback recovery=PASS | manifest=preserved | freeze=preflight-only | side_effects=fixture-only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
