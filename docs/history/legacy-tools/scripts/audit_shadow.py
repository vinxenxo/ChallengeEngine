import json
from pathlib import Path

def run_shadow_audit(c6_dir_str: str, c7_dir_str: str) -> None:
    c6_dir = Path(c6_dir_str).resolve()
    c7_dir = Path(c7_dir_str).resolve()

    if not c6_dir.exists() or not c7_dir.exists():
        print("Directorios de salida C6 u output_c7 no encontrados.")
        return

    challenges = [f"CHALLENGE_{i:03d}" for i in range(1, 10)]
    mismatches = 0

    fields_to_check = [
        "rng_version",
        "initial_seed",
        "final_seed",
        "seed_used",
        "attempts",
        "close_calls",
        "hook_frames",
        "game_frames",
        "reveal_frames",
        "cta_frames",
        "total_frames",
        "winning_frame",
        "winning_frame_game",
        "winning_frame_in_valid_window",
        "winning_time",
        "winning_time_game",
        "score",
        "minimum_distance",
    ]

    print(f"Iniciando auditoría de sombra ampliada C6 ({c6_dir}) vs C7 ({c7_dir})...\n")

    for ch_id in challenges:
        c6_manifest_path = c6_dir / ch_id / f"{ch_id}_manifest.json"
        c7_manifest_path = c7_dir / ch_id / f"{ch_id}_manifest.json"

        if not c6_manifest_path.is_file() or not c7_manifest_path.is_file():
            print(f"[{ch_id}] Faltan manifiestos para comparación cruzada.")
            mismatches += 1
            continue

        c6_data = json.loads(c6_manifest_path.read_text(encoding="utf-8"))
        c7_data = json.loads(c7_manifest_path.read_text(encoding="utf-8"))

        c6_tel = c6_data.get("telemetry", {})
        c7_tel = c7_data.get("telemetry", {})

        challenge_mismatch = False
        for field in fields_to_check:
            val_c6 = c6_tel.get(field)
            val_c7 = c7_tel.get(field)
            if val_c6 != val_c7:
                print(f"[{ch_id}] Discrepancia en '{field}': C6={val_c6} vs C7={val_c7}")
                challenge_mismatch = True

        if challenge_mismatch:
            mismatches += 1
        else:
            print(f"[{ch_id}] SHADOW MATCH OK — 100% Invarianza Determinista")

    print(f"\nAuditoría ampliada finalizada. Discrepancias encontradas: {mismatches}/9")

if __name__ == "__main__":
    run_shadow_audit("./output", "./output_c7")