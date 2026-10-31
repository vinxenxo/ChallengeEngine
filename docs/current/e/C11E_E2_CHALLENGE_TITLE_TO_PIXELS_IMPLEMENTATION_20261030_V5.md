# C11-E E2 — implementación Challenge_001 title-to-pixels (V5)

**Estado:** `V4_PACKAGE_READY_WINDOWS_EXECUTION_PENDING`  
**Fecha:** 2026-10-30

## Objetivo

Dos renders aislados de `CHALLENGE_001`. Única diferencia de request: `production_override.title`. `request.seed=193847` y `request.music_seed=840001` permanecen independientes y constantes. Audio permanece desactivado; E3 aborda D3 y mux.

## Camino de datos

1. E1 `prepare_c11e_production_intent()` valida el request compartido GUI/CLI y reutiliza el resolver D9.9.
2. Builder E2 genera los dos requests y sidecars editoriales, preservando provenance, profile, selección y los dominios de seed.
3. Se crea una configuración efectiva clonada de `CHALLENGE_001.json`, con seed explícita y hash idéntico A/B. No se edita la definición C original.
4. `C11EChallenge001E2.tscn` hereda la escena C `Main.tscn`. `C11EChallenge001E2.gd` extiende `GeneradorMaestro.gd`, valida los hashes de sidecar/config/source y añade un `TypographyLabel` E al `UnifiedSocialFrame.HeaderContent`.
5. El campo utiliza el slot separado `header.editorial_title`. No sustituye `hook_text`, `HookComponent`, CTA ni cualquier dato del gameplay o `FrameSnapshot.custom_data`.
6. Godot Movie Maker captura AVI por A/B. FFmpeg entrega `REVIEW_720` 720×1280 a 30 FPS; FFprobe valida la salida sin audio.

## Aceptación pixel

- Source: 540 frames, 540×960, 60 FPS.
- Body `x=0,y=144,w=540,h=816`: 540/540 frames idénticos.
- Title slot `x=24,y=24,w=496,h=104`: 540/540 frames diferentes.
- Resto del Header: strips top/bottom/left/right 540/540 idénticos.
- MP4 entregados: 270/270 frames diferentes; geometría, FPS, codec y audio verificados.
- Se conservan seis PNG de revisión; revisión humana independiente.

## Fallo V3 y corrección V4

V3 fue detenido antes de escribir: el guard de rutas generó un prefijo con dos separadores consecutivos a partir de `TrimEnd('\') + '\'`; la ruta válida acababa en `StartsWith=false`. V4 implementa delimitación usando `DirectorySeparatorChar` (un carácter), normaliza el root con `GetFullPath` y mantiene checks contra rutas rooted, segmentos `..`, symlinks/reparse points y destinos que salen del repo.

V4 fija el checkout exacto `main/a3c7c5d` con padre `bc8330e`, árbol limpio y receipts/source pins E1. No acepta cualquier descendiente. Si el preflight vuelve a fallar, no crea artefactos de producción ni lanza Godot.

## Estado de evidencia

Las 9 pruebas Python E2 y el pair builder se habían superado en copia aislada. No hay todavía evidencia Windows de parse PowerShell, parse GDScript, Godot, AVI/MP4 ni comparaciones pixel. El error V3 no es fallo de render, ya que no existió dispatch.
