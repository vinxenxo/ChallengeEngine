import os
import sys
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TESTS_DIR = PROJECT_ROOT / "tests"

# Registro explícito y contractual de suites.
# La identidad es el path relativo desde la carpeta 'tests/'.
KNOWN_SUITES = {
    "C6EAssetIntegrityTest.gd": "[C6E_ASSET_INTEGRITY_SUITE] PASS",
    "C6E2BadgeAndFontRegressionTest.gd": "[C6E2_BADGE_FONT_REGRESSION_SUITE] PASS",
    "C6E2ComponentLayoutValidationTest.gd": "[C6E2_COMPONENT_LAYOUT_VALIDATION_SUITE] PASS",
    "C6E2ComponentSystemTest.gd": "[C6E2_COMPONENT_SYSTEM_SUITE] PASS",
    "C6E2CountdownContractTest.gd": "[C6E2_COUNTDOWN_CONTRACT_SUITE] PASS",
    "C6E3PresentationValidationTest.gd": "[C6E3_PRESENTATION_VALIDATION_SUITE] PASS",
    "C6E4WinningHighlightContractTest.gd": "[C6E4_WINNING_HIGHLIGHT_CONTRACT_SUITE] PASS",
    "C6EPresentationProfileIsolationTest.gd": "[C6E_PRESENTATION_PROFILE_ISOLATION_SUITE] PASS",
    "C6F1MigrationEquivalenceTest.gd": "[C6F1_MIGRATION_EQUIVALENCE_SUITE] PASS",
    "C6F2AdapterMetadataBindingTest.gd": "[C6F2_ADAPTER_METADATA_BINDING_SUITE] PASS",
    "C6F2AssetFamilyContractTest.gd": "[C6F2_ASSET_FAMILY_CONTRACT_SUITE] PASS",
    "C6F2AudioProfileContractTest.gd": "[C6F2_AUDIO_PROFILE_CONTRACT_SUITE] PASS",
    "C6F2AuthoringAdapterContractTest.gd": "[C6F2_AUTHORING_ADAPTER_CONTRACT_SUITE] PASS",
    "C6F2AuthoringDeterminismTest.gd": "[C6F2_AUTHORING_DETERMINISM_SUITE] PASS",
    "C6F2AuthoringGeneratorContractTest.gd": "[C6F2_AUTHORING_GENERATOR_CONTRACT_SUITE] PASS",
    "C6F2AuthoringRequestContractTest.gd": "[C6F2_AUTHORING_REQUEST_SUITE] PASS",
    "C6F2DeterminismTest.gd": "[C6F2_DETERMINISM_SUITE] PASS",
    "C6F2DifficultyCorpusTest.gd": "[C6F2_DIFFICULTY_CORPUS_SUITE] PASS",
    "C6F2DifficultyMonotonicityTest.gd": "[C6F2_DIFFICULTY_MONOTONICITY_SUITE] PASS",
    "C6F2LegacyEquivalenceTest.gd": "[C6F2_LEGACY_EQUIVALENCE_SUITE] PASS",
    "C6F2PresentationBindingContractTest.gd": "[C6F2_PRESENTATION_BINDING_CONTRACT_SUITE] PASS",
    "C6F2ProductiveGeneratorTest.gd": "[C6F2_PRODUCTIVE_GENERATOR_SUITE] PASS",
    "C6F2ResolverCorrectnessTest.gd": "[C6F2_RESOLVER_CORRECTNESS_SUITE] PASS",
    "C6F2VideoProfileContractTest.gd": "[C6F2_VIDEO_PROFILE_CONTRACT_SUITE] PASS",
    "C6F3PresentationBindingTest.gd": "[C6F3_PRESENTATION_BINDING_SUITE] PASS",
    "C6F3SimulationOrchestratorTest.gd": "[C6F3_SIMULATION_ORCHESTRATOR_SUITE] PASS",
    "C6F3TimelineBuilderTest.gd": "[C6F3_TIMELINE_BUILDER_SUITE] PASS",
    "C6F4CanonicalV2CatchTest.gd": "[C6F4_CANONICAL_V2_CATCH_SUITE] PASS",
    "C6F4CanonicalV2ChooseTest.gd": "[C6F4_CANONICAL_V2_CHOOSE_SUITE] PASS",
    "C6F4CanonicalV2CountTest.gd": "[C6F4_CANONICAL_V2_COUNT_SUITE] PASS",
    "C6F4CanonicalV2FindTest.gd": "[C6F4_CANONICAL_V2_FIND_SUITE] PASS",
    "C6F4CanonicalV2HitTest.gd": "[C6F4_CANONICAL_V2_HIT_SUITE] PASS",
    "C6F4CanonicalV2ParkingTest.gd": "[C6F4_CANONICAL_V2_PARKING_SUITE] PASS",
    "C6F4CanonicalV2PilotTest.gd": "[C6F4_CANONICAL_V2_PILOT_SUITE] PASS",
    "C6F4EffectiveRuntimeTest.gd": "[C6F4_EFFECTIVE_RUNTIME_SUITE] PASS",
    "C6F4ShadowRuntimeBridgeTest.gd": "[C6F4_SHADOW_RUNTIME_BRIDGE_SUITE] PASS",
    "DeterministicLCGStatelessTest.gd": "[RNG_TEST_SUITE] PASS",
    "ParkingMechanicV2IsolationTest.gd": "[PARKING_V2_ISOLATION_SUITE] PASS",
    "PilotMechanicDDIHardeningTest.gd": "[DDI_R1] PASS",
    "PilotMechanicIsolationTest.gd": "[PILOT_ISOLATION_SUITE] PASS",
    "RNGArchitectureTest.gd": "[RNG_ARCHITECTURE_SUITE] PASS",
    "mechanics/catch/CatchMechanicIsolationTest.gd": "[CATCH_V1_ISOLATION_SUITE] PASS",
    "mechanics/catch/CatchPresentationContractTest.gd": "[CATCH_PRESENTATION_CONTRACT_SUITE] PASS",
    "mechanics/choose/ChooseMechanicIsolationTest.gd": "[CHOOSE_V1_ISOLATION_SUITE] PASS",
    "mechanics/find/FindMechanicIsolationTest.gd": "[FIND_V1_ISOLATION_SUITE] PASS",
    "C6E2StructuralAuditTest.gd": "[C6E2_STRUCTURAL_AUDIT_SUITE] PASS",
    "C6E3RuntimePresentationValidationTest.gd": "[C6E3_RUNTIME_PRESENTATION_SUITE] PASS",
    "mechanics/hit/HitMechanicIsolationTest.gd": "[HIT_V1_ISOLATION_SUITE] PASS",
}

FATAL_PATTERNS = [
    "SCRIPT ERROR:",
    "Parse Error:",
    "Failed to load script",
    "Invalid access",
    "Invalid assignment",
    "Cannot call method",
    "CrashHandlerException",
]

def discover_test_suites():
    discovered = []
    
    for root, _, files in os.walk(str(TESTS_DIR)):
        for file in files:
            if file.endswith("Test.gd") and not file.startswith("."):
                suite_path = Path(root) / file
                rel_path = suite_path.relative_to(TESTS_DIR).as_posix()
                
                if rel_path not in KNOWN_SUITES:
                    print(f"[FATAL] Test no registrado descubierto: {rel_path}.")
                    print("Por seguridad, debes registrar explícitamente su marcador de éxito en KNOWN_SUITES.")
                    sys.exit(1)
                
                pass_marker = KNOWN_SUITES[rel_path]
                discovered.append((rel_path, suite_path, pass_marker))
                
    # Orden determinista garantizado para que el corpus se ejecute siempre igual
    discovered.sort(key=lambda item: item[0])
    return discovered

def run_suite(rel_path: str, suite_path: Path, pass_marker: str) -> bool:
    name = Path(rel_path).name
    print(f"\n[RUNNER] Ejecutando {name} ({rel_path})...")
    
    cmd = ["godot", "--headless", "--path", str(PROJECT_ROOT), "--script", str(suite_path)]
    
    try:
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True, 
            encoding="utf-8", 
            cwd=str(PROJECT_ROOT)
        )
        
        combined_output = []
        fatal_detected = False
        
        # Lectura asíncrona para detectar errores fatales inmediatamente
        for line in process.stdout:
            combined_output.append(line)
            for pattern in FATAL_PATTERNS:
                if pattern in line:
                    print(f"[RUNNER-FAIL] {name}: detectado patrón fatal temprano: {pattern.strip()}")
                    print(f"       Trazado: {line.strip()}")
                    process.kill()
                    fatal_detected = True
                    break
            if fatal_detected:
                break
                
        if fatal_detected:
            return False
            
        process.wait(timeout=60)
        
    except subprocess.TimeoutExpired:
        print(f"[RUNNER-FAIL] Timeout ejecutando {name}.")
        process.kill()
        return False
    except OSError as exc:
        print(f"[RUNNER-FAIL] No se pudo iniciar Godot: {exc}")
        return False

    if process.returncode != 0:
        print(f"[RUNNER-FAIL] {name}: exit code {process.returncode}")
        return False

    full_output = "".join(combined_output)
    if pass_marker not in full_output:
        print(f"[RUNNER-FAIL] {name}: falta marcador de éxito '{pass_marker}'.")
        return False

    print(f"[RUNNER-PASS] {name} -> OK")
    return True

def main() -> None:
    print("=== PYTHON TEST RUNNER — ALL CORPUS ===")
    
    suites = discover_test_suites()
    if not suites:
        print("[BATCH-RUNNER] No se encontraron suites válidas (*Test.gd).")
        sys.exit(1)

    results = []
    for rel_path, suite_path, pass_marker in suites:
        passed = run_suite(rel_path, suite_path, pass_marker)
        results.append((rel_path, passed))

    failed = [rel_path for rel_path, passed in results if not passed]

    if failed:
        print(f"\n[BATCH-RUNNER] FAIL — {len(failed)} suite(s) fallaron.")
        for rel_path in failed:
            print(f"  - {rel_path}")
        sys.exit(1)

    print(f"\n[BATCH-RUNNER] PASS — {len(results)} suite(s) superaron la auditoría E2E.")
    sys.exit(0)

if __name__ == "__main__":
    main()