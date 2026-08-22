import os
import re

# Configuración de rutas
MECHANICS = {
    "HIT_V1": "core/mechanics/hit/HitMechanic.gd",
    "PILOT": "core/mechanics/pilot/PilotMechanic.gd",
    "PARKING_V2": "core/mechanics/parking/ParkingMechanicV2.gd"
}

# Códigos ANSI para colores en terminal
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def extract_method_body(content: str, method_name: str) -> str:
    """Extrae el cuerpo de un método ignorando saltos de línea en la firma."""
    # Busca 'func method_name(...) -> ...:' y captura todo hasta el siguiente 'func ' o el fin de archivo
    pattern = rf"func\s+{method_name}\b[^:]*:\s*(.*?)(?=\nfunc\s|\Z)"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1)
    return ""

def audit_mechanic(name: str, filepath: str) -> bool:
    print(f"\n{YELLOW}=== AUDITANDO: {name} ==={RESET}")
    print(f"File: {filepath}")
    
    if not os.path.exists(filepath):
        print(f"{RED}[FAIL] Archivo no encontrado.{RESET}")
        return False
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    setup_body = extract_method_body(content, "setup")
    prepare_body = extract_method_body(content, "prepare")
    simulate_body = extract_method_body(content, "simulate")

    if not all([setup_body, prepare_body, simulate_body]):
        print(f"{RED}[FATAL] No se pudieron extraer los 3 métodos del ciclo de vida.{RESET}")
        return False

    all_passed = True

    # Axioma 1: Aislamiento Transaccional (Cero llamadas RNG en simulate)
    rng_calls = re.findall(r"(_rng_context|sample_float|DETERMINISTIC_LCG\.sample)", simulate_body)
    if rng_calls:
        print(f"{RED}[FAIL] Axioma 1 (Aislamiento): Llamadas RNG encontradas en simulate(): {set(rng_calls)}{RESET}")
        all_passed = False
    else:
        print(f"{GREEN}[PASS] Axioma 1 (Aislamiento): simulate() puro, cero RNG.{RESET}")

    # Axioma 2: Integridad Temporal (Guardas de tamaño de buffer en simulate)
    # Busca si se está comparando el .size() con total_frames o total_game_frames
    if re.search(r"\.size\(\)\s*!=\s*total_(game_)?frames", simulate_body):
        print(f"{GREEN}[PASS] Axioma 2 (Integridad Temporal): Guarda de tamaño de buffer presente.{RESET}")
    else:
        print(f"{RED}[FAIL] Axioma 2 (Integridad Temporal): Falta validación de tamaño de buffer contra total_frames en simulate().{RESET}")
        all_passed = False

    # Axioma 3: Secuencialidad Estricta (Guardas de setup y prepare)
    if "_is_setup" in simulate_body and "_is_prepared" in simulate_body:
        print(f"{GREEN}[PASS] Axioma 3 (Secuencialidad Estricta): Guardas _is_setup e _is_prepared presentes.{RESET}")
    else:
        print(f"{RED}[FAIL] Axioma 3 (Secuencialidad Estricta): Falta verificación de _is_setup o _is_prepared en simulate().{RESET}")
        all_passed = False

    # Axioma 4: Amnesia por Intento (Limpieza de buffers)
    if ".clear()" in setup_body and ".clear()" in prepare_body:
        print(f"{GREEN}[PASS] Axioma 4 (Amnesia por Intento): .clear() ejecutado en setup() y prepare().{RESET}")
    else:
        print(f"{RED}[FAIL] Axioma 4 (Amnesia por Intento): Falta .clear() en setup() o prepare().{RESET}")
        all_passed = False

    # Axioma 5: Burbujeo de Errores (Manejo de _error_state)
    if "_error_state" in setup_body and "_error_state" in prepare_body:
        print(f"{GREEN}[PASS] Axioma 5 (Burbujeo de Errores): _error_state propagado correctamente.{RESET}")
    else:
        print(f"{RED}[FAIL] Axioma 5 (Burbujeo de Errores): _error_state no manejado en setup() y prepare().{RESET}")
        all_passed = False

    return all_passed

def main():
    print("Iniciando auditoría C3-E (Temporal Lifecycle Hardening)...")
    total = len(MECHANICS)
    passed = 0
    
    for name, path in MECHANICS.items():
        if audit_mechanic(name, path):
            passed += 1

    print("\n========================================")
    if passed == total:
        print(f"{GREEN}AUDITORÍA ESTATICA C3-E SUPERADA ({passed}/{total}){RESET}")
    else:
        print(f"{RED}AUDITORÍA ESTATICA C3-E FALLIDA ({passed}/{total} mecánicas conformes){RESET}")

if __name__ == "__main__":
    main()