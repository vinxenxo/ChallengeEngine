extends SceneTree

## C11-A.1 factory isolation contract.
## Source-level guard for the historical challenge qualification runner.
## The factory must execute isolated from any project-local C11-C override.cfg.

var failures: Array[String] = []

func _initialize() -> void:
    var path := "res://tools/qa/c11/run_c11a1_challenge_bulk_qa.ps1"
    var source := FileAccess.get_file_as_string(path)
    _assert(source.find("function Invoke-C11A1FactoryIsolated") >= 0, "C11-A.1 runner must define the isolation helper.")
    _assert(source.find("Join-Path $WorkingDirectory 'override.cfg'") >= 0, "C11-A.1 runner must isolate the historical factory process.")
    _assert(source.find("Copy-Item -LiteralPath $overridePath -Destination $backupPath -Force") >= 0, "C11-A.1 runner must quarantine a pre-existing root override.cfg.")
    _assert(source.find("Remove-Item -LiteralPath $overridePath -Force") >= 0, "C11-A.1 runner must remove a leaked override.cfg after the factory run.")
    _assert(source.find("Copy-Item -LiteralPath $backupPath -Destination $overridePath -Force") >= 0, "C11-A.1 runner must restore the pre-existing override.cfg byte-for-byte after the factory run.")
    _assert(source.find("$proc = Invoke-C11A1FactoryIsolated") >= 0, "C11-A.1 runner must invoke the isolation helper for each factory run.")
    _assert(source.find("--config', $ConfigPath") >= 0, "C11-A.1 isolation helper must preserve the explicit factory config argument.")

    if failures.is_empty():
        print("[C11A1_FACTORY_ISOLATION_CONTRACT_SUITE] PASS")
        quit(0)
        return
    for failure in failures:
        push_error(failure)
    print("[C11A1_FACTORY_ISOLATION_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
    quit(1)

func _assert(condition: bool, message: String) -> void:
    if not condition:
        failures.append(message)
