import json
import os

# 1. Crear el archivo del Fractal que falta
fractal_def = {
    "schema_version": "2.0",
    "content_id": "VISUAL_LOOP_FRACTAL_CANONICAL",
    "content_version": "1.0.0",
    "kind": "visual_loop",
    "subtype": "fractal",
    "engine_version": "1.0",
    "authoring_version": "1.0",
    "rng_version": "2.0",
    "seed": 12345,
    "presentation": {"profile_id": "social_default_v1", "coordinate_space": "2d"},
    "assets": {"family_id": "f1"},
    "audio": {"profile_id": "a1", "enabled": False},
    "provenance": {"author": "system", "timestamp_ms": 1000},
    "payload": {
        "domain": "visual_loop",
        "duration": 2.0,
        "fps": 30,
        "frame_count": 60,
        "visual_parameters": {
            "generator": "fractal",
            "speed": 1.0,
            "complexity": 3,
            "layers": [{"blend_mode": "alpha"}]
        }
    }
}

os.makedirs("definitions", exist_ok=True)
with open("definitions/visual_loop_fractal_canonical.json", "w", encoding="utf-8") as f:
    json.dump(fractal_def, f, indent=4)
print("[+] Creado: visual_loop_fractal_canonical.json")

# 2. Parchear los 8 archivos existentes
files_to_patch = [
    "visual_loop_vector_field_canonical.json",
    "visual_loop_particle_flow_canonical.json",
    "visual_loop_kaleidoscope_canonical.json",
    "visual_loop_geometric_canonical.json",
    "visual_drill_tracking_canonical.json",
    "visual_drill_pursuit_canonical.json",
    "visual_drill_saccade_canonical.json",
    "visual_drill_peripheral_scan_canonical.json"
]

for filename in files_to_patch:
    filepath = os.path.join("definitions", filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Inyectar propiedades faltantes del Envelope
        data["seed"] = 12345
        data["rng_version"] = "2.0"
        if "schema_version" not in data:
            data["schema_version"] = "2.0"
            
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"[+] Parcheado: {filename} (añadido seed y rng_version)")
    else:
        print(f"[-] Archivo no encontrado: {filename}")

print("\n[OK] Todas las definiciones canónicas han sido estandarizadas.")