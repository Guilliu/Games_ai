![Games AI](https://github.com/Guilliu/games_ai/blob/main/games%20ai.jpeg)
# Games AI:

**Games AI** es una librería para el desarrollo de juegos en Python, tanto a nivel estructural como de estrategias.

## <b>Enfoque</b>

En cada juego se construye un objeto capaz de representar las distintas observaciones del mismo durante el trascurso de una partida. Adicionalmente, este objeto debe poder almacenar toda la información relevante correspondiente a una o varias observaciones concretas.

Para crear distintos comportamientos de juego se usan **agentes** capaces de reproducir una cierta táctica o estrategia a la hora de jugar. Se exploran distintas técnicas en búsqueda de las mejores estrategia de juego:
 - **Heurística**: Esta aproximación apoya sus decisiones en maximizar una **función de evaluación** definida de manera experta. Este planteamiento asume que el oponente siempre juega de manera óptima (**minimax algorithm**) e intenta optimizar el tiempo de computación (variación **alpha–beta pruning**).

 - **Aprendizaje por refuerzo**: Ya no existe una función de evaluación que oriente al agente hacías los mejores movimientos... En su lugar, el agente aprende a jugar ajustando un modelo inicial en base a **'recompensas'** que obtiene cuando su desempeño es bueno y **'penalizaciones'** que recibe cuando su rendimiento deja que desear...

## <b>Chess</b>

Recreación del juego del ajedrez: https://en.wikipedia.org/wiki/Chess.

### <b>Estructura</b>
Su estructura es muy sencilla, únicamente cuenta con un script:
-	*modules3.py*

En él, tenemos las dos clases principales de este módulo: `obs` y `pieces`. Cada una de ellas hace bla bla bla...

### <b>Ejemplos de uso</b>
Tenemos tres notebooks que pretenden ilustrar los distintos usos de este módulo:

- En `01 playground` se muestra como está construido el juego y como se pueden hacer acciones.

- En `02 tests` se calculan todas las posibles partidas posibles tras n movimientos y se compara el resultado contra el consenso alcanzado por la mayoría de módulos homologados: https://en.wikipedia.org/wiki/Shannon_number.

- En `03 agents` se juegan partidas entre los distintos tipos de agentes diseñados (en desarrollo).

Se recomienda descargar los notebooks para poder visualizarlos mejor en Jupyter (y así probar a ejecutarlos) ya que en GitHub su visualización es mucho peor, sobre todo la parte de los tableros. Si no, también se pueden descargar las versiones HTML (si se abren directamente en GitHub solo se muestra su código fuente 😥...) o usar https://htmlpreview.github.io/ para visualizar estos HTML sin necesidad de descargarlos.

### <b>Dependencias</b>

Únicamente usa `pandas` y `random.randint`.

## <b>Inspiración</b>

AlphaGo - The Movie: https://www.youtube.com/watch?v=WXuK6gekU1Y.

