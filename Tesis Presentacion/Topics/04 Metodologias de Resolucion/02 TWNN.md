
### Intro 

Este algoritmo, denominado Time Window Nearest Neighbor (TWNN) por mi, porque se basa en NN y tiene en cuenta ventanas de tiempo, no hay muchas vueltas.

Nace de la necesidad de un baseline simple que sirva como referencia para comparar con enfoques de mayor complejidad computacional. No busca optimizar exhaustivamente el costo total, sino construir rápidamente una solución factible que respete todas las restricciones del problema.

Esto es algo que se suele hacer, usar esta algortimo de baseline para poder compararlo con algo. Por ejemplo [17] el problema de los fardos de donde va a sacar un dataset para poder comparar su algoritmo ? Es algo  muy a la medida lo que necesita, entonces lo que hizo fue implementar un algortimo basado en NN para tener un baseline para comparar su algortimo.

La heurística se inspira en una estrategia de planificación humana: priorizar clientes
con mayor urgencia temporal y, una vez iniciada una ruta, seleccionar secuencialmente el cliente factible más cercano. 
Basicamente lo podemos ver como un greedy que tiene dos fases:
1. asignar clientes a transportistas (clustering)
2. construccion de rutas para cada transportista

### Implementacion 
1. **Asignacion**
	1. Ordenamos a los clientes por el centro de su ventana temporal $(e_i + l_i)/2$ 
	2. Segun este orden va asignando los clientes a los transportistas que minimiza el tiempo de inicio de servicio: $max(si , ei)$
		1. considerando únicamente aquellos vehículos para los cuales dicho tiempo es factible (es decir, $max(si , ei ) ≤ li$ )
		2. y que aún cuenten con capacidad disponible
	3. Si ningún vehículo puede atender a un cliente respetando su ventana de tiempo, la instancia se declara infactible
		1. Por esto decimos que no es inteligente 
	4. Finalizamos con una asignación cliente-vehículo que determina qué clientes serán atendidos por cada vehículo
2. **Construcción de rutas**
	1. Se construye la ruta de cada vehículo. Partiendo desde su depósito de origen, se selecciona iterativamente el cliente aún no visitado con menor tiempo de viaje desde el nodo actual, siempre que su atención sea factible dentro de su ventana de tiempo
	2. Este proceso se repite hasta que todos los clientes asignados al vehículo han sido visitados
	3. La ruta se cierra dirigiéndose al nodo de retorno correspondiente