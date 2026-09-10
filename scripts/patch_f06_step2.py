import os
import re

def patch_file(filepath, replacements):
    if not os.path.exists(filepath):
        print(f"[!] Archivo no encontrado: {filepath}")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    for pattern, repl in replacements:
        content = re.sub(pattern, repl, content)
        
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[OK] Parcheado con éxito: {filepath}")
    else:
        print(f"[-] No se requirieron cambios (o ya estaba parcheado) en: {filepath}")

# 1. Corrección de Fixtures (De diccionarios vacíos a arrays)
gd_replacements = [
    (r'"targets"\s*:\s*\{[\s\n]*\}', '"targets": []'),
    (r'"distractors"\s*:\s*\{[\s\n]*\}', '"distractors": []')
]

patch_file("tests/C6F035ContentRuntimeBoundaryTest.gd", gd_replacements)
patch_file("tests/C6F042VisualDrillRuntimeTest.gd", gd_replacements)

# 2. Alineación de marcadores esperados en el Runner Global
run_all_replacements = [
    (r'("C6F06VisualLoopPlaybackTest\.gd"\s*:\s*)"[^"]+"', r'\1"[C6F0_6_PLAYBACK_SUITE] PASS"'),
    (r'("C6F06VisualLoopPhysicalExportTest\.gd"\s*:\s*)"[^"]+"', r'\1"[C6F0_6_PHYSICAL_EXPORT_SUITE] PASS"'),
    (r'("C6F06VisualDrillPlaybackTest\.gd"\s*:\s*)"[^"]+"', r'\1"[C6F0_6_DRILL_PLAYBACK_SUITE] PASS"'),
    (r'("C6F06VisualDrillPhysicalExportTest\.gd"\s*:\s*)"[^"]+"', r'\1"[C6F0_6_DRILL_PHYSICAL_EXPORT_SUITE] PASS"')
]

patch_file("tests/run_all.py", run_all_replacements)
print("=== Proceso de parcheo completado ===")