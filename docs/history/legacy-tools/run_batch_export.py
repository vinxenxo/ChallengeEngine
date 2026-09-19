import os
import subprocess
import json
import hashlib
import time

CANONICAL_DEFS = [
    ("visual_loop", "fractal", "definitions/visual_loop_fractal_canonical.json"),
    ("visual_loop", "vector_field", "definitions/visual_loop_vector_field_canonical.json"),
    ("visual_loop", "particle_flow", "definitions/visual_loop_particle_flow_canonical.json"),
    ("visual_loop", "kaleidoscope", "definitions/visual_loop_kaleidoscope_canonical.json"),
    ("visual_loop", "geometric", "definitions/visual_loop_geometric_canonical.json"),
    ("visual_drill", "tracking", "definitions/visual_drill_tracking_canonical.json"),
    ("visual_drill", "pursuit", "definitions/visual_drill_pursuit_canonical.json"),
    ("visual_drill", "saccade", "definitions/visual_drill_saccade_canonical.json"),
    ("visual_drill", "peripheral_scan", "definitions/visual_drill_peripheral_scan_canonical.json")
]

# Matriz de semillas para control de determinismo cruzado:
# Run 0: Seed 12345 (A)
# Run 1: Seed 12345 (B) -> Debe dar hash idéntico a A (A == B)
# Run 2: Seed 54321 (C) -> Debe dar hash diferente (A != C)
SEEDS_MATRIX = [12345, 12345, 54321]

def compute_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in f:
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def run_batch():
    print("==========================================================")
    print("C6-F0.8-F2/F3 — BATCH PHYSICAL EXPORT & DETERMINISM AUDIT")
    print("==========================================================")
    
    output_dir = "output_batch_audit"
    os.makedirs(output_dir, exist_ok=True)
    
    results = []
    hash_tracking = {}
    temp_def_path = "definitions/_temp_batch_def.json"
    
    # Asegurar que existe la escena piloto base
    pilot_tscn_path = "tests/F0_8MovieMakerPilot.tscn"
    if not os.path.exists(pilot_tscn_path):
        print("[-] Error crítico: No se encuentra la escena piloto en 'tests/F0_8MovieMakerPilot.tscn'.")
        return

    run_index = 0
    total_runs = len(CANONICAL_DEFS) * len(SEEDS_MATRIX)
    
    for kind, subtype, base_path in CANONICAL_DEFS:
        with open(base_path, "r", encoding="utf-8") as f:
            base_data = json.load(f)
            
        for seed_idx, seed_val in enumerate(SEEDS_MATRIX):
            run_index += 1
            run_id = f"{kind}_{subtype}_seed{seed_val}_run{seed_idx}"
            print(f"\n[{run_index}/{total_runs}] Exportando: {kind}/{subtype} | Seed: {seed_val} (Run {seed_idx})...")
            
            # Inyectar seed en definición temporal
            mod_data = base_data.copy()
            mod_data["seed"] = seed_val
            
            with open(temp_def_path, "w", encoding="utf-8") as tf:
                json.dump(mod_data, tf, indent=4)
                
            # Sobrescribir temporalmente la escena piloto para que apunte a la definición temporal
            # Nota: El VisualContentPlayer lee content_definition_path. Podemos reescribir la escena o inyectarlo por código.
            # Una forma limpia y directa es regenerar el contenido de la escena .tscn apuntando a temp_def_path.
            pilot_content = f"""[gd_scene load_steps=2 format=3]

[ext_resource type="Script" path="res://core/presentation/rendering/VisualContentPlayer.gd" id="1_player"]

[node name="F0_8MovieMakerPilot" type="Node2D"]

[node name="VisualContentPlayer" type="Node2D" parent="."]
script = ExtResource("1_player")
content_definition_path = "{temp_def_path}"
"""
            with open(pilot_tscn_path, "w", encoding="utf-8") as pf:
                pf.write(pilot_content)
                
            movie_output = os.path.abspath(os.path.join(output_dir, f"{run_id}.avi"))
            if os.path.exists(movie_output):
                os.remove(movie_output)
                
            # Comando Godot con interfaz real (sin --headless, tal como funcionó el piloto)
            cmd = [
                "godot", "--path", ".",
                pilot_tscn_path,
                "--write-movie", movie_output,
                "--fixed-fps", "30",
                "--quit-after", "60"
            ]
            
            start_time = time.time()
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            duration_sec = time.time() - start_time
            
            artifact_exists = os.path.exists(movie_output)
            file_size = os.path.getsize(movie_output) if artifact_exists else 0
            file_hash = compute_sha256(movie_output) if artifact_exists and file_size > 0 else "INVALID"
            
            payload_data = base_data.get("payload", base_data.get("content", {}))
            fps = payload_data.get("fps", 30)
            frame_count = payload_data.get("frame_count", 60)
            
            record = {
                "run_id": run_id,
                "kind": kind,
                "subtype": subtype,
                "seed": seed_val,
                "seed_index": seed_idx,
                "fps": fps,
                "frame_count": frame_count,
                "resolution": "540x960",
                "duration_render_sec": round(duration_sec, 2),
                "artifact_path": movie_output,
                "size_bytes": file_size,
                "sha256": file_hash,
                "exit_code": res.returncode
            }
            results.append(record)
            
            print(f"    -> Exit Code: {res.returncode} | Size: {file_size} bytes | SHA-256: {file_hash[:12]}...")
            
            if seed_idx == 0:
                hash_tracking[(kind, subtype, "A")] = file_hash
            elif seed_idx == 1:
                hash_tracking[(kind, subtype, "B")] = file_hash
            elif seed_idx == 2:
                hash_tracking[(kind, subtype, "C")] = file_hash

    # Limpieza de archivos temporales
    if os.path.exists(temp_def_path):
        os.remove(temp_def_path)
        
    manifest_path = os.path.join(output_dir, "BATCH_EXPORT_MANIFEST.json")
    with open(manifest_path, "w", encoding="utf-8") as mf:
        json.dump(results, mf, indent=4)
        
    print("\n==========================================================")
    print("VERIFICACIÓN DE DETERMINISMO CRUZADO (A == B y A != C):")
    print("==========================================================")
    
    determinism_failures = 0
    for kind, subtype, _ in CANONICAL_DEFS:
        hash_a = hash_tracking.get((kind, subtype, "A"))
        hash_b = hash_tracking.get((kind, subtype, "B"))
        hash_c = hash_tracking.get((kind, subtype, "C"))
        
        match_ab = (hash_a == hash_b) and (hash_a != "INVALID")
        diff_ac = (hash_a != hash_c) and (hash_c != "INVALID")
        
        status_str = "PASS" if (match_ab and diff_ac) else "FAIL"
        if status_str == "FAIL":
            determinism_failures += 1
            
        print(f"[{status_str}] {kind} / {subtype} -> A(12345) == B(12345): {match_ab} | A(12345) != C(54321): {diff_ac}")

    print("\n==========================================================")
    if determinism_failures == 0:
        print("RESULTADO GLOBAL F2/F3: PASS — Matriz de exportación y determinismo físico certificada.")
    else:
        print(f"RESULTADO GLOBAL F2/F3: FAIL — {determinism_failures} discrepancias de determinismo detectadas.")
    print("==========================================================")

if __name__ == "__main__":
    run_batch()