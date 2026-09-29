extends SceneTree

## C11-A.1 canonical producer routing contract.
## Historical A1 manifest semantics are preserved through an explicit adapter.

var failures: Array[String] = []

func _initialize() -> void:
    var source := FileAccess.get_file_as_string("res://tools/qa/c11/run_c11a1_challenge_bulk_qa.ps1")
    _assert(source.find("tools/prototypes/c11c_bulk/run_c11c_challenge_production.ps1") >= 0, "A1 must route to canonical Challenge producer.")
    _assert(source.find("function Invoke-C11A1CanonicalProducer") >= 0, "Canonical producer helper missing.")
    _assert(source.find("-DeliveryProfile', 'MASTER_1080'") >= 0, "A1 must retain MASTER_1080 historical envelope.")
    _assert(source.find("-KeepAvi") >= 0, "A1 must retain source AVI evidence.")
    _assert(source.find("function Write-C11A1CompatibilityManifest") >= 0, "A1 compatibility manifest adapter missing.")
    _assert(source.find("C11-A.1-CANONICAL-PRODUCER-ADAPTER-V1") >= 0, "Adapter schema missing.")
    _assert(source.find("artifacts = [ordered]@{") >= 0, "Historical artifacts wrapper missing.")
    _assert(source.find("final_video") >= 0 and source.find("raw_video") >= 0, "Historical final/raw video artifact fields missing.")
    _assert(source.find("function Read-C11A1TelemetryFromLog") >= 0, "Canonical producer telemetry reader missing.")
    _assert(source.find("function Resolve-C11A1FactoryArtifact") >= 0, "A1 compatibility artifact resolver missing.")
    _assert(source.find("buildFactoryBytes") >= 0, "Legacy build_factory state guard missing.")
    _assert(source.find("producer_exit_code = $null") >= 0, "A1 run record must predeclare producer_exit_code for StrictMode updates.")
    _assert(source.find("canonical_producer_manifest = $null") >= 0, "A1 run record must predeclare canonical_producer_manifest for StrictMode updates.")
    _assert(source.find("Invoke-C11A1FactoryIsolated") < 0, "Obsolete factory invocation must not return.")
    _assert(source.find("-BuildFactory") < 0, "Obsolete build_factory argument binding must not return.")
    _assert(source.find("[int64]$SingleSeed = 0") >= 0, "Single-run seed parameter missing.")
    _assert(source.find("$singleMode =") >= 0 and source.find("if ($singleMode)") >= 0, "Single-run mode branch missing.")
    _assert(source.find("$seedCases = @([pscustomobject]@{ Label = ('SINGLE_' + [string]$SingleSeed)") >= 0, "Single-run seed injection missing.")

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
