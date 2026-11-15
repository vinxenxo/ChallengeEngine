from __future__ import annotations

from pathlib import Path
import hashlib
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "tools" / "c11d" / "d9" / "RUN_C11E_E4C_PURSUIT_TIERS_1_TO_5_V1.ps1"
DRIVER = ROOT / "tools" / "c11d" / "d9" / "c11e_e4c_pursuit_tier_batch.py"
INSTALLER = ROOT.parent / "INSTALL_C11E_E4C_PURSUIT_BATCH_OVERLAY_V5_3.ps1"


class PursuitRunnerContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.raw = RUNNER.read_bytes()
        self.text = self.raw.decode("ascii")

    def test_runner_is_ascii_and_has_no_bom(self):
        self.assertFalse(self.raw.startswith(b"\xef\xbb\xbf"))
        self.assertTrue(all(byte < 128 for byte in self.raw))

    def test_runner_self_parses_with_powershell_51_ast(self):
        self.assertIn("[System.Management.Automation.Language.Parser]::ParseFile($PSCommandPath", self.text)
        self.assertIn("WINDOWS_POWERSHELL_5_1_REQUIRED", self.text)

    def test_prepare_only_is_default_and_execute_is_explicit(self):
        self.assertIn("[switch]$Execute", self.text)
        self.assertIn("if ($Execute) { $argsList += '--execute' }", self.text)
        self.assertNotIn("$argsList += '--execute'\n", self.text.replace("if ($Execute) { $argsList += '--execute' }", ""))

    def test_child_process_waits_before_reading_logs_and_captures_exit(self):
        start = self.text.index("Start-Process -FilePath $python")
        exit_pos = self.text.index("$exitCode = [int]$process.ExitCode", start)
        stdout_pos = self.text.index("Get-Content -LiteralPath $stdoutPath", start)
        stderr_pos = self.text.index("Get-Content -LiteralPath $stderrPath", start)
        self.assertLess(start, exit_pos)
        self.assertLess(exit_pos, stdout_pos)
        self.assertLess(exit_pos, stderr_pos)
        self.assertIn("-Wait -PassThru -RedirectStandardOutput", self.text)

    def test_exact_pursuit_driver_pin_matches_staged_driver_bytes(self):
        actual = hashlib.sha256(DRIVER.read_bytes()).hexdigest()
        match = re.search(r"if \(\$driverSha -ne '([0-9a-f]{64})'\)", self.text)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), actual)
        self.assertEqual(actual, "04dec31bc882c9d48ff0a47751a6dfb726b8160374eb552c04158dca9536b6ca")
        self.assertNotIn("7164a83c882116081cda720b37c47107e9145ad2b918b759470b06c5eb3d5522", self.text)

    def test_exact_style_guides_v23_through_v31_remain_pinned(self):
        for value in (
            "C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261114_V23.md",
            "1900b8a06f52156ff18790adb44ef82268c386e2633d2b31237ebc705208c3a5",
            "C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261115_V27.md",
            "93b83ec7c5a640235edc3d70e877088896babe9d6d3b1fc3ed224fe0b6b07f43",
            "C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261115_V28.md",
            "24d9e24ac09a7a8a58445838525a306fc3f3fb8bb31f9dfa5ac7265ed3b71239",
            "C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261115_V29.md",
            "76d9187f7d8c9b44ed940f18fd242f2205e6caf357c8b7dc19756fa1cf8a0c0a",
            "C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261115_V30.md",
            "57d653890535849c7a1d55733c29b1f7fe574010a8cdb18b8d2fd86565b50c83",
            "C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261115_V31.md",
            "e856e3d2385aab67b6fcfb4f6cc05e013b2792e02ae3058e97172a9fd72edbac",
        ):
            self.assertIn(value, self.text)
        self.assertIn("--require-v31-guide", self.text)

    def test_wrapper_recovers_t1_without_rerender_and_executes_only_t2_to_t5(self):
        self.assertIn("PURSUIT_T1_RECOVERY=EXISTING_RECEIPT_AND_MEDIA_AUDITED_NO_RERENDER", self.text)
        self.assertIn("PURSUIT_T2_TO_T5=EXECUTION_SCOPE", self.text)
        self.assertIn("if ($exitCode -ne 0) { throw", self.text)
        self.assertIn("PRODUCTION_DISPATCH=FALSE", self.text)
        self.assertIn("RELEASE_AUTHORITY=NONE", self.text)

    def test_installer_captures_native_python_streams_and_checks_v4_preimages(self):
        installer = INSTALLER.read_text(encoding="ascii")
        self.assertIn("Start-Process -FilePath $FilePath", installer)
        self.assertIn("-RedirectStandardOutput $StdoutPath", installer)
        self.assertIn("-RedirectStandardError $StderrPath", installer)
        self.assertIn("$exitCode = [int]$process.ExitCode", installer)
        self.assertNotIn("& $python $stageTest1 2>&1", installer)
        installer_manifest = json.loads((INSTALLER.parent / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
        preimages = {op.get("preimage_sha256") for op in installer_manifest["operations"] if op["operation"] == "REPLACE"}
        self.assertEqual(len(preimages), 4)
        for digest in (
            "7164a83c882116081cda720b37c47107e9145ad2b918b759470b06c5eb3d5522",
            "32a06a0438d7f237ba4b33c9eded7208d8e86dc05b9dbcd46c2880a547c593da",
            "947b37c9b34ef66ff87b242c3b3adf1330b2bf2aa707a6d4caf4e7f5e06e21e1",
            "98b1e1c0b578dc60c741783c1840e5bd4654d99b445fa49c981348f60c269ed6",
        ):
            self.assertIn(digest, preimages)

    def test_installer_enforces_35_pins_frozen_manifest_and_prepare_only(self):
        installer = INSTALLER.read_text(encoding="ascii")
        for value in (
            "SOURCE_PIN_COUNT_EXPECTED=35", "35/35", "FROZEN_C11C_MANIFEST_POST_PIN_MISMATCH",
            "PASS_PREPARE_ONLY_NO_RENDER", "PURSUIT_BATCH_EXECUTION=NOT_STARTED_PREPARE_ONLY",
            "renderer_invoked", "godot_invoked", "ffmpeg_invoked", "production_media_created", "production_dispatch",
            "Invoke-C11EAtomicReplace", "TRANSACTION_STARTED", "ROLLBACK",
        ):
            self.assertIn(value, installer)
        self.assertNotIn("git status", installer.lower())
        self.assertNotIn("git rev-parse", installer.lower())


    def test_installer_resolves_and_dotsources_atomic_helper_from_payload_layout(self):
        installer = INSTALLER.read_text(encoding="ascii")
        support = "Join-Path $stageRoot 'payload\\support\\C11E_AtomicFileOps.ps1'"
        atomic_test = "Join-Path $stageRoot 'payload\\support\\TEST_C11E_ATOMIC_FILE_OPS_V1.ps1'"
        self.assertIn(support, installer)
        self.assertIn(atomic_test, installer)
        self.assertIn(". $atomicSupport", installer)
        self.assertIn("Get-Command $requiredFunction -CommandType Function", installer)
        self.assertIn("Write-JsonAtomic $atomicJsonProbe", installer)
        self.assertNotIn("Join-Path $stageRoot 'support\\C11E_AtomicFileOps.ps1'", installer)
        self.assertNotIn("Join-Path $stageRoot 'support\\TEST_C11E_ATOMIC_FILE_OPS_V1.ps1'", installer)
        self.assertLess(installer.index(". $atomicSupport"), installer.index("Write-JsonAtomic $atomicJsonProbe"))

    def test_installer_stages_canonical_fixture_for_test_import_and_project_definition(self):
        installer = INSTALLER.read_text(encoding="ascii")
        self.assertIn("$testFixture = Join-Path $stageProject 'tests\\fixtures\\visual_drill_pursuit_canonical.json'", installer)
        self.assertIn("$definitionFixture = Join-Path $stageProject 'definitions\\visual_drill_pursuit_canonical.json'", installer)
        self.assertIn("Copy-Item -LiteralPath $canonicalFixture -Destination $testFixture -Force", installer)
        self.assertIn("Copy-Item -LiteralPath $canonicalFixture -Destination $definitionFixture -Force", installer)
        self.assertNotIn("Copy-Item -LiteralPath (Join-Path $stageRoot 'INSTALL_C11E_E4C_PURSUIT_BATCH_OVERLAY_V5_3.ps1')", installer)

    def test_installer_rechecks_all_35_source_pins_at_transaction_boundary(self):
        installer = INSTALLER.read_text(encoding="ascii")
        boundary = installer.index("$stage = 'FINAL_PRETRANSACTION_PIN_AND_STYLE_GUIDE_RECHECK'")
        transaction = installer.index("$transactionStarted = $true")
        self.assertLess(boundary, transaction)
        self.assertIn("Assert-SourcePins @($manifest.source_pins) 'PRE_TRANSACTION'", installer)
        self.assertIn("FROZEN_C11C_MANIFEST_PRETRANSACTION_PIN_MISMATCH", installer)
        self.assertIn("FINAL_PRETRANSACTION_STYLE_GUIDES=3/3 PASS", installer)

    def test_v5_3_manifest_records_four_pinned_replacements_and_add_only_docs(self):
        installer_manifest = json.loads((INSTALLER.parent / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
        self.assertEqual(installer_manifest["schema"], "C11E-E4C-PURSUIT-BATCH-OVERLAY-MANIFEST-V5_3")
        self.assertEqual(installer_manifest["package_id"], "C11E_E4C_PURSUIT_BATCH_OVERLAY_V5_3_20261115")
        replacements = {op["destination"]: op for op in installer_manifest["operations"] if op["operation"] == "REPLACE"}
        self.assertEqual(len(replacements), 4)
        self.assertEqual(replacements["tools/c11d/d9/c11e_e4c_pursuit_tier_batch.py"]["preimage_sha256"],
                         "7164a83c882116081cda720b37c47107e9145ad2b918b759470b06c5eb3d5522")
        self.assertEqual(replacements["tests/test_c11e_e4c_pursuit_tier_batch.py"]["preimage_sha256"],
                         "32a06a0438d7f237ba4b33c9eded7208d8e86dc05b9dbcd46c2880a547c593da")
        self.assertEqual(replacements["tools/c11d/d9/RUN_C11E_E4C_PURSUIT_TIERS_1_TO_5_V1.ps1"]["preimage_sha256"],
                         "947b37c9b34ef66ff87b242c3b3adf1330b2bf2aa707a6d4caf4e7f5e06e21e1")
        self.assertEqual(replacements["tests/test_c11e_e4c_pursuit_runner_contract.py"]["preimage_sha256"],
                         "98b1e1c0b578dc60c741783c1840e5bd4654d99b445fa49c981348f60c269ed6")
        self.assertGreaterEqual(sum(1 for op in installer_manifest["operations"] if op["operation"] == "ADD"), 10)


    def test_installer_prevalidates_zip_member_paths_before_extraction(self):
        installer = INSTALLER.read_text(encoding="ascii")
        archive_open = installer.index("[IO.Compression.ZipFile]::OpenRead($zip)")
        expand = installer.index("Expand-Archive -LiteralPath $zip")
        self.assertLess(archive_open, expand)
        for value in (
            "V5_3_UNSAFE_ZIP_MEMBER", "V5_3_DUPLICATE_ZIP_MEMBER",
            "V5_3_REQUIRED_ZIP_MEMBER_MISSING", "$member.Contains('\\')",
            "$member.EndsWith('/')", "V5_3_ZIP_ENTRY_SET_FAIL",
        ):
            self.assertIn(value, installer)

    def test_installer_finishes_and_persists_all_backups_before_transaction(self):
        installer = INSTALLER.read_text(encoding="ascii")
        backup_stage = installer.index("$stage = 'BACKUP_PREPARATION'")
        backup_count = installer.index("if ($backupRecords.Count -ne 4)", backup_stage)
        journal_backup = installer.index("$journal.backups = @($backupRecords)", backup_count)
        final_recheck = installer.index("# Recheck every REPLACE and ADD destination", journal_backup)
        transaction = installer.index("$transactionStarted = $true", final_recheck)
        self.assertLess(backup_stage, backup_count)
        self.assertLess(backup_count, journal_backup)
        self.assertLess(journal_backup, final_recheck)
        self.assertLess(final_recheck, transaction)
        self.assertIn("transaction_started=$false", installer[backup_stage:transaction])
        self.assertIn("V5_3_FINAL_REPLACE_PREIMAGE_DRIFT", installer[final_recheck:transaction])
        self.assertIn("V5_3_FINAL_ADD_DESTINATION_EXISTS", installer[final_recheck:transaction])
        boundary_marker = installer.index("$journal.transaction_started = $true", final_recheck)
        durable_marker = installer.index("Write-JsonAtomic $journalPath $journal", boundary_marker)
        local_flag = installer.index("$transactionStarted = $true", durable_marker)
        rollback_state = installer.index("$operationInFlight = 0", final_recheck)
        self.assertLess(rollback_state, boundary_marker)
        self.assertLess(boundary_marker, durable_marker)
        self.assertLess(durable_marker, local_flag)

    def test_installer_rechecks_each_destination_immediately_before_atomic_operation(self):
        installer = INSTALLER.read_text(encoding="ascii")
        transaction_boundary = installer.index("$stage = 'TRANSACTION_STARTED'")
        transaction_loop = installer.index("foreach ($op in $operations) {", transaction_boundary)
        immediate_replace = installer.index("V5_3_IMMEDIATE_PREIMAGE_DRIFT", transaction_loop)
        immediate_add = installer.index("V5_3_IMMEDIATE_ADD_COLLISION", transaction_loop)
        atomic_replace = installer.index("Invoke-C11EAtomicReplace -SourcePath $temp -DestinationPath $dest", transaction_loop)
        self.assertLess(transaction_loop, immediate_replace)
        self.assertLess(immediate_replace, immediate_add)
        self.assertLess(immediate_add, atomic_replace)
        self.assertIn("$receipt.backup_records = @($backupRecords)", installer)
        self.assertIn("backup_records=@($backupRecords)", installer)


    def test_installer_enforces_exact_staged_python_test_count(self):
        installer = INSTALLER.read_text(encoding="ascii")
        self.assertIn("$testCountMatch = [regex]::Match($tests.Stderr", installer)
        self.assertIn("$expectedTestCount = [int]$manifest.python_tests.total", installer)
        self.assertIn("$expectedTestCount -ne 37", installer)
        self.assertIn("STAGED_PYTHON_TEST_COUNT_MISMATCH", installer)

    def test_installer_requires_existing_destination_parent_directories(self):
        installer = INSTALLER.read_text(encoding="ascii")
        preflight = installer[installer.index("$stage = 'OPERATION_PREIMAGE_PREFLIGHT'"):installer.index("$stage = 'BACKUP_PREPARATION'")]
        transaction = installer[installer.index("$index = 0\n    $operationInFlight"):installer.index("$stage = 'POSTIMAGE_SOURCE_PIN_AND_FROZEN_MANIFEST_AUDIT'")]
        self.assertIn("Test-Path -LiteralPath $destinationParent -PathType Container", preflight)
        self.assertIn("V5_3_DESTINATION_PARENT_MISSING", preflight)
        self.assertNotIn("New-Item -ItemType Directory", transaction)

    def test_installer_scopes_rollback_to_committed_and_in_flight_operations(self):
        installer = INSTALLER.read_text(encoding="ascii")
        self.assertIn("$operationInFlight = $index", installer)
        self.assertIn("$rollbackThrough = [Math]::Max($committedCount,$operationInFlight)", installer)
        self.assertIn("for ($i=$rollbackThrough-1; $i -ge 0; $i--)", installer)
        self.assertIn("$operationInFlight = 0", installer)
        self.assertIn("operationTempInFlight", installer)

    def test_installer_binds_each_replacement_to_its_exact_payload(self):
        installer = INSTALLER.read_text(encoding="ascii")
        self.assertIn("$expectedReplacementPayloads = @{", installer)
        self.assertIn("V5_3_REPLACEMENT_PAYLOAD_BINDING_FAIL", installer)
        self.assertIn("Invoke-C11EAtomicCreate -SourcePath $temp -DestinationPath $dest", installer)


if __name__ == "__main__":
    unittest.main(verbosity=2)
