
### Intro
Ant Colony Optimization (ACO), u optimización por colonia de hormigas, es una metaheurística inspirada en el comportamiento de las colonias de hormiga. 

Pertenece a la familia de la swarm intelligence (inteligencia de enjambre), un área de la inteligencia artificial y la computación bioinspirada que modela el comportamiento colectivo de grupos de animales, como hormigas, abejas, pájaros o peces, donde individuos simples, sin un líder central, colaboran para resolver problemas complejos de manera eficiente

- Las hormigas exploran aleatoriamente los alrededores del hormiguero. Cuando encuentran comida, regresan dejando un rastro de feromonas por el camino de vuelta, una sustancia que puede ser detectada por otras hormigas.
- Las hormigas pueden seguir varios caminos hacia la comida y luego de vuelta hacia el hormiguero. Se observó que, gracias al refuerzo del rastro de feromonas de las sucesivas hormigas que viajan desde la comida al hormiguero, solo el camino más corto se mantiene en uso, dado que las hormigas prefieren seguir el camino con mayor concentración de feromonas. 
- El refuerzo de las feromonas es autocatalítico (es decir, el propio proceso se refuerza a sí mismo): mientras más corto sea el camino, menor tiempo le tomará a las hormigas ir y volver, reforzando la feromona en el mejor trayecto, mientras que las hormigas en trayectos más largos siguen aún en viaje.
- A su vez, las feromonas se evaporan gradualmente con el tiempo: esto evita que el sistema converja prematuramente hacia una solución subóptima y mantiene la capacidad de exploración del algoritmo.
- Luego de un tiempo, la mayoría de las hormigas termina usando el camino más corto, mientras que una minoría opta por caminos alternativos. El comportamiento de esta minoría es importante, ya que permite explorar nuevos caminos que pueden derivar en mejores rutas no consideradas inicialmente. Este balance entre explotar los caminos conocidos y explorar nuevos constituye un principio central en el diseño de metaheurísticas, conocido como el dilema exploración–explotación.

### Implementacion
El algoritmo se divide en 3 fases, de las cuales las dos primeras las hacen cada hormigas a nivel individual. Mientras que la tercera se realiza de formas colectiva. Antes necesitamos definir algunas variables

La implementación utiliza dos matrices de feromonas que aprenden aspectos complementarios del problema:
- τvc asig , con v ∈ V y c ∈ C: registra la afinidad de asignar el cliente c al vehículo v.
- τijruta , con i, j ∈ N : registra la afinidad de visitar el nodo j inmediatamente después del nodo i dentro de una ruta.

#### Fase 1 — Asignación cliente-vehículo
Mismo objetivo que la fase 1 de TWNN, terminar con una asignacion cliente-vehiculo. 
Cambia la menara de como hace la seleccion, COMPLETAR: SE CREA UNA FUBNCION DE PROBABILIAD QUE DEPENDE DE LAS FEROMONAS (TAO CV) Y DEL ATRACTIVO (DEFINIDO COMO EL INVERSO DE LA DISTANCIA). QUE ADEMAS SE PONDERAN MEDINATE EXPONENTES QUE PODEMOS AJUSTAR PARA DARLE MAS PESO A UNO U OTRO
α pondera la información histórica (feromonas) y β la información heurística

#### Fase 2 — Construcción de rutas
Mismo objetivo que la fase 2 de TWNN, pero ahora como construimos la ruta es un poco mas complejo. 
Con probabilidad $q_0$ se elecciona le proximo cliente a visitar por un $score(i,j)$, de caso contrario, se selecciona el proximo vecino con un metodo de ruleta para incentivar a la exploracion (LERR MAS SOBRE ESTO) [[ACO]].
El score es calculado teniendo en cuenta:
-  τijruta
- etaij (es distinta a la de la fase de asignacion): penaliza el tiempo de viaje tij y la urgencia del cliente j
- µij: ahorro de Clarke-Wright [15]: cuánto se reduce el costo yendo directamente de i a j en lugar de hacer el desvío por el depósito. Un ahorro elevado indica que i y j están lejos del depósito pero cerca entre sí, lo que los convierte en un buen par para visitar de forma consecutiva

### Fase 3 — Actualización de feromonas
- Se selecciona la mejor solución de la iteración y se aplica evaporación a ambas matrices, donde ρ ∈ (0, 1] es la tasa de evaporación: controla qué fracción de la feromona se disipa en cada iteración, regulando así la velocidad con que el algoritmo olvida información histórica.
- Luego se refuerzan las asignaciones y los arcos de la mejor solución con ∆: donde Φ es una constante de escala que determina la magnitud del refuerzo, y λ es el peso de penalización aplicado por cada cliente no atendido en soluciones infactibles

### Post-procesamiento
Observando las diferencias entre las soluciones entre milp y aco, se concluyo que la diferencia entre los costos radica en dos diferentes puntos. 
El primero es con la cantidad de vehiculos que utilizan, aco tendia a utilizar mas vehiculos de los necesarios (respecto a la solucion optima), por eso se implemento:
1. Eliminación de vehículos. Se intenta reasignar los clientes de un vehículo al resto mediante inserción por menor incremento de costo, respetando las ventanas de tiempo. Si la reasignación es factible y no incrementa el costo total, el vehículo es eliminado. El proceso se repite hasta que ningún vehículo pueda eliminarse. El segundo aspecto es que cuando coincidian en la cantidad de vehiculos y en la clusterizacion, el problema era que no proponia la misma ruta. Por lo quer se implemento:
2. Búsqueda local 2-opt intra-ruta. Para cada ruta, se invierten segmentos de forma itera-tiva mientras la nueva secuencia sea factible y reduzca el costo.

Como se nombra en [[Líneas de trabajo futuro]], ayudaria al rendimiento si implementariamos un modulo mas que sea 2-opt-inter-ruta. Permite intercambiar clientes entre rutas distintas, actuaría directamente sobre uno de los dos factores que explican la brecha de ACO con respecto al óptimo

Ademas en este trabajo no se parelelizo el trabajo de las hormigas (tambien mencionado en [[Líneas de trabajo futuro]]), que de hacerlo en los mismo 80 segundos de computo podriamos correr muchas mas iteraciones, lo que podria terminar en mejores soluciones simplemente por tener mas libertad de exploracion