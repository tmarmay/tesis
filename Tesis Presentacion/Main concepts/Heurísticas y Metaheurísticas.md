La distinción central es: una heurística construye una solución una sola vez con una regla fija; una metaheurística itera muchas construcciones y aprende entre ellas. Vamos al detalle aplicado a tu propio Capítulo 3.

### Heurística (NN / TWNN)

Nearest Neighbor (y tu variante TWNN con ventanas de tiempo) es una regla greedy de construcción:
  1. Parado en un nodo, mirás los candidatos factibles (no visitados, dentro de ventana de tiempo, capacidad disponible).
  2. Elegís siempre el más cercano/conveniente según un criterio fijo.
  3. Repetís hasta terminar la ruta.

Características clave:
  - Un solo pase, un solo resultado. Corrés el algoritmo una vez y obtenés una solución. No hay "vuelta atrás" ni refinamiento posterior.
  - Determinística (dado el mismo input, mismo output — salvo empates).
  - Miope: decide en base a información local e inmediata ("¿cuál es el mejor paso ahora?"), sin considerar el impacto de esa elección en el resto de la ruta. Por eso puede quedar atrapada en decisiones que parecen buenas al principio pero son malas al final (el clásico problema de NN: dejar un cliente lejano aislado para el final).
  - Sin mecanismo de escape: no tiene forma de decir "esta solución no es tan buena, probemos otra cosa". Lo que construye, construye.
  - Por eso es tu baseline: rápida, simple, pero de calidad limitada (tu resumen dice que ACO logra costos 4 veces menores).

### Metaheurística (ACO)

ACO no es una regla fija, es un marco de búsqueda iterativo y estocástico que corre muchas construcciones y usa la experiencia acumulada para mejorar las siguientes:
  1. En cada iteración, varias hormigas (agentes) construyen soluciones completas, cada una tomando decisiones probabilísticas (no determinísticas) ponderadas por dos factores: feromona $\tau_{ij}$ (qué tan buena resultó esa arista en el pasado) y heurística $\eta_{ij}$ (qué tan atractiva es a priori, típicamente $1/d_{ij}$ — de hecho, notá que este término heurístico es conceptualmente el mismo criterio goloso que usa NN).
  2. Al final de la iteración, se actualizan las feromonas: las aristas de las mejores rutas se refuerzan, y todas se evaporan un poco (para no converger prematuramente a una única solución).
  3. Se repite el proceso durante muchas iteraciones, y la calidad de las soluciones mejora progresivamente porque el sistema "aprende" qué aristas suelen formar parte de buenas rutas.

  Características clave:
  - Múltiples pasadas con memoria entre ellas (la matriz de feromonas es el mecanismo de memoria/aprendizaje).
  - Estocástica: corridas distintas pueden dar soluciones distintas.
  - Balance exploración/explotación: explota lo que ya sabe que funciona (feromona alta) pero sigue explorando otras opciones (por la componente probabilística + evaporación), lo que le permite escapar de óptimos locales que atraparían a una heurística pura.
  - No garantiza el óptimo, pero típicamente converge a soluciones mucho mejores que una heurística de un solo paso, a costa de más tiempo de cómputo.

### La relación entre ambas (el punto que las conecta)

  Una heurística greedy como NN puede pensarse como el caso degenerado de una metaheurística: es como correr ACO con una sola hormiga, una sola iteración, sin feromonas (o feromona uniforme) y sin componente probabilística — solo el término heurístico $\eta$. De hecho, en tu implementación de ACO, el término heurístico probablemente es casi idéntico al criterio
  que usa TWNN (distancia/tiempo), pero envuelto en un proceso iterativo con aprendizaje que la heurística pura no tiene.

  Esto también explica el resultado de tu tesis: TWNN es rapidísima porque no itera nada, MILP es exacta pero carísima porque explora todo el espacio (o lo acota con branch & bound), y ACO queda en el medio — itera y aprende (mejor que NN) pero sin garantía de optimalidad ni el costo de explorar exhaustivamente (más barata que MILP)