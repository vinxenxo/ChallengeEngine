import os
import json

def audit_repo():
    print("==================================================")
    print("C6-F0.8-F2-A — AUDITORÍA DEL PIPELINE DE EXPORTACIÓN")
    print("==================================================")
    
    keywords = ["movie", "write_movie", "MovieMaker", "MovieWriter", "export", "avi", "png", "frames"]
    matches = {}
    
    for root, dirs, files in os.walk("."):
        # Ignorar directorios .git o de caché de Godot
        if ".git" in root or ".godot" in root or "__pycache__" in root:
            continue
            
        for file in files:
            if file.endswith((".gd", ".py", ".json", ".cfg", ".import")):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        found_keywords = [kw for kw in keywords if kw.lower() in content.lower()]
                        if found_keywords:
                            matches[filepath] = found_keywords
                except Exception as e:
                    pass

    print(f"\n[+] Archivos con referencias al pipeline de exportación/video ({len(matches)} encontrados):")
    for filepath, kw_list in matches.items():
        print(f"    - {filepath} -> Keywords: {kw_list}")

    # Buscar specifically VisualContentPlayer o archivos de reproducción
    player_files = []
    for root, dirs, files in os.walk("."):
        if ".git" in root or ".godot" in root:
            continue
        for file in files:
            if "player" in file.lower() or "renderer" in file.lower() or "export" in file.lower():
                player_files.append(os.path.join(root, file))
                
    print(f"\n[+] Componentes clave de Render/Playback localizados:")
    for pf in player_files:
        print(f"    - {pf}")

if __name__ == "__main__":
    audit_repo()