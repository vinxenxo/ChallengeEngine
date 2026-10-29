# C11-D Visual Loop Grammar Parameter Instance — Source Check Fix V1

Additive runtime-failure repair for the parameter-instance probe. The failure was caused by a formatting assumption in a D-owned static source check: the frozen C11-C `grammar_modes` array is multiline, but the probe expected a single inline string.

## Files
- `tools/c11d/d9/materialize_visual_loop_grammar_parameter_instance_in_memory.gd` — checks the geometric profile function slice and produces specific source-check diagnostics.
- `tools/c11d/d9/test_d_renderer_visual_loop_grammar_parameter_instance.py` — adds static regression coverage for the real multiline frozen source and the fixed check.
- `docs/current/d/D_RENDERER_VISUAL_LOOP_GRAMMAR_PARAMETER_INSTANCE_CHECKPOINT_V1.md` — records the failure, repair and renderer-agnostic/shared-editorial design direction.

C11-C remains byte-for-byte untouched. No renderer, material, shader execution, native input or media is created. The new test is a static contract regression; the actual Godot 4.7.1 matrix must pass in Windows before runtime closure.

Run from the repository root:

```powershell
python -B .\tools\c11d\d9\test_d_renderer_visual_loop_grammar_parameter_instance.py
python -B .\tools\c11d\d9\d_renderer_visual_loop_grammar_parameter_instance.py --godot $env:C11D_GODOT_EXECUTABLE --timeout 120
```
