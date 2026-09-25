extends SceneTree

## C11-C 2.13.0 — batch seed spacing contract.
var failures: Array[String] = []

func _initialize() -> void:
    var common := FileAccess.get_file_as_string("res://tools/prototypes/c11c_bulk/C11CProductionBatchCommon.ps1")
    _assert(common.find("stratified_spread_random_v1") >= 0, "Batch common must declare stratified seed strategy.")
    _assert(common.find("function New-C11CUniqueSeeds") >= 0, "Batch common must expose unique seed generation.")
    _assert(common.find("function Assert-C11CSeedSpacing") >= 0, "Batch common must validate minimum seed gaps.")
    _assert(common.find("0.40") >= 0, "Seed strategy must enforce a meaningful fraction of the available bin spacing.")
    var weekly := FileAccess.get_file_as_string("res://tools/prototypes/c11c_bulk/run_c11c_weekly_production_batch.ps1")
    var monthly := FileAccess.get_file_as_string("res://tools/prototypes/c11c_bulk/run_c11c_monthly_production_batch.ps1")
    _assert(weekly.find("New-C11CUniqueSeeds") >= 0, "Weekly batch must use spread seed allocation.")
    _assert(weekly.find("Get-C11CProductionSchedule") >= 0, "Weekly batch must use the canonical production schedule.")
    _assert(monthly.find("Assert-C11CSeedSpacing -Seeds $Seeds") >= 0, "Monthly batch must validate spacing across the whole month.")
    var bulk := FileAccess.get_file_as_string("res://tools/prototypes/c11c_bulk/run_c11c_production_bulk.ps1")
    var bulk25 := FileAccess.get_file_as_string("res://tools/prototypes/c11c_bulk/run_c11c_production_25.ps1")
    _assert(bulk.find("New-C11CUniqueSeeds") >= 0 and bulk.find("Assert-C11CSeedSpacing") >= 0, "Single-family production bulk must use the spread seed policy.")
    _assert(bulk25.find("New-C11CUniqueSeeds") >= 0 and bulk25.find("Assert-C11CSeedSpacing") >= 0, "25-product production batch must use the spread seed policy.")
    if failures.is_empty():
        print("[C11C_SEED_SPREAD_CONTRACT_SUITE] PASS")
        quit(0)
        return
    for f in failures: push_error(f)
    print("[C11C_SEED_SPREAD_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
    quit(1)

func _assert(condition: bool, message: String) -> void:
    if not condition: failures.append(message)
