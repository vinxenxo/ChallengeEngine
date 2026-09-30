extends SceneTree

## C11-C 2.19.12 — real parallel review worker isolation contract.
## This is a source-level contract: Workers>1 must use private worker roots,
## and the scheduler must not be replaced by a global mutex or serial fallback.

var _failures: int = 0

func _assert(condition: bool, message: String) -> void:
    if not condition:
        push_error("ASSERT FAILED: " + message)
        _failures += 1

func _read(path: String) -> String:
    var file := FileAccess.open(path, FileAccess.READ)
    _assert(file != null, "Missing readable file: " + path)
    if file == null:
        return ""
    return file.get_as_text()

func _initialize() -> void:
    var batch := _read("res://tools/prototypes/c11c_bulk/run_c11c_art_direction_batch_v4.ps1")
    var helper := _read("res://tools/prototypes/c11c_bulk/C11CReviewWorkerIsolation.ps1")

    _assert(batch.find("New-C11CReviewWorkerPool") >= 0, "Batch must create a private worker pool.")
    _assert(batch.find("$active.Count -lt $Workers") >= 0, "Batch scheduler must admit multiple active workers.")
    _assert(batch.find("Start-Job") >= 0, "Batch must launch independent worker jobs.")
    _assert(batch.find("WorkerRoot") >= 0, "Each job must receive a private WorkerRoot.")
    _assert(batch.find(".c11c_worker_active") >= 0, "Worker activity markers are required for observed concurrency.")
    _assert(batch.find("maxObservedWorkerConcurrency") >= 0, "Batch must measure observed worker concurrency.")
    _assert(batch.find("-lt 2") >= 0, "Acceptance must reject a falsely serialized multi-worker run.")
    _assert(batch.find("Mutex") < 0, "Global mutex serialization is prohibited.")
    _assert(helper.find("C11C_ReviewWorkers_") >= 0, "Worker pool must use a unique temporary pool root.")
    _assert(helper.find("WorkerRoot") >= 0 or helper.find("worker_00") >= 0, "Helper must materialize private worker roots.")
    _assert(helper.find("override.cfg") >= 0, "Worker isolation must exclude global override.cfg state.")
    _assert(helper.find("Initialize-C11CReviewWorkerClassCache") >= 0, "Worker pool must use explicit class-cache initialization.")
    _assert(helper.find("not launch the editor inside a temporary worker project") >= 0, "Worker class-cache bootstrap must avoid repeated editor startup per worker.")
    _assert(helper.find("source_project_godot_class_cache_then_private_worker_clone") >= 0, "Worker bootstrap mode must clone a valid source-project cache into private workers.")

    if _failures == 0:
        print("[C11C_PARALLEL_REVIEW_WORKER_ISOLATION_CONTRACT_SUITE] PASS")
        quit(0)
        return
    push_error("[C11C_PARALLEL_REVIEW_WORKER_ISOLATION_CONTRACT_SUITE] FAIL (%d failure(s))" % _failures)
    quit(1)
