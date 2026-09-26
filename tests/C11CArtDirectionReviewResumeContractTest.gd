extends SceneTree

## C11-C 2.16.3 — extraordinary art-direction review runner contract.
var failures: Array[String] = []

func _initialize() -> void:
    var script_path: String = "res://tools/prototypes/c11c_bulk/run_c11c_art_direction_review_v3.ps1"
    var script := FileAccess.get_file_as_string(script_path)
    _assert(script.find("[ValidateRange(1,7)][int]$Workers=7") >= 0, "Art-direction review V5 must default to seven workers.")
    _assert(script.find("[switch]$Resume") >= 0, "Art-direction review V5 must expose resumable execution.")
    _assert(script.find("if($Reset -and $Resume)") >= 0, "Resume and reset must be mutually exclusive.")
    _assert(script.find("Test-LoopComplete") >= 0, "Resume mode must skip already completed loop artifacts.")
    _assert(script.find("Test-LongformComplete") >= 0, "Resume mode must skip already completed longforms.")
    _assert(script.find("Test-DrillsComplete") >= 0, "Resume mode must skip an already complete drill stage.")
    _assert(script.find("manifest.revision") >= 0, "Resume mode must validate artifact freshness.")
    _assert(script.find("resumeManifest.seeds") >= 0, "Resume mode must recover the original seed set from the existing corpus manifest.")

    _assert(script.find("Seeds = [int[]]$Seeds") >= 0, "Drill seeds must be bound as one typed Int32 array to avoid PowerShell parameter binding errors.")
    _assert(script.find("C11-C-ART-DIRECTION-REVIEW-STATE-V5") >= 0, "Resume must persist a versioned per-item state ledger.")
    _assert(script.find("completed_loops") >= 0 and script.find("completed_longforms") >= 0, "Resume state must persist completed loop and longform items.")
    _assert(script.find("$existingState.seeds") >= 0, "Resume must recover seeds from a partial state file before relying on the final corpus manifest.")
    _assert(script.find("C11C_AUTHORING_OUTPUT_PATH") >= 0, "Review rendering must isolate authoring snapshots per output root and grammar tag.")
    _assert(script.find("-OutputTag") >= 0, "Concurrent Visual Loop review jobs must isolate artifacts with a grammar output tag.")
    _assert(script.find("_seed_${Seed}_${Grammar}_manifest.json") >= 0, "Resume must identify the exact grammar artifact when a family reuses seeds.")
    _assert(script.find("RESUME PLAN") >= 0, "Resume must report the pending item count before starting new workers.")
    _assert(script.find("existingState.revision -eq '2.16.3'") >= 0, "Resume completion state must belong to the current refinement revision.")
    _assert(script.find("completedLoops.ContainsKey($key)") < 0, "Resume must revalidate loop artifacts instead of trusting a stale completion key.")
    _assert(script.find("review root") >= 0, "Review runner must expose a persistent review root for resume.")
    if failures.is_empty():
        print("[C11C_ART_DIRECTION_REVIEW_RESUME_CONTRACT_SUITE] PASS")
        quit(0)
        return
    for failure in failures:
        push_error(failure)
    print("[C11C_ART_DIRECTION_REVIEW_RESUME_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
    quit(1)

func _assert(condition: bool, message: String) -> void:
    if not condition:
        failures.append(message)
