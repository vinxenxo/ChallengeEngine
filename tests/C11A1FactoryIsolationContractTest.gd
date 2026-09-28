extends SceneTree

## C11-A.1 regression guard — historical Challenge factory must be isolated
## from any C11-C root override.cfg left by visual production tooling.

var failures: Array[String] = []

func _initialize() -> void:
    var source := FileAccess.get_file_as_string("res://tools/qa/c11/run_c11a1_challenge_bulk_qa.ps1")
    _assert(source.find("function Invoke-C11A1FactoryIsolated") >= 0, "C11-A.1 runner must isolate the historical factory process.")
    _assert(source.find("Quarantined pre-existing override.cfg") >= 0, "C11-A.1 runner must quarantine a pre-existing root override.cfg.")
    _assert(source.find("Removed leaked override.cfg") >= 0, "C11-A.1 runner must remove a leaked override.cfg after the factory run.")
    _assert(source.find("Copy-Item -LiteralPath $backupPath -Destination $overridePath") >= 0, "C11-A.1 runner must restore the pre-existing override.cfg byte-for-byte after the factory run.")
    _assert(source.find("Invoke-C11A1FactoryIsolated") >= 0, "C11-A.1 runner must define the isolation helper.")
    _assert(source.rfind("$proc = Invoke-C11A1FactoryIsolated") >= 0, "C11-A.1 runner must invoke the isolation helper for each factory run.")
    _finish()

func _assert(condition: bool, message: String) -> void:
    if not condition:
        failures.append(message)

func _finish() -> void:
    if failures.is_empty():
        print("[C11A1_FACTORY_ISOLATION_CONTRACT_SUITE] PASS")
        quit(0)
        return
    for failure in failures:
        push_error(failure)
    print("[C11A1_FACTORY_ISOLATION_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
    quit(1)
