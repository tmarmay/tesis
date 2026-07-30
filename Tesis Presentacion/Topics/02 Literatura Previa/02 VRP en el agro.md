Como parte de este trabajo, se hizo una investigacion para saber desde donde partiamos para encarar este problema. Los resultados de la busqueda se pueden dividir en dos categorias:
- Uso de VRP en el agro  (Garcia)
- Uso de  MILP, ACO, NN en el agro (Bakhtiari)

## Explicar que hacen Garcia
- Para que lo aplica
	- Recollecion de fardos, distribuidos por el campo y tiene que depositarlo en el granero/deposito
- Variante VRP
	- ubicacion de cada fardo
	- posicion del depostio
	- capacidad de remolque (ej 15 fardos)
	- cantidad de vehiculos disponibles
- Solver
	- Algortimo genetico
- Objetivo
	- Hacer el planning para recolectarlos
- Contra que compara
	- Ojo del driver = hueristica NN
- Benchsmarks
	- No hay, se los crea el
	
## Explicar que hace Bakhtiari
- Para que lo aplica
	- Dismunuir el tiempo no operativo para alguna tarea (ejL arar, fumigar) que requiera hacer pasadas a todo el campo
	- el sabe como gira la maquina y depende en que pasada esta es el tipo de giro que tiene que hacer a la otra pasada y por ende que tiene que hacer a la otra pasada
- Variante VRP
	- Por atras es un vrp pero no sale tan directa como las otras
	- Depende de la geometrica de los campos
	- Depende el tipo de maquinaria y sus giros
	- Depende de donde empieza la maquina (que pasada)
- Solver
	- ACO (instnacias complejas dura hasta 25m)
- Objetivo
	- Hacer la mejor traza teniendo en cuenta la geometria del campo y los giros que la maquinas puede dar (a eso lo llama b-pattern)
	- Minimiza el tiempo no operativo 
- Contra que compara
	- Lo que haria el driver
- Benchsmarks
	- No hay, se los crea el segun experiencia propia de campos reales y operarios

## Explicar que 
- 
Pero no es un problema para nosotros:
- Basta que entreceremos los ojos y nos abstraigamos. 
- Esto nos permite ver este problema como alguna [[03 Variantes de VRP - Definicion del problema]] y nada mas


¿Hay algún trabajo previo del que podamos partir?
- No, específicamente para lo que buscamos: nadie resolvió antes la asignación óptima vehículo-cliente en el contexto agrícola. Pero si entrecerramos los ojos y nos corremos del dominio, el problema no cambia tanto — es la misma asignación vehículo-cliente que la literatura general de VRP viene estudiando hace décadas, bajo nombres como CVRP, VRPTW o MDVRPTW. Ahí sí hay antecedentes sólidos. No los vamos a usar tal cual — vamos a combinarlos, con ajustes propios del dominio — pero nos dan de dónde partir.