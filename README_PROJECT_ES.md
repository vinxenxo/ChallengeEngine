# ChallengeEngineV01 — ¿Qué estamos construyendo?

## La idea, explicada sin tecnicismos

Estamos construyendo una **fábrica automática de vídeos de “Atrápame si puedes”**.

La idea no es crear videojuegos tradicionales. Tampoco queremos que la persona que ve el vídeo controle un personaje ni que tenga que descargar una aplicación.

El vídeo hace todo el trabajo.

En cada vídeo ocurre una pequeña situación de precisión: un coche tiene que aparcar, algo está a punto de chocar, un objeto tiene que caer en el sitio exacto, un símbolo tiene que alinearse… En algún instante concreto existe un **frame ganador**.

La persona que ve el vídeo tiene un único objetivo:

> **Pausarlo justo en el momento correcto.**

Ese pequeño gesto convierte una animación en un reto.

---

## ¿Por qué una fábrica?

Porque la intención no es producir uno o diez vídeos manualmente.

Queremos poder describir un reto con unos pocos datos —por ejemplo, dificultad, duración, tema y semilla— y que el motor pueda construir de forma repetible una nueva situación.

La visión es pasar de:

```text
Idea → hacer un vídeo a mano
```

a:

```text
Idea → configurar un reto → motor → vídeo terminado
```

Eso permite experimentar con muchas situaciones y dificultades sin reconstruir cada animación desde cero.

---

## No estamos haciendo “ports” de juegos retro

Una decisión importante del proyecto es que **no estamos intentando copiar videojuegos antiguos**.

Nos interesa otra cosa: aquella sensación de precisión extrema que tenían algunos juegos clásicos.

El motor no sabe qué son Atari, Activision, Nintendo, River Raid o Pitfall!.

Para el motor sólo existe una pregunta matemática:

> **¿En qué momento exacto ocurre el resultado que queremos que el espectador intente capturar?**

Por eso una estética de 8 bits, por ejemplo, es simplemente una forma de presentar el reto. No cambia las matemáticas que lo generan.

---

## Las grandes familias de retos

Estamos organizando los retos en unas pocas familias matemáticas reutilizables.

### HIT

Algo tiene que alcanzar exactamente un punto.

Ejemplos posibles: una llave entrando en una cerradura, una flecha alcanzando una diana o un balón llegando al punto adecuado.

### CATCH

Hay que conseguir que algo quede dentro de otro elemento o coincida con él.

Por ejemplo, capturar un objeto, introducir algo en una cesta o hacer coincidir una trayectoria con una zona.

### DODGE / SAVE / CONTROL

La clave es atravesar una situación peligrosa y terminar en la posición correcta.

Aquí pertenece nuestro reto de **aparcar el coche**.

### MATCH

Dos cosas tienen que coincidir.

Puede ser una forma, una posición, un patrón, un color u otra combinación definida por el reto.

### FIND

La dificultad consiste en detectar o encontrar algo en el momento adecuado.

### JACKPOT

La situación se construye alrededor de combinaciones que tienen un instante especialmente difícil de capturar.

---

## Y luego están los temas

Una familia matemática puede vestirse de muchas maneras.

Por ejemplo:

```text
garage
sports
fantasy
scifi
retro_8bit_arcade
cyberpunk
```

Un reto de aparcamiento puede tener aspecto de garaje moderno, arcade de 8 bits o ciencia ficción sin convertirse por ello en una nueva familia matemática.

**Las matemáticas generan el reto. El tema genera su aspecto.**

---

## Un ejemplo: “Aparca el coche”

Uno de los primeros retos reales del proyecto consiste en hacer que un coche siga una trayectoria que termina en una plaza.

La trayectoria tiene curvas, una ligera desviación, un posible sobrepaso y pequeñas perturbaciones.

El espectador ve únicamente el resultado visual.

El motor, en cambio, sabe exactamente:

- dónde está el coche en cada frame;
- cuánto se ha separado del objetivo;
- cómo cambia su orientación;
- qué frame es el mejor;
- qué semilla produjo esa situación.

Eso permite generar un reto reproducible y comprobar matemáticamente que sigue siendo el mismo reto cuando se vuelve a producir.

---

## Lo más importante: cada reto tiene una “verdad matemática”

El proyecto separa dos cosas que para el espectador parecen una sola.

**La situación que determina el reto** y **la forma en la que la presentamos**.

Por ejemplo, añadir más partículas, polvo, humo o movimientos de cámara no debería cambiar el frame ganador.

Si cambiar el humo cambia el resultado del reto, significa que hemos mezclado dos cosas que deberían estar separadas.

Gran parte del trabajo que hemos hecho hasta ahora consiste precisamente en blindar esa separación.

---

## ¿En qué punto estamos?

El proyecto ya ha pasado por varias etapas importantes.

### El motor original

Primero se construyó la fábrica básica: definición del reto, simulación, elección del frame ganador, validación temporal y generación del vídeo.

### RNG sin estado

Después sustituimos el sistema de aleatoriedad secuencial por uno en el que cada valor puede identificarse por:

```text
semilla + stream + índice
```

Esto es fundamental porque permite añadir nuevos elementos sin desplazar accidentalmente todos los valores posteriores.

### Streams semánticos

Después dividimos la aleatoriedad en canales con significado.

Por ejemplo:

```text
trayectoria
control
parámetro de esquiva
ruido de dirección
partículas
```

Cada uno tiene su propia identidad.

### PilotMechanic

Creamos después una mecánica de laboratorio extremadamente sencilla para demostrar que el sistema realmente podía aislar la lógica del reto de la presentación.

No es un juego final. Es nuestro tubo de ensayo.

### ParkingMechanicV2

Finalmente hemos llevado esa arquitectura a una mecánica mucho más cercana a producción: el aparcamiento de un coche.

La versión nueva mantiene las matemáticas importantes del sistema anterior, pero utiliza el nuevo modelo de aleatoriedad aislada.

La prueba aislada de esta mecánica ya está superada.

---

## ¿Qué significa “pausa challenge”?

Un vídeo de este tipo suele tener tres partes:

```text
HOOK → GAME → CTA
```

En el perfil actual del motor:

```text
2 s → 7 s → 2 s
```

Es decir, 11 segundos en total a 60 FPS.

Durante el bloque GAME ocurre la acción que contiene el frame ganador.

---

## La visión final

La idea de fondo es sencilla:

> **Crear una máquina capaz de producir retos de precisión en formato vídeo de forma automática, reproducible y escalable.**

No queremos construir un videojuego detrás de cada vídeo.

Queremos construir una **fábrica de pequeñas experiencias imposibles de pausar en el momento correcto**.

Y cada nuevo tema, coche, deporte, criatura, objeto o estética debería poder convertirse en contenido sin tener que reconstruir la arquitectura del motor.

---

## Estado actual

El núcleo determinista está protegido.

La infraestructura de RNG V2.0 está validada.

El laboratorio `PilotMechanic` está validado.

`ParkingMechanicV2` está implementado y validado de forma aislada.

El siguiente paso es conectarlo al flujo general de producción sin tocar el comportamiento histórico de las versiones anteriores.
