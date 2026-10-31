# C11-E — alcance funcional: presentación, editorial y música para las tres familias (V1)

## Resultado de producto

El Producer debe permitir crear desde GUI o CLI un Challenge, Visual Loop o Visual Drill y entregar un MP4 final con: mecánica C intacta, presentación C correcta, valores editoriales D seleccionados por el usuario, banda sonora generada por D3, mux final y provenance verificable. GUI y CLI no pueden mantener rutas de producción distintas.

## Modelo editorial D9.8: utilizar lo habilitado, no lo reservado

Campos habilitados para Challenges, Visual Loops y Visual Drills:
- `title`
- `subtitle`
- `call_to_action`
- `language`

Campos adicionales habilitados solo para Challenges:
- `player_name`
- `challenge_label`

No se habilitan por inferencia `hook`, `preparation_text`, `final_text`, `header_line_1/2`, `footer_line_1/2`, ni flags `show_*`. No se cambia el significado de los slots originales C. Por ejemplo, `title` tiene slot editorial propio y no sustituye `content.hook` ni el CTA C.

D9.8 también ordena la herencia `global → content_type → family → subtype → variant → production_override`, rechazo de campos/selecciones desconocidos y sin fallback silencioso. E conserva esa semántica y ata las capas/resolución a hashes y provenance.

## Reutilización visual por familia

**Challenge:** usar `ChallengePresentationBinder`, `UnifiedSocialFrame`, `PresentationProfile` y la ruta física C. E introduce un contexto/sidecar de presentación tipado, que el adaptador Challenge aplica a slots editoriales propios. No altera `Main.tscn`, la definición C original, el timeline ni `GeneradorMaestro.gd`.

**Visual Loop:** usar el binder Loop y su `render_model`/`C11CVisualEditorialLayer`; preservar familia, grammar/subtype, parámetros y replay determinista. El adaptador E aplica título/subtítulo/CTA/idioma sin cambiar la gramática ni el stream de frames.

**Visual Drill:** usar `VisualDrillPresentationBinder` y la capa editorial visual que ya consume el `render_model`; conservar type y tier explícito, las mecánicas del drill y la identidad de variante.

Los mappings concretos de cada familia deben probarse sobre el modelo/slot real del binder, no asumirse iguales por coincidencia de nombre.

## Música y mux

Reutilizar `tools/c11d/d3/c11d_music_engine_v5.py` y los contratos de perfiles/música D existentes. `request.music_seed` alimenta exclusivamente la generación musical. `request.seed` alimenta exclusivamente el gameplay. El recibo musical registra engine/version, music profile, parámetros permitidos, duración, sample format, sample rate/channels, WAV SHA-256 y relación con el request. FFmpeg muxea el audio en una copia de entrega; FFprobe verifica streams y metadatos. No se vuelve a renderizar gameplay por cambiar únicamente `music_seed`.

## Secuencia de integración

1. E2: Challenge title-to-pixels A/B, sin audio, para aislar la integración editorial visual.
2. E3: mismo Challenge con D3 + FFmpeg mux; demostrar que cambiar solo music seed cambia audio/identidad A/V, pero no los frames de gameplay.
3. E4A/E4B/E4C: un Challenge, un Loop y un Drill reales, cada uno con al menos título/subtítulo/CTA visibles donde corresponda, su perfil de presentación correcto y música D3.
4. E5: replay determinista, independencia de semillas, invariancia de gameplay, regresión de los tres binders y auditoría de medios.
5. E6: Smoke 18; E7: Matrix 101; E8: aceptación formal.

## Contrato visual/delivery heredado

Logical frame 540×960; Header 0–144, Body 144–816, Footer 816–960. REVIEW_720: 720×1280, 30 FPS. No cambiar la geometría heredada para hacer caber campos editoriales sin decisión de diseño y pruebas de safe-area.
