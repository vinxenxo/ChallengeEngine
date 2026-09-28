extends SceneTree

## C11-C 2.19.6 - parallel review worker isolation contract.
## Static-only contract: validates worker-pool preparation ordering, genuine worker-local
## capture roots, lock-free Movie Maker capture, and retired c11c-studio isolation.

var _failures: int = 0

func _assert(condition: bool, message: String) -> void:
    if not condition:
        push_error("ASSERT FAILED: " + message)
        _failures += 1

func _read(path: String) -> String:
    var file := FileAccess.open(path, FileAccess.READ)
    if file == null:
        _assert(false, "Missing readable file: " + path)
        return ""
    return file.get_as_text()

func _finish(label: String) -> void:
    if _failures == 0:
        print("[%s] PASS" % label)
    else:
        push_error("[%s] FAIL (%d failure(s))" % [label, _failures])
    quit(0 if _failures == 0 else 1)

func _initialize() -> void:
    var batch := _read("res://tools/prototypes/c11c_bulk/run_c11c_art_direction_batch_v4.ps1")
    var worker := _read("res://tools/prototypes/c11c_bulk/C11CReviewWorkerIsolation.ps1")
    var movie := _read("res://tools/prototypes/c11c_common/C11CMovieCapture.ps1")
    var suite_text := _read("res://c11c-suite/self_test.py")

    var pool_call := batch.find("$workerPool=New-C11CReviewWorkerPool")
    var capture_call := batch.find("Start-LoopReviewJob -FamilyId")
    _assert(pool_call >= 0, "Batch must create the worker pool")
    _assert(capture_call >= 0, "Batch must invoke capture jobs")
    _assert(pool_call < capture_call, "Worker pool must be prepared before the first capture job is launched")

    _assert(batch.find("-WorkerRoot $workerRoot") >= 0, "Each job must receive its worker-local root")
    _assert(batch.find("$workerLauncher=Join-Path $WorkerRoot $LauncherRelative") >= 0, "Launcher must resolve inside the worker root")
    _assert(batch.find("-File $workerLauncher") >= 0, "Worker must invoke PowerShell from inside its worker root")
    _assert(batch.find("[C11-C-WORKER] slot=") >= 0, "Worker runtime marker must identify slot/root")
    _assert(batch.find("powershell.exe @ChildArgs") < 0, "Legacy nested global-project child invocation must be absent")
    _assert(batch.find("Mutex") < 0, "Batch must not use a global mutex")

    _assert(worker.find("Join-Path $sourceRoot 'artifacts'") >= 0, "Worker copy must exclude generated artifacts")
    _assert(worker.find("Join-Path $sourceRoot 'c11c-studio'") >= 0, "Worker copy must exclude retired c11c-studio")
    _assert(worker.find("Join-Path $sourceRoot '.godot'") >= 0, "Worker copy must exclude source .godot state")
    _assert(worker.find("/XF 'override.cfg'") >= 0, "Worker copy must not inherit a shared override.cfg")
    _assert(worker.find("ValidateRange(1,7)") >= 0, "Worker pool must support 1..7 worker slots")
    _assert(worker.find("Initialize-C11CReviewWorkerProject") >= 0, "Worker pool must bootstrap each isolated Godot project")
    _assert(worker.find("'--headless','--editor'") >= 0, "Worker bootstrap must use a headless editor scan")
    _assert(worker.find("'--quit'") >= 0, "Worker bootstrap must terminate after class-cache scan")
    _assert(worker.find("global_script_class_cache.cfg") >= 0, "Worker bootstrap must require the Godot global class cache")
    _assert(worker.find("PresentationProfile") >= 0, "Worker bootstrap must verify PresentationProfile registration")
    _assert(worker.find("GODOT_BIN") >= 0, "Worker bootstrap must honor GODOT_BIN when provided")
    _assert(worker.find("${i}") >= 0, "Worker error interpolation must delimit slot variable before colon")
    _assert(worker.find("$i:") < 0, "Worker helper must not use invalid PowerShell $i: interpolation")

    _assert(movie.find("System.Threading.Mutex") < 0, "Movie capture helper must not serialize project-wide captures")
    _assert(suite_text.find("C11CParallelReviewWorkerIsolationContractTest.gd") >= 0, "Suite self-test must require the new contract")
    _assert(suite_text.find("c11c-studio") >= 0, "Suite self-test must audit retired studio references")

    _finish("C11C_PARALLEL_REVIEW_WORKER_ISOLATION_CONTRACT_SUITE")
