# C9-D — Authoring Reproducibility

## Contract

The same `authoring_batch.json` executed twice by the same Godot authoring generator must produce:

- the same generated Runtime V1 file set;
- byte-identical JSON files (`SHA-256` equality);
- semantically equal parsed JSON content.

This gate is intentionally independent of `build_factory.py`: C9-D validates the determinism of the **Authoring → Canonical V2 → Runtime V1** transformation itself.

## Command

```powershell
python.exe .\scripts\c9_d_authoring_reproducibility.py
```

## Evidence required

A successful run ends with:

```text
[C9-D] RESULTADO GLOBAL DE REPRODUCIBILIDAD DE AUTHORING: PASS
```
