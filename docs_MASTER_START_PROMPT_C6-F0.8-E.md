# START PROMPT PARA INGENIERO JEFE: FASE C6-F0.8 (VISUAL DRILLS COMPLETADOS)

## 1. CONTEXTO INMEDIATO
Acabamos de finalizar con éxito rotundo (81/81 PASS E2E) el Hito C6-F0.8-E. Este hito se enfocaba en migrar la subfamilia *Visual Drills* (Peripheral Scan, Tracking, Pursuit, Saccade) al nuevo paradigma C6:
1. **Flujos Cosméticos Deterministas:** Se conectaron los Streams 2011, 2012, 2013 y 2014.
2. **Variación Limpia:** Todos los generadores exponen y usan `generate_with_variation()`.
3. **Renderizado Pasivo por Shader:** Toda la lógica pesada visual ocurre en GPU (shaders) y los Nodos 2D solo actúan como inyectores de parámetros y routers (`VisualDrillRenderer.gd`).
4. **Respeto Legacy:** El registro global RNG (`RNGStreamRegistry.gd`) está limpio y soporta tanto las mecánicas del corpus V1/V2 como los nuevos bucles visuales.

## 2. OBJETIVOS ESTRATÉGICOS PARA EL INGENIERO
Al cargar este prompt, te encuentras en un entorno inmaculado donde **el 100% de los tests corren**. Toda la infraestructura visual procedural y reactiva está terminada.

**Opciones principales para tu siguiente movimiento:**
- [A] **Validación de Artefactos Físicos (Exportación E2E):** Lanzar el renderizador batch (`convert_to_gifs.py` o análogo en Godot) para renderizar todas las muestras visuales usando el `MovieMaker` y verificar que los archivos de video/gif generados lucen correctamente y reflejan el determinismo.
- [B] **Mantenimiento y Schemas:** Asegurar que los generadores de schemas JSON o la validación estática de perfiles (`ContentSchemaValidator.gd`) sean conscientes de la familia `visual_drill` y `visual_loop` antes de desplegarlos al autor final.
- [C] **Siguiente Dominio (Mecánicas V2 / Audio / etc.):** Declarar el sistema visual "Production Ready" e iniciar la siguiente fase mayor de arquitectura según el roadmap maestro.

## 3. INSTRUCCIONES INICIALES SUGERIDAS (Para pegar en la consola del LLM)
"Contexto cargado. Estoy viendo el 81/81 PASS y la estabilización del Stream 2011-2014 en el RNG Registry. Muéstrame el roadmap restante o sugiéreme cómo proceder para exportar las demos de los cuatro drills (`peripheral_scan`, `tracking`, `pursuit`, `saccade`) en .avi/.gif de forma batch para validar el render final de la GPU."
