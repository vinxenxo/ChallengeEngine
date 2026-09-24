# START PROMPT — C11-C ART DIRECTION 2.0

## CONTEXTO

Continuamos el proyecto `ChallengeEngineV01_STATELESS` en una nueva ventana de contexto.

El baseline de ingeniería C11-B está CLOSED / CERTIFIED / FROZEN. No se reabre.

La presentación C11-C está consolidada en **v2.1.4** y ya fue validada en Windows con Godot 4.7.1 hasta el preflight/toolchain y ejecución física de captura.

## ESTADO CANÓNICO

Cinco familias:

- Geometric Waves (`geometric`)
- Fractal Bloom (`fractal`)
- Sacred Symmetry (`kaleidoscope`)
- Living Particles (`particle_flow`)
- Invisible Forces (`vector_field`)

Entrega física:

- 720x1280
- 9:16
- 30 FPS
- baseline temporal de review: 18 s / 540 frames
- audio activado por defecto
- `-NoSound` / `-Silent` = un único MP4 sin audio
- sin `_silent.mp4` abandonado
- social sidecar generado

El toolchain tiene tres zonas independientes:

`prototype` = experimentación  
`review` = análisis  
`production` = productos finales protegidos

## CORPUS DE ENTRADA

La revisión debe utilizar **25 vídeos: 5 variaciones por familia**.

Usar las mismas cinco seeds entre las cinco familias para permitir comparación transversal.

## QUÉ HAY QUE HACER AHORA

No empieces programando.

Primero analiza el corpus completo y formula una Dirección de Arte 2.0 coherente.

La revisión debe responder:

- ¿Qué elementos hacen que una pieza parezca premium?
- ¿Qué elementos siguen pareciendo prototipo?
- ¿Qué familias tienen una identidad más clara y cuáles necesitan mayor diferenciación visual?
- ¿Qué paletas sobreviven realmente a una pantalla móvil?
- ¿Qué proporción debe existir entre arte protagonista y UI editorial?
- ¿La transición del hook aporta personalidad o distrae?
- ¿Qué elementos se perciben como matemáticos y cuáles como decoración genérica?
- ¿Dónde aparece sensación de screensaver?
- ¿Qué variaciones por seed son realmente interesantes?
- ¿Qué rasgos deben convertirse en reglas universales y cuáles deben permanecer específicos de familia?

## RESTRICCIONES

No modificar todavía:

- matemática del engine;
- RNG del engine;
- `SimulationResult`;
- contratos C7/C9;
- C11-B geometry;
- duración variable;
- arquitectura productiva.

No introducir assets externos, imágenes AI ni material pre-renderizado como contenido artístico.

## HISTÓRICO DE CAMBIOS YA CERRADO

Ya están incorporados:

- 720x1280 para social delivery;
- color más vivo para móvil;
- audio ambiental seguro para altavoces móviles;
- Header/Footer con líneas decorativas;
- color editorial basado en paleta;
- eliminación de la identidad repetida `VISUAL LOOP // FAMILY` del Footer;
- Matrix / split-flap hook;
- technobabble con parámetros reales;
- social sidecars;
- MP4 único con/sin audio;
- separación review vs production;
- toolchain PowerShell consolidado;
- validación de entrega 720x1280.

## OBJETIVO DE ESTA VENTANA

Convertir las observaciones del corpus en un **C11-C Art Direction 2.0 Contract** claro, medible y específico por familia.

Orden de trabajo:

1. observación;
2. diagnóstico;
3. principios;
4. contrato DA 2.0;
5. implementación;
6. regeneración;
7. comparación contra baseline v2.1.4.

No saltarse pasos ni volver a entrar en una cadena de microparches de infraestructura.
