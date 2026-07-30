Comencemos hablando un poco sobre la historia de VRP:
- El VRP con Capacidad fue introducido por Dantzig y Ramser en 1959 [1], bajo el nombre de “Problema de Despacho de Camiones”, como una generalización del Problema del Viajante de Comercio (TSP) al incorporar múltiples vehículos
- Desde entonces, se desarrollaron numerosas variantes con el objetivo de modelar problemas reales de distribución con mayor fidelidad.
- Una caracteristica del los problemas VRP es su complejidad:
	- El TSP pertenece a la clase [[NP-HARD]] [2] debido a que el número de rutas posibles crece factorialmente con la cantidad de ciudades (hay (n − 1)!/2 rutas distintas para n ciudades), lo que hace que la búsqueda exhaustiva sea computacionalmente inviable incluso para instancias de tamaño moderado
	- El VRP, que contiene al TSP como caso particular, es también [[NP-HARD]]; las distintas variantes que incorporan restricciones adicionales (capacidad, ventanas de tiempo, múltiples depósitos) extienden aún más esta complejidad.

- Decir que esto es un VRP nos da un modelo — nos dice qué hay que optimizar. Pero no nos dice cómo resolverlo. Y como ya vimos, el VRP es [[NP-HARD]]: no existe un algoritmo que garantice la solución óptima en tiempo razonable para instancias grandes. Por eso la comunidad no converge en un único método, sino en tres familias de estrategias, cada una con un compromiso distinto entre velocidad y calidad de solución:
	- los métodos exactos, como [[MILP]], que garantizan el óptimo al costo de tiempo de cómputo;
	- las heurísticas constructivas, como [[Nearest Neighbor]], rápidas pero sin ninguna garantía;
	- y las metaheurísticas, como Ant Colony Optimization ([[ACO]]), que buscan un punto intermedio entre ambos extremos
	
-  Las distintas variantes que incorporan restricciones adicionales (capacidad, ventanas de tiempo, múltiples depósitos) extienden aún más esta complejidad. Esta característica tiene consecuencias directas: para instancias de tamaño real, los métodos exactos se vuelven computacionalmente inabordables
	- Esto motiva el desarrolo de otras tecnicas como [[Heurísticas y Metaheurísticas]] capaces de obtener soluciones de buena calidad en tiempos razonables.

