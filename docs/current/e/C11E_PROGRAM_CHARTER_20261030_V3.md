# C11-E — carta fundacional del programa

**Versión:** V3 · **Fecha:** 2026-10-30 · **Estado:** fundamento de ingeniería aprobado para iniciar E0 en la conversación; sujeto a verificación del checkout.

## 1. Misión

Construir una única ruta de producción bajo demanda, utilizable desde GUI y CLI, que tome una solicitud canónica (familia, selector, semillas, perfiles y editorial), ejecute la mecánica/generación C correspondiente, introduzca la capa editorial E en el consumidor visual real, incorpore música cuando corresponda y entregue MP4 validados con evidencia reproducible.

El objetivo funcional verificable inicial es que el campo editorial `title` de una solicitud modifique píxeles visibles del vídeo generado para un Challenge de prueba, manteniendo inalterada la verdad de gameplay, el selector y la semilla de juego. Este primer resultado debe ser un MP4 físico inspeccionable, no un plan JSON ni una previsualización declarativa.

## 2. Decisión de arquitectura

E no reconstruye un motor de juego. E integra y completa una cadena que ya existe parcialmente:

- **C11-C:** mecánicas, definiciones, generación de frames, perfiles y composición visual heredada, Movie Maker, pipeline de encode/validación y producción existente.
- **D (reutilización selectiva):** formularios del Producer, modelo editorial universal, resolución de valores, catálogos/perfiles y motor de música D3. Los artefactos D se reutilizan únicamente después de comprobar contrato, fuente y comportamiento real.
- **E:** servicio único de producción, transporte request→familia, adaptadores editoriales visuales, dispatch físico controlado, mux A/V y recibos E de extremo a extremo.

C11-E es el nombre del workstream de integración. Por instrucción explícita del usuario, el checkout local permanece en la rama Git `main`; E no fuerza una rama dedicada. La ref `c11e-unified-editorial-production` ya existente se conserva sin cambios. La etiqueta C11-E no implica que E sea ya un baseline de producción aceptado.

## 3. Alcance incluido

1. Una API/servicio canónico compartido por GUI y CLI; ambos canales deben producir el mismo plan normalizado y llamar al mismo dispatch.
2. Adaptación editorial por familia: Challenge, Loop y Drill. Se permite compartir infraestructura, pero no se presupone que los tres binders tengan slots o temporización idénticos.
3. Consumidor visual real E que reciba valores editoriales validados y los aplique a modelos/píxeles de la familia adecuada.
4. Conservación explícita de seeds y perfiles, con `request.seed` independiente de `request.music_seed`.
5. Pipeline A/V: generar/seleccionar audio mediante D3, muxear sin alterar el vídeo fuente cuando el flujo existente lo permita, y validar con FFmpeg/FFprobe.
6. Pruebas físicas aisladas, determinismo, regresión del motor C, smoke y matriz de cobertura.
7. Evidencia reproducible: request canónico, hashes, fuente/commit, comandos, stdout/stderr, códigos de salida, outputs y validaciones.

## 4. Fuera de alcance

- Rehacer gameplay, generadores C, RNG de juego, detectores de resultado o stream de frames.
- Redefinir contratos visuales C por preferencias no justificadas por el código.
- Proyectar arbitrariamente `FrameSnapshot.custom_data`, inventar coordenadas de mecánicas o introducir bindings no necesarios para editorial estática.
- Cambiar la semántica de `winning_frame`, `close_calls`, `SimulationResult` o `RenderedFrameStream`.
- Corregir CHALLENGE_008/009 por inferencia: su desfase declarado de 11 s frente a 12 s de suma de fases sigue requiriendo resolución basada en contrato/autoridad.
- Reemplazar, reescribir o modificar el paquete C11-C congelado antes de la aceptación formal E.
- Declarar una release, promoción o baseline aprobado solo por lograr un render de laboratorio.

## 5. Autoridad y separación de programas

La petición explícita del usuario de iniciar E constituye autorización para actualizar el enrutamiento documental en la rama local `main` y ejecutar los gates de ingeniería E especificados. El usuario ha indicado que quiere permanecer en `main`; queda prohibido cambiar ramas o publicar refs sin nueva instrucción explícita. La prueba física se habilita como actividad de ingeniería E aislada, no como autorización para publicar, promover o sustituir C11-C. El primer render no se ejecuta durante E0/E1: E2 autoriza dos renders Challenge aislados para la prueba A/B de `title`; E4 amplía cobertura a Loop y Drill.

Los estados D son históricos y scoped: por ejemplo, `D9.10=PREPARE_ONLY`, `D9.14=BLOCKED`, `D9.17=BLOCKED_NO_GO`, `D10=BLOCKED_FOR_PROMOTION` y los locks de renderer/media/binding permanecen verdaderos para los artefactos y gates D a los que pertenecen. No se copian como locks universales de E ni se cambian retrospectivamente. E define su propio estado de renderer, outputs de test y criterios de autorización.

## 6. Baseline C protegido

El manifiesto vivo de C que debe comprobar E0 es `release/C11C_FREEZE_PACKAGE_MANIFEST.json`:

- SHA-256: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`
- Tamaño: `796318` bytes.

El overlay no altera ese fichero. Nunca se extrae un snapshot ZIP sobre el checkout. No se toca el ZIP congelado ni se actualizan los pines C como efecto colateral de la rama E.

## 7. Invariantes no negociables

- Los cinco módulos de `c11c-suite` se conservan: `c11c-producer`, `c11c-test`, `c11c-catalog`, `c11c-config`, `c11c-maintenance`. No crear `c11d-control` ni un sexto módulo para E.
- GUI y CLI convergen en la misma función de servicio/dispatcher; no mantener dos implementaciones de producción.
- `request.seed` pertenece al dominio de gameplay de C; `request.music_seed` al dominio de música D3. No generar seeds de forma automática ni colapsarlos en un master seed implícito.
- `winning_frame` sigue siendo el ancla temporal del Challenge; `close_calls` sigue siendo contador de episodios.
- La editorial E es input de presentación, nunca input de mecánica.
- Fail closed ante campo desconocido, familia incompatible, perfil ausente/inválido, identidad/hash incorrectos, salida fuera del root aislado o discrepancia de duración.
- Los outputs de prueba usan rutas nuevas aisladas, identificadas por run ID; no sobrescribir el corpus C.
- Cada gate se registra por separado; un test PASS no implica autorización de release.

## 8. Definición inicial de éxito

El primer incremento solo se considera funcional cuando dos valores distintos de `title` producen dos vídeos físicamente generados cuyos frames muestran el texto correspondiente y cuyo gameplay permanece equivalente bajo el mismo input/seed. La comparación debe demostrar visualmente la variación editorial y verificar por separado la invariancia del contenido mecánico, duración, frame count y selector. La mera presencia de `title` en el request, plan, bridge, manifiesto o log no es consumo visual.
