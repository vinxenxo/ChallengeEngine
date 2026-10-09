from __future__ import annotations
import ast, json
from pathlib import Path
HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[1]
main=(HERE/"main.py").read_text(encoding="utf-8")
manifest=json.loads((HERE/"BUILD_MANIFEST.json").read_text(encoding="utf-8"))
tree=ast.parse(main)
window=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=="MainWindow")
methods={n.name for n in window.body if isinstance(n,ast.FunctionDef)}
assert "_run_d914_certification_preflight" in methods
assert "D9.14 · REAL-MEDIA CERTIFICATION GATE (BLOCKED)" in main
assert "D9.14 REAL-MEDIA CERTIFICATION PREFLIGHT · NO MEDIA" in main
assert "build_d914_certification_gate(PROJECT)" in main and "validate_d914_certification_gate(gate, PROJECT)" in main
assert manifest["d9_14_real_media_execution"] is False and manifest["d9_14_renderer_activation"] is False
assert manifest["d9_14_media_created"] is False and manifest["d9_14_release_authority"]=="NONE"
# Every private method used directly as a Qt signal callback must exist.
missing=set()
for n in ast.walk(window):
    if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=="connect" and n.args:
        cb=n.args[0]
        if isinstance(cb,ast.Attribute) and isinstance(cb.value,ast.Name) and cb.value.id=="self" and cb.attr.startswith("_") and cb.attr not in methods:
            missing.add(cb.attr)
assert not missing, f"missing Qt callbacks: {sorted(missing)}"
print("C11C_PRODUCER_D9_14_GATE_CONTRACT PASS | UI=BLOCKED visible | no renderer callback | media=false | authority=NONE")
