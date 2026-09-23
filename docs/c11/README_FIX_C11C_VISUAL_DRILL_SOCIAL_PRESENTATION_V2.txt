C11-C VISUAL DRILL SOCIAL PRESENTATION V2 — FIX

Root causes fixed:
1. C11CVisualEditorialLayer.gd now preloads the existing canonical
   res://tools/prototypes/c11c_common/C11CEditorialAnimator.gd.
2. The ambiguous Dictionary inference in the editorial Matrix branch is explicitly typed.
3. VisualContentPlayer now fails closed if the shared editorial layer cannot instantiate or mount.
4. The Drill reviewer captures Godot stdout/stderr per render, fails on compile/runtime error signatures,
   and requires the VisualContentPlayer READY marker before encoding/muxing.
5. The reviewer rejects suspiciously small final artifacts.
6. The canonical C11-C editorial animator is included at its existing path; no duplicate core copy is created.

No simulation/RNG/SimulationResult/timeline/C7/C9/C11-B geometry changes.
